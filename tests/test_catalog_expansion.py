from types import SimpleNamespace
import pytest
from app import collection, db
from app.catalog import BY_ID, SOURCES, selected_sources
from app.models import QueryInput

def test_topic_selection_and_iphone():
    query=QueryInput(countries=['BR'],topics=['tecnologia'],keyword='iPhone',start='2026-09-09',end='2026-09-09')
    selected=selected_sources(query)
    ids=[s['id'] for s in selected]
    assert len(ids)==len(set(ids))==5
    assert {'tecnoblog','canaltech','tecmundo','macmagazine','olhardigital'}<=set(ids)
    assert 'planalto' not in ids and 'fiocruz' not in ids
    assert 'tecnologia' in collection.topics_for('iPhone chega ao Brasil')
    assert collection.allowed('https://www.gov.br/planalto/pt-br/noticia',BY_ID['planalto'])
    assert not collection.allowed('https://www.gov.br/saude/pt-br/noticia',BY_ID['planalto'])
    query.topics=['tecnologia','ciencia']
    assert len(selected_sources(query))==len({s['id'] for s in selected_sources(query)})

@pytest.mark.asyncio
async def test_collect_routes_topics_once_and_respects_disabled(monkeypatch):
    query=QueryInput(countries=['BR'],topics=['tecnologia'],start='2026-09-09',end='2026-09-09')
    settings=db.setting();settings.disabled_sources=['tecnoblog'];db.save_settings(settings)
    called=[]
    class Reader:
        async def close(self): pass
    async def collect_source(reader,source,*args):
        called.append(source['id'])
        return {'source_id':source['id'],'status':'parcial'}
    monkeypatch.setattr(collection,'Reader',Reader)
    monkeypatch.setattr(collection,'collect_source',collect_source)
    rows=await collection.collect(query,'synthetic')
    assert len(rows)==5 and len(called)==4 and len(set(called))==4
    assert 'tecnoblog' not in called and 'canaltech' in called and 'fiocruz' not in called
    assert next(r for r in rows if r['source_id']=='tecnoblog')['status']=='desativada'

@pytest.mark.asyncio
async def test_unknown_expression_local_routing_without_real_model(monkeypatch):
    from app import source_routing,ollama_local
    from app.queries import matching
    source_routing.CLASSIFICATIONS.clear()
    config=db.setting();config.provider='ollama';config.allow_ai=True;db.save_settings(config)
    calls=[]
    async def request(method,path,body=None,**kwargs):
        calls.append(path)
        if path=='/api/show': return {}
        assert body['options']['num_predict']==128 and body['think'] is False
        return {'message':{'content':'{"topics":["saude"],"confident":true}'},'done_reason':'stop'}
    monkeypatch.setattr(ollama_local,'request',request)
    q=QueryInput(countries=['BR','CN'],keyword='tratamento da enxaqueca',start='2026-09-09',end='2026-09-09')
    result=await source_routing.resolve(q)
    assert result['mode']=='semantic' and result['topics']==['saude']
    assert len(selected_sources(q))==10 and all('saude' in s['topics'] for s in selected_sources(q))
    await source_routing.resolve(q)
    assert calls==['/api/show','/api/chat']
    q2=QueryInput(countries=['RU'],keyword='expressao ambigua desconhecida',start='2026-09-09',end='2026-09-09')
    async def ambiguous(*args,**kwargs): return {'message':{'content':'{"topics":[],"confident":false}'}}
    monkeypatch.setattr(ollama_local,'request',ambiguous)
    assert (await source_routing.resolve(q2))['mode']=='general'
    assert selected_sources(q2) and all('jornalismo_geral' in source['groups'] for source in selected_sources(q2))


@pytest.mark.asyncio
@pytest.mark.parametrize('provider',['ollama','codex','openai','gemini'])
async def test_full_expression_routes_with_each_provider(monkeypatch,provider):
    from app import source_routing,ai
    from app.models import TopicClassification
    source_routing.CLASSIFICATIONS.clear()
    monkeypatch.setattr(ai,'get_key',lambda *args:'synthetic')
    config=db.setting();config.provider=provider;config.allow_ai=True
    config.codex_model='synthetic-codex';config.gemini_model='synthetic-gemini';db.save_settings(config)
    seen=[]
    async def classify(expression,countries,settings):
        seen.append((expression,countries,settings.provider))
        return TopicClassification(topics=['politica'],confident=True)
    monkeypatch.setattr(source_routing,'classify',classify)
    q=QueryInput(countries=['BR','US'],keyword='nome novo e decisão de tribunal',start='2026-09-09',end='2026-09-09')
    result=await source_routing.resolve(q)
    assert seen==[(q.keyword,['BR','US'],provider)]
    assert result['mode']=='semantic' and q.topics==[]
    assert all(source['country'] in q.countries and 'politica' in source['topics'] for source in selected_sources(q))

@pytest.mark.asyncio
async def test_manual_choice_wins_and_failure_never_blocks(monkeypatch):
    from app import source_routing
    config=db.setting();config.provider='ollama';config.allow_ai=True;db.save_settings(config)
    async def failing(*args): raise RuntimeError('synthetic failure')
    monkeypatch.setattr(source_routing,'classify',failing)
    q=QueryInput(countries=['BR'],keyword='iphone',topics=['fisica'],start='2026-09-09',end='2026-09-09')
    assert (await source_routing.resolve(q))['mode']=='explicit'
    assert all('fisica' in source['topics'] for source in selected_sources(q))
    q.topics=[]
    result=await source_routing.resolve(q)
    assert result['mode']=='general' and len(result['source_ids'])==10
    assert all(source['country']=='BR' and 'jornalismo_geral' in source['groups'] for source in selected_sources(q))
