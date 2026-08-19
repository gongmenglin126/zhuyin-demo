from pathlib import Path
import re

# ---------- Admin: red box interaction + case clarity ----------
p=Path('app/AdminPortalOccult.tsx')
s=p.read_text()
MARK='// v9.2.3 admin clarity + shake box'
if MARK not in s:
    s=s.replace('"use client";\n','"use client";\n'+MARK+'\n',1)

s=s.replace('import {CSSProperties,FormEvent,ReactNode,useEffect,useMemo,useState} from "react";',
'''import {CSSProperties,FormEvent,PointerEvent as ReactPointerEvent,ReactNode,useEffect,useMemo,useRef,useState} from "react";''')
s=s.replace('import {SharedMaterial,getFirstContactTime,revealZhouConfrontation,triggerAdminWechatBeat} from "./InteractiveWechat";',
'''import {SharedMaterial,getFirstContactTime,triggerAdminWechatBeat} from "./InteractiveWechat";''')

# Replace the old stage-2 item state/logic. Box is no longer an assignable item.
old=''' type Item="plum"|"marble"|"milk"|"clip"|"box";'''
new=''' type Item="plum"|"marble"|"milk"|"clip";'''
assert old in s
s=s.replace(old,new,1)

old=''' const [dragItem,setDragItem]=useState<Item|null>(null);\n const [items,setItems]=useState<Partial<Record<Item,Child|"center">>>({});\n const [moods,setMoods]=useState<Record<Child,"neutral"|"frown"|"smile">>({lin:"neutral",shen:"neutral"});'''
new=''' const [dragItem,setDragItem]=useState<Item|null>(null);\n const [items,setItems]=useState<Partial<Record<Item,Child>>>({});\n const [boxOpened,setBoxOpened]=useState(false);\n const [boxNote,setBoxNote]=useState("盒盖卡住了。");\n const shakeRef=useRef({active:false,lastX:0,lastY:0,phase:"x" as "x"|"y",lastDir:0,h:0,v:0});\n const [moods,setMoods]=useState<Record<Child,"neutral"|"frown"|"smile">>({lin:"neutral",shen:"neutral"});'''
assert old in s
s=s.replace(old,new,1)

old=''' const itemAnswer:Record<Exclude<Item,"box">,Child>={plum:"lin",marble:"lin",milk:"shen",clip:"shen"};\n const ordinaryItems:(Exclude<Item,"box">)[]=["plum","marble","milk","clip"];\n const allOrdinaryPlaced=(next=items)=>ordinaryItems.every(id=>!!next[id]);\n const completeTable=(nextItems:Partial<Record<Item,Child|"center">>)=>{if(allOrdinaryPlaced(nextItems)&&nextItems.box==="center")window.setTimeout(()=>setStage(3),1100)};'''
new=''' const itemAnswer:Record<Item,Child>={plum:"lin",marble:"lin",milk:"shen",clip:"shen"};\n const ordinaryItems:Item[]=["plum","marble","milk","clip"];\n const allOrdinaryPlaced=(next=items)=>ordinaryItems.every(id=>!!next[id]);\n const completeTable=(nextItems=items,opened=boxOpened)=>{if(allOrdinaryPlaced(nextItems)&&opened)window.setTimeout(()=>setStage(3),900)};'''
assert old in s
s=s.replace(old,new,1)

