from pathlib import Path
import re

page=Path('app/page.tsx')
wx=Path('app/InteractiveWechat.tsx')
admin=Path('app/AdminPortalOccult.tsx')

# PAGE: notify desktop when admin discovery injects incoming WeChat messages.
p=page.read_text(encoding='utf-8')
p=p.replace('<AdminPortalOccult loggedIn={true} canUseLegacy={true} onAdminLogin={()=>{}} onCancel={()=>{}}/>','<AdminPortalOccult loggedIn={true} canUseLegacy={true} onAdminLogin={()=>{}} onCancel={()=>{}} onWechatIncoming={()=>setWxRead(false)}/>',1)
p=p.replace('<AdminPortalOccult loggedIn={false} canUseLegacy={verseSeen} onCancel={back} onAdminLogin={()=>{persistedForumIdentity="admin";setForumIdentity("admin");setStack([])}}/>','<AdminPortalOccult loggedIn={false} canUseLegacy={verseSeen} onCancel={back} onAdminLogin={()=>{persistedForumIdentity="admin";setForumIdentity("admin");setStack([])}} onWechatIncoming={()=>setWxRead(false)}/>',1)
assert 'onWechatIncoming={()=>setWxRead(false)}' in p
page.write_text(p,encoding='utf-8')

# WECHAT: keep only main-story contacts, inject believable admin-discovery messages, and add human replies.
w=wx.read_text(encoding='utf-8')
w=w.replace('  quick:{} as Record<string,QuickReply[]>,\n};','  quick:{} as Record<string,QuickReply[]>,\n  adminBeats:{} as Record<string,boolean>,\n};',1)
# remove Fang Jia and parents contact blocks
w=re.sub(r'\n \{id:"f",name:"方嘉".*?\n \]\},', '', w, count=1, flags=re.S)
w=re.sub(r'\n \{id:"p",name:"爸妈".*?\n \]\},', '', w, count=1, flags=re.S)
# remove their text reply / intro handlers
w=re.sub(r'\n if\(contact==="f"&&/沈妍\|联系不上\|没来/\.test\(t\)\)return .*?;', '', w, count=1)
w=re.sub(r'\n if\(contact==="p"&&/沈妍\|联系不上\|没回/\.test\(t\)\)return .*?;', '', w, count=1)
w=w.replace(' if(contactId==="f")return "你好，我是徐宁，沈妍朋友。她今天没来，也联系不上。我现在在她家，她电脑微信还登着。你今天见过她吗？";\n','',1)
w=w.replace(' if(contactId==="p")return "叔叔阿姨，我是徐宁。沈妍今天一直联系不上，我现在在她家。你们今天跟她联系过吗？";\n','',1)

# richer, human admin-related text replies; insert before existing branches so specificity wins
anchor=''' if(contact==="yq"){\n  if(/昨晚|见面|去哪|在哪/.test(t))return'''
replacement=''' if(contact==="yq"){\n  if(/有消息|找到|找到了/.test(t))return [{text:"还没有吗？"},{text:"她昨晚走的时候真的没说别的。"}];\n  if(/昨晚|见面|去哪|在哪/.test(t))return'''
assert anchor in w
w=w.replace(anchor,replacement,1)

anchor=''' if(contact==="zc"){\n  if(/林楠/.test(t))return'''
replacement=''' if(contact==="zc"){\n  if(/后台|管理系统|管理后台/.test(t))return [{text:"什么后台？"},{text:"先把时间、操作人和原始字段留着。"},{text:"状态词先别急着按字面信。"}];\n  if(/已控制|转交|血样/.test(t))return [{text:"先看时间。"},{text:"能不能跟她昨晚的行程对上？"}];\n  if(/林楠/.test(t))return'''
assert anchor in w
w=w.replace(anchor,replacement,1)

