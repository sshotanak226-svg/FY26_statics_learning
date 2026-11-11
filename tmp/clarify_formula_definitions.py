import copy,json,re
from html import escape
from pathlib import Path

SOURCE=Path(r'F:\Document\Fy26 TDH statics lean\output\９章_仮説検定と信頼区間_検定例統一_表示修正.html')
TARGET=Path(r'F:\Document\Fy26 TDH statics lean\output\９章_仮説検定と信頼区間_数式定義整理.html')
html=SOURCE.read_text(encoding='utf-8');pat=r'(<script id="deck-data" type="application/json">)(.*?)(</script>)'
match=re.search(pat,html,re.S);original=json.loads(match[2]);deck=copy.deepcopy(original);changed={}
def eq(tex):return '\n\n$$\n'+tex.strip()+'\n$$\n\n'
def p(text):return '<p>'+escape(text).replace('&lt;br&gt;','<br>')+'</p>'
def f(tex):return '<div class="detail-equation">$$'+escape(tex)+'$$</div>'
def aside(title,*parts):return '<div class="example-detail"><h3>'+title+'</h3>'+''.join(parts)+'</div>'
def edit(page,reason,md=None,right=None,takeaway=None):
 s=deck['slides'][page-1]
 if md is not None:
  s['leftMarkdown']=md.strip();s['body']=[x[2:] for x in md.splitlines() if x.startswith('- ')]
 if right is not None:s['rightHTML']=right
 if takeaway is not None:s['takeaway']=takeaway
 changed[page]=reason
def example(page,change,setup,hyp,why,stat,how,region,right=None,takeaway=None):
 md='- **仮説検定**：'+setup+eq(hyp)+'- **計算する統計量**：'+why+eq(stat)+'- **棄却域の計算**：'+how+eq(region)
 edit(page,change,md,right,takeaway)

example(5,'二項分布の尤度Lを定義してから尤度比を計算。未導出の6.03の境界を削除。',
 r'独立な10回の試行で、表の回数を $K$、表の確率を $\theta$ とする。',
 r'H_0:\theta=0.5,\qquad H_1:\theta=0.7.',
 r'観測した表の回数の確率を尤度とし、二つの仮説で比べる。',
 r'\begin{gathered}L(\theta)=\binom{10}{K}\theta^K(1-\theta)^{10-K},\\[3pt]\Lambda=\frac{L(0.5)}{L(0.7)}=\left(\frac53\right)^{10}\left(\frac37\right)^K.\end{gathered}',
 r'表が増えるほど比は小さくなる。$\Lambda<1$ を採用すると、7回以上で棄却。',
 r'\mathcal R=\{\Lambda<1\}=\{K\ge7\}.',
 takeaway='二つの表確率で同じ観測の尤度を計算し、比が1より小さいときに帰無仮説を棄却する。')
edit(18,'一様最強力性の説明を文章化し、比較用の検定関数の余分な記号を削除。',
 right=aside('標本平均のばらつきと最強力性',
 f(r'\bar X=\frac1n\sum_{i=1}^nX_i,\qquad \operatorname{Var}_{H_0}(\bar X)=\frac{\sigma_0^2}{n}.'),
 p(r'平均差を標準誤差 $\sigma_0/\sqrt n$ で割ると、標準正規分布になる。'),
 p(r'対立する母平均をどの $\mu>\mu_0$ に固定しても、同じ棄却域が最強力となる。'),
 p('したがって、同じ有意水準以下の検定の中で、どの対立値に対しても検出力が最大になる。')))
example(19,'既知分散の正規尤度Lを追加し、尤度比が標本平均と単調に対応する計算を明示。',
 r'$n$ 個の独立な正規標本。標本平均は $\bar X$、母分散 $\sigma_0^2$ は既知。',
 r'H_0:\mu=\mu_0,\qquad H_1:\mu>\mu_0.',
 r'任意の $\mu_1>\mu_0$ で、対数尤度比の $\bar X$ の係数が負になる。',
 r'\begin{gathered}L(\mu)=(2\pi\sigma_0^2)^{-n/2}\exp\!\left[-\frac{\sum_i(X_i-\mu)^2}{2\sigma_0^2}\right],\\[4pt]\log\frac{L(\mu_0)}{L(\mu_1)}=-\frac{n(\mu_1-\mu_0)}{\sigma_0^2}\bar X+\frac{n(\mu_1^2-\mu_0^2)}{2\sigma_0^2},\\[4pt]W=\frac{\sqrt n(\bar X-\mu_0)}{\sigma_0}\overset{H_0}{\sim}N(0,1).\end{gathered}',
 r'$z_\alpha$ は標準正規分布の上側 $\alpha$ 点。境界は $\mu_1$ に依存しない。',
 r'\mathcal R=\{W>z_\alpha\}.')

