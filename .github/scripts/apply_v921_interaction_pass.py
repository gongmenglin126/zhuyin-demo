from pathlib import Path
import re

BRANCH_MARK='// v9.2.1 interaction pass'
wx_path=Path('app/InteractiveWechat.tsx')
page_path=Path('app/page.tsx')
admin_path=Path('app/AdminPortalOccult.tsx')
data_path=Path('content/gameDataFlowV2.ts')

wx=wx_path.read_text()
if BRANCH_MARK in wx:
    print('v9.2.1 already applied')
    raise SystemExit(0)
page=page_path.read_text()
admin=admin_path.read_text()
data=data_path.read_text()

def rep(src, old, new, name):
    if old not in src:
        raise RuntimeError(f'missing marker: {name}')
    return src.replace(old,new,1)

# ---- WeChat: shared clock, first-contact timestamps, subtle Zhou=Zheliu hint ----
wx=rep(wx,
'"use client";\n\nimport {FormEvent,useEffect,useMemo,useRef,useState} from "react";',
'"use client";\n'+BRANCH_MARK+'\n\nimport {FormEvent,useEffect,useMemo,useRef,useState} from "react";\nimport {advanceGameClock} from "./gameClock";',
'wx imports')
wx=rep(wx,
'type Contact={id:string;name:string;note:string;preview:string;messages:Msg[]};',
'type Contact={id:string;name:string;note:string;preview:string;signature?:string;messages:Msg[]};',
'contact signature')
wx=rep(wx,
'type QuickReply={id:string;text:string;reply:ReplyPart[];next?:QuickReply[]};',
'type QuickReply={id:string;text:string;sendText?:string;emphasis?:boolean;reply:ReplyPart[];next?:QuickReply[]};',
'quick metadata')
wx=rep(wx,
'  adminBeats:{} as Record<string,boolean>,\n  activeId:"x",',
'  adminBeats:{} as Record<string,boolean>,\n  firstContact:{} as Record<string,string>,\n  zhouEvidenceSeen:false,\n  zhouConfronted:false,\n  activeId:"x",',
'wechat session contact time')
wx=rep(wx,
'{id:"zc",name:"周川",note:"周川｜烛阴旧闻",preview:"我回了一条",messages:[',
'{id:"zc",name:"周川",note:"周川｜烛阴旧闻",preview:"我回了一条",signature:"柳枝别折，怪可惜的。",messages:[',
'zhou signature')

# Make Zhou less AI-investigator-ish in admin-material reactions.
for old,new in [
('"admin-watchlist":{ly:[{text:"这么多人？"},{text:"……迟迟也在里面？"}],zc:[{text:"先留着。"},{text:"这至少能证明不是只围着沈妍一个人建的后台。"}]}',
 '"admin-watchlist":{ly:[{text:"这么多人？"},{text:"……迟迟也在里面？"}],zc:[{text:"这么多人？"},{text:"这后台不像临时搭的。"}]}'),
('"admin-shen-record":{ly:[{text:"这些时间都记得这么细？"},{text:"10月16号那几条……你先留好。"}],zc:[{text:"把19:49、20:52、21:06这三条单独记下来。"},{text:"转交、样本、状态变更是连续的。"}]}',
 '"admin-shen-record":{ly:[{text:"这些时间都记得这么细？"},{text:"10月16号那几条……截图。"}],zc:[{text:"19:49转交，20:52采血，21:06控制。"},{text:"三个时间是连着的。"}]}'),
('"admin-pair-2004":{ly:[{text:"等一下。"},{text:"‘舍’是身体，‘客’是魂，对吧？"},{text:"那这不就是……把她俩的魂换了吗？"}],zc:[{text:"这份比经文有用。"},{text:"至少它明确写了两边互换，而且执行完成。"}]}',
 '"admin-pair-2004":{ly:[{text:"A、B两边的‘客源’为什么正好写的是对方？"},{text:"这两个字段得跟前面那几句经文一起看。"}],zc:[{text:"这份比经文直接。"},{text:"A、B两边都写了易舍完成。"}]}'),
('"admin-reswap-2026":{ly:[{text:"原来第二次根本不是冲沈妍来的。"},{text:"他们是在拿林楠那一侧做第二次换身体的试验。"},{text:"因为那边那个‘客’已经稳定活了二十多年，他们想看同一个人还能不能再换一次。"}],zc:[{text:"把试验目的和执行时间留着。"},{text:"这能解释他们为什么选一个旧案幸存者。"}]}',
 '"admin-reswap-2026":{ly:[{text:"这里写的是‘再次易舍’，而且特意标了稳定期22年。"},{text:"试验目的那句你怎么看？"}],zc:[{text:"稳定22年以后又做一次。"},{text:"这不像临时决定的。"}]}'),
('"admin-sync-shen":{ly:[{text:"所以对上了。"},{text:"林楠那边第二次一换，沈妍这边才开始梦到那些不属于她的童年。"},{text:"他们抓沈妍，不是要再换她一次，是因为旧的那条联系重新有反应。"}],zc:[{text:"这条已经是他们自己的因果判断。"},{text:"先别管玄学真假，‘控制’和执行批次都留着。"}]}',
 '"admin-sync-shen":{ly:[{text:"时间真的挨得很近。"},{text:"10月12号那边执行完，沈妍这一侧就开始升高。"}],zc:[{text:"他们自己把这条标成了关联异常。"},{text:"‘控制’和执行批次比解释更重要。"}]}'),
('"admin-third-1907":{ly:[{text:"她一直说自己叫沈妍？"},{text:"……那2004年被换进林楠身体里的那个，到底是谁。"}],zc:[{text:"这人的身份陈述值得单独留。"},{text:"如果报警，别只报沈妍一个。"}]}',
 '"admin-third-1907":{ly:[{text:"她一直说自己叫沈妍？"},{text:"还主动要求联系徐宁……这句挺吓人的。"}],zc:[{text:"她连续四次都这么说？"},{text:"那不像一次口误。"}]}')]:
    if old in wx: wx=wx.replace(old,new,1)

