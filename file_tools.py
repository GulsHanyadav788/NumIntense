"""Local file fingerprint utilities. Files are read locally, not uploaded."""
import hashlib, os

def fingerprint(path):
    if not os.path.isfile(path): raise ValueError('Path is not a regular file')
    h = {'md5': hashlib.md5(), 'sha1': hashlib.sha1(), 'sha256': hashlib.sha256()}
    size = 0
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            size += len(chunk)
            for digest in h.values(): digest.update(chunk)
    return {'file': os.path.basename(path), 'size_bytes': size, 'hashes': {k:v.hexdigest() for k,v in h.items()}}
