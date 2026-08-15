"use client";
/* eslint-disable @next/next/no-img-element */
import {FormEvent,ReactNode,useMemo,useState} from "react";
import {ArrowLeft,ChevronRight,Clock3,ExternalLink,Globe2,History as HistoryIcon,Home,LockKeyhole,Maximize2,MessageCircle,Minimize2,NotebookPen,RefreshCw,Search,Wifi,X} from "lucide-react";
import {chats,history,Post,posts,privateEntries,profile} from "../content/gameData";

type App="browser"|"wechat"|"notes"|"verse";
type Route={kind:"home"}|{kind:"post",id:string}|{kind:"profile"}|{kind:"user",name:string}|{kind:"private"}|{kind:"history"}|{kind:"search",q:string};

const contextPosts:Post[]=[
 {
  id:"09114",title:"【旧报摘录】岚棉三厂家属区九岁女童失踪，十三日后异地找回",author:"报刊索引",date:"2009-05-22 11:18",board:"旧闻考据",views:1294,hidden:true,
  excerpt:"2004 年岚州地方报纸摘录：九岁女童林楠失踪十三天后被找到。",
  terms:["岚棉三厂","林楠","2004","失踪","十三天","找回","旧客站"],highlights:["九岁女童林楠","失踪十三天","岚棉三厂家属区","无法完整说明失踪期间经历"],
  body:[
   "地方文献室索引：2004-07-18，岚棉三厂家属区九岁女童林楠失踪，家属当日报警。旧报没有公开具体门牌。",
   "2004-07-31，林楠在外市旧客运站附近被找到。报道写明身体无明显外伤，但无法完整说明失踪期间经历。",
   "这只是旧报摘录。原卷还有同版其他社会新闻，论坛转载没有继续追踪她之后的生活。"
  ],
  replies:[
   {user:"旧纸鸢",time:"11:42",text:"岚州那几年类似寻人简讯不少。要比较的话先记日期、年龄和找回地点，不要只看‘失忆’两个字。"},
   {user:"折柳",time:"12:05",text:"两起儿童失踪发生得接近，不等于彼此有关。先把能核实的字段放在一起，再谈解释。"},
   {user:"报刊索引",time:"12:19",text:"同意。这里只录索引，不做案件关联。",role:"楼主"}
  ]
 },
 {
  id:"17621",title:"八岁走失四天，回来以后突然不吃鱼了",author:"南坡风",date:"2019-08-12 21:07",board:"生活求助",views:2819,hidden:true,
  excerpt:"走失记录能核实；家里最常提的是回来以后口味和怕味道都变了。",
  terms:["走失","失踪","回来以后","口味","鱼","气味","儿童"],highlights:["走失四天","突然不吃鱼","怕消毒水"],
  body:[
   "我八岁时走失过四天，这件事不是家人口述，社区当年的寻人通知和派出所证明都还在。第四天晚上我在邻市汽车站被工作人员发现。",
   "家里一直觉得我回来以后‘像换了个人’，他们举得最多的例子是我突然不吃鱼。走失前我很爱吃，回来后闻到鱼汤会恶心。",
   "还有一个变化是怕消毒水味。这个倒可能很好解释：被找到后我发烧，在医院住了两晚。我自己不记得走失期间发生了什么。",
   "现在只是好奇儿童受惊以后口味变化常不常见，不是来问玄学。"
  ],
  replies:[
   {user:"折柳",time:"21:32",text:"口味变化是真的，也不自动指向某一种原因。把‘走失事实’、‘住院事实’和‘家人后来觉得你变了’分开记会更清楚。"},
   {user:"照骨",time:"22:01",text:"除了消毒水，回来以后有没有突然怕过一种以前不怕的气味？"},
   {user:"南坡风",time:"22:18",text:"家里只记得消毒水。鱼腥味算不算我不知道。",role:"楼主"}
  ]
 },
 {
  id:"18463",title:"小时候被找回来以后，坚持说我们家应该在三楼",author:"旧钥匙",date:"2020-06-03 00:14",board:"生活求助",views:3471,hidden:true,
  excerpt:"走失两天是真事；‘三楼的家’也确实从小反复说过，但来源一直没查清。",
  terms:["被找回来","走失","另一个家","楼层","记错家","儿童"],highlights:["走失两天","应该住三楼","绿色铁门"],
  body:[
   "五岁那年我在庙会走失两天，后来被送到派出所。报警回执家里还留着，所以时间没有争议。",
   "奇怪的是回来后有一年多，我每次上楼都要在三楼停，说‘到了’，可我家一直住五楼。还会说门应该是绿色铁门，门边有很窄的鞋柜。",
   "后来我姨妈翻出旧照片，说我三岁前常住外婆家，正好三楼、绿色门。但那套房的鞋柜位置和我描述的不一样。到底是旧记忆、走失期间住过的地方，还是后来听人说出来的，我不知道。"
  ],
  replies:[
   {user:"小蒋同学",time:"00:37",text:"三岁前住过的房子已经足够形成空间记忆，先别把‘回来后才说’理解成‘回来后才有’。"},
   {user:"折柳",time:"01:02",text:"这条最有用的不是‘另一个家’，而是你能找到外婆家照片做对照。能证实哪部分、不能证实哪部分，要分开。"},
   {user:"旧钥匙",time:"01:19",text:"有道理。我准备找老邻居问问门边到底有没有鞋柜。",role:"楼主"}
  ]
 },
 {
  id:"20142",title:"七岁走失一周，回来以后不会骑原来那辆自行车",author:"白球鞋",date:"2021-11-03 20:41",board:"生活求助",views:4190,hidden:true,
  excerpt:"旧报能查到失踪和找回日期；回来后技能断裂、名字反应迟缓也被家人反复提过。",
  terms:["走失","失踪","旧报","自行车","名字","回来以后","七岁"],highlights:["走失一周","不会骑自行车","叫名字会慢半拍"],
  body:[
   "七岁时走失过一周，旧报能查到失踪和找回日期。我不公开真名，只说这些能被家里之外的记录核实。",
   "回来后最明显的是不会骑原来那辆自行车。不是害怕，是上去就不知道怎么保持平衡。大概两个月后又重新学会了。",
   "我妈还说那阵子叫我名字会慢半拍，有时会先回头看别处。我自己对那一年记忆很碎，所以不知道她有没有把后来的印象说重。",
   "发帖只是想问有没有类似的技能断层。请别私信问地址和真名。"
  ],
  replies:[
   {user:"候鸟第七年",time:"21:06",text:"方便私信聊吗？我小时候也失踪过一段时间。"},
   {user:"白球鞋",time:"21:14",text:"可以，但别在公开区写真名。",role:"楼主"},
   {user:"折柳",time:"21:39",text:"先保留旧报原页。技能、名字反应和失踪记录都是真事实，也不要急着把三件事解释成同一个原因。"},
   {user:"照骨",time:"22:03",text:"被找到当天，有没有人叫过你一个完全陌生的名字？"}
  ]
 }
];

