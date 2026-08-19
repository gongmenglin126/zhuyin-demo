from pathlib import Path

# ---------- Admin ----------
p=Path('app/AdminPortalOccult.tsx')
s=p.read_text()
s=s.replace('import {ArrowLeft,ChevronRight,LockKeyhole,Search,ShieldCheck} from "lucide-react";', 'import {ArrowLeft,ChevronRight,FilePlus2,LockKeyhole,Search,ShieldCheck} from "lucide-react";')
s=s.replace('import {SharedMaterial,getFirstContactTime,triggerAdminWechatBeat} from "./InteractiveWechat";', 'import {SharedMaterial,getFirstContactTime,triggerAdminWechatBeat,triggerZhouLocationThreat} from "./InteractiveWechat";')
s=s.replace('type AdminTab="watch"|"users"|"ops"|"recycle";', 'type AdminTab="watch"|"users"|"candidates"|"ops"|"recycle";')
s=s.replace('type AdminDetail="pair2004"|"lin"|"reswap"|"third"|"sync"|"guestA"|"guestB"|"guestG"|null;', 'type AdminDetail="pair2004"|"lin"|"reswap"|"third"|"sync"|"guestA"|"guestB"|"guestG"|"batch"|"location"|null;')

old='''const adminThirdMaterial:SharedMaterial={id:"admin-third-1907",title:"候舍对象 19-07 · 当前记录",kind:"后台记录",url:"https://www.zhuyinwen.cn/admin/subjects/19-07"};'''
new=old+'''\nconst adminLocationMaterial:SharedMaterial={id:"admin-location-hln04",title:"HL-N-04 · 河临北郊第三仓储区4号库",kind:"位置记录",url:"https://www.zhuyinwen.cn/admin/sites/HL-N-04"};'''
assert old in s
s=s.replace(old,new,1)

start=s.index('function AddMaterialButton(')
end=s.index('\n\nlet adminCaseLevel=',start)
s=s[:start]+'''function AddMaterialButton({material,onCopyMaterial,hasMaterial}:{material:SharedMaterial;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){
 if(!onCopyMaterial)return null;
 const added=!!hasMaterial?.(material.id);
 return <button disabled={added} onClick={()=>onCopyMaterial(material)} style={{minWidth:220,height:46,display:"inline-flex",alignItems:"center",justifyContent:"center",gap:9,margin:"4px 0 16px",padding:"0 16px",border:added?"1px solid #b9c3bd":"2px solid #4b7d67",borderRadius:8,background:added?"#e9eeeb":"#fff",color:added?"#6f7c75":"#2e654d",fontSize:13,fontWeight:800,cursor:added?"default":"pointer",boxShadow:added?"none":"0 5px 14px #284b3b18"}}><FilePlus2 size={20}/>{added?"已加入调查材料":"加入调查材料"}</button>
}'''+s[end:]

# Search final batch and location codes.
old='''if(/^1907$/i.test(t)){setDetail("third");raise(5);return}if(t==="α"){setDetail("guestA");raise(5);return}'''
new='''if(/^1907$/i.test(t)){setDetail("third");raise(5);return}if(/^HN101602$/i.test(t)){setDetail("batch");raise(6);return}if(/^HLN04$/i.test(t)){setDetail("location");raise(7);return}if(t==="α"){setDetail("guestA");raise(5);return}'''
assert old in s
s=s.replace(old,new,1)

# Sidebar candidate library.
old='''<button className={tab==="users"?"active":""} onClick={()=>setTab("users")}>用户查询</button><button className={tab==="ops"?"active":""}'''
new='''<button className={tab==="users"?"active":""} onClick={()=>setTab("users")}>用户查询</button><button className={tab==="candidates"?"active":""} onClick={()=>{setTab("candidates");setDetail(null)}}>候舍库</button><button className={tab==="ops"?"active":""}'''
assert old in s
s=s.replace(old,new,1)
old='''{tab==="ops"&&<Operations/>}'''
new='''{tab==="candidates"&&<CandidateLibrary/>}\n    {tab==="ops"&&<Operations/>}'''
assert old in s
s=s.replace(old,new,1)

