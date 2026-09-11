import hashlib
import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from .catalog import SOURCES

ROOT = Path(__file__).resolve().parent.parent
DATA = Path(os.environ.get('OBS_DATA_DIR') or ROOT / 'data').resolve()

def now():
    return datetime.now(timezone.utc).isoformat()

def dumps(value):
    return json.dumps(value, ensure_ascii=False, separators=(',',':'), default=str)

@contextmanager
def connect():
    DATA.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DATA / 'observatorio.sqlite3', timeout=30)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def init():
    for folder in ['documents','audio','images','backups']:
        (DATA / folder).mkdir(parents=True, exist_ok=True)
    with connect() as db:
        db.execute('PRAGMA journal_mode=WAL')
        db.executescript('''
        CREATE TABLE IF NOT EXISTS summary_cache(key TEXT PRIMARY KEY,value TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS sources(id TEXT PRIMARY KEY,metadata TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'nao_testado',checked_at TEXT,detail TEXT);
        CREATE TABLE IF NOT EXISTS documents(id INTEGER PRIMARY KEY,url TEXT NOT NULL UNIQUE,source_id TEXT NOT NULL REFERENCES sources(id),created_at TEXT NOT NULL,last_seen TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS revisions(id INTEGER PRIMARY KEY,document_id INTEGER NOT NULL REFERENCES documents(id),hash TEXT NOT NULL,body TEXT NOT NULL,created_at TEXT NOT NULL);
        CREATE INDEX IF NOT EXISTS revision_doc ON revisions(document_id,id);
        CREATE TABLE IF NOT EXISTS queries(id TEXT PRIMARY KEY,filters TEXT NOT NULL,result TEXT,created_at TEXT NOT NULL,saved_at TEXT,title TEXT NOT NULL,status TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS analyses(id TEXT PRIMARY KEY,query_id TEXT NOT NULL REFERENCES queries(id),version INTEGER NOT NULL,config TEXT NOT NULL,result TEXT NOT NULL,usage TEXT NOT NULL,created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS audio(id TEXT PRIMARY KEY,analysis_id TEXT NOT NULL REFERENCES analyses(id),script TEXT NOT NULL,path TEXT NOT NULL,model TEXT NOT NULL,voice TEXT NOT NULL,created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS logs(id INTEGER PRIMARY KEY,query_id TEXT,source_id TEXT NOT NULL,status TEXT NOT NULL,detail TEXT NOT NULL,created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS usage(id INTEGER PRIMARY KEY,operation TEXT NOT NULL,model TEXT NOT NULL,usage TEXT NOT NULL,created_at TEXT NOT NULL);
        ''')
        db.execute("INSERT OR IGNORE INTO meta VALUES('schema_version','1')")
        for source in SOURCES:
            db.execute('INSERT INTO sources(id,metadata) VALUES(?,?) ON CONFLICT(id) DO UPDATE SET metadata=excluded.metadata',(source['id'], dumps(source)))
        # Jobs interrupted by closing the program are never left looking active forever.
        db.execute("UPDATE queries SET status='interrompida' WHERE status='coletando'")

def setting():
    from .models import SettingsInput
    with connect() as db:
        row = db.execute("SELECT value FROM meta WHERE key='settings'").fetchone()
    return SettingsInput.model_validate_json(row['value']) if row else SettingsInput()

def save_settings(value):
    with connect() as db:
        db.execute("INSERT INTO meta VALUES('settings',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",(value.model_dump_json(),))

def save_document(source_id, url, body):
    content = dumps(body)
    fingerprint={k:v for k,v in body.items() if k not in {'access_note'}}
    digest = hashlib.sha256(dumps(fingerprint).encode()).hexdigest()
    stamp = now()
    with connect() as db:
        db.execute('INSERT INTO documents(url,source_id,created_at,last_seen) VALUES(?,?,?,?) ON CONFLICT(url) DO UPDATE SET last_seen=excluded.last_seen',(url,source_id,stamp,stamp))
        doc = db.execute('SELECT id FROM documents WHERE url=?',(url,)).fetchone()['id']
        previous = db.execute('SELECT id,hash,body FROM revisions WHERE document_id=? ORDER BY id DESC LIMIT 1',(doc,)).fetchone()
        if previous:
            old=json.loads(previous['body'])
            # A failed/reduced re-read must not replace an earlier readable document.
            # The separate collection log records this failure; original collection time stays intact.
            if old.get('access') in {'texto_extraido','pdf_extraido'} and body.get('access') not in {'texto_extraido','pdf_extraido'}:
                return previous['id'],False
        if previous and previous['hash'] == digest:
            return previous['id'], False
        cursor = db.execute('INSERT INTO revisions(document_id,hash,body,created_at) VALUES(?,?,?,?)',(doc,digest,content,stamp))
        revision = cursor.lastrowid
        # Original extracted text and metadata form a readable, portable document.
        (DATA/'documents'/f'{revision}.json').write_text(content,encoding='utf-8')
        return revision, True

def revision_rows(latest=True):
    sql = '''SELECT r.id AS revision_id,r.document_id,r.created_at AS collected_at,d.url,d.source_id,r.body
             FROM revisions r JOIN documents d ON r.document_id=d.id'''
    if latest:
        sql += ' WHERE r.id=(SELECT MAX(r2.id) FROM revisions r2 WHERE r2.document_id=d.id)'
    with connect() as db:
        return [dict(row) | json.loads(row['body']) for row in db.execute(sql)]

def read_revision(revision):
    with connect() as db:
        row = db.execute('SELECT r.*,d.url,d.source_id FROM revisions r JOIN documents d ON d.id=r.document_id WHERE r.id=?',(revision,)).fetchone()
    return dict(row) | json.loads(row['body']) if row else None

def log(source_id, status, detail, query_id=None):
    stamp = now()
    with connect() as db:
        db.execute('INSERT INTO logs(query_id,source_id,status,detail,created_at) VALUES(?,?,?,?,?)',(query_id,source_id,status,dumps(detail),stamp))
        db.execute('UPDATE sources SET status=?,detail=?,checked_at=? WHERE id=?',(status,dumps(detail),stamp,source_id))

def sources():
    with connect() as db:
        return [json.loads(row['metadata']) | {'status':row['status'],'checked_at':row['checked_at'],'detail':json.loads(row['detail']) if row['detail'] else None} for row in db.execute('SELECT * FROM sources')]