const investigationPosts=[...posts,...contextPosts];
const investigationPrivateEntries=privateEntries.map(entry=>{
 if(entry.id==="p1")return {...entry,highlights:["林楠","这个名字和那间房连在一起","先记下来，不解释"],body:[
  "今晚又梦见那间房。我醒来以后第一反应是去厨房找那个糖盒，手甚至已经准备好先往上抬一下盒盖。",
  "梦里那个称呼这次比以前清楚。我听见的像是一个完整名字：林楠。",
  "我不知道林楠是谁。这个名字一出现，那间房、糖盒、厨房门突然像被钉在一起。我搜了几次，没有马上找到能对应的人。",
  "先记下来，不解释。名字可能来自我很早以前听过的东西，也可能只是梦自己补全。"
 ]};
 if(entry.id==="p2")return {...entry,highlights:["形可易，名可夺，忆可乱","形、名、忆","二客","两门相应","不能拿解释替代原文"],body:[
  "夹墙帖子里的复印页不是经书原页，但‘形可易，名可夺，忆可乱’在几个转录版本里都能对上。",
  "我现在只敢把字面拆开记：形、名、忆被当成三件可以分离的东西。另有两处残句出现‘二客’和‘两门相应’，上下文都缺了。",
  "这些词可以被解释成附身、失忆、改名、宗教比喻，甚至只是后人编出来的术语。哪一种都不能凭这页决定。",
  "把原文和我的理解分开存。以后如果找到现实案例，只对字段，不拿解释替代原文。"
 ]};
 if(entry.id==="p3")return {...entry,highlights:["七个自述","都能找到独立痕迹","证据强度不一样","同一个旧档账号","先不要删掉不合群的案例"],body:[
  "这两个月记了七个自述。七个都能找到至少一项独立痕迹：旧报、报警回执、社区寻人通知、旧照片或者当年的论坛记录。没有一个需要靠‘楼主后来承认是编的’才能排除。",
  "问题是它们支持的东西完全不一样。有的只有失踪和口味变化；有的能确认另一个家的空间细节；有的有技能断层；还有人只是家属觉得‘回来以后变了’。证据强度不能混在一起。",
  "几个帖子下出现过同一个旧档账号，折柳也回复过其中不少。前者也许只是负责整理旧帖，后者本来就长期做旧闻考据。现在都不能因为重复出现就直接当成因果。",
  "先不要删掉‘不合群’的案例。真正有用的可能不是谁最像我，而是哪几个细节总是一起出现。下一步继续查公开记录。"
 ]};
 return entry;
});

