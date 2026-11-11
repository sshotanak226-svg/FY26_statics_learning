from pathlib import Path
import re,json,sys
sys.stdout.reconfigure(encoding='utf-8')
source=Path(r'C:\Users\User\Downloads\９章_仮説検定と信頼区間_例9.5説明追加.html')
target=Path(r'F:\Document\Fy26 TDH statics lean\output\９章_仮説検定と信頼区間_複数選択移動.html')
html=source.read_text(encoding='utf-8');result=html
def replace(old,new):
 global result
 assert result.count(old)==1,old[:100]
 result=result.replace(old,new)
start=result.index('function renderEditNav(){');end=result.index('function populateForm(){',start)
result=result[:start]+Path(r'F:\Document\Fy26 TDH statics lean\tmp\editor_multiselect.js').read_text(encoding='utf-8')+'\n'+result[end:]
old=re.search(r'function moveSlide\(dir\)\{const to=editIndex[\s\S]*?\n(?=function deleteSlide)',result)
assert old
result=result[:old.start()]+result[old.end():]
replace('</head>','''<style id="multi-slide-editor-style">
.editor-selection-bar{display:flex;align-items:center;gap:9px;padding:9px 14px;border-bottom:1px solid #dce5e4;background:#f8fafc;flex-wrap:wrap;font-size:13px;}
.editor-selection-bar button{font-size:13px;padding:7px 10px;}.editor-selection-bar label{display:flex;align-items:center;gap:7px;}
#selected-slide-count{font-weight:700;min-width:130px;color:#1467b3;}#move-target{max-width:340px;width:300px;padding:7px;border:1px solid #cad4d6;border-radius:6px;background:white;}
.editor-selection-hint{color:#52636b;font-size:12px;margin-left:auto;}.editor-work{grid-template-columns:300px minmax(0,1fr);}
.edit-nav{position:relative;padding:10px 8px;overscroll-behavior:contain;}
.edit-slide-row{display:flex;align-items:center;gap:4px;border:1px solid transparent;border-radius:7px;margin-bottom:6px;position:relative;background:transparent;}
.edit-slide-row.selected{background:#e6f0ff;border-color:#8ab5e5;}.edit-slide-row.being-dragged{opacity:.42;}
.edit-slide-row .slide-select{width:17px;height:17px;margin:0 2px 0 4px;accent-color:#1467b3;flex:none;cursor:pointer;}
.edit-slide-row .slide-grip{flex:none;width:22px;text-align:center;color:#607686;font-size:22px;cursor:grab;user-select:none;padding:5px 0;border-radius:4px;}
.edit-slide-row .slide-grip:hover,.edit-slide-row .slide-grip:focus-visible{color:#1467b3;background:#d4e7fb;outline:2px solid #1467b3;outline-offset:0;}
.edit-slide-row button.edit-slide-open{width:auto;min-width:0;flex:1;margin:0;text-align:left;padding:8px 7px;font-size:13px;line-height:1.4;overflow-wrap:anywhere;background:white;border-left:4px solid var(--theme,#1467b3);}
.edit-slide-row button.edit-slide-open.active{background:var(--theme,#1467b3);color:white;}.edit-slide-row.selected button.edit-slide-open:not(.active){background:#f1f6ff;}
.slide-drop-marker{position:absolute;left:7px;right:7px;height:0;border-top:3px solid #1467b3;z-index:5;pointer-events:none;}
.slide-drop-marker[hidden]{display:none;}.slide-drop-marker:before{content:'';position:absolute;left:-2px;top:-6px;width:9px;height:9px;border-radius:50%;background:#1467b3;}
.slide-drop-marker span{position:absolute;right:3px;top:-14px;background:#1467b3;color:white;border-radius:4px;padding:3px 7px;font-size:11px;white-space:nowrap;}
.slide-drag-ghost{position:fixed;left:-1000px;top:-1000px;width:280px;padding:12px 15px;border-radius:8px;background:#1467b3;color:white;box-shadow:0 6px 20px #0004;font-size:12px;}
.slide-drag-ghost strong{display:block;font-size:15px;margin-bottom:5px;}.slide-drag-ghost div{overflow:hidden;white-space:nowrap;text-overflow:ellipsis;margin-top:3px;}
@media(max-width:1000px){.editor-work{grid-template-columns:230px minmax(0,1fr);}.editor-selection-hint{width:100%;margin-left:0;}#move-target{width:260px;}}
@media(max-width:650px){.editor-work{grid-template-columns:190px minmax(0,1fr);}#move-target{max-width:210px;}.edit-slide-row button.edit-slide-open{font-size:12px;}}
</style></head>''')
replace('<div class="editor-work"><aside class="edit-nav"', '''<div class="editor-selection-bar"><span id="selected-slide-count" role="status" aria-live="polite">チェックで複数選択</span><button type="button" id="select-all-slides">全選択</button><button type="button" id="clear-slide-selection">選択解除</button><label>移動先<select id="move-target" aria-label="選択したページの移動先"><option value="">移動先を選択</option></select></label><button type="button" id="move-selected-slides">まとめて移動</button><span class="editor-selection-hint">チェックで複数選択 ／ Shiftで範囲選択 ／ ⠿をドラッグして移動</span></div><div class="editor-work"><aside class="edit-nav"''')
replace("function showEditor(){editIndex=current;populateForm();renderEditNav();openOverlay('edit-dialog');}", "function showEditor(){editIndex=current;populateForm();renderEditNav();openOverlay('edit-dialog');requestAnimationFrame(()=>navRowForId(deck.slides[editIndex].id)?.scrollIntoView({block:'nearest'}));}")
replace("editIndex++;current=editIndex;stashDraft();populateForm();renderEditNav();render();", "editIndex++;current=editIndex;selectedSlideIds.clear();selectionAnchorId=deck.slides[editIndex].id;stashDraft();populateForm();renderEditNav();render();")
replace("historySnapshot();deck.slides.splice(editIndex,1);editIndex=Math.min(editIndex,deck.slides.length-1);", "const removedId=deck.slides[editIndex].id;historySnapshot();deck.slides.splice(editIndex,1);selectedSlideIds.delete(removedId);editIndex=Math.min(editIndex,deck.slides.length-1);")
replace("function undo(){if(!undoStack.length){toast('戻せる変更がありません。');return;}deck=JSON.parse(undoStack.pop());current=Math.min(current,deck.slides.length-1);editIndex=Math.min(editIndex,deck.slides.length-1);populateForm();renderEditNav();render();stashDraft();}", """function undo(){
 if(!undoStack.length){toast('戻せる変更がありません。');return;}
 const shownId=deck.slides[current]?.id,editingId=deck.slides[editIndex]?.id;
 deck=JSON.parse(undoStack.pop());
 const shown=deck.slides.findIndex(s=>s.id===shownId),editing=deck.slides.findIndex(s=>s.id===editingId);
 current=shown>=0?shown:Math.min(current,deck.slides.length-1);
 editIndex=editing>=0?editing:Math.min(editIndex,deck.slides.length-1);
 pruneSlideSelection();populateForm();renderEditNav();render();stashDraft();
}""")
replace('bindImageInput();bindMarkdownIndent();','bindImageInput();bindMarkdownIndent();bindMultiSlideControls();')
old=re.search(r'function advance\(dir\)\{[\s\S]*?\n\}',result)
assert old
result=result[:old.start()]+"function advance(dir){const next=current+dir;if(next>=0&&next<deck.slides.length)go(next);}"+result[old.end():]
replace("$('prev').disabled=pos===0;","$('prev').disabled=current===0;")
replace("next=deck.slides[pos>=0?(main[pos+1]??current+1):current+1];","next=deck.slides[current+1];")
replace("else if(e.key==='Home')go(mainIndices()[0]);else if(e.key==='End')go(mainIndices().at(-1));", "else if(e.key==='Home')go(0);else if(e.key==='End')go(deck.slides.length-1);")
replace('<kbd>End</kbd> 本編の最後','<kbd>End</kbd> 最後のページ')
replace('通常のスライド送りは本編<span id="help-main-count">40</span>枚だけを進みます。質問<span id="help-appendix-count">1</span>枚は「目次」から開けます。','スライドは編集メニューのページ順に進みます。本編<span id="help-main-count">40</span>枚とAppendix<span id="help-appendix-count">1</span>枚を「目次」からも開けます。')
replace('<p><strong>編集内容は自動保存されます。</strong>', '<p><strong>複数ページの移動。</strong>編集画面の左側でチェックを付けると複数選択できます。Shift＋クリックで範囲選択もできます。⠿のつまみをドラッグすると、挿入位置が青い線で表示されます。選択したページは元の順番のまま移動します。リストの上端・下端では自動スクロールします。「移動先」と「まとめて移動」、上下のボタンでも移動できます。「元に戻す」で並べ替えを取り消せます。</p><p><strong>編集内容は自動保存されます。</strong>')
pat=r'<script id="deck-data" type="application/json">([\s\S]*?)</script>'
assert json.loads(re.search(pat,result).group(1))==json.loads(re.search(pat,html).group(1))
target.write_text(result,encoding='utf-8')
print(target)
print('All 79 slides and autosave preserved; multi-selection and drag/drop installed.')
