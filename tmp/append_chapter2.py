from pathlib import Path
import json,re,base64,hashlib
root=Path(r'F:\Document\Fy26 TDH statics lean')
dest=root/'Chapter2_1.md'
original=dest.read_bytes()
backup=root/'tmp/Chapter2_1_追記前.md'
if backup.exists():
    raise RuntimeError('追記前のバックアップが既に存在するため、重複追記を確認してください。')
addition=(root/'tmp/chapter2_continuation.md').read_text(encoding='utf-8')
assert '# 連続確率分布と特性値' not in original.decode('utf-8')
backup.write_bytes(original)
source=(root/'output/html/1005tdh統計勉強会_連続確率分布と変数変換.html').read_text(encoding='utf-8')
deck=json.loads(re.search(r'<script id="deck-data" type="application/json">([\s\S]*?)</script>',source)[1])
for key,name in [('source-fig-2-5','Chapter2_1_図2_5.jpg'),('source-fig-2-8','Chapter2_1_図2_8.jpg')]:
    path=root/'img'/name
    assert not path.exists(),f'既存画像の上書きを避ける：{path}'
    path.write_bytes(base64.b64decode(deck['assets'][key].split(',',1)[1]))
dest.write_bytes(original.rstrip(b'\n')+b'\n\n'+addition.encode('utf-8'))
assert dest.read_bytes().startswith(original)
print(json.dumps({'path':str(dest),'original_bytes':len(original),'addition_chars':len(addition),'addition_lines':len(addition.splitlines()),'total_bytes':dest.stat().st_size,'original_sha256':hashlib.sha256(original).hexdigest()},ensure_ascii=False))