edit(20,'Lを同時密度として定義し、母数集合と最大化の意味を先に説明。未定義の最尤推定値の別表記を削除。',md=r'''
- $\Theta$ は母数全体の集合、$\Theta_0$ は帰無仮説で許される母数の集合。

$$
H_0:\theta\in\Theta_0,\qquad H_1:\theta\in\Theta\setminus\Theta_0.
$$

- 尤度 $L$ は、観測した標本の同時密度を母数の関数と見たもの。離散分布では同時確率を使う。

$$
L(\theta\mid\boldsymbol x)=f(\boldsymbol x\mid\theta).
$$

- 帰無仮説の範囲で最大化した尤度を、母数全体で最大化した尤度で割る。

$$
\Lambda=\frac{\max_{\theta\in\Theta_0}L(\theta\mid\boldsymbol X)}{\max_{\theta\in\Theta}L(\theta\mid\boldsymbol X)}.
$$

- 分子の最大化には帰無仮説の制約があるため、比は1以下。小さいほど帰無仮説を棄却する根拠になる。
''')
deck['slides'][19]['safeFlow']=True

example(25,'尤度LからDを直接導出。ZとΛ=e^(−D/2)を削除し、棄却点をχ²だけで表記。',
 r'$X_1,\ldots,X_n$ は独立な $N(\mu,\sigma_0^2)$ 標本。母分散は既知、標本平均は $\bar X$。',
 r'H_0:\mu=\mu_0,\qquad H_1:\mu\ne\mu_0.',
 r'帰無側は $\mu_0$、制約なしでは $\bar X$ で尤度が最大。二つの高さを比べる。',
 r'\begin{gathered}L(\mu)=(2\pi\sigma_0^2)^{-n/2}\exp\!\left[-\frac{\sum_{i=1}^n(X_i-\mu)^2}{2\sigma_0^2}\right],\\[5pt]D=-2\log\frac{L(\mu_0)}{L(\bar X)}=\frac{n(\bar X-\mu_0)^2}{\sigma_0^2}\overset{H_0}{\sim}\chi_1^2.\end{gathered}',
 r'$\chi^2_{1,\alpha}$ は自由度1のχ²分布の上側 $\alpha$ 点。平均のずれが大きいと棄却。',
 r'\mathcal R=\{D>\chi^2_{1,\alpha}\}=\left\{|\bar X-\mu_0|>\frac{\sigma_0}{\sqrt n}\sqrt{\chi^2_{1,\alpha}}\right\}.',
 right='',takeaway='正規標本の尤度を最大化する前後で比べると、標準化した平均差の二乗が得られる。')

pooled_definition=aside('尤度Lと平方和の定義',
 f(r'\begin{gathered}L(\mu_X,\mu_Y,\sigma^2)=(2\pi\sigma^2)^{-N/2}\\[2pt]{}\times\exp\!\left[-\frac{\textstyle\sum_i(X_i-\mu_X)^2+\sum_j(Y_j-\mu_Y)^2}{2\sigma^2}\right].\end{gathered}'),
 p(r'各群で別々の中心 $\bar X,\bar Y$ を使う平方和を $U$ とする。'),
 f(r'U=\textstyle\sum_i(X_i-\bar X)^2+\sum_j(Y_j-\bar Y)^2.'),
 p(r'帰無仮説では、両群に共通の中心を使う。'),
 f(r'\hat\mu_0=\frac{m\bar X+n\bar Y}{N},\qquad U_0=U+\frac{mn}{N}(\bar X-\bar Y)^2.'),
 p(r'$U_0$ は共通中心からの平方和。$U_0\ge U$ なので、帰無側の最大尤度は大きくならない。'))
