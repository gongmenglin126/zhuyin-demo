"use client";

import {FormEvent,useEffect,useMemo,useRef,useState} from "react";
import {Link2,Search,Send,X} from "lucide-react";

export type SharedMaterial={id:string;title:string;kind:string;url:string};
type Msg={time?:string;who:"沈妍"|"对方";text:string;material?:SharedMaterial};
type Contact={id:string;name:string;preview:string;messages:Msg[]};
type MaterialRule=Record<string,string|null>;

const contacts:Contact[]=[
 {id:"x",name:"徐宁",preview:"我去你家看看。",messages:[
  {time:"10月16日 11:26",who:"对方",text:"明天中午老地方？这次别临时加活啊。"},
  {who:"沈妍",text:"不会，保证准时。我要是迟到就请你吃一个月。"},
  {who:"对方",text:"截图了。"},
  {time:"10月16日 19:48",who:"沈妍",text:"我先出去一趟，明天还是靠窗那桌。"},
  {time:"今天 12:02",who:"对方",text:"我到了，你人呢？"},
  {time:"今天 12:37",who:"对方",text:"电话也不接。看到回我。"},
  {time:"今天 18:37",who:"对方",text:"我去你家看看。"},
 ]},
 {id:"yq",name:"余晴",preview:"等下见",messages:[
  {time:"10月16日 19:31",who:"对方",text:"到了？"},
  {who:"沈妍",text:"嗯"},
  {who:"对方",text:"我还有十分钟"},
  {who:"沈妍",text:"好"},
  {who:"对方",text:"等下见"},
 ]},
 {id:"zc",name:"周川",preview:"先把原始记录留好。",messages:[
  {time:"10月12日 22:08",who:"对方",text:"梦里的称呼还是只有最后两个音？"},
  {who:"沈妍",text:"嗯，我没敢补字。"},
  {who:"对方",text:"对。先把原始记录留好。回来后突然怕什么、以前会做后来不会什么，也分开记，别混成一个解释。"},
  {who:"沈妍",text:"知道。我现在只记时间和原句。"},
 ]},
 {id:"ly",name:"梁茵",preview:"公开区别写真名。",messages:[
  {time:"9月28日 00:42",who:"对方",text:"我不太想在论坛公开区继续说那个名字的问题。"},
  {who:"沈妍",text:"可以。你不想说的我不会追问。"},
  {who:"对方",text:"如果你后面真查旧报，公开区别写真名，也别发找到我的城市。"},
  {who:"沈妍",text:"好。"},
 ]},
 {id:"f",name:"方嘉",preview:"周一的表我先替你交？",messages:[
  {time:"昨天",who:"对方",text:"甲方又改表头了，我真的服。"},
  {who:"沈妍",text:"先别动，我明早统一格式。"},
  {time:"今天",who:"对方",text:"周一的表我先替你交？"},
 ]},
 {id:"p",name:"爸妈",preview:"下周回来吃饭吗",messages:[
  {time:"8月20日",who:"对方",text:"下周回来吃饭吗，你爸买了排骨。"},
  {who:"沈妍",text:"看加班，确定了跟你说。"},
  {who:"对方",text:"少熬夜。"},
 ]},
];

