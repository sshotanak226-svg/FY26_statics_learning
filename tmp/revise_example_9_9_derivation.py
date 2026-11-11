from pathlib import Path
import re,json,copy

src=Path('output/９章_仮説検定と信頼区間_例9.9と9.10追加.html')
dst=Path('output/９章_仮説検定と信頼区間_例9.9導出追加.html')
html=src.read_text(encoding='utf-8')
m=re.search(r'(<script id="deck-data" type="application/json">)(.*?)(</script>)',html,re.S)
old=json.loads(m[2]);deck=copy.deepcopy(old)
s=next(s for s in deck['slides'] if s['id']=='example-9-9-ci-summary')
s['takeaway']='分析者は、検定の受容条件を帰無値μ₀について解き、母平均の信頼区間を求める。'
s['leftMarkdown']=r'''- 独立な正規標本 $X_1,\ldots,X_n\sim N(\mu,\sigma^2)$ では、$n$ は標本数、$\bar X$ は標本平均、$V$ は不偏分散の平方根。分析者は、真の母平均 $\mu$ を区間推定する。

- 両側検定 $H_0:\mu=\mu_0$、$H_1:\mu\ne\mu_0$ は、有意水準 $\alpha$ で次の受容条件を使う。上段は母分散 $\sigma_0^2$ が既知の場合、下段は母分散が未知の場合。

$$
\begin{aligned}
\left|\frac{\sqrt n(\bar X-\mu_0)}{\sigma_0}\right|\le z_{\alpha/2}
&\Longleftrightarrow\quad
\bar X-z_{\alpha/2}\frac{\sigma_0}{\sqrt n}\le\mu_0\le\bar X+z_{\alpha/2}\frac{\sigma_0}{\sqrt n},\\[14pt]
\left|\frac{\sqrt n(\bar X-\mu_0)}V\right|\le t_{n-1,\alpha/2}
&\Longleftrightarrow\quad
\bar X-t_{n-1,\alpha/2}\frac V{\sqrt n}\le\mu_0\le\bar X+t_{n-1,\alpha/2}\frac V{\sqrt n}.
\end{aligned}
$$

- 分析者は、各不等式の下限から上限までを信頼区間とする。$z_{\alpha/2}$ と $t_{n-1,\alpha/2}$ は、それぞれ標準正規分布と自由度 $n-1$ のt分布の上側 $\alpha/2$ 点。'''
s['body']=[p[2:] for p in s['leftMarkdown'].split('\n\n') if p.startswith('- ')]
s['notes']+='''
【表示変更：受容条件から信頼区間への計算】
標本平均と不偏分散の定義式は本文から削除した。本文では標本数n、標本平均barX、不偏分散の平方根Vの意味を文章で明記した。
既知分散の場合、分析者は|sqrt(n)(barX−μ0)/σ0|≤zα/2の両辺に正の値σ0/sqrt(n)を掛け、|barX−μ0|≤zα/2 σ0/sqrt(n)を得る。分析者は絶対値の不等式を−zα/2 σ0/sqrt(n)≤barX−μ0≤zα/2 σ0/sqrt(n)と書き換え、μ0について整理して、barX−zα/2 σ0/sqrt(n)≤μ0≤barX+zα/2 σ0/sqrt(n)を得る。
未知分散の場合、分析者は正の値V/sqrt(n)を用いて同じ代数計算を行う。分析者は|sqrt(n)(barX−μ0)/V|≤t(n−1,α/2)から、barX−t(n−1,α/2)V/sqrt(n)≤μ0≤barX+t(n−1,α/2)V/sqrt(n)を得る。正規標本でσ²>0、n≥2ならV>0は確率1で成り立つ。
各不等式を満たす帰無値μ0の集合が、検定で棄却されない母平均の候補を全て集めた信頼区間である。正規標本の仮定の下では、両方の区間の被覆確率が厳密に1−αになる。
'''
assert [i+1 for i,(a,b) in enumerate(zip(old['slides'],deck['slides'])) if a!=b]==[41]
encoded=json.dumps(deck,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
out=html[:m.start(2)]+encoded+html[m.end(2):]
dst.write_text(out,encoding='utf-8')
print('Changed page 41 only; kept all 83 slides and application code.')
