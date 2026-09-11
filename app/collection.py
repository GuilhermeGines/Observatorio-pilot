"""Leitura limitada a fontes cadastradas, com evidência e falhas explícitas."""
import asyncio
import hashlib
import io
import ipaddress
import json
import re
import socket
import unicodedata
from datetime import datetime, timedelta, timezone
from urllib.parse import urlsplit, urlunsplit, urljoin, parse_qsl, urlencode
from urllib.robotparser import RobotFileParser
from zoneinfo import ZoneInfo
import feedparser
import httpx
import trafilatura
from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_date
from pypdf import PdfReader
from . import db
from .catalog import BY_ID, SOURCES, selected_sources

USER_AGENT = 'ObservatorioFontes/0.1 (personal research; bounded RSS and public-page reader)'
KEYWORDS = {
 'geopolitica':['diploma','foreign','treaty','sanction','international','geopol','外交','международ','санкц'],
 'politica':['eleiç','election','president','congress','governo','minister','parliament','选举','президент','правитель'],
 'ciencia':['research','study','scient','pesquisa','estudo','ciên','科学','исследов','наук'],
 'fisica':['physic','física','quantum','quânt','particle','物理','квант','физик'],
 'astronomia':['space','nasa','astronom','planet','galax','espac','太空','космос','космич'],
 'tecnologia':['technolog','tecnolog','artificial intelligence','inteligência artificial','semiconductor','samsung','iphone','ipad','smartphone','apple','software','人工智能','технолог','интеллект'],
 'economia':['econom','trade','comércio','inflation','inflação','gdp','pib','tariff','market','经济','торгов','эконом'],
 'clima':['climat','energy','energia','ambiente','emission','carbon','气候','能源','энерг','климат'],
 'defesa':['militar','defen','segurança','security','war','guerra','missile','军事','обороны','военн'],
 'saude':['health','saúde','medic','vaccine','vacina','disease','cancer','hospital','医学','здоров','медицин']}

def folded(text):
    return ''.join(c for c in unicodedata.normalize('NFKD',text.casefold()) if not unicodedata.combining(c))

def topics_for(text):
    text = folded(text)
    return [topic for topic, terms in KEYWORDS.items() if any(folded(t) in text for t in terms)]

def canonical(url):
    parts = urlsplit(url)
    query = urlencode([(k,v) for k,v in parse_qsl(parts.query,keep_blank_values=True) if not k.lower().startswith('utm_') and k.lower() not in {'fbclid','gclid'}])
    return urlunsplit((parts.scheme.lower(),parts.netloc.lower(),parts.path or '/',query,''))

def allowed(url, source):
    p = urlsplit(url)
    host = (p.hostname or '').lower()
    try:
        port=p.port
    except ValueError:
        return False
    if source.get('path_prefix') and p.path!='/robots.txt':
        if not p.path.startswith(source['path_prefix']):
            return False
    return p.scheme in {'https','http'} and not p.username and port in {None,80,443} and any(host == d.removeprefix('www.') or host.endswith('.'+d.removeprefix('www.')) for d in source['domains'] if d)

def publication(raw, zone):
    if not raw:
        return None, None
    try:
        # No relative dates or missing year: never turn an unverified date into today's date.
        if not re.search(r'\d{4}', str(raw)):
            return None, str(raw)
        value = parse_date(str(raw), fuzzy=False, tzinfos={'EST':-18000,'EDT':-14400,'CST':-21600,'CDT':-18000,'MST':-25200,'MDT':-21600,'PST':-28800,'PDT':-25200,'MSK':10800})
        if value.tzinfo is None:
            value = value.replace(tzinfo=ZoneInfo(zone))
        return value.astimezone(ZoneInfo(zone)).isoformat(), str(raw)
    except (ValueError,OverflowError,TypeError):
        return None, str(raw)

def classify(source, title, text, author=''):
    sample = folded(title+' '+author+' '+text[:1800])
    if any(x in sample for x in ['opinion:', 'opiniao:', 'editorial:', 'op-ed', '观点', 'мнение:']):
        kind = 'opiniao'
    elif source['kind'] != 'jornalismo':
        kind = 'comunicado_institucional'
    elif any(x in sample for x in ['interview with','entrevista com','интервью с']):
        kind = 'entrevista_sinalizada'
    elif any(x in sample for x in ['investigation by','investigacao da','investigacao de']):
        kind = 'investigacao_sinalizada'
    else:
        kind = 'apuracao_nao_verificada'
    origin = ''
    # Only explicit bylines/credits imply syndication. A mention of Reuters in prose is insufficient.
    credits = folded(author+' '+text[-800:])
    for agency in ['reuters','associated press','agence france-presse','agencia brasil','xinhua','tass','interfax']:
        if agency in folded(author) or re.search(r'(?:com informacoes (?:da|de)|with (?:reporting|information) from|por|by|source:)\s+(?:the\s+)?'+re.escape(agency), credits):
            origin = agency
            kind = 'reproducao_agencia'
            break
    return kind, origin

