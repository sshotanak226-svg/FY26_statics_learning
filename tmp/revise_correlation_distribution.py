from pathlib import Path
import base64,copy,json,re

src=Path('output/９章_仮説検定と信頼区間_フィッシャーz変換概要追加.html')
dst=Path('output/９章_仮説検定と信頼区間_標本相関の分布とt検定.html')
html=src.read_text(encoding='utf-8')
m=re.search(r'(<script id="deck-data" type="application/json">)(.*?)(</script>)',html,re.S)
old=json.loads(m[2]);deck=copy.deepcopy(old)
i=next(i for i,x in enumerate(deck['slides']) if x['id']=='correlation-definition')
s=deck['slides'][i]
s['title']='9.7.1　母相関によって変わる標本相関の分布'
s['takeaway']='母相関ρは、標本相関の分布の位置とばらつき、左右の非対称性を変える。'
s['leftMarkdown']=r'''- $R$ は、$n$ 組の独立な二変量正規標本から得る標本相関。$\rho$ は真の母相関、$r$ は $R$ の観測値（$n>2$）。

- **$\rho=0$**：$R$ の分布は0を中心に対称。密度 $f_R(r)$ は次式に比例する。

$$
f_R(r)\propto(1-r^2)^{(n-4)/2},\quad-1<r<1.
$$

- **$\rho\ne0$**：$R$ の分布は一般に非対称。大標本では、次の正規分布で近似できる。

$$
R\ \overset{\text{近似}}\sim\ N\!\left(\rho,\frac{(1-\rho^2)^2}{n}\right).
$$'''
png=base64.b64encode(Path('tmp/correlation-sampling/r-distributions.png').read_bytes()).decode('ascii')
s['rightHTML']='<div class="corr-density-figure"><h3>母相関が異なる場合の分布</h3><img alt="母相関0、0.5、0.8で異なる標本相関の分布。母相関が大きいほど右へ寄り、左右非対称になる。" src="data:image/png;base64,'+png+'"><p>各母相関について、20組の二変量正規標本を10万回生成し、標本相関の密度を推定した。</p></div>'
s['body']=[p[2:] for p in s['leftMarkdown'].split('\n\n') if p.startswith('- ')]
s['original']='紙面149–150（標本相関の分布と無相関検定）、密度と変数変換の補足'
s['sources']=['pdf','correlation-null-density']
s['notes']='''元の標本相関の計算方法のページを、標本相関の標本分布の説明に置き換えた。標本相関の計算式は既知として扱う。
条件：観測組(Xi,Yi),i=1,...,nは互いに独立で、同じ非退化な二変量正規分布に従い、母相関は−1<ρ<1。Rは標本全体から計算するPearsonの相関係数という確率変数、rは観測された標本相関の値。
標本を取り直すとRが変動する。その標本分布の位置、分散、形はnとρに依存する。ρ=0の下ではXとYが独立になり、Rは0を中心とする対称な分布になる。厳密な密度はf_R(r)=(1−r²)^((n−4)/2)/B(1/2,(n−2)/2),−1<r<1。Bはベータ関数で、分母は密度の積分が1になるための定数。本文の比例記号∝は、rに依存しない定数を省略したことを表す。この分布は[−1,1]に変換したベータ分布であり、(R+1)/2~Beta((n−2)/2,(n−2)/2)、R²~Beta(1/2,(n−2)/2)とも書ける。
ρ≠0における厳密な有限標本密度は、このρ=0の対称なベータ密度とは異なる。本文はその複雑な厳密密度の代わりに、シミュレーションと大標本近似を用いて形とばらつきの変化を示す。ρ>0ではRの分布が右側へ寄り、左側に長い裾を持つ。ρ<0ではその鏡像になる。非対称性と正規近似の精度はnにも依存する。
二変量正規モデルの標本共分散行列の中心極限定理とデルタ法により、sqrt(n)(R−ρ)はN(0,(1−ρ²)²)へ分布収束する。したがって、大標本の分散の一次近似は(1−ρ²)²/n。表示式のρを、有限標本の厳密なE[R]と同一視してはいけない。標本相関は一般に有限標本で偏りを持つ。正規近似はRの範囲[−1,1]の外にも確率を与えるため、特に境界や少数標本の形を厳密に表すものではない。
図はシミュレーション。seed=20261025、各ρ∈{0,0.5,0.8}についてn=20組の標本を100000組生成した。生成法はXi=Ai,Yi=ρAi+sqrt(1−ρ²)Bi、Ai,Biは独立な標準正規。各標本からRを計算し、160区間の密度ヒストグラムをガウス平滑化して曲線にした。各標本のnは20であり、10万という数は密度を描くための標本集合の個数である。
出典：アップロード原資料の紙面149の式(9.17)と紙面150の分布の非対称性の記述。ρ=0における厳密密度をSciPy公式文書のNotesで照合した。
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html
'''