export default function Page(){
 const [stage,setStage]=useState<"title"|"login"|"desktop">("title");
 const [intro,setIntro]=useState(true),[app,setApp]=useState<App|null>(null),[max,setMax]=useState(true),[wxRead,setWxRead]=useState(false),[privateUnlocked,setPrivateUnlocked]=useState(false),[noteUnlocked,setNoteUnlocked]=useState(false);
 if(stage==="title")return <main className="title"><section><small>一段发生在朋友电脑里的调查</small><h1>烛阴旧闻</h1><p>沈妍没有赴约。<br/>至少在今天中午时，你还只把它当成爽约。</p><button onClick={()=>setStage("login")}>进入公寓 <ChevronRight/></button></section></main>;
 if(stage==="login")return <main className="login"><div className="clock"><b>19:06</b><span>10月17日　星期六</span></div><section><div className="avatar">妍</div><h2>沈妍</h2><button className="password" onClick={()=>setStage("desktop")}><span>••••••••</span><ChevronRight/></button><p>你和沈妍从小学低年级就认识。你们互为紧急联系人，也一直留着彼此的备用门锁密码。</p></section></main>;
 const open=(x:App)=>{setApp(x);setMax(x==="browser"||x==="verse");if(x==="wechat")setWxRead(true)};
 const appTitle=app==="browser"?"澄川浏览器":app==="wechat"?"微信":app==="notes"?"本地资料":app==="verse"?"澄川浏览器":"访达";
 return <main className="desktop"><header className="sys"><div><b>●</b><strong>{appTitle}</strong><span>文件</span><span>编辑</span></div><div><Wifi/><span>80%</span><span>10月17日 周六 19:06</span></div></header>
  <div className="shortcuts"><Icon label="浏览器" tone="blue" icon={<Globe2/>} onClick={()=>open("browser")}/><Icon label="微信" tone="green" icon={<MessageCircle/>} badge={!wxRead} onClick={()=>open("wechat")}/><Icon label="本地资料" tone="amber" icon={<NotebookPen/>} onClick={()=>open("notes")}/></div>
  {intro&&<div className="overlay"><section className="intro"><small><Clock3/> 2026年10月17日　19:06</small><h2>沈妍没有来。</h2><p>你们约好今天中午见面。她没有出现，电话关机，微信也没有回复。</p><p>傍晚，你用她留给你的备用门锁密码进了公寓。屋里没人，电脑没有关机，微信和浏览器仍保持登录。</p><blockquote><b>徐宁　18:37</b>我去你家看看。看到回我。</blockquote><em>现在还没有理由把这件事说成犯罪。你只是想先确认，她昨天离开后原本打算去哪里。</em><button onClick={()=>setIntro(false)}>查看电脑</button></section></div>}
  {app&&<Window title={appTitle} max={max} allowMax={app==="browser"||app==="verse"} close={()=>setApp(null)} toggle={()=>setMax(!max)}>{app==="browser"?<Browser privateUnlocked={privateUnlocked} setPrivateUnlocked={setPrivateUnlocked}/>:app==="wechat"?<Wechat/>:app==="notes"?<Notes unlocked={noteUnlocked} onUnlock={()=>setNoteUnlocked(true)} openLink={()=>open("verse")}/>:<VersePage/>}</Window>}
  <nav className="dock"><button onClick={()=>open("browser")}><i className="blue"><Globe2/></i></button><button onClick={()=>open("wechat")}><i className="green"><MessageCircle/>{!wxRead&&<b>1</b>}</i></button><button onClick={()=>open("notes")}><i className="amber"><NotebookPen/></i></button></nav>
 </main>
}
function Icon({label,tone,icon,badge,onClick}:{label:string;tone:string;icon:ReactNode;badge?:boolean;onClick:()=>void}){return <button className="desktop-icon" onClick={onClick}><i className={tone}>{icon}{badge&&<b>1</b>}</i><span>{label}</span></button>}
function Window({title,max,allowMax,close,toggle,children}:{title:string;max:boolean;allowMax:boolean;close:()=>void;toggle:()=>void;children:ReactNode}){return <section className={"window "+(max?"max":"float")}><header><div><button className="red" onClick={close}><X/></button><button className="yellow" onClick={close}><Minimize2/></button>{allowMax&&<button className="green-dot" onClick={toggle}><Maximize2/></button>}</div><b>{title}</b><span/></header>{children}</section>}

