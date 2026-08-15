"use client";

import {FormEvent,useMemo,useState} from "react";
import {ArrowLeft,ChevronRight,History,Home,MessageCircle,Search} from "lucide-react";
import styles from "./v9.module.css";

type Reply={user:string;text:string};
type Post={id:string;title:string;author:string;board:string;date:string;views:number;excerpt:string;body:string[];replies:Reply[];terms?:string[];hidden?:boolean};
type Route={kind:"home"}|{kind:"post";id:string}|{kind:"search";q:string}|{kind:"user";name:string}|{kind:"history"}|{kind:"pm"};

const posts:Post[]=[
 {id:"34021",title:"凌晨两点楼上每天拖椅子，录音却录不到",author:"卷毛",board:"闲聊灌水",date:"今天 00:12",views:482,excerpt:"物业最后查出来像是水箱增压泵。",body:["这周连续四天，凌晨两点零几分，天花板先“咚”一下，再拖三四秒。","更新：物业说两点是水箱补水，今晚先停泵排查。"],replies:[{user:"修空调的老周",text:"先查楼顶增压泵，楼板传声很像家具。"}]},
 {id:"33988",title:"梦里能读清手机上的字正常吗",author:"双拼苦手",board:"梦与睡眠",date:"今天 09:17",views:801,excerpt:"有人说梦里看不清字，但我连请假消息都记得。",body:["我最近做梦会刷手机，聊天列表和时间都很清楚，醒来一查根本没有。"],replies:[{user:"认知实验室民工",text:"不是判断清醒梦的可靠方法。"}]},
 {id:"33897",title:"分享一组岚棉三厂旧址的窗户照片",author:"候鸟第七年",board:"旧闻考据",date:"10月13日 23:44",views:1437,excerpt:"只是拍旧楼。4栋右侧窗框的颜色很奇怪。",body:["上周去了趟岚州，拍了一组岚棉三厂旧家属区。大部分楼已经封了。","我本来只是想找九十年代的蓝色窗框。奇怪的是，看到4栋的时候有一种非常熟悉的感觉。不是“来过”，更像是知道拐进去以后楼梯在哪。","我没进去。旧楼已经封闭，别学我翻围栏。"],replies:[{user:"旧纸鸢",text:"三厂资料可以去岚州市图地方文献室查，网上缺得厉害。"},{user:"折柳",text:"熟悉感先记，不要立刻拿它证明什么。"}],terms:["岚棉三厂","4栋","岚州"]},
 {id:"20847",title:"最近总梦见一间没住过的房子",author:"候鸟第七年",board:"梦与睡眠",date:"6月18日 01:47",views:2841,excerpt:"红铁皮糖盒、褪色蓝窗帘、朝走廊开的厨房门。",body:["这件事从去年十一月开始。最近三个月频率突然变高。","梦里是一间旧单位房。餐边柜上有一个红色铁皮糖盒，右边那幅蓝窗帘晒得发灰，厨房门朝走廊方向开。","有人在厨房里叫我。以前只记得最后两个音像“楠楠”。我不确定是不是名字，也可能只是囡囡。","最不舒服的是，醒来以后我会有几分钟非常确定：那才是我家。"],replies:[{user:"逆光风筝",text:"“楠楠”也不一定是名字，先别补汉字。"},{user:"折柳",text:"先画结构，不要急着给梦里的人起名字。"},{user:"午后雷阵雨",text:"长期反复梦建议继续看睡眠门诊。"}],terms:["楠楠","蓝窗帘","红铁皮糖盒"]},
 {id:"33710",title:"老厂区蓝色窗框到底是什么年代流行的",author:"旧玻璃",board:"旧闻考据",date:"10月12日 18:40",views:590,excerpt:"全国很多单位房都用过，不能靠窗框认地点。",body:["整理旧建筑照片时发现八九十年代蓝色金属窗框特别常见。"],replies:[{user:"旧纸鸢",text:"厂区宿舍标准图纸比窗框颜色靠谱。"}]},
 {id:"33401",title:"找回来的猫突然不吃原来的粮，是不是吓到了",author:"橘猫法官",board:"生活求助",date:"10月10日 22:18",views:712,excerpt:"失踪三天后自己回家，先排除口腔问题。",body:["猫跑出去三天自己回来了，性格也比以前黏人。"],replies:[{user:"猫砂铲屎官",text:"先体检。"}]},
 {id:"33120",title:"2000年代地方报纸怎么查整版",author:"地方志小王",board:"旧闻考据",date:"10月8日 16:02",views:1001,excerpt:"地方文献室常按日期与版次保存缩微或扫描。",body:["如果知道日期，先查地方文献室索引，再按版号调整卷。"],replies:[{user:"报刊索引",text:"很多旧报在线只能看到目录，整版要馆内调。"}]},
 {id:"32902",title:"求推荐不收费的睡眠记录软件",author:"晨昏线",board:"梦与睡眠",date:"10月5日 13:12",views:405,excerpt:"想记录梦境，但不想买会员。",body:["只需要文字和日期，不需要AI解梦。"],replies:[{user:"候鸟第七年",text:"我后来直接用本地表格，避免看前一天内容影响回忆。"}]},
 {id:"16440",hidden:true,title:"岚棉三厂四栋夹墙里翻到一页抄写纸，求认是什么",author:"灰浆桶",board:"旧闻考据",date:"2014-08-03",views:1872,excerpt:"4栋改管线时夹墙里掉出的复印页。",body:["家里以前住岚棉三厂家属区4栋。2010年改管线时，从厨房和走廊之间的夹墙里掉出几张复印纸。","纸上反复出现“形”“名”“忆”几个字，标题最后只剩一个“疏”。"],replies:[{user:"旧纸鸢",text:"2011年有人发过相似页，标题更完整。"},{user:"折柳",text:"现代制表线和字体，至少不是古经原页。"}],terms:["岚棉三厂","4栋","夹墙","形","名","忆"]},
 {id:"09114",hidden:true,title:"【旧报】岚棉三厂家属区九岁女童失踪，十三日后异地找回",author:"报刊索引",board:"旧闻考据",date:"2009-05-22",views:1294,excerpt:"2004年岚州地方报纸摘录。",body:["2004-07-18，岚棉三厂家属区九岁女童林楠失踪，家属当日报警。","2004-07-31，林楠在外市客运站附近被找到。旧报称其身体无明显外伤，但对失踪期间经历无法完整说明。"],replies:[{user:"旧纸鸢",text:"这种找回简讯很多只剩几十字。"},{user:"折柳",text:"如果要做横向比较，先把原报日期、年龄、失踪时长记清楚。"}],terms:["岚棉三厂","林楠","2004","失踪","找回"]},
 {id:"09831",hidden:true,title:"【旧报】九岁女童失踪十三天后在河临南站附近被找回",author:"报刊索引",board:"旧闻考据",date:"2009-05-18",views:935,excerpt:"2004年河临地方报纸索引。",body:["2004-07-17，九岁沈妍在河临市青梧区少年宫外失踪。","2004-07-30，沈妍在河临南站附近被找到，失踪共十三天。"],replies:[{user:"旧纸鸢",text:"版号能查到的话最好一起记。"},{user:"折柳",text:"两个地方的旧报不要只凭“十三天”就硬连。"}],terms:["沈妍","2004","失踪","十三天","河临南站"]},
 {id:"14692",hidden:true,title:"有没有人记得“被找回来”之前的家",author:"反方向的钟",board:"生活求助",date:"2019-04-07",views:6318,excerpt:"小时候走失后，一直觉得父母把自己的名字叫错了。",body:["我六岁时走失过几天，被送回来以后，有很长一段时间觉得他们叫我的名字不对。","我脑子里还有另一个家：鞋要脱在门外，左边抽屉里有一把缺齿木梳。","成年后查到当年的寻人启事，失踪和找回时间都能对上。"],replies:[{user:"二十三页",text:"先找当年寻人启事，比回忆可靠。"},{user:"折柳",text:"能核实旧报的话，把原始信息和成年后的解释分开写。"},{user:"照骨",text:"回来以后有没有突然怕以前不怕的气味？"}],terms:["被找回来","走失","另一个家","折柳","照骨"]},
 {id:"15103",hidden:true,title:"我表哥小时候被换过魂，回来后彻底变了一个人",author:"孤坟蹦迪王",board:"灵异杂谈",date:"2019-09-11",views:7720,excerpt:"楼主称表哥走失七天后性格大变。",body:["我表哥小时候失踪七天，回来以后连狗都不认识。","我舅说当年报过警，但具体年份我不记得。"],replies:[{user:"折柳",text:"你去年帖子里说自己父母都是独生子女，哪来的表哥？"},{user:"孤坟蹦迪王",text:"网络称呼而已，别抬杠。"}],terms:["换魂","失踪","回来"]},
 {id:"17119",hidden:true,title:"七岁走失后总觉得自己应该叫另一个名字",author:"迟迟",board:"生活求助",date:"2021-11-03",views:4190,excerpt:"旧报可以核验；用户不愿公开真实姓名。",body:["七岁时走失过一周，回来后有很长时间觉得家里人叫错了名字。","我后来找到旧报，时间能对上。更怪的是我回来后不会骑原来会骑的自行车。","不贴真实姓名。只想知道有没有人有相似体验。"],replies:[{user:"候鸟第七年",text:"我小时候也失踪过。方便私信吗？"},{user:"迟迟",text:"可以，但别在公开区写真名。"},{user:"折柳",text:"先留好原始旧报，不要只靠家人口述。"},{user:"照骨",text:"你被找到当天，有没有人叫过你一个完全陌生的名字？"}],terms:["迟迟","失踪","另一个名字","旧报","折柳","照骨"]},
 {id:"15571",hidden:true,title:"小时候失踪后突然改用左手，有类似的吗",author:"夏夜停电",board:"生活求助",date:"2020-02-14",views:2040,excerpt:"自称八岁时失踪五天，回来后惯用手改变。",body:["家里一直说我八岁走丢五天，回来以后突然改成左手。","但我问父母具体日期，他们谁都说不清，也找不到报警记录。"],replies:[{user:"折柳",text:"如果没有任何可核验记录，先不要把成年习惯变化反推成失踪证据。"},{user:"照骨",text:"有没有反复梦见固定的室内？"}],terms:["失踪","惯用手","折柳","照骨"]}
];

