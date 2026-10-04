from pathlib import Path
import re, json, base64, io, html as html_module
from PIL import Image

root=Path(r'F:\Document\Fy26 TDH statics lean')
template=Path(r'C:\Users\User\Downloads\９章　仮説検定と信頼区間_編集済み (3).html').read_text(encoding='utf-8')
assets={}
def figure(key,page,box,caption):
    im=Image.open(root/f'tmp/source-pages/page-{page:02d}-0.png').crop(box)
    b=io.BytesIO();im.save(b,format='JPEG',quality=93)
    assets[key]='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
    return f'<figure><img data-asset="{key}" alt="{caption}"></figure><p class="math-caption">{caption}</p>'
fig25=figure('source-fig-2-5',1,(440,100,1700,960),'図2.5　確率密度関数と分布関数（PDF 1ページ）')
fig28=figure('source-fig-2-8',5,(480,90,1830,1020),'図2.8　標準正規分布と様々な正規分布（PDF 5ページ）')
slides=[]
def add(title,summary,left='',right='',pages='',section='2.2.1',proof=False,role=None,notes=''):
    s=dict(id=f'pdf-slide-{len(slides)+1:02d}',title=title,takeaway=summary,leftMarkdown=left,rightHTML=right,
           theme='proof' if proof else 'explain',majorSection=section,section=section,subsection=section,
           original=f'1005tdh統計勉強会用.pdf　PDF {pages}ページ' if pages else '提供PDF全体の構成',
           sources=['pdf'],notes=notes or (f'対応：PDF {pages}ページ。原資料の定義・記号・説明に沿って扱う。' if pages else ''),
           minutes=1,appendix=False,body=[],equations=[],table=[],diagram='',flow=[],answers=[],layout='split')
    if role:s['role']=role
    slides.append(s)
def eq(*tex):return '<div class="proof-panel">'+''.join('<div class="proof-equation">$$'+html_module.escape(t)+'$$</div>' for t in tex)+'</div>'

