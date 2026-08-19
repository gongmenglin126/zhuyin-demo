"use client";

import {useEffect,useMemo,useState} from "react";
import type {EndingKind} from "./endingState";

const delaySteps=(setStep:(n:number)=>void,max:number,base=1500)=>{
 const timers:number[]=[];
 for(let i=1;i<=max;i++)timers.push(window.setTimeout(()=>setStep(i),base*i+(i>3?450:0)));
 return ()=>timers.forEach(window.clearTimeout);
};

export default function GameEnding({kind}:{kind:Exclude<EndingKind,null>}){
 const [step,setStep]=useState(0);
 useEffect(()=>delaySteps(setStep,kind==="home"?8:kind==="true"?11:10,kind==="true"?1350:1500),[kind]);
 return <div style={s.cover}>{kind==="home"?<HomeEnding step={step}/>:kind==="true"?<TrueEnding step={step}/>:<DoubleEnding step={step}/>}</div>;
}

function DesktopShell({children,date="10月20日 周二 22:41"}:{children:React.ReactNode;date?:string}){
 return <div style={s.desktop}><div style={s.sys}><span><b>●</b> 微信</span><span>Wi‑Fi　80%　{date}</span></div>{children}</div>;
}
function WechatFrame({title="徐宁",children,draft,notice}:{title?:string;children:React.ReactNode;draft?:string;notice?:{name:string;text:string}}){
 return <><div style={s.window}><div style={s.winHead}><span>● ● ●</span><b>微信</b><span/></div><div style={s.wx}><aside style={s.side}><div style={s.me}>妍　沈妍</div><div style={s.contactActive}>{title}</div><div>梁茵</div><div>周川</div></aside><main style={s.chat}><header style={s.chatHead}>{title}</header><section style={s.messages}>{children}</section><footer style={s.footer}><div style={s.input}>{draft||""}{draft!==undefined&&<i style={s.cursor}/>}</div></footer></main></div></div>{notice&&<div style={s.notice}><b>微信新消息 · {notice.name}</b><span>{notice.text}</span></div>}</>;
}
function Bubble({mine=false,children}:{mine?:boolean;children:React.ReactNode}){return <div style={{...s.bubble,...(mine?s.mine:{})}}>{children}</div>}

function HomeEnding({step}:{step:number}){
 const draft=step<2?"":step===2?"我到底是谁":step===3?"我对徐宁到底是谁":step===4?"如果她知道了，她会怎么看我":step>=5?"徐宁，如果你知道小时候回来的人已经不是原来的沈妍了，你以后看到我的时候，会觉得我是谁":"";
 const notice=step>=7?{name:"林楠",text:"救救我"}:step>=6?{name:"林楠",text:"怎么办":"" as never}:undefined;
 return <DesktopShell>{step===0?<div style={s.blackDate}>2026年10月20日　22:41</div>:<WechatFrame draft={draft} notice={notice&&{name:notice.name,text:step>=7?"救救我":"怎么办"}}><Bubble>到家了吗？</Bubble><Bubble mine>到了。</Bubble><Bubble>医生说先休息。你别乱想。</Bubble>{step>=5&&<div style={s.unsent}>消息没有发送。</div>}</WechatFrame>}{step>=8&&<EndingTitle title="归家" sub="她回到了自己的电脑前。"/>}</DesktopShell>;
}

function TrueEnding({step}:{step:number}){
 const lines=["沈妍……","不是。","林楠。","我是不是林楠……","为什么我知道徐宁这个名字……","我到底是谁啊……","为什么要这样对我……","我以前长什么样？"];
 const shown=Math.max(0,Math.min(lines.length,step-1));
 const draft=step<9?undefined:step===9?"她是不是我":step===10?"我是不是她":"我们到底谁是谁";
 return <DesktopShell date="10月21日 周三 00:18">{step===0?<div style={s.blackDate}>2026年10月21日　00:18</div>:step<9?<div style={s.recording}><div style={s.file}>OBS_19-07_1013_0317.wav</div><div style={s.wave}>▂▃▂▅▇▅▂▁▃▆▇▃▂▁▅▃▂▆▇▂▁</div><div style={s.transcript}>{lines.slice(0,shown).map((x,i)=><p key={i}>{x}</p>)}</div><small>内部问询录音 · 自动转写</small></div>:<WechatFrame draft={draft}><Bubble>你睡了吗？</Bubble><Bubble mine>没有。</Bubble>{step>=11&&<div style={s.unsent}>消息没有发送。</div>}</WechatFrame>}{step>=11&&<EndingTitle title="谁是我" sub="两个名字都还在，答案没有。"/>}</DesktopShell>;
}

