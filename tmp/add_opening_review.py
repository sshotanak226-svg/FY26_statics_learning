from pathlib import Path
from html import escape
import re,json,copy

src=Path('output/９章_仮説検定と信頼区間_標本相関の分布とt検定.html')
dst=Path('output/９章_仮説検定と信頼区間_冒頭復習2枚追加.html')
html=src.read_text(encoding='utf-8')
m=re.search(r'(<script id="deck-data" type="application/json">)(.*?)(</script>)',html,re.S)
old=json.loads(m[2]);deck=copy.deepcopy(old)
template=copy.deepcopy(next(s for s in deck['slides'] if s['id']=='correlation-definition'))
def eq(t):return '<div class="detail-equation">$$'+escape(t)+'$$</div>'
def make(id,title,takeaway,left,right,notes,sources):
 s=copy.deepcopy(template)
 s.update(id=id,title=title,takeaway=takeaway,leftMarkdown=left,rightHTML=right,
          section='復習',majorSection='復習',subsection='過去の復習',minutes=1,
          original='本章を読むための基礎事項の復習',notes=notes,sources=sources)
 s.pop('role',None);s.pop('testExample',None)
 s['body']=[p[2:] for p in left.split('\n\n') if p.startswith('- ')]
 return s

tf=make(
 'opening-review-t-f','復習①　T統計量とF統計量',
 'T統計量は差を標準誤差で評価し、F統計量は二つの分散成分の比を評価する。',
 r'''- **T統計量**は、推定値 $\hat\theta$ と帰無値 $\theta_0$ の差を、推定標準誤差で割って評価する。

$$
T=\frac{\hat\theta-\theta_0}{\widehat{\operatorname{SE}}(\hat\theta)}.
$$

- 推定標準誤差は、推定値の標準偏差を標本から推定した値。

- **t分布になる条件**：帰無仮説の下で $Z\sim N(0,1)$ と $U\sim\chi^2_\nu$ が独立で、次の形に書ける場合（$\nu$ は自由度）。

$$
T=\frac{Z}{\sqrt{U/\nu}}\sim t_\nu.
$$''',
 '<div class="opening-review-detail">'+''.join([
  '<h3>F統計量：二つの分散成分の比</h3>',
  '<p>F統計量は、二つの分散成分の比から、ばらつきの違いを評価する。</p>',
  r'<p>帰無仮説の下で、$U_1$ と $U_2$ が独立で、</p>',
  eq(r'U_1\sim\chi^2_{\nu_1},\qquad U_2\sim\chi^2_{\nu_2},'),
  eq(r'F=\frac{U_1/\nu_1}{U_2/\nu_2}\sim F_{\nu_1,\nu_2}.'),
  r'<p>$\nu_1$ は分子の自由度、$\nu_2$ は分母の自由度。分析者は、F統計量を分散の比較や分散分析に使う。</p>',
 ])+'</div>',
 '''このページは本章に先立つ基礎事項の復習である。
T統計量は、推定値と帰無値の差を、標本から推定した標準誤差で割り、差の大きさを標準誤差を単位として表す。推定標準誤差は各データの標準偏差ではなく、推定量が標本の取り方で変動する標準偏差の推定値である。
この形式の統計量が常にt分布になるわけではない。帰無仮説の下で、標準正規変数Zと、Zから独立な自由度νのカイ二乗変数Uを用いてT=Z/sqrt(U/ν)と書けることが、表示した厳密なt分布の根拠である。カイ二乗変数Uは、整数νなら独立なν個の標準正規変数の二乗和として表せる。正規標本で母平均を扱う場合は、平均と不偏分散の独立性により、この形が得られる。正規分布を仮定しない大標本のワルド統計量では、通常は標準正規分布の近似を使う。
F統計量の基本形は、独立なカイ二乗変数U1,U2をそれぞれの自由度ν1,ν2で割った比である。分散の比較では、帰無仮説の下で共通の母分散が比から消える。分散分析では、帰無仮説の下で群間と群内の平均平方の比がこの形になる。分子・分母の順序と自由度の順序は対応する。
T~tνならT²~F(1,ν)であり、両分布は独立な正規・カイ二乗変数を通じて関係する。本文は項目数を絞るため、この関係の式を省いた。
出典：University of Leicester, Sampling Distributions, PDF7ページ。
https://www.le.ac.uk/users/dsgp1/COURSES/LEISTATS/STATSLIDE8.pdf
''',
 ['review-t-f-distributions']
)