proof=copy.deepcopy(s)
proof.update(id='correlation-t-density-proof',title='9.7.1　標本相関の変換がt分布になる理由',
             takeaway='ρ=0の下で、標本相関をTに変換すると、密度がt分布の密度に一致する。',
             theme='proof',rightHTML='',minutes=1.2)
proof['leftMarkdown']=r'''- **変換**：独立な二変量正規標本の母相関は $\rho=0$。$\nu=n-2>0$ のとき、変換式と微分係数は、

$$
T=\frac{\sqrt\nu\,R}{\sqrt{1-R^2}},\qquad
R=\frac{T}{\sqrt{\nu+T^2}},\qquad
\left|\frac{dr}{dt}\right|=\frac{\nu}{(\nu+t^2)^{3/2}}.
$$

- **密度の変換**：$T$ の密度は、$R$ の密度と、変換による区間の幅の補正 $|dr/dt|$ の積になる。前ページの密度を代入すると、

$$
\begin{aligned}
f_T(t)
&=f_R\!\left(\frac{t}{\sqrt{\nu+t^2}}\right)\frac{\nu}{(\nu+t^2)^{3/2}}\\[5pt]
&\propto\left(1-\frac{t^2}{\nu+t^2}\right)^{(\nu-2)/2}\frac{\nu}{(\nu+t^2)^{3/2}}
\propto\left(1+\frac{t^2}{\nu}\right)^{-(\nu+1)/2}.
\end{aligned}
$$

- 最後の式は、自由度 $\nu$ のt分布の密度と同じ形。両密度の積分は1なので、比例定数も一致する。したがって、$T\sim t_{n-2}$ が厳密に成り立つ。'''
proof['body']=[p[2:] for p in proof['leftMarkdown'].split('\n\n') if p.startswith('- ')]
proof['original']='紙面149の式(9.17)について、標本相関の密度の変数変換による補足'
proof['notes']='''このページは教科書の紙面149の式(9.17)に対する追加の導出であり、教科書にこの計算過程がそのまま掲載されているわけではない。
ρ=0、n>2の独立な非退化二変量正規標本を仮定する。前ページの密度はf_R(r)=c(1−r²)^((n−4)/2)、−1<r<1、c=1/B(1/2,(n−2)/2)である。ν=n−2と置くと指数は(ν−2)/2。
変換t=sqrt(ν)r/sqrt(1−r²)は−1<r<1で単調増加し、実数全体を動く。分析者がt²=νr²/(1−r²)をrについて解くと、r=t/sqrt(ν+t²)。符号は変換の単調性からtと同じである。微分するとdr/dt=ν/(ν+t²)^(3/2)>0。
変数変換の密度公式f_T(t)=f_R(r(t))|dr/dt|を用いる。1−r(t)²=ν/(ν+t²)なので、f_T(t)=c ν^(ν/2)(ν+t²)^(-(ν+1)/2)=c/sqrt(ν) (1+t²/ν)^(-(ν+1)/2)。c/sqrt(ν)=Γ((ν+1)/2)/(sqrt(νπ)Γ(ν/2))であり、これはtν密度の正規化定数である。本文では新しいガンマ関数・ベータ関数の定義を増やさないため、密度の積分が1であることから定数が一致すると説明した。
R自体がt分布に従うわけではない。Rは[−1,1]の中を動く。分析者が変換したTが、ρ=0の下で自由度n−2のt分布に従う。この性質は有限標本で厳密であり、大標本近似ではない。
ρ≠0の場合、この中心t分布は使えない。一般の母相関の検定は、後続のフィッシャーz変換による近似へつながる。
密度の出典：SciPy公式文書のpearsonr Notes。
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html
'''
deck['slides'].insert(i+1,proof)