example(27,'正規二標本のL、U、共通中心とU0を明示。ν・cαの別名を削除。',
 r'独立な正規二標本。標本数は $m,n$、$N=m+n$。未知の母分散は共通。',
 r'H_0:\mu_X=\mu_Y,\qquad H_1:\mu_X\ne\mu_Y.',
 r'分散の最尤推定値は制約なしで $U/N$、帰無側で $U_0/N$。右のLに代入する。',
 r'\begin{gathered}\Lambda=\frac{L(\hat\mu_0,\hat\mu_0,U_0/N)}{L(\bar X,\bar Y,U/N)}=\left(\frac{U}{U_0}\right)^{N/2},\\[3pt]D=-2\log\Lambda=N\log\frac{U_0}{U}.\end{gathered}',
 r't分布の上側 $\alpha/2$ 点から境界を求める。Tとの対応は次頁で示す。',
 r'\mathcal R=\left\{D>N\log\!\left(1+\frac{t_{N-2,\alpha/2}^{\,2}}{N-2}\right)\right\}.',
 right=pooled_definition,
 takeaway='各群の中心を別々に選べる場合と、共通の中心しか使えない場合の最大尤度を比べる。')

example(28,'N・Uの定義元と標準誤差の意味を明示。棄却域に不要なdαの再掲を削除。',
 r'独立な等分散の正規二標本。$N=m+n$、$U$ は前頁の群内平方和。',
 r'H_0:\mu_X=\mu_Y,\qquad H_1:\mu_X\ne\mu_Y.',
 r'平均差の標準誤差は $\hat\sigma_U\sqrt{1/m+1/n}$。これで割ってTを作る。',
 r'\begin{gathered}\hat\sigma_U^2=\frac{U}{N-2},\qquad T=\frac{\bar X-\bar Y}{\hat\sigma_U\sqrt{1/m+1/n}},\\[3pt]D=N\log\!\left(1+\frac{T^2}{N-2}\right).\end{gathered}',
 r'$D$ は $T^2$ の増加関数。同じ検定を、t分布の両側境界で表せる。',
 r'\mathcal R=\{|T|>t_{N-2,\alpha/2}\}.')
deck['slides'][27]['rightHTML']=deck['slides'][27]['rightHTML'].replace('dα ≈ 4.386','棄却点 ≈ 4.386').replace('D > dα ⇔ |T| > 2.101','|T| > 2.101 で棄却')
example(29,'Nとプールした分散を再確認。判定に不要な棄却確率の重複式を削除。',
 r'独立な等分散の正規二標本。$N=m+n$、$\hat\sigma_U^2=U/(N-2)$。',
 r'H_0:\mu_X=\mu_Y,\qquad H_1:\mu_X\ne\mu_Y.',
 r'平均差を推定標準誤差で割ると、右の独立な正規変数とχ²変数の比になる。',
 r'T=\frac{\bar X-\bar Y}{\hat\sigma_U\sqrt{1/m+1/n}}\overset{H_0}{\sim}t_{N-2}.',
 r't分布の上側 $\alpha/2$ 点で両裾を切る。正規性・独立性・等分散の下で厳密。',
 r'\mathcal R=\{|T|>t_{N-2,\alpha/2}\}.')

welch_definition=aside('不偏分散と自由度',
 f(r'V_1^2=\frac{\sum_{i=1}^m(X_i-\bar X)^2}{m-1},\quad V_2^2=\frac{\sum_{j=1}^n(Y_j-\bar Y)^2}{n-1}.'),
 p('分母のばらつきをχ²分布で近似し、自由度を求める。原資料では整数部分を使う。'),
 f(r'\nu=\left\lfloor\frac{(V_1^2/m+V_2^2/n)^2}{(V_1^2/m)^2/(m-1)+(V_2^2/n)^2/(n-1)}\right\rfloor.'),
 p('このTは厳密なt分布ではない。自由度の導出は末尾の補足で説明する。'))
edit(30,'各群の不偏分散を式で定義。自由度の別名νhat_Wを削除してνに統一。',right=welch_definition)
deck['slides'][29]['leftMarkdown']=deck['slides'][29]['leftMarkdown'].replace('独立な正規二標本。両群の母分散が等しいとは仮定しない。',r'$X$ 群 $m$ 個、$Y$ 群 $n$ 個の独立な正規標本。等分散は仮定しない。')

