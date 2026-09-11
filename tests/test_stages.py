from types import SimpleNamespace
import pytest
from app import ai,db
from app.main import app
from app.models import ParagraphSummaryOutput,CrossingsOutput
from test_core import save_query,synthetic_analysis

@pytest.mark.asyncio
async def test_separate_stages_and_cache(synthetic_document):
    second,_=db.save_document('agbr','https://agenciabrasil.ebc.com.br/test/second',synthetic_document|{'title':'Samsung energia pesquisa adicional','text':synthetic_document['text']+' Outro documento.'})
    query,revision=save_query(synthetic_document)
    settings=db.setting();settings.allow_ai=True;db.save_settings(settings)
    calls=[]
    async def parse(**kwargs):
        calls.append(kwargs['text_format'])
        result=ParagraphSummaryOutput(summaries=[{'country':'BR','text':'Teste','paragraph_ids':[ai.plan(query)['payload']['documents'][0]['paragraphs'][0]['id']]}],gaps=[]) if kwargs['text_format'] is ParagraphSummaryOutput else CrossingsOutput(comparisons=[],cross_statements=[],gaps=['Sem conclusão suficiente.'])
        return SimpleNamespace(output_parsed=result,usage=None)
    client=SimpleNamespace(responses=SimpleNamespace(parse=parse))
    with pytest.raises(ValueError,match='primeiro'):
        await ai.analyze(query,client=client,kind='crossings')
    summary=await ai.analyze(query,client=client)
    assert calls==[ParagraphSummaryOutput]
    assert summary['result']['script']=='' and summary['result']['comparisons']==[]
    assert ai.plan(query)['pair_count']==0
    assert ai.plan(query,'crossings')['pair_count']>0
    crossing=await ai.analyze(query,client=client,kind='crossings')
    assert crossing['config']['summary_id']==summary['id']
    assert (await ai.analyze(query,client=client))['id']==summary['id']
    assert (await ai.analyze(query,client=client,kind='crossings'))['id']==crossing['id']
    newer=await ai.analyze(query,client=client,regenerate=True)
    newcross=await ai.analyze(query,client=client,kind='crossings')
    assert newcross['config']['summary_id']==newer['id'] and newcross['id']!=crossing['id']
    assert calls==[ParagraphSummaryOutput,CrossingsOutput,ParagraphSummaryOutput,CrossingsOutput]
    assert not any('/audio' in r.path for r in app.routes)
