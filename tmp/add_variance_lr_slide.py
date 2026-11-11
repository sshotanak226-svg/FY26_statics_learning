from pathlib import Path
import copy, json, re
from html import escape

src=Path(r'F:\Download\９章　仮説検定と信頼区間_編集済み.html')
out=Path(r'F:\Document\Fy26 TDH statics lean\output\９章_仮説検定と信頼区間_分散比と尤度比.html')
text=src.read_text(encoding='utf-8')
match=re.search(r'(<script id="deck-data" type="application/json">)(.*?)(</script>)',text,re.S)
original=json.loads(match[2]); deck=copy.deepcopy(original)
index=next(i for i,s in enumerate(deck['slides']) if s['id']=='variance-test')+1
assert index==31
s=copy.deepcopy(deck['slides'][index-1])
s.update(id='variance-test-likelihood',title='9.4.2　正規二標本の分散比②：尤度比との関係',
    takeaway='F分布なら、推定分散のばらつきも含めて有限標本で正確に棄却点を決められる。',
    original='PDF 17–18ページ（9.4.2）の補足：分散比と尤度比の関係',minutes=1.5)
s['leftMarkdown']=r'''- **仮説検定**：独立な正規二標本（標本数 $m,n$）。

$$
H_0:\sigma_1^2=\sigma_2^2,\qquad H_1:\sigma_1^2\ne\sigma_2^2.
$$

- **計算する統計量**：共通分散での最大尤度を、各群別の最大尤度で割る。$U_1,U_2$ は群内平方和。

$$
U_1=(m-1)V_1^2,\qquad U_2=(n-1)V_2^2,
$$

$$
\Lambda=
\frac{(U_1/m)^{m/2}(U_2/n)^{n/2}}
{\{(U_1+U_2)/(m+n)\}^{(m+n)/2}}.
$$

$U_1/U_2=\{(m-1)/(n-1)\}F$ より、**尤度比もFだけで決まる**。

- **棄却域の計算**：前頁のF検定は、両裾に $\alpha/2$ ずつ配分する。

$$
\mathcal R=\{F<F_{m-1,n-1,1-\alpha/2}\}\cup\{F>F_{m-1,n-1,\alpha/2}\}.
$$'''
s['body']=[x[2:] for x in s['leftMarkdown'].splitlines() if x.startswith('- ')]
def p(t): return '<p>'+escape(t)+'</p>'
def eq(t): return '<div class="detail-equation">$$'+escape(t)+'$$</div>'
s['rightHTML']='<div class="example-detail">'+''.join([
    '<h3>χ²近似とF分布の違い</h3>',
    p('対数尤度比のχ²分布は、大標本での近似。'),
    eq(r'-2\log\Lambda\xrightarrow[H_0]{d}\chi_1^2\qquad(m,n\to\infty).'),
    p('この近似では、有限標本の棄却確率が有意水準からずれることがある。'),
    '<h3>F分布は有限標本でも厳密</h3>',
    eq(r'F=\frac{V_1^2}{V_2^2}\overset{H_0}{\sim}F_{m-1,n-1}.'),
    p('独立なχ²変数を自由度で割った比。分散を推定するばらつきも分布に含む。'),
    p('尤度比の境界もF分布で決められるが、等裾F検定とは一般に異なる。')
])+'</div>'
s['notes']='''前頁では、独立な正規二標本の不偏分散比が、帰無仮説の下で厳密にF分布に従うことを説明した。このスライドは尤度比との接続を補う。
ここで帰無仮説が制約するのは分散だけであり、平均は両群で別々の未知母数のまま。m,nはそれぞれの群の標本数で、各2以上。
共同尤度は L=(2πσ1²)^(-m/2)(2πσ2²)^(-n/2) exp[-Σ(Xi−μ1)²/(2σ1²)−Σ(Yj−μ2)²/(2σ2²)]。
制約なしでは平均はbarX,barY、分散はU1/m,U2/n。帰無仮説の下では平均は同じbarX,barYのままで、共通分散は(U1+U2)/(m+n)。両方の最大尤度で指数は−(m+n)/2となり、係数の比からスライドのΛを得る。
式の上下をU2^((m+n)/2)で割ると、ΛはU1/U2だけの関数になる。U1/U2=(m−1)/(n−1)Fなので、Fが分かればΛも計算できる。Fの極端に小さい側と大きい側でΛは小さくなる。
Λを統計量として使うことと、その棄却点をF分布で計算することは両立する。χ²と比較するのはΛそのものではなく、−2 log Λ。Wilksの定理でχ²1となるのは、両標本数を大きくする正則な漸近設定。分散は正で、帰無モデルは通常の内部の等分散制約。自由度1は制約が一つだから。
一方、Fの帰無分布は有限標本でも厳密。各群の残差平方和を共通母分散で割った量は独立なχ²(m−1),χ²(n−1)で、その自由度で割った比がF。推定値を使うから近似になるわけではない。標本数に依存するばらつきはF分布の自由度に反映済み。
左下は前頁の等裾F検定であり、F_(a,b,p)は上側p点。帰無仮説の下で両裾の確率はそれぞれα/2、合計αとなる。
厳密な尤度比検定そのものを実行するなら、Λ(fL)=Λ(fU)=c、P_H0(F<fL)+P_H0(F>fU)=αを同時に満たす境界を選ぶ。一般に各裾α/2とはならないので、等裾F検定を尤度比検定と同一視しない。
出典：提供スキャンの紙面140–141ページ（PDF17–18ページ、9.4.2）。尤度比の計算とχ²近似との比較は、同モデルからの補足導出。'''
deck['slides'].insert(index,s)
assert len(deck['slides'])==len(original['slides'])+1
assert deck['slides'][:index]+deck['slides'][index+1:]==original['slides']
assert deck['assets']==original['assets']
encoded=json.dumps(deck,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
text=text[:match.start(2)]+encoded+text[match.end(2):]
css='''<style id="variance-likelihood-addition-style">
.slide[data-slide-id="variance-test-likelihood"] .content.has-diagram{grid-template-columns:minmax(0,1.12fr) minmax(0,1fr);gap:34px;}
.slide[data-slide-id="variance-test-likelihood"] .markdown p{margin:3px 0 8px;}
.slide[data-slide-id="variance-test-likelihood"] .markdown>.body-list{margin:0 0 6px;}
.slide[data-slide-id="variance-test-likelihood"] .markdown .katex-display{margin:6px 0;}
.slide[data-slide-id="variance-test-likelihood"] .example-detail{padding-left:24px;}
.slide[data-slide-id="variance-test-likelihood"] .example-detail h3{margin:10px 0;}
.slide[data-slide-id="variance-test-likelihood"] .example-detail h3:first-child{margin-top:0;}
.slide[data-slide-id="variance-test-likelihood"] .example-detail p{margin:8px 0;}
.slide[data-slide-id="variance-test-likelihood"] .detail-equation{margin:8px 0;}
</style>'''
text=text.replace('</head>',css+'</head>',1)
out.write_text(text,encoding='utf-8')
print(out)
print('Inserted physical page',index+1,'; original slides preserved; total',len(deck['slides']))
