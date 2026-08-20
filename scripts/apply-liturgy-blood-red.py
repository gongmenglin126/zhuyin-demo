from pathlib import Path

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
'''

path.write_text(text[:start] + new_block + text[end:])

# trigger one-time workflow
