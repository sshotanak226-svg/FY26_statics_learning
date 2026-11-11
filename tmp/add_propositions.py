from pathlib import Path
import json, re, copy, sys

sys.stdout.reconfigure(encoding='utf-8')
source = Path(r'C:\Users\User\Downloads\９章　仮説検定と信頼区間_編集済み (14).html')
target = Path(r'F:\Document\Fy26 TDH statics lean\output\９章_仮説検定と信頼区間_命題ページ追加.html')
html = source.read_text(encoding='utf-8')
match = re.search(r'(<script id="deck-data" type="application/json">)([\s\S]*?)(</script>)', html)
deck = json.loads(match.group(2))
original = copy.deepcopy(deck)
by_id = {s['id']: s for s in deck['slides']}

def proposition(before, ident, title, takeaway, body, markdown, notes):
    slide = copy.deepcopy(by_id[before])
    slide.update(id=ident, title=title, takeaway=takeaway, body=body,
                 leftMarkdown=markdown, rightHTML='', minutes=0.65,
                 notes=notes, equations=[], diagram='', table=[], flow=[], answers=[])
    slide.pop('role', None)
    return slide

additions = {}
additions['ump-general'] = proposition(
    'ump-general', 'ump-proposition', '9.3.1　定理9.2：一様最強力性の命題',
    '各対立値で得られる最強力検定が共通なら、複合対立仮説に対して一様最強力となる。',
    ['単純対立仮説ごとの有意水準αの尤度比検定の棄却域をRθ₁とする。',
     '検定関数φは共通の棄却域Rに対応し、φ′は同じ第一種誤り確率を持つ任意の検定とする。'],
    r'''- $H_0:\theta=\theta_0$ に対する各 $H_1:\theta=\theta_1>\theta_0$ の最強力検定（有意水準 $\alpha$）の棄却域を $R_{\theta_1}$ とする。

$$
R_{\theta_1}=R\quad(\forall\theta_1>\theta_0)
\quad\Longrightarrow\quad
E_{\theta_1}[\varphi(\boldsymbol X)]
\ge E_{\theta_1}[\varphi'(\boldsymbol X)]
\quad(\forall\theta_1>\theta_0).
$$

- $\varphi=\mathbf 1_R$、$\varphi'$ は $E_{\theta_0}[\varphi'(\boldsymbol X)]=\alpha$ を満たす任意の検定関数。

- 結論：$H_1:\theta>\theta_0$ のどの対立値でも検出力が最大、すなわち**一様最強力**。''',
    'PDF 11ページ（紙面134、定理9.2）。各単純対立仮説の最強力性を前提とし、棄却域が対立値に依存しないことから一様最強力性を示す。')

wilks = by_id['wilks']
wilks.update(
    title='9.3.2　定理9.3：尤度比の漸近分布の命題',
    takeaway='帰無仮説が真で正則条件を満たすとき、変換した尤度比はカイ二乗分布に収束する。',
    body=['母数空間と帰無仮説の母数空間の次元をそれぞれm、kとする。',
          '次の証明では一母数の点帰無仮説、すなわちm=1、k=0の場合を扱う。'],
    leftMarkdown=r'''- 尤度比を $\displaystyle\Lambda(\boldsymbol X)=\frac{\max_{\theta\in\Theta_0}L(\theta\mid\boldsymbol X)}{\max_{\theta\in\Theta}L(\theta\mid\boldsymbol X)}$ とする。

$$
\left.
\begin{gathered}
\theta\in\Theta_0,\qquad \text{正則条件が成立},\\
\dim\Theta=m,\qquad\dim\Theta_0=k<m
\end{gathered}
\right\}
\quad\Longrightarrow\quad
-2\log\Lambda(\boldsymbol X)\xrightarrow{d}\chi^2_{m-k}.
$$

- この極限分布から、有意水準 $\alpha$ の近似的な棄却域を得る。

$$
R=\{-2\log\Lambda(\boldsymbol X)>\chi^2_{m-k,\alpha}\}.
$$

- 次の証明は $\theta\in\mathbb R$、$\Theta_0=\{\theta_0\}$（$m=1,\ k=0$）の場合を扱う。''',
    rightHTML='', equations=[],
    notes='PDF 12–13ページ（紙面135–136、定理9.3）。一般の正則モデルでの結論を先に示す。続く証明①・②は原資料と同じく一母数の点帰無仮説（m=1、k=0）に限定する。境界や非正則モデルに無条件に適用するものではない。')

