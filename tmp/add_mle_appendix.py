from pathlib import Path
import re, json, copy, sys

sys.stdout.reconfigure(encoding='utf-8')
source = Path(r'C:\Users\User\Downloads\９章　仮説検定と信頼区間_編集済み (18).html')
target = Path(r'F:\Document\Fy26 TDH statics lean\output\９章_仮説検定と信頼区間_Appendix追加.html')
html = source.read_text(encoding='utf-8')
match = re.search(r'(<script id="deck-data" type="application/json">)([\s\S]*?)(</script>)', html)
deck = json.loads(match.group(2))
original = copy.deepcopy(deck)

deck['sources']['appendix-score-fisher'] = {
    'title': 'UC Berkeley STAT 210A：Score Function and Fisher Information',
    'url': 'https://stat210a.berkeley.edu/fall-2025/reader/score-fisher.html',
    'detail': 'スコアの平均0、フィッシャー情報量と負の二階微分の期待値の関係。'}
deck['sources']['appendix-mle-normal'] = {
    'title': 'UC Berkeley STAT 135：Proof of Asymptotic Normality, and Confidence Intervals',
    'url': 'https://stat135.berkeley.edu/spring-2026/lectures/lecture-15.html',
    'detail': 'スコアの中心極限定理、曲率の大数の法則、スルツキーの定理による最尤推定量の漸近正規性。本補足は平均値の定理の中間点を用いて等式で整理する。'}

cover = copy.deepcopy(deck['slides'][0])
cover.update(id='appendix-title', title='Appendix', section='Appendix',
             majorSection='Appendix', subsection='', appendix=True, minutes=0,
             original='', sources=[], notes='曲率の確率極限と最尤推定量の漸近正規性に関する補足。')
deck['slides'].append(cover)

def add(ident, title, takeaway, markdown, refs=None, notes=''):
    s = {
        'id':ident, 'title':title, 'section':'Appendix', 'majorSection':'Appendix',
        'subsection':'9.3.2 補足', 'subtitle':'', 'takeaway':takeaway,
        'body':[], 'leftMarkdown':markdown, 'rightHTML':'', 'theme':'proof',
        'layout':'split', 'appendix':True, 'minutes':1,
        'equations':[], 'diagram':'', 'table':[], 'flow':[], 'answers':[],
        'figurePrompt':'', 'original':'9.3.2　曲率の確率極限と最尤推定量の漸近正規性の補足',
        'sources': refs or ['appendix-mle-normal'], 'notes':notes,
    }
    s['body'] = [line[2:] for line in markdown.splitlines() if line.startswith('- ')]
    deck['slides'].append(s)

add('appendix-mle-setting', 'A1　対数尤度・最尤推定量と前提',
    '帰無仮説の下で、母数空間全体における最尤推定量の振る舞いを調べる。',
    r'''- $X_1,\ldots,X_n$ は独立同分布、母数は1次元。$H_0:\theta=\theta_0$ の下で考える。

$$
\ell(\theta)=\sum_{i=1}^n\log f(X_i\mid\theta),
\qquad
\hat\theta=\underset{\theta\in\Theta}{\arg\max}\;\ell(\theta).
$$

- $\hat\theta$ は帰無仮説の制約を課さない最尤推定値。**内部で最大**となるので、$\ell'(\hat\theta)=0$。

- 滑らかさ、微分と積分の交換、$0<I(\theta_0)<\infty$ を仮定する。

- 最尤推定量の一致性と、近傍での曲率の一様収束も仮定する。''',
    notes='1次元の正則なi.i.d.モデルを考える。対数尤度は標本全体についての和、Iは1観測あたり。最尤推定量の一致性はここでの前提であり、スコア方程式だけからは保証されない。')

add('appendix-fisher-identity', 'A2　スコアとフィッシャー情報量',
    '正則条件の下で、スコアの平均は0、分散は負の曲率の期待値に等しい。',
    r'''- 1観測のスコアと曲率に対応する量を定義する。

$$
s_i(\theta)=\frac{\partial}{\partial\theta}\log f(X_i\mid\theta),
\qquad
h_i(\theta)=-\frac{\partial^2}{\partial\theta^2}\log f(X_i\mid\theta).
$$

- $\int f(x\mid\theta)\,dx=1$ を微分すると、真の母数でのスコアの平均は0になる。

$$
E_{\theta_0}[s_i(\theta_0)]
=\int\left.\frac{\partial f(x\mid\theta)}{\partial\theta}\right|_{\theta=\theta_0}\!dx=0.
$$

- さらに二階微分すると、1観測あたりの情報量は次の形で表せる。

$$
I(\theta_0):=\operatorname{Var}_{\theta_0}[s_i(\theta_0)]
=E_{\theta_0}[h_i(\theta_0)].
$$''', refs=['appendix-score-fisher'],
    notes='密度の共通の台と微分・積分の交換などの条件を置く。f″=f{(log f)″+((log f)′)²}の積分が0であることから、スコアの二乗の期待値＝負の二階微分の期待値となる。Iは1観測あたり。')

