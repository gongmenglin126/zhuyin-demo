"use client";

import {FormEvent,useEffect,useMemo,useRef,useState} from "react";
import {Plus,Search,Send,X} from "lucide-react";

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
  {time:"10月13日 00:17",who:"对方",text:"我刚在你梦帖下面也回了。还是那句：先别急着给那两个音补名字。"},
  {who:"沈妍",text:"看到了。你在哪都像在给人审稿。"},
 ]},
 {id:"ly",name:"梁茵",preview:"公开区别写真名。",messages:[
  {time:"9月28日 00:42",who:"对方",text:"我不太想在论坛公开区继续说那个名字的问题。"},
  {who:"沈妍",text:"可以。你不想说的我不会追问。"},
  {who:"对方",text:"如果你后面真查旧报，公开区别写真名，也别发找到我的城市。"},
  {who:"沈妍",text:"好。"},
  {time:"9月28日 01:03",who:"对方",text:"我那个旧号也先不回帖了。有人又在下面问我回来以后会不会认错家。"},
  {who:"沈妍",text:"知道，我不会在公开帖里叫你真名。"},
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

// 只有这些“材料 × 联系人”组合允许发送。null 表示能发，但对方不会立刻回复。
const materialRules:Record<string,MaterialRule>={
  "33897":{
    yq:null,
    zc:"户型和梦里的结构能对上，值得查。但它只能证明‘有现实原型’，不能证明她去过。先找原始记录。",
  },
  "09114":{
    yq:"林楠？她没跟我提过这个人。你从哪翻到的？",
    zc:"先别猜谁绑的。把林楠和沈妍两份旧报并排看：失踪时间、找回时间、回来后最早出现的变化。真正有用的是两边能不能互相对应。",
    ly:"……你怎么查到林楠这个名字的？先别在公开区发。要继续查，就看她回来以后有没有‘名字不对’、‘另一个家’这种很具体的东西。",
  },
  "09831":{
    zc:"沈妍自己的旧报也按同样标准处理。家人口述和原报分开。重点不是‘都失踪过’，是回来以后各自多了什么、少了什么。",
    ly:null,
  },
  "10731":{
    zc:"目前只能证明两起案子时间很近、年龄相同、都被找回。先别直接推同一作案者。",
    ly:"我以前看到这篇时只当巧合。现在再看，真正让我不舒服的是两个人回来以后都像有东西对不上。",
  },
  "14692":{
    zc:"这篇有用，因为它把几种东西分开写了：名字不对、另一个家、生活习惯变化。你可以分别搜这些原话，看是不是只有一个人这样。",
    ly:"这篇我看过。‘别人叫我的名字不对’和‘另一个家’这两句特别像我以前的感觉。先搜原话，别搜‘换魂’。",
  },
  "17428":{
    zc:"这个案例反而很重要：只有口味变化，没有名字错位、陌生家庭记忆或技能断层。它提醒你‘失踪后变了’本身不够说明问题。",
    ly:"我没有这种单纯口味变化。我的情况更接近‘名字像叫错了’和‘脑子里有另一个家’。",
  },
  "private-p1":{
    yq:"她最近跟我说过梦越来越像真的，但没跟我提过林楠这个名字。",
    zc:"这条先别碰经文。最奇怪的是：沈妍记住了一个自己没住过的房间，而且记忆落到了林楠这个名字上。下一步应该找反方向——林楠那边有没有属于沈妍的东西。",
    ly:"她写‘像手已经做过几百次’这句我能理解。你去站里搜几句很普通的话：‘名字不对’、‘另一个家’。有人真的这样写过。",
  },
  "private-p3":{
    yq:null,
    zc:"不用把所有怪事一口气看完。她这份记录已经给了三个能查的方向：‘名字不对’、‘另一个家’、‘回来以后不会’。一次搜一个，先找能核验的案例。",
    ly:"这里面有两类我能确认：名字像叫错了、记得另一个家。我以前在论坛写过，旧号还在。你按这两句搜，比猜我标题快。",
  },
  verse:{
    zc:"这张残页来源字段没了。先把它当宗教文本，不要当事实证明。‘身’‘名’这些词以后如果在别处重复出现，再回来对。",
    ly:"‘身非我身，名非我名’这句我见过。不是公开帖正文，是以前有人发给我的一张旧纸截图。我当时没看懂。",
  },
  sanmen:{
    zc:"先翻成白话，不替它证明：‘舍’像身体，‘客’像魂；‘二客、两门相应’至少是在说两个主体和两个身体一起发生变化。现在别再啃字了，回现实里找：一边失去的东西，有没有正好出现在另一边。如果能对上，才值得谈‘交换’。",
    ly:"我第一次看到也看不懂。你先把沈妍和林楠两个人对着看：一个人记得不属于自己的家，另一个人有没有相反的错位？如果两边能互相补上，我会先猜是‘进错了身体’。是不是互换，我不敢替你下结论。",
  },
};

const textReply=(contact:string,text:string):string|null=>{
 const t=text.replace(/\s/g,"");
 if(contact==="yq"){
  if(/昨晚|见面|去哪|在哪/.test(t))return "昨天见到她了。后来她说还有点事，我就先走了。我以为她回家了。";
  if(/林楠/.test(t))return "这个名字我真没听她说过。";
 }
 if(contact==="zc"){
  if(/林楠/.test(t))return "先别围着名字猜。把两份旧报的日期、年龄、找回后的变化并排放。";
  if(/失踪|不见了|联系不上/.test(t))return "如果现实里确实联系不上，先走正常报警和亲友确认。论坛材料不要代替现实证据。";
  if(/换魂|灵魂|交换/.test(t))return "先别用这个词。你要找的是能区分‘创伤记忆’和‘两个人发生对应错位’的材料。看看一边缺的东西有没有出现在另一边。";
  if(/名字不对|另一个家|回来以后不会/.test(t))return "对，先搜原话。关键词越像当事人会说的话越好，不要搜结论。";
 }
 if(contact==="ly"){
  if(/林楠/.test(t))return "别在这个号里反复写真名。你如果已经看到旧报，就继续查她回来后最早的变化。";
  if(/名字|另一个家|不会/.test(t))return "我能确认的是：有些人回来后真的会觉得名字不对，也有人记得另一个家、突然不会以前会的东西。原因我不知道。";
  if(/换魂|灵魂|交换/.test(t))return "我以前也这么猜过，但只有感觉不算证据。你得先看两个人的‘错位’是不是能互相对应。";
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

 return <div className="wechat" style={{height:"calc(100% - 39px)",minHeight:0,overflow:"hidden"}}>
  <aside style={{height:"100%",minHeight:0,overflowY:"auto"}}><header><i>妍</i><span><b>沈妍</b><small>微信已登录</small></span></header><label><Search/><input value={q} onChange={e=>setQ(e.target.value)} placeholder="搜索联系人和消息"/></label>{visible.map(x=><button className={x.id===id?"active":""} onClick={()=>setId(x.id)} key={x.id}><i>{x.name[0]}</i><span><b>{x.name}</b><small>{x.preview}</small></span></button>)}</aside>
  <main style={{height:"100%",minHeight:0,display:"flex",flexDirection:"column",overflow:"hidden",position:"relative"}}>
   <header style={{flex:"0 0 auto"}}><b>{contact.name}</b><small>聊天记录</small></header>
   <section ref={scrollRef} style={{flex:"1 1 auto",minHeight:0,overflowY:"auto",overscrollBehavior:"contain"}}>{messages.map((m,i)=><div key={i}>{m.time&&<time>{m.time}</time>}<article className={m.who==="沈妍"?"mine":""}><i>{m.who==="沈妍"?"妍":contact.name[0]}</i><p>{m.material?<><b style={{display:"block",fontSize:12,marginBottom:4}}>{m.material.kind}</b>{m.material.title}<small style={{display:"block",marginTop:5,opacity:.65}}>{m.material.url}</small></>:m.text}</p></article></div>)}</section>

   {picker&&<div style={{position:"absolute",left:12,right:12,bottom:76,zIndex:8,maxHeight:"42%",overflowY:"auto",padding:8,border:"1px solid #cfcfcf",borderRadius:9,background:"#fff",boxShadow:"0 10px 35px #0003"}}>
    <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"5px 6px 8px"}}><b style={{fontSize:13}}>发送文件</b><button onClick={()=>setPicker(false)} style={{width:28,height:28,border:0,borderRadius:6,background:"#f2f2f2",display:"grid",placeItems:"center"}}><X size={14}/></button></div>
    {sendable.length?sendable.map(m=><button key={m.id} onClick={()=>sendMaterial(m)} style={{width:"100%",display:"block",padding:"10px",border:0,borderTop:"1px solid #eee",background:"#fff",textAlign:"left"}}><small style={{display:"block",color:"#999",marginBottom:3}}>{m.kind}</small><b style={{fontSize:13,fontWeight:500}}>{m.title}</b></button>):<p style={{margin:0,padding:"18px 10px",borderTop:"1px solid #eee",color:"#999",fontSize:12,textAlign:"center"}}>暂无可发送文件</p>}
   </div>}

   <footer style={{flex:"0 0 auto",padding:"12px 14px",background:"#f7f7f7",borderTop:"1px solid #ddd"}}>
    <form onSubmit={sendText} style={{display:"grid",gridTemplateColumns:"1fr 44px 48px",gap:8,alignItems:"center"}}>
     <input disabled={id==="x"} value={draft} onChange={e=>setDraft(e.target.value)} placeholder={id==="x"?"":"输入消息"} style={{height:48,border:"1px solid #d0d0d0",borderRadius:8,padding:"0 14px",minWidth:0,fontSize:14}}/>
     <button type="button" onClick={()=>setPicker(v=>!v)} disabled={id==="x"} title="文件" aria-label="文件" style={{position:"relative",height:44,width:44,border:"1px solid #d0d0d0",borderRadius:6,background:"#fff",display:"grid",placeItems:"center",color:"#555",opacity:id==="x"?.45:1}}><Plus size={19}/>{sendable.length>0&&<small style={{position:"absolute",right:-4,top:-5,minWidth:16,height:16,padding:"0 4px",borderRadius:8,background:"#39a65a",color:"#fff",fontSize:9,lineHeight:"16px"}}>{sendable.length}</small>}</button>
     <button type="submit" disabled={id==="x"||!draft.trim()} style={{height:44,width:48,border:0,borderRadius:6,background:"#39a65a",color:"#fff",display:"grid",placeItems:"center",opacity:id!=="x"&&draft.trim()?1:.45}}><Send size={16}/></button>
    </form>
   </footer>
  </main>
 </div>;
}
