from pathlib import Path
from html import escape
import re,json,copy

src=Path('F:/Download/９章　仮説検定と信頼区間_編集済み (6).html')
dst=Path('output/９章_仮説検定と信頼区間_フィッシャーz変換概要追加.html')
html=src.read_text(encoding='utf-8')
m=re.search(r'(<script id="deck-data" type="application/json">)(.*?)(</script>)',html,re.S)
old=json.loads(m[2]);deck=copy.deepcopy(old)
i=next(i for i,s in enumerate(deck['slides']) if s['id']=='fisher-z')
s=copy.deepcopy(deck['slides'][i])
s.pop('testExample',None)
s.update(id='fisher-z-introduction',title='9.7.2　フィッシャーのz変換：意味と性質',
         takeaway='フィッシャーのz変換は、標本相関を正規近似しやすい尺度へ変換する。',
         role='content',minutes=1.0)
s['leftMarkdown']=r'''- **変換の目的**：標本相関 $r$ の分布は、真の母相関 $\rho$ が0から離れると左右非対称になる。フィッシャーのz変換は、$r$ を正規近似しやすい値 $z$ に変える。

$$
z=\frac12\log\frac{1+r}{1-r}.
$$

- $\log$ は自然対数。変換前の $r$ は $-1<r<1$、変換後の $z$ は実数全体を取る。例えば、$r=0.8$ の変換値は、

$$
z=\frac12\log\frac{1.8}{0.2}
=\frac12\log9\approx1.099.
$$'''
def eq(t):return '<div class="detail-equation">$$'+escape(t)+'$$</div>'
s['rightHTML']='<div class="fisher-intro-detail">'+''.join([
 '<h3>変換後の性質</h3>',
 r'<p>変換は $r$ の<strong>符号と大小関係を保ち</strong>、$\pm1$ 付近の差を広げる。</p>',
 r'<p>二変量正規の独立な $n$ 組の標本では、$n$ が十分大きいとき、変換値 $z$ の分布は、</p>',
 eq(r'\begin{gathered}\xi=\frac12\log\frac{1+\rho}{1-\rho},\\[4pt]z\ \overset{\text{近似}}{\sim}\ N\!\left(\xi,\frac1{n-3}\right).\end{gathered}'),
 r'<p>$\xi$ は母相関 $\rho$ の変換値。</p>',
 r'<p>変換値の標準誤差は約 $1/\sqrt{n-3}$。標準誤差は<strong>母相関にほぼ依存しない</strong>ため、分析者は正規近似で検定できる。</p>',
])+'</div>'
s['body']=[p[2:] for p in s['leftMarkdown'].split('\n\n') if p.startswith('- ')]
s['original']='PDF27ページ（紙面150、フィッシャーのz変換の定義・正規近似）'
s['notes']='''出典：アップロードされた教科書の紙面149–150ページ（PDF26–27ページ）。変換式と分布の近似式は紙面150ページの上部に載る。
このスライドは、直後の既存スライドが扱うフィッシャー変換による検定の準備である。標本相関rはn組の観測から求めるPearsonの相関係数であり、ρは母集団の真の相関係数である。分析者は各観測値を変換するのではなく、標本から計算した相関係数を変換する。
変換関数g(r)=log{(1+r)/(1−r)}/2は逆双曲線正接artanh(r)である。logは自然対数。−1<r<1では分子と分母が正なので式を計算でき、r→−1でz→−∞、r→1でz→∞、r=0でz=0となる。r=±1では有限な変換値は得られない。
g'(r)=1/(1−r²)>0なので、変換は相関係数の大小関係を保つ。gは奇関数であり、変換は相関係数の符号も保つ。|r|が1に近いほど微分係数が大きいため、端付近の差は変換後の尺度では広がる。数値例ではr=0.8からz=log(9)/2=1.098612...を得る。
独立な二変量正規標本と内点の母相関−1<ρ<1を仮定する。母相関が0から離れると標本相関の標本分布の非対称性が増すため、変換を使って正規分布に近い尺度に移す。標本数nが十分大きく、n>3のとき、変換値の分布を平均ξ=g(ρ)、分散1/(n−3)の正規分布で近似する。第2引数は分散であり、標準誤差は1/sqrt(n−3)。この分布の近似式は、厳密な有限標本の分布や全てのデータ分布についての主張ではない。n>3だけで良い近似が保証されるわけでもない。
標本相関の漸近分散は(1−ρ²)²/nである。デルタ法でgの導関数1/(1−ρ²)を掛けると、変換値の漸近分散は1/nとなる。教科書は、より良い有限標本近似としてn−3を用いると説明する。スライドはこの分散安定化の直感を「母相関にほぼ依存しない標準誤差」と表現した。
変換値zは、それだけで平均0・分散1の標準正規変数になるわけではない。検定では、分析者は帰無値ρ0にも同じ変換を適用してξ0=g(ρ0)を求め、(z−ξ0)/(1/sqrt(n−3))を計算する。直後の既存スライドがその仮説・統計量・棄却域を説明する。
'''
deck['slides'].insert(i,s)
assert len(deck['slides'])==len(old['slides'])+1
assert [x for x in deck['slides'] if x['id']!=s['id']]==old['slides']
assert len({x['id'] for x in deck['slides']})==len(deck['slides'])
encoded=json.dumps(deck,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
out=html[:m.start(2)]+encoded+html[m.end(2):]
style='''<style id="fisher-z-introduction-layout">
.slide[data-slide-id="fisher-z-introduction"] .fisher-intro-detail h3{font-size:32px;line-height:1.4;margin:0 0 14px;color:var(--theme);}
.slide[data-slide-id="fisher-z-introduction"] .fisher-intro-detail p{margin:6px 0;line-height:1.4;}
.slide[data-slide-id="fisher-z-introduction"] .katex-display>.katex>.katex-html{line-height:1.3;}
</style>'''
out=out.replace('</head>',style+'</head>',1)
dst.write_text(out,encoding='utf-8')
print(f'Added page {i+1} before Fisher test. {len(old["slides"])} -> {len(deck["slides"])} slides. Existing slide contents unchanged.')
