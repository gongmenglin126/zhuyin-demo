"use client";

import {CSSProperties,ReactNode,useEffect,useState} from "react";
import {editEndingText} from "../content/endingDialogues";
import type {EndingKind} from "./endingState";

const delaySteps=(setStep:(n:number)=>void,max:number,base=1500)=>{
 const timers:number[]=[];
 for(let i=1;i<=max;i++)timers.push(window.setTimeout(()=>setStep(i),base*i+(i>3?450:0)));
 return ()=>timers.forEach(window.clearTimeout);
};

export default function GameEnding({kind}:{kind:Exclude<EndingKind,null>}){
 const [step,setStep]=useState(0);
 const [newsOpen,setNewsOpen]=useState(true);
 useEffect(()=>{if(newsOpen)return;return delaySteps(setStep,kind==="home"?8:kind==="true"?11:10,kind==="true"?1350:1500)},[kind,newsOpen]);
 return <div style={s.cover}>{newsOpen?<IncidentNews kind={kind} onClose={()=>setNewsOpen(false)}/>:kind==="home"?<HomeEnding step={step}/>:kind==="true"?<TrueEnding step={step}/>:<DoubleEnding step={step}/>}</div>;
}

function DesktopShell({children,date="10月20日 周二 22:41"}:{children:ReactNode;date?:string}){
 return <div style={s.desktop}><div style={s.sys}><span><b>●</b> 微信</span><span>Wi‑Fi　80%　{date}</span></div>{children}</div>;
}

const endingNews={
 home:{date:"2026年10月18日",weekday:"星期日",headline:"北郊仓储区一处非法拘禁点被查处　一名失联女子获救",lead:"警方根据市民提供的网络记录与场地编号，于17日晚对河临北郊第三仓储区4号库展开处置。",body:"现场救出一名此前失联的成年女性，并查获多台电脑、身份档案、采样器材及大量旧纸质资料。警方称案件仍在调查，暂未公布涉案人员身份及具体案情。获救人员已接受检查，家属已取得联系。"},
 true:{date:"2026年10月18日",weekday:"星期日",headline:"北郊仓储区非法拘禁案：两名被控制人员获救",lead:"警方在4号库及相邻隔离间发现两名成年女性，其中一人的登记身份与现场档案存在异常。",body:"两人均无生命危险。警方同时带走多台终端和纸质档案，并表示将核查更多历史记录。因其中一名获救者目前无法稳定陈述姓名与经历，相关身份信息暂不公开。"},
 double:{date:"2026年10月20日",weekday:"星期二",headline:"两名短暂失联女子已自行返家　警方终止公开寻人",lead:"此前先后失联的两名成年女性于20日返回住处，并分别与亲友取得联系。",body:"两人均表示离开期间未遭限制人身自由，也不愿继续接受媒体采访。警方称现阶段未发现需要继续公开协查的情况。有关网络传言暂无证据支持。"},
} as const;
function IncidentNews({kind,onClose}:{kind:Exclude<EndingKind,null>;onClose:()=>void}){
 const item=endingNews[kind];
 return <div style={s.newsStage}><article style={s.newsPaper}>
  <header style={s.newsTop}><span>{editEndingText(item.date)}　{editEndingText(item.weekday)}</span><span>河临 · 电子版</span></header>
  <div style={s.newsMast}>{editEndingText("河临晚报")}</div>
  <div style={s.newsSection}>{editEndingText("社会 · 本地")}</div>
  <h1 style={s.newsHeadline}>{editEndingText(item.headline)}</h1>
  <p style={s.newsLead}>{editEndingText(item.lead)}</p>
  <div style={s.newsRule}/>
  <p style={s.newsBody}>{editEndingText(item.body)}</p>
  <small style={s.newsSource}>{editEndingText("来源：河临晚报电子版 · 案件信息以警方后续通报为准")}</small>
  <button onClick={onClose} style={s.newsClose}>{editEndingText("关闭报道")}</button>
 </article></div>;
}
function WechatFrame({title="徐宁",children,draft,notice,friendRequest}:{title?:string;children:ReactNode;draft?:string;notice?:{name:string;text:string};friendRequest?:{account:string;text:string}}){
 return <><div style={s.window}><div style={s.winHead}><span>● ● ●</span><b>微信</b><span/></div><div style={s.wx}><aside style={s.side}><div style={s.me}>妍　沈妍</div><div style={s.contactActive}>{title}</div><div style={s.contact}>梁茵</div><div style={s.contact}>周川</div></aside><main style={s.chat}><header style={s.chatHead}>{title}</header><section style={s.messages}>{children}</section><footer style={s.footer}><div style={s.input}>{draft?editEndingText(draft):""}{draft!==undefined&&<i style={s.cursor}/>}</div></footer></main></div></div>{notice&&<div style={s.notice}><b>微信新消息 · {notice.name}</b><span>{editEndingText(notice.text)}</span></div>}{friendRequest&&<div style={s.friendRequest}><div style={s.friendAvatar}>?</div><span><small>新的朋友</small><b>{friendRequest.account}</b><em>验证消息：{editEndingText(friendRequest.text)}</em></span></div>}</>;
}
function Bubble({mine=false,children}:{mine?:boolean;children:ReactNode}){return <div style={{...s.bubble,...(mine?s.mine:{})}}>{typeof children==="string"?editEndingText(children):children}</div>}

