from pathlib import Path
import copy,json,re

src=Path('output/９章_仮説検定と信頼区間_非正規標本の大標本近似追加.html')
dst=Path('output/９章_仮説検定と信頼区間_相関ZUの帰無分布導出.html')
html=src.read_text(encoding='utf-8')
m=re.search(r'<script id="deck-data" type="application/json">(.*?)</script>',html,re.S)
old=json.loads(m[1]);deck=copy.deepcopy(old)
s=deck['slides'][48]
assert s['id']=='correlation-t-density-proof'
s['leftMarkdown']=s['leftMarkdown'].replace(r'$\sigma_Y$ は $Y$ の母標準偏差とする。', r'$\mu_Y,\sigma_Y$ は $Y$ の母平均・母標準偏差とする。')
old_bullet=r'- **t分布との関係**：$H_0$ の下で $Z\sim N(0,1)$ と $U\sim\chi^2_{n-2}$ は独立。正規標本の直交分解では、平均と $X$ 方向の2成分を除くため、$U$ の自由度は $n-2$ となる。'
new_bullet=r'- **帰無仮説の役割**：$H_0$ は母相関 $\rho$ を0とし、$S_{XY}$ や $R$ を0には固定しない。二変量正規性より $X$ と $Y$ は独立となる。次頁で $Z,U$ の分布と独立性を導く。'
assert old_bullet in s['leftMarkdown']
s['leftMarkdown']=s['leftMarkdown'].replace(old_bullet,new_bullet)
s['body']=[p[2:] for p in s['leftMarkdown'].split('\n\n') if p.startswith('- ')]
s['notes']+='\n帰無仮説は母相関ρを0に固定するが、母平均μX,μY、母標準偏差σX,σYは未知のままでよい。標本共分散S_XYや標本相関Rは無作為標本に依存するため、帰無仮説の下でも一般には0ではない。二変量正規性があるので、ρ=0からXとYの独立性が従う。分布と独立性の導出は次の補足スライドで示す。\n'

p=copy.deepcopy(s)
p.update(id='correlation-null-ZU-derivation',title='9.7.1　ZとUの分布・独立性の導出',
    takeaway='帰無仮説と正規性により、Zと、Uを構成するn−2個の標準正規成分が独立になる。',
    sources=['pdf','normal-orthogonal-decomposition'],
    original='二変量正規標本の相関検定について、帰無仮説の作用、Zの線形結合、Uの直交分解を補足',minutes=1.2)
