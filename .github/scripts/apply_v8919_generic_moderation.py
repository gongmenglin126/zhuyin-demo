from pathlib import Path

roots=[Path('app'),Path('content')]
changed=[]
for root in roots:
    for p in root.rglob('*'):
        if p.suffix not in {'.ts','.tsx'}:
            continue
        s=p.read_text(encoding='utf-8')
        n=s.replace('站务-槐序','站务').replace('版务-青砖','版务')
        if n!=s:
            p.write_text(n,encoding='utf-8')
            changed.append(str(p))

if not changed:
    raise SystemExit('no moderation names found')

for root in roots:
    for p in root.rglob('*'):
        if p.suffix in {'.ts','.tsx'}:
            s=p.read_text(encoding='utf-8')
            assert '站务-槐序' not in s
            assert '版务-青砖' not in s
print('\n'.join(changed))
