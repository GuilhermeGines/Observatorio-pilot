from types import SimpleNamespace
import pytest
from bs4 import BeautifulSoup
from app import ai,db,hardware,article_images
from app.queries import read_query
from test_core import save_query,synthetic_analysis

def test_hardware_profiles_and_memory_guard(monkeypatch):
    monkeypatch.setattr(hardware,'inventory',lambda:{'gpus':['AMD Radeon'],'memory_available_gb':2})
    assert hardware.environment('auto')['OLLAMA_IGPU_ENABLE']=='1'
    assert hardware.environment('cpu')['CUDA_VISIBLE_DEVICES']=='-1'
    with pytest.raises(ValueError,match='Memória'): hardware.check_memory(3)

def test_relevant_spans_and_invalid_reference():
    from app.relevant_text import select, resolve, group_duplicates
    from app.models import ParagraphSummaryOutput
    doc={'revision_id':1,'country':'BR','source_name':'Teste','title':'Título','text':('Introdução distante. '*100)+'\n\nO iPhone tem uma nova câmera.\n\nContexto da câmera.'}
    selected=select(doc,'iPhone',[],400)
    assert 'iPhone' in selected['text'] and len(selected['text'])<=410
    assert all(p['text'] in doc['text'] for p in selected['paragraphs'])
    assert len(group_duplicates([doc,doc|{'revision_id':2}])[0])==1
    stage=ParagraphSummaryOutput(summaries=[{'country':'BR','text':'Teste','paragraph_ids':['inventado']}],gaps=[])
    with pytest.raises(ValueError): resolve(stage,{'documents':[selected]})

@pytest.mark.asyncio
async def test_summary_cache_between_queries_and_language_policy(synthetic_document):
    query,revision=save_query(synthetic_document)
    settings=db.setting();settings.allow_ai=True;db.save_settings(settings)
    calls=[]
    async def parse(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(output_parsed=kwargs['text_format'](summaries=[{'country':'BR','text':'Síntese de teste','paragraph_ids':[ai.plan(query)['payload']['documents'][0]['paragraphs'][0]['id']]}],gaps=[]),usage=None)
    client=SimpleNamespace(responses=SimpleNamespace(parse=parse))
    first=await ai.analyze(query,client=client)
    with db.connect() as c:
        c.execute("INSERT INTO queries(id,filters,result,created_at,title,status) VALUES(?,?,?,?,?,?)",('second',db.dumps(query['filters']),db.dumps(query['result']),db.now(),'second','pronta'))
    second=await ai.analyze(read_query('second'),client=client)
    assert len(calls)==1 and second['usage']['cache_only']
    assert second['result']['summaries']==first['result']['summaries']
    assert first['config']['language_policy']=='BR-pt_others-en'
    assert 'US, CN e RU em inglês' in calls[0]['input'][0]['content']
    assert set(ai.plan(query)['payload']['documents'][0])=={'revision_id','country','source_name','title','text','paragraphs'}
