from pathlib import Path
from html import escape
import copy, json, re

src = Path('F:/Download/９章_仮説検定と信頼区間_ベルヌーイ情報量補足.html')
dst = Path('output/９章_仮説検定と信頼区間_区間推定概要改訂.html')
html = src.read_text(encoding='utf-8')
m = re.search(r'(<script id="deck-data" type="application/json">)(.*?)(</script>)', html, re.S)
original = json.loads(m[2])
deck = copy.deepcopy(original)
s = deck['slides'][37]
assert s['id'] == 'intro-9.6'
s['title'] = '9.6　概要：区間推定と信頼区間'
s['takeaway'] = '真の母数を含むように区間を作り、推定の不確かさを幅で表す。'
s['leftMarkdown'] = r'''- 母平均・母比率などの**真の母数 $\theta$** を、標本 $\boldsymbol X$ から作る区間 $[L(\boldsymbol X),U(\boldsymbol X)]$ で推定する。$L$ は下限、$U$ は上限。

- **信頼係数 $1-\alpha$** は、区間が真の母数を含む確率の保証水準（例：95％）。どの真の値でも、

$$
P_\theta\{L(\boldsymbol X)\le\theta\le U(\boldsymbol X)\}\ge1-\alpha.
$$

- **母数は固定、区間は標本ごとに変わる。**'''
def eq(tex):
    return '<div class="detail-equation">$$' + escape(tex) + '$$</div>'
s['rightHTML'] = '<div class="example-detail">' + ''.join([
    '<h3>検定との関係</h3>',
    r'<p>各候補 $\theta_0$ を帰無値として検定し、<strong>棄却されない値を区間に集める。</strong></p>',
    '<h3>例：正規母平均の95％区間</h3>',
    r'<p>母標準偏差 $\sigma$ は既知、$n$ は標本数、$\bar X$ は標本平均。</p>',
    eq(r'\left[\bar X-1.96\frac{\sigma}{\sqrt n},\ \bar X+1.96\frac{\sigma}{\sqrt n}\right].'),
    '<p><strong>9.6では</strong>、最尤推定量・平均・比率の区間を求め、区間幅から必要な標本数を考える。</p>',
]) + '</div>'
s['body'] = [
    '真の母数を、標本から計算する下限と上限の間の区間で推定する。',
    '信頼係数は、繰り返し標本を取り区間を作る方法の被覆確率の保証水準。',
    '検定で棄却されない母数の候補を集め、平均や比率の区間と標本数へ展開する。',
]
s['notes'] = '''対応：アップロード原資料 PDF 21–25ページ（紙面144–148、9.6）。
区間推定の目的は、母平均や母比率といった真の未知の母数を、標本から計算する範囲で推定すること。推定値と真の値を区別する。L(X)とU(X)は標本全体Xを入力にして求める下限・上限で、標本の取り方により変動する。
信頼係数1−αは、どの真の母数の値についても、作った区間がその真の値を含む確率を少なくとも1−αとする保証水準。αはその補数であり、例えば1−α=0.95ならα=0.05。確率は母数θの下で標本Xを繰り返し得ることに対して取る。真の母数自体は固定で、観測後の一本の固定区間にθが入る確率を95％とする解釈ではない。
検定との関係：候補θ0ごとに有意水準αの検定を行い、棄却されない候補を全て集めると、被覆確率が少なくとも1−αの信頼集合を得る。それが区間になる場合を扱う。仮説を棄却しないことは、その仮説の正しさを証明することではない。
具体例：独立なXi~N(μ,σ²)、σ既知。H0:μ=μ0に対する5％両側検定で棄却されない条件は、|sqrt(n)(barX−μ0)/σ|≤z0.025。これをμ0について解くと、barX−z0.025 σ/sqrt(n)≤μ0≤barX+z0.025 σ/sqrt(n)。標準正規の上側2.5％点z0.025を小数第2位まで丸めた1.96を用いて表示した。厳密な点では被覆確率0.95、1.96はその数値近似である。
9.6の展開：信頼区間の定義と検定の反転、信頼係数の解釈、最尤推定量・母平均・比率・対応した比率差の区間、区間の幅と必要標本数。正規モデルの厳密な区間と、大標本での近似区間を区別する。標準誤差が小さいほど同じ信頼係数で区間を狭くでき、典型的には標本数を増やすと半幅が1/sqrt(n)に比例して小さくなる。
'''
assert len(deck['slides']) == len(original['slides'])
assert [i+1 for i,(a,b) in enumerate(zip(original['slides'], deck['slides'])) if a != b] == [38]
encoded = json.dumps(deck, ensure_ascii=False, separators=(',', ':')).replace('</script', '<\\/script')
result = html[:m.start(2)] + encoded + html[m.end(2):]
assert result[:m.start(2)] == html[:m.start(2)]
assert result[result.index('</script>', m.start(2)):] == html[m.end(2):]
scoped_style = '''<style id="ci-overview-layout">
.slide[data-slide-id="intro-9.6"] .text-block{justify-content:center;}
.slide[data-slide-id="intro-9.6"] .example-detail h3{font-size:32px;line-height:1.4;margin:0 0 14px;color:var(--theme);}
.slide[data-slide-id="intro-9.6"] .example-detail h3:not(:first-child){margin-top:26px;}
.slide[data-slide-id="intro-9.6"] .example-detail p{margin:12px 0;line-height:1.45;}
</style>'''
result = result.replace('</head>', scoped_style + '</head>', 1)
dst.write_text(result, encoding='utf-8')
print('Updated only page 38; slide count and all application code preserved.')
