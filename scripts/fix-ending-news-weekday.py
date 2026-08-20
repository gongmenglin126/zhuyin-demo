from pathlib import Path

p=Path('app/GameEnding.tsx')
s=p.read_text()
s=s.replace('home:{date:"2026年10月18日",headline:', 'home:{date:"2026年10月18日",weekday:"星期日",headline:', 1)
s=s.replace('true:{date:"2026年10月18日",headline:', 'true:{date:"2026年10月18日",weekday:"星期日",headline:', 1)
s=s.replace('double:{date:"2026年10月20日",headline:', 'double:{date:"2026年10月20日",weekday:"星期二",headline:', 1)
old='<header style={s.newsTop}><span>{editEndingText(item.date)}　星期日</span><span>河临 · 电子版</span></header>'
new='<header style={s.newsTop}><span>{editEndingText(item.date)}　{editEndingText(item.weekday)}</span><span>河临 · 电子版</span></header>'
if old not in s:
    raise SystemExit('news header target not found')
s=s.replace(old,new,1)
p.write_text(s)

p=Path('content/endingDialogues.ts')
s=p.read_text()
marker='};\n\nexport const editEndingText'
insert='  "星期日":"星期日",\n  "星期二":"星期二",\n'
if marker not in s:
    raise SystemExit('ending dialogue marker not found')
s=s.replace(marker,insert+marker,1)
p.write_text(s)
