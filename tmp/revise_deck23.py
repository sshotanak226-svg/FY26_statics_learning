import copy
import json
import re
from html import escape as html_escape
from pathlib import Path

SOURCE=Path(r'C:\Users\User\Downloads\９章　仮説検定と信頼区間_編集済み (23).html')
TARGET=Path(r'F:\Document\Fy26 TDH statics lean\output\９章_仮説検定と信頼区間_検定例統一_表示修正.html')
html=SOURCE.read_text(encoding='utf-8')
pat=r'(<script[^>]*id="deck-data"[^>]*>)(.*?)(</script>)'
match=re.search(pat,html,re.S);original=json.loads(match[2]);deck=copy.deepcopy(original)
examples=[];layout_only=[]

def eq(s):return '\n\n$$\n'+s.strip()+'\n$$\n\n'
def detail(title,content):return '<div class="example-detail"><h3>'+title+'</h3>'+content+'</div>'
def paragraph(text):return '<p>'+html_escape(text).replace('&lt;br&gt;','<br>')+'</p>'
def formula(tex):return '<div class="detail-equation">$$'+html_escape(tex)+'$$</div>'
def example(page,setup,hyp,reason,stat,calculation,region,right=None,takeaway=None):
 s=deck['slides'][page-1]
 s['leftMarkdown']=('- **仮説検定**：'+setup+eq(hyp)+
                    '- **計算する統計量**：'+reason+eq(stat)+
                    '- **棄却域の計算**：'+calculation+eq(region)).strip()
 s['body']=[setup,reason,calculation];s['testExample']=True
 if right is not None:s['rightHTML']=right
 if takeaway:s['takeaway']=takeaway
 examples.append(page)

# A concrete simple-vs-simple example; the LR=1 rule has size .172, not .05.
example(5,'10回の表の回数を $K$ とし、二つの表確率を比べる。',
 r'H_0:\theta=0.5,\qquad H_1:\theta=0.7.',
 '$K$ が大きいほど対立側の尤度が高くなるので、尤度比で比較する。',
 r'\log\Lambda=10\log(5/3)-K\log(7/3),\quad\Lambda=\frac{L(0.5)}{L(0.7)}.',
 'この例では尤度比1を境界にする。有意水準5%の規則ではない。',
 r'\Lambda<1\iff K>6.03\iff K\ge7,\qquad\mathcal R=\{K\ge7\}.',
 right=deck['slides'][4]['rightHTML']+paragraph(r'$P_{0.5}(K\ge7)\approx0.172$<br>$P_{0.7}(K\le6)\approx0.350$'),
 takeaway='表の回数は尤度比と単調に対応する。棄却域の良さは誤り確率でも評価する。')

ump_comparison=detail('一様最強力性',paragraph('同じ有意水準の検定の中で、すべての対立値に対して検出力が最大。')+formula(r'E_\mu[\varphi]\ge E_\mu[\varphi^{\prime}]\quad(\forall\mu>\mu_0)')+paragraph(r'$E_{\mu_0}[\varphi^{\prime}]\le\alpha$ を満たす任意の検定と比較する。'))
example(18,r'独立な正規標本で、母分散 $\sigma_0^2$ は既知。',
 r'H_0:\mu=\mu_0,\qquad H_1:\mu>\mu_0.',
 '帰無値からの平均差を標準誤差で割り、右方向のずれを測る。',
 r'W=\frac{\sqrt n(\bar X-\mu_0)}{\sigma_0}\overset{H_0}{\sim}N(0,1).',
 r'標準正規分布の上側 $\alpha$ 点を使う。この境界は対立値によらない。',
 r'P_{\mu_0}(W>z_\alpha)=\alpha,\qquad\mathcal R=\{W>z_\alpha\}.',
 right=ump_comparison,
 takeaway='既知分散の正規平均では、右側へ標準化した平均差で一様最強力検定を作れる。')
