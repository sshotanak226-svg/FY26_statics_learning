const {chromium} = require('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('fs');
const path = require('path');
const {pathToFileURL} = require('url');
(async () => {
  const browser = await chromium.launch({headless:true, executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
  const page = await browser.newPage({viewport:{width:1720,height:1060}});
  const out = 'F:/Document/Fy26 TDH statics lean/tmp/proposition-qa';
  fs.mkdirSync(out,{recursive:true});
  const errors=[]; page.on('pageerror', e=>errors.push(e.message));
  const original = 'C:/Users/User/Downloads/９章　仮説検定と信頼区間_編集済み (14).html';
  await page.goto(pathToFileURL(original).href+'#16');
  await page.evaluate(()=>document.fonts.ready);
  await page.locator('#stage').screenshot({path:path.join(out,'original-ump-proof.png')});
  await page.goto(pathToFileURL('F:/Document/Fy26 TDH statics lean/output/９章_仮説検定と信頼区間_命題ページ追加.html').href);
  await page.evaluate(()=>document.fonts.ready);
  const report = await page.evaluate(() => ({count:deck.slides.length,mathErrors:mathErrors(),slides:deck.slides.map((s,i)=>({id:s.id,index:i,title:s.title}))}));
  const ids=['ump-proposition','wilks','normal-ump-proposition','ci-coverage-proposition'];
  report.layout=[];
  for (const id of ids) {
    const index=report.slides.find(s=>s.id===id).index;
    await page.evaluate(i=>go(i), index);
    await page.evaluate(()=>document.fonts.ready);
    await page.locator('#stage').screenshot({path:path.join(out,id+'.png')});
    report.layout.push(await page.evaluate(()=>{
      const slide=document.querySelector('#stage .slide');
      const content=slide.querySelector('.content');
      const text=slide.querySelector('.text-block');
      const foot=slide.querySelector('.foot');
      const rect=e=>{const r=e.getBoundingClientRect(); return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height};};
      const cr=rect(content),tr=rect(text),fr=rect(foot);
      return {id:slide.dataset.slideId,content:cr,text:tr,foot:fr,clipped:tr.bottom>fr.top,
        math:[...slide.querySelectorAll('.katex-display')].map(e=>({tex:e.querySelector('annotation')?.textContent,box:rect(e),natural:rect(e.querySelector('.katex-html')),overflow:e.scrollWidth>e.clientWidth+2})),
        errors:[...slide.querySelectorAll('.katex-error')].map(e=>e.textContent)};
    }));
  }
  report.runtimeErrors=errors;
  fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify({count:report.count,mathErrors:report.mathErrors,runtimeErrors:errors,layout:report.layout},null,2));
  await browser.close();
})().catch(e=>{console.error(e); process.exit(1)});
