"""Local estimate only: never represents the Google project's authoritative balance."""
import json
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from . import db, profiles

MODEL='gemini-3.1-flash-lite'

def estimate(rows,config,now=None):
    now=now or datetime.now(timezone.utc)
    pacific=now.astimezone(ZoneInfo('America/Los_Angeles'))
    start=pacific.replace(hour=0,minute=0,second=0,microsecond=0)
    reset=start+timedelta(days=1)
    minute=now-timedelta(seconds=60)
    daily=recent=tokens=0
    partial=False
    expirations=[]
    for row in rows:
        usage=json.loads(row['usage'])
        if usage.get('provider')!='gemini' or usage.get('cache_only') or row['model'].removeprefix('models/')!=MODEL: continue
        stamp=datetime.fromisoformat(usage.get('requested_at') or row['created_at'])
        if stamp.tzinfo is None: stamp=stamp.replace(tzinfo=timezone.utc)
        if start<=stamp<=now: daily+=1
        if minute<stamp<=now:
            recent+=1
            expirations.append(stamp+timedelta(seconds=60))
            if usage.get('input_tokens') is None: partial=True
            else: tokens+=usage['input_tokens']
    windows=[]
    for name,count,limit,renew in [('Por dia',daily,config.gemini_31_rpd,reset),('Por minuto',recent,config.gemini_31_rpm,min(expirations) if expirations else None),('Tokens/min',tokens,config.gemini_31_tpm,min(expirations) if expirations else None)]:
        windows.append({'label':name,'used':count,'limit':limit,'remaining_percent':max(0,round(100*(1-count/limit))) if limit else None,
                        'resets_at':renew.isoformat() if renew else None,'partial':partial if name=='Tokens/min' else False})
    return {'model':MODEL,'estimated':True,'windows':windows}

def current(rows):
    config=db.setting()
    if config.provider!='gemini' or config.gemini_model.removeprefix('models/')!=MODEL:
        matches=[p for p in profiles.available() if p['provider']=='gemini' and p['model'].removeprefix('models/')==MODEL]
        if not matches: return None
        config=profiles.configuration(matches[-1]['id'])
    return estimate(rows,config)