function HomeEnding({step}:{step:number}){
 const draft=step<2?"":step===2?"我到底是谁":step===3?"我对徐宁到底是谁":step===4?"如果她知道了，她会怎么看我":step>=5?"徐宁，如果你知道小时候回来的人已经不是原来的沈妍了，你以后看到我的时候，会觉得我是谁":"";
 const friendRequest=step>=6?{account:"m_0317",text:"救救我。我是沈妍。你是谁？"}:undefined;
 return <DesktopShell>{step===0?<div style={s.blackDate}>2026年10月20日　22:41</div>:<WechatFrame draft={draft} friendRequest={friendRequest}><Bubble>到家了吗？</Bubble><Bubble mine>到了。</Bubble><Bubble>医生说先休息。你别乱想。</Bubble>{step>=5&&<div style={s.unsent}>消息没有发送。</div>}</WechatFrame>}{step>=8&&<EndingTitle title="归家" sub="她回到了自己的电脑前。"/>}</DesktopShell>;
}

function TrueEnding({step}:{step:number}){
 const lines=["沈妍……","不是。","林楠。","我是不是林楠……","为什么我知道徐宁这个名字……","我到底是谁啊……","为什么要这样对我……","我以前长什么样？"];
 const shown=Math.max(0,Math.min(lines.length,step-1));
 const draft=step<9?undefined:step===9?"她是不是我":step===10?"我是不是她":"我们到底谁是谁";
 return <DesktopShell date="10月21日 周三 00:18">{step===0?<div style={s.blackDate}>2026年10月21日　00:18</div>:step<9?<div style={s.recording}><div style={s.file}>OBS_19-07_1013_0317.wav</div><div style={s.wave}>▂▃▂▅▇▅▂▁▃▆▇▃▂▁▅▃▂▆▇▂▁</div><div style={s.transcript}>{lines.slice(0,shown).map((x,i)=><p key={i}>{editEndingText(x)}</p>)}</div><small>内部问询录音 · 自动转写</small></div>:<WechatFrame draft={draft}><Bubble>你睡了吗？</Bubble><Bubble mine>没有。</Bubble>{step>=11&&<div style={s.unsent}>消息没有发送。</div>}</WechatFrame>}{step>=11&&<EndingTitle title="谁是我" sub="两个名字都还在，答案没有。"/>}</DesktopShell>;
}

function DoubleEnding({step}:{step:number}){
 return <DesktopShell date="10月20日 周二 23:06">{step===0?<div style={s.blackDate}>三天后　23:06</div>:<WechatFrame title="梁茵" notice={step>=6?{name:"徐宁",text:"到了。"}:undefined}><Bubble>沈妍？？？</Bubble><Bubble>你终于回来了？</Bubble><Bubble>徐宁呢？她这几天也联系不上。</Bubble>{step>=3&&<Bubble mine>我没事。</Bubble>}{step>=4&&<Bubble mine>她也没事。</Bubble>}{step>=5&&<Bubble>你说话怎么怪怪的。</Bubble>}{step>=7&&<Bubble mine>你以前不是一直想知道，小时候回来以后为什么会觉得家里不对吗。</Bubble>}{step>=8&&<Bubble mine>周末来吧。有人会告诉你。</Bubble>}{step>=9&&<Bubble mine>无相还真，舍身无量。</Bubble>}</WechatFrame>}{step>=10&&<EndingTitle title="双归" sub="两个人都回来了。"/>}</DesktopShell>;
}

function EndingTitle({title,sub}:{title:string;sub:string}){return <div style={s.ending}><small>{editEndingText(sub)}</small><h1>《{editEndingText(title)}》</h1></div>}

