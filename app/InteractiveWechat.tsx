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
    zc:"嗯，这个房型确实像。旧住户那段我会更在意。",
  },
  "09114":{
    yq:"林楠？没听她提过。你从哪翻出来的？",
    zc:"这就有点怪了。沈妍那条旧报你也找到了吗？我想看两边时间。",
    ly:"……林楠？你先别在论坛里写真名。她回来以后，有没有说过“这不是我家”之类的话？",
  },
  "09831":{
    zc:"对，就是这条。你先看日期。还有，她回来以后家里有没有说过她哪儿变了？",
    ly:null,
  },
  "10731":{
    zc:"时间挨得太近了。不过先别急着当成同一伙人。",
    ly:"我以前也看过。那时候觉得只是巧合，现在再看……有点不舒服。",
  },
  "14692":{
    zc:"这篇先留着。“名字不对”和“另一个家”这两句，我感觉不止一个人说过。",
    ly:"这篇我记得。“名字不对”那句……我自己也有过。",
  },
  "17428":{
    zc:"这个反而不像。只是不吃东西，太普通了。",
    ly:"这个跟我不太一样。",
  },
  "private-p1":{
    yq:"她跟我提过那个梦，说最近越来越清楚。林楠这个名字我真没听过。",
    zc:"等下。她梦里的房间后来真找到了？那林楠那边你查过没有？",
    ly:"她写“手自己会动”那句……我有点懂。你搜搜“名字不对”或者“另一个家”吧，我以前看到过类似的。",
  },
  "private-p3":{
    yq:null,
    zc:"这里面有几条我见过类似说法。“名字不对”“另一个家”“回来以后不会”。你分开搜吧。",
    ly:"“名字不对”和“另一个家”这两种我都经历过。旧号里可能还留着。",
  },
  verse:{
    zc:"这句我不懂。先留着吧，别因为它看着像答案就硬往上套。",
    ly:"这句……我见过。以前有人给我发过一张旧纸，差不多就是这个。",
  },
  sanmen:{
    zc:"这下稍微能看懂点了。“舍”像身体，“客”像人……但“二客相契”到底什么意思，我也不敢下结论。你把沈妍和林楠两边对着看。",
    ly:"我第一反应挺邪门的：像是人进错了地方。你别当我结论，我只是看到这几句会这么想。",
  },
};

const textReply=(contact:string,text:string):string|null=>{
 const t=text.replace(/\s/g,"");
 if(contact==="yq"){
  if(/昨晚|见面|去哪|在哪/.test(t))return "见到了。后来她说还有点事，让我先走。我真以为她回家了。";
  if(/林楠/.test(t))return "真没听她提过这个名字。";
 }
 if(contact==="zc"){
  if(/林楠/.test(t))return "沈妍那条旧报你也翻出来了吗？我想先看时间。";
  if(/失踪|不见了|联系不上/.test(t))return "现在还联系不上？那你先报警，也跟她家里说一声。这个别只在网上查。";
  if(/换魂|灵魂|交换/.test(t))return "你先别把“换魂”当答案。两边有没有什么东西能互相对上？没有的话我不敢这么猜。";
  if(/名字不对|另一个家|回来以后不会/.test(t))return "嗯，搜原话吧。比搜“换魂”靠谱。";
 }
 if(contact==="ly"){
  if(/林楠/.test(t))return "你先别在公开区写真名。她回来以后最早哪里不对，你有看到吗？";
  if(/名字|另一个家|不会/.test(t))return "有。我自己也有过。名字像别人的，脑子里又会冒出一个不认识的家。";
  if(/换魂|灵魂|交换/.test(t))return "我也想过……但我不敢说就是。要是两个人的东西真能互相对上，那才吓人。";
 }
 return null;
};

export default function InteractiveWechat({materials}:{materials:SharedMaterial[]}){
 const [id,setId]=useState("x"),[q,setQ]=useState(""),[draft,setDraft]=useState(""),[picker,setPicker]=useState(false);
 const [extra,setExtra]=useState<Record<string,Msg[]>>({});
 const [introduced,setIntroduced]=useState<Record<string,boolean>>({});
 const [typing,setTyping]=useState<Record<string,boolean>>({});
 const scrollRef=useRef<HTMLElement|null>(null);
 const contact=contacts.find(x=>x.id===id)!;
 const visible=contacts.filter(x=>(x.name+x.preview).includes(q));
 const messages=useMemo(()=>[...contact.messages,...(extra[id]||[])],[contact,extra,id]);
 const sendable=useMemo(()=>materials.filter(m=>Object.prototype.hasOwnProperty.call(materialRules[m.id]||{},id)),[materials,id]);
 const appendFor=(contactId:string,items:Msg[])=>setExtra(prev=>({...prev,[contactId]:[...(prev[contactId]||[]),...items]}));
 const introFor=(contactId:string):Msg[]=>{
  if(contactId==="x"||introduced[contactId])return [];
  setIntroduced(prev=>({...prev,[contactId]:true}));
  return [{who:"沈妍",text:"你好，我是徐宁，沈妍的朋友。她今天一直联系不上，我现在在她家。她电脑上微信还登着，冒昧问你两句。"}];
 };
 const delayedReply=(contactId:string,reply:string|null)=>{
  if(!reply)return;
  setTyping(prev=>({...prev,[contactId]:true}));
  const delay=Math.min(1500,850+reply.length*7);
  window.setTimeout(()=>{
   appendFor(contactId,[{who:"对方",text:reply}]);
   setTyping(prev=>({...prev,[contactId]:false}));
  },delay);
 };

 useEffect(()=>{
  const el=scrollRef.current;
  if(el)el.scrollTop=el.scrollHeight;
 },[id,messages.length]);
 useEffect(()=>setPicker(false),[id]);

 const sendText=(e:FormEvent)=>{
  e.preventDefault();
  const text=draft.trim(); if(!text||id==="x")return;
  const contactId=id;
  const reply=textReply(contactId,text);
  appendFor(contactId,[...introFor(contactId),{who:"沈妍",text}]);
  delayedReply(contactId,reply);
  setDraft("");
 };
 const sendMaterial=(material:SharedMaterial)=>{
  const rules=materialRules[material.id];
  if(!rules||!Object.prototype.hasOwnProperty.call(rules,id))return;
  const contactId=id;
  const reply=rules[contactId];
  appendFor(contactId,[...introFor(contactId),{who:"沈妍",text:`[分享] ${material.title}`,material}]);
  delayedReply(contactId,reply);
  setPicker(false);
 };

 return <div className="wechat" style={{height:"calc(100% - 39px)",minHeight:0,overflow:"hidden"}}>
  <aside style={{height:"100%",minHeight:0,overflowY:"auto"}}><header><i>妍</i><span><b>沈妍</b><small>微信已登录</small></span></header><label><Search/><input value={q} onChange={e=>setQ(e.target.value)} placeholder="搜索联系人和消息"/></label>{visible.map(x=><button className={x.id===id?"active":""} onClick={()=>setId(x.id)} key={x.id}><i>{x.name[0]}</i><span><b>{x.name}</b><small>{x.preview}</small></span></button>)}</aside>
  <main style={{height:"100%",minHeight:0,display:"flex",flexDirection:"column",overflow:"hidden",position:"relative"}}>
   <header style={{flex:"0 0 auto"}}><b>{contact.name}</b><small>{typing[id]?"正在输入…":"聊天记录"}</small></header>
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
