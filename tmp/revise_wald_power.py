from pathlib import Path
import json,re,copy

src=Path('output/９章_仮説検定と信頼区間_ワルド利点欠点比較.html')
dst=Path('output/９章_仮説検定と信頼区間_ワルド検出力比較.html')
html=src.read_text(encoding='utf-8')
m=re.search(r'(<script id="deck-data" type="application/json">)(.*?)(</script>)',html,re.S)
a=json.loads(m[2]);d=copy.deepcopy(a)
i=next(i for i,x in enumerate(d['slides']) if x['id']=='intro-9.5');s=d['slides'][i]
old='<tr><td><strong>欠点</strong></td><td>母数を対数などに変えると結果が変わり得る。尤度比は不変。</td></tr>'
new='<tr><td><strong>検出力</strong></td><td>最強力の保証は両者とも一般にない。正則条件下では局所検出力が漸近的に同等。</td></tr>'
assert old in s['rightHTML']
s['rightHTML']=s['rightHTML'].replace(old,new).replace('尤度比検定に対する利点・欠点','尤度比検定との比較')
s['notes']=re.sub(r'欠点2：[^\n]*\n','',s['notes'])
s['notes']=s['notes'].replace('制約付き再推定の不要性、小標本の近似、再母数化への非不変性','制約付き再推定の不要性、小標本の近似')
s['notes']+='''

【検出力と最強力性の補足】
表の「母数の非線形変換」の行を削除し、検出力の比較へ置き換えた。
「尤度比検定だから常に最強力」とは言えない。ネイマン–ピアソンの補題が保証するのは、帰無側と対立側の標本分布がそれぞれ一つに決まる単純仮説同士の問題で、有意水準αに調整された尤度比検定の最強力性。余分な未知母数が残る場合は、θ=θ0と書いてあるだけで単純仮説になるとは限らない。
母数を最大化して作る一般化尤度比検定では、複合仮説・両側仮説に対して一般的な最強力性や一様最強力性の保証はない。単調尤度比など追加の構造により一様最強力性を示せる場合もあるが、個別に証明が必要。
通常のWald検定も、有限標本で最強力または一様最強力という一般的な保証はない。ただし特定のモデルでは尤度比検定と同じ棄却域になり、そこで証明された最適性を共有することはある。Waldの検出力が尤度比より常に低いという序列もない。
表の「正則条件下の局所検出力が漸近的に同等」は、正則な同一尤度モデルで効率的な最尤推定量と一致性のある分散推定を用い、同じ仮説・同じ漸近有意水準のWald検定と尤度比検定を比べる場合の結果。一般の任意の推定量を使ったWald型検定すべてについて、尤度比との同等性を主張するものではない。
局所対立仮説とは、標本数とともに帰無値へ近づく対立値、例えばθn=θ0+h/sqrt(n)（hは固定）を指す。この局所対立の下でWaldの二乗Wn²と−2 log Λnの差が確率的に0へ収束し、共通の非心χ²分布に収束するため、棄却確率の極限が同じになる。
帰無値から固定的に離れた対立値で、一致性のある両検定の検出力が1へ近づくだけでは、検出力の細かな比較にはならない。そのため帰無値付近の局所検出力で比較する。有限標本で数値として常に同じ検出力になるわけでも、全ての対立値で同じ検出力になるわけでもない。
参照：UC Berkeley, Stat 210a, Hypothesis Testing and the Neyman-Pearson Lemma, §3.1（単純仮説同士の最強力性）：
https://stat210a.berkeley.edu/fall-2025/reader/hypothesis-testing.html
参照：Daniel McFadden, Statistical Tools, Chapter7, §7.6、紙面155ページ（尤度比統計量とWald統計量の漸近同等性と同じ局所検出力）：
https://eml.berkeley.edu/~mcfadden/e240a_sp00/ch7.pdf
'''
assert len(d['slides'])==84
for j,(x,y) in enumerate(zip(a['slides'],d['slides'])):
    if j!=i:assert x==y
assert a['assets']==d['assets']
assert a['slides'][i]['leftMarkdown']==s['leftMarkdown']
encoded=json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
html=html[:m.start(2)]+encoded+html[m.end(2):]
html=html.replace('.slide[data-slide-id="intro-9.5"] .example-detail .wald-procon th:first-child{width:15%;}', '.slide[data-slide-id="intro-9.5"] .example-detail .wald-procon th:first-child{width:19%;}')
dst.write_text(html,encoding='utf-8')
print('Only page',i+1,'comparison row and speaker notes updated; all 84 slides retained.')
