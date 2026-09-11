"""Inicialização local: usa apenas a interface já compilada."""
import argparse
import os
import json
import sys
from pathlib import Path
import socket
import threading
import urllib.request
import webbrowser
import uvicorn

ROOT=Path(__file__).resolve().parent
URL='http://127.0.0.1:8765'

def open_when_ready():
    import time
    for _ in range(40):
        try:
            with urllib.request.urlopen(URL+'/api/health',timeout=1) as response:
                if response.status==200:
                    webbrowser.open(URL)
                    return
        except OSError:
            time.sleep(.25)

def main():
    parser=argparse.ArgumentParser(description='Observatório — servidor local')
    parser.add_argument('--no-browser',action='store_true',help='Não abre automaticamente o navegador')
    args=parser.parse_args()
    os.chdir(ROOT)
    if not (ROOT/'app/static/index.html').exists():
        raise SystemExit('Interface compilada ausente. Baixe a distribuição completa ou execute npm run build na pasta frontend.')
    with socket.socket() as probe:
        if probe.connect_ex(('127.0.0.1',8765))==0:
            try:
                with urllib.request.urlopen(URL+'/api/health',timeout=2) as response:
                    status=json.load(response)
                if status.get('local_only') and status.get('version'):
                    if not args.no_browser:
                        webbrowser.open(URL)
                    print('O Observatório já está aberto em '+URL)
                    return
            except Exception:
                pass
            raise SystemExit('A porta 8765 está ocupada por outro programa. Feche o programa que usa essa porta e tente novamente.')
    from app import db
    db.init()
    if db.setting().provider=='ollama':
        try:
            from tools.install_ollama import start
            start()
        except Exception as error:
            print('Ollama: '+str(error)+' A interface continuará disponível.')
    if not args.no_browser:
        threading.Thread(target=open_when_ready,daemon=True).start()
    print('Observatório: '+URL+'\nPara encerrar, pressione Ctrl+C nesta janela. Dados ficam preservados.')
    data=Path(os.environ.get('OBS_DATA_DIR') or ROOT/'data').resolve()
    data.mkdir(parents=True,exist_ok=True)
    pid_file=data/'server-process.json'
    pid_file.write_text(json.dumps({'pid':os.getpid(),'executable':str(Path(getattr(sys,'_base_executable',sys.executable)).resolve()),'root':str(ROOT)}),encoding='utf-8')
    try:
        uvicorn.run('app.main:app',host='127.0.0.1',port=8765,access_log=False,log_level='warning')
    finally:
        pid_file.unlink(missing_ok=True)

if __name__=='__main__':
    main()
