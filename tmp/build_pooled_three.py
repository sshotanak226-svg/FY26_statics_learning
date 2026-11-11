import copy
import json
import math
import re
from pathlib import Path

SOURCE = Path(r'C:\Users\User\Downloads\９章　仮説検定と信頼区間_編集済み (22).html')
TARGET = Path(r'F:\Document\Fy26 TDH statics lean\output\９章_仮説検定と信頼区間_等分散二標本3枚.html')
html = SOURCE.read_text(encoding='utf-8')
pat = r'(<script[^>]*id="deck-data"[^>]*>)(.*?)(</script>)'
match = re.search(pat, html, re.S)
original = json.loads(match[2])
deck = copy.deepcopy(original)
assert deck['slides'][26]['id'] == 'pooled'
base = copy.deepcopy(deck['slides'][26])

def slide(id, title, takeaway, md, right='', notes=''):
    s = copy.deepcopy(base)
    s.update(id=id, title=title, takeaway=takeaway, leftMarkdown=md.strip(),
             rightHTML=right, notes=notes, minutes=1.3, equations=[], diagram='',
             table=[], flow=[], answers=[], figurePrompt='')
    s['body'] = [line[2:] for line in md.splitlines() if line.startswith('- ')]
    return s

# A data chart of the exact transformation, with a clearly labelled example.
N, nu, critical = 20, 18, 2.10092204024096
dcrit = N * math.log1p(critical**2/nu)
def tx(x): return 78 + (x + 4) * 70
def ty(y): return 415 - y * 22.5
def curve(a, b, count=100):
    return ' '.join(('M' if i == 0 else 'L') + f'{tx(x):.2f},{ty(N*math.log1p(x*x/nu)):.2f}'
                    for i in range(count+1) for x in [a+(b-a)*i/count])
blue, red, grey = '#1467b3', '#bd4532', '#52636b'
svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 560" role="img" aria-label="対数尤度比統計量DとTの関係。m=n=10、有意水準5パーセントの例。Dが4.386以上になるのはTの絶対値が2.101以上のとき。確率密度ではない。">']
def text(x,y,s,color=grey,anchor='start',size=27):
    svg.append(f'<text x="{x}" y="{y}" fill="{color}" text-anchor="{anchor}" font-size="{size}">{s}</text>')
text(78,35,'D = −2 log Λ',blue,size=30)
text(78,78,'m = n = 10、α = 5% の例',grey,size=26)
for a,b in [(-4,-critical),(critical,4)]:
    svg.append(f'<rect x="{tx(a):.2f}" y="100" width="{tx(b)-tx(a):.2f}" height="315" fill="#fae5df"/>')
for y in [0,4,8,12]:
    svg.append(f'<line x1="78" y1="{ty(y)}" x2="638" y2="{ty(y)}" stroke="#d8e2e9"/>')
    text(61,ty(y)+9,str(y),anchor='end',size=25)
svg.append(f'<path d="{curve(-4,4,180)}" fill="none" stroke="{blue}" stroke-width="4"/>')
svg.append(f'<line x1="78" y1="{ty(dcrit):.2f}" x2="638" y2="{ty(dcrit):.2f}" stroke="{red}" stroke-width="2.5" stroke-dasharray="8 6"/>')
text(357,ty(dcrit)-15,f'dα ≈ {dcrit:.3f}',red,anchor='middle',size=26)
for sign in [-1,1]:
    x=tx(sign*critical)
    svg.append(f'<line x1="{x}" y1="{ty(dcrit)}" x2="{x}" y2="415" stroke="{red}" stroke-width="2.5" stroke-dasharray="7 5"/>')
    svg.append(f'<circle cx="{x}" cy="{ty(dcrit)}" r="6" fill="{red}"/>')
    text(x,455,('−' if sign<0 else '')+'2.101',red,'middle',25)