anchor=''' if(contact==="ly"){\n  if(/林楠/.test(t))return'''
replacement=''' if(contact==="ly"){\n  if(/后台|管理系统|管理后台/.test(t))return [{text:"……后台？"},{text:"能查账号吗？"},{text:"那你搜一下我。"},{text:"搜“迟迟”就行。"}];\n  if(/有你|搜到你|你的记录|梁茵/.test(t))return [{text:"操"},{text:"真的有？"},{text:"你先别概括。"},{text:"最早那条是什么时候？"}];\n  if(/2021|三月|第一次线下接触/.test(t))return [{text:"等一下。"},{text:"2021年三月我确实见过一个论坛里认识的女的。"},{text:"就吃了顿饭。她一直问我小时候走失那阵的事。"},{text:"我当时真以为就是网友聊天。"}];\n  if(/18[:：]?42|今天|最后更新|设备记录|定位/.test(t))return [{text:"今天？"},{text:"我今天根本没上论坛。"},{text:"……有点恶心了。"},{text:"我先把定位关了。"},{text:"你继续看，别停。"}];\n  if(/终止转交|2024|转交/.test(t))return [{text:"2024年一月……"},{text:"那次有人本来让我跟她去另一个地方。"},{text:"我没去。临时有人来接我，我就走了。"},{text:"所以他们写的“转交”是这个？"}];\n  if(/沈妍.*已控制|已控制.*沈妍/.test(t))return [{text:"……"},{text:"那先别管我这边。"},{text:"你继续找她现在在哪。"}];\n  if(/林楠/.test(t))return'''
assert anchor in w
w=w.replace(anchor,replacement,1)

# module-level injection API used by admin desk; no NPC omniscience beyond the fact that they message Shen's logged-in account.
insert='''\nexport const triggerAdminWechatBeat=(beat:"shen-record")=>{\n if(wechatSession.adminBeats[beat])return false;\n wechatSession.adminBeats={...wechatSession.adminBeats,[beat]:true};\n const push=(contactId:string,items:Msg[])=>{wechatSession.extra={...wechatSession.extra,[contactId]:[...(wechatSession.extra[contactId]||[]),...items]}};\n push("ly",[{who:"对方",text:"你还在查吗？"},{who:"对方",text:"有找到新的东西吗？"}]);\n push("zc",wechatSession.introduced.zc?[{who:"对方",text:"她还是没消息？"}]:[{who:"对方",text:"你昨天不是还在查旧档吗？今天怎么没动静。"}]);\n push("yq",wechatSession.introduced.yq?[{who:"对方",text:"有消息了吗？"}]:[{who:"对方",text:"你今天好点没？"},{who:"对方",text:"怎么一直没回我。"}]);\n notifyWechat();\n return true;\n};\n\n'''
marker='export default function InteractiveWechat'
assert marker in w
w=w.replace(marker,insert+marker,1)
# dynamic preview should show latest injected message
anchor=''' const messages=useMemo(()=>[...contact.messages,...(extra[id]||[])],[contact,extra,id]);\n const sendable='''
replacement=''' const messages=useMemo(()=>[...contact.messages,...(extra[id]||[])],[contact,extra,id]);\n const previewFor=(c:Contact)=>{const added=extra[c.id]||[];return added.length?added[added.length-1].text:c.preview};\n const sendable='''
assert anchor in w
w=w.replace(anchor,replacement,1)
w=w.replace('{x.preview}</small>','{previewFor(x)}</small>',1)

assert '方嘉｜公司' not in w
assert 'name:"爸妈"' not in w
assert 'triggerAdminWechatBeat' in w
assert '搜“迟迟”就行' in w
wx.write_text(w,encoding='utf-8')

# ADMIN: cold, dense operational database + Shen/Liang records.
a=admin.read_text(encoding='utf-8')
a=a.replace('import {ArrowLeft,ChevronRight,LockKeyhole,Search,ShieldCheck} from "lucide-react";','import {ArrowLeft,ChevronRight,LockKeyhole,Search,ShieldCheck} from "lucide-react";\nimport {triggerAdminWechatBeat} from "./InteractiveWechat";',1)
a=a.replace('type Props={loggedIn:boolean;onAdminLogin:()=>void;onCancel:()=>void;canUseLegacy:boolean};','type Props={loggedIn:boolean;onAdminLogin:()=>void;onCancel:()=>void;canUseLegacy:boolean;onWechatIncoming?:()=>void};',1)
a=a.replace('export default function AdminPortalOccult({loggedIn,onAdminLogin,onCancel,canUseLegacy}:Props){','export default function AdminPortalOccult({loggedIn,onAdminLogin,onCancel,canUseLegacy,onWechatIncoming}:Props){',1)
a=a.replace(' if(loggedIn)return <AdminDesk/>;',' if(loggedIn)return <AdminDesk onWechatIncoming={onWechatIncoming}/>;',1)

