import io
import json
import sqlite3
import zipfile
from types import SimpleNamespace
import pytest
from fastapi.testclient import TestClient
from app import ai,db
from app.catalog import SOURCES,BY_ID
from app.collection import FetchError,allowed,base_body,canonical,collect_source,extract_article,feed_entries,publication
from app.main import app
from app.models import AnalysisOutput,QueryInput
from app.queries import matching,make_result,read_query,related_pairs,origin_groups

def query(**kwargs):
    return QueryInput(**({'countries':['BR'],'start':'2026-09-07','end':'2026-09-07'}|kwargs))

def save_query(document):
    revision,_=db.save_document('agbr','https://agenciabrasil.ebc.com.br/test/synthetic',document)
    result=make_result(query())
    with db.connect() as c:
        c.execute('INSERT INTO queries(id,filters,result,created_at,title,status) VALUES(?,?,?,?,?,?)',('synthetic-query',query().model_dump_json(),db.dumps(result),db.now(),'FIXTURE SINTÉTICA','pronta'))
    return read_query('synthetic-query'),revision

def test_catalog_country_groups():
    from app.catalog import TOPICS
    assert len(SOURCES)==len(BY_ID) and len(SOURCES)>60
    for country in ['BR','US','CN','RU']:
        local=[s for s in SOURCES if s['country']==country]
        for group,count in [('jornalismo_geral',10),('governo',1),('universidades',5)]:
            assert sum(group in s['groups'] for s in local)==count
        assert sum(s['kind']=='universidade' for s in local)==5
        for topic in TOPICS:
            assert sum(topic in s['topics'] for s in local)==5


def test_dates_publication_timezone_and_invalid_ranges():
    pub,_=publication('2026-09-08T01:30:00Z','America/Sao_Paulo')
    assert pub.startswith('2026-09-07T22:30')
    assert publication('yesterday','UTC')[0] is None
    with pytest.raises(ValueError): query(start='2026-09-08')
    with pytest.raises(ValueError): query(countries=[])
    with pytest.raises(ValueError): query(topics=['inexistente'])

def test_keyword_never_expands_country_and_uses_publication(synthetic_document):
    db.save_document('agbr','https://agenciabrasil.ebc.com.br/synthetic',synthetic_document)
    other=synthetic_document|{'country':'CN'}
    db.save_document('xinhua','https://english.news.cn/synthetic',other)
    rows=db.revision_rows()
    found=matching(rows,query(keyword='SÁMSUNG'))
    assert len(found)==1 and found[0]['source_id']=='agbr'
    assert matching(rows,query(start='2018-09-23',end='2018-09-23'))==[]
    assert matching(rows,query(),['agbr'])==[]
    assert matching(rows,query(topics=['astronomia']))==[]

def test_document_dedup_version_and_no_downgrade(synthetic_document):
    url='https://agenciabrasil.ebc.com.br/test'
    first,created=db.save_document('agbr',url,synthetic_document)
    same,created2=db.save_document('agbr',url,synthetic_document)
    changed,created3=db.save_document('agbr',url,synthetic_document|{'text':'FIXTURE SINTÉTICA revisada: 12 unidades.'})
    kept,created4=db.save_document('agbr',url,synthetic_document|{'text':'Resumo','access':'resumo_do_feed'})
    assert created and not created2 and first==same and created3 and changed!=first
    assert kept==changed and not created4
    assert '10 unidades' in db.read_revision(first)['text']
    assert '12 unidades' in db.revision_rows()[0]['text']
    assert len(list((db.DATA/'documents').glob('*.json')))==2

def test_snapshot_does_not_change_when_article_changes(synthetic_document):
    saved,revision=save_query(synthetic_document)
    db.save_document('agbr','https://agenciabrasil.ebc.com.br/test/synthetic',synthetic_document|{'text':'FIXTURE SINTÉTICA alterada'})
    reopened=read_query(saved['id'])
    assert reopened['result']['documents'][0]['revision_id']==revision
    assert reopened['result']['documents'][0]['text']==synthetic_document['text']

def test_result_cap_does_not_crowd_out_a_country(synthetic_document):
    for i in range(201):
        db.save_document('agbr',f'https://agenciabrasil.ebc.com.br/synthetic/{i}',synthetic_document)
    db.save_document('nyt','https://www.nytimes.com/synthetic/only',synthetic_document|{'country':'US'})
    result=make_result(query(countries=['BR','US']))
    assert len(result['documents'])==200 and result['total_matches']==202
    assert {d['country'] for d in result['documents']}=={'BR','US'}
    assert next(c for c in result['coverage'] if c['source_id']=='agbr')['matches']==201

