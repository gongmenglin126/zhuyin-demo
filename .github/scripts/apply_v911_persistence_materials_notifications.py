from pathlib import Path
import re

page=Path('app/page.tsx')
wx=Path('app/InteractiveWechat.tsx')
admin=Path('app/AdminPortalOccult.tsx')

# ---------- page.tsx ----------
p=page.read_text(encoding='utf-8')
p=p.replace('import InteractiveWechat,{SharedMaterial} from "./InteractiveWechat";', 'import InteractiveWechat,{SharedMaterial,WechatNotice,focusWechatContact,subscribeWechatNotices} from "./InteractiveWechat";', 1)
old='''let persistedForumIdentity:"shenyan"|"admin"="shenyan";\nlet persistedForumRead:string[]=[];'''
new='''let persistedForumIdentity:"shenyan"|"admin"="shenyan";\nlet persistedForumRead:string[]=[];\nlet persistedForumRoute:Route={kind:"home"};\nlet persistedForumStack:Route[]=[];\nlet persistedForumQ="";'''
assert old in p
p=p.replace(old,new,1)
old=''' const [materials,setMaterials]=useState<SharedMaterial[]>([]);\n const [verseSeen,setVerseSeen]=useState(false);\n const [wxPost,setWxPost]=useState<string|null>(null);\n const rememberMaterial=(m:SharedMaterial)=>setMaterials(prev=>prev.some(x=>x.id===m.id)?prev:[...prev,m]);'''
new=''' const [materials,setMaterials]=useState<SharedMaterial[]>([]);\n const [verseSeen,setVerseSeen]=useState(false);\n const [wxPost,setWxPost]=useState<string|null>(null);\n const [wxNotices,setWxNotices]=useState<(WechatNotice&{id:number})[]>([]);\n const rememberMaterial=(m:SharedMaterial)=>setMaterials(prev=>prev.some(x=>x.id===m.id)?prev:[...prev,m]);\n useEffect(()=>subscribeWechatNotices(notice=>{\n  if(app==="wechat")return;\n  const item={...notice,id:Date.now()+Math.floor(Math.random()*1000)};\n  setWxRead(false);\n  setWxNotices(prev=>[...prev.filter(x=>x.contactId!==notice.contactId),item].slice(-3));\n  window.setTimeout(()=>setWxNotices(prev=>prev.filter(x=>x.id!==item.id)),6500);\n }),[app]);'''
assert old in p
p=p.replace(old,new,1)

old='''  {app&&<Window title={appTitle} max={max} allowMax={app==="browser"||app==="verse"} close={()=>setApp(null)} toggle={()=>setMax(!max)}>{app==="browser"?<Browser privateUnlocked={privateUnlocked} setPrivateUnlocked={setPrivateUnlocked} onCopyMaterial={rememberMaterial} hasMaterial={id=>materials.some(m=>m.id===id)} verseSeen={verseSeen} initialPostId={wxPost} onInitialPostConsumed={()=>setWxPost(null)}/>:app==="wechat"?<InteractiveWechat materials={materials} onOpenPost={id=>{setWxPost(id);setApp("browser");setMax(true)}}/>:app==="notes"?<LocalVault unlocked={noteUnlocked} onUnlock={()=>setNoteUnlocked(true)} openLink={()=>{setVerseSeen(true);open("verse")}}/>:<VersePage onCopyMaterial={rememberMaterial} hasMaterial={id=>materials.some(m=>m.id===id)}/>}</Window>}\n  <nav className="dock">'''
new='''  {app&&<Window title={appTitle} max={max} allowMax={app==="browser"||app==="verse"} close={()=>setApp(null)} toggle={()=>setMax(!max)}>{app==="browser"?<Browser privateUnlocked={privateUnlocked} setPrivateUnlocked={setPrivateUnlocked} onCopyMaterial={rememberMaterial} hasMaterial={id=>materials.some(m=>m.id===id)} verseSeen={verseSeen} initialPostId={wxPost} onInitialPostConsumed={()=>setWxPost(null)}/>:app==="wechat"?<InteractiveWechat materials={materials} onOpenPost={id=>{setWxPost(id);setApp("browser");setMax(true)}}/>:app==="notes"?<LocalVault unlocked={noteUnlocked} onUnlock={()=>setNoteUnlocked(true)} openLink={()=>{setVerseSeen(true);open("verse")}}/>:<VersePage onCopyMaterial={rememberMaterial} hasMaterial={id=>materials.some(m=>m.id===id)}/>}</Window>}\n  {!!wxNotices.length&&<div style={{position:"fixed",right:18,top:38,zIndex:80,width:310,display:"grid",gap:8}}>{wxNotices.map(n=><button key={n.id} onClick={()=>{focusWechatContact(n.contactId);setWxNotices(prev=>prev.filter(x=>x.contactId!==n.contactId));open("wechat")}} style={{display:"grid",gridTemplateColumns:"38px 1fr",gap:10,alignItems:"center",padding:"11px 12px",border:"1px solid #d7ddd9",borderRadius:10,background:"#fff",boxShadow:"0 10px 30px #0003",textAlign:"left",cursor:"pointer"}}><i style={{width:36,height:36,display:"grid",placeItems:"center",borderRadius:9,background:"#2bbd60",color:"#fff",fontStyle:"normal"}}><MessageCircle size={19}/></i><span style={{minWidth:0}}><b style={{display:"block",fontSize:12}}>微信 · {n.name}</b><small style={{display:"block",marginTop:3,color:"#666",whiteSpace:"nowrap",overflow:"hidden",textOverflow:"ellipsis"}}>{n.text}</small></span></button>)}</div>}\n  <nav className="dock">'''
assert old in p
p=p.replace(old,new,1)