# Replace giveItem and add separate shake gestures.
start=s.index(' const frown=(child:Child)=>')
end=s.index(' const progress=',start)
oldblock=s[start:end]
newblock=''' const frown=(child:Child)=>{setMoods(m=>({...m,[child]:"frown"}));window.setTimeout(()=>setMoods(m=>({...m,[child]:"neutral"})),680)};\n const giveItem=(target:Child)=>{\n  if(!dragItem)return;const id=dragItem;\n  if(itemAnswer[id]===target){const next={...items,[id]:target};setItems(next);setDragItem(null);completeTable(next,boxOpened);return;}\n  setDragItem(null);frown(target);\n };\n const beginBoxShake=(e:ReactPointerEvent<HTMLDivElement>)=>{\n  if(boxOpened)return;\n  e.currentTarget.setPointerCapture(e.pointerId);\n  const r=shakeRef.current;r.active=true;r.lastX=e.clientX;r.lastY=e.clientY;r.lastDir=0;\n  setBoxNote("盖子抬起一点，又卡住了。");\n };\n const moveBoxShake=(e:ReactPointerEvent<HTMLDivElement>)=>{\n  const r=shakeRef.current;if(!r.active||boxOpened)return;\n  const dx=e.clientX-r.lastX,dy=e.clientY-r.lastY;\n  if(r.phase==="x"&&Math.abs(dx)>11&&Math.abs(dx)>Math.abs(dy)*1.3){\n   const dir=dx>0?1:-1;if(r.lastDir&&dir!==r.lastDir)r.h+=1;r.lastDir=dir;r.lastX=e.clientX;r.lastY=e.clientY;\n   if(r.h>=3){r.phase="y";r.lastDir=0;setBoxNote("盒子里面轻轻响了一声。");}\n  }else if(r.phase==="y"&&Math.abs(dy)>10&&Math.abs(dy)>Math.abs(dx)*1.15){\n   const dir=dy>0?1:-1;if(r.lastDir&&dir!==r.lastDir)r.v+=1;r.lastDir=dir;r.lastX=e.clientX;r.lastY=e.clientY;\n   if(r.v>=2){r.active=false;setBoxOpened(true);setBoxNote("咔。盒盖松开了。");completeTable(items,true);}\n  }\n };\n const endBoxShake=()=>{const r=shakeRef.current;if(!boxOpened&&r.active)setBoxNote(r.phase==="y"?"里面像是松了一点，但盖子还卡着。":"盒盖还是卡着。");r.active=false};\n'''
s=s[:start]+newblock+s[end:]

# Stage 2: only four items are draggable; the red box is permanently centered and shakeable.
old=re.search(r'  \{stage===2&&<div style=\{v\.tableScene\}>.*?</div>\}\n  \{stage===3&&',s,re.S)
assert old
new='''  {stage===2&&<div style={v.tableScene}><div style={v.tableSeats}><TableSeat place="4栋东侧" mood={moods.lin} side="left" onDrop={()=>giveItem("lin")} items={ordinaryItems.filter(id=>items[id]==="lin")}/><div style={v.centerTable}><div style={v.tableTop}>{ordinaryItems.filter(id=>!items[id]).map(id=><ObjectToken key={id} id={id} draggable onDragStart={()=>setDragItem(id)}/>)}<div style={v.shakeBoxWrap}><div onPointerDown={beginBoxShake} onPointerMove={moveBoxShake} onPointerUp={endBoxShake} onPointerCancel={endBoxShake} style={{...v.object,...v.shakeObject,cursor:boxOpened?"default":"grab",touchAction:"none"}}><i style={{...v.objectIcon,position:"relative",...v.box}}>{boxOpened&&<span style={{position:"absolute",left:1,right:1,top:-7,height:7,border:"1px solid #704236",borderBottom:0,background:"#7d2b23",transform:"rotate(-8deg)",transformOrigin:"left bottom",boxShadow:"0 -2px 8px #0008"}}/>}</i><small>红铁皮盒</small></div><em style={v.boxNote}>{boxNote}</em></div></div></div><TableSeat place="青梧旧楼" mood={moods.shen} side="right" onDrop={()=>giveItem("shen")} items={ordinaryItems.filter(id=>items[id]==="shen")}/></div></div>}\n  {stage===3&&'''
s=s[:old.start()]+new+s[old.end():]

# Object token no longer needs box-open behavior.
s=s.replace('function ObjectToken({id,draggable,onDragStart,opened}:{id:string;draggable?:boolean;onDragStart?:()=>void;opened?:boolean}){const labels:Record<string,string>={plum:"话梅糖",marble:"蓝玻璃弹珠",milk:"奶糖",clip:"红色发卡",box:"红铁皮盒"};return <div draggable={draggable} onDragStart={e=>{e.dataTransfer.effectAllowed="move";onDragStart?.()}} style={{...v.object,cursor:draggable?"grab":"default"}}><i style={{...v.objectIcon,position:"relative",...(id==="plum"?v.plum:id==="marble"?v.marble:id==="milk"?v.milk:id==="clip"?v.clip:v.box)}}>{id==="box"&&opened&&<span style={{position:"absolute",left:1,right:1,top:-7,height:7,border:"1px solid #704236",borderBottom:0,background:"#7d2b23",transform:"rotate(-7deg)",transformOrigin:"left bottom",boxShadow:"0 -2px 8px #0008"}}/>}</i><small>{labels[id]}</small></div>}',
'function ObjectToken({id,draggable,onDragStart}:{id:string;draggable?:boolean;onDragStart?:()=>void}){const labels:Record<string,string>={plum:"话梅糖",marble:"蓝玻璃弹珠",milk:"奶糖",clip:"红色发卡"};return <div draggable={draggable} onDragStart={e=>{e.dataTransfer.effectAllowed="move";onDragStart?.()}} style={{...v.object,cursor:draggable?"grab":"default"}}><i style={{...v.objectIcon,position:"relative",...(id==="plum"?v.plum:id==="marble"?v.marble:id==="milk"?v.milk:v.clip)}}/><small>{labels[id]}</small></div>}',1)

