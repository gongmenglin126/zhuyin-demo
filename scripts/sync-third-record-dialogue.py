from pathlib import Path

p=Path('content/wechatLiveDialogues.ts')
s=p.read_text()
repls={
'  "她连自己到底叫沈妍还是林楠都说不稳。":"她连自己到底叫沈妍还是林楠都说不稳。",':'  "她连自己到底叫沈妍还是林楠都说不稳。":"她能说出来的都只是一些碎片，人物、地点、时间都连不起来。",',
'  "但一听到徐宁这个名字就哭……这比直接认出你更吓人。":"但一听到徐宁这个名字就哭……这比直接认出你更吓人。",':'  "但一听到徐宁这个名字就哭……这比直接认出你更吓人。":"她只对‘沈妍’和‘林楠’这两个名字有反应。",',
}
for old,new in repls.items():
    if old not in s:
        raise SystemExit(f'missing target: {old}')
    s=s.replace(old,new,1)
p.write_text(s)
