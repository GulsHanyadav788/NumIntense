#!/usr/bin/env python3
"""Small local NumIntense API/dashboard. Standard-library only."""
import json, ipaddress, urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from .domain_intel import investigate_domain, rdap

ROOT=Path(__file__).parent

def safe_ip_lookup(value):
    ip=ipaddress.ip_address(value)
    data=rdap(str(ip))
    return {'target':str(ip), 'is_private':ip.is_private, 'is_global':ip.is_global,
            'version':ip.version, 'rdap':data, 'source':'RDAP public service'}

def url_review(value):
    parsed=urllib.parse.urlparse(value)
    if parsed.scheme not in ('http','https') or not parsed.hostname:
        raise ValueError('Provide a complete http(s) URL')
    return {'input':value, 'scheme':parsed.scheme, 'hostname':parsed.hostname, 'port':parsed.port,
            'path':parsed.path, 'query_present':bool(parsed.query), 'fragment_present':bool(parsed.fragment),
            'userinfo_present':bool(parsed.username or parsed.password),
            'note':'URL is parsed only; NumIntense did not visit or download it.'}
class Handler(BaseHTTPRequestHandler):
    def send_json(self,obj,status=200):
        raw=json.dumps(obj,indent=2).encode(); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(raw))); self.send_header('Access-Control-Allow-Origin','http://127.0.0.1:8765'); self.end_headers(); self.wfile.write(raw)
    def do_OPTIONS(self): self.send_response(204); self.send_header('Access-Control-Allow-Origin','http://127.0.0.1:8765'); self.send_header('Access-Control-Allow-Headers','Content-Type'); self.send_header('Access-Control-Allow-Methods','POST,GET,OPTIONS'); self.end_headers()
    def do_GET(self):
        if self.path=='/api/health': return self.send_json({'status':'ok','service':'NumIntense Free Intel API'})
        if self.path=='/' or self.path=='/index.html':
            body=(ROOT/'web'/'index.html').read_bytes(); self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body); return
        self.send_json({'error':'Not found'},404)
    def do_POST(self):
        try:
            length=int(self.headers.get('Content-Length','0')); payload=json.loads(self.rfile.read(length) or b'{}'); target=payload.get('target','').strip()
            if not target: return self.send_json({'error':'Target is required'},400)
            if self.path=='/api/domain': result=investigate_domain(target)
            elif self.path=='/api/ip': result=safe_ip_lookup(target)
            elif self.path=='/api/url': result=url_review(target)
            else: return self.send_json({'error':'Not found'},404)
            self.send_json(result)
        except Exception as e: self.send_json({'error':str(e)},400)
    def log_message(self,fmt,*args): print('[NumIntense API]',fmt%args)
if __name__=='__main__':
    print('NumIntense API/dashboard: http://127.0.0.1:8765  (local-only)')
    HTTPServer(('127.0.0.1',8765),Handler).serve_forever()
