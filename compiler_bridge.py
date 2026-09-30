"""Local Keil C51 bridge. Bind only loopback; no shell or client-controlled paths."""
import json, os, re, subprocess, tempfile, threading
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(os.environ.get('KEIL_C51_HOME', 'C:/Keil_v5/C51'))
ORIGINS = {'https://ye-ye-ban-base-converter-sites.zcq991029.chatgpt.site', 'http://127.0.0.1:8765', 'http://localhost:8765'}
LOCK = threading.Lock()

def compile_c(source):
    if not isinstance(source, str) or len(source.encode('utf8')) > 65536:
        raise ValueError('Source must be at most 64 KB')
    # Allow installed Keil headers only, never filesystem traversal or absolute includes.
    for name in re.findall(r'^\s*#\s*include\s*[<"]([^>"\n]+)', source, re.M):
        if not re.fullmatch(r'[A-Za-z0-9_]+\.h', name, re.I):
            raise ValueError('Only installed header names are allowed: ' + name)
    with LOCK, tempfile.TemporaryDirectory(prefix='c51-build-') as folder:
        path = Path(folder)
        (path/'main.c').write_bytes(source.encode('gbk', errors='replace'))
        # STC compatibility definitions are our own; standard headers come from installed Keil.
        (path/'STC89C52RC.H').write_text('#include <REG52.H>\nsfr AUXR=0x8E;\nsfr AUXR1=0xA2;\nsfr IPH=0xB7;\n', encoding='ascii')
        logs = []
        commands = [
            [str(ROOT/'BIN/C51.exe'), 'main.c', 'OBJECT(main.obj)', f'INCDIR({ROOT / "INC"})', 'OPTIMIZE(0)', 'DEBUG'],
            [str(ROOT/'BIN/BL51.exe'), 'main.obj', 'TO', 'main', 'RAMSIZE(256)'],
            [str(ROOT/'BIN/OHX51.exe'), 'main', 'HEXFILE(main.hex)'],
        ]
        env = dict(os.environ, C51INC=str(ROOT/'INC'), C51LIB=str(ROOT/'LIB'))
        for args in commands:
            proc = subprocess.run(args, cwd=folder, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=20, creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            logs.append(proc.stdout.decode('gbk', errors='replace'))
            if proc.returncode:
                return {'ok':False, 'log':'\n'.join(logs), 'compiler':'Keil C51'}
        return {'ok':True, 'log':'\n'.join(logs), 'hex':(path/'main.hex').read_text(), 'compiler':'Keil C51', 'listing':(path/'main.lst').read_text(errors='replace') if (path/'main.lst').exists() else ''}

class Handler(BaseHTTPRequestHandler):
    def allowed(self):
        return self.headers.get('Origin') in ORIGINS or not self.headers.get('Origin')
    def reply(self, status, data):
        self.send_response(status)
        origin = self.headers.get('Origin')
        if origin in ORIGINS:
            self.send_header('Access-Control-Allow-Origin', origin)
        self.send_header('Access-Control-Allow-Private-Network','true')
        self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Cache-Control','no-store')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf8'))
    def do_OPTIONS(self):
        self.reply(200 if self.allowed() else 403, {})
    def do_GET(self):
        if not self.allowed(): return self.reply(403, {'error':'Origin not allowed'})
        self.reply(200, {'compiler':'Keil C51', 'ready':(ROOT/'BIN/C51.exe').exists()})
    def do_POST(self):
        if not self.allowed(): return self.reply(403, {'error':'Origin not allowed'})
        if self.path != '/compile': return self.reply(404, {})
        try:
            length=int(self.headers.get('Content-Length',0))
            if not 0 < length < 100000: raise ValueError('Invalid request size')
            data=json.loads(self.rfile.read(length))
            self.reply(200, compile_c(data.get('source')))
        except Exception as error:
            self.reply(400, {'ok':False, 'log':str(error)})

if __name__ == '__main__':
    print('Keil C51 bridge: http://127.0.0.1:8766 (loopback only)', flush=True)
    ThreadingHTTPServer(('127.0.0.1',8766),Handler).serve_forever()
