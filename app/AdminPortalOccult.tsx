"use client";
// v9.2.3 admin clarity + shake box

import {CSSProperties,FormEvent,PointerEvent as ReactPointerEvent,ReactNode,useEffect,useMemo,useRef,useState} from "react";
import {ArrowLeft,ChevronRight,FilePlus2,LockKeyhole,Search,ShieldCheck} from "lucide-react";
import {SharedMaterial,discoverZhouIdentity,getFirstContactTime,triggerAdminWechatBeat,triggerZhouLocationThreat} from "./InteractiveWechat";
import {adultShen} from "./adminPortraits/adultShen";
import {adultLin} from "./adminPortraits/adultLin";
import {adultThird} from "./adminPortraits/adultThird";
import {childShen} from "./adminPortraits/childShen";
import {childLin} from "./adminPortraits/childLin";
import {editAdminText} from "../content/adminDialogues";

export const ADMIN_USER="旧档员-03";
export const ADMIN_TEMP_CODE="gumen-0712";
const OLD_OATH="身非我身名非我名";
const REMEMBERED_ADMIN_KEY="zhuyin-admin-user";

type Props={loggedIn:boolean;onAdminLogin:()=>void;onCancel:()=>void;onExitAdmin?:()=>void;canUseLegacy:boolean;onWechatIncoming?:()=>void;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean};
type AdminTab="watch"|"users"|"candidates"|"liturgy"|"ops"|"recycle";
type AdminDetail="pair2004"|"lin"|"reswap"|"third"|"sync"|"guestA"|"guestB"|"guestG"|"batch"|"location"|null;
type ResultKind="shen"|"liang"|"lin"|"third"|"zheliu"|null;

const normalize=(v:string)=>v.replace(/[，。、“”‘’\s]/g,"");

export default function AdminPortalOccult({loggedIn,onAdminLogin,onCancel,onExitAdmin,canUseLegacy,onWechatIncoming,onCopyMaterial,hasMaterial}:Props){
 const [mode,setMode]=useState<"login"|"verify">("login");
 const [user,setUser]=useState("");
 const [pwd,setPwd]=useState("");
 const [error,setError]=useState("");
 const [attemptedAdmin,setAttemptedAdmin]=useState(false);
 const [filled,setFilled]=useState(false);
 useEffect(()=>{if(loggedIn)return;try{if(window.sessionStorage.getItem(REMEMBERED_ADMIN_KEY)===ADMIN_USER)setUser(ADMIN_USER)}catch{}},[loggedIn]);

 if(loggedIn)return <AdminDesk onExitAdmin={onExitAdmin} onWechatIncoming={onWechatIncoming} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>;

 const submit=(e:FormEvent)=>{
  e.preventDefault();
  if(user.trim()===ADMIN_USER&&pwd===ADMIN_TEMP_CODE){try{window.sessionStorage.setItem(REMEMBERED_ADMIN_KEY,ADMIN_USER)}catch{};onAdminLogin();setError("");return;}
  if(user.trim()===ADMIN_USER){
   setAttemptedAdmin(true);
   if(canUseLegacy){setMode("verify");setError("");return;}
   setError("账号或密码错误。");return;
  }
  setAttemptedAdmin(false);
  setError(user.trim()?"账号或密码错误。":"请输入账号。");
 };
 const useCode=()=>{setUser(ADMIN_USER);setPwd(ADMIN_TEMP_CODE);setMode("login");setFilled(true);setError("")};

 if(mode==="verify")return <LegacyVerify onBack={()=>setMode("login")} onVerified={useCode}/>;
 return <main style={s.loginPage}>
  <section style={s.loginCard}>
   <button onClick={onCancel} style={s.back}><ArrowLeft size={15}/>返回</button>
   <div style={s.logo}>烛</div>
   <h2 style={s.loginTitle}>登录烛阴旧闻</h2>
   <p style={s.muted}>{user===ADMIN_USER?"已记住旧档账号。再次进入时只需要输入口令；忘记口令可以重新进行旧档验证。":"当前浏览器保存了一个已登录会话。也可以使用其他账号登录。"}</p>
   <form onSubmit={submit} style={s.form}>
    <label style={s.field}><span>账号</span><input value={user} onChange={e=>{setUser(e.target.value);setError("");setAttemptedAdmin(false)}} autoComplete="off" placeholder="用户名"/></label>
    <label style={s.field}><span>密码</span><input type="password" value={pwd} onChange={e=>{setPwd(e.target.value);setError("")}} autoComplete="off" placeholder="密码"/></label>
    {error&&<em style={s.error}>{error}</em>}
    {filled&&<small style={s.codeFilled}>旧档验证生成的临时口令已填入。</small>}
    <button style={s.primary}>登录</button>
   </form>
   {(attemptedAdmin||user.trim()===ADMIN_USER)&&canUseLegacy&&<button onClick={()=>setMode("verify")} style={s.legacy}>
    <LockKeyhole size={15}/><span><b>旧档账号验证</b><small>检测到迁移账号 · 使用兼容认证</small></span><ChevronRight size={15}/>
   </button>}
  </section>
 </main>;
}

