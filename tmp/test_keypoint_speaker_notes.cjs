const{chromium}=require('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const{pathToFileURL}=require('url'),fs=require('fs'),assert=require('assert/strict');
const file='F:/Document/Fy26 TDH statics lean/output/９章_仮説検定と信頼区間_発表要点原稿.html';
const dir='F:/Document/Fy26 TDH statics lean/tmp/keypoint-notes-qa';fs.mkdirSync(dir,{recursive:true});let browser;
(async()=>{
 browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const c=await browser.newContext({viewport:{width:1720,height:1060}}),p=await c.newPage(),errors=[];p.setDefaultTimeout(12000);p.on('pageerror',e=>errors.push(e.message));
 await p.goto(pathToFileURL(file).href+'#1');await p.evaluate(()=>document.fonts.ready);
 const checks=await p.evaluate(()=>deck.slides.map((s,i)=>{const problems=[];for(const m of mathFragments(s.notes)){try{katex.renderToString(m.tex,{displayMode:m.display,throwOnError:true,strict:false,trust:false});}catch(e){problems.push(e.message)}}return{page:i+1,points:s.notes.split('\n').length,mathErrors:problems}}));
 assert(checks.every(x=>x.points>=3&&x.points<=5&&!x.mathErrors.length));
 const event=p.waitForEvent('popup');await p.locator('#presenter').click();const popup=await event;popup.setDefaultTimeout(12000);popup.on('pageerror',e=>errors.push(e.message));await popup.setViewportSize({width:1440,height:1000});await popup.waitForSelector('#present-notes');
 const reports=[];
 for(let i=0;i<88;i++){
  const title=await p.evaluate(i=>{go(i);return deck.slides[i].title},i);
  await popup.waitForFunction(title=>document.querySelector('#present-title')?.textContent===title,title,{timeout:12000});
  const report=await popup.locator('#present-notes').evaluate(el=>({points:el.querySelectorAll('li').length,mathErrors:el.querySelectorAll('.katex-error').length,overflow:el.scrollWidth>el.clientWidth+2,scrollHeight:el.scrollHeight,height:el.clientHeight}));
  assert.equal(report.points,checks[i].points,'page '+(i+1));assert.equal(report.mathErrors,0,'page '+(i+1));assert.equal(report.overflow,false,'page '+(i+1));reports.push({page:i+1,...report});
  assert.equal(await popup.locator('#present-notes ul').evaluate(el=>getComputedStyle(el).listStyleType),'disc');
  if([6,48,74].includes(i))await popup.screenshot({path:dir+'/presenter-'+String(i+1).padStart(2,'0')+'.png'});
 }
 await p.evaluate(()=>go(48));await popup.waitForFunction(()=>document.querySelector('#present-title').textContent.includes('相関の統計量'));
 await popup.locator('[data-command="edit-notes"]').click();await p.waitForFunction(()=>scriptWritingMode&&document.querySelector('#edit-dialog').classList.contains('open'));
 assert((await p.locator('#edit-script').inputValue()).startsWith('- '));await p.screenshot({path:dir+'/notes-editor.png'});
 const original=await p.evaluate(()=>structuredClone(deck.slides[editIndex]));await p.locator('#edit-script').fill(original.notes+'\n- 発表前の確認項目です。');await p.waitForFunction(()=>!autoSavePending&&autoSaveBrowserState==='saved');
 const after=await p.evaluate(()=>({...deck.slides[editIndex],notes:''}));assert.deepEqual(after,{...original,notes:''});
 await popup.waitForFunction(()=>document.querySelectorAll('#present-notes li').length===6);
 const saved=await p.evaluate(()=>JSON.parse(buildSavedHTML().match(/<script id="deck-data" type="application\/json">([\s\S]*?)<\/script>/)[1]));assert(saved.slides[48].notes.includes('発表前の確認項目です。'));assert.equal(saved.slides.length,88);
 assert.deepEqual(errors,[]);fs.writeFileSync(dir+'/results.json',JSON.stringify({slides:88,points:checks.reduce((n,x)=>n+x.points,0),reports,checks:['all notes use ordered-in-content bullet points','all notes math valid','presenter renders all 88 pages','no horizontal overflow','notes editor and presenter synchronized','notes-only edit preserved slide body','HTML export includes notes'],errors},null,2));console.log(JSON.stringify({slides:88,points:checks.reduce((n,x)=>n+x.points,0),checks:'passed',errors},null,2));await browser.close();
})().catch(async e=>{console.error(e);if(browser)await browser.close();process.exit(1)});
