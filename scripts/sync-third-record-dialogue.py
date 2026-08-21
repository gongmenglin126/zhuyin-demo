from pathlib import Path

p=Path('content/wechatLiveDialogues.ts')
s=p.read_text()
old='  "但一听到徐宁这个名字就哭……这比直接认出你更吓人。":"她听到熟悉的名字会有反应，但自己也说不清为什么。",'
new='  "但一听到徐宁这个名字就哭……这比直接认出你更吓人。":"她只对‘沈妍’和‘林楠’这两个名字有反应。",'
if old not in s:
    raise SystemExit('current 19-07 dialogue target not found')
s=s.replace(old,new,1)
p.write_text(s)