function Browser({privateUnlocked,setPrivateUnlocked}:{privateUnlocked:boolean;setPrivateUnlocked:(value:boolean)=>void}){
 const [route,setRoute]=useState<Route>({kind:"home"}),[stack,setStack]=useState<Route[]>([]),[q,setQ]=useState(""),[read,setRead]=useState<string[]>([]);
 const go=(next:Route)=>{setStack([...stack,route]);setRoute(next);if(next.kind==="post")setRead([...new Set([...read,next.id])])};
 const back=()=>{if(!stack.length)return;setRoute(stack[stack.length-1]);setStack(stack.slice(0,-1))};
 const search=(value=q)=>{if(value.trim()){setQ(value);go({kind:"search",q:value.trim()})}};
 const openUser=(name:string)=>name==="候鸟第七年"?go({kind:"profile"}):go({kind:"user",name});
 return <div className="browser"><div className="tabs"><span>烛</span><b>烛阴旧闻</b></div><div className="bar"><button onClick={back}><ArrowLeft/></button><button onClick={()=>setRoute({...route})}><RefreshCw/></button><div><LockKeyhole/>www.zhuyinwen.cn / {route.kind}</div><button onClick={()=>go({kind:"history"})}><HistoryIcon/></button></div>
  <div className="site"><ForumHeader q={q} setQ={setQ} search={search} home={()=>go({kind:"home"})} me={()=>go({kind:"profile"})}/>
   {route.kind==="home"&&<ForumHome read={read} open={id=>go({kind:"post",id})} me={()=>go({kind:"profile"})}/>} 
   {route.kind==="post"&&<Thread post={investigationPosts.find(x=>x.id===route.id)!} openUser={openUser}/>} 
   {route.kind==="profile"&&<Profile open={id=>go({kind:"post",id})} secret={()=>go({kind:"private"})}/>} 
   {route.kind==="user"&&<UserProfile name={route.name} open={id=>go({kind:"post",id})}/>} 
   {route.kind==="private"&&<Private unlocked={privateUnlocked} onUnlock={()=>setPrivateUnlocked(true)}/>} 
   {route.kind==="history"&&<HistoryPage open={id=>go({kind:"post",id})} me={()=>go({kind:"profile"})} search={search}/>} 
   {route.kind==="search"&&<Results q={route.q} read={read} open={id=>go({kind:"post",id})} openUser={openUser}/>} 
  </div></div>
}
function ForumHeader({q,setQ,search,home,me}:{q:string;setQ:(x:string)=>void;search:(x?:string)=>void;home:()=>void;me:()=>void}){return <><header className="forum-head"><button onClick={home} className="brand"><i>烛</i><span><b>烛阴旧闻</b><small>民俗 · 旧闻 · 城市记忆</small></span></button><div><button onClick={me}><i className="bird">候</i><span><b>候鸟第七年</b><small>当前登录账号</small></span></button></div></header>
 <nav className="forum-nav"><button onClick={home}><Home/>论坛首页</button><button onClick={me}>我的主页</button></nav>
 <form className="forum-search" onSubmit={e=>{e.preventDefault();search()}}><span><Search/><b>全站搜索</b><small>支持用户名、短语、年份、帖子编号</small></span><label><input value={q} onChange={e=>setQ(e.target.value)} placeholder="搜一个你刚看到的名字、地点或原句"/><button>搜索</button></label></form></>}