add('連続確率分布と変数変換','',role='title')
add('アジェンダ','',role='agenda')
add('2.2.1　連続確率分布と特性値','連続確率変数の分布を、密度と累積確率で表す',r'''- 連続確率変数は、実数直線や区間上の連続的な値をとる。

- 電球の寿命は、正の実数値をとる例である。

- 確率密度関数 \(f(x)\) と分布関数 \(F(x)\) で分布を表す。''',fig25,'1')
add('確率密度関数','密度は非負で、全体を積分すると1になる',r'''- 連続確率変数 \(X\) の分布を、確率密度関数（pdf）\(f(x)\) で記述する。

- 密度の値は非負で、曲線の下の面積の総和は1になる。

- \(f(x)\) が最大になる点 \(x\) を**モード**と呼ぶ。''',eq(r'f(x)\ge 0',r'\int_{-\infty}^{\infty} f(x)\,dx=1'),'1')
add('区間の確率と端点','区間の確率は密度の積分で求める',r'''- \(a<b\) のとき、区間 \((a,b)\) に入る確率は密度の積分となる。

- 連続確率変数では、特定の1点をとる確率は0である。

- 区間の端点に等号を含めても確率は変わらない。離散分布では、この性質は一般には成り立たない。''',eq(r'\mathrm{P}(a<X<b)=\int_a^b f(x)\,dx',r'\mathrm{P}(X=c)=\int_c^c f(x)\,dx=0',r'\mathrm{P}(a<X<b)=\mathrm{P}(a\le X\le b)'),'1')
add('分布関数と確率密度関数','累積確率の差が区間確率となり、その微分が密度になる',r'''- 分布関数は \(x\) 以下の値をとる累積確率を表す。

- \(F(x)\) は非減少関数で、左端で0、右端で1に近づく。

- \(f\) が連続な点では、微分の基本公式から \(f(x)=F'(x)\) が成り立つ。''',eq(r'F(x)=\mathrm{P}(X\le x)=\int_{-\infty}^{x}f(u)\,du',r'\mathrm{P}(a<X\le b)=F(b)-F(a)',r'\lim_{x\to-\infty}F(x)=0,\quad\lim_{x\to\infty}F(x)=1'),'1–2')
add('分位点・メディアン・四分位点','分位点は、指定した累積確率に対応する値である',r'''- 増加する区間では、\(F\) の逆関数を用いることができる。

- \(0<p<1\) に対し、\(F(x_p)=p\) を満たす \(x_p\) を**下側100p%分位点**と呼ぶ。

$$x_p=F^{-1}(p)$$''','<table><thead><tr><th>累積確率</th><th>分位点の名称</th></tr></thead><tbody><tr><td>\\(p=1/4\\)</td><td>第1四分位点 \\(x_{0.25}\\)</td></tr><tr><td>\\(p=1/2\\)</td><td>メディアン \\(x_{0.5}\\)</td></tr><tr><td>\\(p=3/4\\)</td><td>第3四分位点 \\(x_{0.75}\\)</td></tr></tbody></table>','2')
add('定義2.8　連続確率変数の期待値','期待値は、値と密度の積を積分して定義する',r'''- \(\int_{-\infty}^{\infty}|x|f(x)\,dx<\infty\) のとき、\(X\) の期待値を定義する。

- 関数 \(g(X)\) の期待値も、元の変数 \(x\) の密度を使って求める。

- 後者では \(\int_{-\infty}^{\infty}|g(x)|f(x)\,dx<\infty\) を仮定する。''',eq(r'\mathrm{E}[X]=\int_{-\infty}^{\infty}xf(x)\,dx',r'\mathrm{E}[g(X)]=\int_{-\infty}^{\infty}g(x)f(x)\,dx'),'2')
add('定義2.9　平均・分散・標準偏差','分散は平均からのずれの二乗の期待値である',r'''- \(\mathrm{E}[|X|]<\infty\) のとき、期待値を分布の**平均**と呼び、\(\mu\) または \(\mu_X\) と表す。

- \(\mathrm{E}[X^2]<\infty\) のとき、分散を \(\sigma^2\)、\(\sigma_X^2\) または \(\operatorname{Var}(X)\) と表す。

- 分散の平方根を**標準偏差**と呼ぶ。''',eq(r'\operatorname{Var}(X)=\mathrm{E}[(X-\mu)^2]',r'=\int_{-\infty}^{\infty}(x-\mu)^2f(x)\,dx',r'\sigma=\sqrt{\operatorname{Var}(X)}'),'2')
add('分散の計算式の導出','分散は二乗の期待値から平均の二乗を引いて求める',r'''\(\mu=\mathrm{E}[X]\)、\(\int f(x)\,dx=1\) を用いて展開する。

$$\begin{aligned}
\operatorname{Var}(X)
&=\int_{-\infty}^{\infty}(x-\mu)^2f(x)\,dx\\
&=\int_{-\infty}^{\infty}(x^2-2\mu x+\mu^2)f(x)\,dx\\
&=\mathrm{E}[X^2]-2\mu\mathrm{E}[X]+\mu^2\\
&=\mathrm{E}[X^2]-(\mathrm{E}[X])^2
\end{aligned}$$''',pages='3',proof=True)

