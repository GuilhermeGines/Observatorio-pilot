"""One editorial image per article, associated by document, never by visual inference."""
import ipaddress
import re
from urllib.parse import urljoin,urlsplit

def safe_url(value):
    if not isinstance(value,str): return False
    try:
        p=urlsplit(value)
        if p.scheme not in {'http','https'} or not p.hostname or p.username or p.password or p.port not in {None,80,443}: return False
        try:
            if not ipaddress.ip_address(p.hostname).is_global: return False
        except ValueError:
            if '.' not in p.hostname or p.hostname.endswith(('.local','.localhost')): return False
    except ValueError: return False
    return not re.search(r'(logo|favicon|avatar|banner|advert|tracking|pixel)',p.path,re.I)

def extract(soup,articles,url):
    candidates=[]
    for article in articles:
        values=article.get('image',[])
        if not isinstance(values,list): values=[values]
        for value in values:
            candidates.append({'url':value.get('url',value.get('contentUrl','')) if isinstance(value,dict) else value,
                               'caption':value.get('caption','') if isinstance(value,dict) else '',
                               'credit':value.get('creditText','') if isinstance(value,dict) else ''})
    meta=soup.select_one('meta[property="og:image"],meta[name="twitter:image"]')
    if meta: candidates.append({'url':meta.get('content',''),'caption':'','credit':''})
    for img in soup.select('article figure img, main figure img'):
        figure=img.find_parent('figure');caption=figure.find('figcaption') if figure else None
        candidates.append({'url':img.get('data-src') or img.get('src',''),
                           'caption':caption.get_text(' ',strip=True) if caption else '',
                           'credit':img.get('data-credit','')})
    for item in candidates:
        if not isinstance(item['url'],str): continue
        item['url']=urljoin(url,item['url'])
        if safe_url(item['url']):
            for img in soup.select('article figure img, main figure img'):
                if urljoin(url,img.get('data-src') or img.get('src',''))==item['url']:
                    figure=img.find_parent('figure');caption=figure.find('figcaption') if figure else None
                    if caption and not item['caption']: item['caption']=caption.get_text(' ',strip=True)
                    if not item['credit']: item['credit']=img.get('data-credit','')
                    break
            return [{**item,'caption':str(item['caption'])[:1000],'credit':str(item['credit'])[:300],'article_url':url}]
    return []

async def download(revision):
    from . import db
    from .collection import Reader
    import hashlib
    doc=db.read_revision(revision)
    images=doc.get('images',[]) if doc else []
    if not images or not safe_url(images[0].get('url')): raise ValueError('Imagem editorial indisponível.')
    url=images[0]['url'];key=hashlib.sha256(url.encode()).hexdigest()
    directory=db.DATA/'images';directory.mkdir(exist_ok=True)
    for ext,mime in [('jpg','image/jpeg'),('png','image/png'),('webp','image/webp'),('gif','image/gif')]:
        path=directory/(key+'.'+ext)
        if path.exists(): return path,mime
    # Reader checks public DNS, redirects, robots.txt and an 8 MB limit.
    source={'id':'article_image','domains':[urlsplit(url).hostname]}
    reader=Reader()
    try: content,ctype,_=await reader.get(url,source)
    finally: await reader.close()
    signatures=[('jpg','image/jpeg',content.startswith(b'\xff\xd8\xff')),('png','image/png',content.startswith(b'\x89PNG\r\n\x1a\n')),('gif','image/gif',content[:6] in {b'GIF87a',b'GIF89a'}),('webp','image/webp',content[:4]==b'RIFF' and content[8:12]==b'WEBP')]
    for ext,mime,valid in signatures:
        if valid and ctype.split(';')[0].strip().lower()==mime:
            path=directory/(key+'.'+ext);path.write_bytes(content);return path,mime
    raise ValueError('A fonte não retornou uma imagem compatível.')