def clean(text):
    return ' '.join(BeautifulSoup(text or '', 'html.parser').get_text(' ',strip=True).split())

def base_body(source, title, summary='', published=None, author=''):
    pub, raw = publication(published,source['timezone'])
    return {'title':clean(title),'text':clean(summary),'published_at':pub,'published_raw':raw,
            'publication_basis':'feed' if pub else 'nao_verificada','language':source['language'],
            'country':source['country'],'topics':topics_for(title+' '+summary),'author':author,
            'access':'resumo_do_feed' if summary else 'somente_metadados',
            'access_note':'Somente o trecho distribuído pela fonte foi lido. Texto integral não confirmado.',
            'study_links':[], 'review_status':'nao_verificado'}

def feed_entries(content, source):
    parsed = feedparser.parse(content)
    result = []
    seen=set()
    for entry in parsed.entries[:60]:
        url = canonical(urljoin(source['channel'],entry.get('link','')))
        if not entry.get('link') or not allowed(url,source) or url in seen:
            continue
        seen.add(url)
        body = base_body(source,entry.get('title','Sem título'),entry.get('summary',''),entry.get('published'),entry.get('author',''))
        # Explicitly supplied full content is kept as a feed excerpt until the article is read.
        result.append((url,body))
    return result

def page_entries(html, source):
    soup = BeautifulSoup(html,'html.parser')
    result, seen = [], set()
    for el in soup.select('nav,footer,header,script,style'):
        el.decompose()
    # Prefer the editorial body over site menus, especially on government portals.
    area=soup.select_one('#content-core, #content, main') or soup
    for anchor in area.select('a[href]'):
        title = anchor.get_text(' ',strip=True)
        url = canonical(urljoin(source['channel'],anchor.get('href','')))
        p = urlsplit(url)
        if len(title)<(8 if source.get('language')=='zh' else 28) or len(title)>350 or url in seen or not allowed(url,source):
            continue
        if len(p.path.strip('/'))<12 or re.search(r'/(tag|category|author|search|login|subscribe|about|contact|video|photo|podcast)s?/',p.path,re.I):
            continue
        if source['id'] in {'itamaraty','inpe'} and not p.path.startswith(urlsplit(source['channel']).path.rstrip('/')+'/'):
            continue
        if re.search(r'\.(jpg|jpeg|png|svg|mp4|mp3|zip)$',p.path,re.I):
            continue
        seen.add(url)
        result.append((url,base_body(source,title)))
        if len(result)>=30:
            break
    return result

def json_objects(value):
    if isinstance(value,dict):
        yield value
        for item in value.values():
            yield from json_objects(item)
    elif isinstance(value,list):
        for item in value:
            yield from json_objects(item)