# Context-aware material replies: facts first, conclusion later.
insert='''\n if(contactId==="ly"&&materialId==="admin-reswap-2026"&&!received("ly","admin-pair-2004"))return [{text:"这里写的是‘再次易舍’。"},{text:"但第一次是哪次？你手里是不是还有2004年的旧案？"}];\n if(contactId==="ly"&&materialId==="admin-sync-shen"&&!received("ly","admin-reswap-2026"))return [{text:"这条只有结果，没有前因。"},{text:"10月12号那边到底做了什么，得先对上。"}];\n'''
wx=rep(wx,' return materialRules[materialId]?.[contactId]??null;\n};',insert+' return materialRules[materialId]?.[contactId]??null;\n};','context material replies')

# Replace auto-answering admin quick replies with actual player reasoning choices.
old=''' if(contactId==="ly"&&materialId==="admin-pair-2004")return [{id:"ly-pair-question",text:"我也是这么想的。",reply:[{text:"可是不对。"},{text:"如果她们小时候已经换完一次了——"},{text:"他们现在为什么又要抓沈妍？"}]}];\n if(contactId==="ly"&&materialId==="admin-reswap-2026")return [{id:"ly-reswap-next",text:"那沈妍为什么也会有反应？",reply:[{text:"对，我也在想这个。"},{text:"你看它最后那句，‘原对契 0712-4471 出现同步异常’。"},{text:"后台应该还有沈妍这一侧的关联记录。"}]}];\n if(contactId==="ly"&&materialId==="admin-sync-shen")return [{id:"ly-sync-now",text:"所以她是被抓回来控制这个异常？",reply:[{text:"我看就是。"},{text:"第二次试验是林楠那边。"},{text:"沈妍是那次试验把二十年前那条旧联系重新扯醒以后，才被他们抓回去的。"},{text:"现在最要紧的是她在哪。"}]}];\n if(contactId==="ly"&&materialId==="admin-third-1907")return [{id:"ly-third-identity",text:"她还要求联系徐宁。",reply:[{text:"……"},{text:"这就更不像随口胡说了。"},{text:"先把这份也留好。真找到地方的话，这个人也得一起报。"}]}];'''
new=''' if(contactId==="ly"&&materialId==="admin-pair-2004")return [\n  {id:"ly-pair-link",text:"只是两个人的档案互相挂靠？",reply:[{text:"可A、B两边都写了‘易舍完成’。"},{text:"只做档案关联没必要写客源。"}]},\n  {id:"ly-pair-swap",text:"舍是身体，客是魂……所以她们互换了？",reply:[{text:"……我也是这么看的。"},{text:"那‘易舍’就是换魂。"}],next:[{id:"ly-pair-why",text:"那既然换过了，为什么现在又抓沈妍？",reply:[{text:"对。这个才是现在的问题。"},{text:"2004那份解释不了2026。得看林楠后来又发生了什么。"}]}]},\n  {id:"ly-pair-held",text:"也可能只是两个人一起被关过？",reply:[{text:"可能，但还是解释不了为什么‘客源’互相写对方。"},{text:"我会先把‘舍’和‘客’的意思对上。"}]}\n ];\n if(contactId==="ly"&&materialId==="admin-reswap-2026"){\n  if(!received("ly","admin-pair-2004"))return [];\n  const syncNext:QuickReply[]=received("ly","admin-sync-shen")?[\n   {id:"ly-sync-wrong-again",text:"所以他们也准备再给沈妍换一次？",reply:[{text:"可沈妍那份写的是‘控制旧对契另一端’，不是再舍对象。"}]},\n   {id:"ly-sync-right",text:"林楠第二次易舍，把2004年的另一端也重新影响了？",reply:[{text:"我也是这么对上的。"},{text:"沈妍不是第二次试验的目标，她是旧对契重新有反应以后被控制的。"},{text:"现在得找她被转到哪。"}]},\n   {id:"ly-sync-forum",text:"还是因为沈妍查论坛查得太深？",reply:[{text:"他们当然一直监控她。"},{text:"但这份处置理由写的是同步异常，不是论坛行为。"}]}\n  ]:[];\n  return [\n   {id:"ly-reswap-shen",text:"他们是想接着给沈妍也换一次？",reply:[{text:"但这份执行对象写的是B侧和19-07。"},{text:"沈妍不在这次执行名单里。"}]},\n   {id:"ly-reswap-test",text:"他们在测试同一个魂能不能连续换身体？",reply:[{text:"对。"},{text:"稳定22年、再次易舍、主体稳定——这几个字段放一起就是这个意思。"}],next:syncNext},\n   {id:"ly-reswap-repeat",text:"只是把2004年的仪式重新做一遍？",reply:[{text:"不太像。"},{text:"这次特意写‘长期样本’和‘第二次更换舍’，目的变了。"}]}\n  ];\n }\n if(contactId==="ly"&&materialId==="admin-sync-shen"){\n  if(!received("ly","admin-reswap-2026"))return [];\n  return [\n   {id:"ly-sync-wrong-again",text:"所以他们也准备再给沈妍换一次？",reply:[{text:"可沈妍那份写的是‘控制旧对契另一端’，不是再舍对象。"}]},\n   {id:"ly-sync-right",text:"林楠第二次易舍，把2004年的另一端也重新影响了？",reply:[{text:"我也是这么对上的。"},{text:"沈妍不是第二次试验的目标，她是旧对契重新有反应以后被控制的。"},{text:"现在得找她被转到哪。"}]},\n   {id:"ly-sync-forum",text:"还是因为沈妍查论坛查得太深？",reply:[{text:"他们当然一直监控她。"},{text:"但这份处置理由写的是同步异常，不是论坛行为。"}]}\n  ];\n }\n if(contactId==="ly"&&materialId==="admin-third-1907")return [{id:"ly-third-identity",text:"她还要求联系徐宁。",reply:[{text:"……"},{text:"那就不能只当身份混乱看了。"},{text:"真找到地点，这个人也得告诉警方。"}]}];'''
wx=rep(wx,old,new,'reasoning quicks')

