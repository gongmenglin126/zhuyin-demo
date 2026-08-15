"use client";

import {FormEvent,useMemo,useState} from "react";
import {Link2,Search,Send} from "lucide-react";

export type SharedMaterial={id:string;title:string;kind:string;url:string};
type Msg={time?:string;who:"沈妍"|"对方";text:string;material?:SharedMaterial};
type Contact={id:string;name:string;preview:string;messages:Msg[]};

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

const materialReply=(contact:string,id:string):string=>{
 const table:Record<string,Record<string,string>>={
  yq:{
   "30177":"她前阵子确实老在找这种旧盒子。我还笑她为了一个梦跑太远。",
   "33897":"这个我没看过。她最近去岚州就是为了旧楼照片？",
   "09114":"林楠？她没跟我提过这个名字。",
   "09831":"她小时候失踪那件事我知道一点，她自己一直不愿细说。",
   sanmen:"这什么旧文？我看不懂。她最近查的已经这么偏了吗？",
  },
  zc:{
   "30177":"物件相似只能当检索入口，不能当身份依据。先留原图和时间。",
   "33897":"户型和梦里结构能对上，值得查；但先找旧报，不要拿熟悉感证明她去过。",
   "09114":"把失踪日期、找回日期、年龄和找回后的变化分开记。尤其不要因为两个案子接近，就先设成同一作案者。",
   "09831":"这条你自己的旧报也要按同样标准处理。家人口述和原报分开。",
   "10731":"这篇楼主的结论是对的：目前只能证明两起案子很接近，不能证明同因。",
   "14692":"这个人的描述里，名字、习惯、空间记忆是三类不同信息。不要把它们互相证明。",
   "17119":"如果她愿意说，先问被找到当天有没有突然害怕以前不怕的东西，以及以前会做后来不会的事。",
   verse:"这张残页来源字段没了。先找同句异文，尤其是‘身’‘名’这些词，别直接按现代意义解释。",
   sanmen:"如果“舍”“客”是这个文本自己的术语，先确认别处是不是也把身体叫舍、魂叫客。‘二客’只能说明它在谈两个主体，还不能自动等于交换。",
  },
  ly:{
   "30177":"这个盒子我不认识。她后来一直在查旧房子吗？",
   "33897":"我没去过岚棉三厂。但她问我的问题和这帖里那些‘回来以后变了什么’很像。",
   "09114":"……你怎么查到林楠这个名字的？先别在公开区发。",
   "09831":"你把两条日期放一起看。别只看‘都失踪过’，看她们分别什么时候不见、什么时候回来。",
   "10731":"我以前看到这篇时只当巧合。现在再看，确实有点不舒服。",
   "14692":"这条我看过。那种‘名字叫错了’的感觉不是只有她有。",
   "17119":"这是我以前的帖子。别把我的真名和论坛账号放到公开区。",
   verse:"‘身非我身，名非我名’这句我见过。不是在公开帖正文里，是别人发给我的一张旧纸截图。",
   sanmen:"我见过“客”这个词。以前有人问我走失回来以后会不会梦到‘故门’，我当时只觉得他说话很怪。你先别把它解释成换魂，但这套词和那些问题确实像是一套东西。",
  },
 };
 return table[contact]?.[id]||"我看到了。你先把原始链接留着，别急着下结论。";
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

export default function InteractiveWechat({clipboard}:{clipboard:SharedMaterial|null}){
 const [id,setId]=useState("x"),[q,setQ]=useState(""),[draft,setDraft]=useState("");
 const [extra,setExtra]=useState<Record<string,Msg[]>>({});
 const contact=contacts.find(x=>x.id===id)!;
 const visible=contacts.filter(x=>(x.name+x.preview).includes(q));
 const messages=useMemo(()=>[...contact.messages,...(extra[id]||[])],[contact,extra,id]);
 const append=(items:Msg[])=>setExtra(prev=>({...prev,[id]:[...(prev[id]||[]),...items]}));
 const sendText=(e:FormEvent)=>{
  e.preventDefault();
  const text=draft.trim(); if(!text||id==="x")return;
  const reply=textReply(id,text);
  append([{who:"沈妍",text},...(reply?[{who:"对方" as const,text:reply}]:[])]);
  setDraft("");
 };
 const sendMaterial=()=>{
  if(!clipboard||id==="x")return;
  append([{who:"沈妍",text:`[分享] ${clipboard.title}`,material:clipboard},{who:"对方",text:materialReply(id,clipboard.id)}]);
 };
 return <div className="wechat">
  <aside><header><i>妍</i><span><b>沈妍</b><small>微信已登录</small></span></header><label><Search/><input value={q} onChange={e=>setQ(e.target.value)} placeholder="搜索联系人和消息"/></label>{visible.map(x=><button className={x.id===id?"active":""} onClick={()=>setId(x.id)} key={x.id}><i>{x.name[0]}</i><span><b>{x.name}</b><small>{x.preview}</small></span></button>)}</aside>
  <main><header><b>{contact.name}</b><small>聊天记录</small></header><section>{messages.map((m,i)=><div key={i}>{m.time&&<time>{m.time}</time>}<article className={m.who==="沈妍"?"mine":""}><i>{m.who==="沈妍"?"妍":contact.name[0]}</i><p>{m.material?<><b style={{display:"block",fontSize:12,marginBottom:4}}>{m.material.kind}</b>{m.material.title}<small style={{display:"block",marginTop:5,opacity:.65}}>{m.material.url}</small></>:m.text}</p></article></div>)}</section>
   <footer style={{display:"grid",gridTemplateColumns:"auto 1fr auto",gap:8,alignItems:"center",padding:"10px 12px"}}>
    <button onClick={sendMaterial} disabled={!clipboard||id==="x"} title={clipboard?`发送：${clipboard.title}`:"先在论坛帖子里复制链接"} style={{height:36,padding:"0 10px",border:"1px solid #d0d0d0",borderRadius:6,background:"#fff",display:"flex",alignItems:"center",gap:5,cursor:clipboard&&id!=="x"?"pointer":"default",opacity:clipboard&&id!=="x"?1:.45}}><Link2 size={15}/>材料</button>
    <form onSubmit={sendText} style={{display:"contents"}}><input disabled={id==="x"} value={draft} onChange={e=>setDraft(e.target.value)} placeholder={id==="x"?"这是你自己的对话":"将以沈妍账号发送"} style={{height:36,border:"1px solid #d0d0d0",borderRadius:6,padding:"0 10px",minWidth:0}}/><button disabled={id==="x"||!draft.trim()} style={{height:36,width:42,border:0,borderRadius:6,background:"#39a65a",color:"#fff",display:"grid",placeItems:"center",opacity:id!=="x"&&draft.trim()?1:.45}}><Send size={16}/></button></form>
    {clipboard&&id!=="x"&&<small style={{gridColumn:"1 / -1",color:"#888",whiteSpace:"nowrap",overflow:"hidden",textOverflow:"ellipsis"}}>最近复制：{clipboard.title}</small>}
   </footer>
  </main>
 </div>;
}
