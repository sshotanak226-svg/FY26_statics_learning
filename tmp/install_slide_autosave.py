from pathlib import Path
import re,json,sys
sys.stdout.reconfigure(encoding='utf-8')
target=Path(r'F:\Document\Fy26 TDH statics lean\output\９章_仮説検定と信頼区間_Appendix多母数拡張.html')
source=target.read_text(encoding='utf-8')
backup=Path(r'F:\Document\Fy26 TDH statics lean\tmp\autosave-before.html')
assert 'function restoreAutomaticDraft()' not in source
backup.write_text(source,encoding='utf-8')
result=source
def replace(old,new):
 global result
 assert result.count(old)==1,old[:100]
 result=result.replace(old,new)
replace('<div class="hint">← → スライド送り', '<span id="autosave-status" class="autosave-status" role="status" aria-live="polite">自動保存：編集すると保存します</span><div class="hint">← → スライド送り')
style='''<style id="autosave-style">
.autosave-status{font-size:12px;line-height:1.4;color:#bfdfd3;white-space:normal;max-width:520px;margin:0 18px;}
.autosave-status[data-state="pending"]{color:#f0d49b;}.autosave-status[data-state="error"]{color:#ffb8aa;}
.editor-save-state{display:flex;flex-direction:column;gap:5px;flex:1;min-width:250px;}
.editor-save-state .autosave-status{color:#176b50;margin:0;max-width:none;}
.editor-save-state .autosave-status[data-state="pending"]{color:#8b6100;}.editor-save-state .autosave-status[data-state="error"]{color:#a32721;}
.editor-panel footer{flex-wrap:wrap;gap:10px;}
@media(max-width:1250px){.appbar .hint{display:none;}.autosave-status{max-width:65vw;margin-right:0;}}
</style>
'''
replace('</head>',style+'</head>')
replace('<span id="edit-status" class="status">変更を反映します。完成したらHTMLを保存してください。</span>', '<div class="editor-save-state"><span id="edit-status" class="status">編集内容は自動保存されます。</span><span id="autosave-edit-status" class="autosave-status" role="status" aria-live="polite">自動保存：編集すると保存します</span></div>')
replace('<button id="save-html" class="primary">HTMLを保存</button>', '<button id="autosave-file" type="button">保存先を接続</button><button id="save-html" class="primary">HTMLを保存</button>')
replace('<p><strong>保存は「HTMLを保存」</strong>。編集内容を含む新しいHTMLをダウンロードします。ブラウザの自動下書きは補助なので、必ずHTMLを保存してください。「JSONを書き出す」はバックアップやデータ編集用です。</p>', '<p><strong>編集内容は自動保存されます。</strong>同じブラウザで同じHTMLを開くと、自動復元されます。画面上部と編集画面に保存状態を表示します。ブラウザの保存データを削除すると復元できなくなるため、持ち運びやバックアップには「HTMLを保存」を使ってください。</p><p><strong>HTMLファイルにも自動保存する場合は「保存先を接続」</strong>。保存するHTMLを一度選ぶと、編集後にそのファイルを更新します。ブラウザが再接続を求める場合は同じボタンを押してください。EdgeまたはChromeで利用できます。「JSONを書き出す」もバックアップに使えます。</p>')
replace('function stashDraft(){try{localStorage.setItem(storageKey,JSON.stringify({date:Date.now(),deck}));}catch(e){} }', Path(r'F:\Document\Fy26 TDH statics lean\tmp\slide_autosave.js').read_text(encoding='utf-8'))
replace("'変更を反映しました。HTMLを保存すると編集内容が残ります。'", "'変更を反映しました。編集内容は自動保存されます。'")
replace("toast('右側に画像を挿入しました。HTMLを保存すると画像も含まれます。');", "toast('右側に画像を挿入しました。画像も自動保存されます。');")
replace("toast('JSONを読み込みました。HTMLを保存すると新しい内容が残ります。');", "toast('JSONを読み込みました。編集内容は自動保存されます。');")
old=""" $('restore-draft').onclick=()=>{try{const draft=JSON.parse(localStorage.getItem(storageKey));historySnapshot();deck=validateDeck(draft.deck);current=0;render();$('draft-banner').style.display='none';toast('下書きを復元しました。HTMLを保存して確定してください。');}catch(e){toast('下書きを復元できません：'+e.message);}};$('dismiss-draft').onclick=()=>$('draft-banner').style.display='none';
 try{const draft=JSON.parse(localStorage.getItem(storageKey));if(draft?.deck&&JSON.stringify(draft.deck)!==JSON.stringify(deck))$('draft-banner').style.display='block';}catch(e){}"""
replace(old,""" $('autosave-file').onclick=connectAutoSaveFile;
 updateAutoSaveStatus();restoreFileConnection();
 window.addEventListener('pagehide',()=>{flushAutoSave();});
 document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='hidden')flushAutoSave();});""")
replace("}else{\n const initial=Number(location.hash.slice(1))-1;", "}else{\n restoreAutomaticDraft();\n const initial=Number(location.hash.slice(1))-1;")
replace('<div id="draft-banner" class="draft-banner">前回の下書きがあります <button id="restore-draft">復元</button><button id="dismiss-draft">閉じる</button></div>','')
# No content, formula, slide order, or asset change.
pat=r'<script id="deck-data" type="application/json">([\s\S]*?)</script>'
assert json.loads(re.search(pat,result).group(1))==json.loads(re.search(pat,source).group(1))
target.write_text(result,encoding='utf-8')
print(target)
print('All 76 slides unchanged; autosave behavior installed.')
