"""Saved model configurations; secrets remain in the operating-system key store."""
import hashlib
import json
from . import db
from .models import SettingsInput

def model(settings):
    return {'ollama':settings.ollama_model,'codex':settings.codex_model,'gemini':settings.gemini_model}.get(settings.provider,settings.model)

def saved():
    with db.connect() as connection:
        row=connection.execute("SELECT value FROM meta WHERE key='ai_profiles'").fetchone()
    return json.loads(row['value']) if row else []

def remember(settings):
    if not model(settings).strip(): return
    identifier=hashlib.sha256((settings.provider+':'+model(settings)).encode()).hexdigest()[:16]
    items=[p for p in saved() if p['id']!=identifier]
    items.append({'id':identifier,'config':settings.model_dump()})
    with db.connect() as connection:
        connection.execute("INSERT INTO meta VALUES('ai_profiles',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",(db.dumps(items),))

def configuration(identifier=None):
    if not identifier: return db.setting()
    item=next((p for p in saved() if p['id']==identifier),None)
    if not item: raise ValueError('Configuração não encontrada. Atualize a seleção de modelos.')
    return SettingsInput.model_validate(item['config'])

def available():
    from .ai import get_key
    items=saved()
    current=db.setting()
    if not any(p['config']['provider']==current.provider and model(SettingsInput.model_validate(p['config']))==model(current) for p in items):
        items.append({'id':'','config':current.model_dump()})
    result=[]
    for item in items:
        setting=SettingsInput.model_validate(item['config'])
        ready=setting.allow_ai and bool(model(setting))
        if setting.provider in {'openai','gemini'}: ready=ready and bool(get_key(setting.provider))
        result.append({'id':item['id'],'provider':setting.provider,'model':model(setting),'ready':bool(ready)})
    return result

def remove(identifier):
    items=saved()
    removed=next((p for p in items if p['id']==identifier),None)
    current=db.setting()
    if removed:
        old=SettingsInput.model_validate(removed['config'])
        if old.provider==current.provider and model(old)==model(current):
            current.allow_ai=False
            db.save_settings(current)
    with db.connect() as connection:
        connection.execute("UPDATE meta SET value=? WHERE key='ai_profiles'",(db.dumps([p for p in items if p['id']!=identifier]),))
