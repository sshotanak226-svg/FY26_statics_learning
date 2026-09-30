
[[確率分布の関係性の目次]]

> [!note] この追記部分の資料の扱い
> 数学的な定義・確率関数・平均・分散は元PDFの記述と、NIST・Encyclopedia of Mathematics・SciPy などの標準資料で照合している。
> 「歴史的経緯」は人物名や年代を並べるのではなく、**それまでの確率モデルでは何が答えられず、どんな問いを扱うために次の分布が必要になるのか**という発展の流れを中心に説明する。
> ここでいう「歴史」は厳密な発明史ではなく、確率分布どうしの理論的な発展関係を学ぶための説明である。実際の発明順序を根拠なく推測することはしない。
> 各分布では、まず「1からこの分布を数式で構成する」で数学的導出を完結させる。その次の「歴史的経緯」では導出を繰り返さず、その分布が必要になった問題意識・既存モデルでは不足した点・後に重要になった理由だけを補う。その後に「前述分布との関係 → 使用条件 → 総和が1 → 平均 → 分散 → 重要な性質」の証明へ進む。


ここからは難しい話は

にまとめていくが、難しすぎるので勉強会では触れません。あくまで自分の備忘録として追加しているので、読んでもわからないと思う

# 確率変数

標本から必要な情報を取り出す対応を確率変数という。（[より詳しい条件](可測関数.md)）
今僕たちが計算したい対象は「サイコロを投げたら1が出た」という現象か？
違う、「サイコロを投げたら"1"が出る」という１という値が欲しい。この考え方が確率変数である。

こうなっていいことって何やねん。A,確率変数によって意味のある数字として標本を表現できる。
ちょっと数式的な描き方すると確率変数Xは
$$
\forall \omega\in\Omega,X(\omega)\in \mathbb{R}
$$
であるが、$\omega$何かは省略されてXで描画される。

確率変数によって標本という概念的なものから扱いやすい数値として定義できた。こっからは事象につなげていくことで確率変数を使用して確率を扱っていく

確率変数で確率を表すときのルールとして
$$P(X=x_i):=P(\{\omega \in \Omega|X(\omega)=x_i\})$$
こうなった場合$P(X=x_i)$は集合を扱う測度ではなく数値を入力に持つ関数として扱えるので$p(x_i)=P(X=x_i)$は確率関数と呼ぶことになる。

確率変数は$\{X(\omega)|\omega \in \Omega\}$と表した時の集合が有限もしくは可算無限のとき離散確率変数といい、非可算無限の場合は連続確率変数という

# 分布関数

分布関数とは、確率変数が$a\in R$以下になる確率値を出力する関数F
$$
F(a)=P(X\le a)
$$
>[!Tips] 分布関数とかいらんでしょ
>実は理論としては重要、どのような分布でも必ず存在するから。
>確率変数Xから誘導される確率測度(像測度)は以下のように定義できる量$\mu$である
>ボレル集合族$\mathcal{B}_ｄ$の集合$B\in \mathcal{B}_d$について
>$$\mu(B)=P(X\in B)=P(X^{-1})=P(\{\omega \in \Omega |X(\omega)\in B\})$$
>このような確率測度はどのような確率空間でも定義できる
>（実はカントール分布という、連続でも離散でもない分布が登場し、その場合この像測度は定義できるが確率関数も密度も定義できないというようなものの解析に必要になる。）
>いま、確率変数を用いて操作している理由の一つが関数として確率を扱いたいから、この像測度を関数として扱えるようにしたのが分布関数である。
>$$F(x)=\mu([-\infty,x])$$

# 期待値と分散

>[!Definition] 定義2.1　離散確率変数の期待値
>$\sum_i^\infty |x_i|p(x_i)<\infty$のとき期待値を$E[X]=\sum_i^\infty x_ip(x_i)$とあらわす。任意の関数ｇについて期待値を取る際は、$\sum_i^\infty |g(x_i)|p(x_i)<\infty$のとき$E[g(X)]=\sum_i^\infty g(x_i)p(x_i)$とあらわす。

>[!tips] $\sum_i^\infty |x_i|p(x_i)<\infty$（可積分性）がなんで必要なん？
>実はこれは「期待値を有限な数値として扱うための」かなりきつい条件である。（このように設定してしまうと無限は期待値として設定してはいけない）
>無限を扱いたい場合(例えば極限で)確率論では、$X^+$(Xが正の値はそのまま取り出し、負は全部０) or $X^-$(負の値は正として取り出し、あとは０)が期待値で有限であれば良いとされることがある。（期待値を計算するうえで互いを相殺し合う２つの内どちらかが有限であれば良い）
>$X=X^+-X^-$という関係性から
>$$E[X]=E[X^+]-E[X^-]$$
>どちらかが無限で残り有限なら期待値$\infty$として扱える。（こうすることで期待値の発散方向などの議論が行える）
>しかし、$X^+,X^-$の両方が$\infty$の場合、$E[X]=\infty-\infty$になり、相殺のさせかた次第で$-\infty,\infty,0$にでもなってしまうため期待値を定義できない。
>この最も有名な分布がコーシー分布である。コーシー分布とは正規分布のように対称的な釣鐘状の分布であるが$X=\infty$まで確率が存在する裾の長い分布である。そのため負でも正でも無限になるので、期待値を定義できないので中央値や別の値で代用せなあかんくなる。

>[!Definition] 定義2.2 　分散
>期待値が定義できるとき、$\mu$または確率変数を明示して$\mu_X$で表す。分散$\sigma^2,\sigma^2_X,var(X)$は
>$$E[(X-\mu)^2]=\sum_i^\infty (x_i-\mu)^2p(x_i)$$
>この値の平方根は標準偏差という


（どうせ標準偏差で平方根取るなら2乗じゃなく絶対値使えばいいのに、、、絶対値は良くない。絶対値は微分できないし扱いづらい関数であるから)

分散の計算方法で有名なものがいくつかあるので紹介
1. $Var(X)=E[X^2]-(E[X])^2$:これは$E[(X-\mu)^2]=E[X^2-2X\mu;\mu^2]=E[X^2]-2E[X]\mu+\mu^2=E[X^2]-2\mu^2+\mu^2$より
2. $E[X(X-1)]=E[X^2]-E[X]$、これに$E[X]^2-E[X]$を引けば導出可能。平均は出せることが多くかつ組み合わせで表現できる分布に反してはX!などを含みやすく$E[X(X-1)]$という形を自然に作りやすいのでよく使用される


# ベルヌーイ分布

ある事象Aについてそれが起きるか起こらないかを表現する分布である。確率変数は0,1の2値の値しか取らないものとして、Aが起きる場合X=1,起きない場合はX=0とする。しっかり書くなら
$$
X(\omega)=1_{\omega \in A}
$$
p(X=1)=pとかけるときベルヌーイ分布は
$$
p(X=x)=p(x)=p^x(1-p)^{1-x}
$$
またベルヌーイ分布で表現できるような、ある施行に対してAが起きたか起きないかを観測する施行をベルヌーイ試行という。


## 1からこの分布を作る：事象を0/1へ変換する

ベルヌーイ分布は「公式を暗記する」より、**1つの事象を指示変数に変換する**ところから作ると理解しやすい。

確率空間 $(\Omega,\mathcal F,P)$ と事象 $A\in\mathcal F$ を考え、

$$
p:=P(A)
$$

とおく。補集合 $A^c$ について、$A\cap A^c=\varnothing$ かつ $A\cup A^c=\Omega$ なので、確率の加法性から

$$
\begin{aligned}
1
&=P(\Omega)\\
&=P(A\cup A^c)\\
&=P(A)+P(A^c)\\
&=p+P(A^c)
\end{aligned}
$$

である。したがって、

$$
\begin{aligned}
P(A^c)
&=1-p
\end{aligned}
$$

となる。

ここで、事象 $A$ が起きたかどうかだけを取り出す確率変数

$$
X(\omega):=
\begin{cases}
1 & (\omega\in A)\\
0 & (\omega\notin A)
\end{cases}
$$

を定義する。これは指示変数 $X=1_A$ である。

すると、

$$
\begin{aligned}
P(X=1)
&=P(\{\omega\in\Omega\mid X(\omega)=1\})\\
&=P(A)\\
&=p
\end{aligned}
$$

であり、

$$
\begin{aligned}
P(X=0)
&=P(\{\omega\in\Omega\mid X(\omega)=0\})\\
&=P(A^c)\\
&=1-p
\end{aligned}
$$

