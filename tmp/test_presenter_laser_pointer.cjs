const{chromium}=require('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const{pathToFileURL}=require('url'),fs=require('fs'),assert=require('assert/strict');
const file='F:/Document/Fy26 TDH statics lean/output/９章_仮説検定と信頼区間_発表者ポインタ連動.html';
const dir='F:/Document/Fy26 TDH statics lean/tmp/presenter-pointer-qa';fs.mkdirSync(dir,{recursive:true});let browser;
(async()=>{
 browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const c=await browser.newContext({viewport:{width:1720,height:1060}}),p=await c.newPage(),errors=[];p.setDefaultTimeout(12000);p.on('pageerror',e=>errors.push(e.message));
 await p.goto(pathToFileURL(file).href+'#49');await p.evaluate(()=>document.fonts.ready);
 const baseline=await p.evaluate(()=>({deck:JSON.stringify(deck),revision:autoSaveRevision}));
 const event=p.waitForEvent('popup');await p.locator('#presenter').click();const popup=await event;popup.setDefaultTimeout(12000);popup.on('pageerror',e=>errors.push(e.message));await popup.setViewportSize({width:1440,height:1000});await popup.waitForSelector('#present-preview .slide');await popup.evaluate(()=>document.fonts.ready);
 const records=[];
 async function point(x,y,label){
  await popup.bringToFront();const r=await popup.locator('#present-preview .slide').boundingBox();await popup.mouse.move(r.x+r.width*x,r.y+r.height*y);
  await p.waitForFunction(({x,y})=>{const e=document.querySelector('#audience-laser-pointer');return e&&!e.hidden&&audienceLaserState&&Math.abs(audienceLaserState.x-x)<.002&&Math.abs(audienceLaserState.y-y)<.002},{x,y},{timeout:12000});
  const mapped=await p.evaluate(()=>{const s=document.querySelector('#stage .slide').getBoundingClientRect(),d=document.querySelector('#audience-laser-pointer').getBoundingClientRect();return{x:(d.x+d.width/2-s.x)/s.width,y:(d.y+d.height/2-s.y)/s.height}});
  assert(Math.abs(mapped.x-x)<.002,label);assert(Math.abs(mapped.y-y)<.002,label);assert(await popup.locator('#presenter-laser-pointer').isVisible());records.push({label,x,y,mapped});
 }
 await point(.15,.2,'upper left');await point(.92,.91,'lower right');await point(.59,.56,'formula center');
 await p.screenshot({path:dir+'/audience-pointer.png'});await popup.screenshot({path:dir+'/presenter-pointer.png'});
 assert.equal(await p.locator('#stage .linked-laser-pointer').count(),0);
 const notes=await popup.locator('#present-notes').boundingBox();await popup.mouse.move(notes.x+20,notes.y+40);await p.waitForFunction(()=>document.querySelector('#audience-laser-pointer').hidden);assert(!(await popup.locator('#presenter-laser-pointer').isVisible()));
 await point(.3,.4,'before audience resize');await p.setViewportSize({width:1100,height:800});
 await p.waitForFunction(()=>{const e=document.querySelector('#audience-laser-pointer'),s=document.querySelector('#stage .slide').getBoundingClientRect(),d=e.getBoundingClientRect();return !e.hidden&&Math.abs((d.x+d.width/2-s.x)/s.width-.3)<.002});
 await point(.75,.65,'resized audience');await popup.setViewportSize({width:1050,height:780});await p.waitForFunction(()=>document.querySelector('#audience-laser-pointer').hidden);await point(.65,.3,'resized presenter');
 const staleId=await p.evaluate(()=>deck.slides[current].id);await p.evaluate(()=>advance(1));await p.waitForFunction(()=>document.querySelector('#audience-laser-pointer').hidden);await popup.waitForFunction(()=>document.querySelector('#present-title').textContent.includes('非正規'));
 await popup.evaluate(slideId=>opener.postMessage({type:'deck-laser-pointer',visible:true,slideId,x:.4,y:.4},'*'),staleId);assert(await p.locator('#audience-laser-pointer').evaluate(e=>e.hidden));await point(.45,.5,'next slide');
 // Fullscreen uses the audience slide rectangle, not the presenter window size.
 await p.locator('#full').click();await p.waitForFunction(()=>document.fullscreenElement!==null);await point(.7,.7,'fullscreen audience');await p.evaluate(()=>document.exitFullscreen());
 await p.evaluate(()=>go(48));await popup.waitForFunction(()=>document.querySelector('#present-title').textContent.includes('相関の統計量'));await point(.2,.5,'return slide');
 await p.locator('#editor').click();await p.waitForFunction(()=>document.querySelector('#audience-laser-pointer').hidden);assert(await p.locator('#script-slide-preview').isVisible());await p.locator('#edit-dialog [data-close]').click();
 const after=await p.evaluate(()=>({deck:JSON.stringify(deck),revision:autoSaveRevision}));assert.deepEqual(after,baseline);
 const saved=await p.evaluate(()=>buildSavedHTML());assert(saved.includes('function receivePresenterLaser'));assert(saved.includes('linked-presenter-laser-style'));
 const hiddenSaved=await p.evaluate(h=>{const doc=new DOMParser().parseFromString(h,'text/html');return doc.querySelector('#audience-laser-pointer').hidden},saved);assert(hiddenSaved);
 await point(.5,.5,'before close');await popup.close();await p.waitForFunction(()=>document.querySelector('#audience-laser-pointer').hidden,{},{timeout:12000});
 assert.deepEqual(errors,[]);fs.writeFileSync(dir+'/results.json',JSON.stringify({records,checks:['mouse hover only','normalized slide coordinates','leave hides both dots','audience resize','presenter resize','page change hides dot','stale slide packet ignored','fullscreen coordinates','editor retained','slide data and autosave revision unchanged','saved HTML excludes active pointer','presenter close hides pointer'],errors},null,2));console.log(JSON.stringify({checks:'passed',positions:records.length,errors},null,2));await browser.close();
})().catch(async e=>{console.error(e);if(browser)await browser.close();process.exit(1)});
