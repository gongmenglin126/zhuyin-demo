"use client";

import {FormEvent,useEffect,useMemo,useRef,useState} from "react";
import {Plus,Search,Send,X} from "lucide-react";

export type SharedMaterial={id:string;title:string;kind:string;url:string};
type Msg={time?:string;who:"沈妍"|"对方";text:string;material?:SharedMaterial};
type Contact={id:string;name:string;note:string;preview:string;messages:Msg[]};
type ReplyPart={text?:string;material?:SharedMaterial};
type MaterialRule=Record<string,ReplyPart[]|null>;

const forumPost=(id:string,title:string):SharedMaterial=>({id,title,kind:"论坛帖子",url:`https://www.zhuyinwen.cn/thread/${id}`});
const returnedPost=forumPost("14692","有没有人记得“被找回来”之前的家");
const ordinaryChangePost=forumPost("17428","小时候走失以后突然不吃香菜，这种变化会持续很多年吗");

// Desktop apps are unmounted when switching windows. Keep the current WeChat session
// at module scope so messages and one-shot material sends survive app switches.
const wechatSession={
  extra:{} as Record<string,Msg[]>,
  introduced:{} as Record<string,boolean>,
  sent:{} as Record<string,boolean>,
};
const wechatSubscribers=new Set<()=>void>();
const notifyWechat=()=>wechatSubscribers.forEach(fn=>fn());

const contacts:Contact[]=[
 {id:"x",name:"徐宁",note:"自己",preview:"我去你家看看。",messages:[
  {time:"10月16日 11:26",who:"对方",text:"明天中午老地方？"},
  {who:"沈妍",text:"嗯"},
  {who:"对方",text:"你别又临时加活"},
  {who:"沈妍",text:"不会，我迟到请你吃一个月"},
  {who:"对方",text:"截图了"},
  {time:"10月16日 19:48",who:"沈妍",text:"我出去一趟，明天还是靠窗那桌"},
  {time:"今天 12:02",who:"对方",text:"我到了"},
  {who:"对方",text:"你人呢？"},
  {time:"今天 12:37",who:"对方",text:"电话也不接，看到回我"},
  {time:"今天 18:37",who:"对方",text:"我去你家看看"},
 ]},
 {id:"yq",name:"余晴",note:"朋友介绍的",preview:"你别又先点一堆",messages:[
  {time:"10月16日 19:31",who:"对方",text:"到了没"},
  {who:"沈妍",text:"到了"},
  {who:"对方",text:"还是里面那桌？"},
  {who:"沈妍",text:"嗯"},
  {who:"对方",text:"我还有十分钟"},
  {who:"沈妍",text:"慢慢来"},
  {who:"对方",text:"你别又先点一堆"},
  {who:"沈妍",text:"已经点了"},
  {who:"对方",text:"……服了"},
 ]},
 {id:"zc",name:"周川",note:"论坛加的",preview:"我在帖里回你了",messages:[
  {time:"10月12日 22:08",who:"对方",text:"你又发帖了？"},
  {who:"沈妍",text:"你刷到了？"},
  {who:"对方",text:"嗯"},
  {who:"对方",text:"这次还是那两个音？"},
  {who:"沈妍",text:"差不多"},
  {who:"沈妍",text:"但我现在越看越像“楠楠”"},
  {who:"对方",text:"你先别自己把自己绕进去"},
  {who:"沈妍",text:"已经进去了"},
  {who:"对方",text:"那你还不睡"},
  {who:"沈妍",text:"睡不着啊"},
  {who:"对方",text:"明早醒了再写，今晚别翻前几次的"},
  {who:"沈妍",text:"行吧"},
  {time:"10月13日 00:17",who:"对方",text:"我在帖里回你了"},
  {who:"沈妍",text:"你还真回啊"},
  {who:"对方",text:"不然呢"},
  {who:"沈妍",text:"你说话真的很像审稿"},
  {who:"对方",text:"职业病"},
 ]},
 {id:"ly",name:"梁茵",note:"论坛私聊加的",preview:"那个号我先不上了",messages:[
  {time:"9月28日 00:42",who:"对方",text:"你还在查那个？"},
  {who:"沈妍",text:"哪个"},
  {who:"对方",text:"名字那个"},
  {who:"沈妍",text:"嗯"},
  {who:"对方",text:"我不想在帖子里讲了"},
  {who:"沈妍",text:"好"},
  {who:"对方",text:"私下可以"},
  {who:"沈妍",text:"你确定？"},
  {who:"对方",text:"嗯，但别写真名"},
  {who:"沈妍",text:"行"},
  {time:"9月28日 01:03",who:"对方",text:"刚又有人私信问我回来以后认不认家"},
  {who:"对方",text:"烦死了"},
  {who:"沈妍",text:"那你那个号先别上了"},
  {who:"对方",text:"我也是这么想"},
  {who:"沈妍",text:"去睡吧，都一点了"},
  {who:"对方",text:"你也好意思说我"},
 ]},
 {id:"f",name:"方嘉",note:"公司",preview:"周一的表我先帮你交？",messages:[
  {time:"昨天 16:22",who:"对方",text:"甲方又改表头了"},
  {who:"对方",text:"我真的服"},
  {who:"沈妍",text:"哈哈哈哈发我"},
  {who:"对方",text:"你还笑"},
  {who:"沈妍",text:"先别动，我明早统一"},
  {time:"今天 09:14",who:"对方",text:"你今天来不来？"},
  {time:"今天 14:05",who:"对方",text:"周一的表我先帮你交？"},
 ]},
 {id:"p",name:"爸妈",note:"家人",preview:"这周回来吃饭吗",messages:[
  {time:"10月15日 18:44",who:"对方",text:"这周回来吃饭吗"},
  {who:"沈妍",text:"不一定"},
  {who:"对方",text:"你爸买了排骨"},
  {who:"沈妍",text:"你们吃吧，我这两天有点事"},
  {who:"对方",text:"又加班？"},
  {who:"沈妍",text:"不是工作"},
  {who:"对方",text:"那也别熬太晚"},
 ]},
];

