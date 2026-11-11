from pathlib import Path
import copy
import json
import re

src = Path('output/９章_仮説検定と信頼区間_発表者ポインタ連動.html')
dst = Path('output/９章_仮説検定と信頼区間_有意水準の説明補足.html')
html = src.read_text(encoding='utf-8')
match = re.search(r'<script id="deck-data" type="application/json">(.*?)</script>', html, re.S)
deck = json.loads(match[1])
before = copy.deepcopy(deck)

s = deck['slides'][7]
old = '- 第一種の誤りを有意水準で抑え、その条件の下で検出力を比較する。'
assert old in s['leftMarkdown']
s['leftMarkdown'] = s['leftMarkdown'].replace(old, '- 有意水準は、帰無仮説が真のときに誤って帰無仮説を棄却する確率の許容上限である。利用者は観測前に有意水準を定める。')
s['notes'] = s['notes'].replace('- 有意水準は、帰無仮説が正しい場合の誤った棄却の確率を抑える基準である。', '- 有意水準は、帰無仮説が真の場合に誤って帰無仮説を棄却する確率の許容上限である。利用者は標本の観測前に有意水準を定める。')

s = deck['slides'][10]
s['takeaway'] = '有意水準は、帰無仮説が真のときの「誤った棄却」の確率に対する許容上限である。'
s['leftMarkdown'] = r'''- **有意水準 $\alpha$**：利用者が標本の観測前に定める、第一種誤りの確率の許容上限。

- 利用者は、帰無仮説を満たすどの母数値でも誤った棄却の確率が $\alpha$ 以下となるように、棄却域 $R$ を定める。

$$
P_{\theta_0}(\boldsymbol X\in R)\le\alpha
\qquad(\forall\theta_0\in\Theta_0).
$$

- $\alpha=0.05$ は、帰無仮説が真のときに検定が帰無仮説を誤って棄却する確率の上限を **5％** とする設定である。

- **検出力**は、対立仮説が真のときに検定が帰無仮説を棄却する確率である。

$$
\beta(\theta_1)=E_{\theta_1}[\varphi(\boldsymbol X)]
=P_{\theta_1}(\boldsymbol X\in R).
$$

- **第二種誤りの確率**は $P_{\theta_1}(\boldsymbol X\in A)=1-\beta(\theta_1)$ である。利用者は、有意水準をそろえて検定の検出力を比較する。'''
s['notes'] = r'''- 利用者は、標本を観測する前に有意水準 α を定める。有意水準 α は、帰無仮説が真のときに検定が帰無仮説を誤って棄却する確率の許容上限である。
- 利用者は、帰無仮説を満たす各母数値で第一種誤りの確率が α 以下となるように、棄却域 R を定める。実際の誤りの確率と α は必ずしも等しくない。
- 有意水準 5％ の検定では、帰無仮説が真の母集団から標本を取り直して検定を繰り返すと、誤った棄却の割合は長期的に 5％ 以下となる。
- 検出力 β(θ1) は、対立値 θ1 の下で検定が帰無仮説を棄却する確率である。第二種誤りの確率は 1−β(θ1) である。
- 利用者は、第一種誤りに対する許容上限をそろえた上で、異なる検定の検出力を比較する。'''

for i, (old_slide, new_slide) in enumerate(zip(before['slides'], deck['slides'])):
    if i not in (7, 10):
        assert old_slide == new_slide, i
assert len(deck['slides']) == len(before['slides']) == 88
serialized = json.dumps(deck, ensure_ascii=False, separators=(',', ':')).replace('</script', '<\\/script')
result = html[:match.start(1)] + serialized + html[match.end(1):]
assert result[:match.start(1)] == html[:match.start(1)]
assert result[result.index('</script>', match.start(1)):] == html[match.end(1):]
dst.write_text(result, encoding='utf-8')
print('Updated pages 8 and 11 only. All 88 slides and application features preserved.')
