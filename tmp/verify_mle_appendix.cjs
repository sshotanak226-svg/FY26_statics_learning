const {chromium} = require('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('fs'), path = require('path');
const {pathToFileURL} = require('url');
(async()=>{
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
  const page=await browser.newPage({viewport:{width:1720,height:1060}});
  const out='F:/Document/Fy26 TDH statics lean/tmp/appendix-qa';fs.mkdirSync(out,{recursive:true});
  const runtimeErrors=[];page.on('pageerror',e=>runtimeErrors.push(e.message));
  await page.goto(pathToFileURL('C:/Users/User/Downloads/９章　仮説検定と信頼区間_編集済み (18).html').href);
  await page.evaluate(()=>document.fonts.ready);
  const sourceTitleStyle=await page.evaluate(()=>{
    const s=document.querySelector('#stage .slide'),h=s.querySelector('h1');
    return {article:s.className,font:getComputedStyle(h).font,position: getComputedStyle(h).textAlign};
  });
  await page.locator('#stage').screenshot({path:path.join(out,'source-title.png')});
  await page.goto(pathToFileURL('F:/Document/Fy26 TDH statics lean/output/９章_仮説検定と信頼区間_Appendix追加.html').href);
  await page.evaluate(()=>document.fonts.ready);
  const report=await page.evaluate(()=>({count:deck.slides.length,mainCount:mainIndices().length,mathErrors:mathErrors(),pages:deck.slides.map((s,i)=>({id:s.id,index:i,title:s.title,appendix:s.appendix}))}));
  report.sourceTitleStyle=sourceTitleStyle;report.layout=[];
  for(const s of report.pages.filter(s=>s.appendix)){
    await page.evaluate(i=>go(i),s.index);await page.evaluate(()=>document.fonts.ready);
    await page.locator('#stage').screenshot({path:path.join(out,s.id+'.png')});
    report.layout.push(await page.evaluate(()=>{
      const slide=document.querySelector('#stage .slide'),content=slide.querySelector('.content'),foot=slide.querySelector('.foot');
      const r=e=>{const b=e.getBoundingClientRect();return {left:b.left,right:b.right,top:b.top,bottom:b.bottom,width:b.width,height:b.height}};
      const sr=r(slide),limit=foot?r(foot).top:sr.bottom;
      const items=content?[...content.querySelectorAll('p,li,.katex-display')]:[slide.querySelector('h1')];
      const clipping=items.map(e=>({text:e.textContent.slice(0,100),box:r(e)})).filter(e=>e.box.bottom>limit+1||e.box.right>sr.right+1||e.box.left<sr.left-1);
      const math=[...slide.querySelectorAll('.katex-display')].map(e=>({tex:e.querySelector('annotation')?.textContent,overflow:e.scrollWidth>e.clientWidth+2,box:r(e)}));
      const h=slide.querySelector('h1');
      return {title:h.textContent,id:slide.dataset.slideId,clipping,math,style:{article:slide.className,font:getComputedStyle(h).font,position:getComputedStyle(h).textAlign},counter:document.querySelector('#counter').textContent};
    }));
  }
  await page.evaluate(()=>go(52));
  const nextEnabled=await page.locator('#next').isEnabled();await page.locator('#next').click();
  const afterMain=await page.locator('#stage h1').textContent();await page.locator('#next').click();
  const afterCover=await page.locator('#stage h1').textContent();
  await page.locator('#prev').click();await page.locator('#prev').click();
  const backToMain=await page.evaluate(()=>current===52);
  await page.evaluate(()=>go(deck.slides.length-1));
  const nextDisabled=await page.locator('#next').isDisabled();
  await page.locator('#overview').click();
  const outline=await page.locator('#outline-body').innerText();
  report.navigation={nextEnabled,afterMain,afterCover,backToMain,nextDisabled,appendixInOutline:outline.includes('Appendix')};
  report.runtimeErrors=runtimeErrors;
  fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify({count:report.count,mainCount:report.mainCount,mathErrors:report.mathErrors,runtimeErrors,navigation:report.navigation,layout:report.layout.map(s=>({title:s.title,clipping:s.clipping,overflow:s.math.filter(m=>m.overflow).length,counter:s.counter}))},null,2));
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