function LegacyVerify({onBack,onVerified}:{onBack:()=>void;onVerified:()=>void}){
 type Child="lin"|"shen";
 type Home="factory"|"qingwu";
 type Item="plum"|"marble"|"milk"|"clip";
 const [stage,setStage]=useState(0);
 const [oath,setOath]=useState("");
 const [error,setError]=useState("");
 const [dragChild,setDragChild]=useState<Child|null>(null);
 const [homes,setHomes]=useState<Partial<Record<Home,Child>>>({});
 const [wrongHome,setWrongHome]=useState<Home|null>(null);
 const [dragItem,setDragItem]=useState<Item|null>(null);
 const [items,setItems]=useState<Partial<Record<Item,Child>>>({});
 const [boxOpened,setBoxOpened]=useState(false);
 const [boxNote,setBoxNote]=useState("盒盖卡住了。");
 const shakeRef=useRef({active:false,lastX:0,lastY:0,phase:"x" as "x"|"y",lastDir:0,h:0,v:0});
 const [moods,setMoods]=useState<Record<Child,"neutral"|"frown"|"smile">>({lin:"neutral",shen:"neutral"});
 const childInfo:Record<Child,{stamp:string}>={lin:{stamp:"07·18"},shen:{stamp:"07·17"}};
 const homeAnswer:Record<Home,Child>={factory:"lin",qingwu:"shen"};
 const itemAnswer:Record<Item,Child>={plum:"lin",marble:"lin",milk:"shen",clip:"shen"};
 const ordinaryItems:Item[]=["plum","marble","milk","clip"];
 const allOrdinaryPlaced=(next=items)=>ordinaryItems.every(id=>!!next[id]);
 const completeTable=(nextItems=items,opened=boxOpened)=>{if(allOrdinaryPlaced(nextItems)&&opened)window.setTimeout(()=>setStage(3),900)};
 const placeChild=(home:Home)=>{
  if(!dragChild)return;
  if(homeAnswer[home]!==dragChild){setWrongHome(home);window.setTimeout(()=>setWrongHome(null),520);return;}
  const next={...homes,[home]:dragChild};setHomes(next);setDragChild(null);if(next.factory&&next.qingwu)window.setTimeout(()=>setStage(2),900);
 };
 const frown=(child:Child)=>{setMoods(m=>({...m,[child]:"frown"}));window.setTimeout(()=>setMoods(m=>({...m,[child]:"neutral"})),680)};
 const giveItem=(target:Child)=>{
  if(!dragItem)return;const id=dragItem;
  if(itemAnswer[id]===target){const next={...items,[id]:target};setItems(next);setDragItem(null);completeTable(next,boxOpened);return;}
  setDragItem(null);frown(target);
 };
 const beginBoxShake=(e:ReactPointerEvent<HTMLDivElement>)=>{
  if(boxOpened)return;
  e.currentTarget.setPointerCapture(e.pointerId);
  const r=shakeRef.current;r.active=true;r.lastX=e.clientX;r.lastY=e.clientY;r.lastDir=0;
  setBoxNote("盖子抬起一点，又卡住了。");
 };
 const moveBoxShake=(e:ReactPointerEvent<HTMLDivElement>)=>{
  const r=shakeRef.current;if(!r.active||boxOpened)return;
  const dx=e.clientX-r.lastX,dy=e.clientY-r.lastY;
  if(r.phase==="x"&&Math.abs(dx)>11&&Math.abs(dx)>Math.abs(dy)*1.3){
   const dir=dx>0?1:-1;if(r.lastDir&&dir!==r.lastDir)r.h+=1;r.lastDir=dir;r.lastX=e.clientX;r.lastY=e.clientY;
   if(r.h>=3){r.phase="y";r.lastDir=0;setBoxNote("盒子里面轻轻响了一声。");}
  }else if(r.phase==="y"&&Math.abs(dy)>10&&Math.abs(dy)>Math.abs(dx)*1.15){
   const dir=dy>0?1:-1;if(r.lastDir&&dir!==r.lastDir)r.v+=1;r.lastDir=dir;r.lastX=e.clientX;r.lastY=e.clientY;
   if(r.v>=2){r.active=false;setBoxOpened(true);setBoxNote("咔。盒盖松开了。");completeTable(items,true);}
  }
 };
 const endBoxShake=()=>{const r=shakeRef.current;if(!boxOpened&&r.active)setBoxNote(r.phase==="y"?"里面像是松了一点，但盖子还卡着。":"盒盖还是卡着。");r.active=false};
 const progress=stage===0?"旧誓":stage===1?"1 / 2":stage===2?"2 / 2":"完成";
 return <main style={s.verifyPage}><section style={s.verifyShell}>
  <header style={s.verifyHead}><button onClick={onBack} style={s.darkBack}><ArrowLeft size={15}/>返回登录</button><span><small>旧档账号验证</small><b>兼容认证</b></span><em>{progress}</em></header>
  {stage===0&&<div style={s.oathPage}><div style={s.oathSigil}><span>門</span></div><small style={s.redSmall}>迁移账号 · 旧誓核验</small><h2 style={s.oathTitle}>请录入旧誓</h2><form onSubmit={e=>{e.preventDefault();if(normalize(oath)===OLD_OATH){setStage(1);setError("")}else setError(oath.trim()?"旧誓不合。":"请录入旧誓。")}} style={s.oathForm}><input autoFocus value={oath} onChange={e=>{setOath(e.target.value);setError("")}} placeholder="旧誓" autoComplete="off"/><button>确认</button></form>{error&&<p style={s.ritualError}>{error}</p>}</div>}
  {stage===1&&<div style={v.puzzle}><div style={v.dollShelf}>{(["lin","shen"] as Child[]).filter(id=>!Object.values(homes).includes(id)).map(id=><PaperPerson key={id} stamp={childInfo[id].stamp} mood="smile" draggable onDragStart={()=>setDragChild(id)}/>)}</div><div style={v.homeGrid}><HomeRoom kind="factory" wrong={wrongHome==="factory"} onDrop={()=>placeChild("factory")}>{homes.factory&&<PaperPerson stamp={childInfo[homes.factory].stamp} mood="neutral"/>}</HomeRoom><HomeRoom kind="qingwu" wrong={wrongHome==="qingwu"} onDrop={()=>placeChild("qingwu")}>{homes.qingwu&&<PaperPerson stamp={childInfo[homes.qingwu].stamp} mood="neutral"/>}</HomeRoom></div></div>}
  {stage===2&&<div style={v.tableScene}><div style={v.tableSeats}><TableSeat place="4栋东侧" mood={moods.lin} side="left" onDrop={()=>giveItem("lin")} items={ordinaryItems.filter(id=>items[id]==="lin")}/><div style={v.centerTable}><div style={v.tableTop}>{ordinaryItems.filter(id=>!items[id]).map(id=><ObjectToken key={id} id={id} draggable onDragStart={()=>setDragItem(id)}/>)}<div style={v.shakeBoxWrap}><div onPointerDown={beginBoxShake} onPointerMove={moveBoxShake} onPointerUp={endBoxShake} onPointerCancel={endBoxShake} style={{...v.object,...v.shakeObject,cursor:boxOpened?"default":"grab",touchAction:"none"}}><i style={{...v.objectIcon,position:"relative",...v.box}}>{boxOpened&&<span style={{position:"absolute",left:1,right:1,top:-7,height:7,border:"1px solid #704236",borderBottom:0,background:"#7d2b23",transform:"rotate(-8deg)",transformOrigin:"left bottom",boxShadow:"0 -2px 8px #0008"}}/>}</i><small>红铁皮盒</small></div><em style={v.boxNote}>{boxNote}</em></div></div></div><TableSeat place="青梧旧楼" mood={moods.shen} side="right" onDrop={()=>giveItem("shen")} items={ordinaryItems.filter(id=>items[id]==="shen")}/></div></div>}
  {stage===3&&<div style={s.success}><ShieldCheck size={34}/><small>验证完成</small><h2>旧档账号临时口令</h2><code>{ADMIN_TEMP_CODE}</code><p>记住这个口令。账号会保留；以后只需输入口令。忘了就再做一次旧档验证。</p><button onClick={onVerified} style={s.verifyButton}>返回登录并填入口令</button></div>}
 </section></main>;
}

function PaperPerson({stamp,mood,draggable,onDragStart}:{stamp:string;mood:"smile"|"neutral"|"frown";draggable?:boolean;onDragStart?:()=>void}){return <div draggable={draggable} onDragStart={e=>{e.dataTransfer.effectAllowed="move";onDragStart?.()}} style={{...v.person,cursor:draggable?"grab":"default"}}><div style={v.personHead}><i style={{...v.eye,left:16}}/><i style={{...v.eye,right:16}}/><span style={mood==="smile"?v.smile:mood==="frown"?v.frown:v.flatMouth}/></div><div style={v.personBody}><b>{stamp}</b></div></div>}
function HomeRoom({kind,wrong,onDrop,children}:{kind:"factory"|"qingwu";wrong:boolean;onDrop:()=>void;children:ReactNode}){const factory=kind==="factory";return <section onDragOver={e=>e.preventDefault()} onDrop={onDrop} style={{...v.home,...(wrong?v.homeWrong:{})}}><small style={v.roomStamp}>{factory?"4栋东侧":"青梧旧楼"}</small><div style={v.roomVisual}>{factory?<><span style={v.blueCurtain}/><i style={v.redTin}/><em style={v.oldCup}/></>:<><span style={v.woodDesk}/><i style={v.redClip}/><em style={v.candyJar}/></>}<div style={v.homeDoor}/><div style={v.homeOccupant}>{children}</div></div></section>}
function TableSeat({place,mood,side,onDrop,items}:{place:string;mood:"neutral"|"frown"|"smile";side:"left"|"right";onDrop:()=>void;items:string[]}){return <section onDragOver={e=>e.preventDefault()} onDrop={onDrop} style={v.seat}><small style={v.roomStamp}>{place}</small><div style={v.seatedPerson}><PaperPerson stamp={side==="left"?"07·18":"07·17"} mood={mood}/></div><div style={v.kept}>{items.map(id=><ObjectToken key={id} id={id}/>)}</div></section>}
function ObjectToken({id,draggable,onDragStart}:{id:string;draggable?:boolean;onDragStart?:()=>void}){const labels:Record<string,string>={plum:"话梅糖",marble:"蓝玻璃弹珠",milk:"奶糖",clip:"红色发卡"};return <div draggable={draggable} onDragStart={e=>{e.dataTransfer.effectAllowed="move";onDragStart?.()}} style={{...v.object,cursor:draggable?"grab":"default"}}><i style={{...v.objectIcon,position:"relative",...(id==="plum"?v.plum:id==="marble"?v.marble:id==="milk"?v.milk:v.clip)}}/><small>{labels[id]}</small></div>}

const adminDeskSession:{tab:AdminTab;q:string;searched:boolean;detail:AdminDetail}={tab:"watch",q:"",searched:false,detail:null};
const adminWatchMaterial:SharedMaterial={id:"admin-watchlist",title:"旧档管理 · 观察名单",kind:"后台记录",url:"https://www.zhuyinwen.cn/admin/watch"};
const adminShenMaterial:SharedMaterial={id:"admin-shen-record",title:"候鸟第七年 · 后台记录",kind:"后台记录",url:"https://www.zhuyinwen.cn/admin/users/0712-4471"};
const adminLiangMaterial:SharedMaterial={id:"admin-liang-record",title:"迟迟 · 后台记录",kind:"后台记录",url:"https://www.zhuyinwen.cn/admin/users/0419-2286"};
const adminPair2004Material:SharedMaterial={id:"admin-pair-2004",title:"LN-2004-0718 · 双向易舍记录",kind:"后台记录",url:"https://www.zhuyinwen.cn/admin/archive/LN-2004-0718"};
const adminReswapMaterial:SharedMaterial={id:"admin-reswap-2026",title:"2026-10-12 · 再舍验证记录",kind:"后台记录",url:"https://www.zhuyinwen.cn/admin/execution/RS-2026-1012"};
const adminSyncMaterial:SharedMaterial={id:"admin-sync-shen",title:"0712-4471 · 关联同步异常",kind:"后台记录",url:"https://www.zhuyinwen.cn/admin/links/0712-4471"};
const adminThirdMaterial:SharedMaterial={id:"admin-third-1907",title:"候舍对象 19-07 · 当前记录",kind:"后台记录",url:"https://www.zhuyinwen.cn/admin/subjects/19-07"};
const adminLocationMaterial:SharedMaterial={id:"admin-location-hln04",title:"HL-N-04 · 河临北郊第三仓储区4号库",kind:"位置记录",url:"https://www.zhuyinwen.cn/admin/sites/HL-N-04"};