となる。

$X$ が取りうる値は $0,1$ だけなので、この2式を1本にまとめると

$$
P(X=x)=p^x(1-p)^{1-x},\qquad x\in\{0,1\}
$$

となる。実際、

$$
\begin{aligned}
x=1:\quad p^1(1-p)^0&=p,\\
x=0:\quad p^0(1-p)^1&=1-p
\end{aligned}
$$

である。

## 歴史的経緯：1を補う「なぜ必要になったか」

ベルヌーイ分布そのものの式は前節で作ったので、ここでは**なぜ「1回の二値試行」を独立したモデルとして切り出す必要があったのか**だけを見る。

確率論の初期には、賭けや偶然に左右される判断を「どちらがどれくらい起こりやすいか」と数量化する問題が中心にあった。しかし、単に1回の勝敗の確率を計算するだけでは、現実の観測から未知の確率について考えることはできない。そこで重要になったのが、**同じ条件の試行を繰り返し、1回1回の成否を共通の単位として扱う**という考え方である。

この「1回分」を切り出しておけば、その後に

- 成功回数を数える
- 成功割合を見る
- 成功するまで待つ

といった別の問題へ同じ部品を使い回せる。実際、Bernoulli の反復試行の研究では、未知の成功確率と多数回の試行で観測される成功割合との関係が問題になり、後の大数の法則につながった。

したがってベルヌーイ分布の重要性は、単に「0と1を取る簡単な分布」であることではなく、**反復試行を数学的に組み立てるための最小単位を与えたこと**にある。

> [!source] 歴史的背景の根拠
> - MacTutor History of Mathematics, “Jacob Bernoulli”: https://mathshistory.st-andrews.ac.uk/Biographies/Bernoulli_Jacob/
> - MacTutor, Bernoulli と大数の法則に関する解説: https://mathshistory.st-andrews.ac.uk/Extras/Talagrand_awards/
## 前述の内容との関係

ここまでに導入した「事象を確率変数で数値化する」という操作の最も単純な例がベルヌーイ分布である。

$$
A
\longrightarrow
1_A
\longrightarrow
\{0,1\}\text{上の確率分布}
$$

という流れになっている。

また、この1個のベルヌーイ確率変数が以降の分布の基本部品になる。独立なベルヌーイ変数を固定回数だけ足せば2項分布になり、最初の成功まで待てば幾何分布になる。

## 現場ではいつ使えるか

1回の観測結果が本質的に2択であり、そのどちらかを $1/0$ で符号化できるときに使う。例えば「検査に合格したか」「部品が不良だったか」「広告がクリックされたか」のような**1回の二値観測**である。

重要なのは、ベルヌーイ分布は1回分の試行を表すという点である。同じ条件の試行を $n$ 回行い、その成功回数を知りたいなら2項分布へ進む。

> [!source] 根拠資料
> - Encyclopedia of Mathematics, “Bernoulli theorem”: https://encyclopediaofmath.org/wiki/Bernoulli_theorem
> - Encyclopedia of Mathematics, “Bernoulli trials”: https://encyclopediaofmath.org/wiki/Bernoulli_scheme
> - OpenStax, “Binomial Distribution”: https://openstax.org/books/introductory-statistics-2e/pages/4-3-binomial-distribution

分布に重要な値として、まず「本当に確率分布になっているか」、つまり確率の総和が1になることを確認しておく。以降の分布でも同じ順番で確認する。

## 確率の総和が1になること

ベルヌーイ分布では $X$ が取りうる値は $0,1$ だけなので、

$$
\begin{aligned}
\sum_{x\in\{0,1\}}p(x)
&=p(0)+p(1)\\
&=p^0(1-p)^{1-0}+p^1(1-p)^{1-1}\\
&=(1-p)+p\\
&=1
\end{aligned}
$$

となる。したがって、ベルヌーイ分布の確率関数は確率の総和が1になる。

## 平均

期待値の定義から、取りうる値をすべて足せばよい。

$$
\begin{aligned}
E[X]
&=\sum_{x\in\{0,1\}}xp(x)\\
&=0\cdot p(0)+1\cdot p(1)\\
&=0\cdot(1-p)+1\cdot p\\
&=p
\end{aligned}
$$

したがって、

$$
E[X]=p
$$

である。

## 分散

まず $E[X^2]$ を計算する。

$$
\begin{aligned}
E[X^2]
&=\sum_{x\in\{0,1\}}x^2p(x)\\
&=0^2(1-p)+1^2p\\
&=p
\end{aligned}
$$

よって、分散の公式 $Var(X)=E[X^2]-(E[X])^2$ を使うと、

$$
\begin{aligned}
Var(X)
&=E[X^2]-(E[X])^2\\
&=p-p^2\\
&=p(1-p)
\end{aligned}
$$

となる。

ここから先では式を短くするために

$$
q:=1-p
$$

と書くことがある。

---

# 2項分布

ベルヌーイ試行を独立に $n$ 回繰り返し、そのうち「成功」した回数を確率変数 $X$ とする。このとき $X$ は

$$
X\in\{0,1,2,\ldots,n\}
$$

の値を取り、この分布を2項分布という。

$$
X\sim Bin(n,p)
$$

と書く。


## 1からこの分布を作る：ベルヌーイ分布を固定回数だけ足す

$i$ 回目のベルヌーイ試行を

$$
X_i=
\begin{cases}
1 & (i\text{回目が成功})\\
0 & (i\text{回目が失敗})
\end{cases}
$$

とし、

$$
P(X_i=1)=p,\qquad P(X_i=0)=q:=1-p
$$

とする。さらに $X_1,\ldots,X_n$ は独立であると仮定する。

成功回数は

$$
X:=X_1+X_2+\cdots+X_n
$$

である。$X=k$ とは、$n$ 個の $X_i$ のうちちょうど $k$ 個が1で、残り $n-k$ 個が0になることである。

成功する位置を1通り固定すると、独立性からその並びの確率は

$$
\begin{aligned}
&p\times\cdots\times p\times q\times\cdots\times q\\
&=p^kq^{n-k}
\end{aligned}
$$

となる。

一方、$n$ 箇所から成功する $k$ 箇所を選ぶ方法は

$$
\binom nk
$$

通りある。それぞれ異なる成功位置を表す事象は互いに排反なので、確率を足し合わせると

$$
\begin{aligned}
P(X=k)
&=\underbrace{p^kq^{n-k}+\cdots+p^kq^{n-k}}_{\binom nk\text{個}}\\
&=\binom nkp^kq^{n-k}
\end{aligned}
$$

となる。これが2項分布の確率関数である。

## 歴史的経緯：1を補う「なぜ必要になったか」

前節ではベルヌーイ試行を $n$ 回並べれば2項分布の式が出ることを示した。ここで重要なのは、**なぜ「並び方」ではなく「成功した個数」だけを取り出す分布が必要だったのか**である。

確率論の初期にはゲームの勝敗やくじのような反復試行が主要な問題だったが、試行を何度も行うようになると、「この並びが起きる確率」よりも、**一定回数の中で目的の事象が何回起きるか**の方が重要になる。さらに、観測された成功割合から元の成功確率について考えるには、成功回数全体のばらつきを扱う必要がある。

このため2項分布は、単発の確率計算と「多数回観測したときの頻度」の間をつなぐ役割を持つようになった。Bernoulli の反復試行の研究でも、試行回数が増えたとき成功割合が真の確率へ近づくことが主要な問題となっており、2項型の成功回数モデルはその土台になっている。

つまり、2項分布が必要になった背景は、**1回の成否を知るだけではなく、反復した結果から頻度や確率について議論したい**という要求にある。前節の数式的構成は、この問題意識を正確な確率分布にしたものと考えればよい。

> [!source] 歴史的背景の根拠
> - MacTutor, Jacob Bernoulli の反復試行と大数の法則の解説: https://mathshistory.st-andrews.ac.uk/Extras/Talagrand_awards/
> - MacTutor, Jacob Bernoulli / *Ars Conjectandi*: https://mathshistory.st-andrews.ac.uk/Strick/Bernoulli_Jacob.pdf
## 前述の分布との関係

ベルヌーイ分布との関係は

$$
X_i\sim Bernoulli(p)
$$

を独立に $n$ 個用意し、

$$
X=\sum_{i=1}^{n}X_i
$$

と置くことに尽きる。このとき

$$
X\sim Bin(n,p)
$$