add('2.2.5　正規分布','正規分布は釣り鐘型の連続確率分布である',r'''- 正規分布は、確率・統計で重要な役割をもつ。

- 中心極限定理により、独立な確率変数の和の分布を正規分布で近似できる。

- 平均と分散によって、中心の位置と分布の広がりが変わる。''',fig28,'4–5','2.2.5')
add('正規分布の確率密度関数','正規分布を平均μと分散σ²で表す',r'''- 正規分布は**ガウス分布**とも呼び、\(N(\mu,\sigma^2)\) と表す。

- パラメータは \(-\infty<\mu<\infty\)、\(\sigma>0\) である。

- \(\mu\) は平均、\(\sigma\) は標準偏差に対応する。''',eq(r'f(x)=\frac{1}{\sqrt{2\pi}\sigma}\exp\!\left\{-\frac{(x-\mu)^2}{2\sigma^2}\right\}',r'-\infty<x<\infty'),'5','2.2.5')
add('標準正規分布','平均0・分散1の正規分布を標準正規分布と呼ぶ',r'''- \(\mu=0\)、\(\sigma=1\) の場合を \(N(0,1)\) と表す。

- 密度を \(\phi(x)\)、分布関数を \(\Phi(x)\) と表す。

- 正規化には \(\int_{-\infty}^{\infty}e^{-x^2/2}\,dx=\sqrt{2\pi}\) を用いる。''',eq(r'\phi(x)=\frac{1}{\sqrt{2\pi}}e^{-x^2/2}',r'\Phi(x)=\int_{-\infty}^{x}\phi(u)\,du'),'5','2.2.5')
add('命題2.13　正規分布の平均と分散','N(μ, σ²) の平均はμ、分散はσ²となる',r'''- \(X\sim N(\mu,\sigma^2)\) とする。

- 密度の積分が1であることを使い、パラメータ \(\mu\) で微分して平均と二次モーメントを求める。''',eq(r'\mathrm{E}[X]=\mu',r'\operatorname{Var}(X)=\sigma^2'),'5–6','2.2.5',True)
add('命題2.13の証明　平均','密度の正規化条件をμで微分すると平均を得る',r'''正規密度を \(f(x;\mu,\sigma)\) と書く。資料では積分と微分を交換して計算する。

$$\begin{aligned}
\int_{-\infty}^{\infty}f(x;\mu,\sigma)\,dx&=1\\
\frac{\partial f}{\partial\mu}&=\frac{x-\mu}{\sigma^2}f(x;\mu,\sigma)\\
\int_{-\infty}^{\infty}(x-\mu)f(x;\mu,\sigma)\,dx&=0\\
\int_{-\infty}^{\infty}xf(x;\mu,\sigma)\,dx&=\mu
\end{aligned}$$

したがって、\(\mathrm{E}[X]=\mu\) が成り立つ。''',pages='5–6',section='2.2.5',proof=True)
add('命題2.13の証明　分散','平均の式をさらにμで微分して二次モーメントを得る',r'''$$\begin{aligned}
\frac{\partial}{\partial\mu}\int_{-\infty}^{\infty}xf(x;\mu,\sigma)\,dx&=1\\
\int_{-\infty}^{\infty}x(x-\mu)f(x;\mu,\sigma)\,dx&=\sigma^2\\
\mathrm{E}[X^2]-\mu\mathrm{E}[X]&=\sigma^2\\
\mathrm{E}[X^2]&=\sigma^2+\mu^2\\
\operatorname{Var}(X)&=\mathrm{E}[X^2]-(\mathrm{E}[X])^2=\sigma^2
\end{aligned}$$''',pages='6',section='2.2.5',proof=True)