f_definition=aside('比を取る二つの不偏分散',
 f(r'\begin{aligned}V_1^2&=\frac{\sum_{i=1}^m(X_i-\bar X)^2}{m-1},\\[4pt]V_2^2&=\frac{\sum_{j=1}^n(Y_j-\bar Y)^2}{n-1}.\end{aligned}'),
 p(r'$H_0$ の下では、それぞれを共通の母分散で割った量がχ²分布に従う。'),
 f(r'\begin{aligned}\frac{(m-1)V_1^2}{\sigma^2}&\sim\chi^2_{m-1},\\[3pt]\frac{(n-1)V_2^2}{\sigma^2}&\sim\chi^2_{n-1}.\end{aligned}'),
 p('両群は独立なので、自由度で割った二つのχ²変数の比がF分布になる。'))
edit(31,'V1²・V2²を定義し、共通分散が消えてF分布になる計算の根拠を表示。',right=f_definition)
deck['slides'][30]['leftMarkdown']=deck['slides'][30]['leftMarkdown'].replace(r'独立な正規二標本。$V_1^2,V_2^2$ は各群の不偏分散。',r'$X$ 群 $m$ 個、$Y$ 群 $n$ 個の独立な正規標本。右の不偏分散を使う。')
edit(32,'差の標本平均barZを定義してから、分散・Tを計算。',md=deck['slides'][31]['leftMarkdown'].replace(
 r'\begin{gathered}V_Z^2=',r'\begin{gathered}\bar Z=\frac1n\sum_{i=1}^nZ_i,\qquad V_Z^2='))

info_definition=aside('情報量から標準誤差を求める',
 p(r'$I(\theta)$ は1観測あたりのFisher情報量。$f$ はモデルの密度。'),
 f(r'I(\theta)=E_\theta\!\left[\left\{\frac{\partial}{\partial\theta}\log f(X\mid\theta)\right\}^2\right].'),
 p('最尤推定量の漸近分散に、推定した母数を代入する。'),
 f(r'\widehat{\operatorname{Var}}(\hat\theta)=\frac1{nI(\hat\theta)}.'),
 p('Wの分母は、その平方根である推定標準誤差。'))
edit(34,'Iが1観測あたりの情報量であることを定義し、Wの分母を標準誤差として表示。',right=info_definition,
 md=deck['slides'][33]['leftMarkdown'].replace(r'W=\sqrt{nI(\hat\theta)}(\hat\theta-\theta_0)',r'W=\frac{\hat\theta-\theta_0}{1/\sqrt{nI(\hat\theta)}}'))
edit(35,'母比率と標本比率を定義。使わないhatθの別名を削除。棄却点zの意味を明記。',
 md=deck['slides'][34]['leftMarkdown'].replace('独立なベルヌーイ標本の母比率を検定する。大標本を仮定。',r'$X_i=1$ を成功、$0$ を失敗とし、成功確率 $\theta$ を検定する。独立・大標本を仮定。').replace(r'\hat\theta=\bar X',r'\bar X=\frac1n\sum_{i=1}^nX_i').replace(r'$0<\bar X<1$ で標準正規近似を使い、両側の境界と比べる。',r'$0<\bar X<1$ とし、標準正規分布の上側 $\alpha/2$ 点を境界に使う。'))
edit(36,'S/√nを標準誤差と説明。重複する棄却域の別表現を削除。',
 md=deck['slides'][35]['leftMarkdown'].replace('中心極限定理を使うため、平均差を推定標準誤差で割る。',r'平均差を推定標準誤差 $S/\sqrt n$ で割ると、帰無分布を標準正規で近似できる。').replace(r'十分に大きい標本では標準正規分布の両側境界を使える。',r'$z_{\alpha/2}$ は標準正規分布の上側 $\alpha/2$ 点。大標本で両側検定する。').replace(r'\mathcal R=\{|W|>z_{\alpha/2}\}=\{\sqrt n\,|\bar X-\mu_0|>S z_{\alpha/2}\}.',r'\mathcal R=\{|W|>z_{\alpha/2}\}.'))
