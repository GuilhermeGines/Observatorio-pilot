from typing import Literal
import asyncio
import io
import json
import os
import secrets
import sqlite3
import uuid
import zipfile
from contextlib import asynccontextmanager, closing
from pathlib import Path
from urllib.parse import urlsplit
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from starlette.middleware.trustedhost import TrustedHostMiddleware
from openai import AsyncOpenAI, OpenAIError
from . import ai, db, profiles
from .catalog import COUNTRIES, TOPICS, BY_ID
from .collection import Reader, allowed, base_body, canonical, collect, extract_article, safe_error
from .models import KeyInput, QueryInput, SettingsInput
from .queries import make_result, read_query

TOKEN=secrets.token_urlsafe(32)
JOBS={}
TASKS=set()
COLLECTION_LOCK=asyncio.Lock()

@asynccontextmanager
async def lifespan(app):
    db.init()
    yield
    for task in list(TASKS):
        task.cancel()
    if TASKS:
        await asyncio.gather(*TASKS,return_exceptions=True)
    ai.codex_provider.SERVER.close()

app=FastAPI(title='Observatório',version='0.1.0',lifespan=lifespan,docs_url=None,redoc_url=None)
app.add_middleware(TrustedHostMiddleware,allowed_hosts=['127.0.0.1','localhost','[::1]'])

@app.middleware('http')
async def local_guard(request:Request,call_next):
    if request.url.path.startswith('/api/') and request.method not in {'GET','HEAD','OPTIONS'}:
        origin=request.headers.get('origin')
        valid_origins={'http://127.0.0.1:8765','http://localhost:8765'}
        if os.environ.get('OBS_DEV')=='1':
            valid_origins|={'http://127.0.0.1:5173','http://localhost:5173'}
        if (origin and origin not in valid_origins) or not secrets.compare_digest(request.headers.get('x-observatorio-token',''),TOKEN):
            return JSONResponse({'detail':'Sessão local inválida. Recarregue a página.'},status_code=403)
    response=await call_next(request)
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['Referrer-Policy']='no-referrer'
    response.headers['Cache-Control']='no-store' if request.url.path.startswith('/api/') else 'no-cache'
    response.headers['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; media-src 'self' blob:; connect-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'self'"
    return response

@app.get('/api/session')
def session():
    return {'token':TOKEN,'countries':COUNTRIES,'topics':TOPICS,'version':'0.1.0'}

@app.get('/api/health')
def health():
    return {'status':'ok','local_only':True,'version':'0.1.0'}

@app.get('/api/sources')
def source_list():
    return db.sources()

@app.get('/api/settings')
def settings():
    with db.connect() as connection:
        usage=[dict(r)|{'usage':json.loads(r['usage'])} for r in connection.execute('SELECT * FROM usage ORDER BY id DESC LIMIT 50')]
        counts={table:connection.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0] for table in ['documents','revisions','analyses','audio']}
    return db.setting().model_dump()|{'key_configured':bool(ai.get_key()),'gemini_key_configured':bool(ai.get_key('gemini')),'ai_profiles':profiles.available(),'key_from_environment':bool(os.environ.get('OPENAI_API_KEY')),'data_dir':str(db.DATA),'usage':usage,'counts':counts}

@app.put('/api/settings')
def put_settings(value:SettingsInput):
    if any(s not in BY_ID for s in value.disabled_sources):
        raise HTTPException(422,'Fonte desconhecida.')
    profiles.remember(db.setting())
    db.save_settings(value)
    profiles.remember(value)
    return settings()

@app.put('/api/gemini/key')
def put_gemini_key(value:KeyInput):
    try: ai.set_key(value.key,'gemini')
    except Exception as error:
        raise HTTPException(400,'Não foi possível guardar a chave no cofre seguro do sistema.') from error
    return {'configured':bool(ai.get_key('gemini'))}

@app.delete('/api/gemini/key')
def delete_gemini_key():
    ai.remove_key('gemini')
    return {'configured':bool(ai.get_key('gemini'))}

@app.get('/api/gemini/models')
async def gemini_models():
    key=ai.get_key('gemini')
    if not key: raise HTTPException(400,'Guarde sua chave Gemini primeiro.')
    try:
        async with AsyncOpenAI(api_key=key,base_url='https://generativelanguage.googleapis.com/v1beta/openai/',max_retries=0,timeout=20) as client:
            catalog=await client.models.list()
            return {'models':[m.id for m in catalog.data if 'gemini' in m.id.lower()],
                    'message':'Conexão verificada. A disponibilidade gratuita depende do plano e modelo no AI Studio.'}
    except OpenAIError:
        raise HTTPException(502,'Não foi possível consultar os modelos Gemini. Confira a chave e a rede.')

