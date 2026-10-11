#!/usr/bin/env python3
"""Input facts adapted from the existing process-rebuilder inspector."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageCms
from io import BytesIO
from _contract import digest

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('source',type=Path)
    ap.add_argument('--role',choices=['ARTWORK_MASTER','PROCESS_EVIDENCE','LAYOUT_REFERENCE'],default='ARTWORK_MASTER')
    a=ap.parse_args()
    with Image.open(a.source) as im:
        im.verify()
    with Image.open(a.source) as im:
        icc=im.info.get('icc_profile')
        description=ImageCms.getProfileDescription(ImageCms.ImageCmsProfile(BytesIO(icc))).strip() if icc else None
        result={'path':str(a.source.resolve()),'role':a.role,'sha256':digest(a.source),'size':list(im.size),
                'mode':im.mode,'format':im.format,'icc_profile':description,'classification':'REQUIRES_VISUAL_REVIEW'}
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':
    main()