function DoubleEnding({step}:{step:number}){
 return <DesktopShell date="10月20日 周二 23:06">{step===0?<div style={s.blackDate}>三天后　23:06</div>:<WechatFrame title="梁茵" notice={step>=6?{name:"徐宁",text:"到了。"}:undefined}><Bubble>沈妍？？？</Bubble><Bubble>你终于回来了？</Bubble><Bubble>徐宁呢？她这几天也联系不上。</Bubble>{step>=3&&<Bubble mine>我没事。</Bubble>}{step>=4&&<Bubble mine>她也没事。</Bubble>}{step>=5&&<Bubble>你说话怎么怪怪的。</Bubble>}{step>=7&&<Bubble mine>你以前不是一直想知道，小时候回来以后为什么会觉得家里不对吗。</Bubble>}{step>=8&&<Bubble mine>周末来吧。有人会告诉你。</Bubble>}{step>=9&&<Bubble mine>无相还真，舍身无量。</Bubble>}</WechatFrame>}{step>=10&&<EndingTitle title="双归" sub="两个人都回来了。"/>}</DesktopShell>;
}

function EndingTitle({title,sub}:{title:string;sub:string}){return <div style={s.ending}><small>{sub}</small><h1>《{title}》</h1></div>}

const s:Record<string,React.CSSProperties>={
 cover:{position:"fixed",inset:0,zIndex:10000,background:"#050505",color:"#eee",userSelect:"none"},desktop:{position:"absolute",inset:0,overflow:"hidden",background:"radial-gradient(circle at 45% 35%,#333944 0,#1c222b 35%,#0b0d11 100%)"},sys:{height:34,display:"flex",justifyContent:"space-between",alignItems:"center",padding:"0 14px",background:"#111b",fontSize:12,backdropFilter:"blur(10px)"},blackDate:{position:"absolute",inset:34,display:"grid",placeItems:"center",background:"#050505",fontSize:18,letterSpacing:".12em",color:"#aaa"},window:{position:"absolute",left:"7%",right:"7%",top:"9%",bottom:"8%",border:"1px solid #333",borderRadius:10,overflow:"hidden",background:"#f5f5f5",boxShadow:"0 28px 80px #000b",color:"#222"},winHead:{height:38,display:"grid",gridTemplateColumns:"1fr auto 1fr",alignItems:"center",padding:"0 12px",background:"#ececec",borderBottom:"1px solid #d0d0d0",fontSize:12},wx:{height:"calc(100% - 38px)",display:"grid",gridTemplateColumns:"210px 1fr"},side:{padding:12,display:"grid",alignContent:"start",gap:4,background:"#e6e6e6",borderRight:"1px solid #ccc",fontSize:12},me:{padding:"12px 10px",fontWeight:700,borderBottom:"1px solid #ccc",marginBottom:8},contactActive:{padding:"11px 10px",background:"#d2d2d2",borderRadius:5,fontWeight:700},chat:{display:"flex",flexDirection:"column",minWidth:0},chatHead:{height:48,display:"flex",alignItems:"center",padding:"0 18px",borderBottom:"1px solid #ddd",fontWeight:700},messages:{flex:1,padding:"20px 28px",overflow:"hidden",background:"#f3f3f3"},bubble:{width:"fit-content",maxWidth:"62%",margin:"0 0 12px",padding:"10px 13px",borderRadius:6,background:"#fff",fontSize:14,lineHeight:1.55,boxShadow:"0 1px 2px #0001"},mine:{marginLeft:"auto",background:"#95ec69"},footer:{height:84,padding:12,borderTop:"1px solid #ddd",background:"#fafafa"},input:{minHeight:54,padding:"10px 12px",background:"#fff",border:"1px solid #ddd",borderRadius:6,fontSize:14,lineHeight:1.6},cursor:{display:"inline-block",width:1,height:"1.1em",marginLeft:2,verticalAlign:"-2px",background:"#333",animation:"blink 1s step-end infinite"},notice:{position:"absolute",right:18,top:48,width:340,padding:"14px 16px",border:"2px solid #49a96b",borderRadius:10,background:"#fff",color:"#222",boxShadow:"0 16px 45px #0007"},notice:{},unsent:{margin:"14px 0",textAlign:"center",fontSize:11,color:"#999"},recording:{position:"absolute",left:"12%",right:"12%",top:"14%",bottom:"12%",padding:"28px 32px",border:"1px solid #303030",borderRadius:8,background:"#111",boxShadow:"0 25px 80px #000",color:"#ddd"},file:{fontFamily:"monospace",fontSize:13,color:"#aaa"},wave:{margin:"24px 0",fontSize:34,letterSpacing:3,color:"#a74b45",whiteSpace:"nowrap",overflow:"hidden"},transcript:{minHeight:300,fontSize:17,lineHeight:1.9},ending:{position:"absolute",inset:0,display:"grid",placeContent:"center",textAlign:"center",background:"#000e",zIndex:20},ending:{},
};