old=''' const [route,setRoute]=useState<Route>(initialPostId?{kind:"post",id:initialPostId}:{kind:"home"}),[stack,setStack]=useState<Route[]>([]),[q,setQ]=useState(""),[read,setRead]=useState<string[]>(()=>[...new Set([...persistedForumRead,...(initialPostId?[initialPostId]:[])])]);'''
new=''' const [route,setRoute]=useState<Route>(()=>initialPostId?{kind:"post",id:initialPostId}:persistedForumRoute),[stack,setStack]=useState<Route[]>(()=>initialPostId?[...persistedForumStack,persistedForumRoute]:persistedForumStack),[q,setQ]=useState(()=>persistedForumQ),[read,setRead]=useState<string[]>(()=>[...new Set([...persistedForumRead,...(initialPostId?[initialPostId]:[])])]);'''
assert old in p
p=p.replace(old,new,1)
old=''' useEffect(()=>{if(initialPostId)onInitialPostConsumed()},[]);'''
new=''' useEffect(()=>{if(initialPostId)onInitialPostConsumed()},[]);\n useEffect(()=>{persistedForumRoute=route;persistedForumStack=stack;persistedForumQ=q},[route,stack,q]);'''
assert old in p
p=p.replace(old,new,1)

# add materials props to admin portal instances
p=p.replace('''<AdminPortalOccult loggedIn={true} canUseLegacy={true} onAdminLogin={()=>{}} onCancel={()=>{}} onWechatIncoming={()=>setWxRead(false)}/>''','''<AdminPortalOccult loggedIn={true} canUseLegacy={true} onAdminLogin={()=>{}} onCancel={()=>{}} onWechatIncoming={()=>setWxRead(false)} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>''',1)
p=p.replace('''<AdminPortalOccult loggedIn={false} canUseLegacy={verseSeen} onCancel={back} onAdminLogin={()=>{persistedForumIdentity="admin";setForumIdentity("admin");setStack([])}} onWechatIncoming={()=>setWxRead(false)}/>''','''<AdminPortalOccult loggedIn={false} canUseLegacy={verseSeen} onCancel={back} onAdminLogin={()=>{persistedForumIdentity="admin";setForumIdentity("admin");setStack([])}} onWechatIncoming={()=>setWxRead(false)} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>''',1)
page.write_text(p,encoding='utf-8')

# ---------- InteractiveWechat.tsx ----------
w=wx.read_text(encoding='utf-8')
w=w.replace('''export type SharedMaterial={id:string;title:string;kind:string;url:string};''','''export type SharedMaterial={id:string;title:string;kind:string;url:string};\nexport type WechatNotice={contactId:string;name:string;text:string};''',1)
w=w.replace('''  quick:{} as Record<string,QuickReply[]>,\n  adminBeats:{} as Record<string,boolean>,''','''  quick:{} as Record<string,QuickReply[]>,\n  adminBeats:{} as Record<string,boolean>,\n  activeId:"x",\n  searchQuery:"",\n  draft:"",''',1)
marker='];\n\nconst materialRules:Record<string,MaterialRule>={'
assert marker in w
notice_code='''\nconst wechatNoticeSubscribers=new Set<(notice:WechatNotice)=>void>();\nexport const subscribeWechatNotices=(fn:(notice:WechatNotice)=>void)=>{wechatNoticeSubscribers.add(fn);return ()=>wechatNoticeSubscribers.delete(fn)};\nconst emitWechatNotice=(contactId:string,text:string)=>{const c=contacts.find(x=>x.id===contactId);if(c)wechatNoticeSubscribers.forEach(fn=>fn({contactId,name:c.name,text}))};\nexport const focusWechatContact=(contactId:string)=>{if(contacts.some(x=>x.id===contactId))wechatSession.activeId=contactId};\n\n'''
w=w.replace(marker,'];\n'+notice_code+'const materialRules:Record<string,MaterialRule>={',1)

