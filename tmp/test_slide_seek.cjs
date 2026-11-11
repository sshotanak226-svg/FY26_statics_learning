const{chromium}=require('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const{pathToFileURL}=require('url');const fs=require('fs');const assert=require('assert/strict');
(async()=>{
 const b=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const c=await b.newContext({viewport:{width:1720,height:1060}}),p=await c.newPage(),errors=[];
 p.on('pageerror',e=>errors.push(e.message));
 const path='F:/Document/Fy26 TDH statics lean/output/９章_仮説検定と信頼区間_ページスライダー.html';
 const url=pathToFileURL(path).href,dir='tmp/slide-seek';fs.mkdirSync(dir,{recursive:true});
 await p.goto(url+'#33');await p.evaluate(()=>document.fonts.ready);
 const seek=p.locator('#slide-seek');
 const check=async(page,count=84)=>{
  assert.equal(await seek.inputValue(),String(page));assert.equal(await seek.getAttribute('max'),String(count));
  assert.equal(await p.evaluate(()=>current),page-1);
  assert.equal(await p.locator('#slide-seek-position').textContent(),`${page} / ${count}`);
  assert.equal(new URL(p.url()).hash,'#'+page);
 };
 await check(33);
 // Real keyboard events keep the native range's focus and change exactly one page.
 await seek.focus();await seek.press('ArrowRight');await check(34);await seek.press('ArrowLeft');await check(33);
 await seek.press('Home');await check(1);await seek.press('End');await check(84);
 const appendix=await p.evaluate(()=>deck.slides.findIndex(s=>s.appendix));
 assert(appendix>=0);await p.evaluate(i=>go(i),appendix);await check(appendix+1);
 assert((await seek.getAttribute('aria-valuetext')).includes('Appendix'));
 await seek.focus();await seek.press('End');await check(84);
 // Move the thumb continuously using real pointer events, without replacing the slider DOM.
 const rect=await seek.boundingBox();const xFor=page=>rect.x+10+(rect.width-20)*(page-1)/83;
 await p.mouse.move(xFor(84),rect.y+rect.height/2);await p.mouse.down();
 await p.mouse.move(xFor(33),rect.y+rect.height/2,{steps:16});await p.mouse.up();
 const dragged=Number(await seek.inputValue());assert(Math.abs(dragged-33)<=1);await check(dragged);
 await p.locator('#next').click();await check(dragged+1);await p.locator('#prev').click();await check(dragged);
 await p.evaluate(()=>location.hash='#17');await p.waitForFunction(()=>current===16);await check(17);
 // Presenter navigation must update the audience slider.
 const waitPopup=p.waitForEvent('popup');await p.locator('#presenter').click();const presenter=await waitPopup;
 presenter.on('pageerror',e=>errors.push(e.message));
 await presenter.locator('[data-command="next"]').click();await p.waitForFunction(()=>current===17);await check(18);
 await presenter.close();
 // Inserting and undoing a slide recalculates the range's page count.
 await p.locator('#editor').click();await p.locator('#duplicate-slide').click();
 await p.waitForFunction(()=>deck.slides.length===85);
 assert.equal(await seek.getAttribute('max'),'85');
 await p.locator('#undo-edit').click();await p.waitForFunction(()=>deck.slides.length===84);
 assert.equal(await seek.getAttribute('max'),'84');
 await p.locator('#edit-dialog [data-close]').click();
 await p.evaluate(()=>go(32));await check(33);
 // Saved HTML retains both the range and its bindings.
 const saved=await p.evaluate(()=>buildSavedHTML());assert(saved.includes('id="slide-seek"'));assert(saved.includes('function syncSlideSeek()'));
 assert.deepEqual(await p.evaluate(()=>mathErrors()),[]);
 await p.screenshot({path:dir+'/desktop.png'});
 for(const width of [1024,375]){
  await p.setViewportSize({width,height:800});await p.screenshot({path:dir+'/width-'+width+'.png'});
  const geometry=await p.evaluate(()=>{
   const v=document.querySelector('#viewport').getBoundingClientRect(),s=document.querySelector('#slide-seekbar').getBoundingClientRect(),r=document.querySelector('#slide-seek').getBoundingClientRect(),o=document.querySelector('#slide-seek-position').getBoundingClientRect();
   return {viewportBottom:v.bottom,seekTop:s.top,rangeLeft:r.left,rangeRight:r.right,outputRight:o.right,width:innerWidth};
  });
  assert(geometry.viewportBottom<=geometry.seekTop+1);assert(geometry.rangeLeft>=0&&geometry.rangeRight<=width&&geometry.outputRight<=width);
 }
 await p.emulateMedia({media:'print'});assert.equal(await p.locator('#slide-seekbar').isVisible(),false);
 assert.deepEqual(errors,[]);
 const report={all84Slides:true,keyboard:true,pointerDragging:true,buttonsAndHashSync:true,appendix:true,presenterSync:true,pageCountAfterEditing:true,savedHtmlRetainsSlider:true,responsive:true,hiddenWhenPrinting:true,mathErrors:[],errors};
 fs.writeFileSync(dir+'/checks.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));await b.close();
})().catch(e=>{console.error(e);process.exitCode=1;});
