from pathlib import Path
import json,re,copy,sys
sys.stdout.reconfigure(encoding='utf-8')
source=Path(r'C:\Users\User\Downloads\９章_仮説検定と信頼区間_Appendix多母数拡張.html')
target=Path(r'F:\Document\Fy26 TDH statics lean\output\９章_仮説検定と信頼区間_例9.5説明追加.html')
html=source.read_text(encoding='utf-8')
m=re.search(r'(<script id="deck-data" type="application/json">)([\s\S]*?)(</script>)',html)
deck=json.loads(m.group(2));original=copy.deepcopy(deck)
index=next(i for i,s in enumerate(deck['slides']) if s['id']=='normal-t')
base=deck['slides'][index]

def slide(ident,title,takeaway,md,notes):
 s=copy.deepcopy(base)
 s.update(id=ident,title=title,takeaway=takeaway,leftMarkdown=md,rightHTML='',
          body=[line[2:] for line in md.splitlines() if line.startswith('- ')],
          notes=notes,minutes=0.65)
 return s

new=[]
new.append(slide('normal-t-lr-transform','9.3.2　例9.5：尤度比をTの式で書き直す',
 '尤度比はT²の関数として厳密に表せるので、同じ検定を別の統計量で表現できる。',
 r'''- 正規標本で $H_0:\mu=\mu_0$、$H_1:\mu\ne\mu_0$ を考える。$n\ge2$ とし、不偏分散と $T$ を定義する。

$$
V^2=\frac1{n-1}\sum_{i=1}^n(X_i-\bar X)^2,
\qquad T=\frac{\sqrt n(\bar X-\mu_0)}{V}.
$$

- 分散の最尤推定値との関係は $n\hat\sigma^2=(n-1)V^2$。前ページの尤度比に代入する。

$$
\begin{aligned}
\Lambda
&=\left\{1+\frac{n(\bar X-\mu_0)^2}{n\hat\sigma^2}\right\}^{-n/2}\\[5pt]
&=\left\{1+\frac{n(\bar X-\mu_0)^2}{(n-1)V^2}\right\}^{-n/2}
=\left\{1+\frac{T^2}{n-1}\right\}^{-n/2}.
\end{aligned}
$$

- この書き換えは**近似ではなく等式**。次ページで、棄却条件も同じになることを示す。''',
 'PDF 14ページ（紙面137、例9.5）。n hatσ²=(n−1)V²とT²=n(barX−μ0)²/V²を代入した厳密な等式。Λは符号付きTの単調関数ではなくT²（または|T|）の減少関数。V>0は非退化な正規標本で確率1で成立する。'))

new.append(slide('normal-t-rejection-equivalence','9.3.2　例9.5：棄却条件が同じになる理由',
 '小さい尤度比で棄却することと、大きい|T|で棄却することは同じ判定になる。',
 r'''- 尤度比の境界を $0<c<1$ とする。両辺を $-2/n$ 乗すると、不等号が反転する。

$$
\begin{aligned}
\Lambda<c
&\quad\Longleftrightarrow\quad
\left(1+\frac{T^2}{n-1}\right)^{-n/2}<c\\[5pt]
&\quad\Longleftrightarrow\quad
1+\frac{T^2}{n-1}>c^{-2/n}\\[5pt]
&\quad\Longleftrightarrow\quad
|T|>\sqrt{(n-1)(c^{-2/n}-1)}.
\end{aligned}
$$

- $b(c):=\sqrt{(n-1)(c^{-2/n}-1)}$ と置けば、

$$
R=\{\Lambda<c\}=\{|T|>b(c)\}.
$$

- **棄却される標本が一致するので、検定は同じ。**''',
 'PDF 14ページ（紙面137、例9.5）のΛ<CとW>C′の関係を具体的に解く。n−1>0、0<c<1によりb(c)>0。大小の向きが反転する理由と両側検定なので|T|を用いることを明示する。棄却事象が一致するため、任意の母数値での棄却確率・検出力も同じ。'))

new.append(slide('normal-t-null-distribution','9.3.2　例9.5：Tの帰無分布を使える理由',
 '正規標本では、平均と分散を組み合わせたTが未知のσに依存しないt分布に従う。',
 r'''- $H_0$ が正しい場合、正規標本の基本性質から次の分布が得られる。

$$
Z=\frac{\sqrt n(\bar X-\mu_0)}{\sigma}\sim N(0,1),
\qquad U=\frac{(n-1)V^2}{\sigma^2}\sim\chi^2_{n-1}.
$$

- 正規標本では $\bar X$ と $V^2$ が独立なので、$Z$ と $U$ も独立。独立な標準正規変数とカイ二乗変数の比は、t分布の定義に一致する。

$$
\frac{Z}{\sqrt{U/(n-1)}}
=\frac{\sqrt n(\bar X-\mu_0)/\sigma}{V/\sigma}
=T\sim t_{n-1}.
$$

- $T$ には未知の $\sigma$ が現れない。**有限標本でも正確な棄却境界**を決められる。''',
 'PDF 14ページ（紙面137、例9.5・式9.15）のt分布への移行を補足。独立同分布N(μ,σ²)、σ²>0、H0:μ=μ0の下で、標本平均の正規分布、残差平方和のカイ二乗分布と両者の独立性を使う。t分布の定義Z/√(U/ν)にν=n−1を代入する。近似的なχ1²検定を経由せずに、元の尤度比検定を正確に校正できる。'))

base.update(
 takeaway='Tの両裾の確率をαに合わせると、元の尤度比検定にも同じ棄却境界を設定できる。',
 leftMarkdown=r'''- $H_0$ の下で $T\sim t_{n-1}$。上側 $\alpha/2$ 点を使い、両裾の確率を $\alpha$ にする。

$$
P_{\mu_0}\{|T|>t_{n-1,\alpha/2}\}=\alpha.
$$

- これに対応する尤度比の境界は、前ページまでの等式から決まる。

$$
c_\alpha=\left\{1+\frac{t_{n-1,\alpha/2}^{\,2}}{n-1}\right\}^{-n/2}.
$$

- 結果として、次の二つは**同じ棄却域**を表す。

$$
\begin{aligned}
R&=\{\Lambda<c_\alpha\}\\[4pt]
&=\{|T|>t_{n-1,\alpha/2}\}.
\end{aligned}
$$''',
 notes='PDF 14ページ（紙面137、例9.5・式9.15）。t_{ν,α/2}は自由度νのt分布の上側α/2点。b(cα)=t_{n−1,α/2}となるcαを逆算する。Λの値をTの値に近似しているのではなく、同じ棄却域を別の統計量で記述し、帰無分布を正確に用いる。')
base['body']=[l[2:] for l in base['leftMarkdown'].splitlines() if l.startswith('- ')]
deck['slides'][index:index]=new
assert len(deck['slides'])==len(original['slides'])+3
assert len({s['id'] for s in deck['slides']})==len(deck['slides'])
for old in original['slides']:
 if old['id']!='normal-t':
  assert old==next(s for s in deck['slides'] if s['id']==old['id']),old['id']
data=json.dumps(deck,ensure_ascii=False,indent=2).replace('<',r'\u003c')
result=html[:m.start(2)]+'\n'+data+'\n'+html[m.end(2):]
assert result[:m.start(2)]==html[:m.start(2)]
assert result.endswith(html[m.end(2):])
target.write_text(result,encoding='utf-8')
print(target)
for i,s in enumerate(deck['slides'],1):
 if s['id'] in {x['id'] for x in new}|{'normal-t'}:print(i,s['title'])
