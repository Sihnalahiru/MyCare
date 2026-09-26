
from pathlib import Path
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def ok(label,cond):
    checks.append((label,bool(cond)))
files=['index.html','styles.css','app.js','manifest.json','sw.js',
       'data/pages.json','data/study.json','data/curriculum.json','data/mcq.json',
       'data/official-answer-key.json','data/image-map.json','data/japanese-questions.json']
for f in files: ok('file:'+f,(ROOT/f).exists())
pages=json.loads((ROOT/'data/pages.json').read_text(encoding='utf-8'))
study=json.loads((ROOT/'data/study.json').read_text(encoding='utf-8'))
cur=json.loads((ROOT/'data/curriculum.json').read_text(encoding='utf-8'))
mcq=json.loads((ROOT/'data/mcq.json').read_text(encoding='utf-8'))
ak=json.loads((ROOT/'data/official-answer-key.json').read_text(encoding='utf-8'))
im=json.loads((ROOT/'data/image-map.json').read_text(encoding='utf-8'))
jp=json.loads((ROOT/'data/japanese-questions.json').read_text(encoding='utf-8'))
ok('pages JSON wrapper + pages array',isinstance(pages.get('pages'),list))
ok('curriculum has parts + lessons',len(cur.get('parts',[]))>=4 and sum(len(p.get('lessons',[])) for p in cur['parts'])>=14)
ok('PDF pages extracted',pages.get('pageCount')==112)
ok('study blocks present',len(study.get('pages',[]))>=50)
ok('unique images extracted',im.get('uniqueImages',0)==314)
ok('MCQ count >= 50',len(mcq)>=50)
ok('official answer key = 52',ak.get('totalQuestions')==52 and sum(len(s['answers']) for s in ak['sets'])==52)
ok('Japanese question records = 52',len(jp.get('questions',[]))==52)
imgfiles=list((ROOT/'assets/images').glob('*'))
ok('all 314 image files exist',len(imgfiles)==314)
ok('all JP page previews exist',len(list((ROOT/'assets/jp-pages').glob('jp-*.jpg')))==52)
text=' '.join(p.get('text','') for p in pages.get('pages',[]))
for needle in ['Quality of Life','Homeostasis','Dementia','Senuki','Swallowing','Housework','1000–1500','2000–3000','300–500','Final Source Reconciliation']:
    ok('content:'+needle,needle.lower() in text.lower())
app=(ROOT/'app.js').read_text(encoding='utf-8')
css=(ROOT/'styles.css').read_text(encoding='utf-8')
ok('voice queue/chunking', 'chunkText' in app and 'playNext' in app and 'speechSynthesis' in app)
ok('language voices en/si/ja', 'en-US' in app and 'si-LK' in app and 'ja-JP' in app)
ok('mobile responsive CSS','@media(max-width:800px)' in css and '@media(max-width:480px)' in css)
ok('compact topic UI','topic-row' in css and 'source-visuals' in css)
ok('no replacement-glyph text', '▯' not in text and '�' not in text)
fails=[x for x in checks if not x[1]]
for label,cond in checks: print(('PASS' if cond else 'FAIL')+' | '+label)
print(f'RESULT: {len(checks)-len(fails)}/{len(checks)} checks passed')
sys.exit(1 if fails else 0)
