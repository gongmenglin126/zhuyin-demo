"use client";

import {FormEvent,useState} from "react";
import {ExternalLink,LockKeyhole} from "lucide-react";

export default function LocalVault({unlocked,onUnlock,openLink}:{unlocked:boolean;onUnlock:()=>void;openLink:()=>void}){
  const [pwd,setPwd]=useState("");
  const [error,setError]=useState("");

  const submit=(e:FormEvent)=>{
    e.preventDefault();
    if(pwd==="红铁皮盒"){
      setError("");
      onUnlock();
      return;
    }
    setError(pwd?"口令不正确":"请输入口令");
  };

  if(unlocked){
    return <main style={styles.page}>
      <section style={styles.card}>
        <div style={styles.lockMark}><LockKeyhole size={26}/></div>
        <small style={styles.eyebrow}>本地缓存 · 已解锁</small>
        <h2 style={styles.title}>保存的缓存页</h2>
        <p style={styles.copy}>一条被单独锁起来的本地记录。</p>
        <div style={styles.address}>https://www.zhuyinwen.cn/archive/cache/baishesong-1986.html</div>
        <button style={styles.primary} onClick={openLink}><ExternalLink size={16}/>打开缓存页面</button>
      </section>
    </main>;
  }

  return <main style={styles.page}>
    <section style={styles.card}>
      <div style={styles.lockMark}><LockKeyhole size={26}/></div>
      <small style={styles.eyebrow}>受保护的本地页面</small>
      <h2 style={styles.title}>需要访问口令</h2>
      <div style={styles.hint}>
        <span><b>口令提示</b>　打开前会卡一下</span>
        <small>4 个汉字</small>
      </div>
      <form onSubmit={submit} style={styles.form}>
        <input autoFocus autoComplete="off" aria-label="四个字访问口令" value={pwd} onChange={e=>{setPwd([...e.target.value.replace(/[，。、“”‘’\s]/g,"")].slice(0,4).join(""));setError("")}} style={styles.input} placeholder="••••"/>
        <button style={styles.primary}>解锁</button>
      </form>
      {error&&<em style={styles.error}>{error}</em>}
    </section>
  </main>;
}

const styles:{[key:string]:React.CSSProperties}={
  page:{height:"calc(100% - 39px)",display:"grid",placeItems:"center",padding:"36px",background:"linear-gradient(145deg,#ece9e2 0%,#e2e0da 100%)",color:"#252925"},
  card:{width:"min(520px,92%)",padding:"42px 44px 38px",border:"1px solid #cbc7be",borderRadius:"14px",background:"rgba(250,249,246,.96)",boxShadow:"0 22px 70px rgba(37,41,37,.13)",textAlign:"center"},
  lockMark:{width:"54px",height:"54px",display:"grid",placeItems:"center",margin:"0 auto 16px",borderRadius:"50%",background:"#3d554d",color:"#fff",boxShadow:"0 8px 24px rgba(61,85,77,.2)"},
  eyebrow:{display:"block",marginBottom:"6px",color:"#89857d",fontSize:"10px",letterSpacing:".14em"},
  title:{margin:"0 0 22px",fontSize:"24px",fontWeight:700,letterSpacing:".03em"},
  copy:{margin:"-10px 0 22px",color:"#77736c",fontSize:"13px"},
  hint:{display:"grid",gap:"7px",margin:"0 0 20px",padding:"14px 16px",border:"1px solid #ded9cf",borderRadius:"9px",background:"#f1eee8",textAlign:"left",color:"#5e5a53",fontSize:"12px",lineHeight:1.65},
  form:{display:"grid",gridTemplateColumns:"1fr 92px",gap:"9px"},
  input:{minWidth:0,padding:"12px 14px",border:"1px solid #bdb8ad",borderRadius:"7px",background:"#fff",outline:"none",fontSize:"16px",letterSpacing:".35em",textAlign:"center",color:"#252925"},
  primary:{minHeight:"43px",display:"inline-flex",alignItems:"center",justifyContent:"center",gap:"7px",padding:"0 18px",border:0,borderRadius:"7px",background:"#3d554d",color:"#fff",fontSize:"13px",cursor:"pointer"},
  error:{display:"block",marginTop:"12px",color:"#9c4037",fontSize:"11px",fontStyle:"normal"},
  address:{margin:"0 0 16px",padding:"13px 14px",border:"1px solid #ddd8ce",borderRadius:"8px",background:"#f2efe9",color:"#4b5e79",font:"12px ui-monospace,SFMono-Regular,Consolas,monospace"}
};
