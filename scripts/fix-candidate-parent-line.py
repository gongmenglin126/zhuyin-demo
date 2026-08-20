from pathlib import Path
p=Path('content/adminDialogues.ts')
s=p.read_text()
old='父亲，目前我中选了。母亲那边先别哭，这是喜事。'
new='父亲母亲，我中选了。这是喜事。'
if old not in s:
    raise SystemExit('target line not found')
p.write_text(s.replace(old,new,1))