となる。

特に $n=1$ なら

$$
Bin(1,p)=Bernoulli(p)
$$

なので、ベルヌーイ分布は2項分布の特殊例でもある。

## 現場ではいつ使えるか

2項分布を使うには、少なくとも次のモデル化が妥当である必要がある。

- 試行回数 $n$ があらかじめ固定されている。
- 各試行は成功・失敗の2値で表せる。
- 各試行の成功確率が同じ $p$ である。
- 試行同士を独立とみなせる。

例えば、一定条件で作られた製品を独立に $n$ 個検査し、不良品数を数える状況は典型例である。NIST でも不適合品数のモデルとして2項分布を用い、品質管理の $p$ 管理図につなげている。

逆に、有限個の集団から**非復元抽出**すると試行は独立でなくなるため、原則として後述する超幾何分布が対応する。

> [!source] 根拠資料
> - NIST/SEMATECH e-Handbook, “Binomial Distribution”: https://itl.nist.gov/div898/handbook/eda/section3/eda366i.htm
> - NIST/SEMATECH e-Handbook, “Proportions Control Charts”: https://itl.nist.gov/div898/handbook/pmc/section3/pmc332.htm
> - Encyclopedia of Mathematics, “Bernoulli trials”: https://encyclopediaofmath.org/wiki/Bernoulli_scheme
> - Encyclopedia of Mathematics, “Binomial distribution”: https://encyclopediaofmath.org/wiki/Binomial_distribution

## 確率関数の導出をもう一度、組合せから確認する

$n$ 回の試行のうち、成功がちょうど $k$ 回、失敗が $n-k$ 回起きたとする。

まず、成功・失敗の並び方を1つ固定する。例えば

$$
\underbrace{\circ\ \circ\ \times\ \circ\ \times\ \cdots}_{n\text{回}}
$$

のように成功する場所が完全に決まっているとする。各試行は独立なので、この1つの並びが起きる確率は

$$
p^kq^{n-k}
$$

である。

一方、$n$ 個の場所から成功する $k$ 個の場所を選ぶ方法は

$$
\binom{n}{k}=\frac{n!}{k!(n-k)!}
$$

通りある。したがって、成功回数がちょうど $k$ 回になる確率は

$$
P(X=k)=\binom{n}{k}p^kq^{n-k},\qquad k=0,1,\ldots,n
$$

となる。

## 確率の総和が1になること

確率関数をすべて足すと、

$$
\begin{aligned}
\sum_{k=0}^{n}P(X=k)
&=\sum_{k=0}^{n}\binom{n}{k}p^kq^{n-k}\\
&=(p+q)^n
\end{aligned}
$$

となる。最後の等号は2項定理そのものである。

ここで $q=1-p$ なので、

$$
\begin{aligned}
(p+q)^n
&=(p+1-p)^n\\
&=1^n\\
&=1
\end{aligned}
$$

したがって、

$$
\sum_{k=0}^{n}P(X=k)=1
$$

が確かめられた。

## 平均

期待値の定義から、

$$
E[X]=\sum_{k=0}^{n}k\binom{n}{k}p^kq^{n-k}
$$

である。$k=0$ の項は $0$ なので、

$$
E[X]=\sum_{k=1}^{n}k\binom{n}{k}p^kq^{n-k}
$$

と書ける。

ここで、係数の部分を変形する。

$$
\begin{aligned}
k\binom{n}{k}
&=k\frac{n!}{k!(n-k)!}\\
&=\frac{k\,n!}{k(k-1)!(n-k)!}\\
&=\frac{n!}{(k-1)!(n-k)!}\\
&=n\frac{(n-1)!}{(k-1)!(n-k)!}\\
&=n\binom{n-1}{k-1}
\end{aligned}
$$

したがって、

$$
\begin{aligned}
E[X]
&=\sum_{k=1}^{n}n\binom{n-1}{k-1}p^kq^{n-k}\\
&=np\sum_{k=1}^{n}\binom{n-1}{k-1}p^{k-1}q^{n-k}
\end{aligned}
$$

となる。

ここで

$$
j=k-1
$$

とおく。$k=1$ のとき $j=0$、$k=n$ のとき $j=n-1$ であり、さらに

$$
n-k=n-(j+1)=n-1-j
$$

なので、

$$
\begin{aligned}
E[X]
&=np\sum_{j=0}^{n-1}\binom{n-1}{j}p^jq^{n-1-j}\\
&=np(p+q)^{n-1}\\
&=np\cdot1^{n-1}\\
&=np
\end{aligned}
$$

となる。

したがって、2項分布の平均は

$$
E[X]=np
$$

である。

## 分散

2項分布では $E[X^2]$ を直接計算するより、まず

$$
E[X(X-1)]
$$

を計算した方が式がきれいになる。

期待値の定義から、

$$
E[X(X-1)]
=\sum_{k=0}^{n}k(k-1)\binom{n}{k}p^kq^{n-k}
$$

である。$k=0,1$ の項は $0$ なので、

$$
E[X(X-1)]
=\sum_{k=2}^{n}k(k-1)\binom{n}{k}p^kq^{n-k}
$$

となる。

係数を丁寧に変形すると、

$$
\begin{aligned}
k(k-1)\binom{n}{k}
&=k(k-1)\frac{n!}{k!(n-k)!}\\
&=k(k-1)\frac{n!}{k(k-1)(k-2)!(n-k)!}\\
&=\frac{n!}{(k-2)!(n-k)!}\\
&=n(n-1)\frac{(n-2)!}{(k-2)!(n-k)!}\\
&=n(n-1)\binom{n-2}{k-2}
\end{aligned}
$$

となる。これを代入すると、

$$
\begin{aligned}
E[X(X-1)]
&=\sum_{k=2}^{n}n(n-1)\binom{n-2}{k-2}p^kq^{n-k}\\
&=n(n-1)p^2\sum_{k=2}^{n}\binom{n-2}{k-2}p^{k-2}q^{n-k}
\end{aligned}
$$

である。

ここで

$$
j=k-2
$$

とおく。$k=2$ のとき $j=0$、$k=n$ のとき $j=n-2$ であり、

$$
n-k=n-(j+2)=n-2-j
$$

なので、

$$
\begin{aligned}
E[X(X-1)]
&=n(n-1)p^2\sum_{j=0}^{n-2}\binom{n-2}{j}p^jq^{n-2-j}\\
&=n(n-1)p^2(p+q)^{n-2}\\
&=n(n-1)p^2
\end{aligned}
$$

となる。

また、

$$
X^2=X(X-1)+X
$$

なので、期待値を取れば

$$
\begin{aligned}
E[X^2]
&=E[X(X-1)]+E[X]\\
&=n(n-1)p^2+np
\end{aligned}
$$

となる。

したがって、

$$
\begin{aligned}
Var(X)
&=E[X^2]-(E[X])^2\\
&=n(n-1)p^2+np-(np)^2\\
&=(n^2-n)p^2+np-n^2p^2\\
&=n^2p^2-np^2+np-n^2p^2\\
&=np-np^2\\
&=np(1-p)\\
&=npq
\end{aligned}
$$

となる。

したがって、2項分布では

$$
E[X]=np,\qquad Var(X)=np(1-p)
$$

である。


---

# 幾何分布


## 1からこの分布を作る：最初の成功まで待つ

独立同分布なベルヌーイ確率変数

$$
B_1,B_2,B_3,\ldots
$$

を考え、

$$
P(B_i=1)=p,\qquad P(B_i=0)=q:=1-p
$$

とする。このノートでは「最初の成功が起こる前の失敗回数」を数えるので、

$$
X:=\min\{j\mid B_j=1\}-1
$$

と定義する。

$X=k$ であるための必要十分条件は

$$
B_1=0,\ B_2=0,\ \ldots,\ B_k=0,\ B_{k+1}=1
$$

である。したがって、

$$
\begin{aligned}
P(X=k)
&=P(B_1=0,\ldots,B_k=0,B_{k+1}=1)\\
&=P(B_1=0)\cdots P(B_k=0)P(B_{k+1}=1)\\
&=\underbrace{q\times\cdots\times q}_{k\text{個}}\times p\\
&=q^kp
\end{aligned}
$$

となる。2行目で使ったのが各試行の独立性である。

## 歴史的経緯：1を補う「なぜ必要になったか」

前節では「最初の成功までの失敗回数」を数えると幾何分布が得られることを示した。歴史的な背景として重要なのは、**確率論の問題が必ずしも「最初に試行回数を決める問題」だけではなかった**ことである。

