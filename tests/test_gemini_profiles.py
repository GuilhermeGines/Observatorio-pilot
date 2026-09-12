import asyncio
import json
from types import SimpleNamespace as NS
from app import ai, db, profiles
from app.main import providers_usage
from test_core import save_query

def test_profiles_preserve_models_and_selection(synthetic_document,monkeypatch):
    monkeypatch.setattr(ai,'get_key',lambda *args:'test-key')
    query,_=save_query(synthetic_document)
    config=db.setting();config.provider='gemini';config.gemini_model='gemini-test';config.allow_ai=True
    profiles.remember(config)
    identifier=profiles.saved()[0]['id']
    config.provider='codex';config.codex_model='codex-test'
    profiles.remember(config);db.save_settings(config)
    assert len(profiles.available())==2
    assert ai.plan(query,profile_id=identifier)['model']=='gemini-test'
    assert db.setting().provider=='codex'
    profiles.remove(identifier)
    assert len(profiles.saved())==1

def test_gemini_generation_is_validated_and_usage_saved(synthetic_document):
    query,_=save_query(synthetic_document)
    config=db.setting();config.provider='gemini';config.gemini_model='gemini-test';config.allow_ai=True
    db.save_settings(config);profiles.remember(config)
    identifier=profiles.saved()[0]['id']
    prepared=ai.plan(query,profile_id=identifier)
    reference=prepared['payload']['documents'][0]['paragraphs'][0]['id']
    async def create(**kwargs):
        assert kwargs['model']=='gemini-test'
        assert kwargs['response_format']['json_schema']['schema']['additionalProperties'] is False
        assert 'paragraph_ids' in json.dumps(kwargs['response_format'])
        content=json.dumps({'summaries':[{'country':'BR','text':'O instituto apresentou uma pesquisa de energia, segundo a fonte.','paragraph_ids':[reference]}],'gaps':[]})
        return NS(choices=[NS(finish_reason='stop',message=NS(content=content))],usage=NS(prompt_tokens=100,completion_tokens=40))
    client=NS(chat=NS(completions=NS(create=create)))
    result=asyncio.run(ai.analyze(query,client=client,profile_id=identifier))
    assert result['config']['provider']=='gemini'
    assert result['result']['summaries'][0]['evidence']
    with db.connect() as connection:
        usage=json.loads(connection.execute('SELECT usage FROM usage').fetchone()['usage'])
    assert usage['provider']=='gemini' and usage['output_tokens']==40

def test_usage_does_not_invent_quota(monkeypatch):
    monkeypatch.setattr(ai,'get_key',lambda *args:'test-key')
    config=db.setting();config.provider='gemini';config.gemini_model='gemini-test';config.allow_ai=True
    profiles.remember(config)
    with db.connect() as connection:
        connection.execute('INSERT INTO usage(operation,model,usage,created_at) VALUES(?,?,?,?)',('analysis','gemini-test',db.dumps({'provider':'gemini','input_tokens':20,'output_tokens':None}),db.now()))
    item=providers_usage()['providers'][0]
    assert item['input_tokens']==20 and item['partial']
    assert 'used_percent' not in item
