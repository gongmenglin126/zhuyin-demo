"use client";

import {FormEvent,useMemo,useState} from "react";
import {ArrowLeft,ChevronRight,LockKeyhole,Search,ShieldCheck} from "lucide-react";

export const ADMIN_USER="旧档员-03";
export const ADMIN_TEMP_CODE="gumen-0712";

type Guest="甲客"|"乙客";
type DoorState={left:Guest[];right:Guest[]};

type Props={
 loggedIn:boolean;
 onAdminLogin:()=>void;
 onCancel:()=>void;
};

export default function AdminPortal({loggedIn,onAdminLogin,onCancel}:Props){
 const [mode,setMode]=useState<"login"|"verify">("login");
 const [user,setUser]=useState("");
 const [pwd,setPwd]=useState("");
 const [error,setError]=useState("");
 const [verified,setVerified]=useState(false);
 const [filled,setFilled]=useState(false);

 if(loggedIn)return <AdminDesk/>;

 const submit=(e:FormEvent)=>{
  e.preventDefault();
  if(user.trim()===ADMIN_USER&&pwd===ADMIN_TEMP_CODE){onAdminLogin();setError("");return;}
  setError(user.trim()?"账号或密码错误":"请输入账号");
 };
 const useCode=()=>{setUser(ADMIN_USER);setPwd(ADMIN_TEMP_CODE);setMode("login");setFilled(true);setError("")};

 if(mode==="verify")return <LegacyVerify onBack={()=>setMode("login")} onVerified={()=>{setVerified(true);useCode()}}/>;

 return <main style={s.loginPage}>
  <section style={s.loginCard}>
   <button onClick={onCancel} style={s.back}><ArrowLeft size={15}/>返回</button>
   <div style={s.logo}>烛</div>
   <h2 style={s.loginTitle}>登录烛阴旧闻</h2>
   <p style={s.muted}>当前浏览器保存了一个已登录会话。也可以使用其他账号登录。</p>
   <form onSubmit={submit} style={s.form}>
    <label style={s.field}><span>账号</span><input value={user} onChange={e=>{setUser(e.target.value);setError("")}} autoComplete="off" placeholder="用户名"/></label>
    <label style={s.field}><span>密码</span><input type="password" value={pwd} onChange={e=>{setPwd(e.target.value);setError("")}} autoComplete="off" placeholder="密码"/></label>
    {error&&<em style={s.error}>{error}</em>}
    {filled&&<small style={s.codeFilled}>旧档验证生成的临时口令已填入。</small>}
    <button style={s.primary}>登录</button>
   </form>
   {user.trim()===ADMIN_USER&&<button onClick={()=>setMode("verify")} style={s.legacy}><LockKeyhole size={15}/><span><b>旧档账号验证</b><small>适用于早期迁移账号</small></span><ChevronRight size={15}/></button>}
   {verified&&<small style={s.muted}>验证已完成。</small>}
  </section>
 </main>;
}

