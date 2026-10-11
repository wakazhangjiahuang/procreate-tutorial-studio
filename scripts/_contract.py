"""Ten-page contract. Artistic decisions remain explicit, hash-bound review data."""
import hashlib
import json
import re
from pathlib import Path, PurePosixPath

VERSION = '1.1.0'
WORKBOOK = '原稿风格与画法资料.xlsx'
EVIDENCE = {'VERIFIED', 'VERIFIED_METADATA', 'OBSERVED', 'INFERRED', 'PROPOSED', 'UNVERIFIED'}
PROCESS = {'REAL_FRAME', 'LAYER_RECONSTRUCTION', 'REASONED'}
ACTIONS = {'DRAW', 'FILL', 'DETAIL', 'ERASE', 'ADJUST'}
PAGE_GATES = ('identity', 'style', 'actionable', 'delta_matches', 'text_exact', 'no_overrender', 'white_background')
TRANSITION_GATES = ('preconditions', 'gap', 'continuity', 'no_future_content')
DNA_DIMENSIONS = {'时代风格', '笔触', '线条', '轮廓', '上色', '画法过程', '构图留白'}

class ContractError(ValueError):
    pass

def need(condition, message):
    if not condition:
        raise ContractError(message)

def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def text_fields(item, keys, where):
    need(isinstance(item, dict), f'{where}: object required')
    for key in keys:
        v = item.get(key)
        need(isinstance(v, str) and v.strip(), f'{where}.{key}: nonempty text required')
        need(not re.search(r'\{\{|\bTODO\b|待填写|实际动作短名', v), f'{where}.{key}: placeholder')

def filename(value):
    need(isinstance(value, str), 'filename must be text')
    p = PurePosixPath(value)
    need(not p.is_absolute() and len(p.parts) == 1 and p.name == value and
         value not in ('.', '..') and not any(c in value for c in ('\\', '\x00', ':')),
         f'unsafe filename: {value!r}')
    return value

def real_file(root, name):
    path = Path(root) / filename(name)
    need(not path.is_symlink() and path.is_file(), f'missing or symlink file: {name}')
    need(path.resolve().is_relative_to(Path(root).resolve()), 'path escapes work directory')
    return path

