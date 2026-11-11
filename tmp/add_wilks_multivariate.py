from pathlib import Path
import json, re, copy, sys

sys.stdout.reconfigure(encoding='utf-8')
source=Path(r'F:\Document\Fy26 TDH statics lean\output\９章_仮説検定と信頼区間_Appendix追加.html')
target=Path(r'F:\Document\Fy26 TDH statics lean\output\９章_仮説検定と信頼区間_Appendix多母数拡張.html')
html=source.read_text(encoding='utf-8')
match=re.search(r'(<script id="deck-data" type="application/json">)([\s\S]*?)(</script>)',html)
deck=json.loads(match.group(2)); original=copy.deepcopy(deck)
assert len(deck['slides'])==65
deck['sources']['appendix-wilks-multi']={
 'title':'Charles University：Modern Statistical Methods, §2.6',
 'url':'https://www2.karlin.mff.cuni.cz/~omelka/Soubory/nmst434/nmst434_course-notes.pdf',
 'detail':'紙面26–30、補題2・定理7。情報行列のブロック逆行列、制約付き尤度比検定と自由度の導出。以下では平方完成によって同じ結論を示す。'}
deck['sources']['appendix-wilks-dimension']={
 'title':'University of Minnesota：Stat 3701, Statistical Models, Part II',
 'url':'https://www.stat.umn.edu/geyer/3701/notes/models2.html',
 'detail':'帰無仮説の下の尤度比検定、自由母数と検定対象の分割、帰無モデルと全モデルの次元差。'}

def add(ident,title,takeaway,md,refs=None,notes=''):
 s=copy.deepcopy(deck['slides'][54])
 s.update(id=ident,title=title,takeaway=takeaway,leftMarkdown=md,
          body=[l[2:] for l in md.splitlines() if l.startswith('- ')],
          original='9.3.2　自由度1から自由度m−kへの多母数拡張',
          sources=refs or ['appendix-wilks-multi'],notes=notes,minutes=1)
 deck['slides'].append(s)

add('appendix-multi-null','A12　多母数への拡張：前提と結論',
 '帰無仮説が正しい場合に、自由度が全母数の次元と帰無モデルの次元の差になる。',
 r'''- データを生成する**真の母数**を $\theta_*$ とする。以下は $H_0$ が正しい、すなわち $\theta_*\in\Theta_0$ の下での議論。

$$
\dim\Theta=m,\qquad\dim\Theta_0=k,
\qquad q:=m-k>0.
$$

- 正則条件として、真値が全母数空間の内部にあり、帰無モデルが真値付近で滑らかな $k$ 次元集合、情報行列が正定値であることなどを仮定する。

$$
\theta_*\in\Theta_0,\quad\text{正則条件}
\quad\Longrightarrow\quad
-2\log\Lambda\xrightarrow{d}\chi^2_q=\chi^2_{m-k}.
$$''', refs=['appendix-wilks-dimension','appendix-wilks-multi'],
 notes='m,kはnによらず固定。独立同分布の正則な識別可能モデルと、制約なし・制約ありの最尤推定量の一致性、局所一様な曲率収束、剰余制御を仮定する。境界・特異点の場合には次元差だけでこの結論は出ない。真値θ*と検定で指定した値を区別する。')

add('appendix-multi-estimators','A13　帰無仮説の下でも動かせる母数',
 '帰無仮説はq成分を固定し、残るk成分は制約の下で再推定する。',
 r'''- 真値付近で母数を次の座標に取り直す。$\psi_0$ は検定で指定する値。

$$
\theta=\begin{pmatrix}\eta\\\psi\end{pmatrix},
\quad\eta\in\mathbb R^k,\quad\psi\in\mathbb R^q,
\qquad H_0:\psi=\psi_0.
$$

- 制約なしの最尤推定値と、帰無仮説の制約を課した最尤推定値を区別する。

$$
\hat\theta=\begin{pmatrix}\hat\eta\\\hat\psi\end{pmatrix}
=\underset{\theta\in\Theta}{\arg\max}\,\ell(\theta),
\qquad
\tilde\theta=\begin{pmatrix}\tilde\eta\\\psi_0\end{pmatrix},
\quad\tilde\eta=\underset{\eta}{\arg\max}\,\ell(\eta,\psi_0).
$$

$$
\Lambda=\frac{L(\tilde\theta\mid\boldsymbol X)}{L(\hat\theta\mid\boldsymbol X)},
\qquad -2\log\Lambda=2\{\ell(\hat\theta)-\ell(\tilde\theta)\}.
$$''',
 notes='滑らかな帰無部分モデルを真値付近でψ=ψ0の形に表す。ηは自由に推定するk成分、ψは帰無仮説が指定するq成分。H0の下の真値はθ*=(η*,ψ0)。k=0ではηの再推定は不要で、点帰無仮説の多母数版になる。')