example(19,r'既知分散の正規標本。任意の $\mu_1>\mu_0$ と比べる。',
 r'H_0:\mu=\mu_0,\qquad H_1:\mu>\mu_0.',
 '帰無側／対立側の尤度比は標本平均の増加で減少するので、$W$ を使える。',
 r'\begin{aligned}\log\frac{L(\mu_0)}{L(\mu_1)}&=-\frac{n(\mu_1-\mu_0)}{\sigma_0^2}(\bar X-\mu_0)+\frac{n(\mu_1-\mu_0)^2}{2\sigma_0^2},\\[3pt]W&=\frac{\sqrt n(\bar X-\mu_0)}{\sigma_0}\overset{H_0}{\sim}N(0,1).\end{aligned}',
 r'帰無分布の上側 $\alpha$ 点で決める。全ての対立値で同じ棄却域となる。',
 r'\mathcal R=\{W>z_\alpha\}\quad\Longrightarrow\quad H_1:\mu>\mu_0\ \text{に対して一様最強力}.',
 right='',takeaway='尤度比の単調性と、帰無分布で定める共通の境界が一様最強力性を与える。')

example(25,r'$X_i$ は独立な $N(\mu,\sigma_0^2)$ 標本。母分散は既知。',
 r'H_0:\mu=\mu_0,\qquad H_1:\mu\ne\mu_0.',
 '平均のずれを標準誤差で割って二乗すると、両方向のずれを評価できる。',
 r'\begin{gathered}Z=\frac{\sqrt n(\bar X-\mu_0)}{\sigma_0},\\[3pt]D=-2\log\Lambda=Z^2\overset{H_0}{\sim}\chi_1^2,\qquad\Lambda=e^{-D/2}.\end{gathered}',
 r'上側 $\alpha$ 点を用いる。$\chi^2_{1,\alpha}=z_{\alpha/2}^{\,2}$ なので両側検定になる。',
 r'\mathcal R=\{D>\chi^2_{1,\alpha}\}=\left\{|\bar X-\mu_0|>\frac{\sigma_0 z_{\alpha/2}}{\sqrt n}\right\}.',
 right='',takeaway='既知の標準誤差で測った平均のずれの二乗が、厳密なχ²検定の統計量になる。')

pooled_detail=detail('尤度比を計算する平方和',
 paragraph(r'$N=m+n,\ \nu=N-2$。各群の平均で測る平方和を $U$ とする。')+
 formula(r'\begin{aligned}U&=\textstyle\sum_i(X_i-\bar X)^2\\&\quad+\textstyle\sum_j(Y_j-\bar Y)^2,\\[4pt]U_0&=U+\frac{mn}{N}(\bar X-\bar Y)^2.\end{aligned}')+
 paragraph('共通平均に制約すると平方和が増え、最大尤度は下がる。')+
 formula(r'\Lambda=\frac{\max_{H_0}L}{\max_{\Theta}L}=\left(\frac{U}{U_0}\right)^{N/2}.'))
example(27,r'独立な正規二標本。未知の母分散 $\sigma^2$ は共通。',
 r'H_0:\mu_X=\mu_Y,\qquad H_1:\mu_X\ne\mu_Y.',
 '平均を等しく制約した際の最大尤度の低下を $D$ で測る。',
 r'D=-2\log\Lambda=N\log\frac{U_0}{U}.',
 r'$t_\nu$ の上側 $\alpha/2$ 点 $c_\alpha$ を使い、$D$ の境界へ変換する。',
 r'\begin{gathered}c_\alpha=t_{\nu,\alpha/2},\qquad d_\alpha=N\log\!\left(1+\frac{c_\alpha^2}{\nu}\right),\\[3pt]\mathcal R=\{D>d_\alpha\}.\end{gathered}',
 right=pooled_detail)

example(28,'独立な正規二標本で、未知の母分散が等しい場合。',
 r'H_0:\mu_X=\mu_Y,\qquad H_1:\mu_X\ne\mu_Y.',
 '帰無分布が既知の $T$ に直すと、有意水準から境界を決められる。',
 r'\begin{gathered}\hat\sigma_U^2=\frac{U}{N-2},\quad T=\frac{\bar X-\bar Y}{\hat\sigma_U\sqrt{1/m+1/n}},\\[3pt]D=N\log\!\left(1+\frac{T^2}{N-2}\right).\end{gathered}',
 '$D$ は $T^2$ の増加関数なので、同じ棄却域を表す。',
 r'\mathcal R=\{D>d_\alpha\}=\{|T|>t_{N-2,\alpha/2}\}.',
 takeaway='統計量をTに書き換えると、同じ棄却域を既知のt分布から計算できる。')