const s:Record<string,CSSProperties>={
 cover:{position:"fixed",inset:0,zIndex:10000,background:"#050505",color:"#eee",userSelect:"none"},
 newsStage:{position:"absolute",inset:0,display:"grid",placeItems:"center",padding:"4vh 5vw",boxSizing:"border-box",background:"radial-gradient(circle at 50% 28%,#403d36 0,#1b1a18 46%,#090909 100%)"},
 newsPaper:{position:"relative",width:"min(880px,92vw)",maxHeight:"88vh",overflow:"auto",boxSizing:"border-box",padding:"26px 38px 34px",background:"#eee9dc",color:"#1b1b18",border:"1px solid #aaa28f",boxShadow:"0 28px 100px #000c",fontFamily:'Georgia,"Songti SC","SimSun",serif'},
 newsTop:{display:"flex",justifyContent:"space-between",paddingBottom:8,borderBottom:"1px solid #8d8779",fontSize:11,color:"#666052"},
 newsMast:{padding:"13px 0 8px",borderBottom:"4px double #37352f",textAlign:"center",fontSize:42,fontWeight:900,letterSpacing:".26em"},
 newsSection:{marginTop:18,fontSize:12,fontWeight:800,letterSpacing:".16em",color:"#736b5e"},
 newsHeadline:{margin:"10px 0 12px",fontSize:"clamp(28px,4vw,46px)",lineHeight:1.18,fontWeight:900,letterSpacing:".02em"},
 newsLead:{margin:"0 0 15px",fontSize:16,lineHeight:1.75,fontWeight:700,color:"#3b3934"},
 newsRule:{height:1,background:"#908878",margin:"15px 0"},
 newsBody:{margin:0,fontSize:15,lineHeight:2,textAlign:"justify",color:"#34322e"},
 newsSource:{display:"block",marginTop:22,paddingTop:11,borderTop:"1px solid #c2bbab",fontSize:10,color:"#847c6d"},
 newsClose:{position:"sticky",float:"right",bottom:0,marginTop:20,padding:"8px 15px",border:"1px solid #797266",background:"#24231f",color:"#f4efe3",fontSize:12,fontWeight:700,cursor:"pointer"},
 desktop:{position:"absolute",inset:0,overflow:"hidden",background:"radial-gradient(circle at 45% 35%,#333944 0,#1c222b 35%,#0b0d11 100%)"},
 sys:{height:34,display:"flex",justifyContent:"space-between",alignItems:"center",padding:"0 14px",background:"#111b",fontSize:12,backdropFilter:"blur(10px)"},
 blackDate:{position:"absolute",inset:34,display:"grid",placeItems:"center",background:"#050505",fontSize:18,letterSpacing:".12em",color:"#aaa"},
 window:{position:"absolute",left:"7%",right:"7%",top:"9%",bottom:"8%",border:"1px solid #333",borderRadius:10,overflow:"hidden",background:"#f5f5f5",boxShadow:"0 28px 80px #000b",color:"#222"},
 winHead:{height:38,display:"grid",gridTemplateColumns:"1fr auto 1fr",alignItems:"center",padding:"0 12px",background:"#ececec",borderBottom:"1px solid #d0d0d0",fontSize:12},
 wx:{height:"calc(100% - 38px)",display:"grid",gridTemplateColumns:"210px 1fr"},
 side:{padding:12,display:"grid",alignContent:"start",gap:4,background:"#e6e6e6",borderRight:"1px solid #ccc",fontSize:12},
 me:{padding:"12px 10px",fontWeight:700,borderBottom:"1px solid #ccc",marginBottom:8},
 contactActive:{padding:"11px 10px",background:"#d2d2d2",borderRadius:5,fontWeight:700},contact:{padding:"10px"},
 chat:{display:"flex",flexDirection:"column",minWidth:0},chatHead:{height:48,display:"flex",alignItems:"center",padding:"0 18px",borderBottom:"1px solid #ddd",fontWeight:700},
 messages:{flex:1,padding:"20px 28px",overflow:"hidden",background:"#f3f3f3"},
 bubble:{width:"fit-content",maxWidth:"62%",margin:"0 0 12px",padding:"10px 13px",borderRadius:6,background:"#fff",fontSize:14,lineHeight:1.55,boxShadow:"0 1px 2px #0001"},mine:{marginLeft:"auto",background:"#95ec69"},
 footer:{height:84,padding:12,borderTop:"1px solid #ddd",background:"#fafafa"},input:{minHeight:54,padding:"10px 12px",background:"#fff",border:"1px solid #ddd",borderRadius:6,fontSize:14,lineHeight:1.6},cursor:{display:"inline-block",width:1,height:"1.1em",marginLeft:2,verticalAlign:"-2px",background:"#333"},
 notice:{position:"absolute",right:18,top:48,width:340,padding:"14px 16px",border:"2px solid #49a96b",borderRadius:10,background:"#fff",color:"#222",boxShadow:"0 16px 45px #0007",display:"grid",gap:5},
 friendRequest:{position:"absolute",right:18,top:48,width:380,display:"grid",gridTemplateColumns:"46px 1fr",gap:12,alignItems:"center",padding:"14px 16px",border:"1px solid #d8d8d8",borderRadius:10,background:"#fff",color:"#222",boxShadow:"0 16px 45px #0007"},
 friendAvatar:{width:46,height:46,display:"grid",placeItems:"center",borderRadius:7,background:"#dadada",color:"#777",fontSize:23,fontWeight:800},
 friendRequestSpan:{display:"grid"},
 unsent:{margin:"14px 0",textAlign:"center",fontSize:11,color:"#999"},
 recording:{position:"absolute",left:"12%",right:"12%",top:"14%",bottom:"12%",padding:"28px 32px",border:"1px solid #303030",borderRadius:8,background:"#111",boxShadow:"0 25px 80px #000",color:"#ddd"},file:{fontFamily:"monospace",fontSize:13,color:"#aaa"},wave:{margin:"24px 0",fontSize:34,letterSpacing:3,color:"#a74b45",whiteSpace:"nowrap",overflow:"hidden"},transcript:{minHeight:300,fontSize:17,lineHeight:1.9},
 ending:{position:"absolute",inset:0,display:"grid",placeContent:"center",textAlign:"center",background:"#000e",zIndex:20},
};