const userMeta:Record<string,{bio:string;since:string}>={
 "候鸟第七年":{bio:"偶尔失眠，拍旧楼。不接付费解梦。",since:"2017-07-12"},
 "折柳":{bio:"旧闻、地方志、民俗文本。引用请带出处。",since:"2009-02-03"},
 "照骨":{bio:"记录，不解释。",since:"2011-09-17"},
 "迟迟":{bio:"偶尔上来看看。私信不常回。",since:"2020-04-12"},
 "孤坟蹦迪王":{bio:"故事当故事看。",since:"2018-05-19"}
};

const initialHistory=[
 {title:"最近总梦见一间没住过的房子",info:"烛阴旧闻 · #20847",route:{kind:"post",id:"20847"} as Route},
 {title:"岚州天气",info:"澄川搜索 · 10月13日",route:null},
 {title:"岚棉三厂旧址公交",info:"澄川地图 · 10月13日",route:null},
 {title:"睡眠门诊预约",info:"河临市第一医院 · 10月12日",route:null},
 {title:"胶片冲扫店营业时间",info:"澄川搜索 · 10月10日",route:null},
 {title:"候鸟第七年 - 用户主页",info:"烛阴旧闻 · 10月09日",route:{kind:"user",name:"候鸟第七年"} as Route}
];