pooled_t_proof=detail('厳密なt分布になる理由',
 paragraph(r'$H_0$ の下で平均差は正規分布、群内平方和はχ²分布に従う。')+
 formula(r'Z=\frac{\bar X-\bar Y}{\sigma\sqrt{1/m+1/n}}\sim N(0,1).')+
 formula(r'W=\frac{U}{\sigma^2}\sim\chi^2_{(m-1)+(n-1)}.')+
 paragraph('正規標本では標本平均と群内平方和が独立。')+
 formula(r'Z\perp W,\qquad T=\frac{Z}{\sqrt{W/(N-2)}}.'))
example(29,'正規性・両群の独立性・共通母分散を仮定する。',
 r'H_0:\mu_X=\mu_Y,\qquad H_1:\mu_X\ne\mu_Y.',
 '標準化した平均差は、独立な正規変数とχ²変数の比になる。',
 r'T=\frac{\bar X-\bar Y}{\hat\sigma_U\sqrt{1/m+1/n}}\overset{H_0}{\sim}t_{N-2}.',
 r'上側 $\alpha/2$ 点で両裾を切る。これは有限標本でも厳密な検定。',
 r'\mathcal R=\{|T|>t_{N-2,\alpha/2}\},\qquad P_{H_0}(\boldsymbol X\in\mathcal R)=\alpha.',
 right=pooled_t_proof)

welch_detail=detail('Welchの自由度',paragraph(r'$V_1^2,V_2^2$ は各群の不偏分散。分母の平均・分散をχ²分布に合わせる。')+
 formula(r'\hat\nu_W=\frac{(V_1^2/m+V_2^2/n)^2}{\dfrac{(V_1^2/m)^2}{m-1}+\dfrac{(V_2^2/n)^2}{n-1}}.')+
 paragraph('原資料では自由度の整数部分を用いる。')+formula(r'\nu=\lfloor\hat\nu_W\rfloor.')+
 paragraph('厳密なt分布ではなく、自由度を合わせた近似。導出は83ページ。'))
example(30,'独立な正規二標本。両群の母分散が等しいとは仮定しない。',
 r'H_0:\mu_X=\mu_Y,\qquad H_1:\mu_X\ne\mu_Y.',
 '各群の分散を別々に推定し、平均差をその標準誤差で割る。',
 r'T=\frac{\bar X-\bar Y}{\sqrt{V_1^2/m+V_2^2/n}}.',
 r'$H_0$ での分布を $t_\nu$ で近似し、上側 $\alpha/2$ 点を使う。',
 r'\mathcal R=\{|T|>t_{\nu,\alpha/2}\}.',right=welch_detail,
 takeaway='等分散を仮定しない平均差は、各群の分散で標準化し、Welchのt近似で検定する。')

example(31,'独立な正規二標本。$V_1^2,V_2^2$ は各群の不偏分散。',
 r'H_0:\sigma_1^2=\sigma_2^2,\qquad H_1:\sigma_1^2\ne\sigma_2^2.',
 '分散の比を取ると、帰無仮説の共通母分散が打ち消される。',
 r'F=\frac{V_1^2}{V_2^2}\overset{H_0}{\sim}F_{m-1,n-1}.',
 r'上側確率 $p$ の点を $F_{a,b,p}$ とし、両裾に $\alpha/2$ ずつ配分する。',
 r'\mathcal R=\{F<F_{m-1,n-1,1-\alpha/2}\}\cup\{F>F_{m-1,n-1,\alpha/2}\}.',
 takeaway='等裾の両側F検定は正規性の下で厳密。尤度比検定とは一般に棄却域が異なる。')

example(32,'対応差 $Z_i=X_i-Y_i$ を作る。組同士は独立で、差は正規分布。',
 r'H_0:\mu_X-\mu_Y=0,\qquad H_1:\mu_X-\mu_Y\ne0.',
 '差を一つの標本として扱うことで、組内の相関を反映できる。',
 r'\begin{gathered}V_Z^2=\frac{\sum_{i=1}^n(Z_i-\bar Z)^2}{n-1},\\[3pt]T=\frac{\sqrt n\,\bar Z}{V_Z}\overset{H_0}{\sim}t_{n-1}.\end{gathered}',
 '差の標本数 $n$ から自由度を決め、両側の境界と比べる。',
 r'\mathcal R=\{|T|>t_{n-1,\alpha/2}\}.',
 takeaway='対応のある二標本は、各組の差を用いる一標本のt検定として扱う。')

