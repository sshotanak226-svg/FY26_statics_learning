from pathlib import Path
import re,json

src=Path('F:/Download/９章　仮説検定と信頼区間_編集済み (8).html')
dst=Path('output/９章_仮説検定と信頼区間_発表者ポインタ連動.html')
html=src.read_text(encoding='utf-8')
data=re.search(r'<script id="deck-data" type="application/json">(.*?)</script>',html,re.S)[1]
assert 'id="audience-laser-pointer"' not in html
html=html.replace('</main>','</main><div id="audience-laser-pointer" class="linked-laser-pointer" aria-hidden="true" hidden></div>',1)
css=Path('tmp/presenter_laser_pointer.css').read_text(encoding='utf-8')
html=html.replace('</head>','<style id="linked-presenter-laser-style">'+css+'</style></head>',1)
em=re.search(r'<script id="slide-engine">(.*?)</script>',html,re.S);engine=em[1]
engine=engine.replace('function render(){\n','function render(){\n hideAudienceLaser();\n',1)
old="$('stage').style.transform=`translate(-50%, -50%) scale(${Math.max(.08,scale)})`;"
assert old in engine
engine=engine.replace(old,old+'positionAudienceLaser();',1)
engine=engine.replace('function openOverlay(id){','function openOverlay(id){hideAudienceLaser();',1)
engine=engine.replace('if(isPresenter||!presenterWindow||presenterWindow.closed)return;', 'if(isPresenter||!presenterWindow||presenterWindow.closed){if(!isPresenter)hideAudienceLaser();return;}',1)
engine=engine.replace("const notes=$('present-notes');","const laser=bindPresenterLaser();\n const notes=$('present-notes');",1)
engine=engine.replace("if(previewHTML!==d.html){$('present-preview').innerHTML=d.html;$('present-preview').style.pointerEvents='none';previewHTML=d.html;scale();}","laser.setSlide(d.slideId);\n  if(previewHTML!==d.html){laser.clear();$('present-preview').innerHTML=d.html;$('present-preview').style.pointerEvents='auto';previewHTML=d.html;scale();}",1)
old_message="if(ev.source!==presenterWindow)return;if(ev.data?.type==='presenter-ready')"
new_message="if(ev.source!==presenterWindow)return;if(ev.data?.type==='deck-laser-pointer'){receivePresenterLaser(ev.data);return;}if(ev.data?.type==='presenter-ready')"
assert old_message in engine
engine=engine.replace(old_message,new_message,1)
engine=engine.replace('\nnormalizeDeck(deck);','\n'+Path('tmp/presenter_laser_pointer.js').read_text(encoding='utf-8')+'\nnormalizeDeck(deck);',1)
html=html[:em.start(1)]+engine+html[em.end(1):]
html=html.replace('聴衆には元のスライドウィンドウを共有してください。','聴衆には元のスライドウィンドウを共有してください。左のスライド上でカーソルを動かすと、両画面の同じ位置に赤いポインタが表示されます。',1)
html=html.replace('発表原稿、次のスライド、予定時間、タイマーを表示します。','発表原稿、次のスライド、予定時間、タイマーを表示します。発表者画面のスライド上でカーソルを動かすと、聴衆用スライドにも赤いポインタが連動します。カーソルがスライドから離れるとポインタは消えます。',1)
assert re.search(r'<script id="deck-data" type="application/json">(.*?)</script>',html,re.S)[1]==data
dst.write_text(html,encoding='utf-8')
print('Added linked laser pointer; all '+str(len(json.loads(data)['slides']))+' slides and notes preserved.')