# Case trail / object legend helpers.
anchor='''function AddMaterialButton({material,onCopyMaterial,hasMaterial}:{material:SharedMaterial;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){if(!onCopyMaterial)return null;const added=!!hasMaterial?.(material.id);return <button disabled={added} onClick={()=>onCopyMaterial(material)} style={{margin:"0 0 12px",padding:"7px 10px",border:"1px solid #b9c3bd",borderRadius:6,background:added?"#eef1ef":"#fff",color:"#40564c",fontSize:12,cursor:added?"default":"pointer",opacity:added?.6:1}}>{added?"已添加到材料":"添加到材料"}</button>}\n'''
assert anchor in s
helpers='''\nlet adminCaseLevel=0;\nfunction CaseTrail({level,openShen,openDetail}:{level:number;openShen:()=>void;openDetail:(x:Exclude<AdminDetail,null>)=>void}){\n const items=[\n  {label:"沈妍",sub:"徐宁认识的朋友 · A侧登记身体",go:openShen},\n  {label:"2004旧案",sub:"LN-2004-0718 · A/B双向易舍",go:()=>openDetail("pair2004")},\n  {label:"林楠",sub:"B侧登记身体",go:()=>openDetail("lin")},\n  {label:"2026再舍",sub:"RS-2026-1012 · B侧 / 19-07",go:()=>openDetail("reswap")},\n  {label:"同步异常",sub:"AN-0712-1012 · 沈妍A侧",go:()=>openDetail("sync")},\n  {label:"19-07",sub:"第三名成年候舍对象",go:()=>openDetail("third")},\n ];\n return <section style={s.caseTrail}><b style={s.caseTitle}>关联对象</b><div style={s.caseGrid}>{items.filter((_,i)=>i<=level).map((x,i)=><button key={x.label} onClick={x.go} style={s.caseButton}><strong>{x.label}</strong><small>{x.sub}</small></button>)}</div>{level>=2&&<div style={s.identityLegend}><b>对象口径</b><span><strong>沈妍</strong>＝A侧登记身体／徐宁认识的朋友</span><span><strong>林楠</strong>＝B侧登记身体</span><span><strong>19-07</strong>＝第三名成年候舍对象</span><small>后台页面标题按“舍”的登记身份命名；“客源”单独记录，不等于页面标题里的姓名。</small></div>}</section>\n}\n'''
s=s.replace(anchor,anchor+helpers,1)