def test_feed_uses_published_not_updated_and_rejects_external():
    feed=b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Synthetic A</title><link href="https://agenciabrasil.ebc.com.br/a"/><updated>2026-09-07T12:00:00Z</updated></entry><entry><title>Synthetic B</title><link href="https://example.com/b"/><published>2026-09-07T12:00:00Z</published></entry></feed>'''
    entries=feed_entries(feed,BY_ID['agbr'])
    assert len(entries)==1 and entries[0][1]['published_at'] is None
    assert canonical('https://EXAMPLE.com/a?utm_source=x&id=4#top')=='https://example.com/a?id=4'
    assert not allowed('http://127.0.0.1/admin',BY_ID['agbr'])
    assert not allowed('https://agenciabrasil.ebc.com.br.evil.com/a',BY_ID['agbr'])

def test_paywall_never_extracts_protected_body():
    html=b'''<html><script type="application/ld+json">{"@type":"NewsArticle","headline":"SYNTHETIC paywall","datePublished":"2026-09-07","isAccessibleForFree":false}</script><article><p>PROTECTED BODY synthetic fixture</p></article></html>'''
    result=extract_article(html,'https://www.nytimes.com/synthetic',BY_ID['nyt'],base_body(BY_ID['nyt'],'SYNTHETIC','Public summary.'))
    assert result['text']=='Public summary.' and result['access']=='parcial_restrito'

@pytest.mark.asyncio
async def test_partial_source_failure_preserves_feed_evidence():
    class FakeReader:
        async def get(self,url,source):
            if url==source['channel']:
                return b'''<rss version="2.0"><channel><item><title>FIXTURE SINTETICA</title><link>https://agenciabrasil.ebc.com.br/test-fixture</link><pubDate>Mon, 07 Sep 2026 12:00:00 GMT</pubDate><description>Public synthetic snippet.</description></item></channel></rss>''','application/xml',url
            raise FetchError('HTTP 403; conteúdo não recuperado.')
    result=await collect_source(FakeReader(),BY_ID['agbr'],query(),'test',2)
    assert result['status']=='parcial'
    assert len(db.revision_rows())==1 and db.revision_rows()[0]['text']=='Public synthetic snippet.'
    assert len(result['detail']['failures'])==1

@pytest.mark.asyncio
async def test_one_failure_does_not_discard_other_sources(monkeypatch):
    from app import collection
    monkeypatch.setattr(collection,'SOURCES',[BY_ID['agbr'],BY_ID['g1']])
    async def fake(reader,source,*args):
        return {'source_id':source['id'],'status':'indisponivel' if source['id']=='g1' else 'disponivel'}
    monkeypatch.setattr(collection,'collect_source',fake)
    results=await collection.collect(query(),'test')
    assert {r['status'] for r in results}=={'indisponivel','disponivel'}

def test_related_pair_blocking_and_common_origin(synthetic_document):
    a=synthetic_document|{'revision_id':1,'source_id':'agbr','origin':'reuters'}
    b=a|{'revision_id':2,'source_id':'g1'}
    c=a|{'revision_id':3,'title':'Astronomia distante sem relação','topics':['astronomia']}
    assert len(related_pairs([a,b,c]))==1
    assert origin_groups([a,b])[0]['revision_ids']==[1,2]

def test_api_csrf_history_export_backup_and_restart(synthetic_document):
    saved,revision=save_query(synthetic_document)
    with TestClient(app,base_url='http://127.0.0.1:8765') as client:
        assert client.post('/api/queries',json=query().model_dump(mode='json')).status_code==403
        headers={'X-Observatorio-Token':client.get('/api/session').json()['token']}
        assert client.put('/api/settings',headers=headers|{'Origin':'https://evil.test'},json={}).status_code==403
        assert client.get('/api/history').json()==[]
        response=client.post('/api/queries/synthetic-query/save',headers=headers,json={'title':'FIXTURE SINTÉTICA — consulta salva'})
        assert response.status_code==200
        assert len(client.get('/api/history?country=BR').json())==1
        assert client.get('/api/history?country=CN').json()==[]
        assert client.get('/api/history?start=2018-01-01&end=2018-12-31').json()==[]
        exported=client.get('/api/queries/synthetic-query/export').json()
        assert exported['query']['result']['documents'][0]['revision_id']==revision
        response=client.post('/api/backup',headers=headers,json={})
        assert response.status_code==200
        backup=client.get('/api/backups/'+response.json()['id'])
        with zipfile.ZipFile(io.BytesIO(backup.content)) as archive:
            assert 'observatorio.sqlite3' in archive.namelist()
            assert f'documents/{revision}.json' in archive.namelist()
            assert not json.loads(archive.read('manifest.json'))['credentials_included']
        assert client.get('/api/settings').json()['key_configured'] is False
        assert 'key' not in client.get('/api/settings').json()
    db.init()
    assert read_query(saved['id'])['saved_at'] is not None

