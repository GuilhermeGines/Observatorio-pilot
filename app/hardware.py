"""Local, read-only inventory and conservative runtime preferences."""
import ctypes
import os
import platform
from . import ollama_local

def inventory():
    result={'cpu':platform.processor() or 'Não verificado','threads':os.cpu_count(),
            'gpus':[],'memory_total_gb':None,'memory_available_gb':None,'notes':[]}
    if os.name=='nt':
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r'HARDWARE\DESCRIPTION\System\CentralProcessor\0') as key:
                result['cpu']=winreg.QueryValueEx(key,'ProcessorNameString')[0].strip()
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r'SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}') as root:
                for i in range(winreg.QueryInfoKey(root)[0]):
                    name=winreg.EnumKey(root,i)
                    if not name.isdigit(): continue
                    with winreg.OpenKey(root,name) as key:
                        try:
                            gpu=winreg.QueryValueEx(key,'DriverDesc')[0]
                            if gpu not in result['gpus']: result['gpus'].append(gpu)
                        except OSError: pass
        except OSError:
            result['notes'].append('Parte do inventário não pôde ser lida.')
        class Memory(ctypes.Structure):
            _fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong)]+[(n,ctypes.c_ulonglong) for n in ['total','available','page_total','page_available','virtual_total','virtual_available','extended']]
        m=Memory();m.length=ctypes.sizeof(m)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)):
            result.update(memory_total_gb=round(m.total/2**30,2),memory_available_gb=round(m.available/2**30,2))
    result['recommendation']='auto' if result['gpus'] else 'cpu'
    result['reserve_gb']=max(2,round((result['memory_total_gb'] or 12)*.25))
    result['notes'].append('GPU detectada não comprova aceleração. Memória compartilhada não é memória adicional; nenhuma inferência foi executada.')
    return result

async def inspect():
    import asyncio
    result=await asyncio.to_thread(inventory)
    try:
        result['ollama_version']=(await ollama_local.request('GET','/api/version')).get('version')
        result['loaded_models']=(await ollama_local.request('GET','/api/ps')).get('models',[])
    except ValueError as error:
        result['ollama_version']=None;result['loaded_models']=[];result['notes'].append(str(error))
    return result

def environment(profile='auto'):
    info=inventory()
    gpu=profile=='auto' and bool(info['gpus'])
    return {'OLLAMA_NUM_PARALLEL':'1','OLLAMA_MAX_LOADED_MODELS':'1',
            'OLLAMA_IGPU_ENABLE':'1' if gpu else '0','OLLAMA_VULKAN':'1' if gpu else '0',
            'GGML_VK_VISIBLE_DEVICES':'' if gpu else '-1',
            'CUDA_VISIBLE_DEVICES':'' if gpu else '-1','ROCR_VISIBLE_DEVICES':'' if gpu else '-1'}

def check_memory(reserve_gb):
    available=inventory()['memory_available_gb']
    if available is not None and available<reserve_gb:
        raise ValueError(f'Memória livre abaixo da margem de {reserve_gb:g} GB. Feche outros programas ou ajuste o perfil em Configurações.')
