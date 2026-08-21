from pathlib import Path

# trigger: warm public lure + Liang realization

def replace_once(path, old, new, label):
    p=Path(path)
    s=p.read_text()
    if old not in s:
        raise SystemExit(f'missing target: {label}')
    p.write_text(s.replace(old,new,1))

# 1) Liang's reaction: personal memory first, realization second.
replace_once(
    'app/InteractiveWechat.tsx',
    '"admin-watchlist":{ly:[{text:"……"},{text:"我早就知道。"},{text:"我早就知道这个论坛不正常。"},{text:"我以前还以为只是这里怪人多。"},{text:"原来不是我们碰巧聚到一起。"},{text:"是它一直在等我们自己搜回来。"}],zc:[{text:"这么多人？"},{text:"这后台不像临时搭的。"}]},',
    '"admin-watchlist":{ly:[{text:"我第一次搜自己身上那些怪事的时候，那篇帖子就在搜索结果第一条。"},{text:"我以为我终于找到了所谓的‘病友’。"},{text:"我还觉得，原来真的有人跟我一样。"},{text:"没想到……"},{text:"不是我找到他们。"},{text:"是他们一直把这些帖子放在那里，等我们自己搜进来。"}],zc:[{text:"这么多人？"},{text:"这后台不像临时搭的。"}]},',
    'Liang return-to-nest reaction'
)

# 2) Add a warm public sticky by the admin. It should feel kind before the backend reveal.
p=Path('content/gameDataFlowV2.ts')
s=p.read_text()
marker='export const posts:Post[]=[...patched,posterMemory,linSnackPost,linMarblePost,shenCandyPost,thresholdNamePost,ritualFragmentPost,adminAccountPost,facelessIdolPost].sort((a,b)=>toRank(a.date)-toRank(b.date));'
if marker not in s:
    raise SystemExit('posts export marker missing')
welcome='''const welcomePost:Post={\n id:"31003",title:"【置顶】写给第一次来到这里的人：你不需要先证明自己",author:"旧档员-03",date:"2016-07-12 00:08",board:"站务区",views:48612,hidden:false,\n excerpt:"如果你因为一段说不清的梦、记忆或旧事来到这里，可以慢慢写。这里不会要求你先证明自己的经历。",\n terms:["新人","第一次来到","说不清的经历","站务","欢迎"],highlights:["这里接纳所有愿意认真描述自己经历的人","你不需要先证明它是真的","有些困惑，并不只有你一个人经历过"],\n body:[\n  "这几年经常有人私信问：我只是做了一个很奇怪的梦，或者记得一点根本说不清来源的东西，这种内容能不能发在这里。可以。",\n  "很多人来到这里，心里都带着一件说不清楚的事。可能是一段反复出现的梦，一间明明没住过却觉得熟悉的房子，一个莫名亲切的名字，也可能只是某种很难解释的感觉。",\n  "这里接纳所有愿意认真描述自己经历的人。你不需要先证明它是真的，也不用担心别人觉得你奇怪。如果愿意，就把自己确实记得的东西写下来：一个名字、一种味道、一扇门、一件小时候的东西，都可以。记不清的地方空着就好。",\n  "当然，论坛不能代替医生、警方或其他专业帮助。如果这些事已经明显影响睡眠和生活，现实里的帮助永远比网友猜测重要。",\n  "无论最后有没有答案，希望你至少能知道：有些困惑，并不只有你一个人经历过。"\n ],\n replies:[\n  reply("纸页边角","2016-07-12 00:31","这条挺好，最近新人确实多。很多人一上来就怕自己说得太离谱。"),\n  reply("旧档员-03","00:46","能确认什么就写什么，想不起来的地方不用硬补。","版主"),\n  reply("迟迟","2017-07-22 23:26","谢谢。我就是搜小时候一些很怪的事搜进来的，本来只是想看看有没有人跟我一样。"),\n  reply("雨停以前","2022-03-18 01:14","翻到这条突然有点安心。我删了三次草稿，还是决定发出来看看。"),\n  reply("版务","2026-01-03 09:12","长期置顶。涉及现实人身安全、失踪或伤害风险的内容，请优先联系当地警方或可信任的现实联系人。","版主")\n ]\n};\n\n'''
s=s.replace(marker,welcome+marker.replace('facelessIdolPost]','facelessIdolPost,welcomePost]'),1)
p.write_text(s)

# 3) Keep the warm sticky first on the forum homepage.
replace_once(
    'app/page.tsx',
    'const HOME_POST_IDS=["34106","34091","34086","34080","34064","34055","34049","20847","34043","33992","33981"];',
    'const HOME_POST_IDS=["31003","34106","34091","34086","34080","34064","34055","34049","20847","34043","33992","33981"];',
    'home post ids'
)

# 4) Lock the intended double-read into canon.
p=Path('docs/CANON_v3.0_世界观与游戏设定唯一权威集.md')
s=p.read_text()
old='- 组织会维护、恢复、移动具有筛查价值的旧档，使其长期可被类似对象检索到；\n- 恐怖点是：**不是他们先找到了异常者，而是异常记忆最终会把人带回这个论坛。**'
new='- 组织会维护、恢复、移动具有筛查价值的旧档，使其长期可被类似对象检索到；\n- 公共区长期置顶一篇由 `旧档员-03` 发布的温情欢迎帖，表面上强调“你不需要先证明自己”“这里接纳所有愿意认真描述自己经历的人”，并鼓励新人记录名字、味道、房间、童年物件等真实细节；首次阅读必须像正常的互助社区公告，只有看到后台“归巢索引”后，玩家才意识到这些温和的提示同时也是主动收集筛查字段；\n- 恐怖点是：**不是他们先找到了异常者，而是异常记忆最终会把人带回这个论坛。**'
if old not in s:
    raise SystemExit('canon nest section target missing')
p.write_text(s.replace(old,new,1))