start=a.find('function AdminDesk()')
end=a.find('function RitualPhoto()',start)
assert start>=0 and end>start, 'AdminDesk block not found'
new_block=r'''function AdminDesk({onWechatIncoming}:{onWechatIncoming?:()=>void}){
 const [tab,setTab]=useState<"watch"|"users"|"ops"|"recycle">("watch");
 const [q,setQ]=useState("");
 const [searched,setSearched]=useState(false);
 const result=useMemo<"shen"|"liang"|null>(()=>{if(!searched)return null;const t=q.trim();if(/候鸟第七年|沈妍|0712-4471/.test(t))return "shen";if(/迟迟|梁茵|0419-2286/.test(t))return "liang";return null},[searched,q]);
 const fireShenBeat=()=>{if(triggerAdminWechatBeat("shen-record"))onWechatIncoming?.()};
 const doSearch=(e?:FormEvent)=>{e?.preventDefault();setSearched(true);if(/候鸟第七年|沈妍|0712-4471/.test(q.trim()))fireShenBeat()};
 const openKnown=(name:string)=>{setQ(name);setSearched(true);setTab("users");if(/候鸟第七年|沈妍/.test(name))fireShenBeat()};
 return <main style={s.adminPage}>
  <header style={s.adminHead}><div><i>烛</i><span><b>烛阴旧闻</b><small>旧档管理</small></span></div><span style={s.adminAccount}>旧档员-03</span></header>
  <div style={s.adminLayout}>
   <aside style={s.adminSide}><button className={tab==="watch"?"active":""} onClick={()=>setTab("watch")}>观察名单</button><button className={tab==="users"?"active":""} onClick={()=>setTab("users")}>用户查询</button><button className={tab==="ops"?"active":""} onClick={()=>setTab("ops")}>操作记录</button><button className={tab==="recycle"?"active":""} onClick={()=>setTab("recycle")}>删除记录</button></aside>
   <section style={s.adminBody}>
    {tab==="watch"&&<WatchList openKnown={openKnown}/>} 
    {tab==="users"&&<><h2>用户查询</h2><form onSubmit={doSearch} style={s.adminSearch}><Search size={16}/><input value={q} onChange={e=>{setQ(e.target.value);setSearched(false)}} placeholder="用户名 / UID / 关联姓名"/><button>查询</button></form>{searched&&!result&&<p style={s.adminEmpty}>没有匹配用户。</p>}{result==="shen"&&<ShenRecord/>}{result==="liang"&&<LiangRecord/>}</>}
    {tab==="ops"&&<Operations/>}
    {tab==="recycle"&&<Recycle/>}
   </section>
  </div>
 </main>;
}

const watchRows=[
 ["0712-4471","候鸟第七年","沈妍","已控制","10-16 21:06"],
 ["0419-2286","迟迟","梁茵","持续观察","今天 18:42"],
 ["3188-2204","纸鸢北","—","待复核","今天 17:51"],
 ["4410-1733","潮湿墙角","贺某","接触完成","今天 16:27"],
 ["2257-9031","雨停以前","—","观察 II","今天 14:09"],
 ["5830-1642","旧车站","张某","已排除","昨天 23:44"],
 ["7741-0928","白炽灯坏了","—","观察 I","昨天 21:02"],
 ["6602-3511","三号窗","孙某","待复核","10-15 18:06"],
 ["1194-6208","河堤左边","—","已排除","10-15 15:31"],
 ["9021-4470","借火","刘某","观察 II","10-14 22:19"],
 ["3107-0584","九月潮气","—","资料补全","10-14 11:42"],
 ["8172-3306","碎瓷片","王某","观察 I","10-13 20:11"],
 ["5928-7743","旧伞","—","已排除","10-13 08:55"],
 ["2031-9916","南站末班车","赵某","待复核","10-12 19:37"],
 ["7350-1102","台阶第七级","—","观察 II","10-12 03:26"],
];
function WatchList({openKnown}:{openKnown:(name:string)=>void}){return <><h2>观察名单</h2><div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:8,margin:"0 0 14px"}}>{[["活跃观察","83"],["待复核","17"],["本月线下接触","6"],["样本待登记","2"]].map(([k,v])=><span key={k} style={{padding:"10px 12px",border:"1px solid #d5d9d6",background:"#fff"}}><small style={{display:"block",color:"#8a918d"}}>{k}</small><b style={{fontSize:20}}>{v}</b></span>)}</div><div style={{border:"1px solid #d5d9d6",background:"#fff",fontSize:12}}><div style={{display:"grid",gridTemplateColumns:"110px 1.2fr 1fr 1fr 110px",gap:8,padding:"8px 10px",background:"#eef1ef",color:"#6c746f",fontWeight:700}}><span>UID</span><span>论坛账号</span><span>关联姓名</span><span>状态</span><span>最后更新</span></div>{watchRows.map((r,i)=>{const known=r[1]==="候鸟第七年"||r[1]==="迟迟";return <button key={r[0]} onClick={()=>known&&openKnown(r[1])} style={{width:"100%",display:"grid",gridTemplateColumns:"110px 1.2fr 1fr 1fr 110px",gap:8,padding:"9px 10px",border:0,borderTop:"1px solid #edf0ee",background:i%2?"#fbfcfb":"#fff",textAlign:"left",fontSize:12,cursor:known?"pointer":"default"}}><code>{r[0]}</code><b style={{fontWeight:known?700:500}}>{r[1]}</b><span>{r[2]}</span><span>{r[3]}</span><time>{r[4]}</time></button>})}</div></>}

function ShenRecord(){return <article style={s.userRecord}>
 <header style={s.userHead}><i>候</i><span><h3>候鸟第七年</h3><small>实名关联：沈妍 · UID 0712-4471 · 最后活动 2026-10-16 19:48</small></span><em>已控制</em></header>
 <div style={s.statusGrid}><span><small>对契匹配</small><b>92%</b></span><span><small>血样</small><b>已采集</b></span><span><small>当前状态</small><b>已转移</b></span><span><small>下一步</small><b>等待执行</b></span></div>
 <section style={s.adminPanel}><h4>关联信息</h4><Record date="旧案" title="2004-07-17" meta="年龄 9 · 失踪 13 天" text="关联旧案：LN-2004-0718；关联对象：林楠。"/><Record date="首次录入" title="2021-06-14" meta="自动索引匹配" text="论坛实名映射完成；进入长期观察。"/></section>
 <section style={s.adminPanel}><h4>观察记录</h4><Record date="2021-06-14 02:31" title="加入观察名单" meta="自动任务" text="旧案年龄、找回时长与历史样本重合。观察等级 I。"/><Record date="2022-11-03 01:17" title="站内搜索记录" meta="候鸟第七年" text="查询：小时候走失 / 记不得 / 回来以后。"/><Record date="2023-04-19 03:08" title="草稿删除" meta="镜像保留" text="内容涉及“另一个家”；未公开发布。"/><Record date="2024-09-07 00:46" title="旧厂区内容访问" meta="行为记录" text="连续查看岚棉三厂旧址照片 37 分钟。"/><Record date="2025-12-18 02:54" title="附件上传" meta="私密主题" text="室内布局草图与 LN-2004 居住地址局部结构相符。"/><Record date="2026-06-19 03:12" title="内容命中" meta="梦境帖" text="红铁皮盒、蓝窗帘、厨房位置重复出现。"/><Record date="2026-08-22 04:12" title="观察等级调整" meta="操作人：照骨" text="II → III；对契匹配 92%；恢复旧案关联观察。"/><Record date="2026-10-12 22:41" title="公开区接触" meta="监控记录" text="与站内账号发生旧案资料交流。继续观察。"/><Record date="2026-10-16 19:49" title="线下转交" meta="执行：旧档员-03" text="完成。停止公开区接触。"/><Record date="2026-10-16 20:52" title="样本登记" meta="内部任务" text="血样 2 管；保存状态：有效。"/><Record date="2026-10-16 21:06" title="人员状态变更" meta="旧档员-03" text="观察中 → 已控制。"/></section>
 <section style={s.adminPanel}><h4>执行信息</h4><Record date="HN-1016-02" title="对象类型：返契祭品" meta="执行批次" text="主祭：未分配；执行条件：待复核。"/></section>
 <section style={s.adminPanel}><h4>私密内容镜像</h4><Record date="2026-06-19 03:12" title="昨晚又梦到了" meta="仅自己可见 · 自动镜像" text="红铁皮盒、蓝窗帘，还有那个听不清的称呼。"/><Record date="2026-09-11 02:08" title="9月11日，几条旧帖" meta="仅自己可见 · 自动镜像" text="另一个家、回来以后不会以前会的东西。"/></section>
 </article>}

function LiangRecord(){return <article style={s.userRecord}>
 <header style={s.userHead}><i>迟</i><span><h3>迟迟</h3><small>实名关联：梁茵 · UID 0419-2286 · 关联设备仍在线</small></span><em>持续观察</em></header>
 <div style={s.statusGrid}><span><small>对契匹配</small><b>74%</b></span><span><small>旧案记录</small><b>匹配</b></span><span><small>线下接触</small><b>2 次</b></span><span><small>最后更新</small><b>今天 18:42</b></span></div>
 <section style={s.adminPanel}><h4>观察记录</h4><Record date="2017-07-22 23:18" title="加入观察名单" meta="账号：迟迟" text="旧案检索命中；实名映射后持续观察。"/><Record date="2018-01-03 02:11" title="站内搜索记录" meta="行为记录" text="查询：回来以后 / 不认识自己家 / 小时候走失。"/><Record date="2019-04-17 01:26" title="草稿删除" meta="镜像保留" text="未发布内容涉及“另一个家”。"/><Record date="2020-11-06 18:31" title="身份资料补全" meta="后台人工" text="实名、旧案、常用设备关联完成。"/><Record date="2021-03-12 19:08" title="线下接触 1" meta="批次 QW-21-03" text="完成基础问询；对象未意识到测试性质。"/><Record date="2022-08-29 20:14" title="物件反应记录" meta="接触后补录" text="固定物件识别无明显结果；保留观察。"/><Record date="2024-01-08 18:52" title="线下接触 2" meta="批次 QW-24-01" text="原计划进入下一地点；对象提前离开。"/><Record date="2024-01-08 19:07" title="终止转交" meta="现场记录" text="陪同人员提前出现；对象离开。未继续。"/><Record date="2025-06-19 03:29" title="建立关联观察" meta="关联 UID 0712-4471" text="与候鸟第七年公开互动频率上升。"/><Record date="2026-08-22 04:18" title="恢复高频观察" meta="自动任务" text="因 UID 0712-4471 匹配值升高，重新启用关联记录。"/><Record date="2026-10-17 18:42" title="设备记录刷新" meta="自动写入" text="关联设备 P-4477；位置采样：河临北区。"/></section>
 <section style={s.adminPanel}><h4>备注</h4><Record date="当前" title="对象未确认被观察" meta="内部备注" text="不主动接触；保留设备与公开区记录。"/></section>
 </article>}

function Operations(){return <><h2>操作记录</h2><div style={s.adminPanel}><Record date="2026-10-17 18:42" title="设备记录刷新：0419-2286" meta="自动任务" text="P-4477 / 河临北区"/><Record date="2026-10-17 17:51" title="新增待复核对象：3188-2204" meta="自动任务" text="旧案索引匹配 61%"/><Record date="2026-10-17 16:27" title="线下接触完成：4410-1733" meta="执行组 02" text="返回持续观察"/><Record date="2026-10-16 21:06" title="人员状态变更：0712-4471" meta="旧档员-03" text="观察中 → 已控制"/><Record date="2026-10-16 20:52" title="样本登记：0712-4471" meta="内部任务" text="血样 2 管 / 有效"/><Record date="2026-10-16 19:49" title="线下转交：0712-4471" meta="旧档员-03" text="完成"/><Record date="2026-10-16 18:31" title="草稿镜像写入：0712-4471" meta="自动任务" text="1 条"/><Record date="2026-10-15 23:17" title="观察等级调整：4410-1733" meta="照骨" text="I → II"/><Record date="2026-10-15 18:06" title="关键词命中：6602-3511" meta="公开区" text="进入待复核"/><Record date="2026-10-14 22:19" title="观察记录更新：9021-4470" meta="自动任务" text="新增 3 条行为记录"/><Record date="2026-10-14 11:42" title="资料补全：3107-0584" meta="人工" text="实名关联失败"/><Record date="2026-10-13 20:11" title="新增观察：8172-3306" meta="自动任务" text="等级 I"/><Record date="2026-10-12 03:26" title="观察等级调整：7350-1102" meta="照骨" text="I → II"/><Record date="2026-08-22 04:18" title="恢复关联观察：0419-2286" meta="自动任务" text="关联 0712-4471"/><Record date="2026-08-22 04:12" title="观察等级调整：0712-4471" meta="照骨" text="II → III；匹配 92%"/></div></>}
function Recycle(){return <><h2>删除记录</h2><div style={s.adminPanel}><Record date="2026-10-16 18:31" title="未发布草稿" meta="候鸟第七年 · 已删除" text="原始内容已删除；镜像保留。"/><Record date="2026-10-16 20:47" title="IMG_1016_2047.jpg" meta="现场终端 03" text="上传 20:47；原始文件已删除；缓存缩略图可用。"/><RitualPhoto/><Record date="2013-07-09 03:14" title="旧教页缓存" meta="旧档恢复 · 已删除" text="页面文件已删除；缓存图像与文字层仍可读。"/><figure style={s.scripture}><img src="assets/occult/huanzhen-scripture-v904.webp" alt="无相还真会黑底朱字旧教页"/></figure></div></>}
'''
a=a[:start]+new_block+a[end:]
assert '旧客回响' not in a
assert '归门观察' not in a
assert '添加归门标记' not in a
assert 'function LiangRecord' in a
assert '观察名单' in a
admin.write_text(a,encoding='utf-8')

print('v9.1.0 admin + NPC scene patch applied')