# Free-text interrogation for Yu Qing + less repetitive Zhou speech.
wx=rep(wx,
'  if(/昨晚|见面|去哪|在哪/.test(t))return [{text:"昨晚是见到了。"},{text:"后来她说胃不舒服，我就先走了。"},{text:"她没跟我说后面去哪。"}];',
'  if(/几点|分开|什么时候走/.test(t))return [{text:"我九点左右先走的。"},{text:"21:03那句‘到家说一声’就是我离开以后发的。"}];\n  if(/后来|别人|谁来|还有人|介绍/.test(t))return [{text:"……后来确实有人过来了一下。"},{text:"是之前跟她聊过旧事的一个女的。"},{text:"我跟那个人也不熟，就是以前介绍她们认识。"}];\n  if(/昨晚|见面|去哪|在哪/.test(t))return [{text:"昨晚是见到了。"},{text:"她说胃不舒服，我九点左右先走。"},{text:"她没跟我说后面去哪。"}];',
'yq interrogation')
wx=wx.replace('if(/后台|管理系统|管理后台/.test(t))return [{text:"什么后台？"},{text:"先把时间、操作人和原始字段留着。"},{text:"状态词先别急着按字面信。"}];','if(/后台|管理系统|管理后台/.test(t))return [{text:"什么后台？"},{text:"你截图了吗？尤其时间和操作人。"}];',1)
wx=wx.replace('if(/已控制|转交|血样/.test(t))return [{text:"先看时间。"},{text:"能不能跟她昨晚的行程对上？"}];','if(/已控制|转交|血样/.test(t))return [{text:"转交、采血、控制是连着的吗？"},{text:"这就不像普通账号记录了。"}];',1)

