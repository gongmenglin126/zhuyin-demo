"use client";

import {FormEvent,useState} from "react";
import {ExternalLink,FileArchive,LockKeyhole} from "lucide-react";

export default function LocalVault({unlocked,onUnlock,openLink}:{unlocked:boolean;onUnlock:()=>void;openLink:()=>void}){
  const [pwd,setPwd]=useState("");
  const [error,setError]=useState("");
  const [deepPwd,setDeepPwd]=useState("");
  const [deepError,setDeepError]=useState("");
  const [deepUnlocked,setDeepUnlocked]=useState(false);

  const submit=(e:FormEvent)=>{
    e.preventDefault();
    if(pwd==="红铁皮盒"){
      setError("");
      onUnlock();
      return;
    }
    setError(pwd?"口令不正确":"请输入口令");
  };
  const submitDeep=(e:FormEvent)=>{
    e.preventDefault();
    if(deepPwd==="身非我身名非我名"){
      setDeepError("");
      setDeepUnlocked(true);
      return;
    }
    setDeepError(deepPwd?"密码错误":"请输入密码");
  };

  if(unlocked){
    return <main style={{...styles.page,overflow:"auto",placeItems:"start center"}}>
      <section style={{...styles.card,width:"min(620px,92%)",margin:"26px 0",textAlign:"left"}}>
        <div style={{display:"flex",alignItems:"center",gap:12,marginBottom:18}}><div style={{...styles.lockMark,margin:0}}><LockKeyhole size={24}/></div><div><small style={styles.eyebrow}>本地缓存 · 已解锁</small><h2 style={{...styles.title,margin:0}}>保存的缓存页</h2></div></div>
        <p style={{...styles.copy,margin:"0 0 14px"}}>一条被单独锁起来的旧站缓存。</p>
        <div style={styles.address}>https://www.zhuyinwen.cn/archive/cache/baishesong-1986.html</div>
        <button style={styles.primary} onClick={openLink}><ExternalLink size={16}/>打开缓存页面</button>
      </section>

      <section style={{...styles.card,width:"min(620px,92%)",margin:"0 0 34px",textAlign:"left"}}>
        <div style={{display:"flex",alignItems:"center",gap:12,marginBottom:18}}><div style={{...styles.lockMark,margin:0,background:"#5b5149"}}><FileArchive size={24}/></div><div><small style={styles.eyebrow}>旧站附件 · 加密压缩包</small><h2 style={{...styles.title,margin:0}}>archive_0712.zip</h2></div></div>
        {!deepUnlocked?<>
          <p style={{...styles.copy,margin:"0 0 16px"}}>压缩包需要密码。这里没有额外的密码提示。</p>
          <form onSubmit={submitDeep} style={styles.form}>
            <input autoComplete="off" aria-label="八个字压缩包密码" value={deepPwd} onChange={e=>{setDeepPwd([...e.target.value.replace(/[，。、“”‘’\s]/g,"")].slice(0,8).join(""));setDeepError("")}} style={{...styles.input,letterSpacing:".18em"}} placeholder="••••••••"/>
            <button style={styles.primary}>解压</button>
          </form>
          {deepError&&<em style={styles.error}>{deepError}</em>}
        </>:<article style={{fontSize:14,lineHeight:1.9,color:"#403d38"}}>
          <small style={{display:"block",color:"#888",marginBottom:10}}>恢复文件：sanmen_fragment.txt · 来源字段缺失</small>
          <p>残页把人的身体称作“舍”，把其中的魂称作“客”。其中一行可辨为：<strong>身为舍，魂为客。</strong></p>
          <p>另一段反复出现三个词：<strong>形、名、忆</strong>。原句为：“形可易，名可夺，忆可乱；客不可凭一门自证。”</p>
          <p>后半页破损，只剩两处能连起来的短句：<strong>二客相契，两门相应</strong>；以及“<strong>再舍者，故门有声</strong>”。</p>
          <p style={{color:"#777"}}>没有标题全文，也没有年代。文件旁只保留了许妍的一句备注：<br/>“先别解释。把它和现实里的对应关系分开记。”</p>
        </article>}
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
