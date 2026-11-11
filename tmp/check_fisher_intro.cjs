const {chromium}=require('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url');const assert=require('assert/strict');
(async()=>{
 const b=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const p=await b.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));
 await p.goto(pathToFileURL(process.argv[2]).href+'#48');await p.evaluate(()=>document.fonts.ready);
 assert.deepEqual(await p.evaluate(()=>({count:deck.slides.length,slider:Number(document.getElementById('slide-seek').max),id:deck.slides[current].id})),{count:84,slider:84,id:'fisher-z-introduction'});
 assert.deepEqual(await p.evaluate(()=>mathErrors()),[]);
 await p.evaluate(()=>go(48));
 assert.equal(await p.locator('#stage article').getAttribute('data-slide-id'),'fisher-z');
 const saved=await p.evaluate(()=>buildSavedHTML());
 const d=JSON.parse(saved.match(/<script id="deck-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
 assert.equal(d.slides.length,84);assert.equal(d.slides[47].id,'fisher-z-introduction');assert.equal(d.slides[48].id,'fisher-z');
 assert(d.slides[47].leftMarkdown.includes('1.099'));assert(d.slides[47].notes.length>100);
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({newPage:48,nextPageIsTest:true,slides:84,pageSliderSynced:true,savedHtmlRetainsNewPage:true,allLatexValid:true,errors}));
 await b.close();
})();