// 只有这些“材料 × 联系人”组合允许发送；null 代表消息能发出去，但对方不会立刻回复。
const materialRules:Record<string,MaterialRule>={
  "33897":{
    yq:null,
    zc:"户型和梦里结构能对上，值得查；但先找原始记录，不要拿熟悉感证明她去过。",
  },
  "09114":{
    zc:"把失踪日期、找回日期、年龄和找回后的变化分开记。尤其不要因为两个案子接近，就先设成同一作案者。",
    ly:"……你怎么查到林楠这个名字的？先别在公开区发。",
  },
  "09831":{
    zc:"这条你自己的旧报也要按同样标准处理。家人口述和原报分开。",
    ly:null,
  },
  "10731":{
    zc:"这篇楼主的结论是对的：目前只能证明两起案子很接近，不能证明同因。",
    ly:"我以前看到这篇时只当巧合。现在再看，确实有点不舒服。",
  },
  "14692":{
    ly:"这条我看过。那种‘名字叫错了’的感觉不是只有她有。",
  },
  verse:{
    zc:"这张残页来源字段没了。先找同句异文，尤其是‘身’‘名’这些词，别直接按现代意义解释。",
    ly:"‘身非我身，名非我名’这句我见过。不是在公开帖正文里，是别人发给我的一张旧纸截图。",
  },
  sanmen:{
    zc:"如果‘舍’‘客’是这个文本自己的术语，先确认别处是不是也把身体叫舍、魂叫客。‘二客’只能说明它在谈两个主体，还不能自动等于交换。",
    ly:"我见过‘客’这个词。以前有人问我走失回来以后会不会梦到‘故门’，我当时只觉得他说话很怪。你先别把它解释成换魂，但这套词和那些问题确实像是一套东西。",
  },
};

const textReply=(contact:string,text:string):string|null=>{
 const t=text.replace(/\s/g,"");
 if(contact==="yq"){
  if(/昨晚|见面|去哪|在哪/.test(t))return "昨天见到她了。后来她说还有点事，我就先走了。我以为她回家了。";
  if(/林楠/.test(t))return "这个名字我真没听她说过。";
 }
 if(contact==="zc"){
  if(/林楠/.test(t))return "先别围着名字猜。把两份旧报的日期、年龄、找回地点列出来。";
  if(/失踪|不见了|联系不上/.test(t))return "如果现实里确实联系不上，先走正常报警和亲友确认。论坛材料不要代替现实证据。";
  if(/换魂|灵魂|交换/.test(t))return "这是解释，不是事实。先找能区分‘创伤记忆’和‘身份错位’的材料。";
 }
 if(contact==="ly"){
  if(/林楠/.test(t))return "别在这个号里反复写真名。你如果已经看到旧报，就继续查她回来后最早的变化。";
  if(/名字|另一个家|不会/.test(t))return "我能确认的是：有些人回来后真的会觉得名字不对，也有人突然不会以前会的东西。原因我不知道。";
  if(/换魂|灵魂|交换/.test(t))return "我以前也这么猜过，但只有感觉不算证据。你得先解释为什么两个人的‘错位’会互相对应。";
 }
 return null;
};

