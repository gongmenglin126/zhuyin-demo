from pathlib import Path
import json


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"missing target: {label}")
    return text.replace(old, new, 1)


def add_map_entries(path: str, marker: str, entries: list[str]):
    p = Path(path)
    s = p.read_text()
    lines = []
    for item in entries:
        key = json.dumps(item, ensure_ascii=False)
        lines.append(f"  {key}:{key},")
    payload = "\n".join(lines) + "\n"
    if marker not in s:
        raise SystemExit(f"missing map marker: {path}")
    # avoid duplicate insertion on retries
    if entries and json.dumps(entries[0], ensure_ascii=False) in s:
        return
    s = s.replace(marker, payload + marker, 1)
    p.write_text(s)

# 1) Shen Yan private note: shallow fragments -> sudden deepening after Oct 12
p = Path('content/gameDataFlowV2.ts')
s = p.read_text()
marker = 'export const privateEntries:PrivateEntry[]=['
private_def = '''const deepMemoryPrivate:PrivateEntry={
 id:"p4",title:"10月14日，越来越清楚了",date:"2026-10-14 02:41",
 highlights:["前几个月不是这样的","从前天晚上开始不一样","越来越清楚","我是在想起一件发生过的事"],
 body:[
  "前几个月不是这样的。那时候醒过来只剩几个东西：红铁皮盒、窗帘、厨房门，还有一个听不清的名字。写下来以后就散了，白天基本不会想起，也没影响我做别的事。",
  "从前天晚上开始不一样。细节不是变多一点，是越来越清楚。我开始知道从餐桌走到厨房要踩过哪几块裂砖，知道杯子平时放在哪一格，甚至知道有人从厨房出来时会先扶一下门框。",
  "这些不是我后来查旧帖查出来的。有些细节我根本没写过，也没在照片里见过。",
  "最让我害怕的是，我现在已经不像是在反复梦见那间屋。",
  "我是在想起一件发生过的事。"
 ],
 images:[]
};

'''
if 'id:"p4",title:"10月14日，越来越清楚了"' not in s:
    s = replace_once(s, marker, private_def + marker, 'insert deep memory private')
    s = replace_once(s, ' sanmenPrivate,\n];', ' sanmenPrivate,\n deepMemoryPrivate,\n];', 'append deep memory private')
p.write_text(s)

# 2) Yuqing confrontation based on Shen admin record, keeping the historical 20:46/21:03 chat intact
p = Path('app/InteractiveWechat.tsx')
s = p.read_text()
old = '"admin-shen-record":{ly:[{text:"这些时间都记得这么细？"},{text:"10月16号那几条……截图。"}],zc:[{text:"19:49转交，20:52采血，21:06控制。"},{text:"三个时间是连着的。"}]},'
new = '"admin-shen-record":{yq:[{text:"……"},{text:"你从哪看到这个的？"}],ly:[{text:"这些时间都记得这么细？"},{text:"10月16号那几条……截图。"}],zc:[{text:"19:49转交，20:52采血，21:06控制。"},{text:"三个时间是连着的。"}]},'
if new not in s:
    s = replace_once(s, old, new, 'Yuqing admin material rule')
quick_marker = 'const quickAfterMaterial=(contactId:string,materialId:string):QuickReply[]=>{\n'
quick_insert = ''' if(contactId==="yq"&&materialId==="admin-shen-record")return [
  {id:"yq-admin-transfer",text:"你说九点左右才走。后台为什么19:49已经写了‘线下转交’？",emphasis:true,reply:[{text:"……"},{text:"那个人十九点多就到了。"},{text:"我把沈妍交给她以后，剩下的不是我负责。"}],next:[
   {id:"yq-admin-chat",text:"那20:46和21:03这些聊天呢？",reply:[{text:"‘你不吃了’和‘到家说一声’是他们让我发的。"},{text:"沈妍账号后来回的那几句，不是她发的。"},{text:"她的手机那时候已经不在她手里了。"}],next:[
    {id:"yq-admin-know",text:"你知道他们会把她怎么样？",reply:[{text:"不知道具体会做什么。"},{text:"我知道那不是普通见面。"},{text:"我只负责把人带到，后面的事他们从来不跟我说。"},{text:"我能说的就这些。"}]}
   ]}
  ]}
 ];
'''
if 'id:"yq-admin-transfer"' not in s:
    s = replace_once(s, quick_marker, quick_marker + quick_insert, 'Yuqing confrontation quick chain')