for x in [-4,0,4]: text(tx(x),455,str(x),anchor='middle',size=25)
text(660,454,'T',blue,size=28)
text(140,134,'棄却',red,'middle',28)
text(575,134,'棄却',red,'middle',28)
text(357,501,'D > dα ⇔ |T| > 2.101',blue,'middle',28)
text(357,544,'曲線は統計量の変換式（確率密度ではない）',grey,'middle',23)
svg.append('</svg>')
chart = '<div class="pooled-log-chart">' + ''.join(svg) + '</div>'

md1 = r'''
- 独立な正規二標本。母分散は未知だが共通とし、母平均が等しいかを検定する。

$$
\begin{gathered}
X_i\overset{\mathrm{iid}}{\sim}N(\mu_X,\sigma^2),\quad
Y_j\overset{\mathrm{iid}}{\sim}N(\mu_Y,\sigma^2),\quad N=m+n,\\[4pt]
H_0:\mu_X=\mu_Y,\qquad H_1:\mu_X\ne\mu_Y.
\end{gathered}
$$

- 各群の平均を使う群内平方和を $U$、共通平均に制約した平方和を $U_0$ とする。

$$
\begin{aligned}
U&=\textstyle\sum_{i=1}^{m}(X_i-\bar X)^2+\sum_{j=1}^{n}(Y_j-\bar Y)^2,\\[4pt]
U_0&=U+\frac{mn}{N}(\bar X-\bar Y)^2.
\end{aligned}
$$

- 帰無仮説の制約で最大尤度が低下するほど、対数尤度比統計量 $D$ は大きくなる。

$$
\Lambda=\frac{\max_{H_0}L}{\max_{\Theta}L}
=\left(\frac{U}{U_0}\right)^{N/2},\qquad
D=-2\log\Lambda=N\log\frac{U_0}{U}.
$$
'''
notes1 = r'''独立な正規二標本、m,n>=2、σ²>0を仮定する。帰無・対立の両方で共通分散は未知。分母の最大化は帰無仮説を含む全母数空間Θ上で行う。
対数尤度は ℓ(μX,μY,σ²)=−N/2 log(2πσ²)−[Σ(Xi−μX)²+Σ(Yj−μY)²]/(2σ²)。
制約なしの最尤推定値はμX=barX、μY=barY、σhat²=U/N。H0下では共通平均μhat0=(m barX+n barY)/N、σtilde²=U0/N。
群内・群間の平方和分解より、U0=Σ(Xi−μhat0)²+Σ(Yj−μhat0)²=U+mn/N(barX−barY)²。
σ²を最適化した最大尤度は(2πS/N)^(-N/2) exp(−N/2)であり、比を取るとΛ=(U/U0)^(N/2)。D=N log(U0/U)。この計算は有限標本でも厳密。Uは最尤分散U/Nの分子であり、次頁の不偏分散はU/(N−2)である。
原資料：PDF 15–16ページ（9.4.1）。本スライドは同モデルの式を展開した説明。'''

