"use client";

import {FormEvent,useState} from "react";
import {FileArchive,Link2,LockKeyhole} from "lucide-react";
import type {SharedMaterial} from "./InteractiveWechat";

export default function DeepArchiveGate({onCopyMaterial}:{onCopyMaterial:(m:SharedMaterial)=>void}){
 const [pwd,setPwd]=useState(""),[error,setError]=useState(""),[unlocked,setUnlocked]=useState(false);
 const submit=(e:FormEvent)=>{
  e.preventDefault();
  if(pwd==="身非我身名非我名"){setUnlocked(true);setError("");return;}
  setError(pwd?"密码错误":"请输入密码");
 };
 return <section style={{marginTop:22,border:"1px solid #d7cec1",borderRadius:8,background:"#f6f2eb",overflow:"hidden"}}>
  <header style={{display:"flex",alignItems:"center",gap:10,padding:"12px 14px",borderBottom:"1px solid #ddd4c8",background:"#eee7dc"}}><FileArchive size={18}/><span><b style={{display:"block"}}>本地附件：archive_0712.zip</b><small style={{color:"#837a71"}}>许妍在这条私密记录里保存的本地文件链接</small></span></header>
  {!unlocked?<div style={{padding:16}}><p style={{margin:"0 0 12px",fontSize:13,color:"#625b54"}}>压缩包已加密。文件本身没有密码提示。</p><form onSubmit={submit} style={{display:"grid",gridTemplateColumns:"1fr 90px",gap:8}}><label style={{position:"relative"}}><LockKeyhole size={15} style={{position:"absolute",left:10,top:11,color:"#8a8179"}}/><input autoComplete="off" value={pwd} onChange={e=>{setPwd([...e.target.value.replace(/[，。、“”‘’\s]/g,"")].slice(0,8).join(""));setError("")}} placeholder="8 个汉字" style={{width:"100%",height:36,padding:"0 10px 0 32px",border:"1px solid #c9c0b5",borderRadius:5,background:"#fff"}}/></label><button style={{border:0,borderRadius:5,background:"#5a5048",color:"#fff",cursor:"pointer"}}>解压</button></form>{error&&<em style={{display:"block",marginTop:8,color:"#a34b43",fontSize:12,fontStyle:"normal"}}>{error}</em>}</div>:
   <article style={{padding:"16px 18px",fontSize:14,lineHeight:1.9,color:"#403c37"}}><small style={{display:"block",color:"#8a8179",marginBottom:10}}>恢复文件：sanmen_fragment.txt · 来源字段缺失</small><p>残页把人的身体称作“舍”，把其中的魂称作“客”。其中一行可辨为：<strong>身为舍，魂为客。</strong></p><p>另一段反复出现三个词：<strong>形、名、忆</strong>。原句为：“形可易，名可夺，忆可乱；客不可凭一门自证。”</p><p>后半页破损，只剩两处能连起来的短句：<strong>二客相契，两门相应</strong>；以及“<strong>再舍者，故门有声</strong>”。</p><p style={{color:"#777"}}>许妍的备注只有一句：“先别解释。把它和现实里的对应关系分开记。”</p><button onClick={()=>onCopyMaterial({id:"sanmen",title:"《三门疏》残页恢复记录",kind:"本地附件",url:"file:///Users/shenyan/Documents/archive_0712.zip"})} style={{display:"inline-flex",alignItems:"center",gap:6,border:"1px solid #b8afa5",background:"#fff",borderRadius:5,padding:"7px 10px",fontSize:12,cursor:"pointer"}}><Link2 size={14}/>复制材料链接</button></article>}
 </section>;
}