p['leftMarkdown']=r'''- **$H_0$ の作用**：二変量正規性と $\rho=0$ により、$Y_i$ の条件付き分布は $X$ の値によらなくなる。

$$
Y_i\mid\boldsymbol X\sim N(\mu_Y,\sigma_Y^2),\qquad
\varepsilon_i=\frac{Y_i-\mu_Y}{\sigma_Y},\qquad
\varepsilon_1,\ldots,\varepsilon_n\mid\boldsymbol X
\overset{\mathrm{iid}}\sim N(0,1).
$$

- **$Z$ の分布**：$X$ の観測値を固定すると、$a_i$ は定数、$\sum_i a_i=0$、$\sum_i a_i^2=1$ となる。正規変数の線形結合 $Z$ の平均は0、分散は1となる。

$$
a_i=\frac{X_i-\bar X}{\sqrt n\,S_X},\qquad
Z=\frac{\sqrt n\,S_{XY}}{\sigma_Y S_X}
=\sum_{i=1}^{n}a_i\varepsilon_i\sim N(0,1).
$$

- **$U$ の分布と独立性**：正規ベクトルを直交方向へ分けると、各成分は無相関なので独立となる。平均方向と $a$ 方向を除く $n-2$ 成分を $V_j\sim N(0,1)$ とすると、

$$
U=\frac{nS_Y^2}{\sigma_Y^2}-Z^2
=\sum_{j=1}^{n-2}V_j^2\sim\chi^2_{n-2},\qquad
Z\perp(V_1,\ldots,V_{n-2})\ \Longrightarrow\ Z\perp U.
$$'''
p['body']=[x[2:] for x in p['leftMarkdown'].split('\n\n') if x.startswith('- ')]
p['notes']=r'''条件：観測組(Xi,Yi)は独立同分布の非退化な二変量正規標本、n>2。母平均、母分散は既知でなくてよい。以下の標準化は分布を証明するための理論上の操作であり、分析者は母平均や母標準偏差を知る必要はない。
1. 帰無仮説の作用：一般の二変量正規分布では、Yi|Xi=xi ~ N(μY+ρσY(xi−μX)/σX, σY²(1−ρ²))。ρ=0を代入するとYi|Xi=xi ~ N(μY,σY²)となり、条件付き分布の平均も分散もxiに依存しなくなる。組間も独立なので、Xの全標本を固定してもεi=(Yi−μY)/σYは独立な標準正規変数となる。帰無仮説はμY=0やσY=1を仮定していない。平均0・分散1を持つのは標準化したεiである。S_XYとRは帰無仮説の下で一般には0でなく、これらの無作為なばらつきが検定の対象となる。
2. Zの変形：S_XY=Σ(Xi−barX)(Yi−barY)/n、S_X²=Σ(Xi−barX)²/n。したがって√n S_XY/(σY S_X)=Σai(Yi−barY)/σY。Σai=0なので、barYを母平均μYへ置き換えても和は変わらない。よってZ=Σaiεi。Xを固定するとaiは定数なので、Zは正規変数の線形結合。E[Z|X]=ΣaiE[εi|X]=0、Var(Z|X)=Σai²Var(εi|X)=1である。Xが一定の値しか取らない事象は、この非退化な正規モデルでは確率0である。
3. Uの意味：平均方向をe=(1,...,1)/√n、Xの中心化方向をa=(a1,...,an)と置くと、eとaは長さ1で互いに直交する。これらに加えて、直交する長さ1のベクトルb1,...,b(n−2)を選び、全体を正規直交基底にする。M=eᵀε=√n barε、Z=aᵀε、Vj=bjᵀεと置く。標準正規ベクトルの直交変換は平均0、共分散行列I_nの多変量正規ベクトルなので、M,Z,V1,...,V(n−2)はすべて独立な標準正規変数となる。特にCov(Z,Vj|X)=aᵀbj=0であり、同時正規性によって独立性が従う。これは「無相関なら常に独立」という主張ではなく、同時正規変数だから成立する。
4. 二乗和の分解：Σ εi²=M²+Z²+ΣVj²。平均方向を除くとΣ(εi−barε)²=Z²+ΣVj²。一方、Σ(εi−barε)²=Σ(Yi−barY)²/σY²=n S_Y²/σY²。従ってU=n S_Y²/σY²−Z²=ΣVj²。元の定義のU=n(S_Y²−S_XY²/S_X²)/σY²とも一致する。n−2個の独立な標準正規変数の二乗和が自由度n−2のカイ二乗分布を持つことから、U|X~χ²(n−2)。またZはV1,...,V(n−2)の全体と独立なので、その関数であるUとも独立となる。
5. 条件付き分布からの結論：Xを固定したときの(Z,U)の同時分布はN(0,1)とχ²(n−2)の積であり、固定したXの値に依存しない。そのため、Xを固定しない場合にも同じ積の同時分布を持ち、Z~N(0,1)、U~χ²(n−2)、ZとUの独立性が成立する。スライドのZとUの分布表示はこの結論を用いている。
6. 前頁との接続：R=Z/√(Z²+U)なので、1−R²=U/(Z²+U)。従ってT=√(n−2)R/√(1−R²)=Z/√{U/(n−2)}~t(n−2)。正規変数とカイ二乗変数の独立性がt分布のために必要であり、個別の周辺分布だけを確認しても十分ではない。
標本残差εi−barε−aiZそのものは互いに独立ではない。独立なのは、残りのn−2本の直交方向へ射影した座標Vjである。各方向の正規化（長さ1）を行っているため、Vjの分散が1になる。
参考：University of Washington, Yen-Chi Chen, STAT512 Lecture 8, Linear models and multivariate normal distributions：正規変数の線形変換と、同時正規変数の無相関と独立の同値性。
https://faculty.washington.edu/yenchic/20A_stat512/Lec8_Linear.html
参考：University of Cambridge, Qingyuan Zhao, IB Statistics (Lent Term 2025)：正規ベクトルの直交射影の独立性と、射影二乗和のカイ二乗分布。
https://www.statslab.cam.ac.uk/~qz280/teaching/statistics-2025/slides.pdf
本ページの記号a,ε,Vを使った導出は、上記の正規分布の性質を既存のZ,Uに適用した補足説明であり、アップロードされた教科書本文の引用ではない。
'''
deck['sources']['normal-orthogonal-decomposition']={
    'title':'University of Washington STAT512：正規変数の線形変換と独立性',
    'url':'https://faculty.washington.edu/yenchic/20A_stat512/Lec8_Linear.html',
    'detail':'正規変数の線形変換、共分散が0の同時正規変数の独立性。Cambridge IB Statisticsの直交射影の性質も発表者原稿に記載。'}
deck['slides'].insert(49,p)
assert len(deck['slides'])==len(old['slides'])+1
assert deck['slides'][:48]==old['slides'][:48]
assert deck['slides'][50:]==old['slides'][49:]
assert len(set(x['id'] for x in deck['slides']))==len(deck['slides'])
payload=json.dumps(deck,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
out=html[:m.start(1)]+payload+html[m.end(1):]
out=out.replace('</head>','''<style>
.slide[data-slide-id="correlation-null-ZU-derivation"] .content.full-width .text-block{padding-top:0;padding-bottom:0;}
.slide[data-slide-id="correlation-null-ZU-derivation"] .markdown>.body-list{margin:0 0 5px;}
.slide[data-slide-id="correlation-null-ZU-derivation"] .content.full-width .markdown>.body-list>li{margin-bottom:8px;}
.slide[data-slide-id="correlation-null-ZU-derivation"] .content.full-width .markdown>.body-list>li:last-child{margin-bottom:0;}
.slide[data-slide-id="correlation-null-ZU-derivation"] .markdown p:has(.katex-display){margin:4px 0;}
.slide[data-slide-id="correlation-null-ZU-derivation"] .katex-display>.katex>.katex-html{line-height:1.3;}
</style></head>''',1)
dst.write_text(out,encoding='utf-8')
audit=Path('tmp/audit_short_correlation_t.cjs').read_text(encoding='utf-8').replace('for(let i=48;i<50;i++)','for(let i=48;i<52;i++)')
Path('tmp/audit_correlation_null_ZU.cjs').write_text(audit,encoding='utf-8')
print('Updated page 49 and inserted derivation page 50. Original page 50 onward preserved; total 89 slides.')
