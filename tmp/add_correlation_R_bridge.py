from pathlib import Path
import copy,json,re

src=Path('output/９章_仮説検定と信頼区間_相関t分布の説明簡略化.html')
dst=Path('output/９章_仮説検定と信頼区間_相関Rの途中式追加.html')
html=src.read_text(encoding='utf-8')
m=re.search(r'<script id="deck-data" type="application/json">(.*?)</script>',html,re.S)
old=json.loads(m[1]);deck=copy.deepcopy(old)
s=deck['slides'][48]
assert s['id']=='correlation-t-density-proof'
s['leftMarkdown']=r'''- **条件と記号**：標本 $(X_i,Y_i)$ は独立な二変量正規標本、$H_0:\rho=0$、$n>2$。$S_{XY},S_X^2,S_Y^2$ は分母を $n$ とする標本共分散・標本分散、$\sigma_Y$ は $Y$ の母標準偏差とする。

- **$Y$ の変動を分ける**：$Z$ は $X$ の変動方向に沿う成分、$U$ は残りの成分の二乗和を表す。

$$
Z=\frac{\sqrt n\,S_{XY}}{\sigma_Y S_X},\qquad
U=\frac{n}{\sigma_Y^2}\left(S_Y^2-\frac{S_{XY}^2}{S_X^2}\right)
\quad\Longrightarrow\quad Z^2+U=\frac{nS_Y^2}{\sigma_Y^2}.
$$

$$
R=\frac{S_{XY}}{S_X S_Y}
=\frac{\sqrt n\,S_{XY}/(\sigma_Y S_X)}{\sqrt{nS_Y^2/\sigma_Y^2}}
=\frac{Z}{\sqrt{Z^2+U}}.
$$

- **t分布との関係**：$H_0$ の下で $Z\sim N(0,1)$ と $U\sim\chi^2_{n-2}$ は独立。正規標本の直交分解では、平均と $X$ 方向の2成分を除くため、$U$ の自由度は $n-2$ となる。

$$
T=\frac{\sqrt{n-2}\,R}{\sqrt{1-R^2}}
=\frac{Z}{\sqrt{U/(n-2)}}\sim t_{n-2}.
$$'''
s['body']=[p[2:] for p in s['leftMarkdown'].split('\n\n') if p.startswith('- ')]
s['notes']+='\n今回追加した途中式では、S_X²=Σ(Xi−barX)²/n、S_Y²=Σ(Yi−barY)²/n、S_XY=Σ(Xi−barX)(Yi−barY)/nの規約を使う。Z=√n S_XY/(σY S_X)、U=n(S_Y²−S_XY²/S_X²)/σY²と定義すると、Z²+U=n S_Y²/σY²。Rの分子・分母に同じ正数√n/σYを掛ければ、R=Z/√(Z²+U)となる。Uは、中心化したYから中心化したXへの射影を取り除いた残差の平方和をσY²で割った量である。σYは未知でも、同じ倍率が分子・分母で消えるため、Rの計算にσYの値は不要である。\n'
assert len(deck['slides'])==len(old['slides'])
assert [i+1 for i,(a,b) in enumerate(zip(old['slides'],deck['slides'])) if a!=b]==[49]
payload=json.dumps(deck,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
out=html[:m.start(1)]+payload+html[m.end(1):]
out=out.replace('.slide[data-slide-id="correlation-t-density-proof"] .markdown p:has(.katex-display){margin:8px 0;}', '.slide[data-slide-id="correlation-t-density-proof"] .markdown p:has(.katex-display){margin:4px 0;}')
out=out.replace('</head>', '''<style>
.slide[data-slide-id="correlation-t-density-proof"] .content.full-width .markdown>.body-list>li{margin-bottom:12px;}
.slide[data-slide-id="correlation-t-density-proof"] .content.full-width .markdown>.body-list>li:last-child{margin-bottom:0;}
</style></head>''',1)
dst.write_text(out,encoding='utf-8')
print('Updated page 49 only; 87 slides retained.')
