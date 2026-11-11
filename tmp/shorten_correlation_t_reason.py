from pathlib import Path
import re,json,copy

src=Path('F:/Download/９章　仮説検定と信頼区間_編集済み (7).html')
dst=Path('output/９章_仮説検定と信頼区間_相関t分布の説明簡略化.html')
html=src.read_text(encoding='utf-8')
m=re.search(r'(<script id="deck-data" type="application/json">)(.*?)(</script>)',html,re.S)
old=json.loads(m[2]);deck=copy.deepcopy(old)
s=deck['slides'][48]
assert s['id']=='correlation-t-density-proof'
s['title']='9.7.1　相関の統計量がt分布になる理由'
s['takeaway']='母相関が0の正規標本では、Tは独立な正規変数とカイ二乗変数の比になる。'
s['leftMarkdown']=r'''- **条件**：$n$ 組の標本 $(X_i,Y_i)$ は互いに独立な二変量正規標本。帰無仮説は $H_0:\rho=0$、標本相関は $R$ とする（$n>2$）。

- **正規標本の性質**：母標準偏差で割った $Y$ の変動は、平均の方向、中心化した $X$ の方向、残りの方向に分かれる。$X$ 方向の成分 $Z$ と、残りの成分の二乗和 $U$ は独立になり、

$$
Z\sim N(0,1),\qquad U\sim\chi^2_{n-2},\qquad
R=\frac{Z}{\sqrt{Z^2+U}}.
$$

- **T統計量への書き換え**：分析者が上の $R$ を代入すると、t分布の基本形になる。

$$
T=\frac{\sqrt{n-2}\,R}{\sqrt{1-R^2}}
=\frac{Z}{\sqrt{U/(n-2)}}
\sim t_{n-2}.
$$

- **自由度が $n-2$ になる理由**：平均の1成分と $X$ 方向の1成分を除くため、残りの成分数は $n-2$。'''
s['body']=[p[2:] for p in s['leftMarkdown'].split('\n\n') if p.startswith('- ')]
s['rightHTML']=''
s['minutes']=0.8
s['original']='紙面149の式(9.17)について、独立な正規・カイ二乗変数の比による補足'
s['sources']=['pdf','review-t-f-distributions']
assert all(k in deck['sources'] for k in s['sources'])
s['notes']='''このページは、密度の変数変換・微分係数・正規化定数による導出を使わず、正規標本の直交分解とt分布の基本形で説明する。
条件：観測組(Xi,Yi),i=1,...,nは独立同分布の非退化な二変量正規標本、n>2。H0:ρ=0ではXとYは独立であり、Xの全観測値を固定しても、Yは共通の平均μYと分散σY²を持つ独立な正規標本である。
Yの標本ベクトルを、平均の方向（全成分が1/sqrt(n)の単位ベクトル）、中心化したXの方向、両者と直交する残りのn−2方向に分解する。中心化したXの方向の単位ベクトルはui=(Xi−barX)/sqrt{Σ(Xj−barX)²}。Xが定数になる確率は0なので、この方向は確率1で定まる。
Yの母標準偏差σYで割った各方向の成分は、平均方向を除き、独立な標準正規変数になる。X方向の成分をZ=Σui(Yi−barY)/σYとする。残りの成分をZ2,...,Z(n−1)とすると、U=Σj Zj²は自由度n−2のカイ二乗変数であり、ZとUは独立になる。残りの方向の正規成分が独立になる根拠は、正規ベクトルにおける直交する方向の共分散が0であり、同時正規分布では無相関が独立を意味するためである。
Yの中心化平方和はΣ(Yi−barY)²/σY²=Z²+U。一方、X方向への射影によりΣ(Xi−barX)(Yi−barY)/(σY sqrt{Σ(Xi−barX)²})=Zとなるため、標本相関R=Z/sqrt(Z²+U)が得られる。σYは理論上の標準化に使った未知の母標準偏差だが、Rの式と最終的なTの式から消えるため、分析者はσYを知る必要がない。
この分解は、Xの観測値を固定した条件付き分布で成立する。ZとUの条件付き同時分布はXの値に依存しないため、無条件でもZ~N(0,1)、U~χ²(n−2)、ZとUの独立性が成立する。
1−R²=U/(Z²+U)なので、sqrt(n−2)R/sqrt(1−R²)=Z/sqrt{U/(n−2)}。独立な標準正規変数と自由度n−2のカイ二乗変数から、この比を作った分布がt(n−2)分布である。これはρ=0の下で有限標本でも厳密に成立する。
残差の個々の成分Yi−barYが互いに独立という意味ではない。スライドの「方向の成分」は、直交する方向に分解した座標を指す。自由度n−2は、n方向から平均方向の1方向とX方向の1方向を除いた残りの方向数である。
教科書の対応：紙面149、式(9.17)。この分解の補足説明は教科書本文の引用ではない。t分布の基本形は冒頭の復習スライド、およびUniversity of Leicesterの講義資料PDF7ページと対応する。
https://www.le.ac.uk/users/dsgp1/COURSES/LEISTATS/STATSLIDE8.pdf
'''
assert len(deck['slides'])==len(old['slides'])
assert [i+1 for i,(a,b) in enumerate(zip(old['slides'],deck['slides'])) if a!=b]==[49]
encoded=json.dumps(deck,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
out=html[:m.start(2)]+encoded+html[m.end(2):]
dst.write_text(out,encoding='utf-8')
print('Shortened page 49 only; density-change calculations removed. All 87 slides retained.')