function LegacyVerify({onBack,onVerified}:{onBack:()=>void;onVerified:()=>void}){
 const [stage,setStage]=useState(0);
 const [doors,setDoors]=useState<DoorState>({left:["甲客"],right:["乙客"]});
 const [selected,setSelected]=useState<Guest|null>(null);
 const [error,setError]=useState("");
 const move=(target:"left"|"right")=>{
  if(!selected)return;
  setDoors(prev=>({
   left:[...prev.left.filter(x=>x!==selected),...(target==="left"&&!prev.left.includes(selected)?[selected]:[])],
   right:[...prev.right.filter(x=>x!==selected),...(target==="right"&&!prev.right.includes(selected)?[selected]:[])],
  }));
  setSelected(null);setError("");
 };
 const checkSwap=()=>{
  if(doors.left.length===1&&doors.left[0]==="乙客"&&doors.right.length===1&&doors.right[0]==="甲客"){setStage(1);setError("");return;}
  if(!doors.left.length||!doors.right.length||doors.left.length>1||doors.right.length>1)setError("一门无客，一门有余。");
  else setError("二客未易。");
 };
 return <main style={s.verifyPage}>
  <section style={s.verifyShell}>
   <header style={s.verifyHead}><button onClick={onBack} style={s.darkBack}><ArrowLeft size={15}/>返回登录</button><span><small>旧档账号验证</small><b>两门演算</b></span><em>{stage<3?`${stage+1} / 3`:"完成"}</em></header>
   {stage===0&&<div style={s.ritual}>
    <p style={s.verse}>二客各有所舍。</p>
    <RitualAltar/>
    <div style={s.doors}>
     <Door title="甲舍" name="甲名" guests={doors.left} selected={selected} onSelect={setSelected} onDrop={()=>move("left")}/>
     <div style={s.swapMark}>⇄</div>
     <Door title="乙舍" name="乙名" guests={doors.right} selected={selected} onSelect={setSelected} onDrop={()=>move("right")}/>
    </div>
    <p style={s.help}>{selected?`已选中 ${selected}。选择另一侧的“放入此舍”。`:"点击“客”，再选择要放入的“舍”。"}</p>
    {error&&<p style={s.ritualError}>{error}</p>}
    <button onClick={checkSwap} style={s.verifyButton}>验门</button>
   </div>}
   {stage===1&&<div style={s.ritual}>
    <p style={s.verse}>二客相易。名仍在门上。</p>
    <div style={s.doors}>
     <StaticDoor title="甲舍" name="甲名" guest="乙客"/>
     <div style={s.swapMark}>⇄</div>
     <StaticDoor title="乙舍" name="乙名" guest="甲客"/>
    </div>
    <p style={s.help}>门外仍呼旧名。</p>
    {error&&<p style={s.ritualError}>{error}</p>}
    <div style={s.choiceRow}><button onClick={()=>setError("名不随客。")}>交换名牌</button><button onClick={()=>{setStage(2);setError("")}}>保持名牌</button></div>
   </div>}
   {stage===2&&<div style={s.ritual}>
    <p style={s.verse}>形可易，名可夺，忆可乱。</p>
    <div style={s.memoryGrid}>
     <span>蓝窗帘</span><span>旧客站</span><span>话梅</span><span>厨房门</span><span>另一个家</span><span>叫错的名字</span>
    </div>
    <p style={s.help}>有些东西回不到原处。</p>
    {error&&<p style={s.ritualError}>{error}</p>}
    <div style={s.choiceRow}><button onClick={()=>setError("忆不可尽归。")}>全部归回原位</button><button onClick={()=>setStage(3)}>保留残缺与错位</button></div>
   </div>}
   {stage===3&&<div style={s.success}>
    <p style={s.afterVerse}>身非我身　名非我名</p>
    <ShieldCheck size={34}/>
    <small>验门通过</small>
    <h2>旧档账号临时口令</h2>
    <code>{ADMIN_TEMP_CODE}</code>
    <p>临时口令仅用于本次旧档认证。</p>
    <button onClick={onVerified} style={s.verifyButton}>返回登录并填入口令</button>
   </div>}
  </section>
 </main>;
}

function RitualAltar(){return <div style={s.altar} aria-hidden="true">
 <span style={{...s.candle,left:42}}/><span style={{...s.candle,right:42}}/>
 <span style={s.threadA}/><span style={s.threadB}/>
 <div style={s.altarRing}><b>門</b><small>身非我身</small></div>
 <div style={s.altarTable}><span>甲</span><em>名非我名</em><span>乙</span></div>
</div>}

function Door({title,name,guests,selected,onSelect,onDrop}:{title:string;name:string;guests:Guest[];selected:Guest|null;onSelect:(g:Guest)=>void;onDrop:()=>void}){
 return <section style={s.door}><header><b>{title}</b><span>{name}</span></header><div style={s.guestBox}>{guests.length?guests.map(g=><button key={g} onClick={()=>onSelect(g)} style={{...s.guest,...(selected===g?s.guestSelected:{})}}>{g}</button>):<em>空</em>}</div><button onClick={onDrop} disabled={!selected} style={s.drop}>放入此舍</button></section>;
}
function StaticDoor({title,name,guest}:{title:string;name:string;guest:Guest}){return <section style={s.door}><header><b>{title}</b><span>{name}</span></header><div style={s.guestBox}><i style={{...s.guest,...s.guestSelected}}>{guest}</i></div></section>}

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