# Replace AdminDesk with progressive in-place case navigation; remove duplicate header/subtitle.
start=s.index('function AdminDesk(')
end=s.index('\n\nconst watchRows=',start)
new_admin='''function AdminDesk({onWechatIncoming,onCopyMaterial,hasMaterial}:{onWechatIncoming?:()=>void;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){\n const [tab,setTab]=useState<AdminTab>(()=>adminDeskSession.tab);\n const [q,setQ]=useState(()=>adminDeskSession.q);\n const [searched,setSearched]=useState(()=>adminDeskSession.searched);\n const [detail,setDetail]=useState<AdminDetail>(()=>adminDeskSession.detail);\n const [caseLevel,setCaseLevel]=useState(()=>adminCaseLevel);\n const result=useMemo<ResultKind>(()=>{if(!searched)return null;const t=q.trim();if(/候鸟第七年|沈妍|0712-4471/.test(t))return "shen";if(/迟迟|梁茵|0419-2286/.test(t))return "liang";if(/林楠/.test(t))return "lin";if(/19-07|候舍/.test(t))return "third";return null},[searched,q]);\n useEffect(()=>{adminDeskSession.tab=tab;adminDeskSession.q=q;adminDeskSession.searched=searched;adminDeskSession.detail=detail;adminCaseLevel=caseLevel},[tab,q,searched,detail,caseLevel]);\n useEffect(()=>{const timer=window.setTimeout(()=>{if(triggerAdminWechatBeat("shen-record"))onWechatIncoming?.()},900);return ()=>window.clearTimeout(timer)},[]);\n const fireShenBeat=()=>{if(triggerAdminWechatBeat("shen-record"))onWechatIncoming?.()};\n const raise=(n:number)=>setCaseLevel(v=>Math.max(v,n));\n const doSearch=(e?:FormEvent)=>{e?.preventDefault();const t=q.trim();setSearched(true);if(/^LN-2004-0718$/i.test(t)){setDetail("pair2004");raise(2);return}if(/^RS-2026-1012$/i.test(t)){setDetail("reswap");raise(5);return}if(/^AN-0712-1012$/i.test(t)){setDetail("sync");raise(5);return}if(/^19-07$/i.test(t)){setDetail("third");raise(5);return}setDetail(null);if(/候鸟第七年|沈妍|0712-4471/.test(t)){raise(1);fireShenBeat()}if(/林楠/.test(t))raise(3)};\n const openKnown=(name:string)=>{setQ(name);setSearched(true);setDetail(null);setTab("users");if(/候鸟第七年|沈妍/.test(name)){raise(1);fireShenBeat()}};\n const openShen=()=>{setQ("沈妍");setSearched(true);setDetail(null);setTab("users");raise(1)};\n const openDetail=(next:Exclude<AdminDetail,null>)=>{setDetail(next);setTab("users");raise(next==="pair2004"?2:next==="lin"?3:5)};\n const showCase=caseLevel>0&&(!!detail||result==="shen"||result==="lin"||result==="third");\n return <main className="admin-clean" style={s.adminPage}><style>{`.admin-clean h2,.admin-clean h3,.admin-clean h4{margin:0;font:700 16px/1.35 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#252925}.admin-clean small{font-size:11px}.admin-clean b,.admin-clean strong{font-family:inherit}.admin-clean p{font-size:12px;line-height:1.6}`}</style>\n  <header style={s.adminHead}><strong style={{fontSize:14,fontWeight:700}}>旧档管理</strong><span style={s.adminAccount}>旧档员-03</span></header>\n  <div style={s.adminLayout}>\n   <aside style={s.adminSide}><button className={tab==="watch"?"active":""} onClick={()=>{setTab("watch");setDetail(null)}}>观察名单</button><button className={tab==="users"?"active":""} onClick={()=>setTab("users")}>用户查询</button><button className={tab==="ops"?"active":""} onClick={()=>{setTab("ops");setDetail(null)}}>操作记录</button><button className={tab==="recycle"?"active":""} onClick={()=>{setTab("recycle");setDetail(null)}}>删除记录</button></aside>\n   <section style={s.adminBody}>\n    {tab==="watch"&&<WatchList openKnown={openKnown} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>}\n    {tab==="users"&&<><div style={s.sectionTitle}>用户查询</div><form onSubmit={doSearch} style={s.adminSearch}><Search size={16}/><input value={q} onChange={e=>{setQ(e.target.value);setSearched(false)}} placeholder="姓名 / UID / 记录编号"/><button>查询</button></form>{showCase&&<CaseTrail level={caseLevel} openShen={openShen} openDetail={openDetail}/>} {detail?<AdminDetailPage detail={detail} openDetail={openDetail} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>:<>{searched&&!result&&<p style={s.adminEmpty}>没有匹配记录。</p>}{result==="shen"&&<ShenRecord openDetail={openDetail} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>} {result==="liang"&&<LiangRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>} {result==="lin"&&<LinRecord openDetail={openDetail}/>} {result==="third"&&<ThirdRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>}</>}</>}\n    {tab==="ops"&&<Operations/>}\n    {tab==="recycle"&&<Recycle/>}\n   </section>\n  </div>\n </main>;\n}'''
s=s[:start]+new_admin+s[end:]

# Clearer body-vs-source wording in the key records.
s=s.replace('''<Record date="A" title="舍：沈妍" meta="客源：林楠" text="易舍完成；返家后持续观察。"/><Record date="B" title="舍：林楠" meta="客源：沈妍" text="易舍完成；返家后持续观察。"/>''',
'''<Record date="A侧" title="登记身体：沈妍" meta="客源：林楠" text="易舍完成；页面仍按登记身体‘沈妍’归档。"/><Record date="B侧" title="登记身体：林楠" meta="客源：沈妍" text="易舍完成；页面仍按登记身体‘林楠’归档。"/>''',1)
s=s.replace('''<Record date="选择" title="B侧旧客" meta="稳定期 22 年" text="2004年易舍后长期稳定；作为连续易舍样本。候舍对象 19-07：自愿，匹配通过。"/>''',
'''<Record date="选择" title="B侧：林楠登记身体" meta="旧客稳定期 22 年" text="2004年后B侧长期稳定；候舍对象19-07为第三名成年对象，匹配通过。"/>''',1)
s=s.replace('''<Record date="结果" title="执行完成" meta="2026-10-12 22:13" text="两侧生命体征稳定；原对契出现同步异常。"/>''',
'''<Record date="结果" title="执行完成" meta="2026-10-12 22:13" text="B侧旧客转入19-07舍；19-07原客转入B侧舍。随后A侧沈妍出现原对契同步异常。"/>''',1)

