const {chromium}=require('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const {pathToFileURL}=require('url');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const page=await browser.newPage({viewport:{width:1720,height:1060}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 const out='F:/Document/Fy26 TDH statics lean/tmp/example-9-5-qa';fs.mkdirSync(out,{recursive:true});
 await page.goto(pathToFileURL('C:/Users/User/Downloads/９章_仮説検定と信頼区間_Appendix多母数拡張.html').href+'#26');
 await page.evaluate(()=>document.fonts.ready);
 await page.locator('#stage').screenshot({path:path.join(out,'original-normal-t.png')});
 await page.goto(pathToFileURL('F:/Document/Fy26 TDH statics lean/output/９章_仮説検定と信頼区間_例9.5説明追加.html').href+'#26');
 await page.evaluate(()=>document.fonts.ready);
 const ids=['normal-t-lr-transform','normal-t-rejection-equivalence','normal-t-null-distribution','normal-t'];
 const report=await page.evaluate(()=>({count:deck.slides.length,mainCount:mainIndices().length,mathErrors:mathErrors(),autosave:typeof restoreAutomaticDraft==='function'}));
 report.layout=[];
 for(const id of ids){
  await page.evaluate(id=>go(deck.slides.findIndex(s=>s.id===id)),id);
  await page.evaluate(()=>document.fonts.ready);
  await page.locator('#stage').screenshot({path:path.join(out,id+'.png')});
  report.layout.push(await page.evaluate(()=>{
   const s=document.querySelector('#stage .slide'),foot=s.querySelector('.foot'),sr=s.getBoundingClientRect(),limit=foot.getBoundingClientRect().top;
   const r=e=>{const b=e.getBoundingClientRect();return {left:b.left,right:b.right,top:b.top,bottom:b.bottom}};
   const clipping=[...s.querySelectorAll('.content p,.content li,.content .katex-display')].map(e=>({text:e.textContent.slice(0,70),box:r(e)})).filter(e=>e.box.bottom>limit+1||e.box.right>sr.right+1||e.box.left<sr.left-1);
   return {id:s.dataset.slideId,clipping,overflow:[...s.querySelectorAll('.katex-display')].filter(e=>e.scrollWidth>e.clientWidth+2).length};
  }));
 }
 assert.equal(report.count,79);assert.equal(report.mainCount,56);assert.equal(report.autosave,true);
 assert.deepEqual(report.mathErrors,[]);assert.deepEqual(errors,[]);
 report.errors=errors;fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