function ForumHome({read,open,me}:{read:string[];open:(id:string)=>void;me:()=>void}){const [board,setBoard]=useState("全部");const visible=investigationPosts.filter(p=>!p.hidden).slice(0,10);const shown=board==="全部"?visible:visible.filter(p=>p.board===board);return <main className="forum-page"><div className="columns"><section className="topics"><div className="boards">{["全部","闲聊灌水","旧闻考据","梦与睡眠","生活求助","站务区"].map(x=><button className={x===board?"active":""} onClick={()=>setBoard(x)} key={x}>{x}</button>)}</div><div className="notice"><b>站务</b><button onClick={()=>open("31002")}>旧帖合并、原链接与存档编号说明</button></div><header className="list-head"><b>最新 / 热门</b><span>{shown.length}个主题</span><span>回复 / 浏览</span></header>{shown.map(p=><Row key={p.id} p={p} read={read.includes(p.id)} open={()=>open(p.id)}/>)}</section><aside><button className="account" onClick={me}><i>候</i><b>候鸟第七年</b><small>上次活动：10月16日 19:48</small><dl><div><dt>主题</dt><dd>8</dd></div><div><dt>回复</dt><dd>47</dd></div><div><dt>收藏</dt><dd>12</dd></div></dl><span>查看个人主页</span></button><section className="side"><h3>论坛提示</h3><p>旧内容不会全部出现在首页。找过去的帖子，通常要靠搜索或用户主页。</p></section></aside></div><footer>烛阴旧闻 · 建站于 2008 年 7 月 12 日 · 当前在线 127 人</footer></main>}
function Row({p,read,open}:{p:Post;read:boolean;open:()=>void}){return <button className={"row "+(read?"read":"")} onClick={open}><i>{p.board==="站务区"?"务":p.board==="旧闻考据"?"档":p.board==="梦与睡眠"?"梦":"帖"}</i><span><b>{p.title}</b><p>{p.excerpt}</p><small>{p.author} · {p.board} · {p.date}</small></span><em><b>{p.replies.length}</b><small>{p.views}</small></em></button>}
function Thread({post,openUser}:{post:Post;openUser:(name:string)=>void}){const [zoom,setZoom]=useState<{src:string;caption:string}|null>(null);const media=post.images||(post.image?[{src:post.image,caption:"附件：room_0617.jpg（凭记忆重画的第六版）"}]:[]);return <main className="thread"><div className="crumb">论坛首页 <ChevronRight/> {post.board} <ChevronRight/> #{post.id}</div><header className="thread-title"><span>{post.board}</span><h2>{post.title}</h2><p>楼主：<button className="author-link" onClick={()=>openUser(post.author)}><b>{post.author}</b></button>　发表于 {post.date}　浏览 {post.views}</p></header><Floor user={post.author} time={post.date} no="楼主" role="楼主" openUser={openUser}><>{post.body.map((x,i)=><p key={i}><MarkedText text={x} marks={post.highlights}/></p>)}{!!media.length&&<div className="attachments">{media.map(x=><figure key={x.src}><button onClick={()=>setZoom(x)} title="点击查看原图"><img src={x.src} alt={x.caption}/><span><Maximize2/>查看原图</span></button><figcaption>{x.caption}</figcaption></figure>)}</div>}</></Floor>{post.replies.map((x,i)=><Floor key={i} user={x.user} time={x.time} no={(i+2)+"楼"} role={x.role} openUser={openUser}><MarkedText text={x.text} marks={post.highlights}/></Floor>)}{post.archive&&<div className="archive"><Clock3/><MarkedText text={post.archive} marks={post.highlights}/></div>}<div className="reply"><h3>回复主题</h3><p>该账号近期没有在公开区继续发言。</p></div>{zoom&&<button className="lightbox" onClick={()=>setZoom(null)}><span><X/>关闭</span><img src={zoom.src} alt={zoom.caption}/><em>{zoom.caption}</em></button>}</main>}
function Floor({user,time,no,role,children,openUser}:{user:string;time:string;no:string;role?:string;children:ReactNode;openUser:(name:string)=>void}){return <article className="floor"><aside><i>{user[0]}</i><button className="author-link" onClick={()=>openUser(user)}><b>{user}</b></button>{role&&<em>{role}</em>}<small>注册用户</small></aside><section><header><span>{time}</span><b>{no}</b></header><div>{children}</div></section></article>}
function MarkedText({text,marks=[]}:{text:string;marks?:string[]}){const usable=marks.filter(Boolean).sort((a,b)=>b.length-a.length);if(!usable.length)return <>{text}</>;const escaped=usable.map(x=>x.replace(/[.*+?^${}()|[\]\\]/g,"\\$&"));const parts=text.split(new RegExp(`(${escaped.join("|")})`,"g"));return <>{parts.map((part,i)=>usable.includes(part)?<strong className="clue" key={i}>{part}</strong>:part)}</>}
function Profile({open,secret}:{open:(id:string)=>void;secret:()=>void}){return <main className="profile"><header><i>候</i><span><h2>候鸟第七年</h2><p>偶尔失眠，拍旧楼。私信不看付费解梦。</p><small>注册于 2017-07-12 · 最后活动 2026-10-16 19:48 · 当前登录账号</small></span><dl><div><dt>主题</dt><dd>8</dd></div><div><dt>回复</dt><dd>47</dd></div><div><dt>收藏</dt><dd>12</dd></div></dl></header><div className="profile-grid"><section className="panel"><h3>公开主题（8） <small>按发布时间从早到晚</small></h3>{profile.topics.map(id=>{const p=investigationPosts.find(x=>x.id===id)!;return <button key={id} onClick={()=>open(id)}><span><b>{p.title}</b><small>{p.board} · {p.date}</small></span><ChevronRight/></button>})}</section><aside><button className="secret-card" onClick={secret}><LockKeyhole/><span><b>私密主题（3）</b><small>仅自己可见</small></span><ChevronRight/></button><section className="panel searches"><h3>账号信息</h3><p style={{padding:"12px",margin:0}}>最近搜索不在主页直接展示。需要从浏览器本地历史里判断她最近查过什么。</p></section></aside></div></main>}
function UserProfile({name,open}:{name:string;open:(id:string)=>void}){const rows=useMemo(()=>{const out:{id:string;kind:string;title:string;text:string;date:string}[]=[];investigationPosts.forEach(p=>{if(p.author===name)out.push({id:p.id,kind:"主题",title:p.title,text:p.excerpt,date:p.date});p.replies.forEach(r=>{if(r.user===name)out.push({id:p.id,kind:"回复",title:p.title,text:r.text,date:r.time})})});return out},[name]);return <main className="profile"><header><i>{name[0]}</i><span><h2>{name}</h2><p>公开账号资料</p><small>可查看仍保留在站内的公开主题与回复记录</small></span><dl><div><dt>可见记录</dt><dd>{rows.length}</dd></div></dl></header><section className="panel"><h3>公开发言记录</h3>{rows.length?rows.map((r,i)=><button key={r.id+"-"+i} onClick={()=>open(r.id)}><span><b>{r.kind} · {r.title}</b><small>{r.date}</small><p>{r.text}</p></span><ChevronRight/></button>):<div className="empty"><p>没有可见记录，或旧内容已无法通过该账号索引。</p></div>}</section></main>}
function Private({unlocked,onUnlock}:{unlocked:boolean;onUnlock:()=>void}){
 const [pwd,setPwd]=useState(""),[error,setError]=useState(""),[id,setId]=useState<string|null>(null),[zoom,setZoom]=useState<{src:string;caption:string}|null>(null);
 const active=id?investigationPrivateEntries.find(x=>x.id===id):null;
 if(unlocked)return <main className="private forum-private"><div className="private-crumb">个人主页 <ChevronRight/> 私密主题</div><section className="private-account-band"><i>候</i><span><small>候鸟第七年</small><h2>私密主题</h2></span><em><LockKeyhole/>仅当前账号可见</em></section>{!active?<section className="private-topic-list"><header><span><b>私密主题</b><small>{investigationPrivateEntries.length} 篇内容，按保存时间排列</small></span><em>最后编辑</em></header>{investigationPrivateEntries.map(x=><button key={x.id} onClick={()=>setId(x.id)}><i><LockKeyhole/></i><span><b>{x.title}</b><p>{x.body[0]}</p></span><time>{x.date.split(" ")[0]}<small>{x.date.split(" ")[1]}</small></time></button>)}</section>:<section className="private-thread"><button className="private-back" onClick={()=>setId(null)}><ArrowLeft/>返回私密主题</button><header className="private-thread-title"><small>私密主题</small><h2>{active.title}</h2><p>{active.date}</p></header><article className="private-post"><header><i>候</i><span><b>候鸟第七年</b><small>仅自己可见 · 编辑于 {active.date}</small></span><em><LockKeyhole/>私密</em></header><div>{active.body.map((x,i)=><p key={i}><MarkedText text={x} marks={active.highlights}/></p>)}{active.images?.map(x=><figure key={x.src}><button onClick={()=>setZoom(x)}><img src={x.src} alt={x.caption}/><span><Maximize2/>查看原图</span></button><figcaption>{x.caption}</figcaption></figure>)}</div></article></section>}{zoom&&<button className="lightbox" onClick={()=>setZoom(null)}><span><X/>关闭</span><img src={zoom.src} alt={zoom.caption}/><em>{zoom.caption}</em></button>}</main>;
 const chars=[...pwd];
 return <main className="private private-gate"><div className="private-crumb">个人主页 <ChevronRight/> 私密主题</div><section className="private-gate-card"><div className="private-gate-mark"><LockKeyhole/></div><small>候鸟第七年</small><h2>私密主题</h2><p>此区域使用独立访问口令。</p><form onSubmit={e=>{e.preventDefault();if(pwd==="身非我身名非我名"){onUnlock();setError("")}else setError(pwd?"口令不正确。":"请输入访问口令。")}}><label className="secret-boxes"><input autoComplete="off" value={pwd} onChange={e=>{const value=[...e.target.value.replace(/[，。、“”‘’\s]/g,"")].slice(0,8).join("");setPwd(value);setError("")}} aria-label="八字访问口令"/>{Array.from({length:8},(_,i)=><span className={i===chars.length?"current":""} key={i}>{chars[i]||""}</span>)}</label><small>8 个汉字</small><button>进入</button></form>{error&&<em>{error}</em>}</section></main>
}
function HistoryPage({open,me,search}:{open:(id:string)=>void;me:()=>void;search:(q:string)=>void}){const natural=[history[0],{title:"河临明日天气",info:"天气 · 多云转小雨"},history[1],{title:"公交换乘：青梧区 → 河西路",info:"地图 · 页面已关闭"},history[5],{title:"胶片冲洗店营业时间",info:"本地生活 · 页面已关闭"},history[2],history[6],history[4],{title:"旧单位房 厨房门 朝走廊",info:"图片搜索 · 页面已关闭"}];return <main className="history"><header><HistoryIcon/><span><h2>浏览记录</h2><p>沈妍的本地记录</p></span></header><section>{natural.map((x:any,i)=><button key={i} onClick={()=>x.id?open(x.id):x.profile?me():x.query?search(x.query):undefined}><time>{i<4?"昨天":"10月15日"}</time><span><b>{x.title}</b><small>{x.info}</small></span><ChevronRight/></button>)}</section></main>}
function Results({q,read,open,openUser}:{q:string;read:string[];open:(id:string)=>void;openUser:(name:string)=>void}){const n=norm(q);const found=useMemo(()=>{const tokens=q.split(/\s+/).map(norm).filter(Boolean);return investigationPosts.filter(p=>{const hay=norm([p.title,p.author,p.excerpt,...p.body,...(p.terms||[]),p.archive||"",...p.replies.flatMap(r=>[r.user,r.text])].join(" "));return tokens.every(token=>hay.includes(token))||n===p.id})},[q,n]);const users=useMemo(()=>{const names=new Set<string>();investigationPosts.forEach(p=>{names.add(p.author);p.replies.forEach(r=>names.add(r.user))});return [...names].filter(name=>norm(name).includes(n)).slice(0,8)},[n]);return <main className="results"><header><Search/><span><h2>搜索“{q}”</h2><p>公开主题 {found.length} 条{users.length?`，用户 ${users.length} 条`:""}</p></span></header><section>{users.map(name=><button className="user-result" onClick={()=>openUser(name)} key={name}><i>{name[0]}</i><span><b>用户：{name}</b><small>查看公开主题与回复历史</small></span><ChevronRight/></button>)}{found.map(p=><Row key={p.id} p={p} read={read.includes(p.id)} open={()=>open(p.id)}/>)}{!found.length&&!users.length&&<div className="empty"><Search/><h3>没有找到完全匹配的公开内容</h3><p>试试更短的人名、地点、年份、原句或帖子编号。</p></div>}</section></main>}
const norm=(x:string)=>x.toLowerCase().replace(/[“”‘’#，。！？、\s]/g,"");

function Notes({unlocked,onUnlock,openLink}:{unlocked:boolean;onUnlock:()=>void;openLink:()=>void}){
 const [pwd,setPwd]=useState(""),[error,setError]=useState(""),[attempts,setAttempts]=useState(0),[selected,setSelected]=useState<"report"|"room"|"cache">("report");
 const submit=(e:FormEvent)=>{e.preventDefault();if(pwd==="0407"){onUnlock();setError("")}else{setAttempts(x=>x+1);setError(pwd?"密码不正确":"请输入密码")}};
 const notes=[
  {id:"report" as const,title:"河临晚报索引",kind:"文本记录",preview:"2004 年两条旧报记录"},
  {id:"room" as const,title:"房间细节",kind:"观察记录",preview:"红盒、蓝窗帘、厨房门"},
  {id:"cache" as const,title:"缓存页",kind:"受保护文件",preview:unlocked?"zhuyinwen.cn/archive/cache/……":"需要四位密码"}
 ];
 return <main className="local-records"><aside className="record-index"><header><span><NotebookPen/></span><div><b>本地资料</b><small>沈妍的电脑 · 3 个文件</small></div></header><nav>{notes.map(x=><button className={selected===x.id?"active":""} onClick={()=>setSelected(x.id)} key={x.id}><span className="record-file-icon">{x.id==="cache"&&!unlocked?<LockKeyhole/>:<NotebookPen/>}</span><span><b>{x.title}</b><small>{x.kind}</small><p>{x.preview}</p></span><ChevronRight/></button>)}</nav></aside><section className="record-view">{selected==="report"?<article className="record-document"><header><small>文本记录</small><h1>河临晚报索引</h1></header><p>2004 年的两条旧报记录，应该说的是同一个人。</p><section className="record-timeline"><span><time>2004-07-17</time><b>失踪启事</b><small>青梧区少年宫外</small></span><span><time>2004-07-30</time><b>找回简讯</b><small>河临南站附近</small></span></section><div className="record-clue"><b>缓存页</b><p>两个版号，按“失踪—找回”的顺序。</p></div></article>:selected==="room"?<article className="record-document"><header><small>观察记录</small><h1>房间细节</h1></header><dl className="room-record"><div><dt>餐边柜</dt><dd>红色铁皮盒，套盖，打开前会卡一下</dd></div><div><dt>窗帘</dt><dd>蓝色，右边晒得更浅</dd></div><div><dt>厨房门</dt><dd>朝走廊方向开</dd></div><div><dt>走廊</dt><dd>浅色小方砖，有几块裂了</dd></div></dl></article>:unlocked?<article className="record-document cache-record"><header><small>受保护文件</small><h1>缓存页</h1></header><p className="cache-address">https://www.zhuyinwen.cn/archive/cache/baishesong-1986.html</p><button onClick={openLink}><ExternalLink/>打开缓存页面</button></article>:<div className="record-lock"><div className="record-lock-icon"><LockKeyhole/></div><small>受保护文件</small><h2>缓存页</h2><p>输入四位密码。</p><form onSubmit={submit}><input type="password" inputMode="numeric" maxLength={4} value={pwd} onChange={e=>{setPwd(e.target.value.replace(/\D/g,"").slice(0,4));setError("")}} placeholder="••••" autoComplete="off"/><button>解锁</button></form>{error&&<em>{error}</em>}{attempts>=2&&<small className="record-hint"><b>提示</b>先看“河临晚报索引”，再去论坛找对应版号。</small>}</div>}</section></main>
}

function VersePage(){return <main className="verse-page"><header><LockKeyhole/><span>www.zhuyinwen.cn/archive/cache/baishesong-1986.html</span><b>缓存页面</b></header><section className="verse-image-view simple"><figure><img src="assets/baishesong-recovered-scan-v1.webp" alt="一张来源不明的黑纸红字抄写页扫描件"/><figcaption><span>scan_07_untitled.tif</span><em>来源字段已删除 · 缓存于 2026-10-16 19:49</em></figcaption></figure></section></main>}
function Wechat(){const [id,setId]=useState("x"),[q,setQ]=useState("");const active=chats.find(x=>x.id===id)!;const visible=chats.filter(x=>(x.name+x.preview).includes(q));return <div className="wechat"><aside><header><i>妍</i><span><b>沈妍</b><small>微信已登录</small></span></header><label><Search/><input value={q} onChange={e=>setQ(e.target.value)} placeholder="搜索联系人和消息"/></label>{visible.map(x=><button className={x.id===id?"active":""} onClick={()=>setId(x.id)} key={x.id}><i>{x.name[0]}</i><span><b>{x.name}</b><small>{x.preview}</small></span></button>)}</aside><main><header><b>{active.name}</b><small>聊天记录</small></header><section>{active.messages.map((m,i)=><div key={i}>{m[0]&&<time>{m[0]}</time>}<article className={m[1]==="沈妍"?"mine":""}><i>{m[1][0]}</i><p>{m[2]}</p></article></div>)}</section><footer>该电脑上的微信仍保持登录 · 当前未连接手机</footer></main></div>}