# 19-07 should be identity-fragmented, not a clean 'I am Shen Yan'.
old='''<Record date="10-12 22:36" title="身份陈述异常" meta="连续 4 次" text="对象否认登记身份，反复陈述：‘我叫沈妍。’"/><Record date="10-12 23:02" title="环境识别异常" meta="问询记录" text="声称住所不在当前登记地址；要求联系徐宁。"/>'''
new='''<Record date="10-12 22:36" title="身份陈述异常" meta="姓名不稳定" text="对象在‘沈妍’‘林楠’与登记身份之间反复切换；多次中断并追问‘我到底是谁’。"/><Record date="10-12 23:02" title="记忆与情绪反应" meta="问询记录" text="能描述不属于登记身份的旧屋细节；听到‘徐宁’时持续哭泣，随后反问‘她是谁，为什么我知道这个名字？’"/>'''
assert old in s
s=s.replace(old,new,1)

# Make the sync record explicitly say who was caught vs who underwent the second swap.
s=s.replace('''<Record date="处置理由" title="控制旧对契另一端" meta="执行 HN-1016-02" text="同步反应持续升高，可能影响二次易舍稳定性。转入控制，保留作旧对契稳定评估。"/>''',
'''<Record date="处置理由" title="控制A侧：沈妍" meta="执行 HN-1016-02" text="B侧（林楠登记身体）完成再舍后，A侧沈妍同步反应持续升高，可能影响试验稳定性；因此控制沈妍。沈妍不是本次再舍对象。"/>''',1)

# Operation record: no auto-unlock of Zhou. '折柳' is visually strong, discovery happens via forum search.
pattern=r'function Operations\(\)\{const zhouTime=getFirstContactTime\("zc"\);useEffect\(\(\)=>\{if\(zhouTime\)revealZhouConfrontation\(\)\},\[zhouTime\]\);return '
assert re.search(pattern,s)
s=re.sub(pattern,'function Operations(){const zhouTime=getFirstContactTime("zc");return ',s,count=1)
s=s.replace('''{zhouTime&&<Record date={`2026-10-17 ${zhouTime}`} title="访问者身份补录：0712-4471" meta="来源：折柳" text="访问者：徐宁。保留观察。"/>}''',
'''{zhouTime&&<Record date={`2026-10-17 ${zhouTime}`} title="访问者身份补录：0712-4471" meta="来源：折柳" metaStrong text="访问者：徐宁。保留观察。"/>}''',1)

# Record supports strong operation-source meta.
old='''function Record({date,title,meta,text}:{date:string;title:string;meta:string;text:string}){return <div style={s.record}><time>{date}</time><span><b>{title}</b><small>{meta}</small><p>{text}</p></span></div>}'''
new='''function Record({date,title,meta,text,metaStrong=false}:{date:string;title:string;meta:string;text:string;metaStrong?:boolean}){return <div style={s.record}><time>{date}</time><span><b>{title}</b><small style={metaStrong?{color:"#111",fontWeight:900,fontSize:12}:undefined}>{meta}</small><p>{text}</p></span></div>}'''
assert old in s
s=s.replace(old,new,1)

# Add styles for the case trail and shake box.
style_anchor=''' adminPage:{minHeight:"calc(100% - 39px)",background:"#e7eae7",color:"#252925"},'''
assert style_anchor in s
s=s.replace(style_anchor,style_anchor+'''sectionTitle:{margin:"0 0 10px",fontSize:16,fontWeight:700,color:"#252925"},caseTrail:{maxWidth:900,margin:"14px 0 6px",padding:"12px",border:"1px solid #c8ceca",borderRadius:8,background:"#f7f8f6"},caseTitle:{display:"block",marginBottom:8,fontSize:12},caseGrid:{display:"flex",gap:7,flexWrap:"wrap"},caseButton:{minWidth:138,padding:"8px 10px",border:"1px solid #c8ceca",borderRadius:6,background:"#fff",textAlign:"left",cursor:"pointer"},identityLegend:{display:"grid",gridTemplateColumns:"repeat(3,minmax(0,1fr))",gap:6,marginTop:10,padding:"9px 10px",borderTop:"1px solid #dde1de",fontSize:11,lineHeight:1.5},''',1)

