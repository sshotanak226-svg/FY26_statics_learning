const {chromium}=require('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const {pathToFileURL}=require('url');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const page=await browser.newPage({viewport:{width:1720,height:1060}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 const out='F:/Document/Fy26 TDH statics lean/tmp/multi-slide-qa';fs.mkdirSync(out,{recursive:true});
 await page.goto(pathToFileURL('F:/Document/Fy26 TDH statics lean/output/９章_仮説検定と信頼区間_複数選択移動.html').href+'#26');
 await page.evaluate(()=>document.fonts.ready);
 const baseline=await page.evaluate(()=>JSON.parse(JSON.stringify(deck))),order=baseline.slides.map(s=>s.id);
 assert.equal(order.length,79);assert.deepEqual(await page.evaluate(()=>mathErrors()),[]);
 await page.locator('#editor').click();
 const row=id=>page.locator('.edit-slide-row').filter({has:page.locator('input[data-select-slide='+JSON.stringify(id)+']')});
 const check=id=>row(id).locator('input');
 const clear=async()=>{if(await page.locator('#clear-slide-selection').isEnabled())await page.locator('#clear-slide-selection').click();};
 const actualOrder=()=>page.evaluate(()=>deck.slides.map(s=>s.id));
 const saved=()=>page.waitForFunction(()=>!autoSavePending&&autoSaveBrowserState==='saved');

 await check(order[2]).check();await check(order[6]).click({modifiers:['Shift']});
 assert.deepEqual(await page.evaluate(()=>selectedIdsInOrder()),order.slice(2,7));
 await clear();
 await check(order[2]).check();await check(order[5]).check();await check(order[9]).check();
 assert.equal(await page.locator('#selected-slide-count').textContent(),'3枚選択中');
 const editId=await page.evaluate(()=>deck.slides[editIndex].id),shownId=await page.evaluate(()=>deck.slides[current].id);
 await page.locator('#move-target').selectOption('before:'+order[20]);
 await page.locator('#move-selected-slides').click();
 const selected=[order[2],order[5],order[9]],remaining=order.filter(id=>!selected.includes(id)),at=remaining.indexOf(order[20]);
 const expected=[...remaining.slice(0,at),...selected,...remaining.slice(at)];
 assert.deepEqual(await actualOrder(),expected);
 assert.equal(await page.evaluate(()=>deck.slides[editIndex].id),editId);
 assert.equal(await page.evaluate(()=>deck.slides[current].id),shownId);
 assert.equal(await page.locator('#edit-form [name="title"]').inputValue(),baseline.slides.find(s=>s.id===editId).title);
 await page.screenshot({path:path.join(out,'selected-moved.png')});
 await page.locator('#undo-edit').click();assert.deepEqual(await actualOrder(),order);
 assert.equal(await page.evaluate(()=>deck.slides[editIndex].id),editId);
 await clear();await check(order[2]).check();await check(order[4]).check();
 await page.locator('#move-up').click();
 const stepped=[...order];for(let i=1;i<stepped.length;i++)if([order[2],order[4]].includes(stepped[i])&&![order[2],order[4]].includes(stepped[i-1]))[stepped[i-1],stepped[i]]=[stepped[i],stepped[i-1]];
 assert.deepEqual(await actualOrder(),stepped);
 await page.locator('#move-down').click();assert.deepEqual(await actualOrder(),order);

 // Real native drag/drop: move two separated checked pages before page 9.
 await clear();await check(order[2]).check();await check(order[4]).check();
 await row(order[2]).scrollIntoViewIfNeeded();
 await row(order[8]).scrollIntoViewIfNeeded();
 const from=await row(order[2]).locator('.slide-grip').boundingBox();
 assert(from);
 await page.mouse.move(from.x+from.width/2,from.y+from.height/2);await page.mouse.down();
 await page.mouse.move(from.x+from.width/2+12,from.y+from.height/2+12,{steps:5});
 // Dragging can scroll the sidebar, so target its current visible position.
 for(let attempt=0;attempt<3;attempt++){
  const to=await row(order[8]).boundingBox();assert(to);
  await page.mouse.move(to.x+60,to.y+3,{steps:12});
  await page.evaluate(()=>new Promise(requestAnimationFrame));
  if(await page.evaluate(()=>slideBoundaryAt(slideDragY)===8))break;
 }
 await page.waitForFunction(()=>dragSlideIds.length===2&&!document.getElementById('slide-drop-marker').hidden);
 await page.screenshot({path:path.join(out,'drag-target.png')});
 const boundary=await page.evaluate(()=>slideBoundaryAt(slideDragY));
 assert.equal(boundary,8);
 await page.mouse.up();
 const dragRemaining=order.filter(id=>![order[2],order[4]].includes(id)),dragAt=dragRemaining.indexOf(order[8]);
 const dragExpected=[...dragRemaining.slice(0,dragAt),order[2],order[4],...dragRemaining.slice(dragAt)];
 assert.deepEqual(await actualOrder(),dragExpected);
 assert.equal(await page.evaluate(()=>dragSlideIds.length),0);
 await saved();await page.reload();assert.deepEqual(await actualOrder(),dragExpected);
 await page.locator('#editor').click();
 // Stored slide records must retain every title, formula, and asset.
 const after=await page.evaluate(()=>JSON.parse(JSON.stringify(deck.slides)));
 for(const slide of baseline.slides)assert.deepEqual(after.find(s=>s.id===slide.id),slide);

 // Dragging near an edge scrolls a long list; cancelling must not reorder.
 await row(dragExpected[0]).scrollIntoViewIfNeeded();
 const source=await row(dragExpected[0]).locator('.slide-grip').boundingBox();
 const nav=await page.locator('#edit-nav').boundingBox();
 await page.mouse.move(source.x+10,source.y+10);await page.mouse.down();
 await page.mouse.move(source.x+22,source.y+22,{steps:5});
 await page.mouse.move(nav.x+80,nav.y+nav.height-12,{steps:12});
 await page.waitForFunction(()=>document.getElementById('edit-nav').scrollTop>800);
 await page.mouse.move(nav.x+nav.width+50,nav.y+100,{steps:5});await page.mouse.up();
 assert.deepEqual(await actualOrder(),dragExpected);
 await clear();
 await page.locator('#select-all-slides').click();assert.equal(await page.evaluate(()=>selectedSlideIds.size),79);
 assert(await page.locator('#move-up').isDisabled());assert(await page.locator('#move-down').isDisabled());
 await clear();assert.equal(await page.evaluate(()=>selectedSlideIds.size),0);

 // Moving across the Appendix boundary must also change playback order.
 const appendixId=baseline.slides.find(s=>s.id==='appendix-title').id;
 await check(appendixId).check();await page.locator('#move-target').selectOption('start');await page.locator('#move-selected-slides').click();
 assert.equal((await actualOrder())[0],appendixId);
 await page.locator('#edit-dialog [data-close]').click();
 await page.evaluate(()=>go(0));assert(await page.locator('#prev').isDisabled());
 await page.locator('#next').click();assert.equal(await page.evaluate(()=>current),1);
 await page.evaluate(()=>go(deck.slides.length-1));assert(await page.locator('#next').isDisabled());
 await page.locator('#editor').click();await page.locator('#undo-edit').click();
 assert.deepEqual(await actualOrder(),dragExpected);
 await clear();
 await page.evaluate(()=>{go(deck.slides.findIndex(s=>s.id==='normal-t'));});
 await page.locator('#edit-dialog [data-close]').click();await page.locator('#editor').click();
 await page.screenshot({path:path.join(out,'editor-ready.png')});
 assert.deepEqual(errors,[]);assert.deepEqual(await page.evaluate(()=>mathErrors()),[]);
 const report={rangeSelection:true,nonContiguousBulkMove:true,relativeOrderPreserved:true,activeEditorPreserved:true,undo:true,stepMove:true,nativeDragDrop:true,insertionIndicator:true,autoScroll:true,cancelledDragDoesNotMove:true,autosaveRestore:true,allSelect:true,appendixPlaybackOrder:true,allSlideDataPreserved:true,runtimeErrors:errors};
 fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