add('appendix-curvature-lln', 'A3　曲率の極限：大数の法則',
    '標本全体の負の二階微分をnで割ると、1観測の曲率の標本平均になる。',
    r'''- 対数尤度は和なので、二階微分も各観測の二階微分の和になる。

$$
-\frac1n\ell''(\theta_0)
=\frac1n\sum_{i=1}^n h_i(\theta_0).
$$

- $h_i(\theta_0)$ は独立同分布で、期待値は $I(\theta_0)$。可積分性の下で大数の法則を使う。

$$
\frac1n\sum_{i=1}^n h_i(\theta_0)
\xrightarrow{p}E_{\theta_0}[h_i(\theta_0)]
=I(\theta_0).
$$

- ここでの評価点は、まず**真の母数 $\theta_0$** に固定している。''',
    refs=['appendix-score-fisher','appendix-mle-normal'],
    notes='E|h_i(θ0)|<∞を仮定する。負の観測情報量をnで平均化することで、1観測あたりのフィッシャー情報量に収束する。')

add('appendix-curvature-random', 'A4　評価点を推定値に置き換える根拠',
    '一致性に加え、曲率の近傍での一様収束を使って、ランダムな評価点を扱う。',
    r'''- $H(\theta):=E_{\theta_0}[h_i(\theta)]$ と置き、その連続性と近傍 $U$ での一様収束を仮定する。

$$
\sup_{\theta\in U}
\left|-\frac1n\ell''(\theta)-H(\theta)\right|\xrightarrow{p}0.
$$

- 任意の $T_n\xrightarrow{p}\theta_0$ に対して、次の二つの誤差がともに0に近づく。

$$
\left|-\frac1n\ell''(T_n)-I(\theta_0)\right|
\le
\left|-\frac1n\ell''(T_n)-H(T_n)\right|
+|H(T_n)-H(\theta_0)|.
$$

- $H(\theta_0)=I(\theta_0)$。$T_n=\hat\theta$、または中間点 $\tilde\theta$ とすれば、

$$
-\frac1n\ell''(\hat\theta)\xrightarrow{p}I(\theta_0),
\qquad
-\frac1n\ell''(\tilde\theta)\xrightarrow{p}I(\theta_0).
$$''',
    notes='点ごとの大数の法則だけではランダムな評価点への置換は保証されない。本ページの局所一様収束とHの連続性は十分条件。H(θ)=Eθ0h_i(θ)なので、一般にはI(θ)=Eθh_i(θ)とは異なるが、θ=θ0で一致する。P(T_n∈U)→1となる事象で不等式を適用する。推定量の一致性により、中間点もθ0へ確率収束する。')

add('appendix-score-clt', 'A5　スコアの極限：中心極限定理',
    '平均0・分散Iのスコアを足し合わせ、√nで割ると正規分布に収束する。',
    r'''- 標本全体のスコアは、1観測のスコアの和である。

$$
\ell'(\theta_0)=\sum_{i=1}^n s_i(\theta_0),
\qquad
E_{\theta_0}[s_i(\theta_0)]=0,
\quad\operatorname{Var}_{\theta_0}[s_i(\theta_0)]=I(\theta_0).
$$

- 独立同分布で有限分散なので、中心極限定理を適用する。

$$
\frac{\ell'(\theta_0)}{\sqrt{nI(\theta_0)}}
\xrightarrow{d}N(0,1)
\quad\Longrightarrow\quad
\frac{\ell'(\theta_0)}{\sqrt n}
\xrightarrow{d}N(0,I(\theta_0)).
$$

- 後で推定誤差を表す比の、**分子の極限**として使う。''',
    refs=['appendix-score-fisher','appendix-mle-normal'])

