from pathlib import Path

# --- Admin verification gameplay ---
p=Path('app/AdminPortalOccult.tsx')
s=p.read_text()
start=s.index('function LegacyVerify(')
end=s.index('function AdminDesk()')
new=r'''function LegacyVerify({onBack,onVerified}:{onBack:()=>void;onVerified:()=>void}){
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
 const [moods,setMoods]=useState<Record<Child,"neutral"|"frown">>({lin:"neutral",shen:"neutral"});
 const [bothReach,setBothReach]=useState(false);

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
    setItems(next);setBothReach(true);setDragItem(null);completeTable(next);return;
   }
   setBothReach(true);setDragItem(null);window.setTimeout(()=>{if(items.box!=="center")setBothReach(false)},850);return;
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
     <TableSeat place="4栋东侧" mood={moods.lin} reach={bothReach} side="left" onDrop={()=>giveItem("lin")} items={ordinaryItems.filter(id=>items[id]==="lin")}/>
     <div style={v.centerTable} onDragOver={e=>e.preventDefault()} onDrop={()=>giveItem("center")}>
      <div style={v.tableTop}>
       {(["plum","marble","milk","clip","box"] as Item[]).filter(id=>!items[id]).map(id=><ObjectToken key={id} id={id} draggable onDragStart={()=>setDragItem(id)}/>) }
       {items.box==="center"&&<ObjectToken id="box"/>}
      </div>
     </div>
     <TableSeat place="青梧旧楼" mood={moods.shen} reach={bothReach} side="right" onDrop={()=>giveItem("shen")} items={ordinaryItems.filter(id=>items[id]==="shen")}/>
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

function TableSeat({place,mood,reach,side,onDrop,items}:{place:string;mood:"neutral"|"frown";reach:boolean;side:"left"|"right";onDrop:()=>void;items:string[]}){
 return <section onDragOver={e=>e.preventDefault()} onDrop={onDrop} style={v.seat}>
  <small style={v.roomStamp}>{place}</small>
  <div style={v.seatedPerson}>
   <PaperPerson stamp={side==="left"?"07·18":"07·17"} mood={mood}/>
   {reach&&<span style={{...v.arm, ...(side==="left"?{right:-52,transform:"rotate(-8deg)"}:{left:-52,transform:"rotate(8deg)"})}}/>}
  </div>
  <div style={v.kept}>{items.map(id=><ObjectToken key={id} id={id}/>)}</div>
 </section>
}

function ObjectToken({id,draggable,onDragStart}:{id:string;draggable?:boolean;onDragStart?:()=>void}){
 const labels:Record<string,string>={plum:"话梅糖",marble:"蓝玻璃弹珠",milk:"奶糖",clip:"红色发卡",box:"红铁皮盒"};
 return <div draggable={draggable} onDragStart={e=>{e.dataTransfer.effectAllowed="move";onDragStart?.()}} style={{...v.object,cursor:draggable?"grab":"default"}}>
  <i style={{...v.objectIcon,...(id==="plum"?v.plum:id==="marble"?v.marble:id==="milk"?v.milk:id==="clip"?v.clip:v.box)}}/>
  <small>{labels[id]}</small>
 </div>
}

const v:Record<string,React.CSSProperties>={
 puzzle:{padding:"34px 44px 40px",minHeight:510,background:"radial-gradient(circle at 50% 28%,#301614 0,#171414 42%,#0b0b0b 100%)"},
 dollShelf:{height:150,display:"flex",justifyContent:"center",alignItems:"flex-end",gap:52},
 person:{position:"relative",width:88,height:128,userSelect:"none",filter:"drop-shadow(0 8px 9px #0009)"},
 personHead:{position:"absolute",left:20,top:0,width:48,height:48,borderRadius:"50% 50% 44% 44%",background:"#d8c9a9",border:"1px solid #8d745c"},
 eye:{position:"absolute",top:16,width:5,height:6,borderRadius:"50%",background:"#1b1714"},
 smile:{position:"absolute",left:12,top:25,width:24,height:11,borderBottom:"3px solid #4b1714",borderRadius:"0 0 18px 18px"},
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

'''
s=s[:start]+new+s[end:]
# remove explicit Lin/Shen marks in the later recovered photo
s=s.replace('<i style={{...s.photoDoll,left:"23%"}}>沈</i><i style={{...s.photoDoll,right:"23%"}}>林</i>','<i style={{...s.photoDoll,left:"23%"}}/><i style={{...s.photoDoll,right:"23%"}}/>')
p.write_text(s)

