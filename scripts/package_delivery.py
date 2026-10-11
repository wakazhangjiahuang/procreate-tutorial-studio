#!/usr/bin/env python3
"""Whitelist exactly ten PNG and one XLSX. Original and QA remain internal."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from _contract import load_plan, WORKBOOK, digest, need, real_file
from verify_pages import verify
from build_workbook import validate_workbook

def package(plan_path,workdir,review_path,output):
    workdir=Path(workdir);output=Path(output)
    plan=load_plan(plan_path)
    verify(plan_path,workdir,review_path)
    workbook=real_file(workdir,WORKBOOK)
    validate_workbook(workbook,plan)
    names=[s['filename'] for s in plan['steps']]+[WORKBOOK]
    need(len(set(names))==11,'delivery must contain 11 unique files')
    need(not output.is_symlink() and output.resolve() not in [real_file(workdir,n).resolve() for n in names],
         'output may not overwrite an input or symlink')
    hashes={name:digest(real_file(workdir,name)) for name in names}
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            archive.write(real_file(workdir,name),arcname=name)
    with zipfile.ZipFile(output) as archive:
        need(archive.namelist()==names and len(archive.infolist())==11,'ZIP member set/order mismatch')
        need(archive.testzip() is None,'ZIP CRC failure')
        for name,expected in hashes.items():
            need(hashlib.sha256(archive.read(name)).hexdigest()==expected,'ZIP byte hash mismatch')
    return {'status':'PACKAGE_TEST_PASS' if plan['work_type']=='SYNTHETIC_TEST' else 'PACKAGE_PASS',
            'output':str(output),'images':10,'workbooks':1,'members':11,'sha256':digest(output),
            'target_software_trial':'NOT_ESTABLISHED','review':'HASH_BOUND_RECORDED_PASS'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('plan');ap.add_argument('workdir');ap.add_argument('review');ap.add_argument('output')
    a=ap.parse_args();print(json.dumps(package(a.plan,a.workdir,a.review,a.output),ensure_ascii=False))

if __name__=='__main__':
    main()