function norm(v:string){return v.toLowerCase().replace(/[“”‘’#，。！？、\s]/g,"")}
function hay(p:Post){return norm([p.title,p.author,p.board,p.excerpt,...p.body,...p.replies.flatMap(r=>[r.user,r.text]),...(p.terms||[])].join(" "))}

export default function V9ForumSlice(){
 const [route,setRoute]=useState<Route>({kind:"home"});
 const [stack,setStack]=useState<Route[]>([]);
 const [q,setQ]=useState("");
 const [searches,setSearches]=useState<string[]>([]);
 const [pmUnlocked,setPmUnlocked]=useState(false);
 const [pmRead,setPmRead]=useState(false);
 const [pmChoice,setPmChoice]=useState<null|"safe"|"direct">(null);

 const go=(next:Route)=>{setStack(s=>[...s,route]);setRoute(next)};
 const back=()=>{setStack(s=>{if(!s.length)return s;setRoute(s[s.length-1]);return s.slice(0,-1)})};
 const search=(value=q)=>{
  const clean=value.trim(); if(!clean)return;
  setQ(clean); setSearches(s=>[clean,...s.filter(x=>x!==clean)].slice(0,8));
  if((norm(clean).includes("折柳")||norm(clean).includes("照骨")||norm(clean).includes("林楠"))&&searches.some(x=>norm(x).includes("失踪"))) setPmUnlocked(true);
  go({kind:"search",q:clean});
 };
 const userRows=(name:string)=>posts.flatMap(p=>[
  ...(p.author===name?[{post:p,label:"主题",text:p.title}]:[]),
  ...p.replies.filter(r=>r.user===name).map(r=>({post:p,label:"回复",text:r.text}))
 ]);
 const results=useMemo(()=>route.kind!=="search"?[]:posts.filter(p=>route.q.split(/\s+/).map(norm).filter(Boolean).every(t=>hay(p).includes(t))),[route]);

 return <main className={styles.desktop}><section className={styles.window}>
  <header className={styles.browserbar}><button onClick={back}><ArrowLeft/></button><div className={styles.url}>🔒 www.zhuyinwen.cn / {route.kind}</div><button onClick={()=>go({kind:"history"})}><History/></button></header>
  <section className={styles.forum}>
   <header className={styles.head}><div className={styles.logo}>烛</div><div><h1>烛阴旧闻</h1><p>民俗 · 旧闻 · 城市记忆</p></div><div className={styles.account}><b>候鸟第七年</b><small>当前登录账号</small></div></header>
   <nav className={styles.nav}><button onClick={()=>go({kind:"home"})}><Home/>论坛首页</button><button onClick={()=>go({kind:"user",name:"候鸟第七年"})}>我的主页</button><button onClick={()=>{setPmRead(true);go({kind:"pm"})}}><MessageCircle/>私信{pmUnlocked&&!pmRead&&<em>1</em>}</button></nav>
   <form className={styles.searchbar} onSubmit={(e:FormEvent)=>{e.preventDefault();search()}}><Search/><input value={q} onChange={e=>setQ(e.target.value)} placeholder="搜索用户名、地点、年份、帖子编号或原句"/><button>全站搜索</button></form>
   <div className={styles.main}><section className={styles.content}>
    {route.kind==="home"&&<><div className={styles.pagehead}><h2>论坛首页</h2><p>最新与热门主题。旧主题不会全部出现在首页。</p></div>{posts.filter(p=>!p.hidden).map(p=><Topic key={p.id} p={p} open={()=>go({kind:"post",id:p.id})}/>)}</>}
    {route.kind==="search"&&<><div className={styles.pagehead}><h2>搜索“{route.q}”</h2><p>公开索引 {results.length} 条</p></div>{results.length?results.map(p=><Topic key={p.id} p={p} open={()=>go({kind:"post",id:p.id})}/>):<div className={styles.empty}>没有找到完全匹配的公开内容。试试更短的人名、地点、年份或账号。</div>}</>}
    {route.kind==="post"&&<Thread p={posts.find(p=>p.id===route.id)!} openUser={name=>go({kind:"user",name})}/>}
    {route.kind==="user"&&<UserPage name={route.name} rows={userRows(route.name)} openPost={id=>go({kind:"post",id})}/>}
    {route.kind==="history"&&<><div className={styles.pagehead}><h2>浏览记录</h2><p>沈妍这几天的浏览记录，主线和日常混在一起。</p></div>{initialHistory.map((h,i)=><button key={i} className={styles.historyrow} onClick={()=>h.route&&go(h.route)} disabled={!h.route}><span><b>{h.title}</b><small>{h.info}</small></span><ChevronRight/></button>)}</>}
    {route.kind==="pm"&&<PrivateMessages unlocked={pmUnlocked} choice={pmChoice} choose={setPmChoice}/>} 
   </section>
   <aside className={styles.side}>
    <section><h3>当前账号</h3><button onClick={()=>go({kind:"user",name:"候鸟第七年"})}>查看候鸟第七年的公开发言</button></section>
    <section><h3>最近搜索</h3>{searches.length?searches.map(s=><button key={s} onClick={()=>search(s)}>{s}</button>):<p>暂无。</p>}</section>
    <section><h3>论坛说明</h3><p>点击用户名可查看该账号的公开主题与回复记录。搜索结果来自公开索引；部分旧帖不会出现在首页。</p></section>
   </aside></div>
  </section>
 </section></main>
}

function Topic({p,open}:{p:Post;open:()=>void}){return <button className={styles.topic} onClick={open}><i>{p.board.includes("旧闻")?"档":p.board.includes("梦")?"梦":"帖"}</i><span><b>{p.title}</b><p>{p.excerpt}</p><small>{p.author} · {p.board} · {p.date}</small></span><em>{p.replies.length} 回复<br/>{p.views} 浏览</em></button>}

function Thread({p,openUser}:{p:Post;openUser:(name:string)=>void}){return <><div className={styles.crumb}>论坛首页 <ChevronRight/> {p.board} <ChevronRight/> #{p.id}</div><header className={styles.threadtitle}><span>{p.board}</span><h2>{p.title}</h2><p>楼主：{p.author} · {p.date} · 浏览 {p.views}</p></header><Floor user={p.author} label="楼主" onUser={()=>openUser(p.author)}>{p.body.map((x,i)=><p key={i}>{x}</p>)}</Floor>{p.replies.map((r,i)=><Floor key={i} user={r.user} label={`${i+2}楼`} onUser={()=>openUser(r.user)}><p>{r.text}</p></Floor>)}<div className={styles.replynote}>当前试玩不开放自由回复。等论坛具有真实反馈逻辑后再开放发言。</div></>}

function Floor({user,label,onUser,children}:{user:string;label:string;onUser:()=>void;children:React.ReactNode}){return <article className={styles.floor}><aside><i>{user[0]}</i><button onClick={onUser}>{user}</button><small>注册用户</small></aside><section><header>{label}</header>{children}</section></article>}

function UserPage({name,rows,openPost}:{name:string;rows:{post:Post;label:string;text:string}[];openPost:(id:string)=>void}){const meta=userMeta[name]||{bio:"该用户未填写简介。",since:"未知"};return <><header className={styles.userhead}><i>{name[0]}</i><span><h2>{name}</h2><p>{meta.bio}</p><small>注册于 {meta.since} · 公开发言 {rows.length} 条</small></span></header><div className={styles.usertabs}>公开发言记录</div>{rows.length?rows.map((r,i)=><article key={`${r.post.id}-${i}`} className={styles.userrow}><span>{r.label}</span><button onClick={()=>openPost(r.post.id)}>{r.post.title}</button><p>{r.text}</p><small>{r.post.date} · #{r.post.id}</small></article>):<div className={styles.empty}>没有可见历史记录。</div>}</>}

function PrivateMessages({unlocked,choice,choose}:{unlocked:boolean;choice:null|"safe"|"direct";choose:(v:"safe"|"direct")=>void}){if(!unlocked)return <div className={styles.empty}>没有新的私信。</div>;return <><div className={styles.pagehead}><h2>私信</h2><p>当前登录：候鸟第七年</p></div><section className={styles.chat}><p><b>迟迟</b><br/>你是不是在翻候鸟以前那些帖子？</p><p><b>迟迟</b><br/>如果是她本人，让她别在公开区写真名。</p>{choice&&<p className={styles.mine}><b>候鸟第七年</b><br/>{choice==="safe"?"只是帮她找一些旧资料。":"沈妍失踪了。你知道什么？"}</p>}{choice==="safe"&&<p><b>迟迟</b><br/>……那先别联系那些主动问地址的人。尤其是总问“被找到当天发生了什么”的。</p>}{choice==="direct"&&<p><b>迟迟</b><br/>我不知道她现在在哪。你如果不是她本人，先别在这个号上继续写真名。去看她以前给我的公开回复。</p>}{!choice&&<div className={styles.choices}><button onClick={()=>choose("safe")}>只是帮她找一些旧资料。</button><button onClick={()=>choose("direct")}>沈妍失踪了。你知道什么？</button></div>}</section></>}
