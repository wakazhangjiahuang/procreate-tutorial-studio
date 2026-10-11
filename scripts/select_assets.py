#!/usr/bin/env python3
"""Select and hash-check exact local assets. No network or full-repo scan."""
import argparse
import json
from pathlib import Path, PurePosixPath
from _contract import need, digest

def select(manifest_path,task):
    manifest_path=Path(manifest_path);root=manifest_path.parent
    m=json.loads(manifest_path.read_text(encoding='utf-8'))
    need(m.get('schema_version')=='1.1.0','unsupported manifest')
    need(task in m.get('entrypoints',{}),'unknown task entrypoint')
    assets={x['id']:x for x in m['assets']}
    need(len(assets)==len(m['assets']),'duplicate asset IDs')
    result=[]
    for ident in m['entrypoints'][task]:
        need(ident in assets,'unknown entrypoint asset')
        item=assets[ident];raw=item['path'];p=PurePosixPath(raw)
        need(not p.is_absolute() and '..' not in p.parts and '\\' not in raw,'unsafe asset path')
        local=root/raw
        need(local.is_file() and not local.is_symlink() and local.resolve().is_relative_to(root.resolve()),'asset missing/unsafe')
        need(task in item['task_tags'],'asset task tag mismatch')
        need(digest(local)==item['sha256'],'asset hash mismatch')
        result.append({'id':ident,'path':str(local.resolve()),'sha256':item['sha256']})
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('manifest');ap.add_argument('task')
    a=ap.parse_args();print(json.dumps(select(a.manifest,a.task),ensure_ascii=False))

if __name__=='__main__':
    main()
