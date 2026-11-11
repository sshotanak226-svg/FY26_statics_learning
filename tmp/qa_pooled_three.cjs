const {chromium}=require('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url');
const fs=require('fs'),assert=require('assert/strict');
const file='F:/Document/Fy26 TDH statics lean/output/９章_仮説検定と信頼区間_等分散二標本3枚.html';
(async()=>{
 const b=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const p=await b.newPage({viewport:{width:1720,height:1060}}), errors=[];
 p.on('pageerror',e=>errors.push(e.message));
 await p.goto(pathToFileURL(file).href+'#27');await p.evaluate(()=>document.fonts.ready);
 assert.equal(await p.evaluate(()=>deck.slides.length),83);
 const checks=[];
 for(const number of [27,28,29,30]){
  await p.evaluate(i=>go(i-1),number);
  await p.locator('#stage').screenshot({path:`tmp/pooled-three-qa/slide${number}.png`});
  checks.push(await p.locator('#stage article').evaluate(el=>{
   const sr=el.getBoundingClientRect(),r=el.querySelector('.content').getBoundingClientRect(),scale=sr.width/1600;
   const bad=[];
   for(const target of el.querySelectorAll('.content .katex-display .katex-html,.content .markdown>ul,.content .markdown>p,.content .pooled-t-result>p,.content .pooled-t-result>h3,.content svg,.content .pooled-chart-note')){
    const b=target.getBoundingClientRect();
    if(b.left<sr.left-1||b.right>sr.right+1||b.bottom>sr.bottom-45*scale||b.top<r.top-2)bad.push({tag:target.tagName,cls:target.className,text:target.textContent.slice(0,70),x:(b.left-sr.left)/scale,y:(b.top-sr.top)/scale,w:b.width/scale,h:b.height/scale});
   }
   return {id:el.dataset.slideId,content:{top:(r.top-sr.top)/scale,height:r.height/scale},bad,mathErrors:[...el.querySelectorAll('.katex-error')].map(x=>x.textContent)};
  }));
 }
 await p.locator('#editor').click();
 assert(await p.locator('#selected-slide-count').isVisible());
 await p.locator('#edit-dialog [data-close]').click();
 assert.deepEqual(errors,[]);
 fs.writeFileSync('tmp/pooled-three-qa/geometry.json',JSON.stringify({checks,errors},null,2));
 console.log(JSON.stringify({checks,errors},null,2));
 await b.close();
})();
