#!/usr/bin/env python3
"""Launch the NumIntense free local intelligence dashboard."""
from intelligence.local_api import HTTPServer, Handler
if __name__ == '__main__':
    print('NumIntense Free Intel dashboard: http://127.0.0.1:8765')
    print('Local-only server. Press Ctrl+C to stop.')
    HTTPServer(('127.0.0.1',8765),Handler).serve_forever()
