from pathlib import Path
from html import escape
import re,json,copy

src=Path('output/９章_仮説検定と信頼区間_ページスライダー_検出力行削除.html')
dst=Path('output/９章_仮説検定と信頼区間_ベルヌーイ情報量補足.html')
html=src.read_text(encoding='utf-8')
m=re.search(r'(<script id="deck-data" type="application/json">)(.*?)(</script>)',html,re.S)
a=json.loads(m[2]);d=copy.deepcopy(a)
i=next(i for i,x in enumerate(d['slides']) if x['id']=='bernoulli-wald');s=d['slides'][i]
def eq(t):return '<div class="detail-equation">$$'+escape(t)+'$$</div>'
s['rightHTML']='<div class="example-detail">'+''.join([
 '<h3>情報量からWの分母を求める</h3>',
 '<p>ベルヌーイ分布の1観測あたりの情報量は、</p>',
 eq(r'I(\theta)=\frac1\theta+\frac1{1-\theta}=\frac1{\theta(1-\theta)}.'),
 r'<p>最尤推定値 $\hat\theta=\bar X$ を代入すると、</p>',
 eq(r'\frac1{\sqrt{nI(\hat\theta)}}=\sqrt{\frac{\bar X(1-\bar X)}n}.'),
 '<p><strong>この推定標準誤差が、Wの分母。</strong></p>'
])+'</div>'
s['notes']+='''

【追加補足：情報量とWの分母】
ベルヌーイ1観測の対数尤度はℓ1(θ)=X log θ+(1−X)log(1−θ)。二階微分は−X/θ²−(1−X)/(1−θ)²。Eθ[X]=θを使うと、1観測あたりのFisher情報量はI(θ)=−Eθ[ℓ1''(θ)]=1/θ+1/(1−θ)=1/{θ(1−θ)}。
独立なn観測の情報量はnI(θ)。最尤推定量θhat=barXの分散はこの例では正確にθ(1−θ)/n=1/{nI(θ)}となる。未知のθをθhat=barXで置き換え、平方根を取ると、推定標準誤差は1/sqrt(nI(θhat))=sqrt(barX(1−barX)/n)。これが左のWの分母であり、前頁の一般式と一致する。
分散の式が正確であることと、標準化したWが有限標本で正規分布に従うことは別。Wの正規分布による判定は大標本の近似である。0<barX<1を仮定し、境界付近や少数標本には注意する。
'''
assert len(d['slides'])==len(a['slides'])==84
assert [j+1 for j,(x,y) in enumerate(zip(a['slides'],d['slides'])) if x!=y]==[35]
encoded=json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
html=html[:m.start(2)]+encoded+html[m.end(2):]
dst.write_text(html,encoding='utf-8')
print('Added a concise information-to-SE explanation on page 35 only; 84 slides and page slider retained.')