v_anchor='''objectIcon:{display:"block",position:"relative",width:38,height:30},'''
assert v_anchor in s
s=s.replace(v_anchor,v_anchor+'''shakeBoxWrap:{width:120,display:"grid",justifyItems:"center",gap:7,margin:"0 8px"},shakeObject:{width:96,minHeight:82,border:"1px solid #7a4a40",background:"#e7d7bd",boxShadow:"0 7px 14px #0007"},boxNote:{display:"block",minHeight:28,maxWidth:120,color:"#b8aaa0",fontSize:10,lineHeight:1.35,textAlign:"center",fontStyle:"normal"},''',1)

p.write_text(s)

# ---------- WeChat: fix Liang wording, make Zhou hostile after identity reveal ----------
p=Path('app/InteractiveWechat.tsx')
s=p.read_text()
MARK='// v9.2.3 identity clarity + hostile Zhou'
if MARK not in s:
    s=s.replace('// v9.2.2b WeChat hard lock\n','// v9.2.2b WeChat hard lock\n'+MARK+'\n',1)

# Do not pre-hint Zhou via WeChat signature; forum search will expose real name directly.
s=s.replace('signature:"柳枝别折，怪可惜的。",','',1)

# Track identity discovery even if the player searches before contacting Zhou.
s=s.replace('''  zhouEvidenceSeen:false,\n  zhouConfronted:false,''','''  zhouEvidenceSeen:false,\n  zhouIdentityKnown:false,\n  zhouConfronted:false,''',1)

# Replace reveal function with a hostile, non-helper branch and add discovery function.
start=s.index('export const revealZhouConfrontation=()=>{')
end=s.index('\n\nconst materialRules:',start)
new_reveal='''export const revealZhouConfrontation=()=>{\n const stamp=wechatSession.firstContact.zc;\n if(!wechatSession.zhouIdentityKnown||!stamp||wechatSession.zhouConfronted)return false;\n wechatSession.zhouEvidenceSeen=true;\n wechatSession.freeText={...wechatSession.freeText,zc:false};\n wechatSession.freeReturn={...wechatSession.freeReturn,zc:[]};\n wechatSession.quick={...wechatSession.quick,zc:[{id:"zc-zheliu",text:"你是折柳？",emphasis:true,reply:[{text:"你为什么搜这个号。"}],next:[{id:"zc-zheliu-real",text:"论坛实名资料写的是周川。后台来源写的是折柳。",reply:[{text:"……"},{text:"把后台关掉。"},{text:"现在。"}],next:[{id:"zc-zheliu-log",text:`我${stamp}才告诉你我是徐宁，同一分钟后台就有折柳补录。`,reply:[{text:"关掉。"},{text:"我说关掉。"},{text:"不要再给梁茵发任何东西。"}],next:[{id:"zc-zheliu-how",text:"你怎么知道我给她发了？",reply:[{text:"……"},{text:"徐宁，你听我一次。"},{text:"离开沈妍家。别报警。"}]}]}]}]};\n notifyWechat();\n return true;\n};\nexport const discoverZhouIdentity=()=>{wechatSession.zhouIdentityKnown=true;notifyWechat();return revealZhouConfrontation()};'''
s=s[:start]+new_reveal+s[end:]