additions['ump-proof'] = proposition(
    'ump-proof', 'normal-ump-proposition', '9.3.1　正規平均の一様最強力性の命題',
    '既知分散の正規母集団では、標本平均の右片側検定が一様最強力となる。',
    ['既知分散の正規標本で平均がμ₀より大きいかを検定する。',
     '右片側検定が全てのμ>μ₀で最大の検出力を持つことを示す。'],
    r'''- $X_1,\ldots,X_n\overset{\mathrm{iid}}{\sim}N(\mu,\sigma_0^2)$（$\sigma_0^2$ は既知）。$H_0:\mu=\mu_0$、$H_1:\mu>\mu_0$。

$$
R=\left\{\frac{\sqrt n(\bar X-\mu_0)}{\sigma_0}>z_\alpha\right\}
\quad\Longrightarrow\quad
E_\mu[\varphi(\boldsymbol X)]\ge E_\mu[\varphi'(\boldsymbol X)]
\quad(\forall\mu>\mu_0).
$$

- $\varphi=\mathbf 1_R$、$z_\alpha$ は標準正規分布の上側 $\alpha$ 点。$\varphi'$ は $E_{\mu_0}[\varphi'(\boldsymbol X)]=\alpha$ を満たす任意の検定関数。

- 結論：この右片側検定は $H_1:\mu>\mu_0$ に対して**一様最強力**。''',
    'PDF 9–11ページ（紙面132–134）。既知分散の正規平均の片側検定に関する命題。続くページでは単純対立仮説ごとの尤度比を計算し、棄却域がμ₁に依存しないことを示す。')

additions['ci-proof'] = proposition(
    'ci-proof', 'ci-coverage-proposition', '9.6.1　信頼集合の被覆確率の命題',
    '各候補の受容域を反転すると、被覆確率が1−αの信頼集合が得られる。',
    ['各候補θ₀に対する受容確率が1−αとなる受容域を用いる。',
     'その受容域を反転した集合が、真の母数を確率1−αで含むことを示す。'],
    r'''- $A(\theta_0)$ を $H_0:\theta=\theta_0$ に対する検定の受容域とする。

$$
\left.
\begin{gathered}
P_{\theta_0}\{\boldsymbol X\in A(\theta_0)\}=1-\alpha
\quad(\forall\theta_0\in\Theta),\\[4pt]
C(\boldsymbol x)=\{\theta_0\in\Theta:\boldsymbol x\in A(\theta_0)\}
\end{gathered}
\right\}
\quad\Longrightarrow\quad
\begin{gathered}
P_\theta\{\theta\in C(\boldsymbol X)\}=1-\alpha\\
(\forall\theta\in\Theta).
\end{gathered}
$$

- 結論：$C(\boldsymbol X)$ は信頼係数 $1-\alpha$ の**信頼集合**。''',
    'PDF 21–22ページ（紙面144–145、定義9.8と検定の反転）。ここでは原資料に合わせ、各母数での受容確率が厳密に1−αとなる場合を述べる。')

slides = []
for slide in deck['slides']:
    if slide['id'] in additions:
        slides.append(additions[slide['id']])
    slides.append(slide)
deck['slides'] = slides
assert len(slides) == len(original['slides']) + 3
assert len({s['id'] for s in slides}) == len(slides)
for old in original['slides']:
    if old['id'] != 'wilks':
        assert old == next(s for s in slides if s['id'] == old['id']), old['id']
serialized = json.dumps(deck, ensure_ascii=False, indent=2).replace('<', r'\u003c')
result = html[:match.start(2)] + '\n' + serialized + '\n' + html[match.end(2):]
assert result[:match.start(2)] == html[:match.start(2)]
assert result.endswith(html[match.end(2):])
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(result, encoding='utf-8')
print(target)
for i, slide in enumerate(slides, 1):
    if slide['id'] in {s['id'] for s in additions.values()} | {'wilks'}:
        print(i, slide['title'])