@app.get('/api/ai-profiles/{identifier}')
def get_profile(identifier:str):
    try: return profiles.configuration(identifier).model_dump()
    except ValueError as error: raise HTTPException(404,str(error))

@app.delete('/api/ai-profiles/{identifier}')
def delete_profile(identifier:str):
    profiles.remove(identifier)
    return settings()

@app.get('/api/providers/usage')
def providers_usage():
    result={p['provider']:{'provider':p['provider'],'input_tokens':0,'output_tokens':0,'partial':False,'calls':0} for p in profiles.available() if p['ready']}
    with db.connect() as connection:
        rows=connection.execute('SELECT usage,model,created_at FROM usage').fetchall()
    for row in rows:
        usage=json.loads(row['usage']);provider=usage.get('provider','openai')
        if provider not in result or usage.get('cache_only'): continue
        item=result[provider];item['calls']+=1
        for field in ['input_tokens','output_tokens']:
            if usage.get(field) is None: item['partial']=True
            else: item[field]+=usage[field]
    if 'gemini' in result:
        from .gemini_quota import current
        result['gemini']['quota']=current(rows)
    return {'providers':list(result.values())}

@app.get('/api/codex/status')
async def codex_status():
    return await ai.codex_provider.status()

@app.post('/api/codex/login')
async def codex_login():
    try: return await ai.codex_provider.login()
    except (ValueError,OSError) as error: raise HTTPException(400,str(error))

@app.get('/api/codex/limits')
async def codex_limits():
    limits=await ai.codex_provider.limits()
    with db.connect() as connection:
        records=[json.loads(r['usage']) for r in connection.execute('SELECT usage FROM usage')]
    records=[r for r in records if r.get('provider')=='codex']
    limits['observatorio_tokens']=sum((r.get('input_tokens') or 0)+(r.get('output_tokens') or 0) for r in records)
    limits['token_records_incomplete']=any(r.get('input_tokens') is None or r.get('output_tokens') is None for r in records)
    return limits

@app.get('/api/ollama/status')
async def ollama_status():
    return await ai.ollama_local.status(db.setting().ollama_model)

@app.get('/api/hardware')
async def hardware_info():
    from .hardware import inspect
    return await inspect()

@app.post('/api/hardware/apply')
async def apply_hardware():
    if ai.API_LOCK.locked():
        raise HTTPException(409,'Aguarde o término da análise ou classificação antes de aplicar o perfil.')
    from tools.install_ollama import restart_owned
    async with ai.API_LOCK:
        try:
            await asyncio.to_thread(restart_owned)
        except Exception as error:
            raise HTTPException(400,str(error))
    return {'message':'Perfil aplicado e Ollama reiniciado. Aceleração será confirmada quando você gerar um resumo.'}

@app.put('/api/key')
def put_key(value:KeyInput):
    try:
        ai.set_key(value.key)
    except Exception:
        raise HTTPException(400,'Não foi possível gravar no cofre seguro do sistema. Nenhuma chave foi salva em arquivo. Use OPENAI_API_KEY no ambiente se necessário.')
    return {'configured':True}

@app.delete('/api/key')
def delete_key():
    try:
        ai.remove_key()
    except Exception:
        raise HTTPException(400,'Não foi possível remover a credencial do cofre.')
    return {'configured':bool(ai.get_key()),'notice':'Chaves fornecidas por variável de ambiente devem ser removidas no ambiente antes de reiniciar.'}

@app.post('/api/key/test')
async def test_key():
    if not ai.get_key():
        raise HTTPException(400,'Nenhuma chave cadastrada.')
    try:
        async with AsyncOpenAI(api_key=ai.get_key(),max_retries=0,timeout=20) as client:
            await client.models.retrieve(db.setting().model)
    except OpenAIError:
        raise HTTPException(400,'Não foi possível validar o acesso ao modelo. Verifique chave, permissões, nome do modelo e conexão. Nenhum texto documental foi enviado.')
    return {'message':'Chave e acesso ao catálogo do modelo validados. A geração e o saldo dependem da conta; nenhum texto foi enviado.'}

