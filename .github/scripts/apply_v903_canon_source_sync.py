from pathlib import Path

# Sync old/base content layers so removed name mechanics cannot reappear through a legacy path.
for path in ['content/gameData.ts','content/gameDataFlow.ts']:
    p=Path(path)
    s=p.read_text()
    s=s.replace('形可易，名可夺，忆可乱','形可易，忆可乱')
    s=s.replace('白纸抄本谈形、名、忆','白纸抄本谈形与忆')
    s=s.replace('白纸反复谈形、名、忆','白纸反复谈形与忆')
    s=s.replace('它像是在解释身份为什么不能只靠身体、名字或记忆。','它像是在讨论身体与记忆为什么会彼此错位。')
    s=s.replace('"名可夺",','')
    s=s.replace(',"名可夺"','')
    s=s.replace('"形是身体","名是别人怎么叫我","忆是我记得什么","像魂穿","两个人一起换"','"身为舍","魂为客","二客","两门相应"')
    s=s.replace('如果形是身体，名是别人怎么叫我，忆是我记得什么，那么它讨论的可能不是梦，也不只是失忆。第一反应是像魂穿，可那种说法通常只有一个人进去。这里为什么一直写“两门相应”“二客”？','我现在只能确认几个词反复出现：舍、客、二客、两门。它们怎么连起来，我还没有现实材料能证明。')
    s=s.replace('我在图上先标了自己的理解：会不会不是一个人占了另一个人的身体，而是两个人一起换？先留问号，不能拿猜测当答案。','我把能辨认的出处和异文圈出来，先不往“它究竟发生了什么”上补答案。')
    s=s.replace('images:[{src:"assets/sanmen-shenyan-annotations-v1.webp",caption:"附件：沈妍保存的《三门疏》残页；只圈出处与异文"}]','images:[]')
    p.write_text(s)

# WeChat must use the new mechanism vocabulary too.
p=Path('app/InteractiveWechat.tsx')
s=p.read_text()
s=s.replace('但“名可夺，忆可乱”这句看着很不舒服。','但“忆可乱”这几个字看着很不舒服。')
s=s.replace('text:"“名可夺，忆可乱”这句你怎么看？"','text:"“忆可乱”这句你怎么看？"')
s=s.replace('{text:"但“名”这个字让我不舒服。"},','')
s=s.replace('“赤烛照舍，黄符定名”像什么？','“赤烛引客，黄符镇舍”像什么？')
s=s.replace('“定名”听着像他们自己固定用的词。','“镇舍”听着像他们自己固定用的词。')
p.write_text(s)

# Guard all live/bundled content layers against the removed mechanism and the spoiler phrasing.
for path in ['content/gameData.ts','content/gameDataFlow.ts','content/gameDataFlowV2.ts','app/InteractiveWechat.tsx','app/AdminPortalOccult.tsx','app/page.tsx']:
    s=Path(path).read_text()
    for banned in ['名可夺','黄符定名','像魂穿','两个人一起换']:
        if banned in s:
            raise SystemExit(f'{path}: stale wording remains: {banned}')