example(34,r'1母数の正則なモデルで、最尤推定量 $\hat\theta$ を用いる。',
 r'H_0:\theta=\theta_0,\qquad H_1:\theta\ne\theta_0.',
 '推定誤差を情報量から求めた標準誤差で割り、尺度をそろえる。',
 r'W=\sqrt{nI(\hat\theta)}(\hat\theta-\theta_0)\xrightarrow[H_0]{d}N(0,1).',
 r'標準正規分布の上側 $\alpha/2$ 点を使う大標本の近似検定。',
 r'\mathcal R=\{|W|>z_{\alpha/2}\}.',
 takeaway='Wald検定は、推定値と帰無値の差を推定標準誤差で割り、正規近似で判断する。')
example(35,'独立なベルヌーイ標本の母比率を検定する。大標本を仮定。',
 r'H_0:\theta=\theta_0,\qquad H_1:\theta\ne\theta_0.',
 '標本比率の分散を推定し、帰無値との差を標準誤差で割る。',
 r'\hat\theta=\bar X,\qquad W=\frac{\bar X-\theta_0}{\sqrt{\bar X(1-\bar X)/n}}.',
 r'$0<\bar X<1$ で標準正規近似を使い、両側の境界と比べる。',
 r'\mathcal R=\{|W|>z_{\alpha/2}\}.',
 takeaway='ベルヌーイ母数のWald検定は、標本比率の推定標準誤差で差を評価する。')
example(36,'独立同分布で、有限の正の分散を持つ標本。正規性は仮定しない。',
 r'H_0:\mu=\mu_0,\qquad H_1:\mu\ne\mu_0.',
 '中心極限定理を使うため、平均差を推定標準誤差で割る。',
 r'S^2=\frac1n\sum_i(X_i-\bar X)^2,\qquad W=\frac{\sqrt n(\bar X-\mu_0)}S\xrightarrow[H_0]{d}N(0,1).',
 '十分に大きい標本では標準正規分布の両側境界を使える。',
 r'\mathcal R=\{|W|>z_{\alpha/2}\}=\{\sqrt n\,|\bar X-\mu_0|>S z_{\alpha/2}\}.',
 right='',takeaway='一般の母平均は、標本平均の中心極限定理により大標本で近似検定できる。')
example(37,'夫婦ごとの支持指標の差 $Z_i=X_i-Y_i$ を用い、組同士は独立とする。',
 r'H_0:\theta_1=\theta_2,\qquad H_1:\theta_1\ne\theta_2.',
 '差の平均は支持率差を推定し、差の分散は夫婦内の依存も反映する。',
 r'\begin{gathered}\bar Z=\bar X-\bar Y,\qquad S^2=\frac1n\sum_i(Z_i-\bar Z)^2,\\[3pt]W=\frac{\sqrt n\,\bar Z}{S}\xrightarrow[H_0]{d}N(0,1).\end{gathered}',
 '十分な組数と $S>0$ の下で、標準正規近似による両側検定を行う。',
 r'\mathcal R=\{|W|>z_{\alpha/2}\}.',right='',
 takeaway='夫婦の支持率は独立な二群として扱わず、各夫婦の回答差を標準化して比べる。')

example(50,'独立な二変量正規の観測組。標本相関を $r=R_{XY}$ とする。',
 r'H_0:\rho=0,\qquad H_1:\rho\ne0.',
 '標本相関を回帰係数のt統計量に変換すると、既知の帰無分布を使える。',
 r'T=\frac{\sqrt{n-2}\,r}{\sqrt{1-r^2}}\overset{H_0}{\sim}t_{n-2}.',
 '自由度 $n-2$ のt分布の両側境界を使う（$n>2$）。',
 r'\mathcal R=\{|T|>t_{n-2,\alpha/2}\}.',right='',
 takeaway='二変量正規の無相関検定では、標本相関を変換したTが厳密なt分布に従う。')
