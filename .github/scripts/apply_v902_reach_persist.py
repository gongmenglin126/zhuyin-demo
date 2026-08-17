from pathlib import Path
p=Path('app/AdminPortalOccult.tsx')
s=p.read_text()
old='reach={bothReach}'
new='reach={bothReach||items.box==="center"}'
if s.count(old)!=2:
    raise SystemExit(f'expected 2 reach props, got {s.count(old)}')
s=s.replace(old,new)
p.write_text(s)
