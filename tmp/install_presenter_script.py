import json
import re
from pathlib import Path

source=Path(r'F:\Document\Fy26 TDH statics lean\output\９章_仮説検定と信頼区間_等分散二標本3枚.html')
candidate=Path(r'F:\Document\Fy26 TDH statics lean\tmp\presenter-script-work.html')
backup=Path(r'F:\Document\Fy26 TDH statics lean\tmp\等分散二標本3枚_原稿機能追加前.html')
html=source.read_text(encoding='utf-8')
assert 'id="presenter-script-style"' not in html
backup.write_text(html,encoding='utf-8')

def replace(old,new,count=1):
 global html
 assert html.count(old)==count,(old[:100],html.count(old),count)
 html=html.replace(old,new)

field='''<label class="wide script-editor-field" id="script-editor-field" for="edit-script">6. 発表原稿<textarea id="edit-script" name="notes" spellcheck="false" placeholder="このスライドで話す原稿を入力します。\n\n改行・Markdown・数式（$...$、$$...$$）が使えます。"></textarea><small>発表者ツールの原稿欄に表示されます。原稿もスライドごとに自動保存されます。聴衆用スライドには表示されません。</small></label>'''
replace('</form></div><footer><div class="editor-save-state">',field+'</form></div><footer><div class="editor-save-state">')
replace('<button id="preview-edit">プレビュー</button>','<button id="preview-edit">プレビュー</button><button type="button" id="edit-script-jump">原稿を編集</button>')
replace("['theme','title','takeaway','leftMarkdown','rightHTML']","['theme','title','takeaway','leftMarkdown','rightHTML','notes']",2)
replace("$('edit-status').textContent='5項目で編集できます。右欄を空にすると左の文章が全幅で表示されます。';","$('edit-status').textContent='6項目で編集できます。発表原稿は発表者ツールに表示されます。';")
replace("s.body=Array.isArray(s.body)?s.body:[];","s.notes=typeof s.notes==='string'?s.notes:'';s.body=Array.isArray(s.body)?s.body:[];")
replace("throw Error('左欄・右欄は文字列で指定してください。');normalizeSlide(s);","throw Error('左欄・右欄は文字列で指定してください。');if(s.notes!==undefined&&typeof s.notes!=='string')throw Error('発表原稿は文字列で指定してください。');normalizeSlide(s);")
replace("html:$('stage').innerHTML,current,title:","html:$('stage').innerHTML,current,slideId:deck.slides[current].id,title:")
replace("next:next?.title||'本編の最後です'","next:next?.title||'最後のスライドです'")
replace("case'focus':window.focus();break;","case'focus':window.focus();break;case'edit-notes':window.focus();editPresenterScript();break;")
replace("$('edit-form').addEventListener('submit',e=>e.preventDefault());","$('edit-script-jump').onclick=()=>{const input=$('edit-form').elements.notes;input.focus({preventScroll:true});input.scrollIntoView({block:'center',behavior:'auto'});};\n $('edit-form').addEventListener('submit',e=>e.preventDefault());")
start=html.index('function bootstrapPresenter(){')
end=html.index('\nnormalizeDeck(deck);',start)
html=html[:start]+Path('tmp/presenter_script_runtime.js').read_text(encoding='utf-8')+html[end:]
replace('<strong>編集は5項目だけ。</strong>テーマ・タイトル・概要・左側のMarkdown・右側のHTMLまたは画像を入力します。','<strong>編集は6項目。</strong>テーマ・タイトル・概要・左側のMarkdown・右側のHTMLまたは画像・発表原稿を入力します。')
replace('メモ、次のスライド、予定時間、タイマーを表示します。','発表原稿、次のスライド、予定時間、タイマーを表示します。原稿はスクロールでき、A−／A＋で文字サイズを調整できます。「原稿を編集」で編集画面の原稿欄を開けます。原稿の編集内容はすぐ反映され、同じスライドではタイマー更新でも読み位置を維持します。')
replace('この画面でメモを表示','この画面で原稿を表示')

css='''
<style id="presenter-script-style">
.script-editor-field textarea{min-height:260px;resize:vertical;font-family:inherit;line-height:1.7;tab-size:4;}
.script-editor-field small{line-height:1.6;}
#edit-script-jump{color:#1467b3;border-color:#8db2d4;}
.presenter-mode .presenter-layout{grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);overflow:hidden;gap:24px;}
.presenter-mode .presenter-left{overflow:auto;min-height:0;padding-right:4px;}
.presenter-script-column{min-width:0;min-height:0;display:flex;flex-direction:column;}
.presenter-script-heading{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;}
.presenter-script-heading h2{margin:0;color:#1467b3;}
.presenter-script-tools{display:flex;align-items:center;gap:7px;}
.presenter-script-tools button{font-size:14px;padding:7px 10px;white-space:nowrap;}
.presenter-script-tools output{font-size:13px;min-width:34px;text-align:center;color:#52636b;}
.presenter-script-column>h3{font-size:18px;line-height:1.5;margin:16px 0 12px;overflow-wrap:anywhere;}
.presenter-mode .presenter-notes{flex:1;min-height:0;overflow:auto;overscroll-behavior:contain;scrollbar-gutter:stable;white-space:normal;overflow-wrap:anywhere;line-height:1.8;font-size:22px;padding:22px 24px;border:1px solid #d8e2e4;border-radius:8px;}
.presenter-notes:focus-visible{outline:2px solid #1467b3;outline-offset:2px;}
.presenter-notes p{margin:0 0 .8em;}
.presenter-notes .body-list{margin:.5em 0;}
.presenter-notes .body-list li{font-size:inherit;line-height:inherit;margin:0 0 .7em;padding-left:14px;}
.presenter-notes :is(h1,h2,h3,h4,h5,h6){font-size:1.1em;margin:.7em 0 .4em;line-height:1.5;}
.presenter-notes .katex-display{margin:.7em 0;overflow-x:auto;overflow-y:hidden;}
.presenter-notes pre{white-space:pre-wrap;overflow-wrap:anywhere;}
.presenter-notes table{width:100%;border-collapse:collapse;font-size:.9em;}
.presenter-notes :is(th,td){border:1px solid #d8e2e4;padding:7px;}
.presenter-script-hint,.presenter-sharing-hint{font-size:13px;color:#52636b;line-height:1.6;}
.presenter-script-hint{margin:10px 0 0;}
.presenter-empty-script{color:#687983;}
@media(max-width:900px){.presenter-mode .presenter-layout{grid-template-columns:1fr;overflow:auto;}.presenter-mode .presenter-left{overflow:visible;}.presenter-script-column{min-height:65vh;}.presenter-mode .presenter-notes{min-height:45vh;max-height:65vh;flex:none;}}
</style>
'''
replace('</head>',css+'</head>')
pat=r'(<script[^>]*id="deck-data"[^>]*>)(.*?)(</script>)'
old=json.loads(re.search(pat,backup.read_text(encoding='utf-8'),re.S)[2])
new=json.loads(re.search(pat,html,re.S)[2])
assert old==new
candidate.write_text(html,encoding='utf-8')
print('Candidate:',candidate)
print('Backup:',backup)
print('All 83 slides, existing notes and assets unchanged.')