add('appendix-score-mvt', 'A6　スコアに平均値の定理を使う',
    'ℓ′を一つの関数として扱うと、ℓ″を中間点で評価する等式が得られる。',
    r'''- $g(\theta)=\ell'(\theta)$ と置く。平均値の定理より、$\theta_0$ と $\hat\theta$ の間のある $\tilde\theta$ について、

$$
g(\hat\theta)-g(\theta_0)
=g'(\tilde\theta)(\hat\theta-\theta_0).
$$

- $g'=\ell''$ と、内部の最尤推定値での $\ell'(\hat\theta)=0$ を代入する。

$$
0=\ell'(\hat\theta)
=\ell'(\theta_0)+\ell''(\tilde\theta)(\hat\theta-\theta_0).
$$

- 中間点 $\tilde\theta$ を使うので、これは**近似ではなく等式**。一致性から $\tilde\theta\xrightarrow{p}\theta_0$ となる。''',
    notes='スコアgが区間で連続、内部で微分可能であるとして平均値の定理を適用する。hatθ=θ0のときはtildeθ=θ0として式を扱える。元資料の対数尤度の二次近似とは別に、ここではスコアを対象に平均値の定理を用いる。')

add('appendix-score-algebra', 'A7　推定誤差を比の形に整理する',
    '移項して割り算し、√nを掛け、最後に分子と分母をnで割る。',
    r'''- スコアの等式から、推定誤差を取り出す。

$$
\begin{aligned}
0&=\ell'(\theta_0)+\ell''(\tilde\theta)(\hat\theta-\theta_0),\\[5pt]
-\ell''(\tilde\theta)(\hat\theta-\theta_0)&=\ell'(\theta_0),\\[5pt]
\sqrt n(\hat\theta-\theta_0)
&=\frac{\sqrt n\,\ell'(\theta_0)}{-\ell''(\tilde\theta)}\\[5pt]
&=\frac{\ell'(\theta_0)/\sqrt n}{-\ell''(\tilde\theta)/n}.
\end{aligned}
$$

- 最後の行では分子・分母を $n$ で割った。$\sqrt n/n=1/\sqrt n$ を使っている。''',
    notes='分母−ℓ″(tildeθ)/nが正のI(θ0)へ確率収束するので、確率が1に近づく事象で分母は0ではなく、割り算ができる。')

add('appendix-mle-slutsky', 'A8　比の極限から漸近正規性を得る',
    '分子の正規極限を、分母が収束する正の定数Iで割る。',
    r'''- 分子には中心極限定理、分母には曲率の確率極限を使う。

$$
\frac{\ell'(\theta_0)}{\sqrt n}\xrightarrow{d}Z,
\quad Z\sim N(0,I(\theta_0)),
\qquad
-\frac1n\ell''(\tilde\theta)\xrightarrow{p}I(\theta_0)>0.
$$

- スルツキーの定理から、比は $Z/I(\theta_0)$ に分布収束する。

$$
\sqrt n(\hat\theta-\theta_0)
\xrightarrow{d}\frac{Z}{I(\theta_0)}
\sim N\!\left(0,\frac1{I(\theta_0)}\right).
$$

- 分散は $I(\theta_0)/I(\theta_0)^2=1/I(\theta_0)$。係数は $n$ ではなく **$\sqrt n$**。''')

add('appendix-taylor-close', 'A9　二次近似に必要な「近さ」',
    '帰無仮説の下で、最尤推定値とθ₀の差は確率的に $n^{-1/2}$ の規模になる。',
    r'''- 漸近正規性から、$\sqrt n(\hat\theta-\theta_0)$ は確率的に有界となる。

$$
\sqrt n(\hat\theta-\theta_0)\xrightarrow{d}
N\!\left(0,\frac1{I(\theta_0)}\right)
\quad\Longrightarrow\quad
\hat\theta-\theta_0=O_p(n^{-1/2})\xrightarrow{p}0.
$$

- $O_p(n^{-1/2})$ は、差に $\sqrt n$ を掛けた量が確率的に有界、という意味。

- 二次展開の一次項は $\ell'(\hat\theta)=0$ により消える。**剰余項 $r_n$** は次ページで扱う。

$$
\ell(\theta_0)=\ell(\hat\theta)
+\frac12\ell''(\hat\theta)(\theta_0-\hat\theta)^2+r_n.
$$''',
    notes='近さは帰無仮説と正則な漸近正規性から導かれる。二次展開の一次項はℓ′(hatθ)=0により消える。Opとopを区別し、ここで剰余項をまだ0とは置かない。')

add('appendix-taylor-remainder', 'A10　二次近似の剰余項を制御する',
    '三階微分が近傍で $O_p(n)$ なら、三次の剰余項は確率的に0へ近づく。',
    r"""- 三次までのテイラーの定理より、$\theta_0$ と $\hat\theta$ の間のある $\xi_n$ について、

$$
r_n=\frac16\ell'''(\xi_n)(\theta_0-\hat\theta)^3.
$$

- 十分条件として、$\theta_0$ の近傍 $U$ で三階微分の大きさを制御する。

$$
\sup_{\theta\in U}|\ell'''(\theta)|=O_p(n),
\quad\hat\theta-\theta_0=O_p(n^{-1/2})
\quad\Longrightarrow\quad
r_n=O_p(n^{-1/2})=o_p(1).
$$

- $o_p(1)$ は確率的に0に近づく項。そのため、対数尤度の二次近似を漸近的に正当化できる。""",
    notes='この三階微分による制御は十分条件の一例であり、最小限の必要条件ではない。1観測の三階微分に近傍で可積分な包絡関数があれば、i.i.d.の和をOp(n)で制御できる。hatθとθ0の間のξ_nがUに入る確率は1へ近づく。')

