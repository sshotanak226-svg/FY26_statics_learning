from pathlib import Path
import json,re,copy

src=Path('F:/Download')/'９章　仮説検定と信頼区間_編集済み (2).html'
dst=Path('F:/Document/Fy26 TDH statics lean/output/９章_仮説検定と信頼区間_ワルド利点欠点比較.html')
html=src.read_text(encoding='utf-8')
m=re.search(r'(<script id="deck-data" type="application/json">)(.*?)(</script>)',html,re.S)
original=json.loads(m[2]);d=copy.deepcopy(original)
idx=next(i for i,s in enumerate(d['slides']) if s['id']=='intro-9.5')
s=d['slides'][idx]
s['rightHTML']='''<div class="example-detail wald-overview-detail">
<h3>尤度比検定に対する利点・欠点</h3>
<table class="wald-procon"><thead><tr><th>評価</th><th>ワルド検定の特徴</th></tr></thead><tbody>
<tr><td><strong>利点</strong></td><td>推定値と標準誤差で計算。帰無制約での再推定が不要。</td></tr>
<tr><td><strong>欠点</strong></td><td>小標本・境界付近では、正規近似が不安定になりやすい。</td></tr>
<tr><td><strong>欠点</strong></td><td>母数を対数などに変えると結果が変わり得る。尤度比は不変。</td></tr>
</tbody></table>
<p><strong>使う場面</strong>：大標本で標準誤差が安定し、再推定を省きたいとき。</p>
<p class="wald-section-route"><strong>9.5の流れ</strong>：最尤推定量 → 比率 → 平均 → 夫婦の差</p>
</div>'''
s['notes']+='''

【比較表の説明】
利点：通常の尤度比検定は、制約なしと帰無仮説の制約ありで最大尤度を比べる。Wald検定は制約なしの推定値と推定分散・共分散から構成でき、帰無制約下のモデルを別に推定する必要がない。既に推定値と標準誤差が出力されているときや、制約付き最適化の計算負担が大きいときに便利。
欠点1：Wald検定は推定量の局所的な正規近似と、その点での標準誤差に頼る。標本が少ない場合、尤度が強く非対称な場合、推定値が母数空間の境界付近にある場合には、近似が悪くなり得る。例えば母比率が0や1に近い場合の通常のWald検定には注意が必要。大標本という条件は単にnが一定の数を超えればよいという意味ではなく、有効な情報量やモデルの状況による。
欠点2：同じ帰無仮説でも、θでWald検定を作る場合と、正のθをlog θへ変換して作る場合では、有限標本の統計量とp値が変わり得る。変換後の標準誤差はデルタ法などで対応させても、Wald統計量は一般には厳密に一致しない。これに対し、尤度比は、同じモデル・同じ帰無仮説を滑らかな1対1の母数変換で表し直すだけなら不変。単位の線形変更だけで一般に結果が変わるという意味ではない。
使用場面：正則条件が妥当で、推定値が境界から離れ、推定量の正規近似と標準誤差が安定する十分な標本があり、推定結果を使って簡便に仮説を調べたいとき。尤度比の制約付き再推定に計算コストがかかる場合は利点が大きい。
尤度比検定が常に有限標本で厳密という意味ではない。通常のχ²近似を使う尤度比検定にも条件があり、境界では標準的なχ²の定理が使えない場合がある。小標本でWaldが不安定なら、モデルに応じて尤度比・スコア・厳密法などを検討する。どれを選んでも無条件で正確になるわけではない。
後続の9.5.1では最尤推定量と情報量、例9.6では母比率、9.5.2では母平均、例9.7では夫婦内の差の平均と標準誤差を扱い、同じ標準化の仕組みを適用する。

【比較の参考文献】
SAS Institute, SAS/ETS 13.1 User's Guide, The QLIM Procedure, Tests on Parameters（制約付き再推定の不要性、小標本の近似、再母数化への非不変性）：
https://support.sas.com/documentation/cdl/en/etsug/66840/HTML/default/etsug_qlim_details22.htm
UCLA OARC, How can I perform the likelihood ratio and Wald test in Stata?（二つのモデルを推定する尤度比と、制約なしのモデルの推定から構成するWaldとの計算の違い）：
https://stats.oarc.ucla.edu/stata/faq/how-can-i-perform-the-likelihood-ratio-wald-and-lagrange-multiplier-score-test-in-stata/
'''
assert len(d['slides'])==len(original['slides'])==84
for i,(a,b) in enumerate(zip(original['slides'],d['slides'])):
    if i!=idx:assert a==b
assert d['slides'][idx]['leftMarkdown']==original['slides'][idx]['leftMarkdown']
assert d['assets']==original['assets']
encoded=json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
html=html[:m.start(2)]+encoded+html[m.end(2):]
css='''<style id="wald-comparison-revision-style">
.slide[data-slide-id="intro-9.5"] .example-detail .wald-procon{table-layout:fixed;}
.slide[data-slide-id="intro-9.5"] .example-detail .wald-procon th:first-child{width:15%;}
.slide[data-slide-id="intro-9.5"] .example-detail .wald-procon th,.slide[data-slide-id="intro-9.5"] .example-detail .wald-procon td{padding:8px 9px;line-height:1.35;}
.slide[data-slide-id="intro-9.5"] .example-detail .wald-section-route{font-size:28px;line-height:1.4;margin-top:12px;}
</style>'''
html=html.replace('</head>',css+'</head>',1)
dst.write_text(html,encoding='utf-8')
print('Revised page',idx+1,'comparison and speaker notes. Original left side and all other slides preserved.')