# Export first-contact evidence and confrontation trigger.
old='export const focusWechatContact=(contactId:string)=>{if(contacts.some(x=>x.id===contactId))wechatSession.activeId=contactId};'
new='''export const focusWechatContact=(contactId:string)=>{if(contacts.some(x=>x.id===contactId))wechatSession.activeId=contactId};\nexport const getFirstContactTime=(contactId:string)=>wechatSession.firstContact[contactId]||null;\nexport const revealZhouConfrontation=()=>{\n const stamp=wechatSession.firstContact.zc;\n if(!stamp||wechatSession.zhouConfronted)return false;\n wechatSession.zhouEvidenceSeen=true;\n wechatSession.quick={...wechatSession.quick,zc:[{id:"zc-zheliu",text:"你是折柳？",emphasis:true,reply:[{text:"你在哪看到这个号的？"}],next:[{id:"zc-zheliu-admin",text:"后台。",reply:[{text:"……"},{text:"你现在还在沈妍家？"}],next:[{id:"zc-zheliu-answer",text:"你还没回答我。",reply:[{text:"是。"}],next:[{id:"zc-zheliu-time",text:`我${stamp}才第一次联系你。后台同一分钟就有折柳的记录。`,reply:[{text:"……"},{text:"你先从她家出来。"}],next:[{id:"zc-zheliu-why",text:"为什么？",reply:[{text:"现在别问这个。"},{text:"先出去。"}]}]}]}]}]}]};\n notifyWechat();\n return true;\n};'''
wx=rep(wx,old,new,'zhou evidence exports')

# Intro replies and explicit first-contact bubble.
anchor='''const introText=(contactId:string)=>{\n if(contactId==="yq")return "你好，我是徐宁，沈妍朋友。她今天一直联系不上，我现在在她家。你们昨晚是不是见过？她走的时候有说去哪吗？";\n if(contactId==="zc")return "你好，我是徐宁，沈妍朋友。她今天一直联系不上。我现在在她家，她电脑微信还登着。看到你们最近有聊天，方便问你两句吗？";\n if(contactId==="ly")return "你好，我是徐宁，沈妍朋友。她今天一直联系不上。我现在在她家，她电脑微信还登着。看到你们最近有聊天，方便问你两句吗？";\n return "你好，我是徐宁，沈妍朋友。她今天一直联系不上，我现在在她家。";\n};'''
replacement=anchor+'''\n\nconst introReply=(contactId:string):{parts:ReplyPart[];next:QuickReply[]}=>{\n if(contactId==="yq")return {parts:[{text:"你是徐宁？沈妍提过你。"},{text:"她今天还没回你？昨晚我们确实见过。"}],next:[{id:"yq-left-when",text:"你们昨晚几点分开的？",reply:[{text:"我九点左右先走的。"},{text:"21:03那句‘到家说一声’就是我走以后发的。"}],next:[{id:"yq-after-person",text:"她后来还见了别人吗？",reply:[{text:"……后来确实有人过来了一下。"},{text:"是之前跟她聊过旧事的一个女的。"},{text:"我跟那个人也不熟，就是以前介绍她们认识。"}]}]}]};\n if(contactId==="zc")return {parts:[{text:"徐宁？她提过你。"},{text:"她今天一直没回？电话也不通？"}],next:[]};\n if(contactId==="ly")return {parts:[{text:"徐宁？我知道你，沈妍提过。"},{text:"她怎么了？"}],next:[]};\n return {parts:[],next:[]};\n};'''
wx=rep(wx,anchor,replacement,'intro reply')

