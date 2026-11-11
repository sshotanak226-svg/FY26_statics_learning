from pathlib import Path
import re,json,copy

src=Path('output/９章_仮説検定と信頼区間_編集画面左右分割.html')
dst=Path('output/９章_仮説検定と信頼区間_発表要点原稿.html')
html=src.read_text(encoding='utf-8')
m=re.search(r'<script id="deck-data" type="application/json">(.*?)</script>',html,re.S)
old=json.loads(m[1]);deck=copy.deepcopy(old)
reference=json.loads(Path('tmp/speech_slide_content.json').read_text(encoding='utf-8'))
text='\n\n'.join(Path('tmp/'+name).read_text(encoding='utf-8') for name in ['speech_keypoints_01_30.md','speech_keypoints_31_60.md','speech_keypoints_61_88.md'])
points={}
for match in re.finditer(r'^\[(\d+)\]\n(.*?)(?=^\[\d+\]\n|\Z)',text,re.S|re.M):
    number=int(match[1]);assert number not in points
    note=match[2].strip();lines=note.splitlines()
    assert 3<=len(lines)<=5,(number,len(lines))
    assert all(line.startswith('- ') for line in lines),number
    assert not re.search(r'https?://|出典[：:]|参考文献[：:]',note),number
    points[number]=note
assert set(points)==set(range(1,len(deck['slides'])+1))
assert len(deck['slides'])==88
for i,s in enumerate(deck['slides']):
    assert s['id']==reference[i]['id']
    s['notes']=points[i+1]
    assert {k:v for k,v in s.items() if k!='notes'}=={k:v for k,v in old['slides'][i].items() if k!='notes'}
assert {k:v for k,v in deck.items() if k!='slides'}=={k:v for k,v in old.items() if k!='slides'}
payload=json.dumps(deck,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
out=html[:m.start(1)]+payload+html[m.end(1):]
assert out[:m.start(1)]==html[:m.start(1)]
out=out.replace('</head>','''<style id="speaker-keypoint-list-style">
.presenter-notes .body-list{list-style:disc;padding-left:1.3em;margin:.3em 0;}
.presenter-notes .body-list>li{display:list-item;border:0;padding-left:.15em;margin-bottom:.8em;}
.presenter-notes .body-list>li::marker{color:#1467b3;font-size:1em;}
</style></head>''',1)
dst.write_text(out,encoding='utf-8')
report=[{'page':i+1,'id':s['id'],'points':len(s['notes'].splitlines()),'characters':len(s['notes']),'maxPointCharacters':max(map(len,s['notes'].splitlines()))} for i,s in enumerate(deck['slides'])]
Path('tmp/keypoint_notes_content_check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'slides':len(deck['slides']),'onlyChangedField':'notes','points':sum(x['points'] for x in report),'maxPointCharacters':max(x['maxPointCharacters'] for x in report),'maxSlideCharacters':max(x['characters'] for x in report)},ensure_ascii=True))