add('appendix-multi-information','A14　スコアと曲率をベクトル・行列にする',
 '一次微分はm次元のスコア、二次微分はm×mのヘッセ行列になる。',
 r'''- $\ell(\theta)=\sum_i\log f(X_i\mid\theta)$ の微分を、ベクトルと行列で表す。

$$
U_n(\theta):=\nabla\ell(\theta),
\qquad H_n(\theta):=\nabla^2\ell(\theta).
$$

- 1観測のスコアを $s_i(\theta)=\nabla\log f(X_i\mid\theta)$ とすると、真値での平均は零ベクトル。

$$
E_{\theta_*}[s_i(\theta_*)]=\boldsymbol0,
\qquad
\mathcal I:=\operatorname{Cov}_{\theta_*}[s_i(\theta_*)]
=-E_{\theta_*}[\nabla^2\log f(X_i\mid\theta_*)].
$$

- $\mathcal I$ は真値での**1観測あたりの情報行列**。正定値なので逆行列が存在する。''',
 refs=['appendix-score-fisher'],
 notes='以降はIを情報行列として使う代わりにmathcal Iと表記し、単位行列mathbf I_qと区別する。H_nは標本全体のヘッセ行列。微分と積分の交換により多変量でもスコア平均0と情報等式が成立する。')

add('appendix-multi-score-expansion','A15　ベクトルのスコア方程式を展開する',
 '線分に沿ってヘッセ行列を積分し、推定誤差をスコアから取り出す。',
 r'''- 内部の最尤推定値では $U_n(\hat\theta)=\boldsymbol0$。微積分の基本定理から、

$$
\boldsymbol0=U_n(\theta_*)+
\left[\int_0^1H_n\!\left(\theta_*+t(\hat\theta-\theta_*)\right)dt\right]
(\hat\theta-\theta_*).
$$

- 積分した曲率を $n$ で割り、負号を付けた行列を $M_n$ と置く。

$$
M_n:=-\frac1n\int_0^1H_n\!\left(\theta_*+t(\hat\theta-\theta_*)\right)dt.
$$

$$
\boldsymbol0=U_n(\theta_*)-nM_n(\hat\theta-\theta_*)
\quad\Longrightarrow\quad
\sqrt n(\hat\theta-\theta_*)=M_n^{-1}\frac{U_n(\theta_*)}{\sqrt n}.
$$''',
 refs=['appendix-score-fisher','appendix-wilks-multi'],
 notes='多変量では全成分に共通する一つの中間点があるとは限らないため、単一tildeθの平均値表示を使わず、線分上の積分で厳密な等式を表す。M_n→mathcal Iかつmathcal I正定値により、確率が1に近づく事象でM_nは可逆。')

add('appendix-multi-normal','A16　多母数の最尤推定量の漸近正規性',
 'スコアの多変量中心極限定理と曲率の確率極限を組み合わせる。',
 r'''- スコアは独立同分布のベクトルの和なので、多変量中心極限定理が使える。

$$
\frac{U_n(\theta_*)}{\sqrt n}\xrightarrow{d}Z,
\quad Z\sim N_m(\boldsymbol0,\mathcal I),
\qquad M_n\xrightarrow{p}\mathcal I.
$$

- 行列版のスルツキーの定理を使って、前ページの積に代入する。

$$
\sqrt n(\hat\theta-\theta_*)
\xrightarrow{d}\mathcal I^{-1}Z
\sim N_m(\boldsymbol0,\mathcal I^{-1}).
$$

- 極限の共分散行列は $\mathcal I^{-1}\mathcal I(\mathcal I^{-1})^\top=\mathcal I^{-1}$。スカラーの $1/I$ が、行列の逆行列に置き換わる。''',
 refs=['appendix-score-fisher','appendix-wilks-multi'],
 notes='情報行列は対称正定値。推定量の一致性と局所一様収束から、線分上の平均曲率M_nが真値での情報行列に確率収束する。正規極限の成分は一般に相関しており、ここではまだ独立な標準正規成分とはしない。')