ゲームや反復試行では、「あと何回行えば目的の結果が初めて出るのか」「目的の結果が出るまで続けると、どれくらい待つのか」という**停止条件を持つ問題**も自然に現れる。この種の問題では、試行回数を先に固定する2項分布だけでは問いの形に直接対応できない。

幾何分布に相当する考え方は確率論のかなり初期から現れており、MacTutor が紹介する数学用語史では、1654年の Fermat と Pascal の議論の一部を幾何分布に基づく議論とみなす数学史研究が紹介されている。一方で “geometric distribution” という現在の名称自体はずっと後に定着した。

したがってこの分布は、**固定された回数の中の成功数だけでなく、「最初に成功するまで」というランダムな待ち時間も確率論の対象にする必要があった**という流れの中で理解するとよい。

> [!source] 歴史的背景の根拠
> - MacTutor, “Earliest Known Uses ... (G)”: https://mathshistory.st-andrews.ac.uk/Miller/mathword/g/
> - Encyclopedia of Mathematics, “Geometric distribution”: https://encyclopediaofmath.org/wiki/Geometric_distribution
## 前述の分布との関係

ベルヌーイ分布が「1回の成否」を表したのに対し、幾何分布はベルヌーイ試行を

$$
失敗,\ldots,失敗,成功
$$

となるまで反復したときの**停止までの待ち時間**を表す。

同じベルヌーイ試行からでも、

$$
\text{固定回数の成功数}\longrightarrow Bin(n,p)
$$

を作るのか、

$$
\text{最初の成功までの失敗数}\longrightarrow Geo(p)
$$

を作るのかで分布が変わる。

## 現場ではいつ使えるか

「成功するまで同じ試行を繰り返す」状況で、各試行の成功確率 $p$ が変わらず、試行を独立とみなせるときに使える。例えば通信の再送を成功するまで繰り返す回数、一定条件の探索で最初に目的物が見つかるまでの失敗回数などを、この仮定の下でモデル化できる。

ただし成功確率が試行ごとに変化する場合や、過去の失敗が次の成功確率を変える場合には幾何分布の仮定は崩れる。


> [!source] 根拠資料
> - Encyclopedia of Mathematics, “Geometric distribution”: https://encyclopediaofmath.org/wiki/Geometric_distribution
> - SciPy, `scipy.stats.geom`: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.geom.html
> - OpenStax, “Geometric Distribution”: https://openstax.org/books/statistics/pages/4-4-geometric-distribution-optional


## 確率の総和が1になること

$0<p\le1$ とする。このとき $0\le q<1$ なので、無限等比級数（幾何級数）が収束する。

$$
\begin{aligned}
\sum_{k=0}^{\infty}P(X=k)
&=\sum_{k=0}^{\infty}pq^k\\
&=p\sum_{k=0}^{\infty}q^k\\
&=p\frac{1}{1-q}\\
&=p\frac{1}{1-(1-p)}\\
&=p\frac{1}{p}\\
&=1
\end{aligned}
$$

したがって、幾何分布の確率の総和は1になる。

## 平均

まず、期待値の定義にそのまま幾何分布の確率関数を代入して、**これから何を計算しなければならないのか**を確認する。

$$
\begin{aligned}
E[X]
&=\sum_{k=0}^{\infty}kP(X=k)\\
&=\sum_{k=0}^{\infty}kpq^k\\
&=p\sum_{k=0}^{\infty}kq^k
\end{aligned}
$$

したがって、平均を求める問題は

$$
\sum_{k=0}^{\infty}kq^k
$$

を計算する問題に帰着する。

ここで困るのは、すでに知っている無限等比級数

$$
\sum_{k=0}^{\infty}q^k
$$

には係数 $k$ が付いていないことである。

では、**既知の $q^k$ から $kq^k$ を作るには、どのような演算をすればよいか**を考える。

$q^k$ を $q$ で微分すると、べき乗の微分公式から

$$
\frac{d}{dq}q^k=kq^{k-1}
$$

となる。

ここで重要なのは、微分によって指数として隠れていた $k$ が

$$
q^k
\longrightarrow
kq^{k-1}
$$

のように**係数として前に出てくる**ことである。

期待値で欲しいのは $kq^k$ なので、さらに $q$ を掛ければ

$$
\begin{aligned}
q\frac{d}{dq}q^k
&=q\left(kq^{k-1}\right)\\
&=kq^k
\end{aligned}
$$

となり、まさに欲しかった形が得られる。

つまり、ここで微分を使うのは単なる計算テクニックではなく、

$$
\boxed{
q^k\text{ の指数 }k\text{ を係数として取り出したい}
}
$$

という目的に対して、

$$
\boxed{
q\frac{d}{dq}
}
$$

という演算が

$$
q\frac{d}{dq}q^k=kq^k
$$

を満たすからである。

したがって、

$$
\sum_{k=0}^{\infty}q^k
$$

という計算済みの級数に $q\dfrac{d}{dq}$ を作用させれば、

$$
\sum_{k=0}^{\infty}kq^k
$$

を作れるはずだ、という方針に自然に行き着く。

そこで無限等比級数

$$
S(q):=\sum_{k=0}^{\infty}q^k=\frac{1}{1-q}
$$

を考える。


ここから実際に計算する。

両辺を $q$ で微分すると、

$$
\begin{aligned}
S'(q)
&=\frac{d}{dq}\sum_{k=0}^{\infty}q^k\\
&=\sum_{k=1}^{\infty}kq^{k-1}
\end{aligned}
$$

であり、一方右辺は

$$
\begin{aligned}
\frac{d}{dq}\frac{1}{1-q}
&=\frac{d}{dq}(1-q)^{-1}\\
&=-(1-q)^{-2}\cdot(-1)\\
&=(1-q)^{-2}\\
&=\frac{1}{(1-q)^2}
\end{aligned}
$$

となる。よって、

$$
\sum_{k=1}^{\infty}kq^{k-1}=\frac{1}{(1-q)^2}
$$

である。

両辺に $q$ を掛けると、

$$
\sum_{k=1}^{\infty}kq^k=\frac{q}{(1-q)^2}
$$

となる。

したがって、

$$
\begin{aligned}
E[X]
&=\sum_{k=0}^{\infty}kP(X=k)\\
&=\sum_{k=0}^{\infty}kpq^k\\
&=p\sum_{k=1}^{\infty}kq^k\\
&=p\frac{q}{(1-q)^2}\\
&=p\frac{q}{p^2}\\
&=\frac{q}{p}
\end{aligned}
$$

となる。

したがって、

$$
E[X]=\frac{1-p}{p}=\frac{q}{p}
$$

である。
なんとなくこの様になるのは理解できる。なぜなら、$E[X]$は１回成功するまでに何回平均して失敗するかである、一回の施工にあたって成功と失敗がｐ：ｑで行われるんだから上記のような値になりうる
例えば、p=0.2である時、１っかい成功するまでに（0.8/0.2=）４回失敗していると考えられるでしょ。


## 分散

先ほどの

$$
S'(q)=\sum_{k=1}^{\infty}kq^{k-1}=\frac{1}{(1-q)^2}
$$

をもう1回微分する。

左辺は

$$
\frac{d}{dq}\sum_{k=1}^{\infty}kq^{k-1}
=\sum_{k=2}^{\infty}k(k-1)q^{k-2}
$$

である。

右辺は

$$
\begin{aligned}
\frac{d}{dq}(1-q)^{-2}
&=-2(1-q)^{-3}\cdot(-1)\\
&=2(1-q)^{-3}\\
&=\frac{2}{(1-q)^3}
\end{aligned}
$$

である。したがって、

$$
\sum_{k=2}^{\infty}k(k-1)q^{k-2}=\frac{2}{(1-q)^3}
$$

となる。

両辺に $pq^2$ を掛けると、

$$
\begin{aligned}
E[X(X-1)]
&=\sum_{k=0}^{\infty}k(k-1)pq^k\\
&=pq^2\sum_{k=2}^{\infty}k(k-1)q^{k-2}\\
&=pq^2\frac{2}{(1-q)^3}\\
&=pq^2\frac{2}{p^3}\\
&=\frac{2q^2}{p^2}
\end{aligned}
$$

となる。

ここで、

$$
X^2=X(X-1)+X
$$

なので、