example(51,'独立な二変量正規の観測組で、指定した母相関を検定する。',
 r'H_0:\rho=\rho_0,\qquad H_1:\rho\ne\rho_0.',
 'Fisher変換で分散をほぼ一定にし、帰無値からのずれを標準化する。',
 r'\begin{gathered}z=\frac12\log\frac{1+r}{1-r},\quad\xi_0=\frac12\log\frac{1+\rho_0}{1-\rho_0},\\[3pt]W=\sqrt{n-3}(z-\xi_0).\end{gathered}',
 '$n>3$ で、大標本では $H_0$ の下の $W$ を標準正規分布で近似する。',
 r'\mathcal R=\{|W|>z_{\alpha/2}\}.',
 takeaway='Fisher変換により、零以外の母相関についても正規近似で検定できる。')
example(52,'47都道府県の出生率と死亡率。独立な二変量正規の観測を仮定する。',
 r'H_0:\rho=0,\qquad H_1:\rho\ne0.',
 '標本相関をt統計量に変換し、無相関のときのばらつきと比較する。',
 r'n=47,\quad r=-0.603,\quad T=\frac{\sqrt{45}\,r}{\sqrt{1-r^2}}\approx-5.07.',
 '有意水準5%の両側境界を超えるため、無相関を棄却する。',
 r'\mathcal R=\{|T|>t_{45,0.025}\},\qquad |T|\approx5.07>2.014.',
 takeaway='標本相関−0.603を帰無分布で評価すると、有意水準5%で無相関を棄却する。')

unknown_setup=r'独立な正規標本。母平均・母分散はともに未知（$n\ge2$）。'
unknown_hyp=r'H_0:\mu=\mu_0,\qquad H_1:\mu\ne\mu_0.'
unknown_defs=detail('分散の推定と尤度比',
 formula(r'\begin{aligned}\hat\sigma^2&=\frac1n\sum_i(X_i-\bar X)^2,\\\hat\sigma_0^2&=\frac1n\sum_i(X_i-\mu_0)^2,\\V^2&=\frac{n\hat\sigma^2}{n-1}.\end{aligned}')+
 paragraph('帰無値で測る平方和は、最小の平方和に平均差の二乗が加わる。')+
 formula(r'\hat\sigma_0^2=\hat\sigma^2+(\bar X-\mu_0)^2.'))
example(77,unknown_setup,unknown_hyp,
 '帰無値を課したときの尤度低下を、推定分散の比から計算する。',
 r'D=-2\log\Lambda=n\log\frac{\hat\sigma_0^2}{\hat\sigma^2}.',
 r'$t_{n-1}$ の上側 $\alpha/2$ 点を、対数尤度比の境界へ変換する。',
 r'\begin{gathered}d_\alpha=n\log\!\left(1+\frac{t_{n-1,\alpha/2}^{\,2}}{n-1}\right),\\[3pt]\mathcal R=\{D>d_\alpha\}.\end{gathered}',right=unknown_defs)

unknown_transform=detail('尤度比をTの式に直す',paragraph(r'$n\hat\sigma^2=(n-1)V^2$ を代入する。')+
 formula(r'\begin{aligned}\Lambda&=\left(1+\frac{n(\bar X-\mu_0)^2}{n\hat\sigma^2}\right)^{-n/2}\\[7pt]&=\left(1+\frac{T^2}{n-1}\right)^{-n/2}.\end{aligned}')+
 paragraph('近似ではなく等式。T²が大きいほど尤度比は小さくなる。'))
example(78,unknown_setup,unknown_hyp,
 '未知の母標準偏差を $V$ で推定し、平均差を標準化する。',
 r'V^2=\frac{\sum_i(X_i-\bar X)^2}{n-1},\qquad T=\frac{\sqrt n(\bar X-\mu_0)}V.',
 '$T$ の両側境界は、尤度比による境界と厳密に対応する。',
 r'\mathcal R=\{|T|>t_{n-1,\alpha/2}\}=\{\Lambda<c_\alpha\}.',right=unknown_transform)

unknown_equiv=detail('棄却条件の同値変形',paragraph(r'$0<c<1$。負のべき乗なので不等号が反転する。')+
 formula(r'\begin{aligned}\Lambda<c&\iff 1+\frac{T^2}{n-1}>c^{-2/n}\\[7pt]&\iff |T|>\sqrt{(n-1)(c^{-2/n}-1)}.\end{aligned}')+
 paragraph('棄却される標本の集合が同じなので、検定も同じ。'))