def extract_article(content, url, source, body, content_type='text/html'):
    result = dict(body)
    if 'application/pdf' in content_type or urlsplit(url).path.lower().endswith('.pdf'):
        reader = PdfReader(io.BytesIO(content))
        result['text'] = '\n\n'.join((p.extract_text() or '') for p in reader.pages[:80])[:180000]
        result['access'] = 'pdf_extraido'
        result['access_note'] = 'Texto extraído de até 80 páginas; tabelas e imagens podem não ter sido interpretadas. Data deve ser verificada no documento.'
    else:
        html = content.decode('utf-8',errors='replace') if isinstance(content,bytes) else content
        soup = BeautifulSoup(html,'html.parser')
        objects=[]
        for script in soup.select('script[type="application/ld+json"]'):
            try:
                objects += list(json_objects(json.loads(script.string or script.get_text())))
            except (ValueError,TypeError):
                pass
        articles=[o for o in objects if any(t in str(o.get('@type','')) for t in ['Article','Report','Posting'])]
        paywall=any(o.get('isAccessibleForFree') in [False,'False','false'] for o in objects)
        date_raw=next((o.get('datePublished') for o in articles if o.get('datePublished')),None)
        if not date_raw:
            tag=soup.select_one('meta[property="article:published_time"],meta[name="citation_publication_date"],meta[name="datePublished"],meta[name="publishdate"],meta[name="PubDate"]')
            date_raw=tag.get('content') if tag else None
        if not date_raw and source['id']=='globaltimes':
            tag=soup.select_one('.pub_time')
            date_raw=tag.get_text(' ',strip=True).removeprefix('Published:').strip() if tag else None
        if not date_raw and source['id'] in {'itamaraty','inpe'}:
            tag=soup.select_one('.documentPublished .value, .documentPublished')
            if tag:
                match=re.search(r'(\d{2})/(\d{2})/(\d{4})\s+(\d{2})h(\d{2})',tag.get_text(' ',strip=True))
                if match:
                    day,month,year,hour,minute=match.groups()
                    date_raw=f'{year}-{month}-{day}T{hour}:{minute}:00'
        pub,raw=publication(date_raw,source['timezone'])
        if pub:
            result.update(published_at=pub,published_raw=raw,publication_basis='metadado_editorial')
        title=next((o.get('headline') for o in articles if o.get('headline')),None)
        if not title:
            h=soup.select_one('h1')
            title=h.get_text(' ',strip=True) if h else None
        if title and len(clean(str(title)))>=15:
            result['title']=clean(str(title))
        author=next((o.get('author') for o in articles if o.get('author')),None)
        if author:
            result['author']='; '.join(str(o.get('name','')) for o in json_objects(author)) if isinstance(author,(dict,list)) else str(author)
        if paywall:
            result['access']='parcial_restrito'
            result['access_note']='A fonte sinaliza conteúdo restrito. Mantido apenas resumo/metadados distribuídos; corpo protegido excluído.'
        else:
            text=trafilatura.extract(html,include_comments=False,include_tables=True,favor_precision=True,deduplicate=True)
            if text and len(text)>200:
                result['text']=text[:180000]
                result['access']='texto_extraido'
                result['access_note']='Texto publicamente retornado e extraído. Extração automática pode omitir elementos; consulte o original.'
        links=[]
        for a in soup.select('a[href]'):
            link=urljoin(url,a['href'])
            host=(urlsplit(link).hostname or '').lower()
            if any(host==d or host.endswith('.'+d) for d in ['doi.org','arxiv.org','biorxiv.org','medrxiv.org','nature.com','science.org','pubmed.ncbi.nlm.nih.gov','pmc.ncbi.nlm.nih.gov','zenodo.org','clinicaltrials.gov']):
                links.append({'url':link,'label':a.get_text(' ',strip=True)[:180] or 'Estudo ou dados referenciados','status':'preprint' if any(d in host for d in ['arxiv.org','biorxiv.org','medrxiv.org']) else 'revisao_nao_verificada'})
        result['study_links']=list({x['url']:x for x in links}.values())[:20]
        if result['study_links'] and all(x['status']=='preprint' for x in result['study_links']):
            result['review_status']='links_para_preprint'
    result['topics']=topics_for(result['title']+' '+result['text'])
    result['genre'],result['origin']=classify(source,result['title'],result['text'],result.get('author',''))
    return result

class FetchError(Exception):
    pass

class Reader:
    def __init__(self):
        self.client=httpx.AsyncClient(timeout=httpx.Timeout(18,connect=8),headers={'User-Agent':USER_AGENT,'Accept':'application/rss+xml, application/atom+xml, text/html, application/pdf, */*'},follow_redirects=False,trust_env=False)
        self.robots={}
        self.robot_lock=asyncio.Lock()

    async def close(self):
        await self.client.aclose()

    async def raw(self,url,source,respect_robots=False):
        for _ in range(6):
            if not allowed(url,source):
                raise FetchError('Redirecionamento ou domínio fora da fonte cadastrada; não seguido.')
            if respect_robots:
                await self.check_robots(url,source)
            host=urlsplit(url).hostname
            addresses=await asyncio.get_running_loop().getaddrinfo(host,None,type=socket.SOCK_STREAM)
            if not addresses or any(not ipaddress.ip_address(x[4][0]).is_global for x in addresses):
                raise FetchError('Endereço de rede local ou reservado recusado.')
            async with self.client.stream('GET',url) as response:
                if response.status_code in {301,302,303,307,308}:
                    url=urljoin(url,response.headers.get('location',''))
                    continue
                if response.status_code>=400:
                    raise FetchError(f'HTTP {response.status_code}; conteúdo não recuperado.')
                chunks=[]
                size=0
                async for chunk in response.aiter_bytes():
                    size+=len(chunk)
                    if size>8_000_000:
                        raise FetchError('Documento excede limite de 8 MB do piloto.')
                    chunks.append(chunk)
                return b''.join(chunks), response.headers.get('content-type',''), str(response.url)
        raise FetchError('Limite de redirecionamentos atingido.')

    async def check_robots(self,url,source):
        origin=urlunsplit((*urlsplit(url)[:2],'','',''))
        async with self.robot_lock:
            if origin not in self.robots:
                robot=RobotFileParser()
                try:
                    content,_,_=await self.raw(origin+'/robots.txt',source)
                    robot.parse(content.decode('utf-8',errors='replace').splitlines())
                    self.robots[origin]=robot
                except FetchError as error:
                    if 'HTTP 404' in str(error) or 'HTTP 410' in str(error):
                        robot.parse([])
                        self.robots[origin]=robot
                    else:
                        self.robots[origin]=None
                except (httpx.HTTPError,OSError):
                    self.robots[origin]=None
        robot=self.robots[origin]
        if robot is None:
            raise FetchError('Não foi possível verificar robots.txt; coleta adiada.')
        if not robot.can_fetch(USER_AGENT,url):
            raise FetchError('Leitura não permitida pelo robots.txt da fonte.')
        # Honor declared delay, bounded by deferring overly slow sites.
        delay=robot.crawl_delay(USER_AGENT) or robot.crawl_delay('*') or 0
        if delay>15:
            raise FetchError('A fonte exige intervalo superior ao limite desta coleta; coleta adiada.')
        if delay:
            await asyncio.sleep(delay)

    async def get(self,url,source):
        return await self.raw(url,source,respect_robots=True)