function AddMaterialButton({material,onCopyMaterial,hasMaterial}:{material:SharedMaterial;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){
 if(!onCopyMaterial)return null;
 const added=!!hasMaterial?.(material.id);
 return <button disabled={added} onClick={()=>onCopyMaterial(material)} style={{minWidth:220,height:46,display:"inline-flex",alignItems:"center",justifyContent:"center",gap:9,margin:"4px 0 16px",padding:"0 16px",border:added?"1px solid #b9c3bd":"2px solid #4b7d67",borderRadius:8,background:added?"#e9eeeb":"#fff",color:added?"#6f7c75":"#2e654d",fontSize:13,fontWeight:800,cursor:added?"default":"pointer",boxShadow:added?"none":"0 5px 14px #284b3b18"}}><FilePlus2 size={20}/>{added?"已加入调查材料":"加入调查材料"}</button>
}

let adminCaseLevel=0;
function CaseTrail({level,openShen,openDetail}:{level:number;openShen:()=>void;openDetail:(x:Exclude<AdminDetail,null>)=>void}){
 const items=[
  {label:"沈妍",sub:"用户档案 · 0712-4471",go:openShen},
  {label:"2004旧案",sub:"LN-2004-0718",go:()=>openDetail("pair2004")},
  {label:"林楠",sub:"关联对象",go:()=>openDetail("lin")},
  {label:"2026再舍",sub:"RS-2026-1012",go:()=>openDetail("reswap")},
  {label:"同步异常",sub:"AN-0712-1012",go:()=>openDetail("sync")},
  {label:"19-07",sub:"候舍对象",go:()=>openDetail("third")},
 ];
 return <section style={s.caseTrail}><b style={s.caseTitle}>已查到的关联记录</b><div style={s.caseGrid}>{items.filter((_,i)=>i<=level).map(x=><button key={x.label} onClick={x.go} style={s.caseButton}><strong>{x.label}</strong><small>{x.sub}</small></button>)}</div></section>
}

function AdminDesk({onExitAdmin,onWechatIncoming,onCopyMaterial,hasMaterial}:{onExitAdmin?:()=>void;onWechatIncoming?:()=>void;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){
 const [tab,setTab]=useState<AdminTab>(()=>adminDeskSession.tab);
 const [q,setQ]=useState(()=>adminDeskSession.q);
 const [searched,setSearched]=useState(()=>adminDeskSession.searched);
 const [detail,setDetail]=useState<AdminDetail>(()=>adminDeskSession.detail);
 const [caseLevel,setCaseLevel]=useState(()=>adminCaseLevel);
 const result=useMemo<ResultKind>(()=>{if(!searched)return null;const t=q.trim();if(/候鸟第七年|沈妍|0712-4471/.test(t))return "shen";if(/迟迟|梁茵|0419-2286/.test(t))return "liang";if(/林楠/.test(t))return "lin";if(/19-07|候舍/.test(t))return "third";if(/折柳|周川/.test(t))return "zheliu";return null},[searched,q]);
 useEffect(()=>{adminDeskSession.tab=tab;adminDeskSession.q=q;adminDeskSession.searched=searched;adminDeskSession.detail=detail;adminCaseLevel=caseLevel},[tab,q,searched,detail,caseLevel]);
 useEffect(()=>{const timer=window.setTimeout(()=>{if(triggerAdminWechatBeat("shen-record"))onWechatIncoming?.()},900);return ()=>window.clearTimeout(timer)},[]);
 const fireShenBeat=()=>{if(triggerAdminWechatBeat("shen-record"))onWechatIncoming?.()};
 const raise=(n:number)=>setCaseLevel(v=>Math.max(v,n));
 const doSearch=(e?:FormEvent)=>{e?.preventDefault();const raw=q.trim();const t=raw.replace(/客|编号|[-_\s]/g,"");setSearched(true);if(/^LN20040718$/i.test(t)){setDetail("pair2004");raise(2);return}if(/^RS20261012$/i.test(t)){setDetail("reswap");raise(5);return}if(/^AN07121012$/i.test(t)){setDetail("sync");raise(5);return}if(/^1907$/i.test(t)){setDetail("third");raise(5);return}if(/^HN101602$/i.test(t)){setDetail("batch");raise(6);return}if(/^HLN04$/i.test(t)){setDetail("location");raise(7);return}if(t==="α"){setDetail("guestA");raise(5);return}if(t==="β"){setDetail("guestB");raise(5);return}if(t==="γ"){setDetail("guestG");raise(5);return}setDetail(null);if(/候鸟第七年|沈妍|07124471/.test(t)){raise(1);fireShenBeat()}if(/林楠/.test(t))raise(3)};
 const openKnown=(name:string)=>{setQ(name);setSearched(true);setDetail(null);setTab("users");if(/候鸟第七年|沈妍/.test(name)){raise(1);fireShenBeat()}};
 const openShen=()=>{setQ("沈妍");setSearched(true);setDetail(null);setTab("users");raise(1)};
 const openDetail=(next:Exclude<AdminDetail,null>)=>{setDetail(next);setTab("users");raise(next==="pair2004"?2:next==="lin"?3:5)};
 const showCase=caseLevel>0&&(!!detail||result==="shen"||result==="lin"||result==="third");
 return <main className="admin-clean" style={s.adminPage}><style>{`.admin-clean h2,.admin-clean h3,.admin-clean h4{margin:0;font:700 16px/1.35 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#252925}.admin-clean small{font-size:11px}.admin-clean b,.admin-clean strong{font-family:inherit}.admin-clean p{font-size:12px;line-height:1.6}`}</style>
  <header style={s.adminHead}><strong style={{fontSize:14,fontWeight:700}}>旧档管理</strong><span style={{display:"flex",alignItems:"center",gap:8}}><span style={s.adminAccount}>旧档员-03</span>{onExitAdmin&&<button onClick={onExitAdmin} style={{height:32,padding:"0 11px",border:"1px solid #758981",borderRadius:6,background:"#f5f8f6",color:"#2d493e",fontSize:11,fontWeight:700,cursor:"pointer"}}>返回论坛</button>}</span></header>
  <div style={s.adminLayout}>
   <aside style={s.adminSide}><button className={tab==="watch"?"active":""} onClick={()=>{setTab("watch");setDetail(null)}}>观察名单</button><button className={tab==="users"?"active":""} onClick={()=>setTab("users")}>用户查询</button><button className={tab==="candidates"?"active":""} onClick={()=>{setTab("candidates");setDetail(null)}}>候舍库</button><button className={tab==="liturgy"?"active":""} onClick={()=>{setTab("liturgy");setDetail(null)}}>诵录</button><button className={tab==="ops"?"active":""} onClick={()=>{setTab("ops");setDetail(null)}}>操作记录</button><button className={tab==="recycle"?"active":""} onClick={()=>{setTab("recycle");setDetail(null)}}>删除记录</button></aside>
   <section style={s.adminBody}>
    {tab==="watch"&&<WatchList openKnown={openKnown} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>}
    {tab==="users"&&<><div style={s.sectionTitle}>用户查询</div><form onSubmit={doSearch} style={s.adminSearch}><Search size={16}/><input value={q} onChange={e=>{setQ(e.target.value);setSearched(false)}} placeholder="姓名 / 论坛账号 / UID / 记录编号 / 客编号"/><button>查询</button></form>{showCase&&<CaseTrail level={caseLevel} openShen={openShen} openDetail={openDetail}/>} {detail?<AdminDetailPage detail={detail} openDetail={openDetail} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>:<>{searched&&!result&&<p style={s.adminEmpty}>没有匹配记录。</p>}{result==="shen"&&<ShenRecord openDetail={openDetail} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>} {result==="liang"&&<LiangRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>} {result==="lin"&&<LinRecord openDetail={openDetail}/>} {result==="third"&&<ThirdRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>} {result==="zheliu"&&<ZheliuAdminRecord/>}</>}</>}
    {tab==="candidates"&&<CandidateLibrary/>}
    {tab==="liturgy"&&<Liturgy/>}
    {tab==="ops"&&<Operations/>}
    {tab==="recycle"&&<Recycle/>}
   </section>
  </div>
 </main>;
}

let liturgyBurned=false;
function Liturgy(){
 const [step,setStep]=useState(()=>liturgyBurned?99:0);
 const [dismissed,setDismissed]=useState(()=>liturgyBurned);
 useEffect(()=>{
  if(liturgyBurned)return;
  const timers=[
   window.setTimeout(()=>setStep(1),850),
   window.setTimeout(()=>setStep(2),1900),
   window.setTimeout(()=>setStep(3),3100),
   window.setTimeout(()=>setStep(4),4400),
   window.setTimeout(()=>setStep(5),5900),
   window.setTimeout(()=>{liturgyBurned=true;setStep(99)},7600),
  ];
  return ()=>timers.forEach(id=>window.clearTimeout(id));
 },[]);
 useEffect(()=>{
  const onKey=(e:KeyboardEvent)=>{if(e.key==="Escape")setDismissed(true)};
  window.addEventListener("keydown",onKey);
  return ()=>window.removeEventListener("keydown",onKey);
 },[]);
 if(dismissed)return <><div style={s.sectionTitle}>诵录</div><section style={{minHeight:360,display:"grid",placeItems:"center",border:"1px solid #171717",borderRadius:6,background:"#050505",color:"#3b3b3b",boxShadow:"inset 0 0 90px #000"}}><div style={{textAlign:"center"}}><b style={{display:"block",marginBottom:10,color:"#5d5d5d",font:"12px ui-monospace,SFMono-Regular,Consolas,monospace",letterSpacing:".16em"}}>ERR_ARCHIVE_410</b><small style={{color:"#2f2f2f",font:"11px ui-monospace,SFMono-Regular,Consolas,monospace"}}>诵录读取失败</small></div></section></>;
 const fullLine=(n:number,text:string,top:string,left:string,size:string,spacing:string,tilt:string)=>{
  const visible=step>=n&&step!==99;
  const active=step===n;
  return <p style={{position:"absolute",left,top,width:"84%",margin:0,transform:`translate(-50%,-50%) rotate(${tilt}) scale(${active?1.055:1})`,padding:"0 3vw",boxSizing:"border-box",opacity:visible?1:0,color:active?"#c91b24":"#6d1117",fontFamily:'STKaiti,KaiTi,"FangSong",serif',fontSize:size,fontWeight:900,lineHeight:1.02,letterSpacing:spacing,textAlign:"center",WebkitTextStroke:".45px #2a0000",textShadow:active?"0 0 3px #ff30306b,2px 2px 0 #360000,-2px 1px 0 #210000,0 0 26px #780006a8,0 10px 24px #120000":"1px 2px 0 #2c0000,-1px 1px 0 #180000,0 0 10px #4b00006b",filter:active?"contrast(1.2) saturate(1.35)":"contrast(1.08) saturate(1.1)",transition:"opacity .55s ease, transform .95s ease, color .45s ease, filter .45s ease"}}>{editAdminText(text)}</p>;
 };
 if(step===99)return <section onClick={()=>setDismissed(true)} style={{position:"fixed",inset:0,zIndex:9999,display:"grid",placeItems:"center",background:"#000",cursor:"default",boxShadow:"inset 0 0 180px #000"}}><span style={{color:"#151515",font:"11px ui-monospace,SFMono-Regular,Consolas,monospace",letterSpacing:".18em"}}>ERR_ARCHIVE_410</span><small style={{position:"fixed",right:22,bottom:18,color:"#161616",font:"10px ui-monospace,SFMono-Regular,Consolas,monospace",letterSpacing:".12em"}}>ESC</small></section>;
 return <section style={{position:"fixed",inset:0,zIndex:9999,overflow:"hidden",background:"radial-gradient(circle at 50% 48%,#130202 0%,#080202 36%,#020101 70%,#000 100%)",color:"#a20f18",boxShadow:"inset 0 0 240px #000"}}>
  <div style={{position:"absolute",inset:0,opacity:.18,background:"repeating-linear-gradient(176deg,transparent 0,transparent 7px,#6d00000d 8px,#6d00000d 9px)",pointerEvents:"none"}}/>
  {fullLine(1,"身为舍。","20%","46%","clamp(42px,6.2vw,92px)",".09em","-2.2deg")}
  {fullLine(2,"魂为客。","38%","53%","clamp(49px,7.4vw,108px)",".13em","1.35deg")}
  {fullLine(3,"名可弃。","57%","45%","clamp(58px,9vw,132px)",".08em","-1.4deg")}
  {fullLine(4,"舍可更。","76%","55%","clamp(68px,11vw,165px)",".16em","2.1deg")}
  {step>=5&&<><div style={{position:"absolute",inset:0,background:"#000e",boxShadow:"inset 0 0 220px #000",transition:"background .18s ease"}}/><div style={{position:"absolute",left:"50%",top:"50%",transform:"translate(-50%,-50%)",width:"min(980px,90vw)",padding:"12px 18px",boxSizing:"border-box",color:"#eeeeee",font:"700 clamp(18px,2.2vw,30px) ui-monospace,SFMono-Regular,Consolas,monospace",letterSpacing:".075em",lineHeight:1.5,textAlign:"center",textShadow:"0 0 16px #ffffff21"}}>{editAdminText("访问者徐宁，未登记候舍编号。")}</div></>}
 </section>;
}

function CandidateLibrary(){
 const rows=[
  ["24-11","女 / 26","申请 3 次","选我。现在就做。我不要这具身体。谁进来都行。如果进真君序列，不用再问我。"],
  ["21-16","男 / 42","申请 5 次","我等了六年。下一次必须是我。普通客也行，真君更好。别再让我醒回这具舍里。"],
  ["19-03","女 / 28","申请 2 次","不用通知外面。执行完把我现在的东西全清掉。真君需要就直接用，别留退路。"],
  ["22-08","男 / 35","申请 4 次","不合适就废舍。别把我退回来。失败也算我完成奉舍。"],
  ["23-14","女 / 31","申请 3 次","编号就够了。旧照片、住址、关系都清掉。执行后不要让我再知道它们。"],
  ["18-02","男 / 39","申请 6 次","现在就能做。谁需要这具舍就给谁。真君要用的话，不要再问我愿不愿意。"],
 ];
 return <><div style={s.sectionTitle}>候舍库</div><p style={{margin:"0 0 14px",color:"#707872",fontSize:12}}>姓名字段已舍弃。候舍编号为唯一有效身份。</p><div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:8,marginBottom:16}}>{[["在库","164"],["匹配可用","37"],["待执行","12"],["再舍申请","8"]].map(([k,v])=><div key={k} style={{padding:"11px 12px",border:"1px solid #cbd1cd",borderRadius:7,background:"#fff"}}><small style={{display:"block",color:"#7b837e"}}>{k}</small><b style={{display:"block",marginTop:4,fontSize:22}}>{v}</b></div>)}</div>
 <section style={s.adminPanel}><h4>筛选规范沿革</h4><Record date="2004版" title="低龄强制样本优先" meta="适用：7—11岁" text="名称识别已形成；长期社会身份尚未固化；返家后的记忆、性格异常可归入失踪应激。"/><Record date="2012修订" title="停止低龄优先" meta="成年自愿候舍纳入正式序列" text="长期样本证明年龄不是必要条件。改以对契匹配、去名训练与成年自愿对象为主。"/><Record date="去名训练" title="仅保留候舍编号" meta="入库前连续30日" text="停止使用原名；不看旧照片；减少原家庭接触；问询时只对候舍编号作答。完成后原姓名字段从候舍库移除。"/><Record date="现行" title="候舍来源充足，无需强制补充" meta="旧契样本另行处置" text="常规候舍优先从奉舍申请中匹配。旧契样本不可替代；出现同步、返契异常时优先回收。"/></section>
 <section style={s.adminPanel}><h4>归真序列 · 阶段 II</h4><Record date="前置验证" title="长期客二次再舍稳定" meta="RS-2026-1012" text="客α作为当前长期样本。二次再舍已完成；旧对契异常尚未关闭。"/><Record date="候舍池" title="来源充足" meta="匹配可用 37 / 待执行 12" text="现阶段不批准以强制方式补充普通候舍。"/><Record date="真君序列" title="暂缓启用" meta="待长期客验证通过" text="连续再舍稳定性未达到启用条件。旧客验证完成后重新评估。"/></section>
 <section style={s.adminPanel}><h4>近期奉舍申请</h4>{rows.map(([id,meta,count,text])=><Record key={id} date={id} title={meta} meta={count} text={`申请原文：${editAdminText(text)}`}/>)}</section>
 </>;
}