example(79,unknown_setup,unknown_hyp,
 '尤度比は $T^2$ の減少関数なので、大きい $|T|$ で同じ判断ができる。',
 r'\Lambda=\left(1+\frac{T^2}{n-1}\right)^{-n/2},\quad T=\frac{\sqrt n(\bar X-\mu_0)}V.',
 r'$c_\alpha$ をt分布の境界に対応させると、有意水準が $\alpha$ になる。',
 r'\begin{gathered}c_\alpha=\left(1+\frac{t_{n-1,\alpha/2}^{\,2}}{n-1}\right)^{-n/2},\\[3pt]\mathcal R=\{\Lambda<c_\alpha\}=\{|T|>t_{n-1,\alpha/2}\}.\end{gathered}',right=unknown_equiv)

unknown_proof=detail('正規分布とχ²分布の比',
 formula(r'Z=\frac{\sqrt n(\bar X-\mu_0)}\sigma\sim N(0,1).')+
 formula(r'U=\frac{(n-1)V^2}{\sigma^2}\sim\chi^2_{n-1}.')+
 paragraph('正規標本では標本平均と不偏分散が独立。')+
 formula(r'Z\perp U,\qquad T=\frac{Z}{\sqrt{U/(n-1)}}.')+
 paragraph('未知のσが打ち消され、t分布の定義に一致する。'))
example(80,unknown_setup,unknown_hyp,
 '正規性による平均と分散の独立性を使うと、$T$ の分布が厳密に分かる。',
 r'T=\frac{\sqrt n(\bar X-\mu_0)}V\overset{H_0}{\sim}t_{n-1}.',
 r'両裾の確率を $\alpha/2$ ずつにする。有限標本でも厳密に成り立つ。',
 r'\mathcal R=\{|T|>t_{n-1,\alpha/2}\},\qquad P_{\mu_0}(\boldsymbol X\in\mathcal R)=\alpha.',right=unknown_proof)
example(81,unknown_setup,unknown_hyp,
 '平均差を推定標準誤差で割り、未知の分散によらないt分布を利用する。',
 r'T=\frac{\bar X-\mu_0}{V/\sqrt n}\overset{H_0}{\sim}t_{n-1}.',
 r't分布の上側 $\alpha/2$ 点を使う。尤度比による判定とも一致する。',
 r'\mathcal R=\{|T|>t_{n-1,\alpha/2}\}=\{\Lambda<c_\alpha\}.',
 takeaway='平均差を推定標準誤差で割ったTにより、有意水準αの厳密な両側検定ができる。')

example(82,'独立な正規二標本で、「平均差」と「分散比」の問いを区別する。',
 r'\begin{aligned}H_0:\mu_1=\mu_2&,\qquad H_1:\mu_1\ne\mu_2,\\H_0:\sigma_1^2=\sigma_2^2&,\qquad H_1:\sigma_1^2\ne\sigma_2^2.\end{aligned}',
 '平均差は各群の標準誤差で割り、分散の違いは不偏分散の比で測る。',
 r'T=\frac{\bar X-\bar Y}{\sqrt{V_1^2/m+V_2^2/n}},\qquad F=\frac{V_1^2}{V_2^2}.',
 r'平均差はWelchの近似、分散比は厳密なF分布を使う。$\nu$ は30ページの自由度。',
 r'\begin{aligned}\mathcal R_\mu&=\{|T|>t_{\nu,\alpha/2}\},\\[3pt]\mathcal R_{\sigma^2}&=\{F<F_{m-1,n-1,1-\alpha/2}\}\cup\{F>F_{m-1,n-1,\alpha/2}\}.\end{aligned}',right='',
 takeaway='検定したい母数を先に定め、平均差には標準誤差、分散の違いには分散比を使う。')

def replace_md(page,md,takeaway=None):
 s=deck['slides'][page-1];s['leftMarkdown']=md.strip();s['body']=[x[2:] for x in md.splitlines() if x.startswith('- ')]
 if takeaway:s['takeaway']=takeaway
 s['safeFlow']=True;layout_only.append(page)