def load_plan(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    validate_plan(data)
    return data

def validate_plan(data):
    need(isinstance(data, dict) and data.get('schema_version') == VERSION, 'unsupported plan schema')
    need(data.get('work_type') in ('ARTWORK_TUTORIAL', 'SYNTHETIC_TEST'), 'work_type required')
    spec = data.get('delivery', {})
    for key, expected in {'count':10, 'width':3072, 'height':4096, 'format':'PNG', 'color_space':'sRGB', 'background':'#FFFFFF'}.items():
        need(spec.get(key) == expected, f'delivery.{key} must be {expected}')
    source = data.get('source')
    text_fields(source, ('id', 'title', 'path', 'sha256'), 'source')
    src = Path(source['path'])
    need(src.is_absolute() and src.is_file(), 'source.path must be an existing absolute file')
    need(re.fullmatch('[0-9a-f]{64}', source['sha256']), 'invalid source SHA256')
    need(digest(src) == source['sha256'], 'source content changed')
    need(source.get('process_evidence') in PROCESS, 'invalid source process evidence')
    dna = data.get('visual_dna')
    need(isinstance(dna, list) and dna, 'visual_dna missing')
    for row in dna:
        text_fields(row, ('dimension','region','observation','evidence','confidence','teaching_effect'), 'visual_dna')
        need(row['evidence'] in EVIDENCE, 'invalid DNA evidence')
    need(DNA_DIMENSIONS.issubset({x['dimension'] for x in dna}), 'incomplete visual DNA dimensions')
    palette = data.get('palette')
    need(isinstance(palette, list) and palette, 'palette missing')
    for row in palette:
        text_fields(row, ('category','object','role','hex','source','evidence'), 'palette')
        need(re.fullmatch('#[0-9A-Fa-f]{6}', row['hex']), 'invalid color HEX')
    sources = data.get('sources')
    need(isinstance(sources, list) and sources, 'sources missing')
    ids = []
    for row in sources:
        text_fields(row, ('id','kind','location','commit','content_hash','read_scope','license','adoption','limit'), 'sources')
        ids.append(row['id'])
    need(len(ids) == len(set(ids)), 'duplicate source IDs')
    source_ids = set(ids)
    brushes = data.get('brushes')
    need(isinstance(brushes, list) and brushes, 'brush responsibilities missing')
    brush_ids = []
    for row in brushes:
        text_fields(row, ('id','role','behavior','settings','evidence','evidence_basis','source_id','alternative'), 'brushes')
        need(row['evidence'] in EVIDENCE, 'invalid brush evidence')
        need(row['source_id'] in source_ids, 'unknown brush source')
        if row.get('native_name'):
            need(row['evidence'] in ('VERIFIED','VERIFIED_METADATA'), 'native name lacks native evidence')
            need(re.fullmatch('[0-9a-f]{64}', row.get('source_sha256','')), 'native evidence lacks source hash')
        brush_ids.append(row['id'])
    need(len(brush_ids) == len(set(brush_ids)), 'duplicate brush IDs')
    ops = data.get('operations')
    need(isinstance(ops, list) and ops, 'operations missing')
    op_index = {}
    for op in ops:
        text_fields(op, ('id','goal','object_material'), 'operations')
        need(op['id'] not in op_index, 'duplicate operation ID')
        need(op.get('classification') in ('REQUIRED','OPTIONAL','NOT_APPLICABLE'), 'invalid classification')
        deps = op.get('depends_on')
        need(isinstance(deps,list) and all(isinstance(x,str) for x in deps), 'invalid dependencies')
        op_index[op['id']] = op
    for op in ops:
        need(set(op['depends_on']).issubset(op_index), 'unknown operation dependency')
    steps = data.get('steps')
    need(isinstance(steps, list) and len(steps) == 10, 'exactly ten steps required')
    names, positions = [], {}
    for i, step in enumerate(steps, 1):
        ident = f'{i:02d}'
        text_fields(step, ('id','filename','learning_goal','region','layer_action','brush_id','brush_behavior',
                          'operation','visible_delta','state_after','completion_check','view'), f'step {ident}')
        need(step['id'] == ident and step.get('type') == 'step', 'step ID/type mismatch')
        name = filename(step['filename'])
        need(name.startswith(ident+'_') and name.endswith('.png'), 'step filename mismatch')
        names.append(name)
        need(step.get('action_type') in ACTIONS, 'non-drawing page cannot count as a step')
        need(step['brush_id'] in brush_ids, 'unknown brush responsibility')
        need(step.get('process_evidence') in PROCESS, 'invalid step process evidence')
        need(step.get('setting_evidence') in EVIDENCE, 'invalid setting evidence')
        pre = step.get('preconditions')
        need(isinstance(pre,list) and pre and all(isinstance(x,str) and x.strip() for x in pre), 'preconditions missing')
        basis = step.get('source_basis')
        need(isinstance(basis,list) and basis and set(basis).issubset(source_ids), 'step source basis missing/unknown')
        text_fields(step.get('display_text'), ('title','action','brush_note','check'), 'display_text')
        need(not re.search('封面|成品展示|复盘|总结|收藏|关注|点赞', step['display_text']['title']), 'non-operation title')
        refs = step.get('references')
        need(isinstance(refs,list) and source['id'] in refs, 'every step must reference master')
        if i > 1:
            need(f'{i-1:02d}' in refs, 'previous approved stage reference missing')
        rects = step.get('white_regions')
        need(isinstance(rects,list) and rects, 'declared blank regions missing')
        for box in rects:
            need(isinstance(box,list) and len(box)==4 and all(type(v) is int for v in box), 'invalid blank rectangle')
            x0,y0,x1,y1 = box
            need(0 <= x0 < x1 <= 3072 and 0 <= y0 < y1 <= 4096, 'blank rectangle outside canvas')
        assigned = step.get('operation_ids')
        need(isinstance(assigned,list) and assigned, 'step operation mapping missing')
        for j, op_id in enumerate(assigned):
            need(op_id in op_index and op_id not in positions, 'operation missing/duplicated across pages')
            need(op_index[op_id]['classification'] != 'NOT_APPLICABLE', 'inapplicable operation assigned')
            positions[op_id] = (i,j)
    need(len(set(names)) == 10, 'duplicate PNG names')
    for op in ops:
        if op['classification'] == 'REQUIRED':
            need(op['id'] in positions, 'required operation omitted')
        if op['id'] in positions:
            for dep in op['depends_on']:
                need(dep in positions and positions[dep] < positions[op['id']], 'dependency omitted, cyclic or scheduled too late')
    text_fields(data.get('generation'), ('tool','model','resolution_method','limitations'), 'generation')
    return data

def verify_review(plan_path, plan, pages, review_path):
    review = json.loads(Path(review_path).read_text(encoding='utf-8'))
    need(review.get('plan_sha256') == digest(plan_path), 'review belongs to a different plan')
    text_fields(review, ('reviewer','review_method','reviewed_at','scope'), 'review')
    rows = review.get('pages')
    need(isinstance(rows,list) and len(rows)==10, 'ten page reviews required')
    for step,row in zip(plan['steps'],rows):
        need(row.get('id')==step['id'], 'review page IDs mismatch')
        need(row.get('sha256')==digest(real_file(pages,step['filename'])), 'page changed after review')
        text_fields(row, ('basis',), 'page review')
        for key in PAGE_GATES:
            need(row.get(key)=='PASS', f'page {step["id"]} review incomplete: {key}')
    transitions = review.get('transitions')
    need(isinstance(transitions,list) and len(transitions)==9, 'nine transition reviews required')
    for i,row in enumerate(transitions,1):
        need(row.get('from')==f'{i:02d}' and row.get('to')==f'{i+1:02d}', 'transition IDs mismatch')
        text_fields(row, ('basis',), 'transition review')
        for key in TRANSITION_GATES:
            need(row.get(key)=='PASS', f'transition {i} incomplete: {key}')
    for key in ('first_step_startable','terminal_matches_master'):
        need(review.get(key)=='PASS', f'{key} not reviewed')
    return review