function UserRecord(){return <article style={s.userRecord}><header><i>候</i><span><h3>候鸟第七年</h3><small>UID 0712-4471 · 注册于 2017-07-12 · 最后活动 2026-10-16 19:48</small></span><em>观察中</em></header><div style={s.statRow}><span><b>8</b><small>公开主题</small></span><span><b>2</b><small>私密主题</small></span><span><b>1</b><small>回收记录</small></span><span><b>4</b><small>内部记录</small></span></div><section style={s.adminPanel}><h4>私密主题</h4><Record date="2026-06-19 03:12" title="昨晚又梦到了" meta="仅自己可见" text="又是那间房。红铁皮盒、蓝窗帘，还有那个听不清的称呼。"/><Record date="2026-09-11 02:08" title="9月11日，几条旧帖" meta="仅自己可见" text="有的人回来以后只是口味变了，也有人一直说名字不对、记得另一个家。"/></section><section style={s.adminPanel}><h4>内部标记</h4><Record date="2026-08-22 04:12" title="case-returned / age9" meta="记录者：照骨" text="与旧报恢复记录存在交叉。继续观察公开检索与私密主题更新。"/><Record date="2026-10-16 19:49" title="状态变更" meta="旧档员-03" text="站内观察 → 线下跟进；停止公开区接触。"/></section></article>}
function Operations(){return <><h2>操作记录</h2><div style={s.adminPanel}><Record date="2026-10-16 19:49" title="用户状态变更：候鸟第七年" meta="旧档员-03" text="站内观察 → 线下跟进"/><Record date="2026-09-11 02:16" title="私密主题索引更新：候鸟第七年" meta="自动任务" text="private/p3 · 索引完成"/><Record date="2026-08-22 04:12" title="添加内部标记：候鸟第七年" meta="照骨" text="case-returned / age9"/><Record date="2026-07-12 01:31" title="附件指纹命中" meta="旧档恢复任务" text="sanmen_fragment.txt · 与旧档附件组存在近似记录"/></div></>}
function Recycle(){return <><h2>回收记录</h2><div style={s.adminPanel}><Record date="2026-10-16 18:31" title="未发布草稿" meta="候鸟第七年 · 私密草稿 · 已删除" text="照骨问的问题不是随机的。它在不同人的帖子下面问的是同一套东西。旧档员-03也反复碰过这些帖。先把账号记下来。"/><Record date="2026-10-16 20:47" title="附件缓存" meta="旧档员-03 · 已删除" text="IMG_1016_2047.jpg · 原始来源字段缺失 · 仅恢复缩略图"/><RitualThumbnail/></div></>}
function RitualThumbnail(){return <figure style={s.photo}><div style={s.photoRoom}><span style={s.photoCandleL}/><span style={s.photoCandleR}/><i style={s.photoChairL}/><i style={s.photoChairR}/><b style={s.photoTableMark}>門</b><em style={s.photoLine}/></div><figcaption style={s.photoCaption}>IMG_1016_2047.jpg　恢复 14%</figcaption></figure>}

function Record({date,title,meta,text}:{date:string;title:string;meta:string;text:string}){return <div style={s.record}><time>{date}</time><span><b>{title}</b><small>{meta}</small><p>{text}</p></span></div>}