$$
\begin{aligned}
E[X^2]
&=E[X(X-1)]+E[X]\\
&=\frac{2q^2}{p^2}+\frac{q}{p}
\end{aligned}
$$

である。よって、

$$
\begin{aligned}
Var(X)
&=E[X^2]-(E[X])^2\\
&=\frac{2q^2}{p^2}+\frac{q}{p}-\left(\frac{q}{p}\right)^2\\
&=\frac{2q^2}{p^2}+\frac{pq}{p^2}-\frac{q^2}{p^2}\\
&=\frac{q^2+pq}{p^2}\\
&=\frac{q(q+p)}{p^2}\\
&=\frac{q}{p^2}
\end{aligned}
$$

となる。最後に $p+q=1$ を使った。

したがって、幾何分布では

$$
E[X]=\frac{q}{p},\qquad Var(X)=\frac{q}{p^2}
$$

である。

## 尾確率と無記憶性

幾何分布の重要な特徴は**無記憶性**である。

まず $m$ 回以上失敗する確率を計算する。

$$
\begin{aligned}
P(X\ge m)
&=\sum_{k=m}^{\infty}pq^k\\
&=pq^m\sum_{j=0}^{\infty}q^j\\
&=pq^m\frac{1}{1-q}\\
&=pq^m\frac{1}{p}\\
&=q^m
\end{aligned}
$$

ここで2行目では $k=m+j$ と置き換えた。

したがって、分布関数も

$$
\begin{aligned}
P(X\le k)
&=1-P(X\ge k+1)\\
&=1-q^{k+1}
\end{aligned}
$$

と求められる。

次に、すでに $m$ 回失敗しているという条件の下で、さらに $n$ 回以上失敗する確率を計算する。

$$
\begin{aligned}
P(X\ge m+n\mid X\ge m)
&=\frac{P(X\ge m+n,\ X\ge m)}{P(X\ge m)}
\end{aligned}
$$

$X\ge m+n$ なら必ず $X\ge m$ なので、

$$
\{X\ge m+n\}\subseteq\{X\ge m\}
$$

であり、共通部分は

$$
\{X\ge m+n\}\cap\{X\ge m\}=\{X\ge m+n\}
$$

となる。したがって、

$$
\begin{aligned}
P(X\ge m+n\mid X\ge m)
&=\frac{P(X\ge m+n)}{P(X\ge m)}\\
&=\frac{q^{m+n}}{q^m}\\
&=q^n\\
&=P(X\ge n)
\end{aligned}
$$

となる。

つまり、「ここまで何回失敗したか」を知っても、その後の待ち時間の分布は変わらない。これを幾何分布の**無記憶性**という。


---

# 負の2項分布


## 1からこの分布を作る：$r$ 回目の成功まで待つ

幾何分布では最初の成功まで待った。これを「$r$ 回目の成功まで」に一般化する。

独立同分布なベルヌーイ試行を繰り返し、

$$
P(\text{成功})=p,\qquad P(\text{失敗})=q:=1-p
$$

とする。$r$ 回目の成功が起きるまでに観測された失敗回数を $X$ とする。

$X=k$ なら全試行回数は $r+k$ 回であり、最後の $(r+k)$ 回目は必ず成功である。最後の1回を除く最初の $r+k-1$ 回には、$r-1$ 回の成功と $k$ 回の失敗が入っている。

この並び方は

$$
\binom{r+k-1}{k}
$$

通りである。1つの並びの確率は独立性から

$$
\begin{aligned}
p^{r-1}q^k\times p
&=p^rq^k
\end{aligned}
$$

なので、

$$
P(X=k)=\binom{r+k-1}{k}p^rq^k,
\qquad k=0,1,2,\ldots
$$

となる。

## 歴史的経緯：1を補う「なぜ必要になったか」

前節では、最初の成功まで待つ幾何分布を「$r$ 回目の成功まで」へ広げると負の2項分布が得られることを示した。ここでは、**なぜその一般化が統計的にも必要になったのか**を見る。

現実の観測では「1回成功したら終了」とは限らず、一定数の成功が集まるまで観測を続ける設計がある。このように**得たい成功数を先に決め、必要な試行数や失敗数の方をランダムにする**考え方は、固定回数だけ観測する2項分布とは逆向きのサンプリングになる。これは現在では inverse binomial sampling と呼ばれる考え方につながっている。

さらに20世紀初頭には、酵母細胞の計数誤差や疾病への曝露後の死亡数など、単純な二値試行の教科書的な例を越えた**実際のカウントデータ**を記述する文脈でも負の2項型の分布が現れたことが記録されている。ここから、負の2項分布は待ち時間の分布としてだけでなく、後にはポアソン分布ではばらつきが小さすぎるカウントデータを扱うモデルとしても重要になった。

したがって負の2項分布が必要になった理由は、幾何分布を単に数式的に一般化したからだけではなく、**「一定数の成功を得るまで観測する問題」と「単純なポアソンモデルより大きなばらつきを持つ計数問題」の両方に対応できる分布だったから**と整理できる。

> [!source] 歴史的背景の根拠
> - Cambridge University Press, J. M. Hilbe, *Negative Binomial Regression*, historical introduction: https://assets.cambridge.org/97805211/98158/excerpt/9780521198158_excerpt.pdf
> - Encyclopedia of Mathematics, “Negative binomial distribution”: https://encyclopediaofmath.org/wiki/Negative_binomial_distribution
## 幾何分布との関係

幾何分布は負の2項分布の $r=1$ の場合である。

$$
\begin{aligned}
P(X=k)
&=\binom{1+k-1}{k}p^1q^k\\
&=\binom{k}{k}pq^k\\
&=pq^k
\end{aligned}
$$

したがって、

$$
NBin(1,p)=Geo(p)
$$

である。

また、$r$ 回の成功までの失敗回数を成功ごとの待ち時間へ分ければ、

$$
X=Y_1+\cdots+Y_r
$$

と書け、各 $Y_i$ は独立な $Geo(p)$ に従う。

## 現場ではいつ使えるか

第一の使い方は定義そのもので、「成功を $r$ 回得るまでに何回失敗するか」を扱う停止時刻問題である。


> [!source] 根拠資料
> - Encyclopedia of Mathematics, “Negative binomial distribution”: https://encyclopediaofmath.org/wiki/Negative_binomial_distribution
> - SciPy, `scipy.stats.nbinom`: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.nbinom.html



## 確率の総和が1になること

まず次の級数を使う。

$$
\sum_{k=0}^{\infty}\binom{r+k-1}{k}q^k=\frac{1}{(1-q)^r}
$$
[これの導出の仕方](負の二項分布の総和のための級数.md)

したがって、

$$
\begin{aligned}
\sum_{k=0}^{\infty}P(X=k)
&=\sum_{k=0}^{\infty}\binom{r+k-1}{k}p^rq^k\\
&=p^r\sum_{k=0}^{\infty}\binom{r+k-1}{k}q^k\\
&=p^r\frac{1}{(1-q)^r}\\
&=p^r\frac{1}{p^r}\\
&=1
\end{aligned}
$$

となる。


## 平均

計算を見やすくするため、

$$
C_r(k):=\binom{r+k-1}{k}
$$

とおく。

先ほどの恒等式を

$$
S(q):=\sum_{k=0}^{\infty}C_r(k)q^k=(1-q)^{-r}
$$

と書く。

両辺を $q$ で微分すると、

$$
\sum_{k=1}^{\infty}kC_r(k)q^{k-1}
=r(1-q)^{-r-1}
$$

となる。右辺の微分は

$$
\begin{aligned}
\frac{d}{dq}(1-q)^{-r}
&=-r(1-q)^{-r-1}\cdot(-1)\\
&=r(1-q)^{-r-1}
\end{aligned}
$$

である。

両辺に $q$ を掛けると、

$$
\sum_{k=1}^{\infty}kC_r(k)q^k
=rq(1-q)^{-r-1}
$$

となる。

したがって、

$$
\begin{aligned}
E[X]
&=\sum_{k=0}^{\infty}kC_r(k)p^rq^k\\
&=p^r\sum_{k=1}^{\infty}kC_r(k)q^k\\
&=p^r\,rq(1-q)^{-r-1}\\
&=p^r\,rq\,p^{-r-1}\\
&=\frac{rq}{p}
\end{aligned}
$$

となる。

したがって、

$$
E[X]=\frac{r(1-p)}{p}=\frac{rq}{p}
$$

である。

## 分散

先ほどの式