overview=next(x for x in deck['slides'] if x['id']=='intro-9.7')
overview['rightHTML']=overview['rightHTML'].replace('標本相関と無相関検定','標本相関の分布とt検定')
test=next(x for x in deck['slides'] if x['id']=='corr-null')
test['original']='PDF26ページ（紙面149、式9.17）'
test['notes']='''出典：アップロード原資料の紙面149、式(9.17)。
前ページの変数変換により、独立な二変量正規標本でρ=0のとき、T=sqrt(n−2)R/sqrt(1−R²)が自由度n−2のt分布に厳密に従う。分析者は観測された標本相関rからtの観測値を計算し、t分布の両側の上側α/2点と比較する。ここでt分布はRの分布ではなく、変換したTの帰無分布である。rの計算方法の説明は省略した。
'''
deck['sources']['correlation-null-density']={
 'title':'SciPy公式文書：pearsonrの厳密な帰無密度',
 'url':'https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html',
 'detail':'独立な正規標本（母相関0）における標本相関の密度とベータ分布の関係。t分布への変換は、この密度から追加計算した。'
}
new_ids={proof['id']}
assert len(deck['slides'])==len(old['slides'])+1
retained=[x for x in deck['slides'] if x['id'] not in new_ids]
changed=[j+1 for j,(a,b) in enumerate(zip(old['slides'],retained)) if a!=b]
assert changed==[45,46,47],changed
assert len({x['id'] for x in deck['slides']})==len(deck['slides'])
encoded=json.dumps(deck,ensure_ascii=False,separators=(',',':')).replace('</script','<\\/script')
out=html[:m.start(2)]+encoded+html[m.end(2):]
style='''<style id="correlation-sampling-layout">
.slide[data-slide-id="correlation-definition"] .corr-density-figure h3{font-size:32px;line-height:1.4;margin:0 0 10px;color:var(--theme);}
.slide[data-slide-id="correlation-definition"] .corr-density-figure p{margin:8px 0;line-height:1.4;}
.slide[data-slide-id="correlation-definition"] .corr-density-figure img{width:100%;max-height:430px;}
.slide[data-slide-id="correlation-definition"] .markdown>.body-list{margin-bottom:8px;}
.slide[data-slide-id="correlation-definition"] .markdown p:has(.katex-display){margin:8px 0;}
.slide[data-slide-id="correlation-definition"] .katex-display>.katex>.katex-html{line-height:1.3;}
.slide[data-slide-id="correlation-t-density-proof"] .content.full-width .text-block{padding-top:0;padding-bottom:0;}
.slide[data-slide-id="correlation-t-density-proof"] .markdown>.body-list{margin-bottom:8px;}
.slide[data-slide-id="correlation-t-density-proof"] .markdown p:has(.katex-display){margin:8px 0;}
.slide[data-slide-id="correlation-t-density-proof"] .katex-display>.katex>.katex-html{line-height:1.3;}
</style>'''
out=out.replace('</head>',style+'</head>',1)
dst.write_text(out,encoding='utf-8')
print(f'Revised pages 45-46; added proof at 47; test now 48. {len(old["slides"])} -> {len(deck["slides"])} slides. All other slide contents preserved.')
