import json
from app.codex_provider import Server,strict_output_schema
from app import ai,db
from test_core import save_query

def test_strict_schemas_cover_nested_objects():
    def check(node):
        if isinstance(node,list):
            for value in node: check(value)
        elif isinstance(node,dict):
            assert 'default' not in node
            if node.get('type')=='object':
                assert node['additionalProperties'] is False
                assert set(node['required'])==set(node['properties'])
            for value in node.values(): check(value)
    for kind in ['summary','crossings']: check(strict_output_schema(kind))

def test_codex_wire_result_and_usage(monkeypatch,tmp_path):
    server=Server();server.cwd=tmp_path
    monkeypatch.setattr(server,'status',lambda:{'connected':True,'models':[{'id':'test-model','efforts':['low']}]})
    calls=[]
    def call(method,params,*args,**kwargs):
        calls.append((method,params))
        if method=='thread/start': return {'thread':{'id':'thread1'}}
        assert params['effort']=='low' and params['sandboxPolicy']=={'type':'readOnly'}
        assert 'paragraph_ids' in json.dumps(params['outputSchema'])
        return {'turn':{'id':'turn1'}}
    monkeypatch.setattr(server,'call',call)
    events=iter([
        {'method':'thread/tokenUsage/updated','params':{'threadId':'thread1','tokenUsage':{'last':{'inputTokens':30,'outputTokens':20}}}},
        {'method':'item/completed','params':{'threadId':'thread1','item':{'type':'agentMessage','phase':'final_answer','text':json.dumps({'summaries':[{'country':'BR','text':'Teste','paragraph_ids':['r1p0']}],'gaps':[]})}}},
        {'method':'turn/completed','params':{'threadId':'thread1','turn':{'id':'turn1','status':'completed'}}},
    ])
    monkeypatch.setattr(server,'receive',lambda deadline:next(events))
    result,usage=server.generate({'model':'test-model','analysis_kind':'summary'},{'documents':[]},'prompt',None)
    assert result.summaries[0].paragraph_ids==['r1p0']
    assert usage['provider']=='codex' and usage['input_tokens']==30 and usage['output_tokens']==20
    assert calls[0][1]['ephemeral'] is True

def test_codex_plan_uses_selected_model_without_api_key(synthetic_document):
    query,_=save_query(synthetic_document)
    settings=db.setting();settings.provider='codex';settings.codex_model='chosen-model';db.save_settings(settings)
    plan=ai.plan(query)
    assert plan['provider']=='codex' and plan['model']=='chosen-model'
    assert 'assinatura' in plan['notice']
