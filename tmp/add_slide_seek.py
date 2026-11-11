from pathlib import Path
import re,json

src=Path('output/９章_仮説検定と信頼区間_ワルド検出力比較.html')
out=Path('output/９章_仮説検定と信頼区間_ページスライダー.html')
html=src.read_text(encoding='utf-8')
original=html
data=json.loads(re.search(r'<script id="deck-data" type="application/json">(.*?)</script>',html,re.S)[1])
n=len(data['slides'])
old='<div class="progress" id="progress"></div>'
new=f'''<div class="slide-seekbar" id="slide-seekbar" aria-label="ページ移動">
<label for="slide-seek">全ページ</label>
<input type="range" id="slide-seek" min="1" max="{n}" step="1" value="1" aria-label="スライドのページ" aria-describedby="slide-seek-position">
<output id="slide-seek-position" for="slide-seek">1 / {n}</output>
</div>'''
assert html.count(old)==1
html=html.replace(old,new,1)
old=" $('progress').style.width=(s.appendix?100:(pos+1)/main.length*100)+'%';"
assert html.count(old)==1
html=html.replace(old,' syncSlideSeek();',1)
js='''function syncSlideSeek(){
 const slider=$('slide-seek');if(!slider)return;
 const total=deck.slides.length,page=Math.min(current+1,Math.max(1,total)),slide=deck.slides[current];
 slider.max=String(Math.max(1,total));slider.value=String(page);slider.disabled=total<2;
 slider.setAttribute('aria-valuetext',`${page} / ${total}、${slide?.appendix?'Appendix、':''}${slide?.title||''}`);
 slider.title=`${page} / ${total}　${slide?.title||''}`;
 slider.style.setProperty('--seek-percent',`${total>1?(page-1)/(total-1)*100:0}%`);
 $('slide-seek-position').textContent=`${page} / ${total}`;
}
'''
assert html.count('function resizeStage(){')==1
html=html.replace('function resizeStage(){',js+'function resizeStage(){',1)
init=" $('prev').onclick=()=>advance(-1);"
assert html.count(init)==1
html=html.replace(init," $('slide-seek').addEventListener('input',e=>go(Number(e.target.value)-1));\n"+init,1)
helptext='スライドは編集メニューのページ順に進みます。'
html=html.replace(helptext,'下のスライダーを動かすと、本編・Appendixを通して任意のページへ移動できます。'+helptext,1)
css='''<style id="slide-seekbar-style">
#viewport{bottom:108px;}
.slide-seekbar{position:fixed;left:0;right:0;bottom:66px;height:42px;display:flex;align-items:center;gap:14px;padding:0 20px;background:#102a36;color:#deecea;z-index:11;}
.slide-seekbar label{font-size:13px;white-space:nowrap;}
.slide-seekbar output{font-size:14px;min-width:66px;text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap;}
#slide-seek{appearance:none;-webkit-appearance:none;display:block;flex:1;min-width:0;width:100%;height:32px;margin:0;background:transparent;cursor:pointer;--seek-percent:0%;touch-action:pan-y;}
#slide-seek::-webkit-slider-runnable-track{height:6px;border-radius:4px;background:linear-gradient(to right,#62b1ff 0%,#62b1ff var(--seek-percent),#58717d var(--seek-percent),#58717d 100%);}
#slide-seek::-webkit-slider-thumb{appearance:none;-webkit-appearance:none;width:20px;height:20px;margin-top:-7px;background:#fff;border:3px solid #62b1ff;border-radius:50%;box-shadow:0 1px 4px #0007;}
#slide-seek::-moz-range-track{height:6px;background:#58717d;border-radius:4px;}
#slide-seek::-moz-range-progress{height:6px;background:#62b1ff;border-radius:4px;}
#slide-seek::-moz-range-thumb{width:14px;height:14px;background:#fff;border:3px solid #62b1ff;border-radius:50%;}
#slide-seek:focus-visible{outline:2px solid #b8dfff;outline-offset:2px;border-radius:4px;}
#slide-seek:disabled{opacity:.5;cursor:default;}
@media(max-width:600px){.slide-seekbar{gap:9px;padding:0 12px;}.slide-seekbar label{font-size:12px;}.slide-seekbar output{min-width:60px;}}
@media print{.slide-seekbar{display:none!important;}}
</style>'''
html=html.replace('</head>',css+'</head>',1)
assert re.search(r'<script id="deck-data" type="application/json">(.*?)</script>',html,re.S)[1]==re.search(r'<script id="deck-data" type="application/json">(.*?)</script>',original,re.S)[1]
out.write_text(html,encoding='utf-8')
print('Created bottom page slider for',n,'slides; all slide data unchanged.')