# Liang: make the central question explicitly about why Shen Yan was caught.
s=s.replace('''"admin-sync-shen":{ly:[{text:"时间真的挨得很近。"},{text:"10月12号那边执行完，沈妍这一侧就开始升高。"}],zc:[{text:"他们自己把这条标成了关联异常。"},{text:"‘控制’和执行批次比解释更重要。"}]},''',
'''"admin-sync-shen":{ly:[{text:"这份写得很清楚：被控制的是沈妍。"},{text:"触发原因是B侧再舍完成后，沈妍这边出现同步异常。别把‘谁做了第二次易舍’和‘谁被抓’混成一个人。"}],zc:[{text:"他们自己把这条标成了关联异常。"},{text:"‘控制’和执行批次比解释更重要。"}]},''',1)
s=s.replace('''const correct:QuickReply={id:"ly-sync-right",text:"林楠第二次易舍，把2004年的另一端也重新影响了？",reply:[{text:"我也是这么对上的。"},{text:"沈妍不是第二次试验的目标，她是旧对契重新有反应以后被控制的。"},{text:"现在得找她被转到哪。"}]};''',
'''const correct:QuickReply={id:"ly-sync-right",text:"所以沈妍被抓，是因为B侧再舍后她这个旧对契另一端出了异常？",reply:[{text:"对。"},{text:"抓的是沈妍；做第二次易舍的是B侧‘林楠’那具登记身体。两件事不是同一个人。"},{text:"沈妍不是第二次试验的目标，她是试验后出现的异常，所以才被控制。"},{text:"现在得找沈妍被转到哪。"}]};''',1)
s=s.replace('''const wrongAgain:QuickReply={id:"ly-sync-wrong-again",text:"所以他们也准备再给沈妍换一次？",reply:[{text:"可沈妍那份写的是‘控制旧对契另一端’，不是再舍对象。"}]};''',
'''const wrongAgain:QuickReply={id:"ly-sync-wrong-again",text:"所以他们抓沈妍，是准备再给沈妍换一次？",reply:[{text:"不是。沈妍这份写的是‘控制A侧旧对契另一端’，本次再舍对象在B侧。"}]};''',1)
s=s.replace('''const nextAfterCorrect:QuickReply[]=received("ly","admin-reswap-2026")?reswapReasoningChoices(received("ly","admin-sync-shen")):[{id:"ly-pair-why",text:"那既然换过了，为什么现在又抓沈妍？",reply:[{text:"对。这个才是现在的问题。"},{text:"2004那份解释不了2026。得看林楠后来又发生了什么。"}]}];''',
'''const nextAfterCorrect:QuickReply[]=received("ly","admin-reswap-2026")?reswapReasoningChoices(received("ly","admin-sync-shen")):[{id:"ly-pair-why",text:"那为什么2026年又把沈妍抓走？",reply:[{text:"对，这才是现在的问题。"},{text:"先分清：沈妍是A侧登记身体，林楠是B侧登记身体。2004只解释她们为什么有关联，还解释不了沈妍这次为什么被控制。"},{text:"要看B侧2026年的执行，再看沈妍自己的同步异常。"}]}];''',1)
s=s.replace('''const correct:QuickReply={id:"ly-reswap-test",text:"他们在测试同一个魂能不能连续换身体？",reply:[{text:"对。"},{text:"稳定22年、再次易舍、主体稳定——这几个字段放一起就是这个意思。"}],next:includeSync?syncReasoningChoices():[]};''',
'''const correct:QuickReply={id:"ly-reswap-test",text:"他们在测试同一个‘客’能不能连续换身体？",reply:[{text:"对。"},{text:"而且这里做第二次易舍的是B侧，也就是‘林楠’这具登记身体，不是沈妍。"},{text:"稳定22年、再次易舍、主体稳定——这几个字段放一起就是这个意思。"}],next:includeSync?syncReasoningChoices():[]};''',1)

# 19-07 material response matches fragmented identity.
s=s.replace('''"admin-third-1907":{ly:[{text:"她一直说自己叫沈妍？"},{text:"还主动要求联系徐宁……这句挺吓人的。"}],zc:[{text:"她连续四次都这么说？"},{text:"那不像一次口误。"}]},''',
'''"admin-third-1907":{ly:[{text:"她连自己到底叫沈妍还是林楠都说不稳。"},{text:"但一听到徐宁这个名字就哭……这比直接认出你更吓人。"}],zc:[{text:"姓名陈述来回变？"},{text:"那就不是一句口误能解释的。"}]},''',1)

# Zhou can no longer receive materials once confronted.
s=s.replace(''' const canPickMaterial=id!=="x"&&!!introduced[id]&&!actionLocked&&!hasQuick&&!freeText[id];''',
''' const zhouHostile=id==="zc"&&wechatSession.zhouConfronted;\n const canPickMaterial=id!=="x"&&!!introduced[id]&&!actionLocked&&!hasQuick&&!freeText[id]&&!zhouHostile;''',1)
s=s.replace(''' const sendable=useMemo(()=>id==="x"||!introduced[id]?[]:materials.filter(m=>{const rules=materialRules[m.id];return !!rules&&Object.prototype.hasOwnProperty.call(rules,id)&&rules[id]!==null&&!sent[`${id}:${m.id}`]}),[materials,id,sent,introduced]);''',
''' const sendable=useMemo(()=>id==="x"||!introduced[id]||zhouHostile?[]:materials.filter(m=>{const rules=materialRules[m.id];return !!rules&&Object.prototype.hasOwnProperty.call(rules,id)&&rules[id]!==null&&!sent[`${id}:${m.id}`]}),[materials,id,sent,introduced,zhouHostile]);''',1)

