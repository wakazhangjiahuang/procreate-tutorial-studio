#!/usr/bin/env python3
"""Decode, color, blank-region and current review checks; never guess art quality."""
import argparse
import json
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageCms
from _contract import load_plan, need, real_file, verify_review

def verify(plan_path,pages,review_path=None):
    plan=load_plan(plan_path)
    pages=Path(pages)
    expected={s['filename'] for s in plan['steps']}
    actual={p.name for p in pages.glob('*.png')}
    need(expected==actual,'PNG set differs from expected ten pages')
    for step in plan['steps']:
        path=real_file(pages,step['filename'])
        with Image.open(path) as im:
            im.verify()
        with Image.open(path) as im:
            need(im.format=='PNG' and im.size==(3072,4096),'PNG format or dimensions mismatch')
            need(im.mode in ('RGB','RGBA'),'PNG must be RGB or RGBA')
            if im.mode=='RGBA':
                need(im.getchannel('A').getextrema()==(255,255),'white page must be opaque')
            icc=im.info.get('icc_profile')
            has_srgb_chunk='srgb' in im.info
            if icc:
                profile=ImageCms.ImageCmsProfile(BytesIO(icc))
                has_srgb_chunk='srgb' in ImageCms.getProfileDescription(profile).lower()
            need(has_srgb_chunk,'sRGB encoding/profile required; cannot assume untagged color space')
            for rect in step['white_regions']:
                extrema=im.crop(tuple(rect)).convert('RGB').getextrema()
                need(all(pair==(255,255) for pair in extrema),f'{step["id"]}: declared blank region is not pure white')
    if review_path:
        verify_review(plan_path,plan,pages,review_path)
    return {'status':'PAGES_WITH_REVIEW_PASS' if review_path else 'PAGES_STRUCTURE_PASS',
            'pages':10,'visual_quality':'RECORDED_REVIEW_PASS' if review_path else 'REQUIRES_VISUAL_REVIEW',
            'work_type':plan['work_type']}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('plan');ap.add_argument('pages');ap.add_argument('--review')
    a=ap.parse_args()
    print(json.dumps(verify(a.plan,a.pages,a.review),ensure_ascii=False))

if __name__=='__main__':
    main()