# Admin detail routing.
old=''' if(detail==="guestG")return <GuestRecord id="γ"/>;
 return <SyncRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>;'''
new=''' if(detail==="guestG")return <GuestRecord id="γ"/>;
 if(detail==="batch")return <BatchRecord/>;
 if(detail==="location")return <LocationRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>;
 return <SyncRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>;'''
assert old in s
s=s.replace(old,new,1)

# Insert candidate library before watchRows.
marker='''const watchRows=['''
insert='''function CandidateLibrary(){
 const rows=[
  ["24-11","女 / 26","申请 3 次","选我。现在就可以。我不要这个身体了。别再让我等。"],
  ["21-16","男 / 42","申请 5 次","我等了六年。下一次必须是我。换进去的是谁都行。执行以后不要把我退回来。"],
  ["19-03","女 / 28","申请 2 次","不用通知任何人，也不用保留我现在的身份。下一批有空位就把我排进去。"],
  ["22-08","男 / 35","申请 4 次","如果这具舍不合适就废掉。别取消我的资格。我必须完成一次易舍。"],
  ["23-14","女 / 31","申请 3 次","把我的姓名删掉。我不想再用它。执行后不要告诉我原来的住址，也不要让我回去。"],
  ["18-02","男 / 39","申请 6 次","我准备好了。谁来都可以。把这具舍交出去，把我原来的资料清掉。"],
 ];
 return <><div style={s.sectionTitle}>候舍库</div><p style={{margin:"0 0 14px",color:"#707872",fontSize:12}}>姓名字段已舍弃。候舍编号为唯一有效身份。</p><div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:8,marginBottom:16}}>{[["在库","164"],["匹配可用","37"],["待执行","12"],["再舍申请","8"]].map(([k,v])=><div key={k} style={{padding:"11px 12px",border:"1px solid #cbd1cd",borderRadius:7,background:"#fff"}}><small style={{display:"block",color:"#7b837e"}}>{k}</small><b style={{display:"block",marginTop:4,fontSize:22}}>{v}</b></div>)}</div>
 <section style={s.adminPanel}><h4>筛选规范沿革</h4><Record date="2004版" title="低龄强制样本优先" meta="适用：7—11岁" text="名称识别已形成；长期社会身份尚未固化；返家后的记忆、性格异常可归入失踪应激。"/><Record date="2012修订" title="停止低龄优先" meta="成年自愿候舍纳入正式序列" text="长期样本证明年龄不是必要条件。改以对契匹配、去名训练与成年自愿对象为主。"/><Record date="现行" title="候舍来源充足，无需强制补充" meta="旧契样本另行处置" text="常规候舍优先从奉舍申请中匹配。旧契样本不可替代；出现同步、返契异常时优先回收。"/></section>
 <section style={s.adminPanel}><h4>近期奉舍申请</h4>{rows.map(([id,meta,count,text])=><Record key={id} date={id} title={meta} meta={count} text={`申请原文：${text}`}/>)}</section>
 </>;
}

'''
assert marker in s
s=s.replace(marker,insert+marker,1)

# Batch and location pages inserted before SyncRecord.
marker='''function SyncRecord({onCopyMaterial,hasMaterial}'''
insert='''function BatchRecord(){return <article style={s.userRecord}><h2 style={{marginTop:0}}>HN-1016-02</h2><p style={s.subtle}>返契异常控制批次</p><section style={s.adminPanel}><h4>执行记录</h4><Record date="对象" title="0712-4471 · 沈妍" meta="旧对契异常端" text="10月16日完成线下转交、采样与控制。"/><Record date="处置" title="转入内部场地" meta="场地代码：HL-N-04" text="人员已于21:18转入。外部联络关闭。"/><Record date="状态" title="在场" meta="未转移" text="最新场地回报：10月17日18:55。"/></section></article>}
function LocationRecord({onCopyMaterial,hasMaterial}:{onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){
 useEffect(()=>{triggerZhouLocationThreat()},[]);
 return <article style={s.userRecord}><h2 style={{marginTop:0}}>HL-N-04</h2><p style={s.subtle}>内部场地索引</p><AddMaterialButton material={adminLocationMaterial} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/><section style={s.adminPanel}><h4>场地信息</h4><Record date="地址" title="河临北郊第三仓储区 · 4号库" meta="旧冷链仓改造" text="西侧员工通道；内部隔离间 3；当前批次 HN-1016-02。"/><Record date="当前" title="在用" meta="10月17日 18:55" text="0712-4471仍在场。未登记转移。"/></section></article>
}

'''
assert marker in s
s=s.replace(marker,insert+marker,1)

