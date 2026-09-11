"""Ollama somente em loopback, sem credenciais OpenAI ou fallback para nuvem."""
import json
import httpx
from .models import output_model

BASE = 'http://127.0.0.1:11434'

def local_model(name):
    return bool(name) and 'cloud' not in name.lower() and '://' not in name and '..' not in name

async def request(method, path, body=None, timeout=5):
    try:
        async with httpx.AsyncClient(base_url=BASE, trust_env=False, follow_redirects=False,
                                     timeout=httpx.Timeout(timeout, connect=3)) as client:
            response = await client.request(method, path, json=body)
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException:
        raise ValueError('O Ollama excedeu o tempo de espera. Tente menos documentos ou uma resposta menor; nenhuma repetição foi feita.')
    except httpx.HTTPStatusError as error:
        if error.response.status_code == 404:
            raise ValueError('Modelo não encontrado no Ollama. Use Instalar-Qwen.cmd ou confira o nome em Configurações.')
        raise ValueError('O Ollama não conseguiu processar a solicitação. Confira se há memória disponível e se o modelo está instalado.')
    except (httpx.RequestError, ValueError):
        raise ValueError('O Ollama local não respondeu corretamente em 127.0.0.1:11434. Abra o Ollama ou use Iniciar.cmd.')

async def status(model):
    try:
        data = await request('GET', '/api/tags')
        models = [m['name'] for m in data.get('models', []) if local_model(m.get('name','')) and not m.get('remote_host') and not m.get('remote_model')]
        return {'reachable': True, 'installed': model in models, 'models': models,
                'message': 'Ollama conectado; modelo disponível.' if model in models else 'Ollama conectado, mas o modelo selecionado ainda não está instalado.'}
    except ValueError as error:
        return {'reachable': False, 'installed': False, 'models': [], 'message': str(error)}

def messages(payload, prompt, kind='summary'):
    schema = output_model(kind).model_json_schema()
    system = prompt + '\nRetorne somente JSON conforme o formato estruturado solicitado.'
    return schema, system, json.dumps(payload, ensure_ascii=False)

def output_budget(config, payload, prompt):
    _, system, user = messages(payload, prompt, config.get('analysis_kind','summary'))
    remaining = config['ollama_context'] - len((system + user).encode('utf-8')) - 512
    if remaining < 1000:
        raise ValueError('Os documentos ocupam o contexto local. Reduza a entrada para reservar espaço para uma resposta completa.')
    return min(config['max_output_tokens'], remaining)

async def generate(config, payload, prompt, progress=None):
    from .hardware import check_memory
    check_memory(config.get('memory_reserve_gb',3))
    model = config['model']
    if not local_model(model):
        raise ValueError('Escolha um modelo instalado localmente, sem o sufixo cloud.')
    details = await request('POST', '/api/show', {'model': model})
    if details.get('remote_host') or details.get('remote_model'):
        raise ValueError('Este modelo usa a nuvem. Selecione o Qwen instalado localmente.')
    schema, system, user = messages(payload, prompt, config.get('analysis_kind','summary'))
    limit = output_budget(config, payload, prompt)
    body = {
        'model': model, 'messages': [{'role':'system','content':system},{'role':'user','content':user}],
        'format': schema, 'stream': True, 'think': False, 'keep_alive': '5m',
        'options': {'temperature': 0, 'num_ctx': config['ollama_context'],
                    'num_predict': limit,**({'num_gpu':0} if config.get('resource_profile')=='cpu' else {})}}
    if progress:
        progress(5, 'Carregando o modelo e lendo os documentos')
    content = ''
    data = {}
    try:
        async with httpx.AsyncClient(trust_env=False, timeout=httpx.Timeout(600, connect=5)) as client:
            async with client.stream('POST', BASE+'/api/chat', json=body) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    chunk = json.loads(line)
                    if chunk.get('error'):
                        raise ValueError('O Ollama interrompeu a geração. Confira a memória disponível e o registro local.')
                    content += chunk.get('message', {}).get('content', '')
                    if progress and content:
                        # Estimate only: final response length cannot be known in advance.
                        progress(min(90, 10+int(80*len(content)/(3*limit))), 'Gerando o texto · progresso estimado')
                    if chunk.get('done'):
                        data = chunk
                        break
    except httpx.HTTPError:
        raise ValueError('A conexão com o Ollama foi interrompida. Nenhuma repetição automática foi feita.')
    data['message'] = {'content': content}
    if not data.get('done') or data.get('done_reason') == 'length':
        raise ValueError('O modelo atingiu o limite antes de completar a análise. Reduza os documentos ou aumente o limite da resposta.')
    try:
        result = output_model(config.get('analysis_kind','summary')).model_validate_json(data['message']['content'])
    except (KeyError, ValueError):
        raise ValueError('O modelo local não retornou uma análise no formato esperado. Nenhuma análise incompleta foi salva.')
    usage = {'provider':'ollama', 'input_tokens':data.get('prompt_eval_count',0),
             'output_tokens':data.get('eval_count',0), 'duration_seconds':data.get('total_duration',0)/1e9,
             'load_seconds':data.get('load_duration',0)/1e9,'input_seconds':data.get('prompt_eval_duration',0)/1e9,'generation_seconds':data.get('eval_duration',0)/1e9,
             'cost':'Processamento local, sem chamada à OpenAI'}
    return result, usage