# First contact records the actual game time. Materials are locked until intro.
old=''' const sendable=useMemo(()=>materials.filter(m=>Object.prototype.hasOwnProperty.call(materialRules[m.id]||{},id)&&!sent[`${id}:${m.id}`]),[materials,id,sent]);'''
new=''' const sendable=useMemo(()=>id==="x"||!introduced[id]?[]:materials.filter(m=>Object.prototype.hasOwnProperty.call(materialRules[m.id]||{},id)&&!sent[`${id}:${m.id}`]),[materials,id,sent,introduced]);'''
wx=rep(wx,old,new,'sendable after intro')
old=''' const ensureIntro=(contactId:string):Msg[]=>{\n  if(contactId==="x"||wechatSession.introduced[contactId])return [];\n  wechatSession.introduced={...wechatSession.introduced,[contactId]:true};\n  notifyWechat();\n  return [{who:"沈妍",text:introText(contactId)}];\n };'''
new=''' const ensureIntro=(contactId:string):Msg[]=>{\n  if(contactId==="x"||wechatSession.introduced[contactId])return [];\n  const stamp=advanceGameClock(1);\n  wechatSession.introduced={...wechatSession.introduced,[contactId]:true};\n  wechatSession.firstContact={...wechatSession.firstContact,[contactId]:stamp};\n  notifyWechat();\n  return [{time:`今天 ${stamp}`,who:"沈妍",text:introText(contactId)}];\n };\n const sendIntroduction=(contactId:string)=>{\n  if(contactId==="x"||wechatSession.introduced[contactId])return;\n  const intro=ensureIntro(contactId);\n  appendFor(contactId,intro);\n  const start=introReply(contactId);\n  delayedParts(contactId,start.parts,start.next);\n };'''
wx=rep(wx,old,new,'ensure intro timing')

# sendQuick may display a short label but send a fuller message; mark confrontation once used.
old='''  appendFor(id,[{who:"沈妍",text:item.text}]);\n  delayedParts(id,item.reply,item.next||[]);'''
new='''  appendFor(id,[{who:"沈妍",text:item.sendText||item.text}]);\n  if(item.id==="zc-zheliu")wechatSession.zhouConfronted=true;\n  delayedParts(id,item.reply,item.next||[]);'''
wx=rep(wx,old,new,'send quick metadata')

# Header signature + explicit intro bubble + emphasized confrontation chip.
wx=rep(wx,
'<header style={{flex:"0 0 auto"}}><b>{contact.name}</b><small>{typing[id]?"正在输入…":contact.note}</small></header>',
'<header style={{flex:"0 0 auto"}}><b>{contact.name}</b><small>{typing[id]?"正在输入…":contact.note}</small>{contact.signature&&<small style={{display:"block",marginTop:3,color:"#929892",fontSize:10}}>个性签名：{contact.signature}</small>}</header>',
'wechat signature header')
intro_ui='''\n   {!typing[id]&&id!=="x"&&!introduced[id]&&<div style={{flex:"0 0 auto",padding:"10px 14px 0",background:"#f7f7f7"}}><button onClick={()=>sendIntroduction(id)} style={{padding:"8px 13px",border:"1px solid #b9d6c3",borderRadius:16,background:"#fff",color:"#267747",fontSize:12,fontWeight:700}}>先自我介绍</button></div>}\n'''
wx=rep(wx,'\n   {!typing[id]&&(quick[id]||[]).length>0&&<div',intro_ui+'\n   {!typing[id]&&(quick[id]||[]).length>0&&<div','intro bubble')
wx=rep(wx,
'style={{maxWidth:"100%",padding:"7px 11px",border:"1px solid #cfd8d2",borderRadius:15,background:"#fff",color:"#3c6250",fontSize:12,textAlign:"left"}}',
'style={{maxWidth:"100%",padding:item.emphasis?"9px 14px":"7px 11px",border:item.emphasis?"2px solid #9f3f36":"1px solid #cfd8d2",borderRadius:15,background:item.emphasis?"#fff8f6":"#fff",color:item.emphasis?"#8c3029":"#3c6250",fontSize:12,fontWeight:item.emphasis?800:400,textAlign:"left"}}',
'emphasis quick')

