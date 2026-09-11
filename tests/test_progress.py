"""Verificação curta da integração por streaming; nenhuma inferência real."""
import json
import httpx
import pytest
from app import ai,db,ollama_local
from app.queries import read_query
from test_core import save_query,synthetic_analysis

@pytest.mark.asyncio
@pytest.mark.parametrize('truncated',[False,True])
async def test_local_stream_progress_and_save(synthetic_document,monkeypatch,truncated):
    query,revision=save_query(synthetic_document)
    settings=db.setting()
    settings.provider='ollama';settings.allow_ai=True
    settings.ollama_context=32768;settings.max_output_tokens=32768
    db.save_settings(settings)
    ai.ANALYSIS_PROGRESS.clear()
    from app.models import ParagraphSummaryOutput
    output=ParagraphSummaryOutput(summaries=[{'country':'BR','text':'Resumo de teste','paragraph_ids':[ai.plan(query)['payload']['documents'][0]['paragraphs'][0]['id']]}],gaps=[]).model_dump_json()
    def handle(request):
        if request.url.path=='/api/show':
            return httpx.Response(200,json={'model_info':{}})
        body=json.loads(request.content)
        assert body['stream'] is True
        assert 3000<body['options']['num_predict']<32768
        return httpx.Response(200,text='\n'.join(json.dumps(x) for x in [
            {'message':{'content':output[:30]},'done':False},
            {'message':{'content':output[30:]},'done':False},
            {'message':{'content':''},'done':True,'done_reason':'length' if truncated else 'stop','eval_count':100}]))
    original=httpx.AsyncClient
    monkeypatch.setattr(ollama_local.httpx,'AsyncClient',lambda **kwargs:original(transport=httpx.MockTransport(handle),**kwargs))
    if truncated:
        with pytest.raises(ValueError,match='limite'):
            await ai.analyze(query)
        assert ai.ANALYSIS_PROGRESS[query['id']]['state']=='error'
        assert not read_query(query['id'])['analyses']
    else:
        result=await ai.analyze(query)
        assert read_query(query['id'])['analyses'][0]['id']==result['id']
        assert ai.ANALYSIS_PROGRESS[query['id']]['percent']==100