replace_md(4,r'''
- 観測結果を各仮説の下で評価し、尤度比を判断の指標にする。

$$
\frac{p(k\mid H_0)}{p(k\mid H_1)}.
$$

- 帰無仮説を棄却するかどうかの規則でも、誤った判断が起こり得る。
    - 第一種誤り：帰無仮説が真なのに棄却する。
    - 第二種誤り：対立仮説が真なのに帰無仮説を棄却しない。

- 一方の誤りを小さくする際は、もう一方の誤りも確認する。
''')
replace_md(9,r'''
- 第一種誤りは帰無仮説が真なのに棄却する確率。これを有意水準以下に抑える。

$$
P_{\theta_0}(\boldsymbol X\in R)\le\alpha.
$$

- 検出力は、対立仮説が真のときに帰無仮説を棄却できる確率。

$$
\beta(\theta_1)=E_{\theta_1}[\varphi(\boldsymbol X)]
=P_{\theta_1}(\boldsymbol X\in R).
$$

- 第二種誤りの確率は検出力の補数。同じ有意水準の下で検出力を比較する。

$$
P_{\theta_1}(\boldsymbol X\in A)=1-\beta(\theta_1).
$$
''')
replace_md(14,r'''
- **手順1**　同じ第一種誤り確率を持つ検定関数を比較する。

$$
E_{\theta_0}[\varphi]=E_{\theta_0}[\varphi']=\alpha
\quad\Longrightarrow\quad
\int(\varphi-\varphi')f_0\,d\boldsymbol x=0.
$$

- **手順2**　対立側の検出力の差から、帰無側の零となる項を差し引く。

$$
\begin{aligned}
E_{\theta_1}[\varphi-\varphi']
&=\int(\varphi-\varphi')f_1\,d\boldsymbol x
-k\int(\varphi-\varphi')f_0\,d\boldsymbol x\\[4pt]
&=\int(\varphi-\varphi')(f_1-kf_0)\,d\boldsymbol x.
\end{aligned}
$$

- 積分は標本空間全体にわたる。表記を短くするため、次の記号を使った。

$$
f_j=f(\boldsymbol x\mid\theta_j),\qquad
\varphi=\varphi(\boldsymbol x),\quad\varphi'=\varphi'(\boldsymbol x).
$$
''')
replace_md(24,r'''
- **手順1**　大数の法則とスコアの中心極限定理から、曲率と推定誤差の極限を得る。

$$
-\frac{\ell''(\hat\theta)}n\xrightarrow{p}I(\theta_0),
\qquad\sqrt n(\hat\theta-\theta_0)\xrightarrow{d}N\!\left(0,\frac1{I(\theta_0)}\right).
$$

- **手順2**　推定誤差を標準化して二乗する。

$$
Z_n=\sqrt{nI(\theta_0)}(\hat\theta-\theta_0)\xrightarrow{d}N(0,1)
\quad\Longrightarrow\quad Z_n^2\xrightarrow{d}\chi_1^2.
$$

- **手順3**　二次展開へ代入し、スルツキーの定理を使う。

$$
-2\log\Lambda=\frac{-\ell''(\hat\theta)}{nI(\theta_0)}Z_n^2+o_p(1)
\xrightarrow{d}\chi_1^2.
$$
''')
replace_md(46,r'''
- 既知分散の正規標本では、標準正規分布の境界を使う。

- 両側検定で棄却されない母平均を集めると、両側信頼区間になる。

$$
\left[\bar X-z_{\alpha/2}\frac{\sigma_0}{\sqrt n},\quad
\bar X+z_{\alpha/2}\frac{\sigma_0}{\sqrt n}\right].
$$

- 右片側検定を反転すると、下側信頼区間になる。

$$
\left[\bar X-z_\alpha\frac{\sigma_0}{\sqrt n},\quad\infty\right).
$$
''')
replace_md(83,r'''
- $Q$ を平均差の推定分散とする。独立な正規標本では、その平均・分散が求まる。

$$
\begin{aligned}
Q&=V_1^2/m+V_2^2/n,\qquad a=\sigma_1^2/m,\quad b=\sigma_2^2/n,\\
E[Q]&=a+b,\qquad\operatorname{Var}(Q)=2\{a^2/(m-1)+b^2/(n-1)\}.
\end{aligned}
$$

- $Q$ をχ²分布の定数倍で近似し、平均と分散を一致させる。

$$
Q\approx\frac{a+b}{\nu}U,\quad U\sim\chi_\nu^2
\quad\Longrightarrow\quad
\frac{2(a+b)^2}{\nu}=2\left\{\frac{a^2}{m-1}+\frac{b^2}{n-1}\right\}.
$$

- $\nu$ を求め、母分散を不偏分散で置き換える（原資料は整数部分を使用）。

$$
\hat\nu_W=\frac{(V_1^2/m+V_2^2/n)^2}{(V_1^2/m)^2/(m-1)+(V_2^2/n)^2/(n-1)},
\qquad\nu_{\rm used}=\lfloor\hat\nu_W\rfloor.
$$
''')

