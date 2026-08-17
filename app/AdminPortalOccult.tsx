"use client";

import {FormEvent,useMemo,useState} from "react";
import {ArrowLeft,ChevronRight,LockKeyhole,Search,ShieldCheck} from "lucide-react";

export const ADMIN_USER="旧档员-03";
export const ADMIN_TEMP_CODE="gumen-0712";
const OLD_OATH="身非我身名非我名";

type Props={loggedIn:boolean;onAdminLogin:()=>void;onCancel:()=>void;canUseLegacy:boolean};

const normalize=(v:string)=>v.replace(/[，。、“”‘’\s]/g,"");

export default function AdminPortalOccult({loggedIn,onAdminLogin,onCancel,canUseLegacy}:Props){
 const [mode,setMode]=useState<"login"|"verify">("login");
 const [user,setUser]=useState("");
 const [pwd,setPwd]=useState("");
 const [error,setError]=useState("");
 const [attemptedAdmin,setAttemptedAdmin]=useState(false);
 const [filled,setFilled]=useState(false);

 if(loggedIn)return <AdminDesk/>;

 const submit=(e:FormEvent)=>{
  e.preventDefault();
  if(user.trim()===ADMIN_USER&&pwd===ADMIN_TEMP_CODE){onAdminLogin();setError("");return;}
  if(user.trim()===ADMIN_USER){setAttemptedAdmin(true);setError("账号或密码错误。");return;}
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
   <p style={s.muted}>当前浏览器保存了一个已登录会话。也可以使用其他账号登录。</p>
   <form onSubmit={submit} style={s.form}>
    <label style={s.field}><span>账号</span><input value={user} onChange={e=>{setUser(e.target.value);setError("");setAttemptedAdmin(false)}} autoComplete="off" placeholder="用户名"/></label>
    <label style={s.field}><span>密码</span><input type="password" value={pwd} onChange={e=>{setPwd(e.target.value);setError("")}} autoComplete="off" placeholder="密码"/></label>
    {error&&<em style={s.error}>{error}</em>}
    {filled&&<small style={s.codeFilled}>旧档验证生成的临时口令已填入。</small>}
    <button style={s.primary}>登录</button>
   </form>
   {attemptedAdmin&&user.trim()===ADMIN_USER&&canUseLegacy&&<button onClick={()=>setMode("verify")} style={s.legacy}>
    <LockKeyhole size={15}/><span><b>旧档账号验证</b><small>检测到迁移账号 · 使用兼容认证</small></span><ChevronRight size={15}/>
   </button>}
  </section>
 </main>;
}

function LegacyVerify({onBack,onVerified}:{onBack:()=>void;onVerified:()=>void}){
 type Child="lin"|"shen";
 type Home="factory"|"qingwu";
 type Item="plum"|"marble"|"milk"|"clip"|"box";
 const [stage,setStage]=useState(0);
 const [oath,setOath]=useState("");
 const [error,setError]=useState("");
 const [dragChild,setDragChild]=useState<Child|null>(null);
 const [homes,setHomes]=useState<Partial<Record<Home,Child>>>({});
 const [wrongHome,setWrongHome]=useState<Home|null>(null);
 const [dragItem,setDragItem]=useState<Item|null>(null);
 const [items,setItems]=useState<Partial<Record<Item,Child|"center">>>({});
 const [moods,setMoods]=useState<Record<Child,"neutral"|"frown"|"smile">>({lin:"neutral",shen:"neutral"});

 const childInfo:Record<Child,{stamp:string}>={lin:{stamp:"07·18"},shen:{stamp:"07·17"}};
 const homeAnswer:Record<Home,Child>={factory:"lin",qingwu:"shen"};
 const itemAnswer:Record<Exclude<Item,"box">,Child>={plum:"lin",marble:"lin",milk:"shen",clip:"shen"};
 const ordinaryItems:(Exclude<Item,"box">)[]=["plum","marble","milk","clip"];
 const allOrdinaryPlaced=(next=items)=>ordinaryItems.every(id=>!!next[id]);
 const completeTable=(nextItems:Partial<Record<Item,Child|"center">>)=>{
  if(allOrdinaryPlaced(nextItems)&&nextItems.box==="center")window.setTimeout(()=>setStage(3),1100);
 };
 const placeChild=(home:Home)=>{
  if(!dragChild)return;
  if(homeAnswer[home]!==dragChild){setWrongHome(home);window.setTimeout(()=>setWrongHome(null),520);return;}
  const next={...homes,[home]:dragChild};
  setHomes(next);setDragChild(null);
  if(next.factory&&next.qingwu)window.setTimeout(()=>setStage(2),900);
 };
 const frown=(child:Child)=>{
  setMoods(m=>({...m,[child]:"frown"}));
  window.setTimeout(()=>setMoods(m=>({...m,[child]:"neutral"})),680);
 };
 const giveItem=(target:Child|"center")=>{
  if(!dragItem)return;
  const id=dragItem;
  if(id==="box"){
   if(target==="center"){
    const next={...items,box:"center" as const};
    setItems(next);setMoods({lin:"neutral",shen:"neutral"});setDragItem(null);completeTable(next);return;
   }
   const other:Child=target==="lin"?"shen":"lin";
   setMoods(m=>({...m,[target]:"neutral",[other]:"smile"}));
   setDragItem(null);
   window.setTimeout(()=>setMoods(m=>({...m,[other]:"neutral"})),850);
   return;
  }
  if(target==="center"){setDragItem(null);return;}
  if(itemAnswer[id]===target){
   const next={...items,[id]:target};
   setItems(next);setDragItem(null);completeTable(next);return;
  }
  setDragItem(null);frown(target);
 };
 const progress=stage===0?"旧誓":stage===1?"1 / 2":stage===2?"2 / 2":"完成";

 return <main style={s.verifyPage}>
  <section style={s.verifyShell}>
   <header style={s.verifyHead}><button onClick={onBack} style={s.darkBack}><ArrowLeft size={15}/>返回登录</button><span><small>旧档账号验证</small><b>兼容认证</b></span><em>{progress}</em></header>

   {stage===0&&<div style={s.oathPage}>
    <div style={s.oathSigil}><span>門</span><i/></div>
    <small style={s.redSmall}>迁移账号 · 旧誓核验</small>
    <h2 style={s.oathTitle}>请录入旧誓</h2>
    <form onSubmit={e=>{e.preventDefault();if(normalize(oath)===OLD_OATH){setStage(1);setError("")}else setError(oath.trim()?"旧誓不合。":"请录入旧誓。")}} style={s.oathForm}>
     <input autoFocus value={oath} onChange={e=>{setOath(e.target.value);setError("")}} placeholder="旧誓" autoComplete="off"/>
     <button>确认</button>
    </form>
    {error&&<p style={s.ritualError}>{error}</p>}
   </div>}

   {stage===1&&<div style={v.puzzle}>
    <div style={v.dollShelf}>
     {(["lin","shen"] as Child[]).filter(id=>!Object.values(homes).includes(id)).map(id=><PaperPerson key={id} stamp={childInfo[id].stamp} mood="smile" draggable onDragStart={()=>setDragChild(id)}/>) }
    </div>
    <div style={v.homeGrid}>
     <HomeRoom kind="factory" wrong={wrongHome==="factory"} onDrop={()=>placeChild("factory")}>{homes.factory&&<PaperPerson stamp={childInfo[homes.factory].stamp} mood="neutral"/>}</HomeRoom>
     <HomeRoom kind="qingwu" wrong={wrongHome==="qingwu"} onDrop={()=>placeChild("qingwu")}>{homes.qingwu&&<PaperPerson stamp={childInfo[homes.qingwu].stamp} mood="neutral"/>}</HomeRoom>
    </div>
   </div>}

   {stage===2&&<div style={v.tableScene}>
    <div style={v.tableSeats}>
     <TableSeat place="4栋东侧" mood={moods.lin} side="left" onDrop={()=>giveItem("lin")} items={ordinaryItems.filter(id=>items[id]==="lin")}/>
     <div style={v.centerTable} onDragOver={e=>e.preventDefault()} onDrop={()=>giveItem("center")}>
      <div style={v.tableTop}>
       {(["plum","marble","milk","clip","box"] as Item[]).filter(id=>!items[id]).map(id=><ObjectToken key={id} id={id} draggable onDragStart={()=>setDragItem(id)}/>) }
       {items.box==="center"&&<ObjectToken id="box" opened/>}
      </div>
     </div>
     <TableSeat place="青梧旧楼" mood={moods.shen} side="right" onDrop={()=>giveItem("shen")} items={ordinaryItems.filter(id=>items[id]==="shen")}/>
    </div>
   </div>}

   {stage===3&&<div style={s.success}>
    <ShieldCheck size={34}/>
    <small>验证完成</small>
    <h2>旧档账号临时口令</h2>
    <code>{ADMIN_TEMP_CODE}</code>
    <p>临时口令仅用于本次旧档认证。</p>
    <button onClick={onVerified} style={s.verifyButton}>返回登录并填入口令</button>
   </div>}
  </section>
 </main>;
}

function PaperPerson({stamp,mood,draggable,onDragStart}:{stamp:string;mood:"smile"|"neutral"|"frown";draggable?:boolean;onDragStart?:()=>void}){
 return <div draggable={draggable} onDragStart={e=>{e.dataTransfer.effectAllowed="move";onDragStart?.()}} style={{...v.person,cursor:draggable?"grab":"default"}}>
  <div style={v.personHead}><i style={{...v.eye,left:16}}/><i style={{...v.eye,right:16}}/><span style={mood==="smile"?v.smile:mood==="frown"?v.frown:v.flatMouth}/></div>
  <div style={v.personBody}><b>{stamp}</b></div>
 </div>
}

function HomeRoom({kind,wrong,onDrop,children}:{kind:"factory"|"qingwu";wrong:boolean;onDrop:()=>void;children:React.ReactNode}){
 const factory=kind==="factory";
 return <section onDragOver={e=>e.preventDefault()} onDrop={onDrop} style={{...v.home,...(wrong?v.homeWrong:{})}}>
  <small style={v.roomStamp}>{factory?"4栋东侧":"青梧旧楼"}</small>
  <div style={v.roomVisual}>
   {factory?<><span style={v.blueCurtain}/><i style={v.redTin}/><em style={v.oldCup}/></>:<><span style={v.woodDesk}/><i style={v.redClip}/><em style={v.candyJar}/></>}
   <div style={v.homeDoor}/>
   <div style={v.homeOccupant}>{children}</div>
  </div>
 </section>
}

function TableSeat({place,mood,side,onDrop,items}:{place:string;mood:"neutral"|"frown"|"smile";side:"left"|"right";onDrop:()=>void;items:string[]}){
 return <section onDragOver={e=>e.preventDefault()} onDrop={onDrop} style={v.seat}>
  <small style={v.roomStamp}>{place}</small>
  <div style={v.seatedPerson}>
   <PaperPerson stamp={side==="left"?"07·18":"07·17"} mood={mood}/>
  </div>
  <div style={v.kept}>{items.map(id=><ObjectToken key={id} id={id}/>)}</div>
 </section>
}

function ObjectToken({id,draggable,onDragStart,opened}:{id:string;draggable?:boolean;onDragStart?:()=>void;opened?:boolean}){
 const labels:Record<string,string>={plum:"话梅糖",marble:"蓝玻璃弹珠",milk:"奶糖",clip:"红色发卡",box:"红铁皮盒"};
 return <div draggable={draggable} onDragStart={e=>{e.dataTransfer.effectAllowed="move";onDragStart?.()}} style={{...v.object,cursor:draggable?"grab":"default"}}>
  <i style={{...v.objectIcon,position:"relative",...(id==="plum"?v.plum:id==="marble"?v.marble:id==="milk"?v.milk:id==="clip"?v.clip:v.box)}}>{id==="box"&&opened&&<span style={{position:"absolute",left:1,right:1,top:-7,height:7,border:"1px solid #704236",borderBottom:0,background:"#7d2b23",transform:"rotate(-7deg)",transformOrigin:"left bottom",boxShadow:"0 -2px 8px #0008"}}/>}</i>
  <small>{labels[id]}</small>
 </div>
}

const v:Record<string,React.CSSProperties>={
 puzzle:{padding:"34px 44px 40px",minHeight:510,background:"radial-gradient(circle at 50% 28%,#301614 0,#171414 42%,#0b0b0b 100%)"},
 dollShelf:{height:150,display:"flex",justifyContent:"center",alignItems:"flex-end",gap:52},
 person:{position:"relative",width:88,height:128,userSelect:"none",filter:"drop-shadow(0 8px 9px #0009)"},
 personHead:{position:"absolute",left:18,top:0,width:52,height:49,clipPath:"polygon(11% 4%,88% 0,97% 24%,91% 78%,68% 100%,25% 95%,4% 72%,0 23%)",background:"linear-gradient(100deg,#c8b890,#e0d0a8 51%,#b7a27f)",border:"1px solid #745d4a",boxShadow:"inset 8px 0 15px #5b342515"},
 eye:{position:"absolute",top:17,width:7,height:3,borderRadius:"45%",background:"#17120f",boxShadow:"0 0 3px #52120f"},
 smile:{position:"absolute",left:10,top:24,width:31,height:13,borderBottom:"3px solid #521411",borderRadius:"0 0 22px 22px",transform:"rotate(1deg)",boxShadow:"0 2px 2px #5b0f0d33"},
 frown:{position:"absolute",left:12,top:30,width:24,height:10,borderTop:"3px solid #4b1714",borderRadius:"18px 18px 0 0"},
 flatMouth:{position:"absolute",left:15,top:31,width:18,height:2,background:"#4b302a"},
 personBody:{position:"absolute",left:4,top:39,width:80,height:88,display:"grid",placeItems:"center",clipPath:"polygon(34% 0,66% 0,72% 14%,100% 34%,82% 47%,75% 100%,25% 100%,18% 47%,0 34%,28% 14%)",background:"linear-gradient(90deg,#c8b894,#e1d3b3 48%,#bba987)",border:"1px solid #8a7358",color:"#5e4a3c",fontStyle:"normal"},
 homeGrid:{display:"grid",gridTemplateColumns:"1fr 1fr",gap:28,maxWidth:690,margin:"18px auto 0"},
 home:{minHeight:280,padding:"15px 16px 17px",border:"1px solid #59423a",borderRadius:7,background:"#211b19",boxShadow:"inset 0 0 42px #0008",transition:".16s"},
 homeWrong:{borderColor:"#a94339",transform:"translateX(4px)",boxShadow:"inset 0 0 42px #4b0b0b66,0 0 0 1px #7f2e29"},
 roomStamp:{display:"block",marginBottom:8,color:"#8f837b",font:"11px ui-monospace,monospace",letterSpacing:".08em"},
 roomVisual:{position:"relative",height:230,overflow:"hidden",border:"7px solid #171313",background:"linear-gradient(#29221f 0 68%,#3a2d25 68% 100%)"},
 blueCurtain:{position:"absolute",left:18,top:18,width:62,height:112,background:"linear-gradient(90deg,#425c6d,#6d8490,#364f61)",boxShadow:"inset -8px 0 0 #2c4352"},
 redTin:{position:"absolute",left:40,bottom:24,width:58,height:38,border:"2px solid #54201c",borderRadius:5,background:"#8a322b",boxShadow:"inset 0 7px 0 #aa4940"},
 oldCup:{position:"absolute",left:110,bottom:26,width:24,height:28,border:"2px solid #8a8475",borderRadius:"2px 2px 9px 9px",background:"#c3bc9f"},
 woodDesk:{position:"absolute",left:18,right:18,bottom:38,height:48,background:"#6d4936",boxShadow:"0 5px 0 #3d2a22"},
 redClip:{position:"absolute",left:50,top:55,width:50,height:13,border:"4px solid #9a2f2b",borderRadius:"50%",transform:"rotate(-12deg)"},
 candyJar:{position:"absolute",right:42,bottom:82,width:42,height:54,border:"2px solid #aaa59a",borderRadius:"5px 5px 12px 12px",background:"#d8d1c344",boxShadow:"inset 0 -16px 0 #e7dbb388"},
 homeDoor:{position:"absolute",right:18,top:20,width:88,height:148,border:"5px solid #181413",background:"#382c27",boxShadow:"inset -13px 0 0 #2b211e"},
 homeOccupant:{position:"absolute",left:"50%",bottom:12,transform:"translateX(-50%) scale(.72)",transformOrigin:"bottom center"},
 tableScene:{minHeight:515,padding:"26px 28px 38px",background:"radial-gradient(circle at 50% 46%,#35211a 0,#181514 45%,#0a0a0a 100%)"},
 tableSeats:{display:"grid",gridTemplateColumns:"190px 1fr 190px",gap:16,alignItems:"stretch",maxWidth:760,margin:"0 auto"},
 seat:{minHeight:430,padding:"14px",border:"1px solid #4e3c36",borderRadius:7,background:"#1b1716",textAlign:"center"},
 seatedPerson:{position:"relative",width:88,margin:"22px auto 10px"},
 arm:{position:"absolute",top:70,width:64,height:8,borderRadius:8,background:"#d3c19d",border:"1px solid #8b735c",zIndex:5},
 kept:{minHeight:110,display:"flex",flexWrap:"wrap",justifyContent:"center",alignContent:"flex-start",gap:7,paddingTop:10},
 centerTable:{minHeight:430,display:"flex",alignItems:"center",padding:"0 8px"},
 tableTop:{position:"relative",width:"100%",minHeight:300,display:"flex",flexWrap:"wrap",alignContent:"center",justifyContent:"center",gap:14,padding:"36px 22px",border:"8px solid #2b1d18",borderRadius:"48% 48% 12px 12px / 12% 12% 8px 8px",background:"linear-gradient(90deg,#5a3527,#754631 50%,#563225)",boxShadow:"inset 0 0 38px #25100a99,0 18px 35px #0008"},
 object:{width:82,minHeight:72,display:"grid",placeItems:"center",gap:4,padding:"7px 5px",border:"1px solid #655044",borderRadius:7,background:"#eee2c9",color:"#3f3028",boxShadow:"0 5px 9px #0006",userSelect:"none"},
 objectIcon:{display:"block",position:"relative",width:38,height:30},
 plum:{width:30,height:24,borderRadius:"45%",background:"#6f292b",boxShadow:"-12px 1px 0 -6px #c7ad78,12px 1px 0 -6px #c7ad78"},
 marble:{width:28,height:28,borderRadius:"50%",background:"radial-gradient(circle at 32% 30%,#d6f4ff 0 12%,#69a8c5 22%,#275d79 58%,#17394c 100%)",boxShadow:"inset -5px -4px 8px #0a2637"},
 milk:{width:36,height:22,borderRadius:4,background:"#eee6d2",border:"2px solid #c8b98d",boxShadow:"-10px 0 0 -5px #e0d3ab,10px 0 0 -5px #e0d3ab"},
 clip:{width:38,height:15,border:"5px solid #9f302c",borderRadius:"50%",transform:"rotate(-12deg)"},
 box:{width:42,height:30,border:"2px solid #5a1714",borderRadius:4,background:"#913028",boxShadow:"inset 0 7px 0 #b24b3f"},
};

function AdminDesk(){
 const [tab,setTab]=useState<"users"|"ops"|"recycle">("users");
 const [q,setQ]=useState("");
 const [searched,setSearched]=useState(false);
 const found=useMemo(()=>searched&&/候鸟第七年|沈妍/.test(q.trim()),[searched,q]);
 return <main style={s.adminPage}>
  <header style={s.adminHead}><div><i>烛</i><span><b>烛阴旧闻</b><small>旧档管理</small></span></div><span style={s.adminAccount}>旧档员-03</span></header>
  <div style={s.adminLayout}>
   <aside style={s.adminSide}><button className={tab==="users"?"active":""} onClick={()=>setTab("users")}>用户查询</button><button className={tab==="ops"?"active":""} onClick={()=>setTab("ops")}>操作记录</button><button className={tab==="recycle"?"active":""} onClick={()=>setTab("recycle")}>回收记录</button></aside>
   <section style={s.adminBody}>
    {tab==="users"&&<><h2>用户查询</h2><form onSubmit={e=>{e.preventDefault();setSearched(true)}} style={s.adminSearch}><Search size={16}/><input value={q} onChange={e=>{setQ(e.target.value);setSearched(false)}} placeholder="用户名 / UID"/><button>查询</button></form>{searched&&!found&&<p style={s.adminEmpty}>没有匹配用户。</p>}{found&&<UserRecord/>}</>}
    {tab==="ops"&&<Operations/>}
    {tab==="recycle"&&<Recycle/>}
   </section>
  </div>
 </main>;
}

function UserRecord(){return <article style={s.userRecord}>
 <header style={s.userHead}><i>候</i><span><h3>候鸟第七年</h3><small>UID 0712-4471 · 最后活动 2026-10-16 19:48</small></span><em>祭品已收容</em></header>
 <div style={s.statusGrid}><span><small>祭品状态</small><b>已收容</b></span><span><small>对契异常</small><b>是</b></span><span><small>血样</small><b>已取</b></span><span><small>返契准备</small><b>进行中</b></span></div>
 <section style={s.adminPanel}><h4>内部记录</h4><Record date="2026-08-22 04:12" title="归门观察" meta="记录者：照骨" text="旧客回响：高。与 age9 旧案恢复记录存在交叉。"/><Record date="2026-10-16 19:49" title="线下转接" meta="旧档员-03" text="已执行。停止公开区接触。"/><Record date="2026-10-16 21:06" title="祭品登记" meta="内部字段" text="主祭：未指定；引契血：已留；返契：待启。"/></section>
 <section style={s.adminPanel}><h4>私密主题镜像</h4><Record date="2026-06-19 03:12" title="昨晚又梦到了" meta="仅自己可见" text="红铁皮盒、蓝窗帘，还有那个听不清的称呼。"/><Record date="2026-09-11 02:08" title="9月11日，几条旧帖" meta="仅自己可见" text="名字不对、另一个家、回来以后不会以前会的东西。"/></section>
 </article>}
function Operations(){return <><h2>操作记录</h2><div style={s.adminPanel}><Record date="2026-10-16 21:06" title="祭品状态变更：候鸟第七年" meta="旧档员-03" text="待接触 → 已收容"/><Record date="2026-10-16 20:52" title="血样登记" meta="内部任务" text="引契血：已取"/><Record date="2026-10-16 19:49" title="线下转接" meta="旧档员-03" text="已执行"/><Record date="2026-08-22 04:12" title="添加归门标记" meta="照骨" text="对契异常：是；旧客回响：高"/></div></>}
function Recycle(){return <><h2>回收记录</h2><div style={s.adminPanel}><Record date="2026-10-16 18:31" title="未发布草稿" meta="候鸟第七年 · 已删除" text="照骨问的问题不是随机的。旧档员-03也反复碰过这些帖。"/><Record date="2026-10-16 20:47" title="IMG_1016_2047.jpg" meta="旧档员-03 · 原始来源字段缺失" text="标签：祭坛 / 黄符 / 纸偶 / 引契血。仅恢复缩略图。"/><RitualPhoto/><Record date="2013-07-09 03:14" title="旧教页缓存" meta="旧档恢复 · 已删除" text="黑底朱字页面，页脚重复：舍身无量。"/><figure style={s.scripture}><img src="assets/occult/huanzhen-scripture-v904.webp" alt="无相还真会黑底朱字旧教页"/></figure></div></>}
function RitualPhoto(){return <figure style={s.photo}><img src="assets/occult/recovered-redbox-v904.webp" alt="恢复出的红铁皮盒与纸偶旧照片" style={{display:"block",width:"100%",border:"1px solid #372824",background:"#0b0908"}}/><figcaption style={s.photoCaption}>IMG_1016_2047.jpg　恢复 14%</figcaption></figure>}
function Record({date,title,meta,text}:{date:string;title:string;meta:string;text:string}){return <div style={s.record}><time>{date}</time><span><b>{title}</b><small>{meta}</small><p>{text}</p></span></div>}

const s:Record<string,React.CSSProperties>={
 loginPage:{minHeight:"calc(100% - 39px)",display:"grid",placeItems:"center",padding:32,background:"#ece9e2",color:"#292d29"},loginCard:{width:"min(520px,92%)",padding:"28px 34px 34px",border:"1px solid #d2ccc1",borderRadius:12,background:"#fbfaf7",boxShadow:"0 20px 55px #352f2717"},back:{display:"flex",alignItems:"center",gap:6,border:0,background:"transparent",padding:0,color:"#69716d",fontSize:12},logo:{width:52,height:52,display:"grid",placeItems:"center",margin:"20px auto 10px",borderRadius:12,background:"#3d514a",color:"#fff",font:"25px serif"},loginTitle:{margin:"0 0 7px",textAlign:"center",fontSize:23},muted:{display:"block",margin:"0 auto 20px",color:"#8a857e",fontSize:12,lineHeight:1.7,textAlign:"center"},form:{display:"grid",gap:11},field:{display:"grid",gap:5,color:"#666159",fontSize:11},error:{color:"#9a443b",fontSize:11,fontStyle:"normal"},codeFilled:{color:"#49635a",fontSize:11},primary:{height:44,border:0,borderRadius:7,background:"#3d514a",color:"#fff",fontWeight:700},legacy:{width:"100%",display:"grid",gridTemplateColumns:"24px 1fr 20px",alignItems:"center",gap:8,marginTop:18,padding:"11px 12px",border:"1px solid #b28b82",borderRadius:8,background:"#f4ece8",textAlign:"left",color:"#5b302c"},
 verifyPage:{minHeight:"calc(100% - 39px)",display:"grid",placeItems:"center",padding:24,background:"radial-gradient(circle at 50% 52%,#3d1010 0,#161312 42%,#060606 100%)",color:"#e9ece9"},verifyShell:{width:"min(820px,96%)",minHeight:580,border:"1px solid #58332f",borderRadius:8,background:"#171716",boxShadow:"0 32px 110px #000, inset 0 0 110px #8f1b1518",overflow:"hidden"},verifyHead:{height:64,display:"grid",gridTemplateColumns:"1fr auto 1fr",alignItems:"center",padding:"0 18px",borderBottom:"1px solid #432825",background:"#0f0f0f"},darkBack:{justifySelf:"start",display:"flex",alignItems:"center",gap:6,border:0,background:"transparent",color:"#a99f99"},oathPage:{padding:"65px 70px",textAlign:"center"},oathSigil:{position:"relative",width:98,height:98,display:"grid",placeItems:"center",margin:"0 auto 24px",border:"1px solid #7c2824",borderRadius:"50%",boxShadow:"0 0 42px #8f211b55",color:"#b8493f",font:"38px serif"},redSmall:{color:"#9f514b",letterSpacing:".18em"},oathTitle:{margin:"12px 0 8px",font:"28px serif",letterSpacing:".12em",color:"#e3d5c8"},oathCopy:{color:"#8f8881",fontSize:12},oathForm:{display:"grid",gridTemplateColumns:"1fr 100px",gap:10,maxWidth:520,margin:"28px auto 0"},
 ritual:{padding:"30px 54px 42px",textAlign:"center"},blessing:{margin:"0 0 8px",color:"#a33a31",font:"700 15px serif",letterSpacing:".18em"},verse:{margin:"0",font:"18px serif",letterSpacing:".12em",color:"#e1d5c8"},altar:{position:"relative",height:190,maxWidth:560,margin:"22px auto 14px",borderBottom:"1px solid #6b332d",background:"radial-gradient(circle at 50% 46%,#6c1a1738 0,#171515 55%,#0b0b0b 100%)",overflow:"hidden"},candle:{position:"absolute",bottom:34,width:12,height:55,background:"linear-gradient(#7a1814,#a42921)",boxShadow:"0 -12px 22px #ff7a3f88",borderRadius:"3px 3px 0 0"},flame:{position:"absolute",bottom:86,width:16,height:24,borderRadius:"55% 45% 55% 45%",background:"#ffb35e",boxShadow:"0 0 20px #ff6b39",transform:"rotate(10deg)"},paperDoll:{position:"absolute",bottom:42,width:52,height:88,display:"grid",placeItems:"center",background:"#d8c9aa",clipPath:"polygon(35% 0,65% 0,72% 18%,100% 38%,82% 48%,75% 100%,25% 100%,18% 48%,0 38%,28% 18%)",color:"#781f1a",fontStyle:"normal"},threadA:{position:"absolute",left:135,right:135,top:95,height:1,background:"#8f2521",transform:"rotate(10deg)"},threadB:{position:"absolute",left:135,right:135,top:95,height:1,background:"#8f2521",transform:"rotate(-10deg)"},threadC:{position:"absolute",left:"50%",top:45,bottom:34,width:1,background:"#651b18"},altarRing:{position:"absolute",left:"50%",top:38,transform:"translateX(-50%)",width:90,height:90,border:"2px solid #7e2924",borderRadius:"50%",display:"grid",placeItems:"center",background:"#160e0dcc",boxShadow:"0 0 32px #8d241f44",color:"#ba554b"},yellowCharm:{position:"absolute",left:"50%",bottom:18,transform:"translateX(-50%)",width:66,height:104,paddingTop:8,border:"1px solid #8c6540",background:"#a7874f",color:"#641a17",font:"14px serif",boxShadow:"0 3px 20px #0008"},bloodBowl:{position:"absolute",left:"50%",bottom:4,transform:"translateX(-50%)",width:74,height:18,border:"5px solid #332721",borderRadius:"0 0 50% 50%",background:"#2c0808",boxShadow:"0 0 15px #7b171777"},ash:{position:"absolute",left:0,right:0,bottom:0,color:"#6f6258",fontSize:13},doors:{display:"grid",gridTemplateColumns:"1fr 52px 1fr",alignItems:"center",gap:12,margin:"20px auto 18px",maxWidth:630},door:{minHeight:205,padding:18,border:"1px solid #563d39",borderRadius:8,background:"#211c1b"},guestBox:{minHeight:96,display:"flex",alignItems:"center",justifyContent:"center",gap:8,padding:15,margin:"18px 0",border:"1px dashed #6a4b45",borderRadius:6},guest:{display:"inline-grid",placeItems:"center",minWidth:72,height:42,padding:"0 12px",border:"1px solid #8c6b5d",borderRadius:21,background:"#382923",color:"#ead9c8",fontStyle:"normal"},guestSelected:{boxShadow:"0 0 0 2px #b97464",background:"#5a302a"},drop:{height:34,padding:"0 12px",border:"1px solid #65443e",borderRadius:6,background:"#171413",color:"#cfc3b8"},swapMark:{fontSize:28,color:"#8d4a42"},help:{minHeight:22,color:"#978d85",fontSize:12},ritualError:{color:"#d47569",font:"14px serif"},verifyButton:{minWidth:190,height:42,border:"1px solid #8b4b43",borderRadius:5,background:"#4c211d",color:"#f1ded0",fontWeight:700},choiceRow:{display:"flex",justifyContent:"center",gap:12,marginTop:24},memoryTable:{display:"grid",gap:8,maxWidth:570,margin:"26px auto"},memoryRow:{display:"grid",gridTemplateColumns:"1fr 180px",alignItems:"center",gap:12,padding:"11px 12px",border:"1px solid #3e302d",background:"#1d1918",textAlign:"left"},success:{display:"grid",placeItems:"center",padding:"105px 30px",textAlign:"center"},afterVerse:{margin:"0 0 18px",color:"#a33a31",font:"18px serif",letterSpacing:".22em"},
 adminPage:{minHeight:"calc(100% - 39px)",background:"#ecefec",color:"#252925"},adminHead:{height:62,display:"flex",alignItems:"center",justifyContent:"space-between",padding:"0 24px",borderBottom:"1px solid #c6cbc7",background:"#32473f",color:"#fff"},adminAccount:{padding:"6px 10px",borderRadius:6,background:"#24362f",fontSize:11},adminLayout:{minHeight:560,display:"grid",gridTemplateColumns:"180px 1fr"},adminSide:{padding:14,background:"#dde2de",borderRight:"1px solid #c7ccc8"},adminBody:{padding:"28px 34px",overflowY:"auto"},adminSearch:{display:"grid",gridTemplateColumns:"24px 1fr 74px",alignItems:"center",maxWidth:620,padding:"7px 8px",border:"1px solid #c6cbc7",borderRadius:8,background:"#fff"},adminEmpty:{color:"#8b918d"},userRecord:{maxWidth:900,marginTop:22},userHead:{display:"flex",alignItems:"center",gap:12},statusGrid:{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:10,margin:"18px 0"},adminPanel:{marginTop:16,border:"1px solid #ced3cf",borderRadius:8,background:"#fff",overflow:"hidden"},record:{display:"grid",gridTemplateColumns:"150px 1fr",gap:16,padding:"14px 16px",borderTop:"1px solid #eceeec"},
 photo:{margin:0,padding:16,borderTop:"1px solid #eceeec",background:"#f5f5f2"},photoRoom:{position:"relative",height:250,maxWidth:560,margin:"0 auto",overflow:"hidden",border:"9px solid #211c19",background:"radial-gradient(circle at 50% 58%,#5d4235 0,#24201d 30%,#0d0c0b 76%)",boxShadow:"inset 0 0 75px #000"},photoCandle:{position:"absolute",bottom:42,width:9,height:66,background:"#8e2019",boxShadow:"0 -12px 22px #ff8a4e"},photoDoll:{position:"absolute",bottom:58,width:62,height:110,display:"grid",placeItems:"center",background:"#c9b998",clipPath:"polygon(35% 0,65% 0,72% 18%,100% 38%,82% 48%,75% 100%,25% 100%,18% 48%,0 38%,28% 18%)",color:"#641915",font:"700 18px serif",fontStyle:"normal"},photoGate:{position:"absolute",left:"50%",top:42,transform:"translateX(-50%)",width:118,height:104,display:"grid",placeItems:"center",border:"5px solid #251915",borderTopWidth:12,color:"#962a22",font:"28px serif"},photoThread:{position:"absolute",left:"20%",right:"20%",top:138,height:1,background:"#86251f",boxShadow:"0 30px 0 #64221e",transform:"rotate(-5deg)"},photoBowl:{position:"absolute",left:"50%",bottom:32,transform:"translateX(-50%)",width:90,height:24,border:"7px solid #211a17",borderRadius:"0 0 50% 50%",background:"#310909",boxShadow:"0 0 18px #751515"},photoPaper:{position:"absolute",bottom:24,width:76,height:118,background:"#a78a50",transform:"rotate(-12deg)",textDecoration:"none",boxShadow:"inset 0 0 0 2px #7c4c33"},photoCaption:{display:"block",maxWidth:560,margin:"8px auto 0",color:"#777",fontSize:11},scripture:{margin:0,padding:16,borderTop:"1px solid #eceeec",background:"#111"},
};
