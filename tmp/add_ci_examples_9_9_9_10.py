from pathlib import Path
import re,json,copy

src=Path('F:/Download/９章　仮説検定と信頼区間_編集済み (3).html')
dst=Path('output/９章_仮説検定と信頼区間_例9.9と9.10追加.html')
html=src.read_text(encoding='utf-8')
m=re.search(r'(<script id="deck-data" type="application/json">)(.*?)(</script>)',html,re.S)
old=json.loads(m[2]);deck=copy.deepcopy(old)
insertion=next(i for i,s in enumerate(deck['slides']) if s['id']=='paired-ci')
template=copy.deepcopy(deck['slides'][insertion])
def slide(id,title,takeaway,markdown,notes,original):
 s=copy.deepcopy(template)
 s.update(id=id,title=title,takeaway=takeaway,leftMarkdown=markdown,
          body=[p[2:] for p in markdown.split('\n\n') if p.startswith('- ')],
          notes=notes,original=original,rightHTML='',minutes=1.1)
 return s

normal=slide(
 'example-9-9-ci-summary',
 '9.6.2　例9.9：正規母平均の信頼区間',
 '正規標本では、母分散が既知でも未知でも、信頼係数1−αの厳密な区間が得られる。',
 r'''- 分析者は、独立な正規標本 $X_1,\ldots,X_n\sim N(\mu,\sigma^2)$ から、真の母平均 $\mu$ を推定する。標本平均 $\bar X$ と不偏分散 $V^2$ は、

$$
\bar X=\frac1n\sum_{i=1}^nX_i,\qquad V^2=\frac1{n-1}\sum_{i=1}^n(X_i-\bar X)^2.
$$

- 両側検定 $H_0:\mu=\mu_0$、$H_1:\mu\ne\mu_0$ が、有意水準 $\alpha$ で棄却しない帰無値 $\mu_0$ の区間は、

$$
\begin{aligned}
\sigma^2=\sigma_0^2\text{ が既知}:&\quad\left[\bar X-z_{\alpha/2}\frac{\sigma_0}{\sqrt n},\ \bar X+z_{\alpha/2}\frac{\sigma_0}{\sqrt n}\right],\\[4pt]
\sigma^2\text{ が未知}:&\quad\left[\bar X-t_{n-1,\alpha/2}\frac V{\sqrt n},\ \bar X+t_{n-1,\alpha/2}\frac V{\sqrt n}\right].
\end{aligned}
$$

- $z_{\alpha/2}$ と $t_{n-1,\alpha/2}$ は、それぞれ標準正規分布と自由度 $n-1$ のt分布の上側 $\alpha/2$ 点。''',
 '''出典：アップロード原資料の紙面145ページ（PDF22ページ）、例9.9（正規母集団）。
分析者は独立な正規標本から真の母平均μを区間推定する。nは標本数、barXは標本平均、V²は不偏分散、VはV²の非負の平方根である。αは分析者が観測前に定める有意水準であり、1−αは信頼係数である。
母分散がσ0²として既知の場合、H0:μ=μ0の下でZ=sqrt(n)(barX−μ0)/σ0は標準正規分布に厳密に従う。両側検定の棄却域は|Z|>zα/2、受容条件は|Z|≤zα/2である。分析者が受容条件をμ0について解くと、既知分散の欄に示す区間を得る。
母分散が未知の場合、H0の下でT=sqrt(n)(barX−μ0)/Vは自由度n−1のt分布に厳密に従う。正規標本では標本平均と不偏分散が独立で、(n−1)V²/σ²は自由度n−1のカイ二乗分布に従うためである。両側検定の棄却域は|T|>t(n−1,α/2)。分析者が受容条件をμ0について解くと、未知分散の欄に示す区間を得る。
各区間は真の母平均μを確率1−αで含む。母平均μは固定した未知の値であり、標本を取り直すと区間の端点が変動する。例9.9は正規モデルの下で有限標本でも成り立つ厳密な区間を扱う。
原資料には右片側検定から得る下側信頼区間も載る。既知分散の場合、その区間は[barX−zα σ0/sqrt(n),∞)。既存の「正規平均・既知分散」ページはこの片側区間を説明する。
''',
 'PDF22ページ（紙面145、例9.9）'
)

