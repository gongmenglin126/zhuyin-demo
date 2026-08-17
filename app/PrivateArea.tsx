"use client";
/* eslint-disable @next/next/no-img-element */

import {FormEvent,useState} from "react";
import {ArrowLeft,FileText,Link2,LockKeyhole,Maximize2,X} from "lucide-react";
import type {PrivateEntry} from "../content/gameDataFlowV2";
import DeepArchiveGate from "./DeepArchiveGate";
import type {SharedMaterial} from "./InteractiveWechat";

const normalize=(value:string)=>value.replace(/[，。、“”‘’\s]/g,"");

export default function PrivateArea({entries,unlocked,onUnlock,onCopyMaterial,hasMaterial}:{
 entries:PrivateEntry[];
 unlocked:boolean;
 onUnlock:()=>void;
 onCopyMaterial:(m:SharedMaterial)=>void;
 hasMaterial:(id:string)=>boolean;
}){
 const [pwd,setPwd]=useState("");
 const [error,setError]=useState("");
 const [id,setId]=useState<string|null>(null);
 const [zoom,setZoom]=useState<{src:string;caption:string}|null>(null);
 const active=id?entries.find(entry=>entry.id===id):null;

 const submit=(e:FormEvent)=>{
  e.preventDefault();
  if(normalize(pwd)==="林楠"){
   setError("");
   onUnlock();
  }else{
   setError(pwd.trim()?"口令不正确。":"请输入访问口令。");
  }
 };

 if(!unlocked){
  return <main style={s.page}>
   <div style={s.crumb}>个人主页　/　私密主题</div>
   <section style={s.gate}>
    <div style={s.gateIcon}><LockKeyhole size={25}/></div>
    <small style={s.eyebrow}>候鸟第七年 · 仅自己可见</small>
    <h2 style={s.gateTitle}>私密主题</h2>
    <p style={s.gateCopy}>这个区域设置了独立访问口令。</p>
    <form onSubmit={submit} style={s.gateForm}>
     <label style={s.label}>访问口令 <span style={s.labelHint}>2 个汉字</span></label>
     <input
      autoFocus
      autoComplete="off"
      value={pwd}
      onChange={e=>{setPwd(e.target.value);setError("")}}
      aria-label="访问口令"
      placeholder="输入口令"
      style={s.input}
     />
     <button style={s.primary}>进入私密主题</button>
    </form>
    {error&&<em style={s.error}>{error}</em>}
   </section>
  </main>;
 }

 if(!active){
  return <main style={s.page}>
   <div style={s.crumb}>个人主页　/　私密主题</div>
   <section style={s.accountBand}>
    <i style={s.avatar}>候</i>
    <span><small style={s.bandSmall}>候鸟第七年</small><h2 style={s.bandTitle}>私密主题</h2></span>
    <em style={s.privateTag}><LockKeyhole size={14}/>仅当前账号可见</em>
   </section>
   <section style={s.list}>
    <header style={s.listHead}><span><b>保存的私密记录</b><small style={s.listSmall}>{entries.length} 篇 · 按保存时间排列</small></span></header>
    {entries.map(entry=><button key={entry.id} onClick={()=>setId(entry.id)} style={s.row}>
     <i style={s.fileIcon}><FileText size={18}/></i>
     <span style={s.rowText}><b style={s.rowTitle}>{entry.title}</b><p style={s.rowPreview}>{entry.body[0]}</p></span>
     <time style={s.time}>{entry.date.split(" ")[0]}<small>{entry.date.split(" ")[1]}</small></time>
    </button>)}
   </section>
  </main>;
 }

 const share=()=>{onCopyMaterial({
  id:`private-${active.id}`,
  title:active.title,
  kind:"沈妍私密记录",
  url:`local://private/${active.id}`,
 });};

 return <main style={s.page}>
  <div style={s.crumb}>个人主页　/　私密主题　/　{active.title}</div>
  <section style={s.thread}>
   <button onClick={()=>setId(null)} style={s.back}><ArrowLeft size={15}/>返回私密主题</button>
   <header style={s.threadHead}>
    <span><small style={s.eyebrow}>私密记录 · {active.date}</small><h2 style={s.threadTitle}>{active.title}</h2></span>
    <button disabled={hasMaterial(`private-${active.id}`)} onClick={share} style={{...s.share,opacity:hasMaterial(`private-${active.id}`)?.55:1,cursor:hasMaterial(`private-${active.id}`)?"default":"pointer"}}><Link2 size={14}/>{hasMaterial(`private-${active.id}`)?"已添加":"添加到材料"}</button>
   </header>
   <article style={s.article}>
    <header style={s.authorLine}><i style={s.smallAvatar}>候</i><span><b>候鸟第七年</b><small>仅自己可见</small></span></header>
    <div style={s.body}>
     {active.body.map((text,index)=><p key={index}>{mark(text,active.highlights)}</p>)}
     {active.images?.map(image=><figure key={image.src} style={s.figure}>
      <button onClick={()=>setZoom(image)} style={s.imageButton} title="查看原图">
       <img src={image.src} alt={image.caption} style={s.image}/>
       <span style={s.zoomLabel}><Maximize2 size={13}/>查看原图</span>
      </button>
      <figcaption style={s.caption}>{image.caption}</figcaption>
     </figure>)}
     {active.id==="p3"&&<DeepArchiveGate onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>} 
    </div>
   </article>
  </section>
  {zoom&&<button onClick={()=>setZoom(null)} style={s.lightbox}>
   <span style={s.close}><X size={17}/>关闭</span>
   <img src={zoom.src} alt={zoom.caption} style={s.lightboxImage}/>
   <em style={s.lightboxCaption}>{zoom.caption}</em>
  </button>}
 </main>;
}