# admin materials become sendable
old=''' "27614":{zc:[{text:"这篇我有印象。"},{text:"站务后来不是说多人轮用吗。"}],ly:[{text:"我以前没点进去看过。"}]},\n};'''
new=''' "27614":{zc:[{text:"这篇我有印象。"},{text:"站务后来不是说多人轮用吗。"}],ly:[{text:"我以前没点进去看过。"}]},\n "admin-watchlist":{ly:[{text:"这么多人？"},{text:"……迟迟也在里面？"}],zc:[{text:"先留着。"},{text:"这至少能证明不是只围着沈妍一个人建的后台。"}]},\n "admin-shen-record":{ly:[{text:"这些时间都记得这么细？"},{text:"10月16号那几条……你先留好。"}],zc:[{text:"把19:49、20:52、21:06这三条单独记下来。"},{text:"转交、样本、状态变更是连续的。"}]},\n "admin-liang-record":{ly:[{text:"操。"},{text:"真的是我。"},{text:"你先别往下猜，最早那条是什么时候？"}],zc:[{text:"这是梁茵那份？"},{text:"今天18:42还在自动刷新，说明这系统现在还在跑。"}]},\n};'''
assert old in w
w=w.replace(old,new,1)

# make admin beat emit real desktop notifications
old=''' push("ly",[{who:"对方",text:"你还在查吗？"},{who:"对方",text:"有找到新的东西吗？"}]);\n push("zc",wechatSession.introduced.zc?[{who:"对方",text:"她还是没消息？"}]:[{who:"对方",text:"你昨天不是还在查旧档吗？今天怎么没动静。"}]);\n push("yq",wechatSession.introduced.yq?[{who:"对方",text:"有消息了吗？"}]:[{who:"对方",text:"你今天好点没？"},{who:"对方",text:"怎么一直没回我。"}]);\n notifyWechat();'''
new=''' const lyItems=[{who:"对方" as const,text:"你还在查吗？"},{who:"对方" as const,text:"有找到新的东西吗？"}];\n const zcItems=wechatSession.introduced.zc?[{who:"对方" as const,text:"她还是没消息？"}]:[{who:"对方" as const,text:"你昨天不是还在查旧档吗？今天怎么没动静。"}];\n const yqItems=wechatSession.introduced.yq?[{who:"对方" as const,text:"有消息了吗？"}]:[{who:"对方" as const,text:"你今天好点没？"},{who:"对方" as const,text:"怎么一直没回我。"}];\n push("ly",lyItems);push("zc",zcItems);push("yq",yqItems);\n emitWechatNotice("ly",lyItems[lyItems.length-1].text);\n emitWechatNotice("zc",zcItems[zcItems.length-1].text);\n emitWechatNotice("yq",yqItems[yqItems.length-1].text);\n notifyWechat();'''
assert old in w
w=w.replace(old,new,1)

# persist selected contact/search/draft across app switches
old=''' const [id,setId]=useState("x"),[q,setQ]=useState(""),[draft,setDraft]=useState(""),[picker,setPicker]=useState(false);'''
new=''' const [id,setId]=useState(()=>wechatSession.activeId),[q,setQ]=useState(()=>wechatSession.searchQuery),[draft,setDraft]=useState(()=>wechatSession.draft),[picker,setPicker]=useState(false);'''
assert old in w
w=w.replace(old,new,1)
old=''' useEffect(()=>{\n  const el=scrollRef.current;'''
new=''' useEffect(()=>{wechatSession.activeId=id;wechatSession.searchQuery=q;wechatSession.draft=draft},[id,q,draft]);\n useEffect(()=>{\n  const el=scrollRef.current;'''
assert old in w
w=w.replace(old,new,1)

