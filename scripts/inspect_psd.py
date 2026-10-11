#!/usr/bin/env python3
"""Optional read-only PSD facts. No external linked content or history inference."""
import argparse
import json
from pathlib import Path
from _contract import digest

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path)
    a=ap.parse_args()
    if not a.source.is_file():
        ap.error('source PSD missing')
    try:
        from psd_tools import PSDImage
    except ImportError:
        print(json.dumps({'status':'PSD_RUNTIME_UNAVAILABLE','fallback':'Export layered PNGs and the original composite from the drawing app.'}))
        return 2
    psd=PSDImage.open(a.source)
    rows=[]
    def visit(container,parent=''):
        for i,layer in enumerate(container):
            address=f'{parent}/{i}'
            rows.append({'address':address,'name':layer.name,'kind':layer.kind,'visible':layer.visible,
                         'bbox':list(layer.bbox),'opacity':layer.opacity,'group':layer.is_group()})
            if layer.is_group():
                visit(layer,address)
    visit(psd)
    print(json.dumps({'status':'PSD_FACTS_READ','path':str(a.source.resolve()),'sha256':digest(a.source),
                      'size':list(psd.size),'layers':rows,'historical_order':'NOT_ESTABLISHED',
                      'limitations':'No drawing history; compositing support is limited; external links not opened.'},ensure_ascii=False))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