$$
S'(q)=r(1-q)^{-r-1}
$$

をもう1回微分する。

$$
\begin{aligned}
S''(q)
&=\frac{d}{dq}\left[r(1-q)^{-r-1}\right]\\
&=r\left[-(r+1)(1-q)^{-r-2}\right](-1)\\
&=r(r+1)(1-q)^{-r-2}
\end{aligned}
$$

一方、級数側は

$$
S''(q)=\sum_{k=2}^{\infty}k(k-1)C_r(k)q^{k-2}
$$

である。よって、

$$
\sum_{k=2}^{\infty}k(k-1)C_r(k)q^{k-2}
=r(r+1)(1-q)^{-r-2}
$$

となる。

両辺に $p^rq^2$ を掛けると、

$$
\begin{aligned}
E[X(X-1)]
&=p^rq^2r(r+1)(1-q)^{-r-2}\\
&=p^rq^2r(r+1)p^{-r-2}\\
&=\frac{r(r+1)q^2}{p^2}
\end{aligned}
$$

となる。

したがって、

$$
\begin{aligned}
Var(X)
&=E[X(X-1)]+E[X]-(E[X])^2\\
&=\frac{r(r+1)q^2}{p^2}+\frac{rq}{p}-\left(\frac{rq}{p}\right)^2\\
&=\frac{r(r+1)q^2}{p^2}+\frac{rpq}{p^2}-\frac{r^2q^2}{p^2}\\
&=\frac{r(r+1)q^2-r^2q^2+rpq}{p^2}\\
&=\frac{rq^2+rpq}{p^2}\\
&=\frac{rq(q+p)}{p^2}\\
&=\frac{rq}{p^2}
\end{aligned}
$$

となる。

したがって、負の2項分布では

$$
E[X]=\frac{rq}{p},\qquad Var(X)=\frac{rq}{p^2}
$$

である。

$r=1$ とすると負の2項分布は幾何分布になるので、

$$
E[X]=\frac{q}{p},\qquad Var(X)=\frac{q}{p^2}
$$

も同時に得られる。



---

# ポアソン分布

無限回の試行回数でたかだか$\lambda$回しか起こらないような試行についての分布
例えば時間であれば$t\in[0,1]$で制限してもいいし、$t\in[0,\infty]$でもいいがtごとに施行が行われているとしたときに、無限回の試行で平均して$\lambda$回発生するような事象について、全期間内で何回発生するかをx軸にその確率を配置した分布

## 1からこの分布を作る：2項分布の希少事象極限

ポアソン分布は、前述の2項分布から極限として作ることができる。

まず

$$
X_n\sim Bin(n,p_n)
$$

とする。観測機会 $n$ を増やす一方で1回あたりの発生確率を小さくし、期待される総発生回数 $np_n$ を一定値 $\lambda>0$ に保つ。すなわちどんなに発生機会を増やしてもその分、確率は小さくなっていく

$$
p_n=\frac{\lambda}{n}
$$

を置く。

固定した $k$ に対して、

$$
\begin{aligned}
P(X_n=k)
&=\binom nk\left(\frac{\lambda}{n}\right)^k
\left(1-\frac{\lambda}{n}\right)^{n-k}\\
&=\frac{n!}{k!(n-k)!}\frac{\lambda^k}{n^k}
\left(1-\frac{\lambda}{n}\right)^{n-k}\\
&=\frac{\lambda^k}{k!}
\frac{n!}{(n-k)!n^k}
\left(1-\frac{\lambda}{n}\right)^n
\left(1-\frac{\lambda}{n}\right)^{-k}
\end{aligned}
$$

となる。

ここで、

$$
\begin{aligned}
\frac{n!}{(n-k)!n^k}
&=\frac{n(n-1)\cdots(n-k+1)}{n^k}\\
&=\frac nn\frac{n-1}{n}\cdots\frac{n-k+1}{n}\\
&=1\left(1-\frac1n\right)\cdots
\left(1-\frac{k-1}{n}\right)
\end{aligned}
$$

なので、$k$ を固定して $n\to\infty$ とすると

$$
\frac{n!}{(n-k)!n^k}\to1
$$

である。

また、

$$
\left(1-\frac{\lambda}{n}\right)^n\to e^{-\lambda}
$$

かつ、固定した $k$ に対して

$$
\left(1-\frac{\lambda}{n}\right)^{-k}\to1
$$

である。したがって、

$$
\begin{aligned}
\lim_{n\to\infty}P(X_n=k)
&=\frac{\lambda^k}{k!}\times1\times e^{-\lambda}\times1\\
&=\frac{\lambda^k}{k!}e^{-\lambda}
\end{aligned}
$$

となる。この極限を確率関数として持つ分布がポアソン分布である。

## 歴史的経緯：1を補う「なぜ必要になったか」

前節では2項分布の希少事象極限からポアソン分布を導いた。ここでは、その極限を考える必要が生じた背景だけを補う。


この分布の意味は、個々の試行を細かく追う代わりに、**ある区間全体で平均して何件起こるか**という少数の情報で、まれな事象の件数を記述できる点にある。その後、「多数の機会の中で少数だけ生じる事象」を扱うモデルとして価値が認識され、時間・空間内の発生件数を扱う標準的な分布へ発展した。

したがってポアソン分布は、2項分布から式変形すると偶然出てくる分布というより、**「非常に多い機会 × 非常に小さい発生確率」という、通常の反復試行モデルでは扱いづらい領域を簡潔に記述する必要**から重要になった分布と理解するとよい。

> [!source] 歴史的背景の根拠
> - MacTutor History of Mathematics, “Siméon-Denis Poisson”: https://mathshistory.st-andrews.ac.uk/Biographies/Poisson/
> - MacTutor, Poisson の確率論研究の解説: https://mathshistory.st-andrews.ac.uk/Strick/poisson.pdf
## 前述の分布との関係

2項分布で

$$
n\to\infty,\qquad p\to0,\qquad np\to\lambda
$$

とすると、各固定した $k$ の確率はポアソン分布の確率へ収束する。

平均・分散もこの関係と整合する。2項分布では

$$
E[X]=np,\qquad Var(X)=np(1-p)
$$

なので、

$$
\begin{aligned}
E[X]&\to\lambda,\\
Var(X)&=np(1-p)\to\lambda
\end{aligned}
$$

となる。後で直接証明する

$$
E[X]=Var(X)=\lambda
$$

と一致する。

## 現場ではいつ使えるか

一定の時間・空間・面積などの区間内で「事象が何回起きたか」という**カウント**を扱うときの基本分布である。

例えば一定時間内の到着件数、一定面積内の欠陥数、十分小さい発生確率の事象を多数回観測したときの発生回数などが、ポアソン型の仮定が妥当なら対象になる。


> [!source] 根拠資料
> - NIST/SEMATECH e-Handbook, “Poisson Distribution”: https://itl.nist.gov/div898/handbook/eda/section3/eda366j.htm
> - Encyclopedia of Mathematics, “Poisson distribution”: https://encyclopediaofmath.org/wiki/Poisson_distribution
> - Encyclopedia of Mathematics, “Poisson theorem”: https://encyclopediaofmath.org/wiki/Poisson_theorem



## 確率の総和が1になること

指数関数のマクローリン展開（0周りでのテイラー展開、0回りといってもX=0付近でしか成立しないわけではない（近似を取ったら0付近でしか成立しない））

$$
e^\lambda=\sum_{k=0}^{\infty}\frac{\lambda^k}{k!}
$$

を使う。

すると、

$$
\begin{aligned}
\sum_{k=0}^{\infty}P(X=k)
&=\sum_{k=0}^{\infty}\frac{\lambda^k}{k!}e^{-\lambda}\\
&=e^{-\lambda}\sum_{k=0}^{\infty}\frac{\lambda^k}{k!}\\
&=e^{-\lambda}e^\lambda\\
&=e^0\\
&=1
\end{aligned}
$$

となる。

## 平均

期待値の定義から、

$$
E[X]=\sum_{k=0}^{\infty}k\frac{\lambda^k}{k!}e^{-\lambda}
$$

である。$k=0$ の項は $0$ なので、

$$
E[X]=e^{-\lambda}\sum_{k=1}^{\infty}k\frac{\lambda^k}{k!}
$$

と書ける。

ここで、

$$
\begin{aligned}
k\frac{\lambda^k}{k!}
&=\frac{k\lambda^k}{k(k-1)!}\\
&=\frac{\lambda^k}{(k-1)!}\\
&=\lambda\frac{\lambda^{k-1}}{(k-1)!}
\end{aligned}
$$