# --- Distribute clue facts and remove name-as-mechanism text ---
p=Path('content/gameDataFlowV2.ts')
s=p.read_text()
# update Shen old report with a mundane clothing clue
old='const shenYanReport:Post={...shenYanBase,replies:['
new='const shenYanReport:Post={...shenYanBase,terms:[...(shenYanBase.terms||[]),"红色塑料发卡"],highlights:[...(shenYanBase.highlights||[]),"红色塑料发卡"],body:[...shenYanBase.body,"当年的寻人启事衣着栏还记了一项：头发右侧别着一枚红色塑料发卡。"],replies:['
if old not in s: raise SystemExit('shenYanReport anchor missing')
s=s.replace(old,new,1)
# insert three naturally scattered clue posts before the admin-account post
anchor='const adminAccountPost:Post={'
if anchor not in s: raise SystemExit('adminAccountPost anchor missing')
clues=r'''const linSnackPost:Post={
 id:"16544",title:"三厂门口那种酸话梅糖到底叫什么",author:"旧电扇",date:"2015-08-12 21:06",board:"闲聊灌水",views:814,hidden:true,
 excerpt:"聊三厂家属区门口旧小卖部的零食，楼里老住户顺带认出当年的孩子。",terms:["林楠","话梅糖","三厂","小卖部","酸话梅"],highlights:["林楠","话梅糖"],
 body:["突然想起三厂门口小卖部以前卖过一种散装话梅糖，纸是半透明的，酸得牙疼。有人记得叫什么吗？","我小时候住4栋，每次放学都有人蹲门口挑那个吃。"],
 replies:[reply("三厂老住户","21:33","牌子真想不起来。林家那个林楠小时候特别爱吃这个，买一把能一路吃到楼上。"),reply("旧电扇","21:51","对，就是那种。看来我没记错。","楼主")]
};
const linMarblePost:Post={
 id:"16802",title:"小时候那种蓝玻璃弹珠现在还有吗",author:"胶卷过期",date:"2017-05-04 18:42",board:"闲聊灌水",views:632,hidden:true,
 excerpt:"一群老住户聊小时候玩的玻璃弹珠。",terms:["林楠","蓝玻璃弹珠","弹珠","三厂家属区"],highlights:["林楠","蓝玻璃弹珠"],
 body:["收拾旧柜子翻到一颗蓝玻璃弹珠，里面像有一缕白线。小时候三厂那边是不是特别流行这种？"],
 replies:[reply("南门摆摊","19:10","流行。我小学那会儿跟林楠换过好几颗，她只要蓝的，别的颜色都不要。"),reply("胶卷过期","19:26","哈哈原来真有这种执念。","楼主")]
};
const shenCandyPost:Post={
 id:"28641",title:"有人小时候会把奶糖藏枕头下面吗",author:"候鸟第七年",date:"2021-11-06 23:17",board:"闲聊灌水",views:477,hidden:true,
 excerpt:"翻到家里的旧相册，顺手吐槽一件小时候藏糖的蠢事。",terms:["奶糖","小时候","候鸟第七年"],highlights:["奶糖"],
 body:["我妈今天翻旧相册，又开始讲我小时候把奶糖藏枕头下面，第二天化得床单黏成一块。","她说我那几年只认白纸包的奶糖，水果糖塞给我我还不要。有没有人也干过这种蠢事。"],
 replies:[reply("白粥配蛋","23:39","我藏过巧克力，夏天更惨。"),reply("候鸟第七年","23:44","看来小孩都很会给家长制造家务。","楼主")]
};

'''
s=s.replace(anchor,clues+anchor,1)
# include clue posts in the searchable corpus
old='export const posts:Post[]=[...patched,posterMemory,ritualFragmentPost,adminAccountPost].sort((a,b)=>toRank(a.date)-toRank(b.date));'
new='export const posts:Post[]=[...patched,posterMemory,linSnackPost,linMarblePost,shenCandyPost,ritualFragmentPost,adminAccountPost].sort((a,b)=>toRank(a.date)-toRank(b.date));'
if old not in s: raise SystemExit('posts export anchor missing')
s=s.replace(old,new,1)
# update private scripture mechanics and remove the old spoiler image from live play
s=s.replace('highlights:["身为舍，魂为客","形可易，名可夺，忆可乱","二客相契，两门相应","再舍者，故门有声"],','highlights:["身为舍，魂为客","形可易，忆可乱","二客相契，两门相应","再舍者，故门有声"],')
s=s.replace('"形可易，名可夺，忆可乱；客不可凭一门自证。"','"形可易，忆可乱；客不可凭一门自证。"')
s=s.replace('images:[{src:"assets/sanmen-shenyan-annotations-v1.webp",caption:"附件：沈妍保存的《三门疏》残页；只圈出处与异文"}]','images:[]')
# update ritual wording so "name" is not a supernatural variable
s=s.replace('"黄符定名"','"黄符镇舍"')
s=s.replace('"赤烛照舍，黄符定名"','"赤烛引客，黄符镇舍"')
s=s.replace('赤烛照舍，黄符定名。','赤烛引客，黄符镇舍。')
s=s.replace('至少“定名”这个说法我没见过','至少“镇舍”这个说法我没见过')
# make Shen's mundane candy post visible from her profile history
old='topics:flowProfile.topics.filter(id=>posts.some(post=>post.id===id&&post.author==="候鸟第七年")),'
new='topics:[...flowProfile.topics.filter(id=>posts.some(post=>post.id===id&&post.author==="候鸟第七年")),"28641"].filter((id,index,arr)=>arr.indexOf(id)===index),'
if old not in s: raise SystemExit('profile topics anchor missing')
s=s.replace(old,new,1)
p.write_text(s)

