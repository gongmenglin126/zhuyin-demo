from pathlib import Path


def replace_once(path: str, old: str, new: str, label: str):
    p = Path(path)
    s = p.read_text()
    if old not in s:
        raise SystemExit(f"missing fragment: {label}")
    p.write_text(s.replace(old, new, 1))

replacements = {
    '  "两个客，两个门。":"两个客，两个门。",': '  "两个客，两个门。":"我会理解成，是两边绑在一起。",',
    '  "跟你前面那两个人放一起，我第一反应会是两边一起发生了什么。":"跟你前面那两个人放一起，我第一反应会是两边一起发生了什么。",': '  "跟你前面那两个人放一起，我第一反应会是两边一起发生了什么。":"一边出了变化，另一边也会跟着有反应。",',
    '  "但我现在也只能到这。":"但我现在也只能到这。",': '  "但我现在也只能到这。":"不过我就是顺着前一句往下猜，别先往沈妍身上硬套。",',
    '  "两个客、两个门，大概至少不是只说一个人。":"两个客、两个门，大概至少不是只说一个人。",': '  "两个客、两个门，大概至少不是只说一个人。":"听着更像是在说一对，而不是一个人自己发生变化。",',
    '  "再往下我没东西能对。":"再往下我没东西能对。",': '  "再往下我没东西能对。":"再往下我也不敢乱猜。",',
}

p = Path("content/wechatLiveDialogues.ts")
s = p.read_text()
for old, new in replacements.items():
    if old not in s:
        raise SystemExit(f"missing wechat line: {old}")
    s = s.replace(old, new, 1)
p.write_text(s)

replace_once(
    "app/PrivateArea.tsx",
    '   {shared&&<p style={s.sharedHint}>已加入材料列表。打开微信后，在周川或梁茵聊天底部点“选择材料”即可发送。</p>}<article style={s.article}>',
    '   {shared&&<p style={s.sharedHint}>已加入调查材料。</p>}<article style={s.article}>',
    "material hint",
)
