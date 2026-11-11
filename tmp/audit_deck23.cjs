const {chromium}=require('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url');const fs=require('fs');
const file=process.argv[2]||'C:/Users/User/Downloads/９章　仮説検定と信頼区間_編集済み (23).html';
const dir=process.argv[3]||'F:/Document/Fy26 TDH statics lean/tmp/deck23-before';fs.mkdirSync(dir,{recursive:true});
(async()=>{
 const b=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const p=await b.newPage({viewport:{width:1720,height:1060}}),errors=[];p.on('pageerror',e=>errors.push(e.message));
 await p.goto(pathToFileURL(file).href+'#1');await p.evaluate(()=>document.fonts.ready);
 const count=await p.evaluate(()=>deck.slides.length),report=[];
 for(let i=0;i<count;i++){
  await p.evaluate(i=>go(i),i);
  await p.locator('#stage').screenshot({path:dir+'/'+String(i+1).padStart(2,'0')+'.png'});
  const r=await p.locator('#stage article').evaluate(el=>{
   const slide=el.getBoundingClientRect(),content=el.querySelector('.content'),sr=content?.getBoundingClientRect(),scale=slide.width/1600,issues=[];
   if(sr){
    const check=(e,kind)=>{const r=e.getBoundingClientRect();if(!r.width||!r.height)return;
     const rect={x:Math.round((r.left-slide.left)/scale),y:Math.round((r.top-slide.top)/scale),w:Math.round(r.width/scale),h:Math.round(r.height/scale)};
     const outside=r.top<sr.top-2||r.bottom>sr.bottom+3||r.left<sr.left-3||r.right>sr.right+3;
     if(outside)issues.push({kind,text:e.textContent.slice(0,65),...rect});};
    for(const e of content.querySelectorAll('.text-block>*,.right-content>*,.katex-html>.base'))check(e,e.classList.contains('base')?'math':'block');
    for(const col of content.querySelectorAll('.text-block,.right-content')){
     const cr=col.getBoundingClientRect();for(const e of col.querySelectorAll('.katex-html>.base,table,svg,img')){
      if(e.localName==='svg'&&e.parentElement.closest('svg'))continue;
      const br=e.getBoundingClientRect();if(br.left<cr.left-3||br.right>cr.right+3)issues.push({kind:'column',text:e.textContent.slice(0,65),x:Math.round((br.left-slide.left)/scale),right:Math.round((br.right-slide.left)/scale)});
     }
    }
   }
   if(el.classList.contains('test-example')){
    const copy=el.querySelector('.content').cloneNode(true);copy.querySelectorAll('.katex').forEach(e=>e.remove());
    if(copy.textContent.includes('$')||copy.textContent.includes('\\begin{'))issues.push({kind:'unrendered-math',text:copy.textContent.slice(-300)});
   }
   return {id:el.dataset.slideId,issues,mathErrors:[...el.querySelectorAll('.katex-error')].map(e=>e.textContent)};
  });report.push({page:i+1,...r});
 }
 fs.writeFileSync(dir+'/audit.json',JSON.stringify({file,report,errors},null,2));
 console.log(JSON.stringify({count,issues:report.filter(x=>x.issues.length||x.mathErrors.length).map(x=>({page:x.page,id:x.id,issues:x.issues,mathErrors:x.mathErrors})),errors},null,2));await b.close();
})();