p.write_text(s)

# 3) Back-end “return-to-nest” system and individual paths
p = Path('app/AdminPortalOccult.tsx')
s = p.read_text()
watch_old = 'function WatchList({openKnown,onCopyMaterial,hasMaterial}:{openKnown:(name:string)=>void;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){return <><h2>观察名单</h2><AddMaterialButton'
watch_new = 'function WatchList({openKnown,onCopyMaterial,hasMaterial}:{openKnown:(name:string)=>void;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){return <><h2>观察名单</h2><section style={{...s.adminPanel,marginTop:10,marginBottom:14}}><h4>归巢索引</h4><Record date="系统状态" title="运行中" meta="旧档投放 / 相似叙述聚类" text="无需主动寻找。异常记忆会自行形成检索行为；命中旧档后自动进入观察候选。"/><Record date="今日" title="自发回流 14" meta="新注册 3 / 旧账号 11" text="高频入口：另一个家 / 名字不对 / 反复梦见 / 走失后变化。"/></section><AddMaterialButton'
if watch_new not in s:
    s = replace_once(s, watch_old, watch_new, 'return-to-nest watch panel')
shen_old = '<Record date="首次录入" title="2021-06-14" meta="自动索引匹配" text="论坛实名映射完成；进入长期观察。"/>'
shen_new = '<Record date="2021-06-14" title="归巢命中" meta="外部检索 → 旧档主题" text="首次由外部检索进入走失后记忆异常相关旧帖；同类主题持续访问后，论坛账号转入长期观察。"/>'
if shen_new not in s:
    s = replace_once(s, shen_old, shen_new, 'Shen return-to-nest record')
liang_old = '<Record date="2017-07-22 23:18" title="加入观察名单" meta="账号：迟迟" text="旧案检索命中；实名映射后持续观察。"/>'
liang_new = '<Record date="2017-07-22 23:18" title="归巢命中" meta="外部检索 → 旧档主题" text="搜索‘回来以后不认识自己家’进入旧帖；注册后实名映射，转入持续观察。"/>'
if liang_new not in s:
    s = replace_once(s, liang_old, liang_new, 'Liang return-to-nest record')
s = s.replace('title="对象类型：返契祭品"', 'title="对象类型：旧对契异常端"', 1)
p.write_text(s)

# 4) Canon: memory hierarchy, Yuqing cover trail, forum return-to-nest mechanism
p = Path('docs/CANON_v3.0_世界观与游戏设定唯一权威集.md')
s = p.read_text()
second_part = '---\n\n# 第二部：人物唯一口径'
return_nest = '''### 2.2 烛阴旧闻的“归巢”功能

烛阴旧闻在表面上仍是一个约 95% 内容都正常的大型民俗 / 旧闻论坛；其深层用途之一是无相还真会用于筛查历史异常对象的**归巢系统**。

核心逻辑不是组织主动在现实社会里逐个寻找旧样本，而是利用真实旧帖、旧案索引与相似叙述，让出现身份错位、旧屋记忆、名字异常、走失后变化等体验的人在无法解释自身经历时自行检索、注册、发帖和停留。

后台可称这套机制为“归巢索引”：

- 旧帖和真实讨论是入口，不要求公开区充斥教团假账号；
- 系统聚类“另一个家 / 名字不对 / 反复梦见 / 走失后变化”等叙述；
- 命中后转入观察候选，再由照骨、折柳等账号进行人工观察或接触；
- 组织会维护、恢复、移动具有筛查价值的旧档，使其长期可被类似对象检索到；
- 恐怖点是：**不是他们先找到了异常者，而是异常记忆最终会把人带回这个论坛。**

后台允许出现固定句：

> **无需主动寻找。异常记忆会自行形成检索行为。**

'''
if '### 2.2 烛阴旧闻的“归巢”功能' not in s:
    s = replace_once(s, second_part, return_nest + second_part, 'canon return-to-nest')
