// Pointer state is transient UI state and never becomes part of the slide data.
let audienceLaserState=null;
function hideAudienceLaser(){
 audienceLaserState=null;
 const dot=$('audience-laser-pointer');if(dot)dot.hidden=true;
}
function positionAudienceLaser(){
 const dot=$('audience-laser-pointer'),s=audienceLaserState;
 if(!dot||!s)return;
 if(s.slideId!==deck.slides[current]?.id||document.querySelector('.overlay.open')){hideAudienceLaser();return;}
 const slide=$('stage')?.querySelector('.slide');if(!slide){hideAudienceLaser();return;}
 const rect=slide.getBoundingClientRect();
 dot.style.left=(rect.left+s.x*rect.width)+'px';
 dot.style.top=(rect.top+s.y*rect.height)+'px';dot.hidden=false;
}
function receivePresenterLaser(data){
 if(data.visible===false){hideAudienceLaser();return;}
 if(data.slideId!==deck.slides[current]?.id||data.visible!==true)return;
 if(!Number.isFinite(data.x)||!Number.isFinite(data.y)||data.x<0||data.x>1||data.y<0||data.y>1)return;
 audienceLaserState={slideId:data.slideId,x:data.x,y:data.y};positionAudienceLaser();
}
function bindPresenterLaser(){
 const host=$('present-preview');let slideId=null,frame=0,pending=null,showing=false;
 function post(data){if(window.opener&&!window.opener.closed)window.opener.postMessage({type:'deck-laser-pointer',...data},'*');}
 function clear(){
  if(frame){cancelAnimationFrame(frame);frame=0;}pending=null;
  const dot=$('presenter-laser-pointer');if(dot)dot.hidden=true;
  if(showing){showing=false;post({visible:false,slideId});}
 }
 function localDot(){
  let dot=$('presenter-laser-pointer');if(dot)return dot;
  dot=document.createElement('div');dot.id='presenter-laser-pointer';dot.className='linked-laser-pointer presenter-laser-dot';dot.hidden=true;dot.setAttribute('aria-hidden','true');host.append(dot);return dot;
 }
 host.addEventListener('pointermove',ev=>{
  if(!slideId)return;const slide=host.querySelector('.slide');if(!slide){clear();return;}
  const rect=slide.getBoundingClientRect();if(!rect.width||!rect.height){clear();return;}
  const x=(ev.clientX-rect.left)/rect.width,y=(ev.clientY-rect.top)/rect.height;
  if(x<0||x>1||y<0||y>1){clear();return;}
  const dot=localDot(),outer=host.getBoundingClientRect();
  dot.style.left=(ev.clientX-outer.left-host.clientLeft)+'px';dot.style.top=(ev.clientY-outer.top-host.clientTop)+'px';dot.hidden=false;
  showing=true;pending={visible:true,slideId,x,y};
  if(!frame)frame=requestAnimationFrame(()=>{frame=0;if(pending){const packet=pending;pending=null;post(packet);}});
 });
 host.addEventListener('pointerleave',clear);host.addEventListener('pointercancel',clear);
 host.addEventListener('pointerup',ev=>{if(ev.pointerType==='touch')clear();});
 window.addEventListener('blur',clear);window.addEventListener('pagehide',clear);window.addEventListener('resize',clear);
 document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='hidden')clear();});
 return{clear,setSlide(id){if(id!==slideId){clear();slideId=id;}}};
}