md2 = r'''
- 式を変形できても、棄却点 $d_\alpha$ を決めるには $D$ の帰無分布が必要。

$$
P_{H_0}(D>d_\alpha)=\alpha.
$$

- 平均差を標準誤差で割ると、帰無分布が既知の $T$ を得る。

$$
\hat\sigma_U^2=\frac{U}{N-2},\qquad
T=\frac{\bar X-\bar Y}{\hat\sigma_U\sqrt{1/m+1/n}}.
$$

- $D$ は $T^2$ の増加関数なので、同じ棄却域になる。

$$
D=N\log\!\left(1+\frac{T^2}{N-2}\right).
$$
'''
right2 = chart + '<p class="pooled-chart-note">χ²₁は漸近分布。有限標本の正確な境界は、次頁のt分布から決める。</p>'
notes2 = f'''難しさは対数を取る代数計算そのものではなく、有意水準αを満たす有限標本の臨界値dαをDの帰無分布から直接求める点にある。
D=N log(1+mn(barX−barY)²/(N U))。Dは平均差だけでなく、標本ごとに変わる群内平方和Uにも依存する。Dは未知σ²に直接依存しないが、その有限標本分布は単純なχ²₁ではない。
不偏分散σhat_U²=U/(N−2)を用いるとT²=(N−2)mn(barX−barY)²/(N U)。これを代入するとD=N log(1+T²/(N−2))。
g(q)=N log(1+q/(N−2))はq>=0で厳密に単調増加。したがってD>dα iff |T|>sqrt((N−2)(exp(dα/N)−1))。統計量を置き換えても検定の判定は変わらない。
Tは平均差が推定標準誤差の何倍かを表すと同時に、未知の共通分散を含まない既知の帰無分布を持つ。Tがなぜ厳密なt分布に従うかは次頁で示す。
グラフは確率密度ではなくTをDへ写す変換曲線。説明用にm=n=10、N=20、ν=18、α=.05とし、上側.025点cα={critical:.12f}、dα=20 log(1+cα²/18)={dcrit:.12f}。薄赤の範囲は同じ検定の両側棄却域。正確な境界は次頁の結果を先取りして表示。
Wilksのχ²₁は漸近分布として利用できるが、この正規モデルではt分布による有限標本の厳密検定が可能。'''

md3 = r'''
- $H_0$ の下で、平均差を真の標準誤差で割ると標準正規分布に従う。

$$
Z=\frac{\bar X-\bar Y}{\sigma\sqrt{1/m+1/n}}
\sim N(0,1).
$$

- 正規標本の群内平方和はχ²分布に従い、独立な両群の自由度が足し合わされる。

$$
W=\frac{U}{\sigma^2}\sim\chi^2_{(m-1)+(n-1)}
=\chi^2_{N-2}.
$$

- 正規標本では標本平均と群内平方和が独立なので、$Z\perp W$ が成り立つ。
'''
right3 = r'''
<div class="pooled-t-result">
<h3>t分布の定義に一致</h3>
<p>$$
\begin{aligned}
T&=\frac{Z}{\sqrt{W/(N-2)}}\\[5pt]
&=\frac{\bar X-\bar Y}{\hat\sigma_U\sqrt{1/m+1/n}}
\sim t_{N-2}.
\end{aligned}
$$</p>
<h3>有意水準 α の両側棄却域</h3>
<p>$$c_\alpha=t_{N-2,\alpha/2},\qquad R=\{|T|>c_\alpha\}.$$</p>
<p>$c_\alpha$ は t 分布の上側 $\alpha/2$ 点。</p>
<p>$$
d_\alpha=N\log\!\left(1+\frac{c_\alpha^2}{N-2}\right)
$$</p>
<p>$$D>d_\alpha\quad\Longleftrightarrow\quad |T|>c_\alpha.$$</p>
</div>
'''
notes3 = r'''すべての分布と確率はH0が成立する場合のもの。母平均は共通μでよく、特定の既知値である必要はない。
独立な正規標本の平均差はN(0,σ²(1/m+1/n))なのでZ~N(0,1)。
UX=Σ(Xi−barX)²、UY=Σ(Yj−barY)²と置く。UX/σ²~χ²(m−1)、UY/σ²~χ²(n−1)。独立な二群の和なのでW=(UX+UY)/σ²~χ²(N−2)。
各群で標本平均と残差平方和は独立であり、群どうしも独立。ゆえに(barX,barY)と(UX,UY)が独立であり、ZとWも独立。
σhat_U²=U/(N−2)を代入すると、T=Z/sqrt(W/(N−2))。これは独立な標準正規変数とカイ二乗変数の比としてのt分布の定義に厳密に一致する。ここはWelchの近似とは異なり、独立性・正規性・共通母分散の仮定の下で有限標本でも厳密。
cα=t_(N−2,α/2)は上側α/2点、すなわちP(t_(N−2)>cα)=α/2。対称性によりP_H0(|T|>cα)=α。
D=g(T²)の単調性より、dα=N log(1+cα²/(N−2))に対し、D>dα iff |T|>cα。尤度比・対数尤度比・t統計量のどれを使ってもこの棄却域は同一。'''