def test_no_key_cannot_generate_fake_analysis(synthetic_document):
    save_query(synthetic_document)
    with TestClient(app,base_url='http://127.0.0.1:8765') as client:
        headers={'X-Observatorio-Token':client.get('/api/session').json()['token']}
        response=client.post('/api/queries/synthetic-query/analyze',headers=headers,json={})
        assert response.status_code==400
        assert read_query('synthetic-query')['analyses']==[]

def test_backup_restore_is_portable_and_does_not_overwrite(synthetic_document,tmp_path):
    from tools.restore_backup import restore
    save_query(synthetic_document)
    from app.main import backup
    result=backup()
    target=restore(db.DATA/'backups'/(result['id']+'.zip'),tmp_path/'restored')
    with sqlite3.connect(target/'observatorio.sqlite3') as c:
        assert c.execute('SELECT COUNT(*) FROM documents').fetchone()[0]==1
    with pytest.raises(ValueError): restore(db.DATA/'backups'/(result['id']+'.zip'),target)
    malicious=tmp_path/'bad.zip'
    with zipfile.ZipFile(malicious,'w') as z:
        z.writestr('manifest.json',json.dumps({'format':'observatorio-backup-v1'}))
        z.writestr('../escape.txt','malicious path synthetic fixture')
    with pytest.raises(ValueError): restore(malicious,tmp_path/'bad-target')

def test_scoped_government_sources_and_publication_metadata():
    assert not allowed('https://www.gov.br/planalto/noticia',BY_ID['itamaraty'])
    assert allowed('https://www.gov.br/mre/pt-br/noticia',BY_ID['itamaraty'])
    html=b'<html><meta name="PubDate" content="2026/09/04 09:30"><h1>Synthetic statistics publication</h1></html>'
    result=extract_article(html,'https://www.stats.gov.cn/english/test',BY_ID['statscn'],base_body(BY_ID['statscn'],'Synthetic title'))
    assert result['published_at']=='2026-09-04T09:30:00+08:00'

def synthetic_analysis(revision,quote):
    return AnalysisOutput.model_validate({'summaries':[{'country':'BR','text':'RESUMO SINTÉTICO DE TESTE.','evidence':[{'revision_id':revision,'quote':quote}]}],'claims':[],'comparisons':[],'cross_statements':[],'gaps':['FIXTURE SINTÉTICA'],'script':'ROTEIRO SINTÉTICO. Instituto Alfa publicou uma afirmação de teste.'})

def test_hallucinated_citations_are_rejected(synthetic_document):
    saved,revision=save_query(synthetic_document)
    payload=ai.plan(saved)['payload']
    for bad in [synthetic_analysis(revision,'Invented quotation'),synthetic_analysis(999,synthetic_document['text'])]:
        with pytest.raises(ValueError): ai.validate_evidence(bad,payload)
    good=synthetic_analysis(revision,synthetic_document['text'])
    good.summaries[0].country='CN'
    with pytest.raises(ValueError): ai.validate_evidence(good,payload)

@pytest.mark.asyncio
async def test_analysis_version_cache_usage(synthetic_document):
    saved,revision=save_query(synthetic_document)
    settings=db.setting();settings.allow_ai=True;db.save_settings(settings)
    calls=[]
    async def parse(**kwargs):
        calls.append(kwargs)
        assert kwargs['store'] is False
        return SimpleNamespace(output_parsed=kwargs['text_format'](summaries=[{'country':'BR','text':'Teste','paragraph_ids':[ai.plan(saved)['payload']['documents'][0]['paragraphs'][0]['id']]}],gaps=[]),usage=SimpleNamespace(model_dump=lambda:{'input_tokens':30,'output_tokens':20}))
    client=SimpleNamespace(responses=SimpleNamespace(parse=parse))
    one=await ai.analyze(saved,client=client)
    reused=await ai.analyze(saved,client=client)
    two=await ai.analyze(saved,regenerate=True,client=client)
    assert one['id']==reused['id'] and two['version']==2 and len(calls)==2
    assert len(read_query(saved['id'])['analyses'])==2
