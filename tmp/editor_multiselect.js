let selectedSlideIds=new Set(),selectionAnchorId=null;
let dragSlideIds=[],slideDropBoundary=null,slideDragY=null,slideDragScrollFrame=null,slideDragGhost=null;
let suppressEditClickUntil=0;

function selectedIdsInOrder(){return deck.slides.filter(s=>selectedSlideIds.has(s.id)).map(s=>s.id);}
function pruneSlideSelection(){
 const valid=new Set(deck.slides.map(s=>s.id));
 selectedSlideIds=new Set([...selectedSlideIds].filter(id=>valid.has(id)));
 if(!valid.has(selectionAnchorId))selectionAnchorId=null;
}
function effectiveMoveIds(){const ids=selectedIdsInOrder();return ids.length?ids:[deck.slides[editIndex].id];}
function navRowForId(id){return [...$('edit-nav').querySelectorAll('.edit-slide-row')].find(e=>e.dataset.slideId===id);}
function selectSlideForMove(id,checked,range=false){
 const index=deck.slides.findIndex(s=>s.id===id),anchor=deck.slides.findIndex(s=>s.id===selectionAnchorId);
 if(range&&anchor>=0){
  for(let i=Math.min(index,anchor);i<=Math.max(index,anchor);i++){
   if(checked)selectedSlideIds.add(deck.slides[i].id);else selectedSlideIds.delete(deck.slides[i].id);
  }
 }else{
  if(checked)selectedSlideIds.add(id);else selectedSlideIds.delete(id);
  selectionAnchorId=id;
 }
 updateSlideSelectionUI();
}
function updateSlideSelectionUI(){
 pruneSlideSelection();const count=selectedSlideIds.size;
 for(const row of $('edit-nav').querySelectorAll('.edit-slide-row')){
  const selected=selectedSlideIds.has(row.dataset.slideId);
  row.classList.toggle('selected',selected);row.querySelector('input').checked=selected;
 }
 $('selected-slide-count').textContent=count?`${count}枚選択中`:'チェックで複数選択';
 $('clear-slide-selection').disabled=count===0;
 $('select-all-slides').disabled=count===deck.slides.length;
 const ids=new Set(effectiveMoveIds()),positions=deck.slides.map((s,i)=>ids.has(s.id)?i:-1).filter(i=>i>=0);
 $('move-up').disabled=positions[0]===0;
 $('move-down').disabled=positions.at(-1)===deck.slides.length-1;
 $('move-up').title=$('move-down').title=count?'選択したページをまとめて1つ移動します':'編集中のページを1つ移動します';
 $('duplicate-slide').textContent=count>1?'編集中を複製':'複製';
 $('remove-slide').textContent=count>1?'編集中を削除':'削除';
 $('duplicate-slide').title=$('remove-slide').title='現在の編集欄に表示している1枚が対象です';
 const target=$('move-target');
 for(const option of target.options)if(option.dataset.slideTarget)option.disabled=selectedSlideIds.has(option.dataset.slideTarget);
 if(target.selectedOptions[0]?.disabled)target.value='';
 $('move-selected-slides').disabled=count===0||!target.value;
}
function renderEditNav(){
 pruneSlideSelection();const nav=$('edit-nav'),scroll=nav.scrollTop;
 const focus=document.activeElement,focusedId=focus?.closest('.edit-slide-row')?.dataset.slideId;
 const focusKind=focus?.matches('input')?'checkbox':focus?.matches('.slide-grip')?'grip':'open';
 const oldTarget=$('move-target').value;
 let lastSection='';
 nav.innerHTML=deck.slides.map((s,i)=>{
  const section=s.appendix?'Appendix':['title','agenda'].includes(s.role)?'導入':sectionId(s);
  const heading=section!==lastSection?`<h3 class="edit-section">${escapeHTML(section)}${['導入','Appendix'].includes(section)?'':' '+escapeHTML(sectionLabel(section))}</h3>`:'';
  lastSection=section;
  const label=String(i+1)+'　'+s.title;
  return heading+`<div class="edit-slide-row theme-${s.theme} ${i===editIndex?'editing':''} ${selectedSlideIds.has(s.id)?'selected':''}" data-slide-id="${escapeHTML(s.id)}" data-slide-index="${i}" draggable="true"><input type="checkbox" class="slide-select" data-select-slide="${escapeHTML(s.id)}" aria-label="${escapeHTML(label+'を選択')}" ${selectedSlideIds.has(s.id)?'checked':''}><span class="slide-grip" role="button" tabindex="0" aria-label="${escapeHTML(label+'を移動')}" title="ドラッグして移動。上下キーでも移動できます">⠿</span><button type="button" class="edit-slide-open ${i===editIndex?'active':''}" data-edit-slide="${i}" ${i===editIndex?'aria-current="true"':''}>${escapeHTML(label)}</button></div>`;
 }).join('')+'<div id="slide-drop-marker" class="slide-drop-marker" hidden><span></span></div>';
 for(const row of nav.querySelectorAll('.edit-slide-row')){
  const id=row.dataset.slideId,checkbox=row.querySelector('input'),button=row.querySelector('button'),grip=row.querySelector('.slide-grip');
  checkbox.onclick=e=>{e.stopPropagation();selectSlideForMove(id,checkbox.checked,e.shiftKey);};
  button.onclick=e=>{
   if(Date.now()<suppressEditClickUntil)return;
   if(e.shiftKey){selectSlideForMove(id,true,true);return;}
   if(e.ctrlKey||e.metaKey){selectSlideForMove(id,!selectedSlideIds.has(id));return;}
   editIndex=deck.slides.findIndex(s=>s.id===id);selectionAnchorId=id;populateForm();renderEditNav();
  };
  grip.onkeydown=e=>{
   if(e.key==='ArrowUp'||e.key==='ArrowDown'){
    e.preventDefault();if(!selectedSlideIds.has(id)){selectedSlideIds=new Set([id]);updateSlideSelectionUI();}
    moveSlide(e.key==='ArrowUp'?-1:1);
   }else if(e.key===' '||e.key==='Enter'){e.preventDefault();selectSlideForMove(id,!selectedSlideIds.has(id),e.shiftKey);}
  };
  row.onpointerdown=e=>{row.dataset.checkboxDrag=e.target===checkbox?'true':'false';};
  row.ondragstart=e=>startSlideDrag(e,id,row);
  row.ondragend=finishSlideDrag;
 }
 nav.ondragover=e=>{
  if(!dragSlideIds.length)return;e.preventDefault();e.dataTransfer.dropEffect='move';
  slideDragY=e.clientY;showSlideDropBoundary(slideBoundaryAt(e.clientY));startSlideDragScroll();
 };
 nav.ondrop=e=>{
  if(!dragSlideIds.length)return;e.preventDefault();
  const ids=[...dragSlideIds],boundary=slideBoundaryAt(e.clientY);finishSlideDrag();
  moveSlidesToBoundary(ids,boundary);
 };
 nav.ondragleave=e=>{
  const r=nav.getBoundingClientRect();
  if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom){
   $('slide-drop-marker').hidden=true;slideDragY=null;
  }
 };
 $('move-target').innerHTML='<option value="">移動先を選択</option><option value="start">先頭へ</option>'+deck.slides.map((s,i)=>`<option value="before:${escapeHTML(s.id)}" data-slide-target="${escapeHTML(s.id)}">${i+1}ページ：${escapeHTML(s.title)} の前</option>`).join('')+'<option value="end">最後へ</option>';
 if([...$('move-target').options].some(o=>o.value===oldTarget))$('move-target').value=oldTarget;
 nav.scrollTop=scroll;
 if(focusedId){
  const row=navRowForId(focusedId),element=row?.querySelector(focusKind==='checkbox'?'input':focusKind==='grip'?'.slide-grip':'button');
  element?.focus({preventScroll:true});
 }
 const sum=deck.slides.filter(s=>!s.appendix).reduce((n,s)=>n+s.minutes,0);
 $('edit-time').textContent=`　本編 ${sum.toFixed(1)}分（質疑別枠${Math.max(0,deck.plannedMinutes-sum).toFixed(1)}分）`;
 updateSlideSelectionUI();
}
function startSlideDrag(e,id,row){
 if(row.dataset.checkboxDrag==='true'){e.preventDefault();return;}
 if(!selectedSlideIds.has(id))selectedSlideIds=new Set([id]);
 dragSlideIds=selectedIdsInOrder();updateSlideSelectionUI();
 e.dataTransfer.effectAllowed='move';e.dataTransfer.setData('application/x-stat-slide-ids',JSON.stringify(dragSlideIds));
 e.dataTransfer.setData('text/plain',`${dragSlideIds.length}枚のスライドを移動`);
 for(const item of $('edit-nav').querySelectorAll('.edit-slide-row'))item.classList.toggle('being-dragged',dragSlideIds.includes(item.dataset.slideId));
 slideDragGhost=document.createElement('div');slideDragGhost.className='slide-drag-ghost';
 const heading=document.createElement('strong');heading.textContent=`${dragSlideIds.length}枚をまとめて移動`;slideDragGhost.append(heading);
 for(const sid of dragSlideIds.slice(0,3)){
  const label=document.createElement('div');label.textContent=deck.slides.find(s=>s.id===sid).title;slideDragGhost.append(label);
 }
 document.body.append(slideDragGhost);e.dataTransfer.setDragImage(slideDragGhost,18,18);
 suppressEditClickUntil=Date.now()+1000;
}
function slideBoundaryAt(y){
 for(const row of $('edit-nav').querySelectorAll('.edit-slide-row')){
  const r=row.getBoundingClientRect();if(y<r.top+r.height/2)return Number(row.dataset.slideIndex);
 }
 return deck.slides.length;
}
function showSlideDropBoundary(boundary){
 slideDropBoundary=boundary;const marker=$('slide-drop-marker');if(!marker)return;
 const rows=[...$('edit-nav').querySelectorAll('.edit-slide-row')];
 const row=rows[boundary]||rows.at(-1);if(!row)return;
 marker.style.top=(boundary<rows.length?row.offsetTop:row.offsetTop+row.offsetHeight)+'px';
 marker.querySelector('span').textContent=`ここに${dragSlideIds.length}枚を移動`;
 marker.hidden=false;
}
function startSlideDragScroll(){
 if(slideDragScrollFrame!==null)return;
 const tick=()=>{
  slideDragScrollFrame=null;if(!dragSlideIds.length||slideDragY===null)return;
  const nav=$('edit-nav'),r=nav.getBoundingClientRect(),margin=48;
  let speed=0;
  if(slideDragY<r.top+margin)speed=-Math.min(15,Math.max(2,(r.top+margin-slideDragY)/3));
  else if(slideDragY>r.bottom-margin)speed=Math.min(15,Math.max(2,(slideDragY-r.bottom+margin)/3));
  if(speed){nav.scrollTop+=speed;showSlideDropBoundary(slideBoundaryAt(slideDragY));}
  slideDragScrollFrame=requestAnimationFrame(tick);
 };
 slideDragScrollFrame=requestAnimationFrame(tick);
}
function finishSlideDrag(){
 if(dragSlideIds.length)suppressEditClickUntil=Date.now()+250;
 dragSlideIds=[];slideDropBoundary=null;slideDragY=null;
 if(slideDragScrollFrame!==null)cancelAnimationFrame(slideDragScrollFrame);slideDragScrollFrame=null;
 slideDragGhost?.remove();slideDragGhost=null;
 const marker=$('slide-drop-marker');if(marker)marker.hidden=true;
 for(const row of $('edit-nav').querySelectorAll('.being-dragged'))row.classList.remove('being-dragged');
}
function applySlideOrder(next,movingIds){
 if(next.every((s,i)=>s.id===deck.slides[i].id))return false;
 const shownId=deck.slides[current]?.id,editingId=deck.slides[editIndex]?.id;
 historySnapshot();deck.slides=next;
 current=Math.max(0,deck.slides.findIndex(s=>s.id===shownId));
 editIndex=Math.max(0,deck.slides.findIndex(s=>s.id===editingId));
 stashDraft();populateForm();renderEditNav();render();
 navRowForId(movingIds[0])?.scrollIntoView({block:'nearest'});
 toast(`${movingIds.length}枚のページを移動しました。「元に戻す」で戻せます。`);
 return true;
}
function moveSlidesToBoundary(ids,boundary){
 const chosen=new Set(ids),old=deck.slides,moving=old.filter(s=>chosen.has(s.id));
 if(!moving.length)return false;
 const rest=old.filter(s=>!chosen.has(s.id));
 const insertAt=old.slice(0,Math.max(0,Math.min(boundary,old.length))).filter(s=>!chosen.has(s.id)).length;
 return applySlideOrder([...rest.slice(0,insertAt),...moving,...rest.slice(insertAt)],moving.map(s=>s.id));
}
function moveSlide(dir){
 const ids=effectiveMoveIds(),chosen=new Set(ids),next=[...deck.slides];
 const positions=next.map((s,i)=>chosen.has(s.id)?i:-1).filter(i=>i>=0);
 if(dir<0&&positions[0]===0||dir>0&&positions.at(-1)===next.length-1)return;
 if(dir<0){
  for(let i=1;i<next.length;i++)if(chosen.has(next[i].id)&&!chosen.has(next[i-1].id))[next[i-1],next[i]]=[next[i],next[i-1]];
 }else{
  for(let i=next.length-2;i>=0;i--)if(chosen.has(next[i].id)&&!chosen.has(next[i+1].id))[next[i+1],next[i]]=[next[i],next[i+1]];
 }
 applySlideOrder(next,ids);
}
function moveSelectedSlides(){
 const ids=selectedIdsInOrder(),target=$('move-target').value;if(!ids.length||!target)return;
 const boundary=target==='start'?0:target==='end'?deck.slides.length:deck.slides.findIndex(s=>s.id===target.slice(7));
 if(boundary>=0)moveSlidesToBoundary(ids,boundary);
}
function bindMultiSlideControls(){
 $('select-all-slides').onclick=()=>{selectedSlideIds=new Set(deck.slides.map(s=>s.id));updateSlideSelectionUI();};
 $('clear-slide-selection').onclick=()=>{selectedSlideIds.clear();selectionAnchorId=null;updateSlideSelectionUI();};
 $('move-target').onchange=updateSlideSelectionUI;
 $('move-selected-slides').onclick=moveSelectedSlides;
}