export default function InteractiveWechat({materials}:{materials:SharedMaterial[]}){
 const [id,setId]=useState("x"),[q,setQ]=useState(""),[draft,setDraft]=useState(""),[picker,setPicker]=useState(false);
 const [extra,setExtra]=useState<Record<string,Msg[]>>({});
 const scrollRef=useRef<HTMLElement|null>(null);
 const contact=contacts.find(x=>x.id===id)!;
 const visible=contacts.filter(x=>(x.name+x.preview).includes(q));
 const messages=useMemo(()=>[...contact.messages,...(extra[id]||[])],[contact,extra,id]);
 const sendable=useMemo(()=>materials.filter(m=>Object.prototype.hasOwnProperty.call(materialRules[m.id]||{},id)),[materials,id]);
 const append=(items:Msg[])=>setExtra(prev=>({...prev,[id]:[...(prev[id]||[]),...items]}));

 useEffect(()=>{
  const el=scrollRef.current;
  if(el)el.scrollTop=el.scrollHeight;
 },[id,messages.length]);
 useEffect(()=>setPicker(false),[id]);

 const sendText=(e:FormEvent)=>{
  e.preventDefault();
  const text=draft.trim(); if(!text||id==="x")return;
  const reply=textReply(id,text);
  append([{who:"沈妍",text},...(reply?[{who:"对方" as const,text:reply}]:[])]);
  setDraft("");
 };
 const sendMaterial=(material:SharedMaterial)=>{
  const rules=materialRules[material.id];
  if(!rules||!Object.prototype.hasOwnProperty.call(rules,id))return;
  const reply=rules[id];
  append([
    {who:"沈妍",text:`[分享] ${material.title}`,material},
    ...(reply?[{who:"对方" as const,text:reply}]:[]),
  ]);
  setPicker(false);
 };

 return <div className="wechat" style={{height:"100%",minHeight:0,overflow:"hidden"}}>
  <aside style={{height:"100%",minHeight:0,overflowY:"auto"}}><header><i>妍</i><span><b>沈妍</b><small>微信已登录</small></span></header><label><Search/><input value={q} onChange={e=>setQ(e.target.value)} placeholder="搜索联系人和消息"/></label>{visible.map(x=><button className={x.id===id?"active":""} onClick={()=>setId(x.id)} key={x.id}><i>{x.name[0]}</i><span><b>{x.name}</b><small>{x.preview}</small></span></button>)}</aside>
  <main style={{height:"100%",minHeight:0,display:"flex",flexDirection:"column",overflow:"hidden",position:"relative"}}>
   <header style={{flex:"0 0 auto"}}><b>{contact.name}</b><small>聊天记录</small></header>
   <section ref={scrollRef} style={{flex:"1 1 auto",minHeight:0,overflowY:"auto",overscrollBehavior:"contain"}}>{messages.map((m,i)=><div key={i}>{m.time&&<time>{m.time}</time>}<article className={m.who==="沈妍"?"mine":""}><i>{m.who==="沈妍"?"妍":contact.name[0]}</i><p>{m.material?<><b style={{display:"block",fontSize:12,marginBottom:4}}>{m.material.kind}</b>{m.material.title}<small style={{display:"block",marginTop:5,opacity:.65}}>{m.material.url}</small></>:m.text}</p></article></div>)}</section>

   {picker&&<div style={{position:"absolute",left:12,right:12,bottom:62,zIndex:8,maxHeight:"42%",overflowY:"auto",padding:8,border:"1px solid #cfcfcf",borderRadius:9,background:"#fff",boxShadow:"0 10px 35px #0003"}}>
    <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"5px 6px 8px"}}><b style={{fontSize:13}}>选择要发送的材料</b><button onClick={()=>setPicker(false)} style={{width:28,height:28,border:0,borderRadius:6,background:"#f2f2f2",display:"grid",placeItems:"center"}}><X size={14}/></button></div>
    {sendable.map(m=><button key={m.id} onClick={()=>sendMaterial(m)} style={{width:"100%",display:"block",padding:"9px 10px",border:0,borderTop:"1px solid #eee",background:"#fff",textAlign:"left"}}><small style={{display:"block",color:"#999",marginBottom:3}}>{m.kind}</small><b style={{fontSize:13,fontWeight:500}}>{m.title}</b></button>)}
   </div>}

   <footer style={{flex:"0 0 auto",display:"grid",gridTemplateColumns:"auto 1fr auto",gap:8,alignItems:"center",padding:"10px 12px",background:"#f7f7f7",borderTop:"1px solid #ddd"}}>
    {sendable.length>0?<button onClick={()=>setPicker(v=>!v)} disabled={id==="x"} title="选择要发送的材料" style={{height:36,padding:"0 10px",border:"1px solid #d0d0d0",borderRadius:6,background:"#fff",display:"flex",alignItems:"center",gap:5}}><Link2 size={15}/>材料{sendable.length>1?` ${sendable.length}`:""}</button>:<span style={{width:1}}/>}
    <form onSubmit={sendText} style={{display:"contents"}}><input disabled={id==="x"} value={draft} onChange={e=>setDraft(e.target.value)} placeholder={id==="x"?"这是你自己的对话":"将以沈妍账号发送"} style={{height:36,border:"1px solid #d0d0d0",borderRadius:6,padding:"0 10px",minWidth:0}}/><button disabled={id==="x"||!draft.trim()} style={{height:36,width:42,border:0,borderRadius:6,background:"#39a65a",color:"#fff",display:"grid",placeItems:"center",opacity:id!=="x"&&draft.trim()?1:.45}}><Send size={16}/></button></form>
   </footer>
  </main>
 </div>;
}