# ---- Page: visible shared clock and much clearer WeChat notifications ----
page=rep(page,
'import AdminPortalOccult from "./AdminPortalOccult";',
'import AdminPortalOccult from "./AdminPortalOccult";\nimport {advanceGameClock,getGameClock,subscribeGameClock} from "./gameClock";',
'page clock import')
page=rep(page,
' const [wxNotices,setWxNotices]=useState<(WechatNotice&{id:number})[]>([]);',
' const [wxNotices,setWxNotices]=useState<(WechatNotice&{id:number})[]>([]);\n const [clock,setClock]=useState(()=>getGameClock());\n useEffect(()=>subscribeGameClock(setClock),[]);',
'page clock state')
page=page.replace('  if(app==="wechat")return;\n','',1)
page=page.replace('window.setTimeout(()=>setWxNotices(prev=>prev.filter(x=>x.id!==item.id)),6500);','window.setTimeout(()=>setWxNotices(prev=>prev.filter(x=>x.id!==item.id)),12000);',1)
page=rep(page,
' const open=(x:App)=>{setApp(x);setMax(x==="browser"||x==="verse");if(x==="wechat")setWxRead(true)};',
' const open=(x:App)=>{advanceGameClock(1);setApp(x);setMax(x==="browser"||x==="verse");if(x==="wechat")setWxRead(true)};',
'open advances clock')
page=page.replace('<span>10月17日 周六 19:06</span>','<span>10月17日 周六 {clock}</span>',1)
page=page.replace('const go=(next:Route)=>{setStack([...stack,route]);','const go=(next:Route)=>{advanceGameClock(1);setStack([...stack,route]);',1)
page=page.replace('width:310,display:"grid"','width:350,display:"grid"',1)
page=page.replace('padding:"11px 12px",border:"1px solid #d7ddd9"','padding:"13px 14px",border:"2px solid #42a967"',1)
page=page.replace('boxShadow:"0 10px 30px #0003"','boxShadow:"0 14px 38px #0005"',1)
page=page.replace('<b style={{display:"block",fontSize:12}}>微信 · {n.name}</b>','<b style={{display:"block",fontSize:12}}><span style={{marginRight:6,color:"#2a9f55"}}>新消息</span>微信 · {n.name}</b>',1)