p.write_text(s)

# ---------- WeChat ----------
p=Path('app/InteractiveWechat.tsx')
s=p.read_text()
s=s.replace('import {advanceGameClock} from "./gameClock";', 'import {advanceGameClock} from "./gameClock";\nimport {beginEnding} from "./endingState";')
s=s.replace('type QuickReply={id:string;text:string;sendText?:string;emphasis?:boolean;freeText?:boolean;reply:ReplyPart[];next?:QuickReply[]};', 'type QuickReply={id:string;text:string;sendText?:string;emphasis?:boolean;freeText?:boolean;ending?:"report"|"double";reply:ReplyPart[];next?:QuickReply[]};')
s=s.replace('''  zhouConfronted:false,
  activeId:"yq",''','''  zhouConfronted:false,
  locationKnown:false,
  locationThreatSent:false,
  activeId:"yq",''')
# Location material rule.
old=''' "admin-third-1907":{ly:[{text:"她连自己到底叫沈妍还是林楠都说不稳。"},{text:"但一听到徐宁这个名字就哭……这比直接认出你更吓人。"}],zc:[{text:"姓名陈述来回变？"},{text:"那就不是一句口误能解释的。"}]},'''
new=old+'''\n "admin-location-hln04":{ly:[{text:"地址有了。"},{text:"别自己去。报警，把后台记录和这个地址一起交出去。"}]},'''
assert old in s
s=s.replace(old,new,1)

# Threat helper after received.
marker='''const materialReply=(contactId:string,materialId:string):ReplyPart[]|null=>{'''
helper='''export const triggerZhouLocationThreat=()=>{
 wechatSession.locationKnown=true;
 if(wechatSession.locationThreatSent||!wechatSession.zhouIdentityKnown||!wechatSession.zhouConfronted)return false;
 wechatSession.locationThreatSent=true;
 const items:Msg[]=[{who:"对方",text:"别报警。"},{who:"对方",text:"HL-N-04，对吧。"},{who:"对方",text:"沈妍还在我们手里。"}];
 wechatSession.extra={...wechatSession.extra,zc:[...(wechatSession.extra.zc||[]),...items]};
 const final:QuickReply[]=[
  {id:"zc-final-report",text:"我会报警。",emphasis:true,ending:"report",reply:[{text:"那就赌他们比我们快。"}]},
  {id:"zc-final-go",text:"我一个人去。",ending:"double",reply:[{text:"手机留下。"},{text:"到门口以后再联系我。"}]},
 ];
 wechatSession.quick={...wechatSession.quick,zc:[{id:"zc-threat",text:"你在威胁我？",emphasis:true,reply:[{text:"对。"},{text:"我就是在威胁你。"},{text:"一个人来。别报警。"}],next:final}]};
 emitWechatNotice("zc","沈妍还在我们手里。");
 notifyWechat();
 return true;
};

'''
assert marker in s
s=s.replace(marker,helper+marker,1)

