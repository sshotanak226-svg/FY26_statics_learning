from pathlib import Path
import re,json

src=Path('output/９章_仮説検定と信頼区間_原稿分割編集.html')
dst=Path('output/９章_仮説検定と信頼区間_編集画面左右分割.html')
html=src.read_text(encoding='utf-8')
original_data=re.search(r'<script id="deck-data" type="application/json">(.*?)</script>',html,re.S)[1]
form=re.search(r'(<form class="edit-form five-fields" id="edit-form">)(.*?)(</form>)',html,re.S)
content=form[2]
fields=re.search(r'<div class="slide-edit-fields">.*?</div>(?=<section class="script-workspace")',content,re.S)[0]
preview=re.search(r'<section class="script-preview-column".*?</section>',content,re.S)[0]
notes=re.search(r'<label class="wide script-editor-field".*?</label>',content,re.S)[0]
html=html[:form.start(2)]+preview+fields+notes+html[form.end(2):]
html=html.replace('<div class="editor-actions"><button id="add-slide">','<div class="editor-actions"><button type="button" id="toggle-slide-list" aria-controls="edit-nav" aria-expanded="false">ページ一覧・並べ替え</button><button id="add-slide">',1)
html=html.replace('aria-label="原稿を編集するスライド"','aria-label="編集中のスライド"').replace('aria-label="原稿を編集するページ"','aria-label="編集するページ"')
html=html.replace('原稿は右側に入力します','編集内容をすぐ反映します')
em=re.search(r'<script id="slide-engine">(.*?)</script>',html,re.S);engine=em[1]
engine=engine.replace("if(!scriptWritingMode||!host||!stage)return;","if(!host||!stage||host.clientWidth===0||host.clientHeight===0)return;",1)
engine=engine.replace("function renderScriptPreview(){\n if(!scriptWritingMode)return;","function renderScriptPreview(){",1)
engine=engine.replace("if(scriptWritingMode){renderScriptPreview();if(focus)requestAnimationFrame(()=>$('edit-script').focus({preventScroll:true}));}","""$('edit-dialog').classList.remove('page-list-open');$('toggle-slide-list').setAttribute('aria-expanded','false');
 $('script-slide-preview').previousElementSibling.querySelector('span').textContent=scriptWritingMode?'原稿は右側に入力します':'編集内容をすぐ反映します';
 renderScriptPreview();if(scriptWritingMode&&focus)requestAnimationFrame(()=>$('edit-script').focus({preventScroll:true}));""",1)
engine=engine.replace("function bindScriptWriting(){","""function bindScriptWriting(){
 $('toggle-slide-list').onclick=()=>{const open=$('edit-dialog').classList.toggle('page-list-open');$('toggle-slide-list').setAttribute('aria-expanded',String(open));requestAnimationFrame(resizeScriptPreview);};""",1)
needle="$('edit-status').classList.toggle('error',!!errors.length);\n}"
assert engine.count(needle)==1
engine=engine.replace(needle,"$('edit-status').classList.toggle('error',!!errors.length);renderScriptPreview();\n}",1)
html=html[:em.start(1)]+engine+html[em.end(1):]
css=Path('tmp/full_editor_split.css').read_text(encoding='utf-8')
html=html.replace('</head>','<style id="full-editor-split-layout">'+css+'</style></head>',1)
html=html.replace('<strong>編集は6項目。</strong>','<strong>編集画面は左右分割です。</strong>左側にスライド、右側に編集欄を表示し、入力した内容をすぐ反映します。「ページ一覧・並べ替え」でページの複数選択と移動ができます。編集項目は6項目です。')
assert re.search(r'<script id="deck-data" type="application/json">(.*?)</script>',html,re.S)[1]==original_data
assert len(json.loads(original_data)['slides'])==88
dst.write_text(html,encoding='utf-8')
print('Full editor now uses left slide preview and right editable fields. All 88 slide records unchanged.')