add('2.3　確率変数の関数の分布と変数変換','変換後の確率変数の分布を、元の分布から求める',r'''- 連続確率変数 \(X\) を関数 \(g\) で変換し、\(Y=g(X)\) とおく。

- 元の変数と変換後の変数を区別するため、密度と分布関数に添字を付ける。

- まず、実数 \(a,b\) に対する線形変換 \(Y=aX+b\) を考える。''','<table><thead><tr><th>変数</th><th>密度</th><th>分布関数</th></tr></thead><tbody><tr><td>\\(X\\)</td><td>\\(f_X(x)\\)</td><td>\\(F_X(x)\\)</td></tr><tr><td>\\(Y=g(X)\\)</td><td>\\(f_Y(y)\\)</td><td>\\(F_Y(y)\\)</td></tr></tbody></table>','7','2.3')
add('線形変換　a > 0の場合','分布関数を書き換えて微分すると変換後の密度を得る',r'''\(Y=aX+b\)、\(a>0\) とする。

$$\begin{aligned}
F_Y(y)&=\mathrm{P}(aX+b\le y)\\
&=\mathrm{P}\!\left(X\le\frac{y-b}{a}\right)\\
&=F_X\!\left(\frac{y-b}{a}\right)\\[8pt]
f_Y(y)&=\frac{d}{dy}F_X\!\left(\frac{y-b}{a}\right)\\
&=\frac{1}{a}f_X\!\left(\frac{y-b}{a}\right)
\end{aligned}$$''',pages='7–8',section='2.3',proof=True)
add('線形変換　a < 0の場合','負の係数では不等号が反転し、密度に絶対値が現れる',r'''- \(a<0\) では、不等号の向きが反転する。

$$F_Y(y)=1-F_X\!\left(\frac{y-b}{a}\right)$$

$$f_Y(y)=-\frac{1}{a}f_X\!\left(\frac{y-b}{a}\right)$$

- 正負をまとめると、\(a\ne0\) に対して右の式となる。''',eq(r'f_Y(y)=\frac{1}{|a|}f_X\!\left(\frac{y-b}{a}\right)',r'\text{式 }(2.16)'),'8','2.3',True,notes='PDF 8ページ、式(2.16)。原文は「すべての実数a」と記すが、式はa≠0で定義される。a=0ならY=bに退化するため、この密度公式の対象外。')
add('命題2.15　正規分布の線形変換','正規分布の線形変換も正規分布に従う',r'''- \(X\sim N(\mu,\sigma^2)\)、\(Y=aX+b\)、\(a\ne0\) とする。

- 線形変換の密度公式に正規密度を代入する。

- 変換後の平均は \(a\mu+b\)、分散は \(a^2\sigma^2\) となる。''',eq(r'f_Y(y)=\frac{1}{\sqrt{2\pi}|a|\sigma}\exp\!\left\{-\frac{(y-b-a\mu)^2}{2a^2\sigma^2}\right\}',r'Y\sim N(a\mu+b,\,a^2\sigma^2)'),'8','2.3',True)
add('標準化と正規分布の区間確率','標準化により、区間確率をΦの差として計算できる',r'''- \(X\sim N(\mu,\sigma^2)\) を標準化する。

$$Z=\frac{X-\mu}{\sigma}\sim N(0,1)$$

- \(x_1<x_2\) の区間確率は、標準正規分布の分布関数で求める。

- 具体的な値は標準正規分布の数表などで計算する。''',eq(r'\mathrm{P}(x_1<X<x_2)',r'=\mathrm{P}\!\left(\frac{x_1-\mu}{\sigma}<Z<\frac{x_2-\mu}{\sigma}\right)',r'=\Phi\!\left(\frac{x_2-\mu}{\sigma}\right)-\Phi\!\left(\frac{x_1-\mu}{\sigma}\right)'),'8–9','2.3')
add('命題2.16　変数変換の公式','単調な変換では、逆関数とその微分で密度を求める',r'''- \(X\) は密度 \(f_X(x)\) をもつ連続確率変数とする。

- \(g\) は \(f_X(x)\ne0\) の範囲で単調増加または単調減少し、必要な逆関数の微分が存在するとする。

- \(Y=g(X)\) の密度は、元の密度に変換の倍率を掛けた形となる。''',eq(r'f_Y(y)=f_X(g^{-1}(y))\left|\frac{d}{dy}g^{-1}(y)\right|',r'\text{式 }(2.17)'),'9','2.3',True)
add('命題2.16の証明　単調増加','分布関数に逆関数を代入し、連鎖律で微分する',r'''\(g\) が単調増加する場合、逆関数 \(g^{-1}\) を用いる。

$$\begin{aligned}
F_Y(y)&=\mathrm{P}(g(X)\le y)\\
&=\mathrm{P}(X\le g^{-1}(y))\\
&=F_X(g^{-1}(y))\\[8pt]
f_Y(y)&=\frac{d}{dy}F_X(g^{-1}(y))\\
&=f_X(g^{-1}(y))\frac{d}{dy}g^{-1}(y)
\end{aligned}$$''',pages='9',section='2.3',proof=True)
add('単調減少と逆関数の微分','絶対値で増加・減少の両方の変換を表せる',r'''- \(g\) が単調減少する場合は、不等号が反転する。

$$F_Y(y)=1-F_X(g^{-1}(y))$$

- 微分すると負号が現れ、式(2.17)にまとめられる。

- \(y=g(x)\) を \(y\) で微分し、逆関数の微分を求める。''',eq(r'1=g^{\prime}(x)\frac{dx}{dy}',r'\frac{d}{dy}g^{-1}(y)=\frac{1}{g^{\prime}(g^{-1}(y))}',r'\text{式 }(2.18)'),'9','2.3',True)
add('命題2.17　確率積分変換','連続確率変数を自分の分布関数で変換すると一様分布になる',r'''- \(X\) は分布関数 \(F_X\) をもつ連続確率変数とする。

- \(Y=F_X(X)\) とおくと、\(Y\sim U(0,1)\) となる。

- 資料の証明では、逆関数を使って \(0<y<1\) の累積確率を求める。''',eq(r'\mathrm{P}(Y\le y)=\mathrm{P}(F_X(X)\le y)',r'=\mathrm{P}(X\le F_X^{-1}(y))',r'=F_X(F_X^{-1}(y))=y',r'F_Y(y)=y,\quad f_Y(y)=1'),'10','2.3',True,notes='PDF 10ページ、命題2.17。資料の逆関数による表示に準拠。分布関数が狭義増加しない場合は、一般化逆関数で理解する。')
add('命題2.18　逆分布関数による変換','一様分布を逆分布関数で変換すると目的の分布になる',r'''- \(U\sim U(0,1)\) とする。

- 分布関数 \(F\) と密度 \(f\) に対し、\(X=F^{-1}(U)\) とおく。

- \(X\) の分布関数は \(F\)、密度は \(f\) となる。''',eq(r'F_X(x)=\mathrm{P}(F^{-1}(U)\le x)',r'=\mathrm{P}(U\le F(x))=F(x)',r'f_X(x)=F_X^{\prime}(x)=f(x)'),'10','2.3',True)
add('置換積分と1対1でない変換','変換は確率を保ち、1対1でない場合は分布関数から求める',r'''- 変数変換は置換積分に対応し、全体の確率を1に保つ。

$$\int f_X(x)\,dx=\int f_Y(y)\,dy=1$$

- 単調変換では、向きも考慮すると \(f_Y(y)=f_X(x)|dx/dy|\) と表せる。

- 1対1でない変換では、\(\mathrm{P}(g(X)\le y)\) を直接評価する。''',eq(r'f_Y(y)=\frac{d}{dy}\mathrm{P}(g(X)\le y)'),'10','2.3',notes='PDF 10ページ。資料末尾の置換積分の表示に、単調減少の場合も含めた絶対値を明記。')
add('命題2.19　平方変換','平方変換では、正と負の両方の元の値が同じ値に対応する',r'''- \(X\) の密度 \(f_X\) は実数直線上で正とする。

- \(Y=X^2\) とおくと、\(y>0\) は \(x=\sqrt y\) と \(x=-\sqrt y\) に対応する。

- 両方の密度を合わせ、変換の倍率を掛ける。''',eq(r'f_Y(y)=\frac{f_X(\sqrt y)+f_X(-\sqrt y)}{2\sqrt y}',r'y>0\qquad\text{式 }(2.19)'),'11','2.3',True)
add('命題2.19の証明','平方の累積確率を対称な区間の確率に書き換える',r'''\(y>0\) に対して、\(X^2\le y\) は \(-\sqrt y\le X\le\sqrt y\) と同値である。

$$\begin{aligned}
F_Y(y)&=\mathrm{P}(-\sqrt y\le X\le\sqrt y)\\
&=\int_{-\sqrt y}^{\sqrt y}f_X(x)\,dx\\[8pt]
f_Y(y)&=\frac{d}{dy}\int_{-\sqrt y}^{\sqrt y}f_X(x)\,dx\\
&=\frac{f_X(\sqrt y)+f_X(-\sqrt y)}{2\sqrt y}
\end{aligned}$$''',pages='11',section='2.3',proof=True)
add('原点対称な密度の平方変換','元の密度が原点対称なら、平方変換の式が簡単になる',r'''- \(f_X\) が \(x=0\) に関して対称なら、\(f_X(-x)=f_X(x)\) が成り立つ。

- 平方変換の2つの項は等しくなる。

- 標準正規密度 \(\phi\) にも、この形を適用できる。''',eq(r'f_Y(y)=\frac{f_X(\sqrt y)}{\sqrt y},\qquad y>0',r'Z\sim N(0,1)\ \Longrightarrow\ f_{Z^2}(y)=\frac{\phi(\sqrt y)}{\sqrt y}'),'11','2.3')
add('命題2.20　標準正規変数の平方','標準正規変数の平方は自由度1のカイ二乗分布に従う',r'''- \(Z\sim N(0,1)\) のとき、\(Z^2\) は自由度1のカイ二乗分布に従う。

- 資料では、同じ分布をガンマ分布 \(Ga(1/2,2)\) とも表す。

- あわせて \(\Gamma(1/2)=\sqrt\pi\) が成り立つ。''',eq(r'Z^2\sim\chi_1^2=Ga(1/2,2)',r'\Gamma(1/2)=\sqrt\pi'),'11','2.3',True)
add('命題2.20の証明　平方の密度','平方変換の公式に標準正規密度を代入する',r'''\(X=Z^2\)、\(x>0\) とおく。

$$\begin{aligned}
f_X(x)&=\frac{1}{\sqrt x}\phi(\sqrt x)\\
&=\frac{1}{\sqrt{2\pi x}}e^{-x/2}\\
&=\frac{1}{\sqrt\pi}\left(\frac12\right)^{1/2}x^{1/2-1}e^{-x/2}
\end{aligned}$$

この式を積分し、ガンマ分布の正規化と比較する。''',pages='11',section='2.3',proof=True)
add('命題2.20の証明　ガンマ関数との関係','密度の積分が1であることからΓ(1/2)を求める',r'''ガンマ分布 \(Ga(1/2,2)\) の密度の積分は1である。

$$\begin{aligned}
1&=\int_0^{\infty}f_X(x)\,dx\\
&=\frac{\Gamma(1/2)}{\sqrt\pi}\int_0^{\infty}\frac{(1/2)^{1/2}}{\Gamma(1/2)}x^{1/2-1}e^{-x/2}\,dx\\
&=\frac{\Gamma(1/2)}{\sqrt\pi}
\end{aligned}$$

したがって、\(\Gamma(1/2)=\sqrt\pi\)。\(f_X\) は \(Ga(1/2,2)\)、すなわち \(\chi_1^2\) の密度となる。''',pages='11',section='2.3',proof=True)
add('演習問題　問1（二項分布）','二項分布の確率の漸化式と最大値を考える',r'''\(X\sim\operatorname{Bin}(n,p)\) の確率関数を

$$p_k=\mathrm{P}(X=k),\qquad k=0,\ldots,n$$

とする。

**(1)** \(p_k\) を \(p_{k-1}\) を用いて表せ。\(\{p_0,\ldots,p_n\}\) の中で最大を与える \(k\) を求めよ。

**(2) 掲載範囲**　\(p=1/2\) のとき、\(n=10,\ k=9\) のときの確率と、\(n=20,\ k=18\) のときの…

_PDFはこの箇所で途切れており、(2)の続きは収録されていません。_''',pages='11',section='演習')