add('appendix-multi-taylor','A17　尤度比を二次形式で表す',
 '1次元の「曲率×誤差の二乗」を、情報行列による二次形式に広げる。',
 r'''- $\ell(\tilde\theta)$ を制約なしの最尤推定値 $\hat\theta$ のまわりで二次まで展開する。

$$
\ell(\tilde\theta)=\ell(\hat\theta)
+\frac12(\tilde\theta-\hat\theta)^\top
H_n(\hat\theta)(\tilde\theta-\hat\theta)+o_p(1).
$$

- 一次項は $\nabla\ell(\hat\theta)=\boldsymbol0$ で消える。曲率の極限 $-H_n(\hat\theta)/n\xrightarrow{p}\mathcal I$ を使うと、

$$
-2\log\Lambda
=n(\tilde\theta-\hat\theta)^\top\mathcal I
(\tilde\theta-\hat\theta)+o_p(1).
$$

- この段階ではまだ $m$ 次元の式。次に、帰無仮説の下で自由な $k$ 成分を調整する。''',
 notes='固定次元で両最尤推定値の誤差がOp(n^−1/2)、三階微分などの局所的な剰余制御が成立する場合。帰無仮説下の制約付き推定量も正則なk次元モデルのMLEとしてroot-nの誤差を持つ。')

add('appendix-multi-partition','A18　自由なk成分と固定するq成分を分ける',
 '帰無仮説はψを固定するが、ηは尤度が最大になるように動かせる。',
 r'''- 情報行列を、$\eta$ と $\psi$ に対応するブロックに分ける。

$$
\mathcal I=\begin{pmatrix}A&B\\B^\top&C\end{pmatrix},
\qquad A\in\mathbb R^{k\times k},\quad
B\in\mathbb R^{k\times q},\quad C\in\mathbb R^{q\times q}.
$$

- $\delta:=\hat\psi-\psi_0$、$d:=\tilde\eta-\hat\eta$ と置くと、$\tilde\theta-\hat\theta=(d^\top,-\delta^\top)^\top$。

$$
Q(d):=\begin{pmatrix}d\\-\delta\end{pmatrix}^{\!\top}
\mathcal I\begin{pmatrix}d\\-\delta\end{pmatrix}
=d^\top A d-2d^\top B\delta+\delta^\top C\delta.
$$

- 制約下の尤度最大化は、二次近似では $d$ についての $Q(d)$ の最小化になる。''',
 notes='0<k<mの場合の計算。k=0なら自由成分がなく、以降のJはmathcal Iそのものになる。実際の制約付きMLEのdと二次式の最小点との差はop(n^−1/2)であり、尤度比統計量にはop(1)の違いしか生まない。')

add('appendix-multi-square','A19　平方完成で自由な成分を取り除く',
 'k成分を最適に調整すると、q成分の誤差だけを含む二次式が残る。',
 r'''- $A$ は正定値。前ページの式を平方完成する。

$$
\begin{aligned}
Q(d)&=(d-A^{-1}B\delta)^\top A(d-A^{-1}B\delta)
+\delta^\top J\delta,\\[4pt]
J&:=C-B^\top A^{-1}B.
\end{aligned}
$$

- 第一項は非負で、$d=A^{-1}B\delta$ のとき0になる。

$$
\min_d Q(d)=\delta^\top J\delta
\quad\Longrightarrow\quad
-2\log\Lambda=n\delta^\top J\delta+o_p(1).
$$

- $J$ は $q\times q$ の正定値行列。自由な母数 $\eta$ を再推定した後に残る情報量を表す。''',
 notes='JはAに対するシュール補行列で、自由母数の調整後の有効情報行列。正定値性は、δ≠0で(d0,−δ)≠0かつmathcal I正定値であることから、δ^T Jδ=min Q(d)>0と確認できる。平方完成は独立に代数展開して確認できる。')

