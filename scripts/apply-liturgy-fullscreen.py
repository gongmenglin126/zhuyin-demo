from pathlib import Path

# trigger fullscreen liturgy build
path = Path("app/AdminPortalOccult.tsx")
text = path.read_text()
start = text.index("let liturgyBurned=false;\nfunction Liturgy(){")
end = text.index("\nfunction CandidateLibrary(){", start)

new_block = r'''let liturgyBurned=false;
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
 const fullLine=(n:number,text:string,top:string,size:string,spacing:string)=>{
  const visible=step>=n&&step!==99;
  const active=step===n;
  return <p style={{position:"absolute",left:"50%",top,width:"100%",margin:0,transform:`translate(-50%,-50%) scale(${active?1.04:1})`,padding:"0 5vw",boxSizing:"border-box",opacity:visible?1:0,color:active?"#e2d9cf":"#766760",fontFamily:"serif",fontSize:size,fontWeight:700,lineHeight:1.08,letterSpacing:spacing,textAlign:"center",textShadow:active?"0 0 30px #8e281f66,0 0 80px #55100d55":"0 0 16px #000",transition:"opacity .7s ease, transform 1.1s ease, color .7s ease"}}>{editAdminText(text)}</p>;
 };
 if(step===99)return <section onClick={()=>setDismissed(true)} style={{position:"fixed",inset:0,zIndex:9999,display:"grid",placeItems:"center",background:"#000",cursor:"default",boxShadow:"inset 0 0 180px #000"}}><span style={{color:"#151515",font:"11px ui-monospace,SFMono-Regular,Consolas,monospace",letterSpacing:".18em"}}>ERR_ARCHIVE_410</span><small style={{position:"fixed",right:22,bottom:18,color:"#161616",font:"10px ui-monospace,SFMono-Regular,Consolas,monospace",letterSpacing:".12em"}}>ESC</small></section>;
 return <section style={{position:"fixed",inset:0,zIndex:9999,overflow:"hidden",background:"radial-gradient(circle at 50% 46%,#160d0b 0%,#080606 34%,#020202 72%,#000 100%)",color:"#d8cec5",boxShadow:"inset 0 0 220px #000"}}>
  <div style={{position:"absolute",inset:0,opacity:.22,background:"repeating-linear-gradient(180deg,transparent 0,transparent 3px,#ffffff05 4px,#ffffff05 5px)",pointerEvents:"none"}}/>
  <small style={{position:"absolute",left:24,top:20,color:"#3d302d",font:"10px ui-monospace,SFMono-Regular,Consolas,monospace",letterSpacing:".22em"}}>ARCHIVE / LITURGY_07</small>
  {fullLine(1,"身为舍。","19%","clamp(34px,5.6vw,82px)",".18em")}
  {fullLine(2,"魂为客。","36%","clamp(40px,6.8vw,98px)",".20em")}
  {fullLine(3,"名可弃。","54%","clamp(48px,8.4vw,124px)",".24em")}
  {fullLine(4,"舍可更。","73%","clamp(58px,10.5vw,156px)",".28em")}
  {step>=5&&<div style={{position:"absolute",left:"50%",top:"88%",transform:"translate(-50%,-50%)",width:"min(900px,88vw)",padding:"14px 18px",boxSizing:"border-box",borderTop:"1px solid #222",borderBottom:"1px solid #222",background:"#000d",color:"#e4e4e4",font:"700 clamp(13px,1.6vw,20px) ui-monospace,SFMono-Regular,Consolas,monospace",letterSpacing:".07em",textAlign:"center",boxShadow:"0 0 80px #000",animation:"none"}}>{editAdminText("访问者徐宁，未登记候舍编号。")}</div>}
 </section>;
}
'''

path.write_text(text[:start] + new_block + text[end:])