# ---- Admin: remove duplicate branding, search-led investigation, dynamic Zhou evidence ----
admin=rep(admin,
'import {SharedMaterial,triggerAdminWechatBeat} from "./InteractiveWechat";',
'import {SharedMaterial,getFirstContactTime,revealZhouConfrontation,triggerAdminWechatBeat} from "./InteractiveWechat";',
'admin zhou imports')
admin=admin.replace('if(/林楠|LN-2004-0718/.test(t))return "lin";','if(/林楠/.test(t))return "lin";',1)
old='const doSearch=(e?:FormEvent)=>{e?.preventDefault();setSearched(true);setDetail(null);if(/候鸟第七年|沈妍|0712-4471/.test(q.trim()))fireShenBeat()};'
new='''const doSearch=(e?:FormEvent)=>{e?.preventDefault();const t=q.trim();setSearched(true);if(/^LN-2004-0718$/i.test(t)){setDetail("pair2004");return}if(/^RS-2026-1012$/i.test(t)){setDetail("reswap");return}if(/^AN-0712-1012$/i.test(t)){setDetail("sync");return}if(/^19-07$/i.test(t)){setDetail("third");return}setDetail(null);if(/候鸟第七年|沈妍|0712-4471/.test(t))fireShenBeat()};'''
admin=rep(admin,old,new,'admin special search')
admin=rep(admin,
'<header style={s.adminHead}><div><i>烛</i><span><b>烛阴旧闻</b><small>旧档管理</small></span></div><span style={s.adminAccount}>旧档员-03</span></header>',
'<header style={s.adminHead}><div><span><b>旧档管理</b><small>内部资料库</small></span></div><span style={s.adminAccount}>旧档员-03</span></header>',
'admin header')
old='''    {tab==="users"&&(detail?<AdminDetailPage detail={detail} openDetail={openDetail} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>:<><h2>用户查询</h2><form onSubmit={doSearch} style={s.adminSearch}><Search size={16}/><input value={q} onChange={e=>{setQ(e.target.value);setSearched(false);setDetail(null)}} placeholder="用户名 / UID / 关联姓名"/><button>查询</button></form>{searched&&!result&&<p style={s.adminEmpty}>没有匹配用户。</p>}{result==="shen"&&<ShenRecord openDetail={openDetail} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>} {result==="liang"&&<LiangRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>} {result==="lin"&&<LinRecord openDetail={openDetail}/>} {result==="third"&&<ThirdRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>}</>)}'''
new='''    {tab==="users"&&<><h2>用户查询</h2><form onSubmit={doSearch} style={s.adminSearch}><Search size={16}/><input value={q} onChange={e=>{setQ(e.target.value);setSearched(false)}} placeholder="用户名 / UID / 关联姓名 / 记录编号"/><button>查询</button></form>{detail?<AdminDetailPage detail={detail} openDetail={openDetail} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>:<>{searched&&!result&&<p style={s.adminEmpty}>没有匹配用户。</p>}{result==="shen"&&<ShenRecord openDetail={openDetail} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>} {result==="liang"&&<LiangRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>} {result==="lin"&&<LinRecord openDetail={openDetail}/>} {result==="third"&&<ThirdRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>}</>}</>}'''
admin=rep(admin,old,new,'persistent admin search')
# Remove the guided next buttons and leave searchable identifiers in the records.
admin=admin.replace('<DetailLink onClick={()=>openDetail("pair2004")}>查看旧案 LN-2004-0718</DetailLink>','',1)
admin=admin.replace('<DetailLink onClick={()=>openDetail("lin")}>查看关联对象：林楠</DetailLink>','<Record date="关联对象" title="林楠" meta="B侧" text="实名关联已确认。"/>',1)
admin=admin.replace('<Record date="2026-10-12" title="执行记录" meta="记录 1 条" text="状态：完成。"/><DetailLink onClick={()=>openDetail("reswap")}>查看 2026-10-12 执行记录</DetailLink>','<Record date="2026-10-12" title="执行记录" meta="RS-2026-1012" text="状态：完成。"/>',1)
admin=admin.replace('<Record date="结果" title="执行完成" meta="2026-10-12 22:13" text="两侧生命体征稳定；原对契 0712-4471 出现同步异常。"/></section><DetailLink onClick={()=>openDetail("third")}>查看候舍对象 19-07</DetailLink><DetailLink onClick={()=>openDetail("sync")}>查看关联异常：0712-4471</DetailLink>',
'<Record date="结果" title="执行完成" meta="2026-10-12 22:13" text="两侧生命体征稳定；原对契出现同步异常。"/><Record date="关联异常" title="AN-0712-1012" meta="0712-4471" text="同步值异常升高。"/><Record date="候舍对象" title="19-07" meta="执行后隔离" text="存在身份陈述异常。"/></section>',1)
# Dynamic timestamp row appears only after the player has actually introduced themselves to Zhou.
ops_pattern=r'function Operations\(\)\{return <><h2>操作记录</h2><div style=\{s\.adminPanel\}><Record date="2026-10-17 18:51" title="访问异常复核：0712-4471" meta="来源：折柳" text="确认访问者为徐宁。暂不处理。"/>'
ops_repl='''function Operations(){const zhouTime=getFirstContactTime("zc");useEffect(()=>{if(zhouTime)revealZhouConfrontation()},[zhouTime]);return <><h2>操作记录</h2><div style={s.adminPanel}>{zhouTime&&<Record date={`2026-10-17 ${zhouTime}`} title="访问者身份补录：0712-4471" meta="来源：折柳" text="访问者：徐宁。保留观察。"/>}'''
admin,n=re.subn(ops_pattern,ops_repl,admin,count=1)
if n!=1: raise RuntimeError('missing marker: dynamic operations')

# ---- Forum: keep Zheliu's post human, not clue-shaped ----
data=rep(data,
'reply("折柳","次日 00:12","看完了。你这次记得比上次细很多。今天别再翻了，明天再看，越熬越容易把自己绕进去。"),',
'reply("折柳","次日 00:12","看完了。红盒子先别管，明早醒了还记得再说。你这几天是不是又没怎么睡？"),',
'human zheliu reply')

wx_path.write_text(wx)
page_path.write_text(page)
admin_path.write_text(admin)
data_path.write_text(data)
print('Applied v9.2.1 interaction pass')
