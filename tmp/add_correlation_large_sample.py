from pathlib import Path
import json,re,copy

src=Path('output/９章_仮説検定と信頼区間_相関Rの途中式追加.html')
dst=Path('output/９章_仮説検定と信頼区間_非正規標本の大標本近似追加.html')
html=src.read_text(encoding='utf-8')
m=re.search(r'<script id="deck-data" type="application/json">(.*?)</script>',html,re.S)
old=json.loads(m[1]);deck=copy.deepcopy(old)
assert deck['slides'][48]['id']=='correlation-t-density-proof'
s=copy.deepcopy(deck['slides'][48])
s.update(id='correlation-nonnormal-large-sample',title='9.7.1　非正規標本における大標本近似',
    takeaway='正規性がなくても、XとYの独立性と有限な分散の下では、大標本近似が成り立つ。',
    original='正規性を仮定しない独立な2変数について、中心極限定理による相関統計量の大標本近似を補足',
    sources=['correlation-nonnormal-reference'],minutes=1.0)
s['leftMarkdown']=r'''- **成立する条件**：観測組 $(X_i,Y_i)$ は独立同分布、$X$ と $Y$ は独立、両変数の分散は有限かつ正とする。この条件では母相関 $\rho=0$ となり、正規性は不要となる。

- **中心極限定理**：$\mu_X,\mu_Y$ と $\sigma_X,\sigma_Y$ は母平均と母標準偏差を表す。中心極限定理が次式を与える。

$$
Q_i=\frac{(X_i-\mu_X)(Y_i-\mu_Y)}{\sigma_X\sigma_Y},\qquad
E[Q_i]=0,\quad \operatorname{Var}(Q_i)=1,\qquad
\frac1{\sqrt n}\sum_{i=1}^{n}Q_i\xrightarrow{d}N(0,1).
$$

- **相関への接続**：標本平均・標本標準偏差の推定誤差と $R$ は0に近づき、$T$ は次式で近似できる。

$$
T=\frac{\sqrt{n-2}\,R}{\sqrt{1-R^2}}
\approx\sqrt n\,R
\approx\frac1{\sqrt n}\sum_{i=1}^{n}Q_i
\xrightarrow{d}N(0,1).
$$

- **t分布による近似**：$t_{n-2}$ 分布も $N(0,1)$ に近づくため、分析者はt分布を近似に使える。**母相関0だけでは、任意の分布での近似は保証されない。**'''
s['body']=[p[2:] for p in s['leftMarkdown'].split('\n\n') if p.startswith('- ')]
s['notes']='''本ページは教科書本文の引用ではなく、非正規標本で通常の相関統計量を近似評価できる十分条件を示す補足である。「任意の分布でも標本数が多ければ成立する」という無条件の主張は誤りなので記載しない。
条件は、各観測組が独立同分布であること、組内のXとYが独立であること、両変数の分散が有限かつ正であること。離散分布でもよく、正規性は不要。この十分条件は必要条件という意味ではない。組の間の独立性と、組の中のXとYの独立性は異なる条件である。
Q_i=(Xi−μX)(Yi−μY)/(σXσY)と置く。独立性によりE[Q_i]=0、E[Q_i²]=E[(Xi−μX)²]E[(Yi−μY)²]/(σX²σY²)=1。したがってQ_iは独立同分布、平均0、分散1であり、通常の中心極限定理が適用できる。ここではXやY自体が正規分布に変わるとは主張していない。
正確な接続は、sqrt(n)R={ΣQ_i/sqrt(n)−sqrt(n)(barX−μX)(barY−μY)/(σXσY)}/{(S_X/σX)(S_Y/σY)}。S_X²とS_Y²は分母nの標本分散。有限分散と中心極限定理により標本平均の誤差の積にsqrt(n)を掛けた項は確率収束で0になり、大数の法則により分母は1に確率収束する。Slutskyの定理でsqrt(n)R→dN(0,1)。独立性の下ではX,Yそれぞれの4次モーメントまでは仮定する必要がない。
T/sqrt(n)R=sqrt((n−2)/n)/sqrt(1−R²)は確率収束で1になるので、T→dN(0,1)。t(n−2)の分位点も正規分布の分位点へ収束するため、t分位点による両側棄却域はこの条件下で漸近的に有意水準を保つ。有限のnでTが厳密なt分布になるという主張ではない。十分な標本数は分布に依存するため、一律の標本数の基準は示せない。分析者はTの計算に母平均や母標準偏差を知る必要はなく、これらは近似の理由を示す理論上の量である。
母相関0だけでXとYの独立性は保証されない。有限な4次モーメントなどの条件を置く一般の無相関な場合には、sqrt(n)Rの漸近分散はτ²=E[(X−μX)²(Y−μY)²]/(σX²σY²)であり、必ずしも1ではない。例えばX~U(−1,1),Y=X²ならρ=0だがτ²=11/7で、通常のt分位点による検定は大標本でも一般には正当化できない。分散が存在しない分布や観測間に依存がある場合も本ページの十分条件から外れる。
参考文献：Alan D. Hutson (2019), A robust Pearson correlation test for a general point null using a surrogate bootstrap distribution, PLOS ONE 14(5):e0216287. Introduction, equations (4)–(6):一般の分布では相関係数の漸近分散が分布に依存する。独立なX,Yへの簡約と有限分散のみの導出は、本ページで示す補足計算による。
https://pmc.ncbi.nlm.nih.gov/articles/PMC6522008/
'''
deck['sources']['correlation-nonnormal-reference']={'title':'Hutson (2019)：非正規分布におけるPearson相関検定','url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC6522008/','detail':'Introduction, 式(4)–(6)：一般の分布での相関係数の漸近分布と、正規性の誤指定の問題。'}
deck['slides'].insert(49,s)
assert len(deck['slides'])==len(old['slides'])+1
assert deck['slides'][:49]+deck['slides'][50:]==old['slides']
assert len(set(x['id'] for x in deck['slides']))==len(deck['slides'])
payload=json.dumps(deck,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
out=html[:m.start(1)]+payload+html[m.end(1):]
css='''<style>
.slide[data-slide-id="correlation-nonnormal-large-sample"] .content.full-width .text-block{padding-top:0;padding-bottom:0;}
.slide[data-slide-id="correlation-nonnormal-large-sample"] .markdown>.body-list{margin:0 0 8px;}
.slide[data-slide-id="correlation-nonnormal-large-sample"] .content.full-width .markdown>.body-list>li{margin-bottom:10px;}
.slide[data-slide-id="correlation-nonnormal-large-sample"] .content.full-width .markdown>.body-list>li:last-child{margin-bottom:0;}
.slide[data-slide-id="correlation-nonnormal-large-sample"] .markdown p:has(.katex-display){margin:6px 0;}
.slide[data-slide-id="correlation-nonnormal-large-sample"] .katex-display>.katex>.katex-html{line-height:1.3;}
</style>'''
out=out.replace('</head>',css+'</head>',1)
dst.write_text(out,encoding='utf-8')
print('Inserted page 50 after page 49. All original slides unchanged; total 88 slides.')
audit=Path('tmp/audit_short_correlation_t.cjs').read_text(encoding='utf-8').replace('for(let i=48;i<50;i++)','for(let i=48;i<51;i++)')
Path('tmp/audit_correlation_large_sample.cjs').write_text(audit,encoding='utf-8')