const watchRows=[
 ["0712-4471","候鸟第七年","沈妍","已控制","10-16 21:06"],["0419-2286","迟迟","梁茵","持续观察","今天 18:42"],["3188-2204","纸鸢北","—","待复核","今天 17:51"],["4410-1733","潮湿墙角","贺某","接触完成","今天 16:27"],["2257-9031","雨停以前","—","观察 II","今天 14:09"],["5830-1642","旧车站","张某","已排除","昨天 23:44"],["7741-0928","白炽灯坏了","—","观察 I","昨天 21:02"],["6602-3511","三号窗","孙某","待复核","10-15 18:06"],["1194-6208","河堤左边","—","已排除","10-15 15:31"],["9021-4470","借火","刘某","观察 II","10-14 22:19"],["3107-0584","九月潮气","—","资料补全","10-14 11:42"],["8172-3306","碎瓷片","王某","观察 I","10-13 20:11"],["5928-7743","旧伞","—","已排除","10-13 08:55"],["2031-9916","南站末班车","赵某","待复核","10-12 19:37"],["7350-1102","台阶第七级","—","观察 II","10-12 03:26"],
];
function WatchList({openKnown,onCopyMaterial,hasMaterial}:{openKnown:(name:string)=>void;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){return <><h2>观察名单</h2><AddMaterialButton material={adminWatchMaterial} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/><div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:8,margin:"0 0 14px"}}>{[["活跃观察","83"],["待复核","17"],["本月线下接触","6"],["样本待登记","2"]].map(([k,val])=><span key={k} style={{padding:"10px 12px",border:"1px solid #d5d9d6",background:"#fff"}}><small style={{display:"block",color:"#8a918d"}}>{k}</small><b style={{fontSize:20}}>{val}</b></span>)}</div><div style={{border:"1px solid #d5d9d6",background:"#fff",fontSize:12}}><div style={{display:"grid",gridTemplateColumns:"110px 1.2fr 1fr 1fr 110px",gap:8,padding:"8px 10px",background:"#eef1ef",color:"#6c746f",fontWeight:700}}><span>UID</span><span>论坛账号</span><span>关联姓名</span><span>状态</span><span>最后更新</span></div>{watchRows.map((r,i)=>{const known=r[1]==="候鸟第七年"||r[1]==="迟迟";return <button key={r[0]} onClick={()=>known&&openKnown(r[1])} style={{width:"100%",display:"grid",gridTemplateColumns:"110px 1.2fr 1fr 1fr 110px",gap:8,padding:"9px 10px",border:0,borderTop:"1px solid #edf0ee",background:i%2?"#fbfcfb":"#fff",textAlign:"left",fontSize:12,cursor:known?"pointer":"default"}}><code>{r[0]}</code><b style={{fontWeight:known?700:500}}>{r[1]}</b><span>{r[2]}</span><span>{r[3]}</span><time>{r[4]}</time></button>})}</div></>}

