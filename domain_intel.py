"""Domain/IP metadata lookups using public DNS, RDAP, and TLS endpoints.
No scanning, authentication bypass, or private-data collection is performed.
"""
import json, socket, ssl, urllib.request, urllib.error, ipaddress, re
from urllib.parse import urlparse

USER_AGENT = 'NumIntense-FreeIntel/1.0'

def _http_json(url, timeout=8):
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8', errors='replace'))

def normalize_domain(value):
    value = value.strip()
    if '://' in value:
        value = urlparse(value).hostname or ''
    value = value.rstrip('.').lower()
    if not value or any(ch.isspace() for ch in value):
        raise ValueError('Enter a valid domain or URL hostname')
    try:
        ipaddress.ip_address(value)
        return value
    except ValueError:
        pass
    if len(value) > 253 or not re.fullmatch(r'[a-z0-9.-]+', value) or '..' in value:
        raise ValueError('Invalid hostname')
    if any(not label or len(label)>63 or label.startswith('-') or label.endswith('-') for label in value.split('.')):
        raise ValueError('Invalid hostname')
    return value

def dns_records(domain):
    out = {'domain': domain, 'records': {}, 'errors': {}}
    for kind, query_type in [('A', socket.AF_INET), ('AAAA', socket.AF_INET6)]:
        try:
            vals = sorted({r[4][0] for r in socket.getaddrinfo(domain, None, query_type)})
            out['records'][kind] = vals
        except Exception as e:
            out['errors'][kind] = str(e)
    try:
        # MX, TXT, NS via DNS-over-HTTPS public resolver
        for typ in ('MX', 'TXT', 'NS'):
            try:
                data = _http_json(f'https://dns.google/resolve?name={domain}&type={typ}')
                out['records'][typ] = [a.get('data','') for a in data.get('Answer', [])]
            except Exception as e: out['errors'][typ] = str(e)
    except Exception as e: out['errors']['DoH'] = str(e)
    return out

def rdap(domain_or_ip):
    host = normalize_domain(domain_or_ip)
    try:
        ipaddress.ip_address(host)
        endpoint = f'https://rdap.org/ip/{host}'
    except ValueError:
        endpoint = f'https://rdap.org/domain/{host}'
    data = _http_json(endpoint)
    events = data.get('events', [])
    names = data.get('nameservers', [])
    return {'objectClassName': data.get('objectClassName'), 'handle': data.get('handle'),
            'name': data.get('ldhName') or data.get('name'), 'status': data.get('status', []),
            'nameservers': [n.get('ldhName') or n.get('name') for n in names],
            'events': events, 'entity_roles': [e.get('roles',[]) for e in data.get('entities',[])],
            'source':'RDAP public registration data'}

def tls_certificate(domain, port=443):
    ctx = ssl.create_default_context()
    with socket.create_connection((domain, port), timeout=7) as sock:
        with ctx.wrap_socket(sock, server_hostname=domain) as s:
            cert = s.getpeercert()
            return {'host': domain, 'port': port, 'tls_version': s.version(),
                    'cipher': s.cipher(), 'subject': cert.get('subject'),
                    'issuer': cert.get('issuer'), 'not_before': cert.get('notBefore'),
                    'not_after': cert.get('notAfter'), 'subject_alt_names': cert.get('subjectAltName', [])}

def investigate_domain(value):
    domain = normalize_domain(value)
    results = {'target': domain, 'timestamp_utc': __import__('datetime').datetime.utcnow().isoformat()+'Z', 'sources': [], 'data': {}, 'errors': {}}
    results['data']['dns'] = dns_records(domain); results['sources'].append('DNS resolver (system + Google DNS-over-HTTPS)')
    for name, fn in [('rdap', lambda: rdap(domain)), ('tls', lambda: tls_certificate(domain))]:
        try: results['data'][name] = fn(); results['sources'].append('RDAP public service' if name=='rdap' else 'TLS certificate presented by target host')
        except Exception as e: results['errors'][name] = str(e)
    return results