deck=dict(version=1,title='連続確率分布と変数変換',description='1005tdh統計勉強会用.pdfの全11ページに基づくスライド',
          plannedMinutes=45,canvas=[1600,900],slides=slides,assets=assets,editorVersion=2,
          sources={'pdf':{'title':'1005tdh統計勉強会用.pdf','detail':'全11ページ。第2章の抜粋：紙面26–28、正規分布の導入、32–33、変数変換の導入、35–38。書名・著者は提供範囲内に記載なし。','url':''}},
          referenceNote='提供PDFの掲載範囲に準拠。定義2.8–2.9、命題2.13、2.15–2.20と各証明を掲載。演習問1(2)は原資料内で途切れている。',
          sections=[{'id':'2.2.1','title':'連続確率分布と特性値'},{'id':'2.2.5','title':'正規分布'},{'id':'2.3','title':'確率変数の関数の分布と変数変換'},{'id':'演習','title':'二項分布の演習'}],
          design={'font':'Yu Gothic, Meiryo','titlePt':24,'bodyPt':20,'background':'#ffffff','editorFields':['theme','title','takeaway','leftMarkdown','rightHTML']})

# Replace the entire original slide payload and all content-specific diagram presets.
html=re.sub(r'(<script id="deck-data" type="application/json">)[\s\S]*?(</script>)',lambda m:m[1]+json.dumps(deck,ensure_ascii=False,indent=2).replace('<','\\u003c')+m[2],template)
html=re.sub(r'(<script id="diagram-engine">)[\s\S]*?(</script>)',lambda m:m[1]+'\n/* Diagram hooks retained for the slide framework. */\nconst DIAGRAM_NAMES={};\nfunction diagramHTML(){return "";}\nfunction bindDiagramEvents(){}\n'+m[2],html)
html=html.replace('仮説検定と信頼区間 | 45分スライド','連続確率分布と変数変換 | TDH統計勉強会')
html=html.replace('STATISTICS / 仮説検定と信頼区間','連続確率分布と変数変換')
html=html.replace(r'9\.\d+',r'\d+\.\d+')
html=html.replace("s.majorSection=number[1];s.subsection=number[0];s.section=number[0];", "s.majorSection=deck.sections?.find(x=>s.title.startsWith(x.id+'　')||s.title.startsWith(x.id+' '))?.id||number[1];s.subsection=number[0];s.section=number[0];")
html=html.replace('資料の記述についての質問','補足スライド')
html=html.replace('資料にない補足はオレンジの質問にまとめています。','テーマ色を選んで、説明・証明・質問を区別できます。')
html=html.replace('通常のスライド送りは本編<span id="help-main-count">40</span>枚だけを進みます。質問<span id="help-appendix-count">1</span>枚は「目次」から開けます。画面に図のスライダーがある場合は、値を変えて説明できます。左右のスワイプでも送れます。',f'通常のスライド送りは本編<span id="help-main-count">{len(slides)}</span>枚を進みます。補足<span id="help-appendix-count">0</span>枚は「目次」から開けます。左右のスワイプでも送れます。')
html=html.replace('質問も含めて印刷','すべてのスライドを印刷')
html=html.replace("'stat-slides-v1-'","'tdh-continuous-slides-v1-'")
# Keep original geometry, colours, editor, navigation, presenter mode and print support.
out=root/'output/html';out.mkdir(parents=True,exist_ok=True)
dest=out/'1005tdh統計勉強会_連続確率分布と変数変換.html'
dest.write_text(html,encoding='utf-8')
print(f'Created {dest} ({len(slides)} slides, {dest.stat().st_size} bytes)')
