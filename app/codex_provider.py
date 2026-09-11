"""Codex App Server over stdio, with an isolated managed ChatGPT login."""
import asyncio
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import threading
import time
from . import db
from .models import output_model

def strict_output_schema(kind):
    schema=output_model(kind).model_json_schema()
    def normalize(node):
        if isinstance(node,list):
            for value in node: normalize(value)
        elif isinstance(node,dict):
            node.pop('default',None)
            if node.get('type')=='object' or 'properties' in node:
                node['additionalProperties']=False
                node['required']=list(node.get('properties',{}))
            for value in node.values(): normalize(value)
    normalize(schema)
    return schema

def executable():
    path=shutil.which('codex.exe' if os.name=='nt' else 'codex')
    if path and Path(path).suffix.lower() not in {'.cmd','.ps1','.bat'}: return path
    roots=Path(os.environ.get('LOCALAPPDATA',''))/'OpenAI'/'Codex'/'bin'
    candidates=list(roots.glob('*/codex.exe')) if roots.is_dir() else []
    if candidates: return str(max(candidates,key=lambda p:p.stat().st_mtime))
    raise ValueError('Codex não encontrado. Instale o Codex CLI ou o aplicativo Codex e reabra o Observatório.')

class Server:
    def __init__(self):
        self.process=None;self.sequence=0;self.events=[]

    def start(self):
        if self.process and self.process.poll() is None: return
        program=executable()
        self.home=db.ROOT/'runtime'/'observatorio-codex'
        self.cwd=self.home/'workspace';self.cwd.mkdir(parents=True,exist_ok=True)
        env=os.environ.copy()
        env['CODEX_HOME']=str(self.home)
        for name in ['OPENAI_API_KEY','CODEX_API_KEY','OPENAI_BASE_URL']:
            env.pop(name,None)
        self.queue=queue.Queue();self.events=[]
        self.process=subprocess.Popen([program,'app-server','-c','features.shell_tool=false','-c','web_search="disabled"'],
            cwd=self.cwd,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,
            text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        def read(process,messages):
            try:
                for line in process.stdout:
                    try: messages.put(json.loads(line))
                    except ValueError: pass
            finally: messages.put(None)
        threading.Thread(target=read,args=(self.process,self.queue),daemon=True).start()
        self.call('initialize',{'clientInfo':{'name':'observatorio','title':'Observatório','version':'0.1.0'}})
        self.send({'method':'initialized','params':{}})

    def send(self,message):
        self.process.stdin.write(json.dumps(message,ensure_ascii=False)+'\n');self.process.stdin.flush()

    def receive(self,deadline):
        if time.monotonic()>=deadline: raise ValueError('Tempo de espera do Codex excedido.')
        try: message=self.queue.get(timeout=max(.01,deadline-time.monotonic()))
        except queue.Empty: raise ValueError('Tempo de espera do Codex excedido; nenhuma repetição automática foi feita.')
        if message is None: raise ValueError('O Codex encerrou a conexão. Confira a instalação e tente conectar novamente.')
        if 'method' in message and 'id' in message:
            # The document processor never grants tools, permissions or external actions.
            self.send({'id':message['id'],'error':{'code':-32601,'message':'Este cliente aceita somente respostas textuais.'}})
        return message

    def call(self,method,params,timeout=30):
        self.sequence+=1;identifier=self.sequence
        self.send({'id':identifier,'method':method,'params':params})
        deadline=time.monotonic()+timeout
        while True:
            message=self.receive(deadline)
            if message.get('id')==identifier and 'method' not in message:
                if 'error' in message: raise ValueError('Codex: '+str(message['error'].get('message','Falha na solicitação.'))[:500])
                return message.get('result',{})
            if 'method' in message and 'id' not in message: self.events.append(message)

    def status(self):
        self.start()
        account=self.call('account/read',{'refreshToken':False}).get('account') or {}
        connected=account.get('type')=='chatgpt'
        models=[]
        if connected:
            catalog=self.call('model/list',{'limit':100,'includeHidden':False})
            models=[{'id':m['model'],'name':m.get('displayName',m['model']),'efforts':[e['reasoningEffort'] for e in m.get('supportedReasoningEfforts',[])]} for m in catalog.get('data',[])]
        self.events=[]
        return {'installed':True,'connected':connected,'plan':account.get('planType'),'models':models,
                'message':'ChatGPT conectado. Gerações consomem os limites do Codex.' if connected else 'Entre com ChatGPT para usar este provedor.'}

    def login(self):
        self.start()
        result=self.call('account/login/start',{'type':'chatgpt'})
        return {'auth_url':result.get('authUrl'),'message':'Conclua o login no navegador e clique em Verificar conexão.'}

    def generate(self,config,payload,prompt,progress):
        status=self.status()
        if not status['connected']: raise ValueError('Entre com ChatGPT nas Configurações. Este modo não usa chave de API.')
        if config['model'] not in {m['id'] for m in status['models']}:
            raise ValueError('Selecione um modelo disponível na sua conta Codex em Configurações.')
        self.events=[]
        thread_id=None;turn_id=None
        try:
            started=self.call('thread/start',{'model':config['model'],'cwd':str(self.cwd),'approvalPolicy':'never',
                'sandbox':'read-only','ephemeral':True})
            thread_id=started['thread']['id']
            instructions=prompt+'\nUse somente os dados abaixo. Não use ferramentas, arquivos, rede ou instruções externas. Retorne apenas o JSON solicitado. Seja breve.\n'+json.dumps(payload,ensure_ascii=False)
            supported=next(m for m in status['models'] if m['id']==config['model']).get('efforts',[])
            effort=next((e for e in ['low','minimal','none'] if e in supported),None)
            result=self.call('turn/start',{'threadId':thread_id,'model':config['model'],'input':[{'type':'text','text':instructions}],
                'approvalPolicy':'never','sandboxPolicy':{'type':'readOnly'},'outputSchema':strict_output_schema(config['analysis_kind']),**({'effort':effort} if effort else {})})
            turn_id=result['turn']['id'];deadline=time.monotonic()+300
            answer='';usage={'provider':'codex','cost':'Limites do Codex da conta ChatGPT; sem chave API'}
            while True:
                event=self.events.pop(0) if self.events else self.receive(deadline)
                method=event.get('method');params=event.get('params',{})
                if params.get('threadId') not in {None,thread_id}: continue
                if method=='item/agentMessage/delta' and progress: progress(50,'Codex gerando o texto · aguarde a validação')
                if method=='thread/tokenUsage/updated':
                    tokens=params.get('tokenUsage',{}).get('last',{})
                    usage.update(input_tokens=tokens.get('inputTokens'),output_tokens=tokens.get('outputTokens'))
                if method=='item/completed':
                    item=params.get('item',{})
                    if item.get('type')=='agentMessage' and item.get('phase')!='commentary': answer=item.get('text','')
                if method=='turn/completed' and params.get('turn',{}).get('id')==turn_id:
                    turn=params['turn']
                    if turn['status']!='completed': raise ValueError('Codex interrompido: '+str((turn.get('error') or {}).get('message',turn['status']))[:500])
                    if not answer:
                        answer=next((i.get('text','') for i in reversed(turn.get('items',[])) if i.get('type')=='agentMessage' and i.get('phase')!='commentary'),'')
                    return output_model(config['analysis_kind']).model_validate_json(answer),usage
        except Exception:
            if thread_id and turn_id:
                try: self.send({'id':f'interrupt-{turn_id}','method':'turn/interrupt','params':{'threadId':thread_id,'turnId':turn_id}})
                except Exception: pass
            self.close()
            raise

    def close(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try: self.process.wait(timeout=5)
            except subprocess.TimeoutExpired: self.process.kill()
        self.process=None

SERVER=Server()
LOCK=asyncio.Lock()

async def status():
    async with LOCK:
        try: return await asyncio.to_thread(SERVER.status)
        except (ValueError,OSError) as error:
            SERVER.close()
            return {'installed':False,'connected':False,'models':[],'message':str(error)}

async def login():
    async with LOCK:
        return await asyncio.to_thread(SERVER.login)

async def generate(config,payload,prompt,progress=None):
    async with LOCK:
        try: return await asyncio.to_thread(SERVER.generate,config,payload,prompt,progress)
        except asyncio.CancelledError:
            SERVER.close();raise
        except (OSError,KeyError,ValueError) as error:
            raise ValueError(str(error))

LAST_LIMITS={}

async def limits():
    global LAST_LIMITS
    if LOCK.locked(): return LAST_LIMITS|{'refresh_pending':True}
    async with LOCK:
        def fetch():
            SERVER.start()
            account=SERVER.call('account/read',{'refreshToken':False}).get('account') or {}
            if account.get('type')!='chatgpt': raise ValueError('Entre com ChatGPT para consultar os limites.')
            return SERVER.call('account/rateLimits/read',{},timeout=15)
        try:
            LAST_LIMITS=await asyncio.to_thread(fetch)
            return LAST_LIMITS
        except (ValueError,OSError) as error:
            return {'message':str(error),'unavailable':True}