edit(37,'支持率θ1・θ2と差の期待値を明示し、仮説と計算する平均差を接続。',
 md=deck['slides'][36]['leftMarkdown'].replace(r'夫婦ごとの支持指標の差 $Z_i=X_i-Y_i$ を用い、組同士は独立とする。',r'夫 $X_i$、妻 $Y_i$ は支持なら1、非支持なら0。支持率を $\theta_1,\theta_2$ とし、夫婦の組は独立とする。').replace(r'\begin{gathered}\bar Z=\bar X-\bar Y,',r'\begin{gathered}Z_i=X_i-Y_i,\qquad E[Z_i]=\theta_1-\theta_2,\\[3pt]\bar Z=\frac1n\sum_iZ_i=\bar X-\bar Y,').replace(r'十分な組数と $S>0$ の下で、標準正規近似による両側検定を行う。',r'十分な組数と $S>0$ の下で、標準正規分布の上側 $\alpha/2$ 点を使う。'))
edit(50,'nと標本相関rの定義元を明記。未展開の回帰係数への言及を削除。',
 md=deck['slides'][49]['leftMarkdown'].replace(r'独立な二変量正規の観測組。標本相関を $r=R_{XY}$ とする。',r'独立な二変量正規の $n$ 組の標本。$r$ は49ページの式で求める標本相関。').replace('標本相関を回帰係数のt統計量に変換すると、既知の帰無分布を使える。','標本相関をt分布に従う形に変換し、無相関でも生じる相関のばらつきと比べる。').replace(r'自由度 $n-2$ のt分布の両側境界を使う（$n>2$）。',r'自由度 $n-2$ のt分布の上側 $\alpha/2$ 点を使う（$n>2$）。'))
edit(51,'標本相関r、変換値z・ξ0の役割と、標準誤差1/√(n−3)を明記。',
 md=deck['slides'][50]['leftMarkdown'].replace('独立な二変量正規の観測組で、指定した母相関を検定する。',r'独立な二変量正規の $n$ 組の標本。標本相関 $r$ から、母相関 $\rho_0$ を検定する。').replace('Fisher変換で分散をほぼ一定にし、帰無値からのずれを標準化する。',r'$z$ は標本相関、$\xi_0$ は帰無値のFisher変換。標準誤差は近似的に $1/\sqrt{n-3}$。').replace(r'W=\sqrt{n-3}(z-\xi_0)',r'W=\frac{z-\xi_0}{1/\sqrt{n-3}}').replace(r'$n>3$ で、大標本では $H_0$ の下の $W$ を標準正規分布で近似する。',r'大標本で $W$ を標準正規分布で近似し、その上側 $\alpha/2$ 点を使う（$n>3$）。'))

normal_unknown=aside('尤度と分散の最尤推定値',
 f(r'\begin{gathered}L(\mu,\sigma^2)=(2\pi\sigma^2)^{-n/2}\\[2pt]{}\times\exp\!\left[-\frac{\sum_i(X_i-\mu)^2}{2\sigma^2}\right].\end{gathered}'),
 p(r'制約なしでは平均は $\bar X$、帰無仮説では $\mu_0$ に固定する。'),
 f(r'\hat\sigma^2=\frac{\sum_i(X_i-\bar X)^2}{n},\qquad\hat\sigma_0^2=\frac{\sum_i(X_i-\mu_0)^2}{n}.'),
 p('それぞれの最大尤度に代入して比を取る。'),
 f(r'\Lambda=\frac{L(\mu_0,\hat\sigma_0^2)}{L(\bar X,\hat\sigma^2)}=\left(\frac{\hat\sigma^2}{\hat\sigma_0^2}\right)^{n/2}.'))
edit(77,'未知分散の正規尤度Lと、最大尤度に代入する平均・分散を明示。未使用のV²を削除。',right=normal_unknown)
edit(78,'最尤分散の参照元を明記。未定義のcαを棄却域から削除。',
 md=deck['slides'][77]['leftMarkdown'].replace(r'\mathcal R=\{|T|>t_{n-1,\alpha/2}\}=\{\Lambda<c_\alpha\}.',r'\mathcal R=\{|T|>t_{n-1,\alpha/2}\}.'),
 right=deck['slides'][77]['rightHTML'].replace(r'$n\hat\sigma^2=(n-1)V^2$ を代入する。',r'前頁の最尤分散と不偏分散には $n\hat\sigma^2=(n-1)V^2$ の関係がある。'))