なので、

$$
\begin{aligned}
E[X]
&=\lambda e^{-\lambda}\sum_{k=1}^{\infty}\frac{\lambda^{k-1}}{(k-1)!}
\end{aligned}
$$

となる。

$j=k-1$ とおくと、$k=1$ から $\infty$ までの和は $j=0$ から $\infty$ までの和に変わるので、

$$
\begin{aligned}
E[X]
&=\lambda e^{-\lambda}\sum_{j=0}^{\infty}\frac{\lambda^j}{j!}\\
&=\lambda e^{-\lambda}e^\lambda\\
&=\lambda
\end{aligned}
$$

となる。

したがって、

$$
E[X]=\lambda
$$

である。

## 分散

まず $E[X(X-1)]$ を求める。

$$
E[X(X-1)]
=\sum_{k=0}^{\infty}k(k-1)\frac{\lambda^k}{k!}e^{-\lambda}
$$

$k=0,1$ の項は $0$ なので、

$$
E[X(X-1)]
=e^{-\lambda}\sum_{k=2}^{\infty}k(k-1)\frac{\lambda^k}{k!}
$$

である。

係数を変形すると、

$$
\begin{aligned}
k(k-1)\frac{\lambda^k}{k!}
&=k(k-1)\frac{\lambda^k}{k(k-1)(k-2)!}\\
&=\frac{\lambda^k}{(k-2)!}\\
&=\lambda^2\frac{\lambda^{k-2}}{(k-2)!}
\end{aligned}
$$

となる。したがって、

$$
\begin{aligned}
E[X(X-1)]
&=\lambda^2e^{-\lambda}\sum_{k=2}^{\infty}\frac{\lambda^{k-2}}{(k-2)!}
\end{aligned}
$$

である。

$j=k-2$ とおくと、

$$
\begin{aligned}
E[X(X-1)]
&=\lambda^2e^{-\lambda}\sum_{j=0}^{\infty}\frac{\lambda^j}{j!}\\
&=\lambda^2e^{-\lambda}e^\lambda\\
&=\lambda^2
\end{aligned}
$$

となる。

ここで

$$
X^2=X(X-1)+X
$$

なので、

$$
\begin{aligned}
Var(X)
&=E[X(X-1)]+E[X]-(E[X])^2\\
&=\lambda^2+\lambda-\lambda^2\\
&=\lambda
\end{aligned}
$$

となる。

したがって、ポアソン分布では

$$
E[X]=\lambda,\qquad Var(X)=\lambda
$$

であり、**平均と分散が同じ値になる**のが特徴である。


# 超幾何分布

## 1からこの分布を作る：有限母集団から戻さずに選ぶ

壺の中に

- 赤玉が $M$ 個
- 白玉が $N-M$ 個

入っており、合計は $N$ 個であるとする。

この壺から**非復元抽出**、つまり一度取り出した玉を戻さずに $K$ 個の玉を取り出す。取り出した赤玉の個数を $X$ とすると、この $X$ の分布を超幾何分布という。

## $X$ が取りうる範囲

赤玉の個数 $X$ は当然 $0$ 以上なので、

$$
X\ge0
$$

である。

また、取り出す玉は全部で $K$ 個なので、赤玉だけが $K$ 個を超えることはできない。

$$
X\le K
$$

さらに、壺の中に赤玉は $M$ 個しかないので、

$$
X\le M
$$

である。したがって上限は

$$
x_U=\min(K,M)
$$

となる。

一方、取り出した白玉の個数は

$$
K-X
$$

である。白玉は全部で $N-M$ 個しかないので、

$$
K-X\le N-M
$$

でなければならない。これを $X$ について解くと、

$$
\begin{aligned}
K-X&\le N-M\\
-X&\le N-M-K\\
X&\ge K+M-N
\end{aligned}
$$

となる。

もともと $X\ge0$ でもあるので、下限は

$$
x_L=\max(0,K+M-N)
$$

である。

したがって、

$$
x_L\le X\le x_U
$$

の範囲だけ確率が正になる。

## 確率関数の導出

$N$ 個の玉から順番を考えずに $K$ 個を選ぶ方法は

$$
\binom{N}{K}
$$

通りある。

そのうち赤玉をちょうど $x$ 個選ぶには、まず $M$ 個の赤玉から $x$ 個を選ぶ。

$$
\binom{M}{x}
$$

通りである。

さらに、残りの $K-x$ 個は白玉でなければならないので、$N-M$ 個の白玉から $K-x$ 個を選ぶ。

$$
\binom{N-M}{K-x}
$$

通りである。

したがって、「赤玉がちょうど $x$ 個」という条件を満たす選び方は

$$
\binom{M}{x}\binom{N-M}{K-x}
$$

通りである。

すべての $K$ 個の選び方を同じ確率と考えれば、

$$
P(X=x)
=\frac{\binom{M}{x}\binom{N-M}{K-x}}{\binom{N}{K}},
\qquad x_L\le x\le x_U
$$

となる。


## 歴史的経緯：1を補う「なぜ必要になったか」

前節では有限母集団から非復元抽出すると超幾何分布が得られることを示した。ここで補いたいのは、**なぜ2項分布とは別に「有限母集団からの抽出」を独立したモデルとして扱う必要があるのか**である。

実際の標本調査、抜き取り検査、カードや壺からの抽出では、一度選んだ対象を母集団へ戻さないことがある。このときは、標本を1つ取るたびに残っている母集団そのものが変化する。そのため、復元抽出を前提にした独立試行のモデルだけでは、有限母集団から標本を取る際の不確実性を正確に記述できない。

この問題は単なるゲームの計算にとどまらず、**有限個の対象から一部を調べて全体について判断する標本抽出**の基礎になる。後には、周辺度数を固定した分割表で正確な確率を計算する Fisher の正確確率検定にも超幾何分布が使われるようになった。

なお、今回確認した信頼できる資料からは「超幾何分布が誰によって、どの単一の問題を解くため最初に作られたか」という発明史を一意に確認できない。そのため、ここでは発明者や単一の発明動機を推測せず、資料で確認できる**非復元抽出という問題領域がこの分布を必要とする**という点に限定する。

> [!source] 歴史的背景の根拠
> - Encyclopedia of Mathematics, “Hypergeometric distribution”: https://encyclopediaofmath.org/wiki/Hypergeometric_distribution
> - University of California, Berkeley, simple random sampling without replacement の解説: https://www.stat.berkeley.edu/~stark/SticiGui/Text/randomVariables.htm
> - SciPy, `scipy.stats.fisher_exact`: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.fisher_exact.html
## 前述の分布との関係

超幾何分布と2項分布の違いは「1回引いたものを戻すかどうか」に集約できる。

母集団に $N$ 個の要素があり、そのうち $M$ 個が成功対象だとすると、1回目の成功確率は

$$
p=\frac MN
$$

である。

### 復元抽出なら2項分布

毎回取り出した要素を戻すなら、各試行の成功確率は常に $M/N$ のままで、試行同士を独立にできる。$K$ 回中の成功回数 $Y$ は

$$
Y\sim Bin\left(K,\frac MN\right)
$$

となる。

### 非復元抽出なら超幾何分布

戻さない場合、1回成功を引いた後の次の成功確率は

$$
\frac{M-1}{N-1}
$$

へ変わるので、試行は独立ではない。そのため成功数 $X$ は2項分布ではなく、

$$
P(X=x)=
\frac{\binom Mx\binom{N-M}{K-x}}{\binom NK}
$$

という超幾何分布に従う。

この違いは分散にも現れ、後で証明するように

$$
Var(X)=Kp(1-p)\frac{N-K}{N-1}
$$

となる。2項分布の分散 $Kp(1-p)$ に有限母集団補正が掛かるのは、非復元抽出によって抽出同士が負に相関するからである。

## 現場ではいつ使えるか

有限母集団から**非復元でサンプリング**し、その標本に含まれる対象数を数えるときに使う。例えば有限ロットから製品を抜き取り、対象となる製品が何個含まれるかを数える状況が対応する。

また2×2分割表で周辺和を固定した Fisher の正確確率検定では、セルの1つの度数の帰無分布が超幾何分布になる。SciPy の `fisher_exact` の説明でもこの対応が明示されている。


