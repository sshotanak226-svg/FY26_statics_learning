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