# --- Browser wording: no obsolete "定名" phrase, and don't render the outdated scripture image ---
p=Path('app/page.tsx')
s=p.read_text()
s=s.replace('赤烛照舍，黄符定名。','赤烛引客，黄符镇舍。')
s=s.replace('<figure style={{width:"min(720px,100%)",margin:"0 auto",background:"#050404",border:"1px solid #321714",boxShadow:"0 24px 80px #000"}}><img src="assets/occult/huanzhen-scripture.webp" alt="无相还真会黑底朱字旧教页" style={{display:"block",width:"100%"}}/><figcaption style={{padding:"9px 12px",color:"#75645c",fontSize:11}}>scan_07_untitled.tif · 来源字段已删除 · 缓存于 2026-10-16 19:49</figcaption></figure>','<figure style={{width:"min(720px,100%)",margin:"0 auto",padding:"48px 34px",background:"radial-gradient(circle,#1d0d0b 0,#090505 68%)",border:"1px solid #321714",boxShadow:"0 24px 80px #000",textAlign:"center"}}><div style={{width:110,height:110,display:"grid",placeItems:"center",margin:"0 auto 24px",border:"2px solid #7f231f",borderRadius:"50%",color:"#a9342c",font:"42px serif"}}>門</div><b style={{display:"block",color:"#a82e28",font:"700 30px serif",letterSpacing:".18em"}}>无相还真</b><figcaption style={{padding:"20px 12px 0",color:"#75645c",fontSize:11}}>scan_07_untitled.tif · 来源字段已删除 · 缓存于 2026-10-16 19:49</figcaption></figure>')
p.write_text(s)