async def run_query(query_id,value):
    try:
        from .source_routing import resolve
        JOBS[query_id]={'completed':0,'total':0,'source':'Identificando o tema e selecionando as fontes'}
        await resolve(value)
        coverage=None
        if value.mode=='collect':
            async with COLLECTION_LOCK:
                JOBS[query_id]={'completed':0,'total':len(value._source_route['source_ids']),'source':'Iniciando coleta'}
                def progress(n,total,name):
                    JOBS[query_id]={'completed':n,'total':total,'source':name}
                coverage=await collect(value,query_id,progress)
        discovery=None
        if value.mode=='collect' and db.setting().gemini_search_enabled and value.keyword:
            from .expanded_search import discover
            JOBS[query_id]={'completed':0,'total':len(value.countries),'source':'Busca ampliada com Gemini'}
            try:
                discovery=await discover(value,query_id,lambda n,total,name:JOBS.update({query_id:{'completed':n,'total':total,'source':name}}))
            except Exception as error:
                discovery={'model':'gemini-2.5-flash-lite','verified':[],'leads':[],
                           'notes':['Busca ampliada indisponível: '+(str(error) if isinstance(error,ValueError) else safe_error(error))],'calls':0}
        result=make_result(value,coverage)
        if discovery:
            from .queries import add_discovery
            result=add_discovery(result,discovery)
        with db.connect() as connection:
            connection.execute("UPDATE queries SET status='pronta',result=? WHERE id=?",(db.dumps(result),query_id))
    except asyncio.CancelledError:
        with db.connect() as connection:
            connection.execute("UPDATE queries SET status='interrompida' WHERE id=?",(query_id,))
        raise
    except Exception as error:
        # Still expose the already persisted evidence on a job-level failure.
        result=make_result(value)
        result['limitations'].insert(0,'Coleta interrompida: '+safe_error(error)+' Resultados abaixo são do acervo disponível.')
        with db.connect() as connection:
            connection.execute("UPDATE queries SET status='parcial',result=? WHERE id=?",(db.dumps(result),query_id))
    finally:
        JOBS.pop(query_id,None)

@app.post('/api/queries')
async def create_query(value:QueryInput):
    if len(TASKS)>=3:
        raise HTTPException(429,'Há consultas em andamento. Aguarde a conclusão antes de iniciar outra.')
    query_id=uuid.uuid4().hex
    title=(value.keyword or 'Exploração de fontes')+' · '+', '.join(COUNTRIES[c] for c in value.countries)
    with db.connect() as connection:
        connection.execute('INSERT INTO queries(id,filters,created_at,title,status) VALUES(?,?,?,?,?)',(query_id,value.model_dump_json(),db.now(),title,'coletando'))
    task=asyncio.create_task(run_query(query_id,value))
    TASKS.add(task)
    task.add_done_callback(TASKS.discard)
    return {'id':query_id,'status':'coletando'}

@app.get('/api/queries/{query_id}')
def query_detail(query_id:str):
    value=read_query(query_id)
    if not value:
        raise HTTPException(404,'Consulta não encontrada.')
    value['progress']=JOBS.get(query_id)
    return value

class SaveInput(BaseModel):
    title:str=Field(default='',max_length=200)

@app.post('/api/queries/{query_id}/save')
def save_query(query_id:str,value:SaveInput):
    query=query_detail(query_id)
    if not query['result']:
        raise HTTPException(409,'Aguarde o resultado antes de salvar.')
    with db.connect() as connection:
        connection.execute('UPDATE queries SET saved_at=COALESCE(saved_at,?),title=? WHERE id=?',(db.now(),value.title.strip() or query['title'],query_id))
    return query_detail(query_id)

@app.get('/api/history')
def history(search:str='',country:str='',topic:str='',start:str='',end:str=''):
    with db.connect() as connection:
        rows=[dict(r) for r in connection.execute('SELECT id,title,filters,created_at,saved_at,status FROM queries WHERE saved_at IS NOT NULL ORDER BY saved_at DESC')]
    for row in rows:
        row['filters']=json.loads(row['filters'])
    return [r for r in rows if search.casefold() in r['title'].casefold() and (not country or country in r['filters']['countries']) and (not topic or topic in r['filters']['topics']) and (not start or r['filters']['end']>=start) and (not end or r['filters']['start']<=end)]

@app.delete('/api/history/{query_id}')
def unsave(query_id:str):
    with db.connect() as connection:
        connection.execute('UPDATE queries SET saved_at=NULL WHERE id=?',(query_id,))
    return {'message':'Removida da lista de histórico. Documentos e análises permanecem no acervo.'}

@app.get('/api/queries/{query_id}/analysis-plan')
def analysis_plan(query_id:str,kind:Literal['summary','crossings']='summary',profile_id:str|None=None):
    query=query_detail(query_id)
    if not query['result']:
        raise HTTPException(409,'Consulta ainda sem resultado.')
    try:
        return {k:v for k,v in ai.plan(query,kind,profile_id).items() if k!='payload'}
    except ValueError as error:
        raise HTTPException(400,str(error))