const materialRules:Record<string,MaterialRule>={
  "33897":{
    yq:[{text:"这哪？"},{text:"没去过。她昨晚也没提这个。"}],
    zc:[{text:"哦这个，我看过。"},{text:"就是她梦里那个房型吧？"},{text:"确实挺像。"}],
  },
  "09114":{
    yq:[{text:"林楠？"},{text:"没听她说过。"}],
    zc:[{text:"林楠？"},{text:"等等。"},{text:"这个名字她没跟我说过。"},{text:"沈妍小时候那条你也找到了吗？"}],
    ly:[{text:"你怎么找到这个的"},{text:"她没跟我说已经查到名字了。"}],
  },
  "09831":{
    zc:[{text:"……"},{text:"这两条日期挨得也太近了。"}],
    ly:[{text:"这是沈妍？"},{text:"她从来没跟我说过这段。"}],
  },
  "10731":{
    zc:[{text:"我记得这帖。"},{text:"我当年还回过。"},{text:"没想到又绕回来了。"}],
    ly:[{text:"这篇我也看过。"},{text:"那时候真没多想。"}],
  },
  "14692":{
    zc:[{text:"这人我记得。"},{text:"等下，我给你找个完全不像的。"},{material:ordinaryChangePost},{text:"这个就只有口味变了。"}],
    ly:[{text:"这篇别往公开群里发。"},{text:"我以前看完一晚上没睡。"}],
  },
  "17428":{
    zc:[{text:"这个我反而觉得没啥。"},{text:"小时候受惊以后口味变了，也不是不能解释。"}],
    ly:[{text:"这个不像我。"}],
  },
  "private-p1":{
    yq:[{text:"她是跟我说过最近老做同一个梦。"},{text:"但没跟我讲过这么细。"}],
    zc:[{text:"这是她电脑里的？"},{text:"她没给我看过这一版。"},{text:"她最后还是觉得那两个音像“楠楠”啊。"}],
    ly:[{text:"这个感觉让我想到一个旧帖。"},{material:returnedPost},{text:"不一定有关系，就是有点像。"}],
  },
  "private-p3":{
    yq:null,
    zc:[{text:"她居然存了这么多。"},{text:"等下。"},{material:ordinaryChangePost},{text:"这篇她也存了吗？这个其实挺普通的。"}],
    ly:[{text:"有几条我见过。"},{text:"“另一个家”那个我一直记得。"},{material:returnedPost}],
  },
  verse:{
    zc:[{text:"这啥"},{text:"她从哪翻出来的？"}],
    ly:[{text:"等等"},{text:"这句我好像见过。"},{text:"以前有人私信给我一张特别糊的纸，也是这几个字。"}],
  },
  sanmen:{
    zc:[{text:"我看不懂这个。"},{text:"“二客”是不是两个人？"},{text:"我瞎猜的。"}],
    ly:[{text:"……"},{text:"我第一眼觉得像两边位置弄反了。"},{text:"当我没说，我也不知道。"}],
  },
};