edit(79,'V²の参照元を明記し、棄却点の記号をcαに統一。',
 md=deck['slides'][78]['leftMarkdown'].replace(r'独立な正規標本。母平均・母分散はともに未知（$n\ge2$）。',r'独立な正規標本。$V^2$ は前頁の不偏分散。母分散は未知（$n\ge2$）。'),
 right=aside('棄却条件の同値変形',p(r'$0<c_\alpha<1$。負のべき乗なので不等号が反転する。'),
 f(r'\begin{aligned}\Lambda<c_\alpha&\iff 1+\frac{T^2}{n-1}>c_\alpha^{-2/n}\\[7pt]&\iff |T|>\sqrt{(n-1)(c_\alpha^{-2/n}-1)}.\end{aligned}'),p('棄却される標本が同じなので、検定も同じ。')))

unknown_proof=deck['slides'][79]['rightHTML']
unknown_proof=unknown_proof.replace('<h3>正規分布とχ²分布の比</h3>','<h3>正規分布とχ²分布の比</h3>'+p(r'$V^2$ は、次の不偏分散。')+f(r'V^2=\frac{\sum_i(X_i-\bar X)^2}{n-1}.'))
edit(80,'V²を定義してから正規・χ²の比を示す。棄却確率の重複式を削除。',
 md=deck['slides'][79]['leftMarkdown'].replace(r'\mathcal R=\{|T|>t_{n-1,\alpha/2}\},\qquad P_{\mu_0}(\boldsymbol X\in\mathcal R)=\alpha.',r'\mathcal R=\{|T|>t_{n-1,\alpha/2}\}.'),right=unknown_proof)
edit(81,'Vは不偏標準偏差と明記。判定に使わないΛ・cαをまとめの式から削除。',
 md=deck['slides'][80]['leftMarkdown'].replace(r'独立な正規標本。母平均・母分散はともに未知（$n\ge2$）。',r'独立な正規標本。母分散は未知。$V$ は前頁の不偏分散の平方根（$n\ge2$）。').replace(r'\mathcal R=\{|T|>t_{n-1,\alpha/2}\}=\{\Lambda<c_\alpha\}.',r'\mathcal R=\{|T|>t_{n-1,\alpha/2}\}.'))
edit(82,'m・nとV1²・V2²の定義元を明記。',md=deck['slides'][81]['leftMarkdown'].replace('独立な正規二標本で、「平均差」と「分散比」の問いを区別する。',r'$X$ 群 $m$ 個、$Y$ 群 $n$ 個の独立な正規標本。$V_1^2,V_2^2$ は30ページで定義した不偏分散。'))

for i,(a,b) in enumerate(zip(original['slides'],deck['slides']),1):
 assert a['id']==b['id'] and a.get('notes')==b.get('notes')
 if i not in changed:assert a==b
 if b.get('testExample'):
  for token in ['**仮説検定**','**計算する統計量**','**棄却域の計算**','H_0:','H_1:']:assert token in b['leftMarkdown'],(i,token)
assert len(deck['slides'])==83 and deck['assets']==original['assets']
encoded=json.dumps(deck,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
html=html[:match.start(2)]+encoded+html[match.end(2):]
css='''
<style id="formula-definition-style">
.slide[data-slide-id="pooled"] .content.has-diagram{grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:34px;}
.slide[data-slide-id="pooled"] .example-detail{padding-left:22px;}
.slide[data-slide-id="pooled"] .example-detail h3{margin-bottom:10px;}
.slide[data-slide-id="pooled"] .example-detail p{margin:8px 0;}
.slide[data-slide-id="pooled"] .detail-equation{margin:6px 0;}
.slide[data-slide-id="pooled"] .markdown p{margin:3px 0 8px;}
.slide[data-slide-id="pooled"] .markdown>.body-list{margin:0 0 5px;}
.slide[data-slide-id="pooled"] .markdown .katex-display{margin:4px 0;}
.slide[data-slide-id="normal-t-null-distribution"] .example-detail p{margin:8px 0;}
.slide[data-slide-id="normal-t-null-distribution"] .detail-equation{margin:8px 0;}
</style>
'''
html=html.replace('</head>',css+'</head>',1);TARGET.write_text(html,encoding='utf-8')
Path('tmp/formula-definition-changes.json').write_text(json.dumps(changed,ensure_ascii=False,indent=2),encoding='utf-8')
print(TARGET);print('Changed pages:',list(changed))