add('appendix-multi-covariance','A20　残るq成分の共分散を求める',
 'ψの推定誤差の共分散は、調整後の情報行列Jの逆行列になる。',
 r'''- $\mathcal I\binom{u}{v}=\binom{\boldsymbol0}{w}$ を解く。$u$ は $k$ 次元、$v,w$ は $q$ 次元のベクトル。

$$
\left.\begin{aligned}
Au+Bv&=\boldsymbol0,\\
B^\top u+Cv&=w
\end{aligned}\right\}
\quad\Longrightarrow\quad
u=-A^{-1}Bv,\qquad Jv=w.
$$

- $v=J^{-1}w$ なので、逆行列の下側のブロックは、

$$
\bigl(\mathcal I^{-1}\bigr)_{\psi\psi}
=(C-B^\top A^{-1}B)^{-1}=J^{-1}.
$$

- $H_0$ の下では $\psi_*=\psi_0$。A16の正規極限から $\psi$ 成分を取り出す。

$$
\sqrt n\,\delta=\sqrt n(\hat\psi-\psi_0)
\xrightarrow{d}N_q(\boldsymbol0,J^{-1}).
$$''',
 notes='(mathcal I^−1)ψψは逆行列の部分ブロックであり、通常はC^−1とは異なる。Cだけを逆にすると、ηとの相関と再推定を無視することになる。')

add('appendix-multi-whitening','A21　標準化してq個の二乗和にする',
 '極限で独立な標準正規成分がq個残るため、自由度qのカイ二乗分布になる。',
 r'''- $J^{1/2}$ を対称正定値の平方根とし、推定誤差を標準化する。

$$
Z_n:=\sqrt n\,J^{1/2}\delta
\xrightarrow{d}Z\sim N_q(\boldsymbol0,\mathbf I_q).
$$

- $\mathbf I_q$ は単位行列。極限の $Z_1,\ldots,Z_q$ は**独立な標準正規変数**となる。

$$
-2\log\Lambda=Z_n^\top Z_n+o_p(1)
\quad\Longrightarrow\quad
-2\log\Lambda\xrightarrow{d}
\sum_{j=1}^{q}Z_j^2\sim\chi^2_q.
$$

- $q=m-k$ を代入すれば、求める $\chi^2_{m-k}$ への収束が得られる。''',
 notes='共分散はJ^1/2 J^−1 J^1/2=単位行列。多変量正規分布では無相関成分が独立になる。二乗和への変換は連続写像定理、剰余op(1)の処理はスルツキーの定理。有限標本のZ_n成分が厳密に独立とは主張しない。')

add('appendix-multi-df-summary','A22　自由度がm−kになる理由',
 '帰無仮説が固定する独立な成分数が、標準正規変数の二乗和の個数になる。',
 r'''- 全モデルでは $m$ 成分を推定する。帰無モデルでも $k$ 成分は自由に推定できる。

$$
\underbrace{m}_{\text{全母数の次元}}
-\underbrace{k}_{\text{帰無モデルの次元}}
=\underbrace{q}_{\text{帰無仮説が固定する成分数}}
=\text{自由度}.
$$

- $m=1,k=0$ なら $Z_1^2\sim\chi^2_1$。$m=3,k=1$ なら、標準化後の二乗和は $Z_1^2+Z_2^2\sim\chi^2_2$。

$$
\left.
\begin{gathered}
\theta_*\in\Theta_0,\quad\text{正則条件},\\
\dim\Theta=m,\quad\dim\Theta_0=k
\end{gathered}
\right\}
\quad\Longrightarrow\quad -2\log\Lambda\xrightarrow{d}\chi^2_{m-k}.
$$''',
 refs=['appendix-wilks-dimension','appendix-wilks-multi'],
 notes='母数の数だけではなく、真値付近での滑らかなモデルの次元を数える。点帰無仮説の一般化k=0ではJ=mathcal Iで、q=m個の二乗和になる。今回の1母数の点帰無仮説はm=1,k=0の特別な場合。')

assert len(deck['slides'])==76
assert deck['slides'][:65]==original['slides']
assert len({s['id'] for s in deck['slides']})==76
data=json.dumps(deck,ensure_ascii=False,indent=2).replace('<',r'\u003c')
result=html[:match.start(2)]+'\n'+data+'\n'+html[match.end(2):]
assert result[:match.start(2)]==html[:match.start(2)]
assert result.endswith(html[match.end(2):])
target.write_text(result,encoding='utf-8')
print(target)
print('Previous pages retained:',len(original['slides']))
print('New pages:',len(deck['slides'])-len(original['slides']))
