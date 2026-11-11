let scriptWritingMode=false;
function resizeScriptPreview(){
 const host=$('script-slide-preview'),stage=$('script-preview-stage');
 if(!scriptWritingMode||!host||!stage)return;
 const scale=Math.max(.05,Math.min(host.clientWidth/1600,host.clientHeight/900));
 stage.style.transform=`translate(-50%,-50%) scale(${scale})`;
}
function renderScriptPreview(){
 if(!scriptWritingMode)return;
 const s=deck.slides[editIndex],stage=$('script-preview-stage');
 stage.innerHTML=slideHTML(s,editIndex);renderMath(stage);
 // Keep duplicated SVG and control IDs local to this read-only preview.
 const ids=new Map();stage.querySelectorAll('[id]').forEach(el=>{const old=el.id,fresh='script-copy-'+old;ids.set(old,fresh);el.id=fresh;});
 for(const el of stage.querySelectorAll('*'))for(const attr of [...el.attributes]){
  let v=attr.value;
  for(const [old,fresh] of ids){if(v==='#'+old)v='#'+fresh;v=v.split('url(#'+old+')').join('url(#'+fresh+')');if(['for','aria-labelledby','aria-describedby'].includes(attr.name))v=v.split(' ').map(x=>x===old?fresh:x).join(' ');}
  if(v!==attr.value)el.setAttribute(attr.name,v);
 }
 $('script-slide-picker').innerHTML=deck.slides.map((x,i)=>`<option value="${i}">${i+1}. ${escapeHTML(x.title)}</option>`).join('');
 $('script-slide-picker').value=String(editIndex);
 $('script-slide-prev').disabled=editIndex===0;$('script-slide-next').disabled=editIndex===deck.slides.length-1;
 $('script-slide-title').textContent=s.title;
 resizeScriptPreview();requestAnimationFrame(resizeScriptPreview);
}
function setScriptWritingMode(enabled,focus=false){
 scriptWritingMode=!!enabled;$('edit-dialog').classList.toggle('script-writing',scriptWritingMode);
 $('edit-dialog').querySelector('header h2').firstChild.nodeValue=scriptWritingMode?'発表原稿を作成 ':'スライド編集 ';
 $('edit-script-jump').textContent=scriptWritingMode?'← スライド編集に戻る':'原稿を編集';
 $('edit-script-jump').setAttribute('aria-pressed',String(scriptWritingMode));
 if(scriptWritingMode){renderScriptPreview();if(focus)requestAnimationFrame(()=>$('edit-script').focus({preventScroll:true}));}
}
function selectScriptSlide(i){
 if(!Number.isInteger(i)||i<0||i>=deck.slides.length)return;
 editIndex=i;populateForm();renderEditNav();
}
function commitScriptOnly(){
 const notes=$('edit-script').value,s=deck.slides[editIndex];if(notes===s.notes)return;
 historySnapshot();deck.slides[editIndex]={...s,notes};stashDraft();
 if(editIndex===current)syncPresenter();
 $('edit-status').textContent='原稿を反映しました。編集内容は自動保存されます。';$('edit-status').classList.remove('error');
}
function onEditorFieldChange(e){
 if(e.target.name==='notes'){commitScriptOnly();return;}
 if(['theme','title','takeaway','leftMarkdown','rightHTML'].includes(e.target.name))commitForm();
}
function bindScriptWriting(){
 $('script-slide-prev').onclick=()=>selectScriptSlide(editIndex-1);
 $('script-slide-next').onclick=()=>selectScriptSlide(editIndex+1);
 $('script-slide-picker').onchange=e=>selectScriptSlide(Number(e.target.value));
 window.addEventListener('resize',resizeScriptPreview);
 if(typeof ResizeObserver==='function')new ResizeObserver(resizeScriptPreview).observe($('script-slide-preview'));
}
