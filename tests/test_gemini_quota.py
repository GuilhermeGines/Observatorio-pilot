from datetime import datetime,timezone
from app.gemini_quota import estimate,MODEL
from app.models import SettingsInput
from app import db

def row(stamp,**usage):
    return {'model':MODEL,'created_at':stamp,'usage':db.dumps({'provider':'gemini','input_tokens':30,**usage})}

def test_daily_reset_and_minute_are_separate():
    config=SettingsInput(gemini_31_rpm=5,gemini_31_tpm=100,gemini_31_rpd=20)
    now=datetime(2026,9,12,7,0,30,tzinfo=timezone.utc)
    data=[row('2026-09-12T06:59:50+00:00'),row('2026-09-12T07:00:10+00:00'),row('2026-09-12T07:00:15+00:00',cache_only=True)]
    data.append(dict(row('2026-09-12T07:00:12+00:00'),model='gemini-3.5-flash'))
    result=estimate(data,config,now)['windows']
    assert result[0]['used']==1 and result[0]['remaining_percent']==95
    assert result[1]['used']==2 and result[2]['used']==60
    assert result[0]['resets_at']=='2026-09-13T00:00:00-07:00'

def test_unknown_limits_and_missing_tokens():
    now=datetime(2026,1,12,8,0,30,tzinfo=timezone.utc)
    result=estimate([row('2026-01-12T08:00:10+00:00',input_tokens=None)],SettingsInput(),now)['windows']
    assert all(w['remaining_percent'] is None for w in result)
    assert result[2]['partial'] and result[0]['used']==1
    assert result[0]['resets_at'].endswith('-08:00')
