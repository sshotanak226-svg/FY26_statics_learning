function bootstrapPresenter(){
 document.body.classList.add('presenter-mode');
 document.body.innerHTML=`<div class="presenter-layout"><div class="presenter-left"><h2>発表者表示（手元の画面）</h2><div class="presenter-preview" id="present-preview"></div><div class="presenter-info" id="present-info">元のスライド画面と接続しています…</div><div class="presenter-buttons"><button data-command="prev">← 前へ</button><button data-command="next">次へ →</button><button data-command="timer">タイマー開始 / 一時停止</button><button data-command="reset">時間をリセット</button><button data-command="focus">スライド画面へ</button></div><h2>次のスライド</h2><p id="present-next"></p><p class="presenter-sharing-hint">聴衆には元のスライドウィンドウを共有してください。</p></div><section class="presenter-script-column" aria-label="発表原稿"><div class="presenter-script-heading"><h2>発表原稿</h2><div class="presenter-script-tools"><button type="button" id="script-smaller" aria-label="原稿の文字を小さくする">A−</button><output id="script-font-size" aria-live="polite">22px</output><button type="button" id="script-larger" aria-label="原稿の文字を大きくする">A＋</button><button type="button" data-command="edit-notes">原稿を編集</button></div></div><h3 id="present-title">接続しています…</h3><div class="presenter-notes" id="present-notes" tabindex="0" aria-label="このスライドの発表原稿"></div><p class="presenter-script-hint">編集画面の「6. 発表原稿」と同期します。改行・Markdown・数式を使えます。</p></section></div>`;
 const notes=$('present-notes');
 let shownSlide=null,shownNotes=null,previewHTML=null,fontSize=22;
 try{const stored=Number(localStorage.getItem('stat-presenter-script-size'));if(stored>=16&&stored<=36)fontSize=stored;}catch{}
 function setFontSize(size){
  fontSize=Math.max(16,Math.min(36,size));notes.style.fontSize=fontSize+'px';
  $('script-font-size').textContent=fontSize+'px';$('script-smaller').disabled=fontSize<=16;$('script-larger').disabled=fontSize>=36;
  try{localStorage.setItem('stat-presenter-script-size',String(fontSize));}catch{}
 }
 setFontSize(fontSize);
 $('script-smaller').onclick=()=>setFontSize(fontSize-2);$('script-larger').onclick=()=>setFontSize(fontSize+2);
 function scale(){const host=$('present-preview'),s=host.querySelector('.slide');if(s)s.style.transform=`scale(${host.clientWidth/1600})`;}
 window.addEventListener('message',ev=>{
  if(ev.source!==window.opener||ev.data?.type!=='deck-state')return;
  const d=ev.data,slideKey=d.slideId??d.current,raw=typeof d.notes==='string'?d.notes:'';
  if(previewHTML!==d.html){$('present-preview').innerHTML=d.html;$('present-preview').style.pointerEvents='none';previewHTML=d.html;scale();}
  if(slideKey!==shownSlide||raw!==shownNotes){
   const scrollTop=slideKey===shownSlide?notes.scrollTop:0;
   notes.innerHTML=raw.trim()?markdownMarkup(raw):'<p class="presenter-empty-script">原稿が未入力です。「原稿を編集」から入力できます。</p>';
   renderMath(notes);notes.scrollTop=scrollTop;shownSlide=slideKey;shownNotes=raw;
  }
  $('present-title').textContent=d.title;$('present-next').textContent=d.next;
  $('present-info').textContent=`経過 ${d.elapsed} / ${d.total}　${d.running?'計測中':'一時停止'}\nこのスライドの目安：${minutesText(d.minutes)}　開始予定：${minutesText(d.plannedBefore)}`;
 });
 window.addEventListener('resize',scale);
 document.querySelectorAll('[data-command]').forEach(b=>b.onclick=()=>window.opener?.postMessage({type:'deck-command',command:b.dataset.command},'*'));
 window.addEventListener('keydown',e=>{
  if(e.ctrlKey||e.metaKey||e.altKey||e.isComposing||e.target.closest('button,input,select,textarea,a[href]'))return;
  if(e.key==='ArrowRight'||e.key===' '&&!notes.contains(document.activeElement)){e.preventDefault();window.opener?.postMessage({type:'deck-command',command:'next'},'*');}
  if(e.key==='ArrowLeft'){e.preventDefault();window.opener?.postMessage({type:'deck-command',command:'prev'},'*');}
 });
 if(window.opener)window.opener.postMessage({type:'presenter-ready'},'*');else{$('present-info').textContent='元のスライド画面から「発表者表示」を押して開いてください。';}
}

function editPresenterScript(){
 showEditor();
 const input=$('edit-form').elements.notes;
 input.focus({preventScroll:true});input.scrollIntoView({block:'center',behavior:'auto'});
}