# --- Canon v2.3: names are identity experience, not a swap mechanic; puzzle spec ---
p=Path('docs/CANON_v2.3_易舍机制与纸人验证玩法修订.md')
p.write_text('''# 《烛阴旧闻》CANON v2.3 易舍机制与纸人验证玩法修订\n\n状态：**权威修订**  \n生效日期：2026-08-17\n\n> 本文件覆盖 v2.2 中涉及“名可夺 / 定名 / 名不随客 / 管理员还真验门”的机制与玩法描述。与 v2.2、v2.1、v2.0 冲突时，以 v2.3 为准。\n\n## 1. “名”退出易舍物理机制\n\n易舍真正涉及的核心只保留：**舍（身体） / 客（灵魂） / 忆（交换后的残留、混乱与重建）**。\n\n删除以下机制：\n- 名可夺；\n- 名不随客；\n- 名字跟身体或灵魂移动的规则；\n- 定名符作为易舍必要步骤；\n- 管理员验证中的“守原名 / 随客易名”。\n\n姓名只是现实社会对一具身体及其既有身份的称呼。易舍后，家人、户籍、照片和生活环境仍会让外界沿用这具身体原有的姓名，不需要超自然规则解释。\n\n## 2. “身非我身，名非我名”的定位\n\n**身非我身，名非我名**继续保留，但它不是技术规则。\n\n它表达的是易舍者最直观的身份错位体验：身体陌生，别人叫自己的名字也产生“不像在叫我”的感觉。它可以作为无相还真会旧誓/宗教表达存在。\n\n《三门疏》机制句修订为：\n- 身为舍，魂为客；\n- **形可易，忆可乱；**\n- 二客相契，两门相应；\n- 再舍者，故门有声。\n\n旧版“形可易，名可夺，忆可乱”废止。\n\n旧版“赤烛照舍，黄符定名”废止；如旧教材料需要对应短句，改为：**赤烛引客，黄符镇舍。**\n\n## 3. 管理员兼容认证：旧誓之后不再讲宗教话语\n\n玩家仍需先在旧档认证中主动录入旧誓“身非我身，名非我名”。\n\n旧誓通过后的交互验证不再显示“舍身无量”“旧客退位”等仪式台词，也不再把验证做成经文阅读理解。验证本身应像一个来源不明、非常诡异的旧网页小游戏。\n\n## 4. 第一关：两个纸人归入两个家\n\n- 页面出现两个带夸张微笑的纸人。\n- **纸人本体不写“林楠 / 沈妍”。房间也不写姓名。**\n- 两个纸人只保留可从旧报推断身份的日期戳：`07·18` 与 `07·17`。\n- 两个房间用生活细节区分，例如：三厂 4 栋的蓝窗帘/红铁皮盒，与青梧旧楼的红发卡/奶糖罐。\n- 这些归属关系必须由前面论坛帖子、旧报和个人旧帖自然提供。谜题页面不能替玩家写答案。\n- 玩家必须手动拖动两个纸人进入对应房间。\n- 放错不会推进；放对后该纸人的夸张笑容消失，变成无表情。\n- 两个纸人均正确归位后自动进入第二关，不显示“恭喜/第一关成功”。\n\n## 5. 第二关：桌上分物\n\n桌面出现 5 件可拖动物品：\n\n- 林楠侧：**话梅糖、蓝玻璃弹珠**；\n- 沈妍侧：**奶糖、红色发卡**；\n- 共享物：**红铁皮盒**。\n\n交互反馈：\n- 普通物放对：纸人收下，物品留在其手边；\n- 普通物放错：纸人撇嘴，物品回到桌面；\n- 红铁皮盒拖给任意一个纸人：**两个纸人都会同时伸手**，但都不能单独收下；\n- 玩家把红铁皮盒放回两人中间时，两边同时伸手按住它；\n- 四件普通物全部正确归属 + 红铁皮盒位于中央，才算通过。\n\n页面不出现解释“为什么两个人都记得”之类的作者文字。玩家只需要先产生疑问。\n\n## 6. 线索散布原则\n\n分物答案不能集中在一篇答案帖中。至少分散到不同类型的自然材料：\n- 林楠的话梅糖：三厂家属区旧住户闲聊；\n- 林楠的蓝玻璃弹珠：另一篇童年玩具闲聊；\n- 沈妍的红色发卡：旧寻人启事衣着栏；\n- 沈妍的奶糖：候鸟第七年的普通旧帖；\n- 红铁皮盒：继续通过梦帖、旧房照片、本地资料等多处反复出现，不提前解释其“双向反应”。\n\n难度来自“我之前在哪里见过这个”，不是来自隐藏按钮，也不是靠谜题页面给提示。\n\n## 7. 视觉与反馈\n\n- 纸人初始笑容必须明显且不自然；\n- 第一关归位后笑容消失；\n- 第二关错误反馈使用轻微撇嘴，不弹系统报错；\n- 红铁皮盒触发两个纸人同步伸手，是本关最重要的异常视觉反馈；\n- 不使用跳脸；不使用“验证正确/错误”的大字覆盖；\n- 整体仍可保留旧纸、暗红、蜡烛残光等邪教视觉，但**玩法过程中不朗诵宗教话语**。\n''')

# Add supersession notice to v2.2
p=Path('docs/CANON_v2.2_无相还真会宗教感与管理员线修订.md')
s=p.read_text()
notice='> **2026-08-17 v2.3 修订：** “名可夺 / 定名 / 名不随客”及旧管理员验证玩法已由 `CANON_v2.3_易舍机制与纸人验证玩法修订.md` 覆盖。涉及这些内容时以 v2.3 为准。\n\n'
if notice not in s:
    marker='> 本文件对 v2.1 中“私密区/八字经文/管理员认证”结构，以及无相还真会的视觉与宗教表达做正式修订。  \n'
    idx=s.index(marker)
    s=s[:idx]+notice+s[idx:]
p.write_text(s)