const textReply=(contact:string,text:string):ReplyPart[]|null=>{
 const t=text.replace(/\s/g,"");
 if(contact==="yq"){
  if(/昨晚|见面|去哪|在哪/.test(t))return [{text:"昨晚是见到了。"},{text:"后来她说还有点事，我就先走了。"},{text:"她没说去哪。"}];
  if(/林楠/.test(t))return [{text:"真没听过这个名字。"}];
 }
 if(contact==="zc"){
  if(/林楠/.test(t))return [{text:"她没跟我说过这个名字。"},{text:"你从哪翻到的？"}];
  if(/失踪|不见了|联系不上/.test(t))return [{text:"她现在还是完全联系不上？"},{text:"电话也不通？"}];
  if(/换魂|灵魂|交换/.test(t))return [{text:"……你先别吓自己。"},{text:"我现在也不知道。"}];
  if(/名字不对|另一个家|回来以后不会/.test(t))return [{text:"这种说法我好像见过几次。"},{text:"我找找。"}];
 }
 if(contact==="ly"){
  if(/林楠/.test(t))return [{text:"这个名字先别发公开区。"}];
  if(/名字|另一个家|不会/.test(t))return [{text:"嗯。"},{text:"我小时候也说过差不多的话。"}];
  if(/换魂|灵魂|交换/.test(t))return [{text:"你也想到这个了？"},{text:"我以前想过，然后把自己吓得够呛。"}];
 }
 if(contact==="f"&&/沈妍|联系不上|没来/.test(t))return [{text:"她今天也没回我。"},{text:"怎么了？"}];
 if(contact==="p"&&/沈妍|联系不上|没回/.test(t))return [{text:"她没跟我们说今天去哪。"},{text:"电话也打不通吗？"}];
 return null;
};

const introText=(contactId:string)=>{
 if(contactId==="yq")return "你好，我是徐宁，沈妍的朋友。她今天一直联系不上，我现在在她家。看到你们昨晚见过，想问下她走的时候有没有说去哪。";
 if(contactId==="zc")return "你好，我是徐宁，沈妍的朋友。她今天联系不上，我现在在她家。看到你们最近聊过她那些梦和旧帖子，想问你点事。";
 if(contactId==="ly")return "你好，我是徐宁，沈妍的朋友。她今天联系不上。我看到你们之前聊过一些她在查的东西，冒昧问几句。";
 if(contactId==="f")return "你好，我是徐宁，沈妍的朋友。她今天联系不上，我现在在她家，用一下她电脑上的微信。";
 if(contactId==="p")return "叔叔阿姨好，我是徐宁。沈妍今天一直联系不上，我现在在她家。";
 return "你好，我是徐宁，沈妍的朋友。她今天联系不上，我现在在她家。";
};