assert len(examples)==23
for i in examples:
 md=deck['slides'][i-1]['leftMarkdown']
 for token in ['**仮説検定**','**計算する統計量**','**棄却域の計算**','H_0:','H_1:']:
  assert token in md,(i,token)
assert len(deck['slides'])==83
for i,(a,b) in enumerate(zip(original['slides'],deck['slides']),1):
 assert a['id']==b['id']
 assert a.get('notes')==b.get('notes'),('original manuscript changed',i)
 if i not in examples+layout_only:assert a==b
assert original['assets']==deck['assets']

encoded=json.dumps(deck,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
html=html[:match.start(2)]+encoded+html[match.end(2):]
old='class="slide theme-${theme}" data-slide-id='
new='class="slide theme-${theme}${s.testExample?\' test-example\':\'\'}${s.safeFlow?\' safe-flow\':\'\'}" data-slide-id='
assert html.count(old)==1;html=html.replace(old,new)
css='''
<style id="test-example-layout-style">
/* A natural block flow prevents dense formulas from centering into the heading. */
.slide:is(.test-example,.safe-flow) .content{align-items:center;}
.slide:is(.test-example,.safe-flow) .text-block{display:block;height:auto;align-self:center;min-height:0;}
.slide:is(.test-example,.safe-flow) .right-content{min-width:0;height:auto;align-self:center;}
.slide:is(.test-example,.safe-flow) .markdown>.body-list{margin:0 0 7px;}
.slide:is(.test-example,.safe-flow) .markdown>.body-list>li{margin:0;line-height:1.4;}
.slide:is(.test-example,.safe-flow) .markdown p{margin:4px 0 12px;line-height:1.4;}
.slide:is(.test-example,.safe-flow) .katex-display{margin:6px 0;}
.slide:is(.test-example,.safe-flow) .katex-display>.katex>.katex-html{line-height:1.35;}
.slide.test-example .content.has-diagram{grid-template-columns:minmax(0,1.18fr) minmax(0,1fr);gap:42px;}
.slide.test-example .example-detail{border-left:2px solid #ccd9e5;padding-left:28px;line-height:1.45;}
.slide.test-example .example-detail h3{font-size:24pt;line-height:1.4;margin:0 0 18px;color:var(--theme);}
.slide.test-example .example-detail p{margin:12px 0;line-height:1.4;}
.slide.test-example .detail-equation{margin:12px 0;}
.slide.test-example .right-content img{max-width:100%;max-height:440px;object-fit:contain;}
.slide.test-example .right-content>.diagram>svg{max-width:100%;}
.slide.test-example[data-slide-id="pooled-loglr"] .content.has-diagram{grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:32px;}
.slide.test-example .pooled-chart-note{font-size:24pt;line-height:1.35;margin:6px 0 0;}
.slide.test-example .pooled-log-chart svg{max-height:500px;}
.slide.test-example[data-slide-id="coin-model"] .content.has-diagram{grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);}
.slide.test-example[data-slide-id="coin-model"] .right-content>p{margin:12px 0;}
</style>
'''
html=html.replace('</head>',css+'</head>',1)
TARGET.write_text(html,encoding='utf-8')
Path('tmp/deck23-changes.json').write_text(json.dumps({'examples':examples,'otherPages':layout_only,'totalSlides':83,'output':str(TARGET)},ensure_ascii=False,indent=2),encoding='utf-8')
print(TARGET);print('Examples:',examples);print('Other:',layout_only)
