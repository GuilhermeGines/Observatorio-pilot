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
    assert (await source_routing.resolve(q2))['source_ids']==[]
    assert selected_sources(q2)==[]

