from pathlib import Path
from html import escape
import copy,json,re

src=Path('output/９章_仮説検定と信頼区間_区間推定概要改訂.html')
dst=Path('output/９章_仮説検定と信頼区間_区間推定と検定の関係.html')
html=src.read_text(encoding='utf-8')
m=re.search(r'(<script id="deck-data" type="application/json">)(.*?)(</script>)',html,re.S)
old=json.loads(m[2]);deck=copy.deepcopy(old);s=deck['slides'][37]
assert s['id']=='intro-9.6'
def eq(tex):return '<div class="detail-equation">$$'+escape(tex)+'$$</div>'
s['rightHTML']='<div class="example-detail">'+''.join([
 '<h3>検定を反転して区間を作る</h3>',
 r'<p>同じ観測値 $\boldsymbol x$ で、各候補 $\theta_0$ を帰無値とする<strong>有意水準 $\alpha$ の検定</strong>を行う。</p>',
 eq(r'H_0:\theta=\theta_0,\qquad H_1:\theta\ne\theta_0.'),
 '<p><strong>棄却されない候補を全て集める。</strong>その集合が区間になるとき、</p>',
 eq(r'\begin{gathered}\theta_0\in[L(\boldsymbol x),U(\boldsymbol x)]\\\Longleftrightarrow\quad H_0:\theta=\theta_0\text{ を棄却しない}.\end{gathered}'),
 r'<p>真の値が区間から外れるのは、<strong>正しい帰無仮説を棄却した場合</strong>。その確率が $\alpha$ 以下なので、含む確率は $1-\alpha$ 以上になる。</p>',
])+'</div>'
s['takeaway']='検定で棄却されない母数の候補を集めると、信頼区間が得られる。'
s['body']=[
 '真の母数を標本から作る区間で推定し、信頼係数で被覆確率を保証する。',
 '同じ観測値で各候補を帰無値として検定し、棄却されない候補を集める。',
 '真の値が区間から外れる確率は第一種誤りの確率に対応し、有意水準以下になる。',
]
s['notes']='''対応：アップロード原資料 PDF 21–25ページ（紙面144–148、9.6）。
区間推定の目的は、母平均や母比率などの真の未知の母数θを、標本Xから計算した下限L(X)と上限U(X)の間で推定すること。真の母数は固定で、区間の端点が標本により変動する。信頼係数1−αは、全ての真の母数の値で区間がその値を含む確率を少なくとも1−αとする保証水準。
右側は有意水準αの検定を反転する手順。同じ観測標本xを固定したまま、帰無値の候補θ0を動かす。各候補についてH0:θ=θ0対H1:θ≠θ0を検定する。全ての候補を帰無値として調べるという意味であり、異なる標本を候補ごとに取り直すわけではない。
各候補の検定で棄却されない値を全て集めると信頼集合C(x)が得られる。C(x)が区間になる場合、その下限と上限をL(x),U(x)とする。検定を反転しても常に一つの区間になるとは限らないため、スライドでも区間になる場合と明記した。
信頼係数の理由：真の値θがC(X)に入らない事象と、真の値を帰無値としたH0:θ=θを棄却する事象は同じ。各候補に対する検定が有意水準αを守れば、Pθ{θ∉C(X)}≤α。補事象を取るとPθ{θ∈C(X)}≥1−α。各候補の検定の第一種誤り確率がちょうどαなら、被覆確率もちょうど1−αになる。
ここでは全候補について新たに一括した第一種誤りを管理するのではなく、真の値θに対応する検定の誤り確率を用いて被覆確率を示している。棄却しない候補は真の値と証明された値ではなく、観測データからその有意水準では排除できない値。
9.6では信頼区間の定義、検定との対応、繰り返し標本を得るときの信頼係数の解釈を確認し、最尤推定量・母平均・比率の区間と必要な標本数へ進む。近似検定を反転した区間では、被覆確率の保証も近似的になる。
'''
assert len(deck['slides'])==len(old['slides'])
assert [i+1 for i,(a,b) in enumerate(zip(old['slides'],deck['slides'])) if a!=b]==[38]
encoded=json.dumps(deck,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
out=html[:m.start(2)]+encoded+html[m.end(2):]
dst.write_text(out,encoding='utf-8')
print('Updated only page 38. Removed normal example and expanded test inversion and coverage explanation.')