> [!source] 根拠資料
> - Encyclopedia of Mathematics, “Hypergeometric distribution”: https://encyclopediaofmath.org/wiki/Hypergeometric_distribution
> - SciPy, “Hypergeometric Distribution”: https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_hypergeom.html
> - SciPy, `scipy.stats.fisher_exact`: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.fisher_exact.html

## 確率の総和が1になること

確率を全部足すと、

$$
\begin{aligned}
\sum_{x=x_L}^{x_U}P(X=x)
&=\sum_{x=x_L}^{x_U}
\frac{\binom{M}{x}\binom{N-M}{K-x}}{\binom{N}{K}}\\
&=\frac{1}{\binom{N}{K}}
\sum_{x=x_L}^{x_U}\binom{M}{x}\binom{N-M}{K-x}
\end{aligned}
$$

となる。

ここで、

$$
\sum_{x=x_L}^{x_U}\binom{M}{x}\binom{N-M}{K-x}
=\binom{N}{K}
$$

が成り立つ。

なぜなら、右辺の $\binom{N}{K}$ は「赤白を区別せず、$N$ 個全部から $K$ 個選ぶ方法の総数」を表す。一方、左辺は

$$
\text{赤を0個選ぶ場合}
+\text{赤を1個選ぶ場合}
+\cdots
$$

のように、選び方を「赤玉を何個選んだか」で重複なく分類して数え直したものだからである。

したがって、

$$
\begin{aligned}
\sum_{x=x_L}^{x_U}P(X=x)
&=\frac{1}{\binom{N}{K}}\binom{N}{K}\\
&=1
\end{aligned}
$$

となる。


## 平均

超幾何分布の平均は、各抽出が赤玉だったかどうかを表す指示変数を使うと計算しやすい。

$i$ 回目の抽出について

$$
I_i=
\begin{cases}
1 & (i\text{回目に赤玉を引いたとき})\\
0 & (i\text{回目に白玉を引いたとき})
\end{cases}
$$

と定義する。

取り出した赤玉の総数は

$$
X=I_1+I_2+\cdots+I_K
$$

と書ける。

非復元抽出なので各 $I_i$ は独立ではないが、$i$ 回目に赤玉が来る周辺確率は対称性から

$$
P(I_i=1)=\frac{M}{N}=:p
$$

である。したがって、各 $I_i$ は周辺分布だけ見ればベルヌーイ分布であり、

$$
E[I_i]=p
$$

となる。

期待値の線形性には独立性は必要ないので、

$$
\begin{aligned}
E[X]
&=E[I_1+I_2+\cdots+I_K]\\
&=E[I_1]+E[I_2]+\cdots+E[I_K]\\
&=\underbrace{p+p+\cdots+p}_{K\text{個}}\\
&=Kp
\end{aligned}
$$

となる。

$p=M/N$ なので、

$$
E[X]=K\frac{M}{N}
$$

である。

## 分散

分散では独立でないことが重要になる。

$$
X=\sum_{i=1}^{K}I_i
$$

なので、

$$
Var(X)
=\sum_{i=1}^{K}Var(I_i)
+2\sum_{1\le i<j\le K}Cov(I_i,I_j)
$$

である。

まず各 $I_i$ は周辺分布としてベルヌーイ分布なので、

$$
Var(I_i)=p(1-p)
$$

である。

次に $i\ne j$ として共分散を求める。

$$
Cov(I_i,I_j)=E[I_iI_j]-E[I_i]E[I_j]
$$

である。

$I_iI_j=1$ になるのは、$i$ 回目と $j$ 回目の両方で赤玉を引いたときだけなので、

$$
E[I_iI_j]=P(I_i=1,I_j=1)
$$

である。

1回目に対応する位置で赤玉を引く確率は $M/N$、そこですでに赤玉を1個使ったあと、もう1つの指定された位置でも赤玉を引く条件付き確率は $(M-1)/(N-1)$ なので、

$$
\begin{aligned}
E[I_iI_j]
&=\frac{M}{N}\frac{M-1}{N-1}\\
&=\frac{M(M-1)}{N(N-1)}
\end{aligned}
$$

となる。

また、

$$
E[I_i]E[I_j]=p^2=\frac{M^2}{N^2}
$$

である。したがって、

$$
\begin{aligned}
Cov(I_i,I_j)
&=\frac{M(M-1)}{N(N-1)}-\frac{M^2}{N^2}\\
&=\frac{NM(M-1)-M^2(N-1)}{N^2(N-1)}\\
&=\frac{NM^2-NM-M^2N+M^2}{N^2(N-1)}\\
&=\frac{M^2-NM}{N^2(N-1)}\\
&=-\frac{M(N-M)}{N^2(N-1)}\\
&=-\frac{1}{N-1}\frac{M}{N}\frac{N-M}{N}\\
&=-\frac{p(1-p)}{N-1}
\end{aligned}
$$

となる。

つまり、非復元抽出では1回赤玉を引くと次に赤玉を引く確率が少し下がるので、異なる抽出同士には負の共分散が生じる。

$i<j$ の組は

$$
\binom{K}{2}=\frac{K(K-1)}{2}
$$

個ある。したがって、

$$
\begin{aligned}
Var(X)
&=\sum_{i=1}^{K}p(1-p)
+2\sum_{1\le i<j\le K}\left(-\frac{p(1-p)}{N-1}\right)\\
&=Kp(1-p)
+2\binom{K}{2}\left(-\frac{p(1-p)}{N-1}\right)\\
&=Kp(1-p)
-\frac{K(K-1)p(1-p)}{N-1}\\
&=Kp(1-p)\left(1-\frac{K-1}{N-1}\right)\\
&=Kp(1-p)\frac{N-1-(K-1)}{N-1}\\
&=Kp(1-p)\frac{N-K}{N-1}
\end{aligned}
$$

となる。

したがって、超幾何分布では

$$
E[X]=Kp,
\qquad
Var(X)=\frac{N-K}{N-1}Kp(1-p),
\qquad
p=\frac{M}{N}
$$

である。

## 有限母集団補正

2項分布 $Bin(K,p)$ なら分散は

$$
Kp(1-p)
$$

であるのに対して、超幾何分布では

$$
Var(X)=\frac{N-K}{N-1}Kp(1-p)
$$

となる。

この

$$
\frac{N-K}{N-1}
$$

を**有限母集団補正**とみなせる。

非復元抽出では一度引いた玉を戻さないため、各抽出は独立ではなく、同じ色が続く方向のばらつきが抑えられる。そのため

$$
\frac{N-K}{N-1}\le1
$$

となり、超幾何分布の分散は対応する2項分布の分散より小さくなる。

PDFで触れられているように、超幾何分布はフィッシャーの正確確率検定でも利用される。

---

# 追記部分の外部参考資料

以下は上の `[!source]` で使った資料をまとめたもの。アクセス確認日: 2026-09-10。

- Encyclopedia of Mathematics, Bernoulli theorem: https://encyclopediaofmath.org/wiki/Bernoulli_theorem
- Encyclopedia of Mathematics, Bernoulli trials: https://encyclopediaofmath.org/wiki/Bernoulli_scheme
- Encyclopedia of Mathematics, Binomial distribution: https://encyclopediaofmath.org/wiki/Binomial_distribution
- Encyclopedia of Mathematics, Geometric distribution: https://encyclopediaofmath.org/wiki/Geometric_distribution
- Encyclopedia of Mathematics, Negative binomial distribution: https://encyclopediaofmath.org/wiki/Negative_binomial_distribution
- Encyclopedia of Mathematics, Hypergeometric distribution: https://encyclopediaofmath.org/wiki/Hypergeometric_distribution
- Encyclopedia of Mathematics, Poisson distribution: https://encyclopediaofmath.org/wiki/Poisson_distribution
- Encyclopedia of Mathematics, Poisson theorem: https://encyclopediaofmath.org/wiki/Poisson_theorem
- NIST/SEMATECH, Binomial Distribution: https://itl.nist.gov/div898/handbook/eda/section3/eda366i.htm
- NIST/SEMATECH, Poisson Distribution: https://itl.nist.gov/div898/handbook/eda/section3/eda366j.htm
- NIST/SEMATECH, Proportions Control Charts: https://itl.nist.gov/div898/handbook/pmc/section3/pmc332.htm
- SciPy, geometric distribution: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.geom.html
- SciPy, negative binomial distribution: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.nbinom.html
- SciPy, hypergeometric distribution: https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_hypergeom.html
- SciPy, Fisher exact test: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.fisher_exact.html