export default function InteractiveWechat({materials,onOpenPost}:{materials:SharedMaterial[];onOpenPost?:(id:string)=>void}){
 const [id,setId]=useState("x"),[q,setQ]=useState(""),[draft,setDraft]=useState(""),[picker,setPicker]=useState(false);
 const [extra,setExtra]=useState<Record<string,Msg[]>>(()=>({...wechatSession.extra}));
 const [introduced,setIntroduced]=useState<Record<string,boolean>>(()=>({...wechatSession.introduced}));
 const [typing,setTyping]=useState<Record<string,boolean>>({});
 const [sent,setSent]=useState<Record<string,boolean>>(()=>({...wechatSession.sent}));
 const scrollRef=useRef<HTMLElement|null>(null);
 const contact=contacts.find(x=>x.id===id)!;
 const visible=contacts.filter(x=>(x.name+x.note+x.preview).includes(q));
 const messages=useMemo(()=>[...contact.messages,...(extra[id]||[])],[contact,extra,id]);
 const sendable=useMemo(()=>materials.filter(m=>Object.prototype.hasOwnProperty.call(materialRules[m.id]||{},id)&&!sent[`${id}:${m.id}`]),[materials,id,sent]);
 const appendFor=(contactId:string,items:Msg[])=>{
  wechatSession.extra={...wechatSession.extra,[contactId]:[...(wechatSession.extra[contactId]||[]),...items]};
  notifyWechat();
 };
 const ensureIntro=(contactId:string):Msg[]=>{
  if(contactId==="x"||wechatSession.introduced[contactId])return [];
  wechatSession.introduced={...wechatSession.introduced,[contactId]:true};
  notifyWechat();
  return [{who:"沈妍",text:introText(contactId)}];
 };
 const delayedParts=(contactId:string,parts:ReplyPart[]|null)=>{
  if(!parts?.length)return;
  let elapsed=1000+Math.floor(Math.random()*900);
  setTyping(prev=>({...prev,[contactId]:true}));
  parts.forEach((part,index)=>{
   const extraDelay=part.text?Math.min(2200,part.text.length*35):700;
   elapsed+=extraDelay+Math.floor(Math.random()*1000);
   window.setTimeout(()=>{
    if(part.material)appendFor(contactId,[{who:"对方",text:`[链接] ${part.material.title}`,material:part.material}]);
    else if(part.text)appendFor(contactId,[{who:"对方",text:part.text}]);
    if(index===parts.length-1)setTyping(prev=>({...prev,[contactId]:false}));
   },elapsed);
  });
 };

 useEffect(()=>{
  const sync=()=>{
   setExtra({...wechatSession.extra});
   setIntroduced({...wechatSession.introduced});
   setSent({...wechatSession.sent});
  };
  wechatSubscribers.add(sync);
  sync();
  return ()=>{wechatSubscribers.delete(sync)};
 },[]);
 useEffect(()=>{
  const el=scrollRef.current;
  if(el)el.scrollTop=el.scrollHeight;
 },[id,messages.length,typing[id]]);
 useEffect(()=>setPicker(false),[id]);

 const sendText=(e:FormEvent)=>{
  e.preventDefault();
  const text=draft.trim(); if(!text||id==="x")return;
  const intro=ensureIntro(id);
  appendFor(id,[...intro,{who:"沈妍",text}]);
  setDraft("");
  delayedParts(id,textReply(id,text));
 };
 const sendMaterial=(material:SharedMaterial)=>{
  const rules=materialRules[material.id];
  if(!rules||!Object.prototype.hasOwnProperty.call(rules,id))return;
  const intro=ensureIntro(id);
  appendFor(id,[...intro,{who:"沈妍",text:`[分享] ${material.title}`,material}]);
  wechatSession.sent={...wechatSession.sent,[`${id}:${material.id}`]:true};
  notifyWechat();
  setPicker(false);
  delayedParts(id,rules[id]);
 };
 const openMaterial=(material:SharedMaterial)=>{
  if(material.kind==="论坛帖子"&&/^\d+$/.test(material.id)&&onOpenPost)onOpenPost(material.id);
 };

 return <div className="wechat" style={{height:"calc(100% - 39px)",minHeight:0,overflow:"hidden"}}>
  <aside style={{height:"100%",minHeight:0,overflowY:"auto"}}><header><i>妍</i><span><b>沈妍</b><small>微信已登录</small></span></header><label><Search/><input value={q} onChange={e=>setQ(e.target.value)} placeholder="搜索联系人和消息"/></label>{visible.map(x=><button className={x.id===id?"active":""} onClick={()=>setId(x.id)} key={x.id}><i>{x.name[0]}</i><span style={{minWidth:0}}><b>{x.name}</b><small style={{display:"block",marginTop:2,color:"#7f8783",whiteSpace:"nowrap",overflow:"hidden",textOverflow:"ellipsis"}}>{x.note}</small><small style={{display:"block",marginTop:3,whiteSpace:"nowrap",overflow:"hidden",textOverflow:"ellipsis"}}>{x.preview}</small></span></button>)}</aside>
  <main style={{height:"100%",minHeight:0,display:"flex",flexDirection:"column",overflow:"hidden",position:"relative"}}>
   <header style={{flex:"0 0 auto"}}><b>{contact.name}</b><small>{typing[id]?"正在输入…":contact.note}</small></header>
   <section ref={scrollRef} style={{flex:"1 1 auto",minHeight:0,overflowY:"auto",overscrollBehavior:"contain"}}>{messages.map((m,i)=><div key={i}>{m.time&&<time>{m.time}</time>}<article className={m.who==="沈妍"?"mine":""}><i>{m.who==="沈妍"?"妍":contact.name[0]}</i>{m.material?<button type="button" onClick={()=>openMaterial(m.material!)} style={{maxWidth:360,padding:"11px 12px",border:"1px solid #d7d7d7",borderRadius:8,background:"#fff",textAlign:"left",cursor:m.material.kind==="论坛帖子"?"pointer":"default"}}><small style={{display:"block",color:"#888",marginBottom:5}}>{m.material.kind}</small><b style={{display:"block",fontSize:13,fontWeight:600,lineHeight:1.45}}>{m.material.title}</b><small style={{display:"block",marginTop:7,color:"#999",wordBreak:"break-all"}}>{m.material.url}</small>{m.material.kind==="论坛帖子"&&<small style={{display:"block",marginTop:7,color:"#3b7a57"}}>打开帖子</small>}</button>:<p>{m.text}</p>}</article></div>)}</section>

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