# Location and true-ending quick replies.
old=''' if(contactId==="ly"&&materialId==="admin-third-1907")return [{id:"ly-third-identity",text:"她听到徐宁这个名字为什么会哭？",reply:[{text:"……这才吓人。"},{text:"她连名字都说不稳，但情绪反应还在。"},{text:"真找到地点，这个人也得告诉警方。"}]}];'''
new=''' if(contactId==="ly"&&materialId==="admin-third-1907"){
  const base:QuickReply={id:"ly-third-identity",text:"她听到徐宁这个名字为什么会哭？",reply:[{text:"……这才吓人。"},{text:"她连名字都说不稳，但情绪反应还在。"},{text:"真找到地点，这个人也得告诉警方。"}]};
  if(received("ly","admin-location-hln04"))base.next=[{id:"ly-report-both",text:"地址也有了。把19-07一起报给警方。",emphasis:true,ending:"report",reply:[{text:"对。两个人都报。别自己过去。"}]}];
  return [base];
 }
 if(contactId==="ly"&&materialId==="admin-location-hln04"){
  if(received("ly","admin-third-1907"))return [{id:"ly-report-both-now",text:"报警，把沈妍和19-07的记录一起交出去。",emphasis:true,ending:"report",reply:[{text:"对。两个人都报。你别自己去。"}]}];
  return [{id:"ly-report-shen",text:"报警，先把沈妍的位置交出去。",emphasis:true,ending:"report",reply:[{text:"好。截图别漏，地址和批次都给他们。"}]},{id:"ly-check-third",text:"我再确认一下19-07。",reply:[{text:"行，但快点。地址已经有了。"}]}];
 }'''
assert old in s
s=s.replace(old,new,1)

# When Zhou identity confrontation starts, allow pending location threat to fire.
old='''  if(item.id==="zc-zheliu")wechatSession.zhouConfronted=true;
  delayedParts(id,item.reply,item.next||[]);'''
new='''  if(item.id==="zc-zheliu"){wechatSession.zhouConfronted=true;if(wechatSession.locationKnown)window.setTimeout(()=>triggerZhouLocationThreat(),100)}
  delayedParts(id,item.reply,item.next||[]);
  if(item.ending){const kind=item.ending==="double"?"double":received("ly","admin-third-1907")?"true":"home";window.setTimeout(()=>beginEnding(kind),6500)}'''
assert old in s
s=s.replace(old,new,1)

# Make WeChat material control visually obvious.
old='''<form onSubmit={sendText} style={{display:"grid",gridTemplateColumns:"1fr 44px 48px",gap:8,alignItems:"center"}}>'''
new='''<form onSubmit={sendText} style={{display:"grid",gridTemplateColumns:"1fr 64px 48px",gap:8,alignItems:"center"}}>'''
assert old in s
s=s.replace(old,new,1)
old='''<button type="button" onClick={()=>canPickMaterial&&setPicker(v=>!v)} disabled={!canPickMaterial} title="文件" aria-label="文件" style={{position:"relative",height:44,width:44,border:"1px solid #d0d0d0",borderRadius:6,background:"#fff",display:"grid",placeItems:"center",color:"#555",opacity:canPickMaterial?1:.35}}><Plus size={19}/>{sendable.length>0&&<small'''
new='''<button type="button" onClick={()=>canPickMaterial&&setPicker(v=>!v)} disabled={!canPickMaterial} title="发送资料" aria-label="发送资料" style={{position:"relative",height:48,width:64,border:canPickMaterial?"2px solid #4a8a64":"1px solid #d0d0d0",borderRadius:7,background:"#fff",display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",gap:1,color:canPickMaterial?"#2d7550":"#777",opacity:canPickMaterial?1:.35,fontWeight:800}}><Plus size={21}/><span style={{fontSize:10,lineHeight:1}}>资料</span>{sendable.length>0&&<small'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

# ---------- Page ----------
p=Path('app/page.tsx')
s=p.read_text()
s=s.replace('import {advanceGameClock,getGameClock,subscribeGameClock} from "./gameClock";', 'import {advanceGameClock,getGameClock,subscribeGameClock} from "./gameClock";\nimport GameEnding from "./GameEnding";\nimport {getEnding,subscribeEnding} from "./endingState";')
old=''' const [clock,setClock]=useState(()=>getGameClock());
 useEffect(()=>subscribeGameClock(setClock),[]);'''
new=''' const [clock,setClock]=useState(()=>getGameClock());
 const [ending,setEnding]=useState(()=>getEnding());
 useEffect(()=>subscribeGameClock(setClock),[]);
 useEffect(()=>subscribeEnding(setEnding),[]);'''
assert old in s
s=s.replace(old,new,1)
old=''' if(stage==="title")return <main className="title">'''
new=''' if(ending)return <GameEnding kind={ending}/>;
 if(stage==="title")return <main className="title">'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)
print('Applied v9.2.4 candidates, material visibility, final location and endings')