# incoming delayed replies should also create notifications when WeChat isn't active
old=''' const appendFor=(contactId:string,items:Msg[])=>{\n  wechatSession.extra={...wechatSession.extra,[contactId]:[...(wechatSession.extra[contactId]||[]),...items]};\n  notifyWechat();\n };'''
new=''' const appendFor=(contactId:string,items:Msg[])=>{\n  wechatSession.extra={...wechatSession.extra,[contactId]:[...(wechatSession.extra[contactId]||[]),...items]};\n  const incoming=[...items].reverse().find(x=>x.who==="对方"&&!!x.text);\n  if(incoming?.text)emitWechatNotice(contactId,incoming.text);\n  notifyWechat();\n };'''
assert old in w
w=w.replace(old,new,1)
wx.write_text(w,encoding='utf-8')

# ---------- AdminPortalOccult.tsx ----------
a=admin.read_text(encoding='utf-8')
a=a.replace('import {FormEvent,useMemo,useState} from "react";', 'import {FormEvent,useEffect,useMemo,useState} from "react";',1)
a=a.replace('import {triggerAdminWechatBeat} from "./InteractiveWechat";', 'import {SharedMaterial,triggerAdminWechatBeat} from "./InteractiveWechat";',1)
old='''type Props={loggedIn:boolean;onAdminLogin:()=>void;onCancel:()=>void;canUseLegacy:boolean;onWechatIncoming?:()=>void};'''
new='''type Props={loggedIn:boolean;onAdminLogin:()=>void;onCancel:()=>void;canUseLegacy:boolean;onWechatIncoming?:()=>void;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean};'''
assert old in a
a=a.replace(old,new,1)
old='''export default function AdminPortalOccult({loggedIn,onAdminLogin,onCancel,canUseLegacy,onWechatIncoming}:Props){'''
new='''export default function AdminPortalOccult({loggedIn,onAdminLogin,onCancel,canUseLegacy,onWechatIncoming,onCopyMaterial,hasMaterial}:Props){'''
a=a.replace(old,new,1)
old=''' if(loggedIn)return <AdminDesk onWechatIncoming={onWechatIncoming}/>;'''
new=''' if(loggedIn)return <AdminDesk onWechatIncoming={onWechatIncoming} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>;'''
assert old in a
a=a.replace(old,new,1)

# persistent admin UI session + material constants
marker='''function AdminDesk({onWechatIncoming}:{onWechatIncoming?:()=>void}){'''
assert marker in a
insert='''const adminDeskSession:{tab:"watch"|"users"|"ops"|"recycle";q:string;searched:boolean}={tab:"watch",q:"",searched:false};\nconst adminWatchMaterial:SharedMaterial={id:"admin-watchlist",title:"旧档管理 · 观察名单",kind:"后台记录",url:"https://www.zhuyinwen.cn/admin/watch"};\nconst adminShenMaterial:SharedMaterial={id:"admin-shen-record",title:"候鸟第七年 · 后台记录",kind:"后台记录",url:"https://www.zhuyinwen.cn/admin/users/0712-4471"};\nconst adminLiangMaterial:SharedMaterial={id:"admin-liang-record",title:"迟迟 · 后台记录",kind:"后台记录",url:"https://www.zhuyinwen.cn/admin/users/0419-2286"};\n\nfunction AddMaterialButton({material,onCopyMaterial,hasMaterial}:{material:SharedMaterial;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){if(!onCopyMaterial)return null;const added=!!hasMaterial?.(material.id);return <button disabled={added} onClick={()=>onCopyMaterial(material)} style={{margin:"0 0 12px",padding:"7px 10px",border:"1px solid #b9c3bd",borderRadius:6,background:added?"#eef1ef":"#fff",color:"#40564c",fontSize:12,cursor:added?"default":"pointer",opacity:added?.6:1}}>{added?"已添加到材料":"添加到材料"}</button>}\n\nfunction AdminDesk({onWechatIncoming,onCopyMaterial,hasMaterial}:{onWechatIncoming?:()=>void;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){'''
a=a.replace(marker,insert,1)
old=''' const [tab,setTab]=useState<"watch"|"users"|"ops"|"recycle">("watch");\n const [q,setQ]=useState("");\n const [searched,setSearched]=useState(false);'''
new=''' const [tab,setTab]=useState<"watch"|"users"|"ops"|"recycle">(()=>adminDeskSession.tab);\n const [q,setQ]=useState(()=>adminDeskSession.q);\n const [searched,setSearched]=useState(()=>adminDeskSession.searched);'''
assert old in a
a=a.replace(old,new,1)
old=''' const result=useMemo<"shen"|"liang"|null>(()=>{if(!searched)return null;const t=q.trim();if(/候鸟第七年|沈妍|0712-4471/.test(t))return "shen";if(/迟迟|梁茵|0419-2286/.test(t))return "liang";return null},[searched,q]);\n const fireShenBeat=()=>{if(triggerAdminWechatBeat("shen-record"))onWechatIncoming?.()};'''
new=''' const result=useMemo<"shen"|"liang"|null>(()=>{if(!searched)return null;const t=q.trim();if(/候鸟第七年|沈妍|0712-4471/.test(t))return "shen";if(/迟迟|梁茵|0419-2286/.test(t))return "liang";return null},[searched,q]);\n useEffect(()=>{adminDeskSession.tab=tab;adminDeskSession.q=q;adminDeskSession.searched=searched},[tab,q,searched]);\n useEffect(()=>{const timer=window.setTimeout(()=>{if(triggerAdminWechatBeat("shen-record"))onWechatIncoming?.()},900);return ()=>window.clearTimeout(timer)},[]);\n const fireShenBeat=()=>{if(triggerAdminWechatBeat("shen-record"))onWechatIncoming?.()};'''
assert old in a
a=a.replace(old,new,1)