bernoulli=slide(
 'example-9-10-bernoulli-ci',
 '9.6.2　例9.10：ベルヌーイ母比率の信頼区間',
 '標本比率のワルド検定を反転すると、母比率の近似信頼区間が得られる。',
 r'''- 独立な標本 $X_1,\ldots,X_n\sim\operatorname{Ber}(\theta)$ では、$X_i=1$ が成功、$X_i=0$ が失敗を表す。分析者は、標本比率 $\bar X$ と推定標準誤差 $\widehat{\operatorname{SE}}(\bar X)$ から、真の成功確率 $\theta$ を区間推定する。

$$
\bar X=\frac1n\sum_{i=1}^nX_i,\qquad
\widehat{\operatorname{SE}}(\bar X)=\sqrt{\frac{\bar X(1-\bar X)}n}.
$$

- 有意水準 $\alpha$ の両側ワルド検定 $H_0:\theta=\theta_0$、$H_1:\theta\ne\theta_0$ は、次の受容条件を使う。分析者は、この条件を $\theta_0$ について解く。

$$
\left|\frac{\bar X-\theta_0}{\sqrt{\bar X(1-\bar X)/n}}\right|\le z_{\alpha/2}
\quad\Longleftrightarrow\quad
\theta_0\in\left[\bar X-z_{\alpha/2}\sqrt{\frac{\bar X(1-\bar X)}n},\ \bar X+z_{\alpha/2}\sqrt{\frac{\bar X(1-\bar X)}n}\right].
$$

- $z_{\alpha/2}$ は標準正規分布の上側 $\alpha/2$ 点。分析者は、大標本・$0<\bar X<1$ の下で、信頼係数 $1-\alpha$ の近似区間として上の区間を用いる。''',
 '''出典：アップロード原資料の紙面146ページ（PDF23ページ）、例9.10。
Xiは成功を1、失敗を0とする独立なベルヌーイ標本であり、θは各観測の真の成功確率である。nは標本数、barXは成功回数をnで割った標本比率である。分析者は母比率θを推定する。
標本比率の分散はθ(1−θ)/nである。分析者は未知のθをbarXで置き換え、推定標準誤差sqrt{barX(1−barX)/n}を得る。前章のFisher情報量I(θ)=1/{θ(1−θ)}による1/sqrt{nI(barX)}と同じ量である。
H0:θ=θ0対H1:θ≠θ0のワルド統計量はW=(barX−θ0)/sqrt{barX(1−barX)/n}。θ0が0と1の内側にあり、標本数が十分に大きい場合、H0の下でWの分布は標準正規分布で近似できる。有意水準αの近似棄却域は|W|>zα/2であり、受容条件は|W|≤zα/2である。
分析者が受容条件をθ0について解くと、barX−zα/2 sqrt{barX(1−barX)/n}≤θ0≤barX+zα/2 sqrt{barX(1−barX)/n}を得る。右辺の区間が原資料の例9.10にあるワルド型近似信頼区間である。信頼係数1−αは大標本による近似であり、有限標本で全てのθに対する被覆確率を厳密に保証する式ではない。
barXが0または1の場合は推定標準誤差が0になるため、スライドの割り算による受容条件は使えない。成功・失敗の回数が少ない場合やθが境界に近い場合、正規近似の精度が悪くなる。原資料どおりの未調整の区間は端点が[0,1]を超える場合もある。分析者が信頼集合を厳密に定義するときは、母数空間[0,1]との共通部分を考える。
''',
 'PDF23ページ（紙面146、例9.10）'
)

deck['slides'][insertion:insertion]=[normal,bernoulli]
assert len(deck['slides'])==len(old['slides'])+2
assert [s for s in deck['slides'] if s['id'] not in {normal['id'],bernoulli['id']}]==old['slides']
assert len({s['id'] for s in deck['slides']})==len(deck['slides'])
encoded=json.dumps(deck,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
out=html[:m.start(2)]+encoded+html[m.end(2):]
scoped_style='''<style id="ci-examples-9-9-9-10-layout">
.slide:is([data-slide-id="example-9-9-ci-summary"],[data-slide-id="example-9-10-bernoulli-ci"]) .content.full-width .text-block{padding-top:0;padding-bottom:0;}
.slide:is([data-slide-id="example-9-9-ci-summary"],[data-slide-id="example-9-10-bernoulli-ci"]) .markdown>.body-list{margin-bottom:8px;}
.slide:is([data-slide-id="example-9-9-ci-summary"],[data-slide-id="example-9-10-bernoulli-ci"]) .markdown p:has(.katex-display){margin:8px 0;}
.slide:is([data-slide-id="example-9-9-ci-summary"],[data-slide-id="example-9-10-bernoulli-ci"]) .katex-display>.katex>.katex-html{line-height:1.3;}
</style>'''
out=out.replace('</head>',scoped_style+'</head>',1)
dst.write_text(out,encoding='utf-8')
print(f'Added pages {insertion+1} and {insertion+2}; {len(old["slides"])} -> {len(deck["slides"])} slides; existing slides unchanged.')