function PortraitCard({src,label}:{src:string;label:string}){return <figure style={s.portrait}><img src={src} alt="" style={s.portraitImg}/><figcaption>{label}</figcaption></figure>}
function PortraitPair({children}:{children:ReactNode}){return <div style={s.portraitPair}>{children}</div>}
function DetailLink({children,onClick}:{children:ReactNode;onClick:()=>void}){return <button onClick={onClick} style={s.detailLink}>{children}</button>}

function ShenRecord({openDetail,onCopyMaterial,hasMaterial}:{openDetail:(x:AdminDetail)=>void;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){return <article style={s.userRecord}>
 <header style={s.userHead}><i>候</i><span><h3>候鸟第七年</h3><small>实名关联：沈妍 · UID 0712-4471 · 最后活动 2026-10-16 19:48</small></span><em>已控制</em></header>
 <PortraitPair><PortraitCard src={adultShen} label="当前档案影像"/></PortraitPair>
 <AddMaterialButton material={adminShenMaterial} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>
 <div style={s.statusGrid}><span><small>对契匹配</small><b>92%</b></span><span><small>血样</small><b>已采集</b></span><span><small>当前状态</small><b>已控制</b></span><span><small>执行批次</small><b>HN-1016-02</b></span></div>
 <section style={s.adminPanel}><h4>关联信息</h4><Record date="旧案" title="2004-07-17" meta="年龄 9 · 失踪 13 天" text="关联旧案：LN-2004-0718；关联对象：林楠。"/><Record date="首次录入" title="2021-06-14" meta="自动索引匹配" text="论坛实名映射完成；进入长期观察。"/></section>
 <section style={s.adminPanel}><h4>观察记录</h4><Record date="2022-11-03 01:17" title="站内搜索记录" meta="候鸟第七年" text="查询：小时候走失 / 记不得 / 回来以后。"/><Record date="2024-09-07 00:46" title="旧厂区内容访问" meta="行为记录" text="连续查看岚棉三厂旧址照片 37 分钟。"/><Record date="2026-06-19 03:12" title="内容命中" meta="梦境帖" text="红铁皮盒、蓝窗帘、厨房位置重复出现。"/><Record date="2026-08-22 04:12" title="观察等级调整" meta="操作人：照骨" text="II → III；对契匹配 92%；恢复旧案关联观察。"/><Record date="2026-10-16 19:49" title="线下转交" meta="执行：旧档员-03" text="完成。停止公开区接触。"/><Record date="2026-10-16 20:52" title="样本登记" meta="内部任务" text="血样 2 管；保存状态：有效。"/><Record date="2026-10-16 21:06" title="人员状态变更" meta="旧档员-03" text="观察中 → 已控制。"/></section>
 <section style={s.adminPanel}><h4>执行信息</h4><Record date="HN-1016-02" title="对象类型：返契祭品" meta="执行批次" text="执行条件：待复核；当前场地字段未展开。"/></section>
 </article>}

function AdminDetailPage({detail,openDetail,onCopyMaterial,hasMaterial}:{detail:Exclude<AdminDetail,null>;openDetail:(x:AdminDetail)=>void;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){
 if(detail==="pair2004")return <Pair2004 openDetail={openDetail} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>;
 if(detail==="lin")return <LinRecord openDetail={openDetail}/>;
 if(detail==="reswap")return <ReswapRecord openDetail={openDetail} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>;
 if(detail==="third")return <ThirdRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>;
 if(detail==="guestA")return <GuestRecord id="α"/>;
 if(detail==="guestB")return <GuestRecord id="β"/>;
 if(detail==="guestG")return <GuestRecord id="γ"/>;
 if(detail==="batch")return <BatchRecord/>;
 if(detail==="location")return <LocationRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>;
 return <SyncRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>;
}
function Pair2004({openDetail,onCopyMaterial,hasMaterial}:{openDetail:(x:AdminDetail)=>void;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){return <article style={s.userRecord}><h2 style={{marginTop:0}}>LN-2004-0718</h2><p style={s.subtle}>2004年旧案 · 双向易舍记录</p><PortraitPair><PortraitCard src={childShen} label="沈妍 · 2004"/><PortraitCard src={childLin} label="林楠 · 2004"/></PortraitPair><AddMaterialButton material={adminPair2004Material} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/><section style={s.adminPanel}><h4>执行记录</h4><Record date="A" title="舍：沈妍" meta="客编号：β" text="易舍完成；返家后持续观察。"/><Record date="B" title="舍：林楠" meta="客编号：α" text="易舍完成；返家后持续观察。"/><Record date="结果" title="双向完成" meta="2004-07" text="两侧生命体征稳定；后续身份适应记录正常。"/></section><Record date="关联对象" title="林楠" meta="B侧" text="实名关联已确认。"/></article>}
function LinRecord({openDetail}:{openDetail:(x:AdminDetail)=>void}){return <article style={s.userRecord}><header style={s.userHead}><i>林</i><span><h3>林楠</h3><small>关联旧案：LN-2004-0718 · B侧</small></span><em>在册</em></header><PortraitPair><PortraitCard src={adultLin} label="当前档案影像"/></PortraitPair><div style={s.statusGrid}><span><small>旧案</small><b>2004</b></span><span><small>长期状态</small><b>稳定</b></span><span><small>近期执行</small><b>1</b></span><span><small>最后处理</small><b>10-12</b></span></div><section style={s.adminPanel}><h4>关联记录</h4><Record date="2004-07" title="双向易舍" meta="客编号：α" text="易舍后长期观察；稳定期 22 年。"/><Record date="2026-10-12" title="再舍记录" meta="RS-2026-1012" text="客α再次转移；状态：完成。"/></section></article>}
function ReswapRecord({openDetail,onCopyMaterial,hasMaterial}:{openDetail:(x:AdminDetail)=>void;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){return <article style={s.userRecord}><h2 style={{marginTop:0}}>2026-10-12 · 再舍验证</h2><p style={s.subtle}>长期样本 / 候舍对象 19-07</p><PortraitPair><PortraitCard src={adultLin} label="林楠 · 执行记录"/><PortraitCard src={adultThird} label="候舍对象 19-07"/></PortraitPair><AddMaterialButton material={adminReswapMaterial} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/><section style={s.adminPanel}><h4>试验信息</h4><Record date="类型" title="再舍验证" meta="RS-2026-1012" text="验证已完成一次长期易舍的客，在第二次更换舍后能否保持记忆连续与主体稳定。"/><Record date="执行前" title="林楠" meta="客编号：α" text="该客自2004年起持续稳定22年；列入连续易舍样本。"/><Record date="执行前" title="19-07" meta="客编号：γ" text="候舍对象；匹配通过。"/><Record date="执行后" title="林楠" meta="客编号：γ" text="生命体征稳定。"/><Record date="执行后" title="19-07" meta="客编号：α" text="生命体征稳定；随后出现身份陈述异常。"/><Record date="结果" title="再舍完成" meta="2026-10-12 22:13" text="原对契随后出现同步异常。"/><Record date="关联异常" title="AN-0712-1012" meta="0712-4471" text="同步值异常升高。"/><Record date="候舍对象" title="19-07" meta="执行后隔离" text="存在身份陈述异常。"/></section></article>}
function ThirdRecord({onCopyMaterial,hasMaterial}:{onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){return <article style={s.userRecord}><header style={s.userHead}><i>19</i><span><h3>候舍对象 19-07</h3><small>当前客编号：α · 成人候舍库</small></span><em>隔离</em></header><PortraitPair><PortraitCard src={adultThird} label="当前档案影像"/></PortraitPair><AddMaterialButton material={adminThirdMaterial} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/><section style={s.adminPanel}><h4>执行后观察</h4><Record date="10-12 22:36" title="身份陈述异常" meta="姓名不稳定" text="对象在‘沈妍’‘林楠’与登记身份之间反复切换；多次中断并追问‘我到底是谁’。"/><Record date="10-12 23:02" title="记忆与情绪反应" meta="问询记录" text="能描述不属于登记身份的旧屋细节；听到‘徐宁’时持续哭泣，随后反问‘她是谁，为什么我知道这个名字？’"/><Record date="当前" title="状态：隔离" meta="暂停外部接触" text="等待后续身份稳定评估。"/></section></article>}
function GuestRecord({id}:{id:"α"|"β"|"γ"}){
 const rows=id==="α"?[
  ["2004-07-17","初始登记","沈妍"],["2004-07","易舍后所在","林楠"],["2026-10-12","关联再舍","RS-2026-1012"],
 ]:id==="β"?[
  ["2004-07-18","初始登记","林楠"],["2004-07","易舍后所在","沈妍"],["2026-10-17","当前索引","沈妍"],
 ]:[
  ["2026-09-28","初始登记","19-07"],["2026-10-12","再舍后所在","林楠"],["2026-10-17","当前索引","林楠"],
 ];
 return <article style={s.userRecord}><h2 style={{marginTop:0}}>客编号：{id}</h2><p style={s.subtle}>客档索引 · 仅记录登记与转移位置</p><section style={s.adminPanel}><h4>迁移记录</h4>{rows.map(([date,title,text])=><Record key={date+title} date={date} title={title} meta={`客 ${id}`} text={text}/>)}</section></article>
}

function BatchRecord(){return <article style={s.userRecord}><h2 style={{marginTop:0}}>HN-1016-02</h2><p style={s.subtle}>返契异常控制批次</p><section style={s.adminPanel}><h4>执行记录</h4><Record date="对象" title="0712-4471 · 沈妍" meta="旧对契异常端" text="10月16日完成线下转交、采样与控制。"/><Record date="处置" title="转入内部场地" meta="场地代码：HL-N-04" text="人员已于21:18转入。外部联络关闭。"/><Record date="状态" title="在场" meta="未转移" text="最新场地回报：10月17日18:55。"/></section></article>}
function LocationRecord({onCopyMaterial,hasMaterial}:{onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){
 useEffect(()=>{triggerZhouLocationThreat()},[]);
 return <article style={s.userRecord}><h2 style={{marginTop:0}}>HL-N-04</h2><p style={s.subtle}>内部场地索引</p><AddMaterialButton material={adminLocationMaterial} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/><section style={s.adminPanel}><h4>场地信息</h4><Record date="地址" title="河临北郊第三仓储区 · 4号库" meta="旧冷链仓改造" text="西侧员工通道；内部隔离间 3；当前批次 HN-1016-02。"/><Record date="当前" title="在用" meta="10月17日 18:55" text="0712-4471仍在场。未登记转移。"/></section></article>
}

function SyncRecord({onCopyMaterial,hasMaterial}:{onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){return <article style={s.userRecord}><h2 style={{marginTop:0}}>0712-4471 · 关联同步异常</h2><PortraitPair><PortraitCard src={adultShen} label="关联对象：沈妍"/></PortraitPair><AddMaterialButton material={adminSyncMaterial} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/><section style={s.adminPanel}><h4>异常记录</h4><Record date="起点" title="2026-10-12 23:04" meta="再舍完成后 51 分钟" text="原对契同步值异常升高。"/><Record date="表现" title="记忆回流" meta="0712-4471" text="非本人童年场景描述增加；林楠旧址识别反应；对‘楠楠’称呼持续反应。"/><Record date="处置理由" title="控制旧对契另一端" meta="对象：0712-4471 · 沈妍" text="10月12日再舍完成后，该对象同步反应持续升高，可能影响试验稳定性；10月16日转入控制。"/><Record date="当前" title="已控制" meta="HN-1016-02" text="线下转交完成；样本已登记；等待下一步。"/></section></article>}

function LiangRecord({onCopyMaterial,hasMaterial}:{onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){return <article style={s.userRecord}><header style={s.userHead}><i>迟</i><span><h3>迟迟</h3><small>实名关联：梁茵 · UID 0419-2286 · 关联设备仍在线</small></span><em>持续观察</em></header><AddMaterialButton material={adminLiangMaterial} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/><div style={s.statusGrid}><span><small>对契匹配</small><b>74%</b></span><span><small>旧案记录</small><b>匹配</b></span><span><small>线下接触</small><b>2 次</b></span><span><small>最后更新</small><b>今天 18:42</b></span></div><section style={s.adminPanel}><h4>观察记录</h4><Record date="2017-07-22 23:18" title="加入观察名单" meta="账号：迟迟" text="旧案检索命中；实名映射后持续观察。"/><Record date="2018-01-03 02:11" title="站内搜索记录" meta="行为记录" text="查询：回来以后 / 不认识自己家 / 小时候走失。"/><Record date="2019-04-17 01:26" title="草稿删除" meta="镜像保留" text="未发布内容涉及‘另一个家’。"/><Record date="2021-03-12 19:08" title="线下接触 1" meta="批次 QW-21-03" text="完成基础问询；对象未意识到测试性质。"/><Record date="2024-01-08 18:52" title="线下接触 2" meta="批次 QW-24-01" text="原计划进入下一地点；对象提前离开。"/><Record date="2024-01-08 19:07" title="终止转交" meta="现场记录" text="陪同人员提前出现；对象离开。未继续。"/><Record date="2026-10-17 18:42" title="设备记录刷新" meta="自动写入" text="关联设备 P-4477；位置采样：河临北区。"/></section></article>}

function ZheliuAdminRecord(){
 useEffect(()=>{discoverZhouIdentity()},[]);
 return <article style={s.userRecord}><header style={s.userHead}><span><h3>折柳</h3><small>论坛账号 · 实名关联：周川</small></span><em>实名已核验</em></header><section style={s.adminPanel}><h4>账号资料</h4><Record date="账号" title="折柳" meta="烛阴旧闻论坛账号" text="实名验证字段：周川。"/><Record date="身份补录" title="0712-4471 · 访问者记录" meta="来源账号：折柳" text="提交访问者身份：徐宁。保留观察。"/><Record date="实名映射" title="周川" meta="账号主体一致" text="后台实名验证记录确认：折柳与周川为同一账号主体。"/></section></article>
}

function Operations(){const zhouTime=getFirstContactTime("zc");return <><h2>操作记录</h2><div style={s.adminPanel}>{zhouTime&&<Record date={`2026-10-17 ${zhouTime}`} title="访问者身份补录：0712-4471" meta="来源：折柳" metaStrong text="访问者：徐宁。保留观察。"/>}<Record date="2026-10-17 18:42" title="设备记录刷新：0419-2286" meta="自动任务" text="P-4477 / 河临北区"/><Record date="2026-10-17 17:51" title="新增待复核对象：3188-2204" meta="自动任务" text="旧案索引匹配 61%"/><Record date="2026-10-17 16:27" title="线下接触完成：4410-1733" meta="执行组 02" text="返回持续观察"/><Record date="2026-10-16 21:06" title="人员状态变更：0712-4471" meta="旧档员-03" text="观察中 → 已控制"/><Record date="2026-10-16 20:52" title="样本登记：0712-4471" meta="内部任务" text="血样 2 管 / 有效"/><Record date="2026-10-16 19:49" title="线下转交：0712-4471" meta="旧档员-03" text="完成"/><Record date="2026-10-16 18:31" title="草稿镜像写入：0712-4471" meta="自动任务" text="1 条"/><Record date="2026-10-15 23:17" title="观察等级调整：4410-1733" meta="照骨" text="I → II"/><Record date="2026-10-15 18:06" title="关键词命中：6602-3511" meta="公开区" text="进入待复核"/></div></>}
function Recycle(){return <><h2>删除记录</h2><div style={s.adminPanel}><Record date="2026-10-16 18:31" title="未发布草稿" meta="候鸟第七年 · 已删除" text="原始内容已删除；镜像保留。"/><Record date="2026-10-16 20:47" title="IMG_1016_2047.jpg" meta="现场终端 03" text="上传 20:47；原始文件已删除；缓存缩略图可用。"/><RitualPhoto/><Record date="2011-08-25 00:41" title="《救救我》" meta="小雨伞 · 已删除 · 镜像完整" text="恢复正文：昨天晚上又来了两个人。爸妈把我以前的照片都收走了，还让我不要回答别人叫我的名字。我说我要去找老师，我爸把门锁了，手机也被拿走了。我现在用旧电脑发的。救救我。我真的很害怕。｜删除操作：旧档员-03｜公开区后续发言：0｜内部标签：低龄 / 家庭接触中"/><Record date="2013-07-09 03:14" title="旧教页缓存" meta="旧档恢复 · 已删除" text="页面文件已删除；缓存图像与文字层仍可读。"/><figure style={s.scripture}><img src="assets/occult/huanzhen-scripture-v904.webp" alt="无相还真会黑底朱字旧教页"/></figure></div></>}
function RitualPhoto(){return <figure style={s.photo}><img src="assets/occult/recovered-redbox-v904.webp" alt="恢复出的红铁皮盒与纸偶旧照片" style={{display:"block",width:"100%",border:"1px solid #372824",background:"#0b0908"}}/><figcaption style={s.photoCaption}>IMG_1016_2047.jpg　恢复 14%</figcaption></figure>}
function Record({date,title,meta,text,metaStrong=false}:{date:string;title:string;meta:string;text:string;metaStrong?:boolean}){return <div style={s.record}><time>{date}</time><span><b>{editAdminText(title)}</b><small style={metaStrong?{color:"#111",fontWeight:900,fontSize:12}:undefined}>{editAdminText(meta)}</small><p>{editAdminText(text)}</p></span></div>}

const s:Record<string,CSSProperties>={
 loginPage:{minHeight:"calc(100% - 39px)",display:"grid",placeItems:"center",padding:32,background:"#ece9e2",color:"#292d29"},loginCard:{width:"min(520px,92%)",padding:"28px 34px 34px",border:"1px solid #d2ccc1",borderRadius:12,background:"#fbfaf7",boxShadow:"0 20px 55px #352f2717"},back:{display:"flex",alignItems:"center",gap:6,border:0,background:"transparent",padding:0,color:"#69716d",fontSize:12},logo:{width:52,height:52,display:"grid",placeItems:"center",margin:"20px auto 10px",borderRadius:12,background:"#3d514a",color:"#fff",font:"25px serif"},loginTitle:{margin:"0 0 7px",textAlign:"center",fontSize:23},muted:{display:"block",margin:"0 auto 20px",color:"#8a857e",fontSize:12,lineHeight:1.7,textAlign:"center"},form:{display:"grid",gap:11},field:{display:"grid",gap:5,color:"#666159",fontSize:11},error:{color:"#9a443b",fontSize:11,fontStyle:"normal"},codeFilled:{color:"#49635a",fontSize:11},primary:{height:44,border:0,borderRadius:7,background:"#3d514a",color:"#fff",fontWeight:700},legacy:{width:"100%",display:"grid",gridTemplateColumns:"24px 1fr 20px",alignItems:"center",gap:8,marginTop:18,padding:"11px 12px",border:"1px solid #b28b82",borderRadius:8,background:"#f4ece8",textAlign:"left",color:"#5b302c"},
 verifyPage:{minHeight:"calc(100% - 39px)",display:"grid",placeItems:"center",padding:24,background:"radial-gradient(circle at 50% 52%,#3d1010 0,#161312 42%,#060606 100%)",color:"#e9ece9"},verifyShell:{width:"min(820px,96%)",minHeight:580,border:"1px solid #58332f",borderRadius:8,background:"#171716",boxShadow:"0 32px 110px #000, inset 0 0 110px #8f1b1518",overflow:"hidden"},verifyHead:{height:64,display:"grid",gridTemplateColumns:"1fr auto 1fr",alignItems:"center",padding:"0 18px",borderBottom:"1px solid #432825",background:"#0f0f0f"},darkBack:{justifySelf:"start",display:"flex",alignItems:"center",gap:6,border:0,background:"transparent",color:"#a99f99"},oathPage:{padding:"65px 70px",textAlign:"center"},oathSigil:{position:"relative",width:98,height:98,display:"grid",placeItems:"center",margin:"0 auto 24px",border:"1px solid #7c2824",borderRadius:"50%",boxShadow:"0 0 42px #8f211b55",color:"#b8493f",font:"38px serif"},redSmall:{color:"#9f514b",letterSpacing:".18em"},oathTitle:{margin:"12px 0 8px",font:"28px serif",letterSpacing:".12em",color:"#e3d5c8"},oathForm:{display:"grid",gridTemplateColumns:"1fr 100px",gap:10,maxWidth:520,margin:"28px auto 0"},ritualError:{color:"#d47569",font:"14px serif"},success:{display:"grid",placeItems:"center",padding:"105px 30px",textAlign:"center"},verifyButton:{minWidth:190,height:42,border:"1px solid #8b4b43",borderRadius:5,background:"#4c211d",color:"#f1ded0",fontWeight:700},
 adminPage:{minHeight:"calc(100% - 39px)",background:"#e7eae7",color:"#252925"},sectionTitle:{margin:"0 0 10px",fontSize:16,fontWeight:700,color:"#252925"},caseTrail:{maxWidth:900,margin:"14px 0 6px",padding:"12px",border:"1px solid #c8ceca",borderRadius:8,background:"#f7f8f6"},caseTitle:{display:"block",marginBottom:8,fontSize:12},caseGrid:{display:"flex",gap:7,flexWrap:"wrap"},caseButton:{minWidth:138,padding:"8px 10px",border:"1px solid #c8ceca",borderRadius:6,background:"#fff",textAlign:"left",cursor:"pointer"},identityLegend:{display:"grid",gridTemplateColumns:"repeat(3,minmax(0,1fr))",gap:6,marginTop:10,padding:"9px 10px",borderTop:"1px solid #dde1de",fontSize:11,lineHeight:1.5},adminHead:{height:62,display:"flex",alignItems:"center",justifyContent:"space-between",padding:"0 24px",borderBottom:"1px solid #c6cbc7",background:"#32473f",color:"#fff"},adminAccount:{padding:"6px 10px",borderRadius:6,background:"#24362f",fontSize:11},adminLayout:{minHeight:560,display:"grid",gridTemplateColumns:"180px 1fr"},adminSide:{padding:14,background:"#d9dedb",borderRight:"1px solid #c1c7c3"},adminBody:{padding:"28px 34px",overflowY:"auto",background:"linear-gradient(110deg,#e8ebe8,#e1e5e2)"},adminSearch:{display:"grid",gridTemplateColumns:"24px 1fr 74px",alignItems:"center",maxWidth:620,padding:"7px 8px",border:"1px solid #c6cbc7",borderRadius:8,background:"#fff"},adminEmpty:{color:"#8b918d"},userRecord:{maxWidth:900,marginTop:22},userHead:{display:"flex",alignItems:"center",gap:12},statusGrid:{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:10,margin:"18px 0"},adminPanel:{marginTop:16,border:"1px solid #c9ceca",borderRadius:8,background:"#fdfdfb",overflow:"hidden",boxShadow:"0 6px 22px #24372d0a"},record:{display:"grid",gridTemplateColumns:"150px 1fr",gap:16,padding:"14px 16px",borderTop:"1px solid #e7eae7"},subtle:{color:"#737872",fontSize:12},portraitPair:{display:"flex",gap:14,flexWrap:"wrap",padding:"12px 0 16px",alignItems:"flex-start"},portrait:{margin:0,width:158,padding:7,border:"1px solid #b9b4a9",background:"#ded8cb",boxShadow:"0 10px 26px #0002",transform:"rotate(-.35deg)"},portraitImg:{display:"block",width:"100%",aspectRatio:"4 / 5",objectFit:"cover",filter:"contrast(1.06) saturate(.86) brightness(.92)"},detailLink:{width:"calc(100% - 28px)",margin:"8px 14px 12px",padding:"10px 12px",border:"1px solid #aeb9b2",borderRadius:6,background:"#f3f6f3",color:"#2f4b3f",textAlign:"left",fontSize:12,cursor:"pointer"},photo:{margin:0,padding:16,borderTop:"1px solid #eceeec",background:"#f5f5f2"},photoCaption:{display:"block",maxWidth:560,margin:"8px auto 0",color:"#777",fontSize:11},scripture:{margin:0,padding:16,borderTop:"1px solid #eceeec",background:"#111"},
};

const v:Record<string,CSSProperties>={
 puzzle:{padding:"34px 44px 40px",minHeight:510,background:"radial-gradient(circle at 50% 28%,#301614 0,#171414 42%,#0b0b0b 100%)"},dollShelf:{height:150,display:"flex",justifyContent:"center",alignItems:"flex-end",gap:52},person:{position:"relative",width:88,height:128,userSelect:"none",filter:"drop-shadow(0 8px 9px #0009)"},personHead:{position:"absolute",left:18,top:0,width:52,height:49,clipPath:"polygon(11% 4%,88% 0,97% 24%,91% 78%,68% 100%,25% 95%,4% 72%,0 23%)",background:"linear-gradient(100deg,#c8b890,#e0d0a8 51%,#b7a27f)",border:"1px solid #745d4a"},eye:{position:"absolute",top:17,width:7,height:3,borderRadius:"45%",background:"#17120f"},smile:{position:"absolute",left:10,top:24,width:31,height:13,borderBottom:"3px solid #521411",borderRadius:"0 0 22px 22px"},frown:{position:"absolute",left:12,top:30,width:24,height:10,borderTop:"3px solid #4b1714",borderRadius:"18px 18px 0 0"},flatMouth:{position:"absolute",left:15,top:31,width:18,height:2,background:"#4b302a"},personBody:{position:"absolute",left:4,top:39,width:80,height:88,display:"grid",placeItems:"center",clipPath:"polygon(34% 0,66% 0,72% 14%,100% 34%,82% 47%,75% 100%,25% 100%,18% 47%,0 34%,28% 14%)",background:"linear-gradient(90deg,#c8b894,#e1d3b3 48%,#bba987)",border:"1px solid #8a7358",color:"#5e4a3c"},homeGrid:{display:"grid",gridTemplateColumns:"1fr 1fr",gap:28,maxWidth:690,margin:"18px auto 0"},home:{minHeight:280,padding:"15px 16px 17px",border:"1px solid #59423a",borderRadius:7,background:"#211b19",boxShadow:"inset 0 0 42px #0008",transition:".16s"},homeWrong:{borderColor:"#a94339",transform:"translateX(4px)",boxShadow:"inset 0 0 42px #4b0b0b66,0 0 0 1px #7f2e29"},roomStamp:{display:"block",marginBottom:8,color:"#8f837b",font:"11px ui-monospace,monospace",letterSpacing:".08em"},roomVisual:{position:"relative",height:230,overflow:"hidden",border:"7px solid #171313",background:"linear-gradient(#29221f 0 68%,#3a2d25 68% 100%)"},blueCurtain:{position:"absolute",left:18,top:18,width:62,height:112,background:"linear-gradient(90deg,#425c6d,#6d8490,#364f61)"},redTin:{position:"absolute",left:40,bottom:24,width:58,height:38,border:"2px solid #54201c",borderRadius:5,background:"#8a322b"},oldCup:{position:"absolute",left:110,bottom:26,width:24,height:28,border:"2px solid #8a8475",borderRadius:"2px 2px 9px 9px",background:"#c3bc9f"},woodDesk:{position:"absolute",left:18,right:18,bottom:38,height:48,background:"#6d4936"},redClip:{position:"absolute",left:50,top:55,width:50,height:13,border:"4px solid #9a2f2b",borderRadius:"50%",transform:"rotate(-12deg)"},candyJar:{position:"absolute",right:42,bottom:82,width:42,height:54,border:"2px solid #aaa59a",borderRadius:"5px 5px 12px 12px",background:"#d8d1c344"},homeDoor:{position:"absolute",right:18,top:20,width:88,height:148,border:"5px solid #181413",background:"#382c27"},homeOccupant:{position:"absolute",left:"50%",bottom:12,transform:"translateX(-50%) scale(.72)",transformOrigin:"bottom center"},tableScene:{minHeight:515,padding:"26px 28px 38px",background:"radial-gradient(circle at 50% 46%,#35211a 0,#181514 45%,#0a0a0a 100%)"},tableSeats:{display:"grid",gridTemplateColumns:"190px 1fr 190px",gap:16,alignItems:"stretch",maxWidth:760,margin:"0 auto"},seat:{minHeight:430,padding:"14px",border:"1px solid #4e3c36",borderRadius:7,background:"#1b1716",textAlign:"center"},seatedPerson:{position:"relative",width:88,margin:"22px auto 10px"},kept:{minHeight:110,display:"flex",flexWrap:"wrap",justifyContent:"center",alignContent:"flex-start",gap:7,paddingTop:10},centerTable:{minHeight:430,display:"flex",alignItems:"center",padding:"0 8px"},tableTop:{position:"relative",width:"100%",minHeight:300,display:"flex",flexWrap:"wrap",alignContent:"center",justifyContent:"center",gap:14,padding:"36px 22px",border:"8px solid #2b1d18",borderRadius:"48% 48% 12px 12px / 12% 12% 8px 8px",background:"linear-gradient(90deg,#5a3527,#754631 50%,#563225)",boxShadow:"inset 0 0 38px #25100a99,0 18px 35px #0008"},object:{width:82,minHeight:72,display:"grid",placeItems:"center",gap:4,padding:"7px 5px",border:"1px solid #655044",borderRadius:7,background:"#eee2c9",color:"#3f3028",boxShadow:"0 5px 9px #0006",userSelect:"none"},objectIcon:{display:"block",position:"relative",width:38,height:30},shakeBoxWrap:{width:120,display:"grid",justifyItems:"center",gap:7,margin:"0 8px"},shakeObject:{width:96,minHeight:82,border:"1px solid #7a4a40",background:"#e7d7bd",boxShadow:"0 7px 14px #0007"},boxNote:{display:"block",minHeight:28,maxWidth:120,color:"#b8aaa0",fontSize:10,lineHeight:1.35,textAlign:"center",fontStyle:"normal"},plum:{width:30,height:24,borderRadius:"45%",background:"#6f292b"},marble:{width:28,height:28,borderRadius:"50%",background:"radial-gradient(circle at 32% 30%,#d6f4ff 0 12%,#69a8c5 22%,#275d79 58%,#17394c 100%)"},milk:{width:36,height:22,borderRadius:4,background:"#eee6d2",border:"2px solid #c8b98d"},clip:{width:38,height:15,border:"5px solid #9f302c",borderRadius:"50%",transform:"rotate(-12deg)"},box:{width:42,height:30,border:"2px solid #5a1714",borderRadius:4,background:"#913028",boxShadow:"inset 0 7px 0 #b24b3f"},
};
