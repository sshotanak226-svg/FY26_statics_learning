from pathlib import Path
import json,re,copy

src=Path('output/９章_仮説検定と信頼区間_ベルヌーイ情報量補足.html')
dst=Path('output/９章_仮説検定と信頼区間_信頼区間の定義補足.html')
html=src.read_text(encoding='utf-8')
m=re.search(r'(<script id="deck-data" type="application/json">)(.*?)(</script>)',html,re.S)
original=json.loads(m[2]); deck=copy.deepcopy(original)
s=deck['slides'][38]
assert s['id']=='ci-inversion'
s['takeaway']='未知の真の母数を、標本から計算した区間で推定する。信頼係数は、その方法が母数を含む確率の保証値。'
s['body']=[
    'θは推定したい未知の真の母数（例：母平均μ）。推定値θhatとは区別する。',
    '標本Xから下限L(X)と上限U(X)を計算し、θを推定する区間を作る。',
    '信頼係数1−α（例：95%）は、標本を取り直して同じ方法で作る区間が、真のθを含む確率の保証値。'
]
s['leftMarkdown']=r'''- $\theta$ は推定したい**未知の真の母数**（例：母平均 $\mu$）。推定値 $\hat\theta$ とは区別する。

- 標本 $\boldsymbol X$ から下限 $L(\boldsymbol X)$ と上限 $U(\boldsymbol X)$ を計算し、$\theta$ を推定する区間を作る。

- **信頼係数 $1-\alpha$**（例：95%）は、標本を取り直して同じ方法で作る区間が、真の $\theta$ を含む確率の保証値。

$$
P_\theta\!\left\{L(\boldsymbol X)\le\theta\le U(\boldsymbol X)\right\}
\ge 1-\alpha\quad(\forall\theta\in\Theta).
$$
'''
s['rightHTML']=r'''<div data-diagram="sourceInversion"></div><p style="margin:0 0 8px">各候補 $\theta_0$ を検定し、棄却されない候補を集める。</p><div class="detail-equation">$$C(\boldsymbol x)=\{\theta_0\in\Theta:\boldsymbol x\in A(\theta_0)\}.$$</div>'''
s['notes']='''対応：提供PDF 21–22ページ（紙面144–145、定義9.8・式9.23）。
θは推定したい未知の真の母数であり、例えば母集団の平均μ。標本から求める点推定値θhatと区別する。
X=(X1,…,Xn)は標本。L(X)とU(X)は標本から計算する下限と上限で、[L(X),U(X)]が区間推定のための信頼区間となる。
母数θを固定し、その母数の分布から同じ大きさの標本を繰り返し得ることを考える。毎回区間を作ると、その区間が固定された真のθを含む確率が被覆確率。資料の定義では、どのθが真でもこの確率が1−α以上となる方法を、信頼係数1−αの信頼区間と呼ぶ。
例えば1−α=0.95なら、同じ方法による区間が真の母数を含む確率を少なくとも95%保証する。有限回の反復で必ず95%以上の個数が含むと保証する意味ではない。観測後の数値区間に対してθ自身が95%の確率で動くという意味でもない。
右は検定から信頼集合を作る方法。A(θ0)はH0:θ=θ0を棄却しない標本の範囲。観測xがその範囲に入る候補θ0を集めた集合がC(x)。θ∈C(X)とX∈A(θ)は同じ事象なので、受容確率と被覆確率が一致する。資料では受容確率を1−αとする検定を用いるため等号の被覆確率となる。集合が区間なら上下限L,Uで表せる。
'''
assert [i+1 for i,(a,b) in enumerate(zip(original['slides'],deck['slides'])) if a!=b]==[39]
encoded=json.dumps(deck,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
dst.write_text(html[:m.start(2)]+encoded+html[m.end(2):],encoding='utf-8')
audit=Path('tmp/audit_bernoulli_information.cjs').read_text(encoding='utf-8').replace('for(let i=34;i<35;i++)','for(let i=38;i<39;i++)')
Path('tmp/audit_confidence_interval.cjs').write_text(audit,encoding='utf-8')
print('Updated page 39 only; slide count and runtime preserved.')