function mark(text:string,marks:string[]=[]){
 const usable=marks.filter(Boolean).sort((a,b)=>b.length-a.length);
 if(!usable.length)return text;
 const escaped=usable.map(x=>x.replace(/[.*+?^${}()|[\]\\]/g,"\\$&"));
 const parts=text.split(new RegExp(`(${escaped.join("|")})`,"g"));
 return <>{parts.map((part,index)=>usable.includes(part)?<strong key={index} style={s.clue}>{part}</strong>:part)}</>;
}

const s:Record<string,React.CSSProperties>={
 page:{minHeight:"100%",padding:"26px 28px 48px",background:"#eee9df",color:"#292d29"},
 crumb:{maxWidth:1040,margin:"0 auto 12px",color:"#858078",fontSize:11},
 gate:{width:"min(620px,94%)",margin:"56px auto",padding:"44px 48px 40px",border:"1px solid #d0c8bb",borderRadius:14,background:"#fbf9f4",boxShadow:"0 22px 65px #3f372c1a"},
 gateIcon:{width:54,height:54,display:"grid",placeItems:"center",marginBottom:18,borderRadius:13,background:"#40564f",color:"#fff"},
 eyebrow:{display:"block",color:"#8a847b",fontSize:10,letterSpacing:".08em"},
 gateTitle:{margin:"7px 0 8px",fontSize:28},
 gateCopy:{margin:"0 0 28px",color:"#6f6a62",fontSize:13,lineHeight:1.7},
 gateForm:{display:"grid",gridTemplateColumns:"1fr 150px",gap:10,alignItems:"end"},
 label:{gridColumn:"1 / -1",display:"flex",justifyContent:"space-between",color:"#55514b",fontSize:12,fontWeight:700},
 labelHint:{color:"#918a80",fontWeight:400},
 input:{width:"100%",height:50,padding:"0 16px",border:"1px solid #bdb5a8",borderRadius:8,background:"#fff",outline:"none",fontSize:17,letterSpacing:".08em",color:"#252925"},
 primary:{height:50,padding:"0 18px",border:0,borderRadius:8,background:"#40564f",color:"#fff",fontSize:13,fontWeight:700},
 error:{display:"block",marginTop:12,color:"#9e453b",fontSize:12,fontStyle:"normal"},
 accountBand:{maxWidth:1040,display:"flex",alignItems:"center",gap:14,margin:"0 auto",padding:"20px 22px",border:"1px solid #31463f",borderRadius:"10px 10px 0 0",background:"#3b514a",color:"#fff"},
 avatar:{width:48,height:48,display:"grid",placeItems:"center",borderRadius:10,background:"#60776f",font:"22px serif",fontStyle:"normal"},
 bandSmall:{color:"#cbd4d0",fontSize:10},bandTitle:{margin:"2px 0 0",fontSize:21},
 privateTag:{marginLeft:"auto",display:"flex",alignItems:"center",gap:6,color:"#d8dfdc",fontSize:11,fontStyle:"normal"},
 list:{maxWidth:1040,margin:"0 auto",border:"1px solid #d1c8bb",borderTop:0,borderRadius:"0 0 10px 10px",overflow:"hidden",background:"#fbf9f4"},
 listHead:{padding:"16px 20px",background:"#e7e0d5",fontSize:13},listSmall:{display:"block",marginTop:3,color:"#8f887f",fontSize:10,fontWeight:400},
 row:{width:"100%",display:"grid",gridTemplateColumns:"46px minmax(0,1fr) 105px",gap:15,alignItems:"center",padding:"19px 20px",border:0,borderTop:"1px solid #e2dbd0",background:"#fbf9f4",textAlign:"left"},
 fileIcon:{width:38,height:38,display:"grid",placeItems:"center",borderRadius:10,background:"#eee6da",color:"#76534b",fontStyle:"normal"},
 rowText:{minWidth:0},rowTitle:{display:"block",fontSize:15},rowPreview:{margin:"6px 0 0",overflow:"hidden",color:"#777067",fontSize:12,textOverflow:"ellipsis",whiteSpace:"nowrap"},
 time:{color:"#7e786f",fontSize:11,textAlign:"right"},
 thread:{maxWidth:930,margin:"0 auto"},back:{display:"flex",alignItems:"center",gap:6,margin:"0 0 10px",padding:"7px 0",border:0,background:"transparent",color:"#46645b",fontSize:12},
 threadHead:{display:"flex",justifyContent:"space-between",alignItems:"flex-end",gap:18,padding:"22px 24px",border:"1px solid #d1c8bb",borderRadius:"10px 10px 0 0",background:"#fbf9f4"},threadTitle:{margin:"6px 0 0",fontSize:24,lineHeight:1.35},
 share:{flex:"0 0 auto",display:"flex",alignItems:"center",gap:6,padding:"8px 11px",border:"1px solid #c5bbae",borderRadius:7,background:"#fff",color:"#485b55",fontSize:12},
 article:{border:"1px solid #d1c8bb",borderTop:0,borderRadius:"0 0 10px 10px",background:"#fbf9f4"},authorLine:{display:"flex",alignItems:"center",gap:10,padding:"16px 24px",borderBottom:"1px solid #e0d8cc",background:"#f1ece3",fontSize:12},smallAvatar:{width:34,height:34,display:"grid",placeItems:"center",borderRadius:8,background:"#60776f",color:"#fff",fontStyle:"normal"},
 body:{padding:"24px 30px 34px",fontSize:15,lineHeight:1.95},clue:{fontWeight:800,textDecoration:"underline",textDecorationColor:"#b9ad99",textUnderlineOffset:3},
 figure:{width:"min(520px,100%)",margin:"24px auto",padding:10,border:"1px solid #d4ccbf",borderRadius:8,background:"#f0ece4"},imageButton:{position:"relative",width:"100%",display:"block",padding:0,border:0,borderRadius:5,overflow:"hidden",background:"#d9d4cb"},image:{display:"block",width:"100%",maxHeight:360,objectFit:"contain",background:"#e8e3da"},zoomLabel:{position:"absolute",right:8,bottom:8,display:"flex",alignItems:"center",gap:5,padding:"5px 8px",borderRadius:5,background:"#111c",color:"#fff",fontSize:10},caption:{padding:"9px 3px 2px",color:"#77736c",fontSize:11},
 lightbox:{position:"fixed",zIndex:600,inset:0,width:"100%",height:"100%",display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",gap:12,padding:48,border:0,background:"#050807ed",color:"#fff"},close:{position:"absolute",right:24,top:20,display:"flex",alignItems:"center",gap:5},lightboxImage:{maxWidth:"90%",maxHeight:"78%",objectFit:"contain"},lightboxCaption:{fontSize:12,fontStyle:"normal",color:"#ddd"},
};