/* Plain HTML slide framework. Edit through the form, or import/export deck JSON. */
'use strict';
function escapeHTML(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function formatted(s){return escapeHTML(s).replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>');}
const pristineHTML='<!DOCTYPE html>\n'+document.documentElement.outerHTML;
let deck=JSON.parse(document.getElementById('deck-data').textContent);
let current=0,editIndex=0,presenterWindow=null,undoStack=[],lastFocus=null,toastTimer=null;
let timerRunning=false,timerSeconds=0,timerStart=0;
const storageKey='stat-slides-v1-'+location.pathname;
const $=id=>document.getElementById(id);
const THEMES={explain:{name:'説明・解説・補足',color:'#1467b3'},proof:{name:'定理・補題・証明',color:'#242424'},question:{name:'質問',color:'#b9570b'}};
let agendaPage=0;
function safeHTML(raw){
 const t=document.createElement('template');t.innerHTML=String(raw||'');
 t.content.querySelectorAll('script,style,iframe,object,embed,base,link,meta,form,input,textarea,select,button').forEach(e=>e.remove());
 for(const e of t.content.querySelectorAll('*'))for(const a of [...e.attributes]){
  if(/^on/i.test(a.name)||a.name==='srcdoc'||['href','src','xlink:href','action'].includes(a.name)&&/^\s*(javascript|vbscript|data:text\/html):/i.test(a.value))e.removeAttribute(a.name);
 }
 return t.innerHTML;
}
// Share math recognition between Markdown protection, notation migration, and validation.
// Code examples stay literal; $$ must be matched before single-dollar inline math.
function mathFragments(raw){
 const source=String(raw||'');
 const masked=source.replace(/^[ \t]{0,3}(\x60{3,}|~{3,})[^\n]*\n[\s\S]*?^[ \t]{0,3}\1[ \t]*(?:\n|$)|(\x60+)[^\x60\n]*\2/gm,v=>v.replace(/[^\r\n]/g,' '));
 const pattern=/(?<!\\)\$\$([\s\S]*?)(?<!\\)\$\$|\\\(([\s\S]*?)\\\)|\\\[([\s\S]*?)\\\]|(?<![\\$])\$(?!\$)((?:\\.|[^\\$\r\n])+?)(?<!\\)\$(?!\$)/g;
 return [...masked.matchAll(pattern)].map(m=>({start:m.index,end:m.index+m[0].length,raw:source.slice(m.index,m.index+m[0].length),tex:m[1]??m[2]??m[3]??m[4],display:m[1]!==undefined||m[3]!==undefined}));
}
function inlineMathNotation(raw){
 let result=String(raw||'');
 for(const m of mathFragments(result).reverse())if(m.raw.startsWith('\\('))result=result.slice(0,m.start)+'$'+m.tex+'$'+result.slice(m.end);
 return result;
}
function markdownMarkup(raw){
 const source=String(raw||''),math=mathFragments(source);
 let protectedText='',from=0;
 math.forEach((m,i)=>{protectedText+=source.slice(from,m.start)+'MATHPLACEHOLDER'+i+'END';from=m.end;});
 protectedText+=source.slice(from);
 let result=marked.parse(protectedText,{gfm:true,breaks:true});
 result=result.replace(/MATHPLACEHOLDER(\d+)END/g,(_,i)=>escapeHTML(math[Number(i)].raw));
 return safeHTML(result).replace(/<ul>/g,'<ul class="body-list">');
}
function legacyLeft(s){return (s.body||[]).map(x=>'- '+x).join('\n\n')+(s.equations||[]).map(e=>'\n\n$$\n'+e.tex+'\n$$\n\n_'+(e.caption||'')+'_').join('');}
function legacyRight(s){if(s.table?.length)return '<table><thead><tr>'+s.table[0].map(x=>'<th>'+escapeHTML(x)+'</th>').join('')+'</tr></thead><tbody>'+s.table.slice(1).map(row=>'<tr>'+row.map(x=>'<td>'+escapeHTML(x)+'</td>').join('')+'</tr>').join('')+'</tbody></table>';return s.diagram?'<div data-diagram="'+escapeHTML(s.diagram)+'"></div>':'';}
function normalizeSlide(s){
 s.theme=Object.hasOwn(THEMES,s.theme)?s.theme:'explain';s.leftMarkdown=typeof s.leftMarkdown==='string'?s.leftMarkdown:legacyLeft(s);s.rightHTML=typeof s.rightHTML==='string'?s.rightHTML:legacyRight(s);
 s.leftMarkdown=inlineMathNotation(s.leftMarkdown);
 s.notes=typeof s.notes==='string'?s.notes:'';s.body=Array.isArray(s.body)?s.body:[];s.equations=Array.isArray(s.equations)?s.equations:[];s.sources=Array.isArray(s.sources)?s.sources:[];s.minutes=Number.isFinite(s.minutes)?s.minutes:1;s.layout=s.layout||'split';s.appendix=!!s.appendix;return s;
}
function normalizeDeck(d){d.assets=d.assets||{};d.editorVersion=2;d.slides.forEach(normalizeSlide);return d;}
function sectionId(s){return s.majorSection||s.title.match(/^(9\.\d+)/)?.[1]||'追加';}
function sectionLabel(id){const overview=deck.slides.find(s=>!s.appendix&&s.role==='section-overview'&&sectionId(s)===id);if(overview)return overview.title.replace(/^9\.\d+(?:\.\d+)?\s*/,'').replace(/^概要[:：]\s*/,'');const known=deck.sections?.find(x=>x.id===id)?.title;if(known)return known;const first=deck.slides.find(s=>!s.appendix&&sectionId(s)===id);return first?.title.replace(/^9\.\d+(?:\.\d+)?\s*/,'')||id;}
function agendaItems(){
 const result=[],seen=new Set();deck.slides.forEach((s,i)=>{if(s.appendix||['title','theme-guide','agenda'].includes(s.role||s.id))return;const id=sectionId(s);if(seen.has(id))return;seen.add(id);result.push({s,i,id});});return result;
}
function autoAgendaHTML(){
 return `<ol class="agenda-sections">${agendaItems().map(({i,id})=>`<li><button data-agenda-go="${i}"><strong>${escapeHTML(id)}</strong>　${escapeHTML(sectionLabel(id))}</button></li>`).join('')}</ol>`;
}

function rightMarkup(s){
 const raw=s.rightHTML??legacyRight(s);if(!raw.trim())return '';
 const box=document.createElement('div');box.innerHTML=safeHTML(raw);
 box.querySelectorAll('[data-auto-agenda]').forEach(e=>e.innerHTML=autoAgendaHTML());
 box.querySelectorAll('[data-diagram]').forEach(e=>{if(Object.hasOwn(DIAGRAM_NAMES,e.dataset.diagram)){e.classList.add('diagram');e.innerHTML=diagramHTML(e.dataset.diagram,s);}else e.textContent='図の名前を確認してください：'+e.dataset.diagram;});
 box.querySelectorAll('img[data-asset]').forEach(e=>{const data=deck.assets?.[e.dataset.asset];if(typeof data==='string'&&/^data:image\//i.test(data))e.src=data;else e.alt=e.alt||'画像データがありません';});
 return box.innerHTML;
}
function bindSlideActions(root){
 root.querySelectorAll('[data-agenda-page]').forEach(b=>b.onclick=()=>{agendaPage+=Number(b.dataset.agendaPage);render();});
 root.querySelectorAll('[data-agenda-go]').forEach(b=>b.onclick=()=>go(Number(b.dataset.agendaGo)));
}
async function insertImage(file){
 if(!file||!file.type.startsWith('image/')){toast('画像ファイルを選んでください。');return;}
 const data=await new Promise((resolve,reject)=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.onerror=reject;r.readAsDataURL(file);});
 const id='img-'+Date.now()+'-'+Math.random().toString(36).slice(2,7);historySnapshot();deck.assets[id]=data;
 deck.slides[editIndex].rightHTML=`<figure><img data-asset="${id}" alt="${escapeHTML(file.name||'挿入画像')}"></figure>`;
 stashDraft();populateForm();renderEditNav();if(current===editIndex)render();toast('右側に画像を挿入しました。画像も自動保存されます。');
}
function bindImageInput(){
 $('choose-image').onclick=()=>$('image-file').click();$('image-file').onchange=e=>{if(e.target.files[0])insertImage(e.target.files[0]).catch(()=>toast('画像を読み込めませんでした。'));e.target.value='';};
 const host=$('right-insertion');host.addEventListener('dragover',e=>{e.preventDefault();host.classList.add('dragging');});host.addEventListener('dragleave',()=>host.classList.remove('dragging'));host.addEventListener('drop',e=>{e.preventDefault();host.classList.remove('dragging');const f=[...e.dataTransfer.files].find(x=>x.type.startsWith('image/'));if(f)insertImage(f).catch(()=>toast('画像を読み込めませんでした。'));});
 $('edit-form').elements.rightHTML.addEventListener('paste',e=>{const f=[...(e.clipboardData?.items||[])].find(x=>x.type.startsWith('image/'))?.getAsFile();if(f){e.preventDefault();insertImage(f).catch(()=>toast('画像を読み込めませんでした。'));}});
}

function sourceRecord(id){return deck.sources?.[id]||{title:id,url:/^https:\/\//.test(id)?id:''};}
function mathMarkup(eq){let m;try{m=katex.renderToString(eq.tex,{displayMode:true,throwOnError:true,trust:false,strict:false});}catch(e){m=`<span class="katex-error">数式エラー：${escapeHTML(e.message)}</span>`;}return `<div class="equation"><div class="math">${m}</div>${eq.caption?`<div class="caption">${formatted(eq.caption)}</div>`:''}</div>`;}
function slideHTML(s,i){
 const left=markdownMarkup(s.leftMarkdown??legacyLeft(s)),right=rightMarkup(s),theme=Object.hasOwn(THEMES,s.theme)?s.theme:'explain';
 if(s.role==='title')return `<article class="slide title-only theme-${theme}"><h1>${formatted(s.title)}</h1></article>`;
 if(s.role==='agenda')return `<article class="slide agenda-only theme-${theme}"><h1>${formatted(s.title)}</h1><div class="agenda-full">${autoAgendaHTML()}</div></article>`;

 const main=deck.slides.filter(x=>!x.appendix),num=s.appendix?'Appendix '+deck.slides.filter((x,j)=>x.appendix&&x.role!=='title'&&j<=i).length:String(main.indexOf(s)+1).padStart(2,'0')+' / '+main.length;
 return `<article class="slide theme-${theme}${s.testExample?' test-example':''}${s.safeFlow?' safe-flow':''}" data-slide-id="${escapeHTML(s.id)}"><h1>${formatted(s.title)}</h1><div class="takeaway">${formatted(s.takeaway||'このスライドの要点')}</div><div class="content ${right?'has-diagram':'full-width'}"><div class="text-block markdown">${left}</div>${right?`<div class="visual-block right-content">${right}</div>`:''}</div><div class="foot"><span>${num}</span></div></article>`;
}
function renderMath(root){
 if(typeof renderMathInElement!=='function')return;
 renderMathInElement(root,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false},{left:'\\(',right:'\\)',display:false},{left:'\\[',right:'\\]',display:true}],throwOnError:false,trust:false,strict:false});
 // Keep complete equations together when large type makes a comma-separated line too wide.
 // This changes display formatting only; the editable Markdown stays untouched.
 for(const e of root.querySelectorAll('.katex-display')){
  const width=e.getBoundingClientRect().width;
  const natural=[...e.querySelectorAll('.katex-html>.base')].reduce((n,x)=>n+x.getBoundingClientRect().width,0);
  if(!width||natural<=width-4)continue;
  const tex=e.querySelector('annotation')?.textContent||'';
  const splits=[...tex.matchAll(/,\\quad\s*/g)],split=splits.at(-1);
  if(!split||tex.includes('\\begin{'))continue;
  const wrapped='\\begin{gathered}'+tex.slice(0,split.index)+'\\\\[6pt]'+tex.slice(split.index+split[0].length)+'\\end{gathered}';
  try{e.outerHTML=katex.renderToString(wrapped,{displayMode:true,throwOnError:true,trust:false,strict:false});}catch{}
 }
}
function mainIndices(){return deck.slides.map((s,i)=>s.appendix?-1:i).filter(i=>i>=0);}
function minutesText(m){const sec=Math.round(m*60);return `${Math.floor(sec/60)}分${sec%60?sec%60+'秒':''}`;}
function render(){
 const s=deck.slides[current];$('stage').innerHTML=slideHTML(s,current);renderMath($('stage'));bindDiagramEvents($('stage'));bindSlideActions($('stage'));
 const main=mainIndices(),pos=main.indexOf(current);$('counter').textContent=s.appendix?(s.role==='title'?'Appendix':`Appendix ${deck.slides.filter((x,i)=>x.appendix&&x.role!=='title'&&i<=current).length}`):`${pos+1} / ${main.length}`;
 $('help-main-count').textContent=main.length;$('help-appendix-count').textContent=deck.slides.length-main.length;document.querySelector('.brand').textContent=deck.title;
 $('prev').disabled=current===0;$('next').disabled=current===deck.slides.length-1;
 syncSlideSeek();
 document.title=s.title+' | '+deck.title;
 if(!isPresenter&&location.hash!=='#'+(current+1))history.replaceState(null,'','#'+(current+1));
 resizeStage();syncPresenter();
}
function syncSlideSeek(){
 const slider=$('slide-seek');if(!slider)return;
 const total=deck.slides.length,page=Math.min(current+1,Math.max(1,total)),slide=deck.slides[current];
 slider.max=String(Math.max(1,total));slider.value=String(page);slider.disabled=total<2;
 slider.setAttribute('aria-valuetext',`${page} / ${total}、${slide?.appendix?'Appendix、':''}${slide?.title||''}`);
 slider.title=`${page} / ${total}　${slide?.title||''}`;
 slider.style.setProperty('--seek-percent',`${total>1?(page-1)/(total-1)*100:0}%`);
 $('slide-seek-position').textContent=`${page} / ${total}`;
}
function resizeStage(){if(isPresenter)return;const r=$('viewport').getBoundingClientRect(),scale=Math.min((r.width-24)/1600,(r.height-20)/900);$('stage').style.transform=`translate(-50%, -50%) scale(${Math.max(.08,scale)})`;}
function go(i){if(!Number.isInteger(i)||i<0||i>=deck.slides.length)return;current=i;render();}
function advance(dir){const next=current+dir;if(next>=0&&next<deck.slides.length)go(next);}
function refreshCurrentDiagram(){
 const host=$('stage').querySelector('.diagram[data-diagram]');if(!host)return;const temp=document.createElement('div');temp.innerHTML=diagramHTML(host.dataset.diagram,deck.slides[current]);
 const old=host.querySelector('svg'),fresh=temp.querySelector('svg');if(old&&fresh)old.replaceWith(fresh);
 const oldNote=host.querySelector('.viz-note'),newNote=temp.querySelector('.viz-note');if(oldNote&&newNote)oldNote.replaceWith(newNote);
 const outputs=host.querySelectorAll('output');temp.querySelectorAll('output').forEach((o,i)=>{if(outputs[i])outputs[i].textContent=o.textContent;});syncPresenter();
}
function toast(msg){$('toast').textContent=msg;$('toast').classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').classList.remove('show'),4200);}
function openOverlay(id){closeOverlays(false);lastFocus=document.activeElement;$(id).classList.add('open');$(id).querySelector('button,input,select,textarea')?.focus();}
function closeOverlays(restore=true){document.querySelectorAll('.overlay.open').forEach(x=>x.classList.remove('open'));if(restore)lastFocus?.focus({preventScroll:true});}
function showOutline(){
 const groups=[['導入',deck.slides.map((s,i)=>[s,i]).filter(([s])=>!s.appendix&&['title','agenda'].includes(s.role))],...agendaItems().map(({id})=>[id+'　'+sectionLabel(id),deck.slides.map((s,i)=>[s,i]).filter(([s])=>!s.appendix&&!s.role&&sectionId(s)===id||s.role==='section-overview'&&sectionId(s)===id)]),['Appendix',deck.slides.map((s,i)=>[s,i]).filter(([s])=>s.appendix)]];
 $('outline-body').innerHTML=groups.map(([label,items])=>`<h3>${escapeHTML(label)}</h3><div class="outline-grid">${items.map(([s,i])=>`<button class="outline-item ${i===current?'active':''}" data-go="${i}"><small>${s.appendix?'Appendix':String(mainIndices().indexOf(i)+1).padStart(2,'0')}　${escapeHTML(s.subsection||'')}</small><strong>${escapeHTML(s.title)}</strong><small>${minutesText(s.minutes)}</small></button>`).join('')}</div>`).join('');
 $('outline-body').querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>{closeOverlays();go(Number(b.dataset.go));});openOverlay('outline');
}

function showSources(){
 const s=deck.slides[current];$('sources-body').innerHTML=`<p class="source-original">${escapeHTML(s.title)}<br><strong>原資料の対応：</strong>${escapeHTML(s.original||'このスライドには対応ページの指定がありません')}</p><ol class="source-list">${(s.sources||[]).map(id=>{const r=sourceRecord(id);return `<li>${/^https:\/\//.test(r.url||'')?`<a href="${escapeHTML(r.url)}" target="_blank" rel="noopener noreferrer">${escapeHTML(r.title)}</a>`:escapeHTML(r.title)}${r.detail?`<small>${escapeHTML(r.detail)}</small>`:''}</li>`;}).join('')}</ol><p>${escapeHTML(deck.referenceNote||'出典はスライド編集画面から追加できます。')}</p>`;openOverlay('sources');
}
function showNotes(){const s=deck.slides[current];$('notes-body').textContent=`${s.title}\n目安 ${minutesText(s.minutes)}${s.appendix?'（補足）':''}\n\n${s.notes}`;openOverlay('notes');}
async function fullscreen(){try{if(!document.fullscreenElement)await document.documentElement.requestFullscreen();else await document.exitFullscreen();}catch(e){toast('全画面を開始できません。ブラウザのF11でも切り替えられます。');}}
function timeValue(){return timerSeconds+(timerRunning?(Date.now()-timerStart)/1000:0);}
function clockText(v){const n=Math.floor(v);return String(Math.floor(n/60)).padStart(2,'0')+':'+String(n%60).padStart(2,'0');}
function toggleTimer(){if(timerRunning){timerSeconds=timeValue();timerRunning=false;}else{timerStart=Date.now();timerRunning=true;}$('timer-toggle').textContent=timerRunning?'Ⅱ 時間':'▶ 時間';updateTimer();}
function updateTimer(){if(isPresenter)return;$('timer').textContent=clockText(timeValue())+' / '+clockText(deck.plannedMinutes*60);syncPresenter();}
function openPresenter(){
 if(presenterWindow&&!presenterWindow.closed){presenterWindow.focus();syncPresenter();return;}
 const url=new URL(location.href);url.hash='presenter';presenterWindow=window.open(url.href,'stat-presenter','width=1300,height=900');
 if(!presenterWindow){toast('ブラウザが別ウィンドウを止めました。ポップアップを許可して再度押してください。');return;}
 toast('元のスライド画面を聴衆に共有し、発表者ウィンドウを手元に置いてください。');setTimeout(syncPresenter,1000);
}
function syncPresenter(){
 if(isPresenter||!presenterWindow||presenterWindow.closed)return;
 const main=mainIndices(),pos=main.indexOf(current),next=deck.slides[current+1];
 presenterWindow.postMessage({type:'deck-state',html:$('stage').innerHTML,current,slideId:deck.slides[current].id,title:deck.slides[current].title,notes:deck.slides[current].notes,minutes:deck.slides[current].minutes,next:next?.title||'最後のスライドです',elapsed:clockText(timeValue()),running:timerRunning,total:clockText(deck.plannedMinutes*60),plannedBefore:deck.slides.slice(0,current).filter(s=>!s.appendix).reduce((n,s)=>n+s.minutes,0)},'*');
}
function historySnapshot(){undoStack.push(JSON.stringify(deck));if(undoStack.length>80)undoStack.shift();}
let autoSaveTimer=null,autoSavePending=false,autoSaveRevision=0,autoSaveTime=0;
let autoSaveBrowserState='idle',autoSaveFileState='none',autoSaveFileHandle=null;
let autoSaveFileQueue=Promise.resolve(),autoSaveFileTasks=0,autoSaveErrorNotified=false;
let autoSaveConnectionEpoch=0;

function autoSaveClock(time){return new Date(time).toLocaleTimeString('ja-JP',{hour:'2-digit',minute:'2-digit',second:'2-digit'});}
function updateAutoSaveStatus(){
 let message='自動保存：編集すると保存します',kind='idle';
 if(autoSavePending){message='自動保存：保存待ち';kind='pending';}
 else if(autoSaveBrowserState==='saved'){message='ブラウザに保存済み '+autoSaveClock(autoSaveTime);kind='saved';}
 else if(autoSaveBrowserState==='error'){message='ブラウザ保存に失敗・HTMLを保存してください';kind='error';}
 if(autoSaveFileState==='saving'){message+=' ／ HTML保存中';kind='pending';}
 else if(autoSaveFileState==='saved'){message+=' ／ HTMLにも保存済み';}
 else if(autoSaveFileState==='error'){message+=' ／ HTML保存に失敗';kind='error';}
 else if(autoSaveFileState==='permission'){message+=' ／ 保存先を再接続してください';}
 else if(autoSaveFileState==='ready'){message+=' ／ HTML自動保存も有効';}
 for(const id of ['autosave-status','autosave-edit-status']){
  const e=$(id);if(!e)continue;e.textContent=message;e.dataset.state=kind;
  e.title=autoSaveFileHandle?'HTMLの保存先：'+autoSaveFileHandle.name:'編集内容は、このブラウザに保存され、同じHTMLを開くと自動復元されます。';
 }
 const button=$('autosave-file');if(!button)return;
 const available=typeof window.showSaveFilePicker==='function';
 button.disabled=!available;
 button.textContent=autoSaveFileHandle?(autoSaveFileState==='permission'||autoSaveFileState==='error'?'保存先を再接続':'接続を解除'):'保存先を接続';
 button.title=available?'HTMLファイルへの自動保存を設定します':'HTMLファイルへの自動保存はEdgeまたはChromeで利用できます。「HTMLを保存」で書き出すこともできます。';
}

function restoreAutomaticDraft(){
 try{
  const raw=localStorage.getItem(storageKey);if(!raw){updateAutoSaveStatus();return;}
  const draft=JSON.parse(raw),restored=validateDeck(draft.deck);
  if(JSON.stringify(restored)!==JSON.stringify(deck)){
   historySnapshot();deck=restored;
   const savedIndex=deck.slides.findIndex(s=>s.id===draft.currentSlideId);
   if(savedIndex>=0)current=editIndex=savedIndex;
   toast('自動保存した編集内容を復元しました。');
  }
  autoSaveTime=Number(draft.date)||Date.now();autoSaveBrowserState='saved';
 }catch(e){
  autoSaveBrowserState='error';
  toast('保存済みの編集内容を読み込めませんでした。現在のHTMLを表示しています。');
 }
 updateAutoSaveStatus();
}

function stashDraft(){
 autoSavePending=true;autoSaveRevision++;
 clearTimeout(autoSaveTimer);autoSaveTimer=setTimeout(flushAutoSave,650);
 updateAutoSaveStatus();
}
function persistAutomaticDraft(){
 try{
  const time=Date.now();
  localStorage.setItem(storageKey,JSON.stringify({version:2,date:time,currentSlideId:deck.slides[current]?.id,deck}));
  autoSaveTime=time;autoSaveBrowserState='saved';autoSaveErrorNotified=false;return true;
 }catch(e){
  autoSaveBrowserState='error';
  if(!autoSaveErrorNotified){toast('ブラウザへの自動保存に失敗しました。「HTMLを保存」で編集内容を書き出してください。');autoSaveErrorNotified=true;}
  return false;
 }
}
function buildSavedHTML(){
 const data=JSON.stringify(deck,null,2).replace(/</g,'\\u003c');
 return pristineHTML.replace(/(<script id="deck-data" type="application\/json">)[\s\S]*?(<\/script>)/,(_,a,b)=>a+'\n'+data+'\n'+b);
}
function flushAutoSave(){
 clearTimeout(autoSaveTimer);autoSaveTimer=null;
 if(!autoSavePending)return autoSaveFileQueue;
 autoSavePending=false;persistAutomaticDraft();
 if(autoSaveFileHandle&&autoSaveFileState!=='permission'&&autoSaveFileState!=='error')queueHTMLAutoSave(buildSavedHTML(),autoSaveRevision);
 updateAutoSaveStatus();return autoSaveFileQueue;
}
function queueHTMLAutoSave(html,revision){
 const handle=autoSaveFileHandle;if(!handle)return autoSaveFileQueue;
 autoSaveFileTasks++;autoSaveFileState='saving';updateAutoSaveStatus();
 autoSaveFileQueue=autoSaveFileQueue.catch(()=>{}).then(async()=>{
  let writable;
  try{
   if(handle!==autoSaveFileHandle)return;
   writable=await handle.createWritable();await writable.write(html);await writable.close();writable=null;
   if(handle===autoSaveFileHandle)autoSaveFileState=revision===autoSaveRevision&&!autoSavePending?'saved':'ready';
  }catch(e){
   if(writable)try{await writable.abort();}catch{}
   if(handle===autoSaveFileHandle){
    autoSaveFileState='error';
    toast('HTMLへの自動保存に失敗しました。保存先を再接続するか、「HTMLを保存」で書き出してください。');
   }
  }finally{
   autoSaveFileTasks--;if(autoSaveFileTasks&&autoSaveFileState!=='error')autoSaveFileState='saving';
   updateAutoSaveStatus();
  }
 });
 return autoSaveFileQueue;
}

function fileConnectionStore(mode,handle){
 return new Promise((resolve,reject)=>{
  const request=indexedDB.open('stat-slides-autosave-v1',1);
  request.onupgradeneeded=()=>{if(!request.result.objectStoreNames.contains('files'))request.result.createObjectStore('files');};
  request.onerror=()=>reject(request.error);request.onblocked=()=>reject(new Error('保存先の記録を開けません'));
  request.onsuccess=()=>{
   const db=request.result,tx=db.transaction('files',mode==='get'?'readonly':'readwrite'),store=tx.objectStore('files');
   let value;
   const operation=mode==='get'?store.get(storageKey):mode==='delete'?store.delete(storageKey):store.put(handle,storageKey);
   operation.onsuccess=()=>{value=operation.result;};
   tx.oncomplete=()=>{db.close();resolve(value);};tx.onerror=()=>{db.close();reject(tx.error);};tx.onabort=()=>{db.close();reject(tx.error||new Error('保存先の記録に失敗しました'));};
  };
 });
}
async function restoreFileConnection(){
 if(typeof window.showSaveFilePicker!=='function'){updateAutoSaveStatus();return;}
 const epoch=autoSaveConnectionEpoch;
 try{
  const handle=await fileConnectionStore('get');if(!handle)return;
  const permission=await handle.queryPermission({mode:'readwrite'});
  if(epoch!==autoSaveConnectionEpoch)return;
  autoSaveFileHandle=handle;
  autoSaveFileState=permission==='granted'?'ready':'permission';
 }catch{}
 updateAutoSaveStatus();
}
async function connectAutoSaveFile(){
 autoSaveConnectionEpoch++;
 try{
  if(autoSaveFileHandle&&autoSaveFileState!=='permission'&&autoSaveFileState!=='error'){
   await flushAutoSave();await autoSaveFileQueue;
   autoSaveFileHandle=null;autoSaveFileState='none';
   try{await fileConnectionStore('delete');}catch{}
   updateAutoSaveStatus();toast('HTMLの保存先との接続を解除しました。ブラウザへの自動保存は続きます。');return;
  }
  if(autoSaveFileHandle){
   const permission=await autoSaveFileHandle.requestPermission({mode:'readwrite'});
   if(permission!=='granted'){autoSaveFileState='permission';updateAutoSaveStatus();return;}
  }else{
   const name=(deck.slides.find(s=>!s.appendix)?.title||deck.title).replace(/[<>:"/\\|?*\u0000-\u001F]/g,'_').slice(0,70);
   autoSaveFileHandle=await window.showSaveFilePicker({suggestedName:name+'_自動保存.html',types:[{description:'HTMLスライド',accept:{'text/html':['.html']}}]});
   try{await fileConnectionStore('put',autoSaveFileHandle);}catch{}
  }
  autoSaveFileState='ready';autoSavePending=false;clearTimeout(autoSaveTimer);persistAutomaticDraft();
  await queueHTMLAutoSave(buildSavedHTML(),autoSaveRevision);
  if(autoSaveFileState==='saved')toast('このHTMLファイルにも編集内容を自動保存します。');
 }catch(e){
  if(e.name!=='AbortError')toast('保存先を接続できませんでした。ブラウザへの自動保存は利用できます。');
  updateAutoSaveStatus();
 }
}

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

function populateForm(){
 const s=normalizeSlide(deck.slides[editIndex]),f=$('edit-form');for(const name of ['theme','title','takeaway','leftMarkdown','rightHTML','notes'])f.elements[name].value=s[name]||'';
 $('image-preview').innerHTML='';const t=document.createElement('div');t.innerHTML=rightMarkup(s);const im=t.querySelector('img');if(im){$('image-preview').append(im.cloneNode(true));$('image-preview').classList.add('has-image');}else $('image-preview').classList.remove('has-image');
 $('edit-status').textContent='6項目で編集できます。発表原稿は発表者ツールに表示されます。';$('edit-status').classList.remove('error');
}
function lines(value){return value.split(/\r?\n/).map(x=>x.trim()).filter(Boolean);}
function formToSlide(){
 const f=$('edit-form'),s={...deck.slides[editIndex]};for(const name of ['theme','title','takeaway','leftMarkdown','rightHTML','notes'])s[name]=f.elements[name].value;
 s.body=lines(s.leftMarkdown).filter(x=>/^[-*+] /.test(x)).map(x=>x.slice(2));s.equations=[];s.diagram='';s.table=[];
 const number=s.title.match(/^(9\.\d+)(?:\.\d+)?/);if(number){s.majorSection=number[1];s.subsection=number[0];s.section=number[0];}if(s.theme==='question'&&s.original==='')s.section='質問';return s;
}
function commitForm(){
 const s=formToSlide();
 if(JSON.stringify(s)===JSON.stringify(deck.slides[editIndex]))return;historySnapshot();deck.slides[editIndex]=s;stashDraft();renderEditNav();if(editIndex===current)render();
 const errors=mathErrors([s]);$('edit-status').textContent=errors.length?'数式を確認：'+errors[0]:'変更を反映しました。編集内容は自動保存されます。';$('edit-status').classList.toggle('error',!!errors.length);
}
function showEditor(){editIndex=current;populateForm();renderEditNav();openOverlay('edit-dialog');requestAnimationFrame(()=>navRowForId(deck.slides[editIndex].id)?.scrollIntoView({block:'nearest'}));}
function bindMarkdownIndent(){
 const input=$('edit-form').elements.leftMarkdown;
 input.addEventListener('keydown',e=>{
  if(e.key!=='Tab'||e.ctrlKey||e.metaKey||e.altKey||e.isComposing)return;
  e.preventDefault();e.stopPropagation();
  const text=input.value,start=input.selectionStart,end=input.selectionEnd;
  const first=start===0?0:text.lastIndexOf('\n',start-1)+1;
  const last=end>start&&text[end-1]==='\n'?end-1:text.indexOf('\n',end);
  const limit=last<0?text.length:last;
  let firstDelta=0;
  const replacement=text.slice(first,limit).split('\n').map((line,i)=>{
   const removed=e.shiftKey?(line.match(/^(?:\t| {1,4})/)?.[0].length||0):0;
   const delta=e.shiftKey?-removed:4;if(i===0)firstDelta=delta;
   return e.shiftKey?line.slice(removed):'    '+line;
  }).join('\n');
  input.setRangeText(replacement,first,limit,'select');
  if(start===end){const caret=Math.max(first,start+firstDelta);input.setSelectionRange(caret,caret);}
  input.dispatchEvent(new Event('input',{bubbles:true}));
 });
}
function newSlide(duplicate=false){
 historySnapshot();const s=duplicate?JSON.parse(JSON.stringify(deck.slides[editIndex])):{title:'新しいスライド',theme:'explain',section:'追加',layout:'split',body:[],leftMarkdown:'',rightHTML:'',equations:[],diagram:'',table:[],takeaway:'',notes:'',original:'',sources:[],minutes:1,appendix:false};
 if(!duplicate){s.majorSection=sectionId(deck.slides[editIndex]);s.subsection=deck.slides[editIndex].subsection||s.majorSection;s.title=s.subsection+'　新しいスライド';}s.id='slide-'+Date.now()+'-'+Math.random().toString(36).slice(2,7);delete s.role;if(duplicate)s.title+='（複製）';deck.slides.splice(editIndex+1,0,s);editIndex++;current=editIndex;selectedSlideIds.clear();selectionAnchorId=deck.slides[editIndex].id;stashDraft();populateForm();renderEditNav();render();
}
function deleteSlide(){if(deck.slides.length<=1||(!deck.slides[editIndex].appendix&&mainIndices().length===1)){toast('本編には1枚以上のスライドが必要です。');return;}const removedId=deck.slides[editIndex].id;historySnapshot();deck.slides.splice(editIndex,1);selectedSlideIds.delete(removedId);editIndex=Math.min(editIndex,deck.slides.length-1);current=editIndex;stashDraft();populateForm();renderEditNav();render();toast('スライドを削除しました。「元に戻す」で復元できます。');}
function undo(){
 if(!undoStack.length){toast('戻せる変更がありません。');return;}
 const shownId=deck.slides[current]?.id,editingId=deck.slides[editIndex]?.id;
 deck=JSON.parse(undoStack.pop());
 const shown=deck.slides.findIndex(s=>s.id===shownId),editing=deck.slides.findIndex(s=>s.id===editingId);
 current=shown>=0?shown:Math.min(current,deck.slides.length-1);
 editIndex=editing>=0?editing:Math.min(editIndex,deck.slides.length-1);
 pruneSlideSelection();populateForm();renderEditNav();render();stashDraft();
}
function mathErrors(slides=deck.slides){
 const errors=[];for(const s of slides){const t=document.createElement('div');t.innerHTML=safeHTML(s.rightHTML||'');const text=[s.title,s.takeaway,s.leftMarkdown??legacyLeft(s),t.textContent].filter(Boolean).join('\n');
 for(const m of mathFragments(text)){try{katex.renderToString(m.tex,{displayMode:m.display,throwOnError:true,strict:false,trust:false});}catch(err){errors.push(s.title+'：'+err.message);}}}return errors;
}
function download(name,text,type){const url=URL.createObjectURL(new Blob([text],{type})),a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30000);}
function saveHTML(){const errors=mathErrors();if(errors.length){toast('数式エラーがあるため、まず式を修正してください：'+errors[0]);return;}const data=JSON.stringify(deck,null,2).replace(/</g,'\\u003c');const html=pristineHTML.replace(/(<script id="deck-data" type="application\/json">)[\s\S]*?(<\/script>)/,(_,a,b)=>a+data+b);const name=(deck.slides.find(s=>!s.appendix)?.title||deck.title).replace(/[<>:"/\\|?*\u0000-\u001F]/g,'_').slice(0,70);download(name+'_編集済み.html',html,'text/html;charset=utf-8');toast('編集済みHTMLをダウンロードしました。保存先から開いて確認してください。');}
function validateDeck(d){
 if(!d||d.version!==1||!Array.isArray(d.slides)||!d.slides.length||d.slides.length>500)throw Error('スライドデータは1〜500枚で指定してください。');
 const ids=new Set();for(const s of d.slides){if(typeof s.id!=='string'||ids.has(s.id)||typeof s.title!=='string')throw Error('各スライドに異なるidとタイトルが必要です。');ids.add(s.id);if(s.leftMarkdown!==undefined&&typeof s.leftMarkdown!=='string'||s.rightHTML!==undefined&&typeof s.rightHTML!=='string')throw Error('左欄・右欄は文字列で指定してください。');if(s.notes!==undefined&&typeof s.notes!=='string')throw Error('発表原稿は文字列で指定してください。');normalizeSlide(s);}
 if(!d.slides.some(s=>!s.appendix))throw Error('本編には1枚以上必要です。');d.sources=d.sources||{};d.plannedMinutes=Number(d.plannedMinutes)||45;return normalizeDeck(d);
}
async function importJSON(file){try{const d=validateDeck(JSON.parse(await file.text()));historySnapshot();deck=d;current=0;editIndex=0;stashDraft();populateForm();renderEditNav();render();toast('JSONを読み込みました。編集内容は自動保存されます。');}catch(e){toast('読み込めません：'+e.message);}}
function printDeck(all){
 $('print-slides').innerHTML=deck.slides.map((s,i)=>[s,i]).filter(([s])=>all||!s.appendix).map(([s,i])=>`<div class="print-page">${i===current?$('stage').innerHTML:slideHTML(s,i)}</div>`).join('');renderMath($('print-slides'));closeOverlays();document.fonts.ready.then(()=>window.print());
}

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

normalizeDeck(deck);
const isPresenter=location.hash==='#presenter';
if(isPresenter){bootstrapPresenter();}else{
 restoreAutomaticDraft();
 const initial=Number(location.hash.slice(1))-1;if(Number.isInteger(initial)&&initial>=0&&initial<deck.slides.length)current=initial;
 $('slide-seek').addEventListener('input',e=>go(Number(e.target.value)-1));
 $('prev').onclick=()=>advance(-1);$('next').onclick=()=>advance(1);$('overview').onclick=showOutline;$('full').onclick=fullscreen;$('presenter').onclick=openPresenter;$('source').onclick=showSources;$('editor').onclick=showEditor;$('help').onclick=()=>openOverlay('help-dialog');$('timer-toggle').onclick=toggleTimer;
 document.querySelectorAll('[data-close]').forEach(b=>b.onclick=()=>closeOverlays());document.querySelectorAll('.overlay').forEach(o=>o.addEventListener('click',e=>{if(e.target===o)closeOverlays();}));
 $('blackout').onclick=()=>$('blackout').classList.remove('show');$('print-main').onclick=()=>printDeck(false);$('print-all').onclick=()=>printDeck(true);
 bindImageInput();bindMarkdownIndent();bindMultiSlideControls();
 $('edit-script-jump').onclick=()=>{const input=$('edit-form').elements.notes;input.focus({preventScroll:true});input.scrollIntoView({block:'center',behavior:'auto'});};
 $('edit-form').addEventListener('submit',e=>e.preventDefault());$('edit-form').addEventListener('input',commitForm);$('edit-form').addEventListener('change',commitForm);
 $('add-slide').onclick=()=>newSlide();$('duplicate-slide').onclick=()=>newSlide(true);$('move-up').onclick=()=>moveSlide(-1);$('move-down').onclick=()=>moveSlide(1);$('remove-slide').onclick=deleteSlide;$('undo-edit').onclick=undo;$('preview-edit').onclick=()=>{current=editIndex;closeOverlays();render();};$('save-html').onclick=saveHTML;$('export-json').onclick=()=>download('スライドデータ.json',JSON.stringify(deck,null,2),'application/json;charset=utf-8');$('import-json').onclick=()=>$('json-file').click();$('json-file').onchange=e=>{if(e.target.files[0])importJSON(e.target.files[0]);e.target.value='';};
 $('autosave-file').onclick=connectAutoSaveFile;
 updateAutoSaveStatus();restoreFileConnection();
 window.addEventListener('pagehide',()=>{flushAutoSave();});
 document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='hidden')flushAutoSave();});
 window.addEventListener('resize',resizeStage);window.addEventListener('fullscreenchange',resizeStage);window.addEventListener('hashchange',()=>{const i=Number(location.hash.slice(1))-1;if(Number.isInteger(i)&&i>=0&&i<deck.slides.length)go(i);});
 window.addEventListener('message',ev=>{if(ev.source!==presenterWindow)return;if(ev.data?.type==='presenter-ready'){syncPresenter();return;}if(ev.data?.type!=='deck-command')return;switch(ev.data.command){case'next':advance(1);break;case'prev':advance(-1);break;case'timer':toggleTimer();break;case'reset':timerSeconds=0;timerStart=Date.now();updateTimer();break;case'focus':window.focus();break;case'edit-notes':window.focus();editPresenterScript();break;}});
 document.addEventListener('keydown',e=>{
  const overlay=document.querySelector('.overlay.open');if(e.key==='Escape'){closeOverlays();$('blackout').classList.remove('show');return;}
  if(overlay){if(e.key==='Tab'){const focus=[...overlay.querySelectorAll('button,input,textarea,select,a[href]')].filter(x=>!x.disabled&&x.offsetParent!==null),a=focus[0],z=focus.at(-1);if(e.shiftKey&&document.activeElement===a){e.preventDefault();z?.focus();}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a?.focus();}}return;}
  if(/INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName)||e.ctrlKey||e.metaKey||e.altKey)return;
  const key=e.key.toLowerCase();if(['ArrowRight','PageDown',' ','ArrowLeft','PageUp','Home','End'].includes(e.key))e.preventDefault();
  if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' ')advance(1);else if(e.key==='ArrowLeft'||e.key==='PageUp')advance(-1);else if(e.key==='Home')go(0);else if(e.key==='End')go(deck.slides.length-1);else if(key==='f')fullscreen();else if(key==='p')openPresenter();else if(key==='o')showOutline();else if(key==='s')showSources();else if(key==='n')showNotes();else if(key==='e')showEditor();else if(key==='b')$('blackout').classList.toggle('show');else if(key==='?'||key==='h')openOverlay('help-dialog');
 });
 let touch=null;$('viewport').addEventListener('touchstart',e=>{if(e.target.closest('button,input,select'))return;touch={x:e.changedTouches[0].clientX,y:e.changedTouches[0].clientY};},{passive:true});$('viewport').addEventListener('touchend',e=>{if(!touch)return;const dx=e.changedTouches[0].clientX-touch.x,dy=e.changedTouches[0].clientY-touch.y;if(Math.abs(dx)>55&&Math.abs(dx)>Math.abs(dy)*1.5)advance(dx<0?1:-1);touch=null;},{passive:true});
 setInterval(updateTimer,1000);render();
}