regular=make(
 'opening-review-regularity-information','復習②　正則条件とフィッシャー情報量',
 '正則条件は理論を使うための仮定で、情報量は母数の違いを識別する手がかりの強さ。',
 r'''- **正則条件**は、尤度の微分や漸近近似を正当化する仮定。次の項目は代表例であり、必要な条件は定理ごとに異なる。

- 真の母数は母数空間の内部にあり、異なる母数は異なる分布を表す。

- 対数尤度は十分滑らかで、分析者は微分と積分の順序を交換できる。

- フィッシャー情報量は有限で正。多母数では、情報行列は正定値。''',
 '<div class="opening-review-detail">'+''.join([
  '<h3>フィッシャー情報量（一母数）</h3>',
  r'<p>$X$ は1観測、$f(x\mid\theta)$ は確率（密度）関数。情報量 $I(\theta)$ は、観測が母数の違いをどれほど識別しやすいかを表す。</p>',
  eq(r'I(\theta)=E_\theta\!\left[\left\{\frac{\partial}{\partial\theta}\log f(X\mid\theta)\right\}^{\!2}\right].'),
  r'<p>独立同分布の $n$ 観測の情報量は $nI(\theta)$。最尤推定量 $\hat\theta$ の推定標準誤差は、大標本で、</p>',
  eq(r'\widehat{\operatorname{SE}}(\hat\theta)\approx\frac1{\sqrt{nI(\hat\theta)}}.'),
  '<p><strong>情報量が大きいほど、標準誤差は小さい。</strong></p>',
 ])+'</div>',
 '''このページは本章の尤度比検定・ワルド型検定・信頼区間を読むための復習である。
正則条件は、微分・期待値の交換や最尤推定量の漸近正規性などを正当化する仮定の総称であり、全ての定理について同一の短い条件一覧があるわけではない。本文は代表的な内容を簡潔に述べる。情報量の恒等式には微分と積分の交換などが必要であり、最尤推定量の漸近正規性やウィルクスの定理には、さらに識別可能性、一致性、局所的な滑らかさや一様性、帰無空間の滑らかな形など、定理に応じた条件が必要になる。
真の母数が母数空間の内部にあるという条件は、真の値が境界にないという意味。情報量が正・正定値という条件は、局所的に母数の違いを識別できるという条件である。滑らかさや可積分性の条件は、尤度を微分して期待値を計算する操作を正当化する。正則条件が崩れると、通常の正規・カイ二乗の漸近近似がそのまま使えない場合がある。
フィッシャー情報量は、一母数ではI(θ)=Eθ[(∂θ log f(X|θ))²]。Xは一つの観測を表す確率変数であり、Eθはモデルの母数をθとしたときのXの分布に関する期待値。特定の観測値の驚きの大きさ−log f(x|θ)とは別の量である。正則条件の下でスコアの平均は0であり、I(θ)=−Eθ[∂²θ log f(X|θ)]とも書ける。情報量は、対数尤度の平均的な曲率としても解釈できる。
独立同分布のn個の観測では、情報量はnI(θ)に加算される。一母数の正則なモデルでは、真の母数θにおける最尤推定量の分散の大標本近似は1/{nI(θ)}。分析者が未知のθを最尤推定値θhatで置き換え、平方根を取ると、本文の推定標準誤差を得る。標準誤差の式は全ての推定量に共通する厳密な式ではなく、正則な最尤推定における大標本の式である。
本文の情報量と標準誤差の式は一母数の場合を表示した。多母数では情報量は行列であり、漸近共分散行列は情報行列の逆行列をnで割ったものになる。
出典：UC Berkeley STAT210A, Score Function and Fisher Information、および既存の最尤推定量の漸近正規性の補足。
https://stat210a.berkeley.edu/fall-2025/reader/score-fisher.html
https://stat135.berkeley.edu/spring-2026/lectures/lecture-15.html
''',
 ['appendix-score-fisher','appendix-mle-normal']
)

deck['slides'][1:1]=[tf,regular]
deck['sections'].insert(0,{'id':'復習','title':'過去の復習'})
deck['sources']['review-t-f-distributions']={
 'title':'University of Leicester：Sampling Distributions',
 'url':'https://www.le.ac.uk/users/dsgp1/COURSES/LEISTATS/STATSLIDE8.pdf',
 'detail':'PDF7ページ：独立な正規・カイ二乗変数から得られるt分布とF分布。'
}
new={tf['id'],regular['id']}
assert len(deck['slides'])==len(old['slides'])+2
assert [s for s in deck['slides'] if s['id'] not in new]==old['slides']
assert len({s['id'] for s in deck['slides']})==len(deck['slides'])
encoded=json.dumps(deck,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
out=html[:m.start(2)]+encoded+html[m.end(2):]
style='''<style id="opening-review-layout">
.slide:is([data-slide-id="opening-review-t-f"],[data-slide-id="opening-review-regularity-information"]) .opening-review-detail h3{font-size:32px;line-height:1.4;margin:0 0 12px;color:var(--theme);}
.slide:is([data-slide-id="opening-review-t-f"],[data-slide-id="opening-review-regularity-information"]) .opening-review-detail p{margin:8px 0;line-height:1.4;}
.slide:is([data-slide-id="opening-review-t-f"],[data-slide-id="opening-review-regularity-information"]) .markdown>.body-list{margin-bottom:8px;}
.slide:is([data-slide-id="opening-review-t-f"],[data-slide-id="opening-review-regularity-information"]) .markdown p:has(.katex-display){margin:8px 0;}
.slide:is([data-slide-id="opening-review-t-f"],[data-slide-id="opening-review-regularity-information"]) .katex-display>.katex>.katex-html{line-height:1.3;}
</style>'''
out=out.replace('</head>',style+'</head>',1)
dst.write_text(out,encoding='utf-8')
print(f'Added review pages 2 and 3. {len(old["slides"])} -> {len(deck["slides"])} slides. Original slides unchanged; review added to dynamic agenda.')