add('appendix-wilks-connection', 'A11　本編への接続：カイ二乗極限',
    '曲率の極限と推定誤差の正規極限を、尤度比の二次展開に代入する。',
    r'''- 点帰無仮説では $\Lambda=L(\theta_0\mid\boldsymbol X)/L(\hat\theta\mid\boldsymbol X)$。二次展開から、

$$
-2\log\Lambda
=\frac{-\ell''(\hat\theta)}{nI(\theta_0)}
\left\{\sqrt{nI(\theta_0)}(\hat\theta-\theta_0)\right\}^2+o_p(1).
$$

- 曲率の比は1に近づき、標準化した推定誤差の二乗は自由度1のカイ二乗分布に収束する。

$$
\frac{-\ell''(\hat\theta)}{nI(\theta_0)}\xrightarrow{p}1,
\qquad
\left\{\sqrt{nI(\theta_0)}(\hat\theta-\theta_0)\right\}^2
\xrightarrow{d}\chi^2_1.
$$

$$
\Longrightarrow\quad -2\log\Lambda\xrightarrow{d}\chi^2_1.
$$''',
    notes='前の二次展開から−2logΛ＝−ℓ″(hatθ)(hatθ−θ0)²−2r_n。−2r_n＝op(1)としてまとめる。正規変数の二乗の極限には連続写像定理、積とop(1)の組み合わせにはスルツキーの定理を用いる。1次元の点帰無仮説についての結論。')

assert len(deck['slides']) == 65
assert deck['slides'][:53] == original['slides']
assert len({s['id'] for s in deck['slides']}) == 65
data = json.dumps(deck, ensure_ascii=False, indent=2).replace('<', r'\u003c')
result = html[:match.start(2)] + '\n' + data + '\n' + html[match.end(2):]

def replace_exact(old, new):
    global result
    assert result.count(old) == 1, old[:100]
    result = result.replace(old, new)

# Keep the original 53-page main deck and its numbering, while allowing Next
# to continue from its last page into the appended section.
replace_exact("else if(p+dir>=0&&p+dir<indices.length)go(indices[p+dir]);",
              "else if(p+dir>=0&&p+dir<indices.length)go(indices[p+dir]);\n else if(dir>0&&current+1<deck.slides.length)go(current+1);")
replace_exact("$('next').disabled=pos===main.length-1&&!s.appendix;",
              "$('next').disabled=current===deck.slides.length-1;")
replace_exact("next=deck.slides[pos>=0?main[pos+1]:current+1];",
              "next=deck.slides[pos>=0?(main[pos+1]??current+1):current+1];")
replace_exact("filter(([s])=>['title','agenda'].includes(s.role))",
              "filter(([s])=>!s.appendix&&['title','agenda'].includes(s.role))")
replace_exact("['資料の記述についての質問',deck.slides.map((s,i)=>[s,i]).filter(([s])=>s.appendix)]",
              "['Appendix',deck.slides.map((s,i)=>[s,i]).filter(([s])=>s.appendix)]")
replace_exact("s.appendix?(s.theme==='question'?'質問 ':'復習 ')+deck.slides.filter((x,j)=>x.appendix&&j<=i).length",
              "s.appendix?'Appendix '+deck.slides.filter((x,j)=>x.appendix&&x.role!=='title'&&j<=i).length")
replace_exact("s.appendix?`${s.theme==='question'?'質問':'補足'} ${deck.slides.filter((x,i)=>x.appendix&&i<=current).length}`",
              "s.appendix?(s.role==='title'?'Appendix':`Appendix ${deck.slides.filter((x,i)=>x.appendix&&x.role!=='title'&&i<=current).length}`)")
replace_exact("s.appendix?(s.theme==='question'?'質問':'復習'):String(mainIndices().indexOf(i)+1)",
              "s.appendix?'Appendix':String(mainIndices().indexOf(i)+1)")

target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(result, encoding='utf-8')
print(target)
print('Unchanged original pages:',len(original['slides']))
print('Appended pages:',len(deck['slides'])-len(original['slides']))