# pass material props into views
a=a.replace('''{tab==="watch"&&<WatchList openKnown={openKnown}/>}''','''{tab==="watch"&&<WatchList openKnown={openKnown} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>}''',1)
a=a.replace('''{result==="shen"&&<ShenRecord/>}{result==="liang"&&<LiangRecord/>}''','''{result==="shen"&&<ShenRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>} {result==="liang"&&<LiangRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>}''',1)
old='''function WatchList({openKnown}:{openKnown:(name:string)=>void}){return <><h2>观察名单</h2>'''
new='''function WatchList({openKnown,onCopyMaterial,hasMaterial}:{openKnown:(name:string)=>void;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){return <><h2>观察名单</h2><AddMaterialButton material={adminWatchMaterial} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>'''
assert old in a
a=a.replace(old,new,1)
old='''function ShenRecord(){return <article style={s.userRecord}>\n <header style={s.userHead}><i>候</i><span><h3>候鸟第七年</h3><small>实名关联：沈妍 · UID 0712-4471 · 最后活动 2026-10-16 19:48</small></span><em>已控制</em></header>'''
new='''function ShenRecord({onCopyMaterial,hasMaterial}:{onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){return <article style={s.userRecord}>\n <header style={s.userHead}><i>候</i><span><h3>候鸟第七年</h3><small>实名关联：沈妍 · UID 0712-4471 · 最后活动 2026-10-16 19:48</small></span><em>已控制</em></header>\n <AddMaterialButton material={adminShenMaterial} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>'''
assert old in a
a=a.replace(old,new,1)
old='''function LiangRecord(){return <article style={s.userRecord}>\n <header style={s.userHead}><i>迟</i><span><h3>迟迟</h3><small>实名关联：梁茵 · UID 0419-2286 · 关联设备仍在线</small></span><em>持续观察</em></header>'''
new='''function LiangRecord({onCopyMaterial,hasMaterial}:{onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){return <article style={s.userRecord}>\n <header style={s.userHead}><i>迟</i><span><h3>迟迟</h3><small>实名关联：梁茵 · UID 0419-2286 · 关联设备仍在线</small></span><em>持续观察</em></header>\n <AddMaterialButton material={adminLiangMaterial} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>'''
assert old in a
a=a.replace(old,new,1)
admin.write_text(a,encoding='utf-8')

# ---------- self-check ----------
p2=page.read_text(encoding='utf-8'); w2=wx.read_text(encoding='utf-8'); a2=admin.read_text(encoding='utf-8')
checks=[
 ('forum route persistence','persistedForumRoute' in p2 and 'persistedForumStack' in p2),
 ('desktop wx toast','subscribeWechatNotices' in p2 and '微信 · {n.name}' in p2),
 ('wx ui persistence','wechatSession.activeId' in w2 and 'wechatSession.searchQuery' in w2),
 ('admin materials','admin-shen-record' in w2 and 'AddMaterialButton' in a2),
 ('admin open beat','window.setTimeout(()=>{if(triggerAdminWechatBeat' in a2),
 ('admin ui persistence','adminDeskSession' in a2),
]
for name,ok in checks:
    assert ok,name
print('v9.1.1 persistence + admin materials + WeChat notification patch applied')