new_slides = [
    slide('pooled', '9.4.1　等分散の二標本①：仮説と尤度比',
          '未知の共通分散の下で、平均を等しく制約したときの尤度の低下を調べる。', md1, notes=notes1),
    slide('pooled-loglr', '9.4.1　等分散の二標本②：対数尤度比とT',
          '対数尤度比をTの式に直すと、同じ棄却域をt分布で決められる。', md2, right2, notes2),
    slide('pooled-exact-t', '9.4.1　等分散の二標本③：t分布と棄却域',
          '平均差の正規性と群内平方和のχ²分布から、Tは厳密なt分布に従う。', md3, right3, notes3),
]
deck['slides'][26:27] = new_slides
assert len(deck['slides']) == len(original['slides'])+2
assert deck['slides'][:26] == original['slides'][:26]
assert deck['slides'][29:] == original['slides'][27:]
for key in deck:
    if key != 'slides': assert deck[key] == original[key]

data = json.dumps(deck, ensure_ascii=False, separators=(',', ':')).replace('</script', '<\\/script')
html = html[:match.start(2)] + data + html[match.end(2):]
css = '''
<style id="pooled-three-slide-style">
/* Only the three replacement slides use these layout rules. */
.slide:is([data-slide-id="pooled"],[data-slide-id="pooled-loglr"],[data-slide-id="pooled-exact-t"]) .content{align-items:center;}
.slide:is([data-slide-id="pooled"],[data-slide-id="pooled-loglr"],[data-slide-id="pooled-exact-t"]) .markdown>.body-list{margin:8px 0;}
.slide:is([data-slide-id="pooled"],[data-slide-id="pooled-loglr"],[data-slide-id="pooled-exact-t"]) .markdown>.body-list>li{margin-bottom:0;}
.slide:is([data-slide-id="pooled"],[data-slide-id="pooled-loglr"],[data-slide-id="pooled-exact-t"]) .markdown p{margin:10px 0;}
.slide:is([data-slide-id="pooled"],[data-slide-id="pooled-loglr"],[data-slide-id="pooled-exact-t"]) .katex-display{margin:12px 0;}
.slide[data-slide-id="pooled"] .markdown p{margin:6px 0;}
.slide[data-slide-id="pooled"] .katex-display{margin:8px 0;}
.slide[data-slide-id="pooled-loglr"] .content.has-diagram{grid-template-columns:1.12fr 1fr;gap:38px;}
.slide[data-slide-id="pooled-loglr"] .markdown{padding-right:0;}
.pooled-log-chart svg{display:block;width:100%;height:auto;overflow:visible;font-family:'Yu Gothic','Meiryo',sans-serif;}
.pooled-chart-note{margin:8px 0 0;line-height:1.45;color:#52636b;}
.slide[data-slide-id="pooled-exact-t"] .content.has-diagram{grid-template-columns:1fr 1.05fr;gap:45px;}
.pooled-t-result{border-left:2px solid #ccd9e5;padding-left:35px;}
.pooled-t-result h3{font-size:24pt;margin:12px 0;color:#1467b3;line-height:1.4;}
.pooled-t-result p{margin:12px 0;line-height:1.45;}
</style>
'''
html = html.replace('</head>', css+'</head>', 1)
TARGET.write_text(html, encoding='utf-8')
print(TARGET)
print(f'{len(original["slides"])} -> {len(deck["slides"])} slides; only original page 27 replaced with pages 27-29.')
print(f'Chart c_alpha={critical:.9f}; d_alpha={dcrit:.9f}')
