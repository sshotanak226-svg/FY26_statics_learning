from pathlib import Path
from html import escape
import json,re,copy

src=Path('F:/Download')/'９章　仮説検定と信頼区間_編集済み (1).html'
out=Path('F:/Document/Fy26 TDH statics lean/output/９章_仮説検定と信頼区間_ワルド概要改訂.html')
html=src.read_text(encoding='utf-8')
m=re.search(r'(<script id="deck-data" type="application/json">)(.*?)(</script>)',html,re.S)
original=json.loads(m[2]);deck=copy.deepcopy(original)
index=next(i for i,s in enumerate(deck['slides']) if s['id']=='intro-9.5')
s=deck['slides'][index]
s['takeaway']='ワルド型検定は、推定値と帰無値の差が「標準誤差の何倍か」で判断する。'
s['leftMarkdown']=r'''- **仮説検定**：母数 $\theta$ の推定値 $\hat\theta$ と、帰無値 $\theta_0$ の隔たりを調べる。

$$
H_0:\theta=\theta_0,\qquad H_1:\theta\ne\theta_0.
$$

- **計算する統計量**：差を、推定値のばらつき（推定標準誤差）で割る。

$$
W=\frac{\hat\theta-\theta_0}{\widehat{\operatorname{SE}}(\hat\theta)}.
$$

$|W|=2$ なら、帰無値から標準誤差2個分の隔たり。

- **棄却域の計算**：適切な条件と大標本の下で、$H_0$ 時のWを標準正規で近似する（5%両側の例）。

$$
W\xrightarrow[H_0]{d}N(0,1),\qquad
\mathcal R_{5\%}=\{|W|>1.96\}.
$$'''
s['body']=[line[2:] for line in s['leftMarkdown'].splitlines() if line.startswith('- ')]
s['rightHTML']='''<div class="example-detail wald-overview-detail">
<h3>尤度比検定との違い</h3>
<p><strong>尤度比</strong>：帰無仮説を課したとき、自由な推定から最大尤度がどれだけ下がるかを見る。</p>
<p><strong>ワルド</strong>：制約なしの推定値と標準誤差を使う。帰無制約での尤度最大化は不要。</p>
<table><thead><tr><th>9.5章の対象</th><th>標準誤差の求め方</th></tr></thead><tbody>
<tr><td>最尤推定量</td><td>情報量から</td></tr>
<tr><td>母比率（例9.6）</td><td>標本比率から</td></tr>
<tr><td>母平均</td><td>標本数とばらつきから</td></tr>
<tr><td>夫婦の支持率差</td><td>各夫婦の回答差から</td></tr>
</tbody></table><p>情報量は、対数尤度の曲がり方を表す。</p></div>'''
s['notes']='''9.5章の共通する考え方は、推定値と帰無値の隔たりを、推定値自身の標準誤差で標準化して判断すること。
θは検定したい母数、θ0は検定前に指定する帰無値、θhatは標本から得た推定値。H0そのものに確率分布があるという意味ではなく、H0が成り立つときの統計量Wの標本分布を考える。
標準誤差は個々の観測値のばらつきではない。標本を取り直すと推定値も変わるが、その推定値のばらつきが標準誤差。通常は未知なので標本から推定する。SEhat(θhat)はその推定値。
Wは、帰無値との差が推定標準誤差の何倍かを表す。|W|=2なら標準誤差2個分の隔たり。同じ差でも標準誤差が小さければ、偶然の推定誤差として説明しにくい。差の大きさだけで判断せず、推定の精密さも組み込む。
尤度比検定では、帰無仮説の制約のある母数集合と制約のない全体集合で尤度を最大化し、その最大値を比べる。比較の対象はモデルの当てはまり。ワルド型検定では、制約なしで得た推定値とその標準誤差を使い、帰無値との距離を測る。帰無制約下の最大尤度を別に求める必要はない。
これは判定材料と計算の違いであって、尤度比検定が常に厳密でワルド型だけが近似、という区別ではない。正則条件の下では、対応する尤度比検定とワルド検定は大標本で漸近的に同等になるが、有限標本の結果は一致するとは限らない。
このスライドの正規近似には、用いる推定量の漸近正規性と、標準誤差の適切な推定などの条件が必要。一般の母平均や組内の差には中心極限定理を使い、独立性や有限の正の分散などを仮定する。5%両側の例では、標準正規分布の上下の裾に2.5%ずつ配分し、|W|が約1.96を超えたら棄却する。一般には|W|>z_(α/2)。有限標本で厳密に有意水準5%を保証するという意味ではない。
9.5.1では最尤推定量の漸近正規性を使う。1観測あたりのFisher情報量をI(θ)とすると、推定標準誤差は1/sqrt(n I(θhat))。情報量は尤度の曲率、すなわち推定値付近で尤度がどの程度鋭く集中しているかに対応する。
例9.6ではベルヌーイ母数、すなわち母比率を扱う。推定値は標本比率barX、推定標準誤差はsqrt(barX(1−barX)/n)。0<barX<1と十分な標本数が必要。
9.5.2では最尤推定量に限らず、中心極限定理に基づいて母平均を検定する。標本平均barXの標準誤差をS/sqrt(n)で推定し、(barX−μ0)/(S/sqrt(n))を使う。
例9.7では夫婦の支持率差を扱う。各夫婦について夫の回答Xiと妻の回答Yi（支持1、非支持0）の差Zi=Xi−Yiを作り、夫婦間の組は独立とする。その差の平均とばらつきを使うことで、夫婦内の関連を反映する。夫婦を独立な二群と扱わない。
提供資料の対応：PDF19–21ページ、紙面142–144ページ。上記の比較と直感的説明は同章の統計量を整理した補足。'''
s['minutes']=1.5
s['testExample']=True
assert len(deck['slides'])==len(original['slides'])==84
for i,(a,b) in enumerate(zip(original['slides'],deck['slides'])):
    if i!=index:assert a==b
assert original['assets']==deck['assets']
encoded=json.dumps(deck,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
html=html[:m.start(2)]+encoded+html[m.end(2):]
css='''<style id="wald-overview-revision-style">
.slide[data-slide-id="intro-9.5"] .content.has-diagram{grid-template-columns:minmax(0,1.08fr) minmax(0,1fr);gap:36px;}
.slide[data-slide-id="intro-9.5"] .markdown p{margin:4px 0 10px;}
.slide[data-slide-id="intro-9.5"] .markdown>.body-list{margin:0 0 10px;}
.slide[data-slide-id="intro-9.5"] .markdown .katex-display{margin:8px 0;}
.slide[data-slide-id="intro-9.5"] .example-detail{padding-left:24px;}
.slide[data-slide-id="intro-9.5"] .example-detail h3{margin:12px 0 10px;}
.slide[data-slide-id="intro-9.5"] .example-detail h3:first-child{margin-top:0;}
.slide[data-slide-id="intro-9.5"] .example-detail p{margin:8px 0;}
.slide[data-slide-id="intro-9.5"] .example-detail table{margin-top:8px;width:100%;table-layout:fixed;}
.slide[data-slide-id="intro-9.5"] .example-detail th,.slide[data-slide-id="intro-9.5"] .example-detail td{padding:9px 10px;line-height:1.35;}
.slide[data-slide-id="intro-9.5"] .example-detail th:first-child{width:43%;}
</style>'''
html=html.replace('</head>',css+'</head>',1)
out.write_text(html,encoding='utf-8')
print('Revised overview page',index+1,'; total',len(deck['slides']),'; other slides unchanged.')