yq_old = '- 不负责深层经文解释。'
yq_new = '''- 不负责深层经文解释；
- 2026-10-16 负责把沈妍带到指定接触点并完成“转交”，知道这不是普通见面，但不知道易舍、再舍、真君序列等核心机制；
- 转交后仍按要求向沈妍微信发送“你不吃了 / 到家说一声”等正常离场信息；沈妍账号随后出现的“胃不舒服 / 不用 / 嗯”等回复由已经持有其手机的一方发送，用于制造她正常离开的聊天轨迹。'''
if '制造她正常离开的聊天轨迹' not in s:
    s = replace_once(s, yq_old, yq_new, 'canon Yuqing cover trail')
mem_anchor = '沈妍出现的是 β 自己作为林楠时的童年记忆，不是“原沈妍记忆回到身体里”。\n\n## 12. 返契'
mem_block = '''沈妍出现的是 β 自己作为林楠时的童年记忆，不是“原沈妍记忆回到身体里”。

### 11.6 易舍后的记忆层级

第一次易舍成功以后，客可能保留或偶发浮现少量原身份记忆碎片，例如口味变化、名字反应、一个旧屋细节或短暂的“另一个家”感觉。这类碎片通常不连续、不足以重建完整身份，**可以长期不影响正常生活**；组织会记录它们，但不能把所有旧样本都写成持续严重失忆或无法生活。

沈妍 2026 年的情况必须与普通旧样本区分：她在 2004 易舍后长期稳定生活约 22 年，早期即使偶有碎片也很浅；真正明显加深发生在 2026-10-12 α 再舍重新牵动旧对契之后。此后 β 的林楠童年记忆从零散元素快速变得连续、具体，并出现空间顺序、动作习惯和强烈“这是发生过的事”的确定感。

因此沈妍私密记录应形成明确层级：

> 前期：记得几个东西，写完会散，白天基本不影响生活。  
> 10 月 12 日后：细节越来越清楚，开始像真实记忆而不是反复梦境。

## 12. 返契'''
if '### 11.6 易舍后的记忆层级' not in s:
    s = replace_once(s, mem_anchor, mem_block, 'canon memory hierarchy')
p.write_text(s)

# 5) Central editable copy maps
add_map_entries('content/forumDialogues.ts', '};\n\nexport const editForumText', [
 '10月14日，越来越清楚了',
 '前几个月不是这样的。那时候醒过来只剩几个东西：红铁皮盒、窗帘、厨房门，还有一个听不清的名字。写下来以后就散了，白天基本不会想起，也没影响我做别的事。',
 '从前天晚上开始不一样。细节不是变多一点，是越来越清楚。我开始知道从餐桌走到厨房要踩过哪几块裂砖，知道杯子平时放在哪一格，甚至知道有人从厨房出来时会先扶一下门框。',
 '这些不是我后来查旧帖查出来的。有些细节我根本没写过，也没在照片里见过。',
 '最让我害怕的是，我现在已经不像是在反复梦见那间屋。',
 '我是在想起一件发生过的事。',
])
add_map_entries('content/wechatLiveDialogues.ts', '};\n\nexport const editWechatLive', [
 '你从哪看到这个的？',
 '你说九点左右才走。后台为什么19:49已经写了‘线下转交’？',
 '那个人十九点多就到了。',
 '我把沈妍交给她以后，剩下的不是我负责。',
 '那20:46和21:03这些聊天呢？',
 '‘你不吃了’和‘到家说一声’是他们让我发的。',
 '沈妍账号后来回的那几句，不是她发的。',
 '她的手机那时候已经不在她手里了。',
 '你知道他们会把她怎么样？',
 '不知道具体会做什么。',
 '我知道那不是普通见面。',
 '我只负责把人带到，后面的事他们从来不跟我说。',
 '我能说的就这些。',
])
add_map_entries('content/adminDialogues.ts', '};\n\nexport const editAdminText', [
 '归巢索引','运行中','旧档投放 / 相似叙述聚类','无需主动寻找。异常记忆会自行形成检索行为；命中旧档后自动进入观察候选。',
 '自发回流 14','新注册 3 / 旧账号 11','高频入口：另一个家 / 名字不对 / 反复梦见 / 走失后变化。',
 '归巢命中','外部检索 → 旧档主题','首次由外部检索进入走失后记忆异常相关旧帖；同类主题持续访问后，论坛账号转入长期观察。',
 '搜索‘回来以后不认识自己家’进入旧帖；注册后实名映射，转入持续观察。','对象类型：旧对契异常端'
])
