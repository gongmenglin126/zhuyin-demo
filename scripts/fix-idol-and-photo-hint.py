from pathlib import Path
import base64, re

root = Path('.')
svg = root / 'public/assets/occult/factory-faceless-idol.svg'
jpg = root / 'public/assets/occult/factory-faceless-idol.jpg'
data = svg.read_text(encoding='utf-8')
m = re.search(r'data:image/jpeg;base64,([^\"]+)', data)
if not m:
    raise SystemExit('embedded JPEG not found in SVG')
jpg.write_bytes(base64.b64decode(m.group(1)))

p = root / 'content/gameDataFlowV2.ts'
s = p.read_text(encoding='utf-8')
old_hint = '这种老单位房我拍过不少，门窗长得都挺像。只看你这张图，我认不出地方。'
new_hint = '这种老单位房我拍过不少，我帖子里有一组旧家属区的照片，你可以看看像不像。'
if old_hint not in s:
    raise SystemExit('photo hint target not found')
s = s.replace(old_hint, new_hint, 1)
old_asset = 'assets/occult/factory-faceless-idol.svg'
new_asset = 'assets/occult/factory-faceless-idol.jpg'
if old_asset not in s:
    raise SystemExit('idol asset target not found')
s = s.replace(old_asset, new_asset, 1)
p.write_text(s, encoding='utf-8')

svg.unlink()
print('wrote', jpg, jpg.stat().st_size, 'bytes')
print('updated hint and idol asset path')
