from pathlib import Path
import re,json,copy

src=Path('F:/Download/９章_仮説検定と信頼区間_非正規標本の大標本近似追加.html')
dst=Path('output/９章_仮説検定と信頼区間_原稿分割編集.html')
html=src.read_text(encoding='utf-8')
dm=re.search(r'<script id="deck-data" type="application/json">(.*?)</script>',html,re.S)
old=json.loads(dm[1]);deck=copy.deepcopy(old)
removed=[]
def remove_note_citations(notes,page):
    kept=[]
    for line in notes.splitlines():
        original=line
        if re.match(r'^\s*(?:https?://\S+\s*|【比較の参考文献】|(?:出典|対応|参照|教科書の対応)[：:].*)$',line):
            removed.append({'page':page,'removed':line});continue
        if line.startswith('参考文献：'):
            if '(4)–(6):' in line:line=line.split('(4)–(6):',1)[1]
            else:removed.append({'page':page,'removed':line});continue
        if line.startswith('提供資料の対応：'):
            line=line.split('。',1)[1] if '。' in line else ''
        line=re.sub(r'^(?:原資料：)?PDF\s*\d+(?:[–−-]\d+)?ページ（[^）]*）(?:。|に沿って、|の)?','',line)
        if line!=original:removed.append({'page':page,'removed_prefix':original[:len(original)-len(line)]})
        kept.append(line)
    return re.sub(r'\n{3,}','\n\n','\n'.join(kept)).strip()
deck['sources']={};deck['referenceNote']=''
for i,s in enumerate(deck['slides']):
    s['sources']=[];s['original']=''
    s['notes']=remove_note_citations(s.get('notes',''),i+1)
    # All substantive slide fields remain byte-for-byte equivalent as data.
    assert {k:v for k,v in s.items() if k not in {'sources','original','notes'}}=={k:v for k,v in old['slides'][i].items() if k not in {'sources','original','notes'}}
assert len(deck['slides'])==88
payload=json.dumps(deck,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
html=html[:dm.start(1)]+payload+html[dm.end(1):]
html=html.replace('<button id="source">出典</button>','')
html,n=re.subn(r'<div id="sources" class="overlay".*?(?=<div id="notes" class="overlay")','',html,count=1,flags=re.S);assert n==1
html=html.replace('外部出典へのリンクを開くときだけ通信が必要です。','')
html=html.replace('<kbd>S</kbd> 出典　','')
# Keep the existing form and its fields; put the script field into a focused workspace.
start=html.index('<form class="edit-form five-fields" id="edit-form">')+len('<form class="edit-form five-fields" id="edit-form">')
script=html.index('<label class="wide script-editor-field"',start)
html=html[:start]+'<div class="slide-edit-fields">'+html[start:script]+'''</div><section class="script-workspace" aria-label="スライドを見ながら発表原稿を作成">
<section class="script-preview-column" aria-label="原稿を編集するスライド">
<div class="script-preview-heading"><h3>スライド</h3><span>原稿は右側に入力します</span></div>
<div class="script-slide-preview" id="script-slide-preview"><div id="script-preview-stage"></div></div>
<div class="script-page-controls"><button type="button" id="script-slide-prev">← 前へ</button><select id="script-slide-picker" aria-label="原稿を編集するページ"></select><button type="button" id="script-slide-next">次へ →</button></div>
<p class="script-slide-title" id="script-slide-title"></p></section>'''+html[script:]
html=html.replace('6. 発表原稿<textarea id="edit-script"','発表原稿<textarea id="edit-script"',1)
html=html.replace('</small></label></form></div><footer>','</small></label></section></form></div><footer>',1)
html=html.replace('「原稿を編集」で編集画面の原稿欄を開けます。','「原稿を編集」で、左にスライド・右に原稿入力欄を並べた作成画面を開けます。')
html=html.replace('編集画面の「6. 発表原稿」と同期します。','原稿作成画面の入力欄と同期します。')
html=html.replace('入力します。右欄が空なら説明を全幅に表示します。','入力します。「原稿を編集」では左にスライド・右に原稿入力欄を表示し、前後ボタンとページ選択で原稿を切り替えられます。右欄が空なら説明を全幅に表示します。')
em=re.search(r'<script id="slide-engine">(.*?)</script>',html,re.S);engine=em[1]
engine=re.sub(r'function sourceRecord\(id\)\{[^\n]*\}\n','',engine,count=1)
engine,n=re.subn(r'function showSources\(\)\{.*?\n\}\n(?=function showNotes)','',engine,count=1,flags=re.S);assert n==1
engine=engine.replace("$('source').onclick=showSources;",'').replace("else if(key==='s')showSources();",'')
engine=engine.replace("$('edit-status').classList.remove('error');\n}","$('edit-status').classList.remove('error');renderScriptPreview();\n}",1)
engine=engine.replace("function showEditor(){editIndex=current;", "function showEditor(){setScriptWritingMode(false);editIndex=current;",1)
old_fn="""function editPresenterScript(){
 showEditor();
 const input=$('edit-form').elements.notes;
 input.focus({preventScroll:true});input.scrollIntoView({block:'center',behavior:'auto'});
}"""
assert old_fn in engine
engine=engine.replace(old_fn,"function editPresenterScript(){showEditor();setScriptWritingMode(true,true);}")
old_jump="$('edit-script-jump').onclick=()=>{const input=$('edit-form').elements.notes;input.focus({preventScroll:true});input.scrollIntoView({block:'center',behavior:'auto'});};"
assert old_jump in engine
engine=engine.replace(old_jump,"$('edit-script-jump').onclick=()=>setScriptWritingMode(!scriptWritingMode,true);bindScriptWriting();")
engine=engine.replace("addEventListener('input',commitForm)","addEventListener('input',onEditorFieldChange)").replace("addEventListener('change',commitForm)","addEventListener('change',onEditorFieldChange)")
engine=engine.replace('\nnormalizeDeck(deck);','\n'+Path('tmp/script_writing_split.js').read_text(encoding='utf-8')+'\nnormalizeDeck(deck);',1)
html=html[:em.start(1)]+engine+html[em.end(1):]
css=Path('tmp/script_writing_split.css').read_text(encoding='utf-8')
html=html.replace('</head>','<style id="script-writing-layout">'+css+'</style></head>',1)
assert 'function showSources' not in html and 'id="sources"' not in html and 'id="source"' not in html
dst.write_text(html,encoding='utf-8')
Path('tmp/script_citation_removals.json').write_text(json.dumps(removed,ensure_ascii=False,indent=2),encoding='utf-8')
print('88 slides preserved; notes-only editing workspace added; citation UI and source-only notes removed.')
