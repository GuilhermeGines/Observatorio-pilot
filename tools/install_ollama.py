"""Instala a distribuição oficial independente e o Qwen, sem iniciar análises."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import zipfile
import httpx

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / 'runtime'
BIN = RUNTIME / 'ollama'
MODEL = 'qwen3.5:4b'
URL = 'http://127.0.0.1:11434'

def available():
    try:
        with httpx.Client(trust_env=False, timeout=3) as client:
            return client.get(URL + '/api/version').is_success
    except httpx.HTTPError:
        return False

def start():
    if available():
        return
    exe = BIN / 'ollama.exe'
    if not exe.exists():
        raise RuntimeError('Ollama não instalado. Execute Instalar-Qwen.cmd.')
    env = os.environ.copy()
    env.update(OLLAMA_HOST='127.0.0.1:11434', OLLAMA_MODELS=str(RUNTIME / 'models'),
               OLLAMA_NO_CLOUD='1', OLLAMA_NUM_PARALLEL='1')
    sys.path.insert(0,str(ROOT))
    from app import db, hardware
    profile=db.setting().resource_profile
    env.update(hardware.environment(profile))
    RUNTIME.mkdir(exist_ok=True)
    with (RUNTIME / 'ollama.log').open('ab') as output:
        process = subprocess.Popen([str(exe), 'serve'], cwd=ROOT, env=env,
            stdin=subprocess.DEVNULL, stdout=output, stderr=output,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
    (RUNTIME / 'ollama-process.json').write_text(json.dumps({'pid':process.pid,'executable':str(exe)}))
    for _ in range(40):
        if available():
            return
        if process.poll() is not None:
            break
        time.sleep(.5)
    raise RuntimeError('Ollama não iniciou. Consulte runtime/ollama.log.')

def restart_owned():
    """Restart only the executable owned by this installation; never kill by name."""
    if available():
        import ctypes
        record=RUNTIME/'ollama-process.json'
        if os.name!='nt' or not record.exists():
            raise RuntimeError('Ollama externo: reinicie-o manualmente para aplicar o perfil.')
        data=json.loads(record.read_text())
        expected=(BIN/'ollama.exe').resolve()
        if Path(data['executable']).resolve()!=expected:
            raise RuntimeError('Processo não pertence a esta instalação.')
        from ctypes import wintypes
        kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        kernel.OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD];kernel.OpenProcess.restype=wintypes.HANDLE
        kernel.QueryFullProcessImageNameW.argtypes=[wintypes.HANDLE,wintypes.DWORD,wintypes.LPWSTR,ctypes.POINTER(wintypes.DWORD)]
        kernel.TerminateProcess.argtypes=[wintypes.HANDLE,wintypes.UINT]
        kernel.WaitForSingleObject.argtypes=[wintypes.HANDLE,wintypes.DWORD]
        kernel.CloseHandle.argtypes=[wintypes.HANDLE]
        handle=kernel.OpenProcess(0x100001|0x1000,False,int(data['pid']))
        if not handle: raise RuntimeError('Não foi possível confirmar o processo do Ollama; reinicie-o manualmente.')
        try:
            buffer=ctypes.create_unicode_buffer(32768);length=wintypes.DWORD(len(buffer))
            if not kernel.QueryFullProcessImageNameW(handle,0,buffer,ctypes.byref(length)) or Path(buffer.value).resolve()!=expected:
                raise RuntimeError('Identidade do processo não confirmada; nada foi encerrado.')
            if not kernel.TerminateProcess(handle,0): raise RuntimeError('Não foi possível reiniciar o Ollama.')
            kernel.WaitForSingleObject(handle,5000)
        finally: kernel.CloseHandle(handle)
    start()

def install():
    RUNTIME.mkdir(exist_ok=True)
    if not available() and not (BIN / 'ollama.exe').exists():
        with httpx.Client(follow_redirects=True, timeout=120) as client:
            release = client.get('https://api.github.com/repos/ollama/ollama/releases/latest')
            release.raise_for_status()
            asset = next(a for a in release.json()['assets'] if a['name']=='ollama-windows-amd64.zip')
            expected = asset.get('digest','')
            if not expected.startswith('sha256:'):
                raise RuntimeError('A distribuição oficial não informou SHA256; download cancelado.')
            archive = RUNTIME / 'ollama-download.zip'
            print('Baixando Ollama oficial: '+release.json()['tag_name'], flush=True)
            digest = hashlib.sha256()
            with client.stream('GET',asset['browser_download_url']) as response, archive.open('wb') as output:
                response.raise_for_status()
                for chunk in response.iter_bytes(1024*1024):
                    digest.update(chunk)
                    output.write(chunk)
            if digest.hexdigest()!=expected.split(':',1)[1]:
                raise RuntimeError('SHA256 incorreto. Não foi executado nenhum arquivo baixado.')
            print('Arquivo verificado. Extraindo Ollama.', flush=True)
            BIN.mkdir(exist_ok=True)
            with zipfile.ZipFile(archive) as package:
                for member in package.infolist():
                    if not (BIN/member.filename).resolve().is_relative_to(BIN.resolve()):
                        raise RuntimeError('Caminho inválido no pacote.')
                package.extractall(BIN)
            archive.unlink()
    start()
    print('Baixando/verificando Qwen 3.5 4B. O download do modelo tem cerca de 3,4 GB.', flush=True)
    with httpx.Client(trust_env=False, timeout=httpx.Timeout(600, connect=5)) as client:
        with client.stream('POST',URL+'/api/pull',json={'model':MODEL,'stream':True}) as response:
            response.raise_for_status()
            last = ''
            for line in response.iter_lines():
                if not line:
                    continue
                data = json.loads(line)
                if data.get('error'):
                    raise RuntimeError(data['error'])
                status = data.get('status','')
                if status != last:
                    print(status, flush=True)
                    last = status
            if last != 'success':
                raise RuntimeError('Download não concluído.')
    sys.path.insert(0,str(ROOT))
    from app import db
    if not (db.DATA/'observatorio.sqlite3').exists():
        db.init()
    settings = db.setting()
    settings.provider='ollama'
    settings.ollama_model=MODEL
    settings.allow_ai=True
    settings.max_documents=4
    settings.max_chars_per_document=1000
    settings.max_output_tokens=3000
    db.save_settings(settings)
    print('Qwen instalado e selecionado no Observatório. Recarregue a página.', flush=True)

if __name__=='__main__':
    try:
        start() if '--start-only' in sys.argv else install()
    except Exception as error:
        print('Falha: '+str(error), file=sys.stderr)
        sys.exit(1)
