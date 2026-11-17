import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

DIR = Path(__file__).parent
DSN = 'host=localhost port=5432 dbname=announcements user=postgres password=postgres'


def query(sql, params=()):
    with psycopg.connect(DSN, row_factory=dict_row) as conn:
        cur = conn.execute(sql, params)
        return cur.fetchall() if cur.description else cur.rowcount


FIELDS = """announcement_id AS id, announcement_title AS title, announcement_text AS text,
    announcement_created_at AS created_at, announcement_author_id AS author_id"""


class Handler(BaseHTTPRequestHandler):
    def send(self, status, body=b'', content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, status, data):
        self.send(status, json.dumps(data, default=lambda d: d.isoformat()).encode())

    def do_OPTIONS(self):
        self.send(204)

    def do_GET(self):
        if self.path == '/announcements.js':
            self.send(200, (DIR / 'dist' / 'announcements.js').read_bytes(), 'text/javascript; charset=utf-8')
        elif self.path == '/api/announcements':
            self.send_json(200, query(f'SELECT {FIELDS} FROM announcements ORDER BY announcement_id DESC'))
        else:
            self.send_json(404, {'error': 'Не найдено'})

    def do_POST(self):
        if self.path != '/api/announcements':
            return self.send_json(404, {'error': 'Не найдено'})
        try:
            data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            title, text, author_id = data['title'].strip(), data['text'].strip(), int(data['author_id'])
        except (ValueError, KeyError, TypeError, AttributeError):
            return self.send_json(400, {'error': 'Нужны title, text, author_id'})
        if not title or not text:
            return self.send_json(400, {'error': 'Заголовок и текст не должны быть пустыми'})
        row = query(
            f'INSERT INTO announcements (announcement_title, announcement_text, announcement_author_id) '
            f'VALUES (%s, %s, %s) RETURNING {FIELDS}',
            (title, text, author_id),
        )[0]
        self.send_json(201, row)

    def do_DELETE(self):
        prefix = '/api/announcements/'
        if not self.path.startswith(prefix) or not self.path[len(prefix):].isdigit():
            return self.send_json(404, {'error': 'Не найдено'})
        deleted = query('DELETE FROM announcements WHERE announcement_id = %s', (int(self.path[len(prefix):]),))
        self.send_json(200 if deleted else 404, {'deleted': deleted} if deleted else {'error': 'Не найдено'})


ThreadingHTTPServer(('localhost', 8001), Handler).serve_forever()