async def collect_source(reader,source,query,query_id,article_limit):
    detail={'channel':source['channel'],'connector':source['connector'],'candidates':0,'read':0,'saved':0,'failures':[],
            'scope':'Janela recente do canal; sem varredura histórica completa.'}
    try:
        content,content_type,_=await reader.get(source['channel'],source)
        if source['connector']=='feed':
            entries=feed_entries(content,source)
        else:
            entries=page_entries(content.decode('utf-8',errors='replace'),source)
        detail['candidates']=len(entries)
        if not entries:
            raise FetchError('Canal respondeu, mas nenhum item elegível foi identificado. Integração sem conteúdo validado.')
        # Filter the publication date before expensive full-text extraction when a feed supplies it.
        def in_dates(body):
            return not body['published_at'] or str(query.start)<=body['published_at'][:10]<=str(query.end)
        eligible=[(url,b) for url,b in entries if in_dates(b)]
        # Prefer keyword candidates, but read other items too within the explicit source limit.
        eligible.sort(key=lambda x: folded(query.keyword) not in folded(x[1]['title']+' '+x[1]['text']))
        to_read={url for url,_ in eligible[:article_limit]}
        dates=[b['published_at'][:10] for _,b in entries if b['published_at']]
        detail['feed_min_date']=min(dates) if dates else None
        detail['feed_max_date']=max(dates) if dates else None
        for url,body in entries:
            if url in to_read:
                try:
                    article,ctype,final=await reader.get(url,source)
                    body=extract_article(article,final,source,body,ctype)
                    detail['read']+=int(body['access'] in {'texto_extraido','pdf_extraido'})
                except (FetchError,httpx.HTTPError,OSError,ValueError) as error:
                    body['access_note']+=' Falha na leitura: '+safe_error(error)
                    detail['failures'].append({'url':url,'reason':safe_error(error)})
            if 'genre' not in body:
                body['genre'],body['origin']=classify(source,body['title'],body['text'],body.get('author',''))
            _,created=db.save_document(source['id'],url,body)
            detail['saved']+=int(created)
        detail['limited']=len(eligible)>article_limit
        detail['message']=f"{len(entries)} itens identificados; {detail['read']} textos extraídos. Limite de {article_limit} leituras por fonte."
        stale=dates and max(dates)<(datetime.now(timezone.utc)-timedelta(days=60)).date().isoformat()
        status='desatualizado' if stale else ('parcial' if detail['failures'] or detail['read']==0 else 'disponivel')
    except Exception as error:
        status='indisponivel'
        detail['message']=safe_error(error)
    db.log(source['id'],status,detail,query_id)
    return {'source_id':source['id'],'status':status,'detail':detail,'checked_at':db.now()}

def safe_error(error):
    if isinstance(error,FetchError):
        return str(error)[:300]
    if isinstance(error,httpx.TimeoutException):
        return 'Tempo limite da fonte atingido; itens existentes continuam disponíveis.'
    return f'Falha de leitura ({type(error).__name__}); conteúdo não recuperado.'

async def collect(query,query_id,progress=None):
    settings=db.setting()
    selected=selected_sources(query)
    semaphore=asyncio.Semaphore(6)
    results=[]
    async def one(source):
        if source['id'] in settings.disabled_sources:
            result={'source_id':source['id'],'status':'desativada','detail':{'message':'Fonte desativada nas configurações; excluída desta consulta.'}}
        else:
            async with semaphore:
                reader=Reader()
                try:
                    result=await collect_source(reader,source,query,query_id,settings.articles_per_source)
                finally:
                    await reader.close()
        results.append(result)
        if progress:
            progress(len(results),len(selected),source['name'])
    await asyncio.gather(*(one(s) for s in selected))
    return results
