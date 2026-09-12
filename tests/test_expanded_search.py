"""Synthetic checks only; no Gemini call or public news collection."""
from app import db
from app.catalog import BY_ID
from app.collection import base_body
from app.expanded_search import gdelt_links, gdelt_query, publisher
from app.models import QueryInput
from app.queries import add_discovery, make_result


def test_document_index_uses_source_links_not_model_prose():
    payload={'articles':[{'url':'https://techcrunch.com/story','title':'TechCrunch'}]}
    assert gdelt_links(payload)==[{'url':'https://techcrunch.com/story','title':'TechCrunch'}]
    assert gdelt_query('iPhone',['Apple phone'],'US')=='("iPhone" OR "Apple phone") sourcecountry:unitedstates'
    assert 'sourcecountry:' not in gdelt_query('iPhone sourcecountry:russia',[],'US').split(' sourcecountry:')[0]
    assert publisher('https://techcrunch.com/story','US')['id']=='techcrunch'
    assert publisher('https://techcrunch.com/story','BR') is None


def test_verified_article_outside_normal_route_enters_query_evidence():
    query=QueryInput(countries=['US'],keyword='iPhone',start='2026-09-09',end='2026-09-09',mode='collect')
    source=BY_ID['techcrunch']
    body=base_body(source,'iPhone synthetic test publication','iPhone synthetic test text', '2026-09-09T12:00:00-04:00')
    body.update(text='iPhone synthetic test text. '*20,access='texto_extraido',genre='apuracao_nao_verificada',origin='')
    revision_id,_=db.save_document(source['id'],'https://techcrunch.com/synthetic-test',body)
    original=make_result(query,[])
    assert not original['documents']
    result=add_discovery(original,{'model':'gemini-2.5-flash-lite','verified':[{'revision_id':revision_id,'source_id':'techcrunch'}],
        'leads':[],'notes':[],'calls':1})
    assert result['documents'][0]['source_name']=='TechCrunch'
    assert result['documents'][0]['revision_id']==revision_id
    assert result['documents'][0]['text']==body['text']
    assert result['discovery']['verified_count']==1
    assert result['coverage'][-1]['name']=='TechCrunch'