const s:Record<string,React.CSSProperties>={
 loginPage:{minHeight:"calc(100% - 39px)",display:"grid",placeItems:"center",padding:32,background:"#ece9e2",color:"#292d29"},loginCard:{width:"min(520px,92%)",padding:"28px 34px 34px",border:"1px solid #d2ccc1",borderRadius:12,background:"#fbfaf7",boxShadow:"0 20px 55px #352f2717"},back:{display:"flex",alignItems:"center",gap:6,border:0,background:"transparent",padding:0,color:"#69716d",fontSize:12},logo:{width:52,height:52,display:"grid",placeItems:"center",margin:"20px auto 10px",borderRadius:12,background:"#3d514a",color:"#fff",font:"25px serif"},loginTitle:{margin:"0 0 7px",textAlign:"center",fontSize:23},muted:{display:"block",margin:"0 auto 20px",color:"#8a857e",fontSize:12,lineHeight:1.7,textAlign:"center"},form:{display:"grid",gap:11},field:{display:"grid",gap:5,color:"#666159",fontSize:11},error:{color:"#9a443b",fontSize:11,fontStyle:"normal"},codeFilled:{color:"#49635a",fontSize:11},primary:{height:44,border:0,borderRadius:7,background:"#3d514a",color:"#fff",fontWeight:700},legacy:{width:"100%",display:"grid",gridTemplateColumns:"24px 1fr 20px",alignItems:"center",gap:8,marginTop:18,padding:"11px 12px",border:"1px solid #d9d3c9",borderRadius:8,background:"#f4f1eb",textAlign:"left",color:"#494640"},
 verifyPage:{minHeight:"calc(100% - 39px)",display:"grid",placeItems:"center",padding:24,background:"radial-gradient(circle at 50% 54%,#351616 0,#171a18 46%,#090b0a 100%)",color:"#e9ece9"},verifyShell:{width:"min(780px,96%)",minHeight:540,border:"1px solid #4b3a38",borderRadius:10,background:"#1d211f",boxShadow:"0 30px 90px #000, inset 0 0 90px #5b15151c",overflow:"hidden"},verifyHead:{height:64,display:"grid",gridTemplateColumns:"1fr auto 1fr",alignItems:"center",padding:"0 18px",borderBottom:"1px solid #3a423d",background:"#191d1b"},darkBack:{justifySelf:"start",display:"flex",alignItems:"center",gap:6,border:0,background:"transparent",color:"#aeb7b1"},ritual:{padding:"34px 54px 42px",textAlign:"center"},verse:{font:"18px serif",letterSpacing:".12em",color:"#e4ded1"},altar:{position:"relative",height:154,maxWidth:520,margin:"22px auto 6px",borderBottom:"1px solid #6b4a42",background:"radial-gradient(circle at 50% 45%,#6c2a1a33 0,#181b19 58%,#111311 100%)",overflow:"hidden"},candle:{position:"absolute",bottom:28,width:8,height:34,background:"#9b8060",boxShadow:"0 -10px 16px #e48a4e99,0 -5px 4px #ffc079",borderRadius:"2px 2px 0 0"},threadA:{position:"absolute",left:90,right:90,top:76,height:1,background:"#6b2525",transform:"rotate(12deg)",transformOrigin:"center"},threadB:{position:"absolute",left:90,right:90,top:76,height:1,background:"#6b2525",transform:"rotate(-12deg)",transformOrigin:"center"},altarRing:{position:"absolute",left:"50%",top:22,transform:"translateX(-50%)",width:86,height:86,border:"1px solid #7e3d36",borderRadius:"50%",display:"grid",placeItems:"center",background:"#1d1716cc",boxShadow:"0 0 28px #6f201f44",color:"#b99283"},altarTable:{position:"absolute",left:"50%",bottom:0,transform:"translateX(-50%)",width:220,height:34,display:"flex",alignItems:"center",justifyContent:"space-between",padding:"0 18px",border:"1px solid #493633",background:"#171311",color:"#8e756a",font:"12px serif"},afterVerse:{margin:"0 0 18px",color:"#9f6b65",font:"15px serif",letterSpacing:".22em"},doors:{display:"grid",gridTemplateColumns:"1fr 52px 1fr",alignItems:"center",gap:12,margin:"32px auto 18px",maxWidth:620},door:{minHeight:230,padding:18,border:"1px solid #56615a",borderRadius:10,background:"#272e2a"},guestBox:{minHeight:104,display:"flex",alignItems:"center",justifyContent:"center",gap:8,padding:15,margin:"18px 0",border:"1px dashed #59635d",borderRadius:8},guest:{display:"inline-grid",placeItems:"center",minWidth:72,height:42,padding:"0 12px",border:"1px solid #807563",borderRadius:21,background:"#352f28",color:"#e9ddc9",fontStyle:"normal"},guestSelected:{boxShadow:"0 0 0 2px #cab99b",background:"#4b4034"},drop:{height:34,padding:"0 12px",border:"1px solid #56615a",borderRadius:6,background:"#202522",color:"#cbd1cd"},swapMark:{fontSize:28,color:"#77817b"},help:{minHeight:22,color:"#929b95",fontSize:12},ritualError:{color:"#d0958d",font:"14px serif"},verifyButton:{minWidth:190,height:42,border:"1px solid #8c806d",borderRadius:6,background:"#443b31",color:"#efe5d4",fontWeight:700},choiceRow:{display:"flex",justifyContent:"center",gap:12,marginTop:24},memoryGrid:{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:10,maxWidth:550,margin:"34px auto",color:"#c7cec9"},success:{display:"grid",placeItems:"center",padding:"95px 30px",textAlign:"center"},
 adminPage:{minHeight:"calc(100% - 39px)",background:"#eef0ee",color:"#262a27"},adminHead:{height:62,display:"flex",alignItems:"center",justifyContent:"space-between",padding:"0 24px",borderBottom:"1px solid #cbd0cc",background:"#354840",color:"#fff"},adminAccount:{padding:"6px 10px",borderRadius:6,background:"#26372f",fontSize:11},adminLayout:{minHeight:560,display:"grid",gridTemplateColumns:"180px 1fr"},adminSide:{padding:14,background:"#e1e5e2",borderRight:"1px solid #cbd0cc"},adminBody:{padding:"28px 34px",overflowY:"auto"},adminSearch:{display:"grid",gridTemplateColumns:"24px 1fr 74px",alignItems:"center",maxWidth:620,padding:"7px 8px",border:"1px solid #c6cbc7",borderRadius:8,background:"#fff"},adminEmpty:{color:"#8b918d"},userRecord:{maxWidth:850,marginTop:22},statRow:{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:10,margin:"14px 0"},adminPanel:{marginTop:16,border:"1px solid #ced3cf",borderRadius:8,background:"#fff",overflow:"hidden"},record:{display:"grid",gridTemplateColumns:"150px 1fr",gap:16,padding:"14px 16px",borderTop:"1px solid #eceeec"},photo:{margin:"0",padding:"16px",borderTop:"1px solid #eceeec",background:"#f6f6f3"},photoRoom:{position:"relative",height:220,maxWidth:520,margin:"0 auto",overflow:"hidden",border:"8px solid #222",background:"radial-gradient(circle at 50% 58%,#665042 0,#2a2724 32%,#111 72%)",filter:"grayscale(.65) contrast(1.18)",boxShadow:"inset 0 0 65px #000"},photoCandleL:{position:"absolute",left:"24%",bottom:48,width:5,height:26,background:"#c4aa7f",boxShadow:"0 -8px 12px #ffc06b"},photoCandleR:{position:"absolute",right:"24%",bottom:48,width:5,height:26,background:"#c4aa7f",boxShadow:"0 -8px 12px #ffc06b"},photoChairL:{position:"absolute",left:"13%",bottom:42,width:58,height:78,border:"5px solid #171717",borderBottom:0,transform:"rotate(4deg)"},photoChairR:{position:"absolute",right:"13%",bottom:42,width:58,height:78,border:"5px solid #171717",borderBottom:0,transform:"rotate(-4deg)"},photoTableMark:{position:"absolute",left:"50%",bottom:52,transform:"translateX(-50%)",width:110,height:42,display:"grid",placeItems:"center",border:"1px solid #6c5548",background:"#1a1512",color:"#8e7769",font:"22px serif"},photoLine:{position:"absolute",left:"15%",right:"15%",bottom:30,height:1,background:"#766255",boxShadow:"0 -58px 0 #4d3c34",transform:"rotate(-2deg)"},photoCaption:{display:"block",maxWidth:520,margin:"8px auto 0",color:"#777",fontSize:11},
};