const {chromium}=require('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs');const path=require('path');const {pathToFileURL}=require('url');
(async()=>{
const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
const page=await browser.newPage({viewport:{width:1600,height:1000},deviceScaleFactor:1});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
const file=path.resolve('output/html/1005tdh統計勉強会_連続確率分布と変数変換.html');
await page.goto(pathToFileURL(file).href);await page.evaluate(()=>document.fonts.ready);
const count=await page.evaluate(()=>deck.slides.length);
fs.mkdirSync('tmp/rendered',{recursive:true});let audit=[];
for(let i=0;i<count;i++){
await page.evaluate(i=>go(i),i);
await page.locator('#stage img').evaluateAll(imgs=>Promise.all(imgs.map(im=>im.decode().catch(()=>{}))));
const result=await page.evaluate(()=>{
 const a=document.querySelector('#stage .slide'),r=a.getBoundingClientRect(),scale=r.width/1600;
 const elements=[...a.querySelectorAll('h1,.takeaway,.text-block,.visual-block,.katex-html,.foot')];
 const bad=elements.map(e=>{const b=e.getBoundingClientRect();return {class:e.className,x:(b.x-r.x)/scale,y:(b.y-r.y)/scale,w:b.width/scale,h:b.height/scale};}).filter(b=>b.x<-1||b.y<-1||b.x+b.w>1601||b.y+b.h>901);
 const text=a.querySelector('.text-block'),visual=a.querySelector('.visual-block'),foot=a.querySelector('.foot');
 const overflow=[text,visual].filter(Boolean).filter(e=>e.scrollHeight>e.clientHeight+2||e.scrollWidth>e.clientWidth+2).map(e=>({class:e.className,scrollHeight:e.scrollHeight,height:e.clientHeight,scrollWidth:e.scrollWidth,width:e.clientWidth}));
 return {title:deck.slides[current].title,bad,overflow,mathErrors:a.querySelectorAll('.katex-error').length,unrendered:a.innerText.includes('$$'),footOverlap:!!(text&&foot&&text.getBoundingClientRect().bottom>foot.getBoundingClientRect().top+2)};
});
audit.push(result);await page.locator('#stage').screenshot({path:`tmp/rendered/slide-${String(i+1).padStart(2,'0')}.png`});
}
const maths=await page.evaluate(()=>mathErrors());
await page.evaluate(()=>go(1));const agenda=await page.locator('[data-agenda-go]').count();
await page.locator('[data-agenda-go]').first().click();const agendaTarget=await page.evaluate(()=>current);
await page.locator('#editor').click();const fields=await page.locator('#edit-form [name]').count();
await page.locator('[name="takeaway"]').fill('確認用の一時編集');
await page.locator('#undo-edit').click();const restored=await page.locator('[name="takeaway"]').inputValue();
await page.locator('#save-html').click();
fs.writeFileSync('tmp/html-audit.json',JSON.stringify({count,errors,maths,agenda,agendaTarget,fields,restored,audit},null,2));
console.log(JSON.stringify({count,errors,maths,agenda,agendaTarget,fields,issues:audit.filter(x=>x.bad.length||x.overflow.length||x.mathErrors||x.unrendered||x.footOverlap)},null,2));
await browser.close();
})();
