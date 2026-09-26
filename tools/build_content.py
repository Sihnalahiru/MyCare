from __future__ import annotations
import fitz, hashlib, json, re, shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/'assets'/'source-book.pdf'
IMG=ROOT/'assets'/'images'
DATA=ROOT/'data'
IMG.mkdir(parents=True,exist_ok=True); DATA.mkdir(parents=True,exist_ok=True)
if not PDF.exists(): raise SystemExit('ERROR: assets/source-book.pdf not found')

doc=fitz.open(PDF)
seen={}; refs=[]; pages=[]
for pno,page in enumerate(doc, start=1):
    txt=page.get_text('text').replace('\u00a0',' ').strip()
    repairs={'මෙමෙ':'මෙම','වන්න්':'වන්නේ','රරෝ':'රෝ','හරෝ':'හෝ','ගගෞ':'ගෞ','නාකර':'නොකර','නාකළ':'නොකළ','නාමෙැති':'නොමැති','නාසලකා':'නොසලකා','පගෞද්ගලික':'පෞද්ගලික','තාරතුරැ':'තොරතුරු','වටිනාකමේ':'වටිනාකම්','සාමොන්‍ය':'සාමාන්‍ය','මොනසික':'මානසික','අපයරෝජ':'අපයෝජ','කළමෙනාකරණ':'කළමනාකරණ','මොනව':'මානව'}
    for a,b in repairs.items(): txt=txt.replace(a,b)
    pages.append({'page':pno,'text':txt})
    for im in page.get_images(full=True):
        xref=im[0]
        try: info=doc.extract_image(xref)
        except Exception: continue
        raw=info['image']; ext=info['ext']; h=hashlib.sha1(raw).hexdigest()
        was_new = h not in seen
        if was_new:
            fn=f'img-{len(seen)+1:03d}.{ext}'
            (IMG/fn).write_bytes(raw)
            seen[h]={'file':fn,'page':pno,'xref':xref}
        refs.append({'page':pno,'image':seen[h]['file'],'duplicate':not was_new})

(DATA/'pages.json').write_text(json.dumps({'source':PDF.name,'pageCount':len(doc),'pages':pages},ensure_ascii=False,indent=2),encoding='utf-8')
(DATA/'image-map.json').write_text(json.dumps({'uniqueImages':len(seen),'references':refs},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Extracted {len(doc)} pages and {len(seen)} unique embedded images ({len(refs)} references).')


# Build compact study data without illustration-only pseudo-pages.
study_pages=[]
def illustration_only(t):
    lines=[x.strip() for x in t.splitlines() if x.strip()]
    nonmeta=[x for x in lines if not (x.startswith('Original source illustrations') or x.startswith('Source PDF p.') or x.startswith('Images are extracted'))]
    return len(' '.join(nonmeta))<80
for p in pages:
    if not illustration_only(p['text']):
        lines=[x.strip() for x in p['text'].splitlines() if x.strip()]
        topics=[]
        for s in lines:
            if len(s)<140 and (re.match(r'^(?:\d+[\.\)]|[A-Z][A-Z0-9 /—&\-]{6,}|PART )',s) or s.startswith('EXAM TRAP') or s.startswith('FINAL AUDIT')):
                if 'Source PDF' not in s and 'Original source' not in s: topics.append(s)
        study_pages.append({**p,'topics':list(dict.fromkeys(topics))[:12]})
(DATA/'study.json').write_text(json.dumps({'source':PDF.name,'pages':study_pages},ensure_ascii=False,indent=2),encoding='utf-8')