# If identity was discovered before first contact, unlock confrontation after the introduction finishes.
old='''  wechatSession.firstContact={...wechatSession.firstContact,[contactId]:stamp};\n  notifyWechat();\n  return [{time:`今天 ${stamp}`,who:"沈妍",text:introText(contactId)}];'''
new='''  wechatSession.firstContact={...wechatSession.firstContact,[contactId]:stamp};\n  notifyWechat();\n  if(contactId==="zc"&&wechatSession.zhouIdentityKnown)window.setTimeout(()=>revealZhouConfrontation(),0);\n  return [{time:`今天 ${stamp}`,who:"沈妍",text:introText(contactId)}];'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)

# ---------- Forum: red-box hint + direct Zhou real-name reveal ----------
p=Path('content/gameDataFlowV2.ts')
s=p.read_text()
MARK='// v9.2.3 discoverable red-box shake hint'
if MARK not in s:
    s=s.replace('const redBoxBase=',MARK+'\nconst redBoxBase=',1)
s=s.replace('''  highlights:[...new Set([...(redBoxBase.highlights||[]),"红铁皮盒","打开前会卡一下"])],''',
'''  highlights:[...new Set([...(redBoxBase.highlights||[]),"红铁皮盒"])],''',1)
needle='''  replies:[\n    ...redBoxBase.replies,\n'''
assert needle in s
s=s.replace(needle,needle+'''    reply("旧饼干盒","22:57","我家以前这类套盖铁皮盒也会卡。别硬撬，横着左右晃几下，再上下颠两下，盖沿松了就能开。"),\n''',1)
p.write_text(s)

p=Path('app/page.tsx')
s=p.read_text()
MARK='// v9.2.3 Zhou identity discovery'
if MARK not in s:
    s=s.replace('/* eslint-disable @next/next/no-img-element */\n','/* eslint-disable @next/next/no-img-element */\n'+MARK+'\n',1)
s=s.replace('''import InteractiveWechat,{SharedMaterial,WechatNotice,focusWechatContact,subscribeWechatNotices} from "./InteractiveWechat";''',
'''import InteractiveWechat,{SharedMaterial,WechatNotice,discoverZhouIdentity,focusWechatContact,subscribeWechatNotices} from "./InteractiveWechat";''',1)
old=''' const search=(value=q)=>{if(value.trim()){setQ(value);go({kind:"search",q:value.trim()})}};'''
new=''' const search=(value=q)=>{if(value.trim()){const term=value.trim();setQ(value);if(term==="折柳"){go({kind:"user",name:"折柳"});return}go({kind:"search",q:term})}};'''
assert old in s
s=s.replace(old,new,1)
old='''    {route.kind==="user"&&<UserProfile name={route.name} open={id=>go({kind:"post",id})}/>}'''
new='''    {route.kind==="user"&&(route.name==="折柳"?<ZheliuProfile open={id=>go({kind:"post",id})}/>:<UserProfile name={route.name} open={id=>go({kind:"post",id})}/>)}'''
assert old in s
s=s.replace(old,new,1)
anchor='''function ForumHeader({q,setQ,search,home,me,switchAccount}:{q:string;setQ:(x:string)=>void;search:(x?:string)=>void;home:()=>void;me:()=>void;switchAccount:()=>void})'''
assert anchor in s
profile='''function ZheliuProfile({open}:{open:(id:string)=>void}){\n useEffect(()=>{discoverZhouIdentity()},[]);\n return <main className="forum-page"><section style={{maxWidth:760,margin:"0 auto",padding:"22px 24px",border:"1px solid #ddd6ca",borderRadius:8,background:"#fbfaf6"}}><div style={{display:"flex",alignItems:"center",gap:14,paddingBottom:16,borderBottom:"1px solid #e4dfd5"}}><i style={{width:46,height:46,display:"grid",placeItems:"center",borderRadius:"50%",background:"#e8e3d8",fontStyle:"normal",fontWeight:800}}>折</i><span><h2 style={{margin:"0 0 5px",fontSize:20}}>折柳</h2><b style={{display:"block",fontSize:13}}>实名资料：周川</b><small style={{display:"block",marginTop:4,color:"#888"}}>公开资料页 · 烛阴旧闻用户</small></span></div><div style={{padding:"16px 0 4px",fontSize:13,lineHeight:1.8}}><p style={{margin:"0 0 10px"}}>个人资料很少，只保留了实名验证字段和公开回复记录。</p><button onClick={()=>open("20847")} style={{width:"100%",padding:"11px 12px",border:"1px solid #d8d2c7",borderRadius:6,background:"#fff",textAlign:"left",cursor:"pointer"}}><b style={{display:"block"}}>最近公开回复</b><small style={{display:"block",marginTop:4,color:"#777"}}>候鸟第七年的梦帖 · “看完了。红盒子先别管……”</small></button></div></section></main>\n}\n\n'''
s=s.replace(anchor,profile+anchor,1)
p.write_text(s)

print('Applied v9.2.3 admin clarity, Zhou reveal and shake-box puzzle')