@app.get('/api/queries/{query_id}/analysis-progress')
def analysis_progress(query_id:str):
    query_detail(query_id)
    return ai.ANALYSIS_PROGRESS.get(query_id,{'percent':0,'label':'Aguardando início','state':'idle'})

class AnalyzeInput(BaseModel):
    profile_id:str|None=Field(default=None,max_length=64)
    summary_id:str|None=Field(default=None,max_length=64)
    regenerate:bool=False
    kind:Literal['summary','crossings']='summary'

@app.post('/api/queries/{query_id}/analyze')
async def analyze(query_id:str,value:AnalyzeInput):
    query=query_detail(query_id)
    if not query['result']:
        raise HTTPException(409,'Consulta ainda sem resultado.')
    try:
        return await ai.analyze(query,value.regenerate,kind=value.kind,profile_id=value.profile_id,summary_id=value.summary_id)
    except ValueError as error:
        raise HTTPException(400,str(error))
    except OpenAIError:
        raise HTTPException(502,'Falha na API de IA. O acervo foi preservado. Verifique modelo, saldo, permissão e rede. Uma solicitação recebida pela API pode ter custo; não houve repetição automática.')

@app.get('/api/revisions/{revision_id}')
def revision(revision_id:int):
    row=db.read_revision(revision_id)
    if not row:
        raise HTTPException(404,'Documento não encontrado.')
    with db.connect() as connection:
        row['versions']=[dict(r) for r in connection.execute('SELECT id,created_at,hash FROM revisions WHERE document_id=? ORDER BY id DESC',(row['document_id'],))]
    return row

class ImportInput(BaseModel):
    source_id:str
    url:str=Field(max_length=2000)

@app.post('/api/import')
async def import_url(value:ImportInput):
    source=BY_ID.get(value.source_id)
    if not source or not allowed(value.url,source):
        raise HTTPException(422,'Use uma URL pertencente ao domínio da fonte selecionada.')
    reader=Reader()
    try:
        content,ctype,url=await reader.get(canonical(value.url),source)
        body=extract_article(content,url,source,base_body(source,'Documento importado'),ctype)
        revision_id,_=db.save_document(source['id'],canonical(value.url),body)
        db.log(source['id'],'parcial' if not body.get('published_at') else 'disponivel',{'message':'Leitura de URL específica; não representa cobertura de todo o canal.','url':value.url})
        return {'revision_id':revision_id,'document':body,'notice':'Documento salvo no acervo. Documentos sem data de publicação verificável ficam excluídos dos filtros por data.'}
    except Exception as error:
        raise HTTPException(400,safe_error(error))
    finally:
        await reader.close()

@app.get('/api/queries/{query_id}/export')
def export_query(query_id:str):
    content=db.dumps({'format':'observatorio-query-v1','query':query_detail(query_id)})
    return Response(content,media_type='application/json',headers={'Content-Disposition':f'attachment; filename="consulta-{query_id[:8]}.json"'})

@app.post('/api/backup')
def backup():
    backup_id=uuid.uuid4().hex
    folder=db.DATA/'backups'
    snapshot=folder/(backup_id+'.sqlite3')
    target=folder/(backup_id+'.zip')
    with db.connect() as connection,closing(sqlite3.connect(snapshot)) as dest:
        connection.backup(dest)
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as archive:
        archive.write(snapshot,'observatorio.sqlite3')
        for sub in ['documents','audio','images']:
            for file in (db.DATA/sub).glob('*'):
                if file.is_file():
                    archive.write(file,file.relative_to(db.DATA))
        archive.writestr('manifest.json',db.dumps({'format':'observatorio-backup-v1','created_at':db.now(),'credentials_included':False}))
    snapshot.unlink()
    return {'id':backup_id,'message':'Backup criado com banco, documentos e áudios. Credenciais do cofre e do ambiente não são incluídas.'}

@app.get('/api/backups/{backup_id}')
def backup_download(backup_id:str):
    if len(backup_id)!=32 or any(c not in '0123456789abcdef' for c in backup_id):
        raise HTTPException(404)
    path=db.DATA/'backups'/(backup_id+'.zip')
    if not path.exists():
        raise HTTPException(404)
    return FileResponse(path,media_type='application/zip',filename='observatorio-backup.zip')

@app.get('/api/logs')
def logs(source_id:str=''):
    with db.connect() as connection:
        rows=connection.execute('SELECT * FROM logs WHERE (?="" OR source_id=?) ORDER BY id DESC LIMIT 200',(source_id,source_id)).fetchall()
    return [dict(r)|{'detail':json.loads(r['detail'])} for r in rows]

STATIC=Path(__file__).parent/'static'
if STATIC.exists():
    app.mount('/',StaticFiles(directory=STATIC,html=True),name='interface')
