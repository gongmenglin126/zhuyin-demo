"use client";

import {FormEvent,useState} from "react";
import {FileArchive,Link2,LockKeyhole} from "lucide-react";
import type {SharedMaterial} from "./InteractiveWechat";

const normalize=(value:string)=>value.replace(/[，。、“”‘’\s]/g,"");

export default function DeepArchiveGate({onCopyMaterial}:{onCopyMaterial:(m:SharedMaterial)=>void}){
 const [pwd,setPwd]=useState(""),[error,setError]=useState(""),[unlocked,setUnlocked]=useState(false);
 const submit=(e:FormEvent)=>{
  e.preventDefault();
  if(normalize(pwd)==="身非我身名非我名"){setUnlocked(true);setError("");return;}
  setError(pwd.trim()?"密码错误":"请输入密码");
 };
 return <section style={{marginTop:28,border:"1px solid #d7cec1",borderRadius:10,background:"#f6f2eb",overflow:"hidden"}}>
  <header style={{display:"flex",alignItems:"center",gap:10,padding:"14px 16px",borderBottom:"1px solid #ddd4c8",background:"#eee7dc"}}><FileArchive size={18}/><span><b style={{display:"block"}}>本地附件：archive_0712.zip</b><small style={{color:"#837a71"}}>这份附件只出现在沈妍的私密记录里</small></span></header>
  {!unlocked?<div style={{padding:"18px 18px 20px"}}><p style={{margin:"0 0 14px",fontSize:13,color:"#625b54"}}>压缩包已加密。</p><form onSubmit={submit} style={{display:"grid",gridTemplateColumns:"1fr 96px",gap:9}}><label style={{position:"relative"}}><LockKeyhole size={15} style={{position:"absolute",left:12,top:15,color:"#8a8179"}}/><input autoComplete="off" value={pwd} onChange={e=>{setPwd(e.target.value);setError("")}} placeholder="输入密码" style={{width:"100%",height:44,padding:"0 12px 0 36px",border:"1px solid #c9c0b5",borderRadius:7,background:"#fff",fontSize:14,letterSpacing:".03em"}}/></label><button style={{border:0,borderRadius:7,background:"#5a5048",color:"#fff",cursor:"pointer"}}>解压</button></form>{error&&<em style={{display:"block",marginTop:9,color:"#a34b43",fontSize:12,fontStyle:"normal"}}>{error}</em>}</div>:
   <article style={{padding:"20px 22px 22px",fontSize:14,lineHeight:1.85,color:"#403c37"}}>
    <small style={{display:"block",color:"#8a8179",marginBottom:14}}>恢复文件：sanmen_fragment.txt · 来源字段缺失</small>
    <section style={{padding:"14px 16px",border:"1px solid #ded4c6",borderRadius:8,background:"#fff"}}>
     <p style={{margin:0}}><strong>身为舍，魂为客。</strong></p>
     <p style={{margin:"9px 0 0"}}>形可易，名可夺，忆可乱；客不可凭一门自证。</p>
     <p style={{margin:"9px 0 0"}}><strong>二客相契，两门相应。</strong></p>
     <p style={{margin:"9px 0 0"}}><strong>再舍者，故门有声。</strong></p>
    </section>
    <button onClick={()=>onCopyMaterial({id:"sanmen",title:"《三门疏》残页恢复记录",kind:"本地附件",url:"file:///Users/shenyan/Documents/archive_0712.zip"})} style={{display:"inline-flex",alignItems:"center",gap:6,marginTop:14,border:"1px solid #b8afa5",background:"#fff",borderRadius:6,padding:"8px 11px",fontSize:12,cursor:"pointer"}}><Link2 size={14}/>添加到材料</button>
   </article>}
 </section>;
}
