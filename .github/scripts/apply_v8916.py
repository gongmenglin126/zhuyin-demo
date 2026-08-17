from pathlib import Path
import re


def read(path):
    return Path(path).read_text(encoding='utf-8')


def write(path, text):
    Path(path).write_text(text, encoding='utf-8')


def once(s, old, new, label):
    if old not in s:
        raise SystemExit(f'missing pattern: {label}')
    return s.replace(old, new, 1)


def between(s, start, end, replacement, label):
    a=s.find(start)
    if a < 0:
        raise SystemExit(f'missing start: {label}')
    b=s.find(end, a)
    if b < 0:
        raise SystemExit(f'missing end: {label}')
    return s[:a] + replacement + s[b:]

# ---------------- app/page.tsx ----------------
p='app/page.tsx'
s=read(p)
s=once(s,
'import PrivateArea from "./PrivateArea";\n',
'import PrivateArea from "./PrivateArea";\nimport AdminPortal from "./AdminPortal";\n',
'admin import')
s=once(s,
'type Route={kind:"home"}|{kind:"post",id:string}|{kind:"profile"}|{kind:"user",name:string}|{kind:"private"}|{kind:"history"}|{kind:"search",q:string};',
'type Route={kind:"home"}|{kind:"post",id:string}|{kind:"profile"}|{kind:"user",name:string}|{kind:"private"}|{kind:"history"}|{kind:"search",q:string}|{kind:"account"};',
'account route')
s=once(s,
'const investigationPrivateEntries=privateEntries;\n',
'const investigationPrivateEntries=privateEntries;\nlet persistedForumIdentity:"shenyan"|"admin"="shenyan";\n',
'persisted forum identity')
s=once(s,
' const [route,setRoute]=useState<Route>(initialPostId?{kind:"post",id:initialPostId}:{kind:"home"}),[stack,setStack]=useState<Route[]>([]),[q,setQ]=useState(""),[read,setRead]=useState<string[]>(initialPostId?[initialPostId]:[]);',
' const [route,setRoute]=useState<Route>(initialPostId?{kind:"post",id:initialPostId}:{kind:"home"}),[stack,setStack]=useState<Route[]>([]),[q,setQ]=useState(""),[read,setRead]=useState<string[]>(initialPostId?[initialPostId]:[]);\n const [forumIdentity,setForumIdentity]=useState<"shenyan"|"admin">(()=>persistedForumIdentity);',
'browser identity state')
s=once(s,
' const back=()=>{if(!stack.length)return;setRoute(stack[stack.length-1]);setStack(stack.slice(0,-1))};',
' const back=()=>{if(forumIdentity==="admin"||!stack.length)return;setRoute(stack[stack.length-1]);setStack(stack.slice(0,-1))};',
'admin back lock')
new_browser_return=''' return <div className="browser"><div className="tabs"><span>烛</span><b>烛阴旧闻</b></div><div className="bar"><button onClick={back}><ArrowLeft/></button><button onClick={()=>setRoute({...route})}><RefreshCw/></button><div><LockKeyhole/>www.zhuyinwen.cn / {forumIdentity==="admin"?"admin":route.kind}</div><button onClick={()=>forumIdentity==="shenyan"&&go({kind:"history"})}><HistoryIcon/></button></div>
  <div className="site">
   {forumIdentity==="admin"?<AdminPortal loggedIn={true} onAdminLogin={()=>{}} onCancel={()=>{}}/>:route.kind==="account"?<AdminPortal loggedIn={false} onCancel={back} onAdminLogin={()=>{persistedForumIdentity="admin";setForumIdentity("admin");setStack([])}}/>:<>
    <ForumHeader q={q} setQ={setQ} search={search} home={()=>go({kind:"home"})} me={()=>go({kind:"profile"})} switchAccount={()=>go({kind:"account"})}/>
    {route.kind==="home"&&<ForumHome read={read} open={id=>go({kind:"post",id})} me={()=>go({kind:"profile"})}/>} 
    {route.kind==="post"&&<Thread post={investigationPosts.find(x=>x.id===route.id)!} openUser={openUser} onCopyMaterial={onCopyMaterial}/>} 
    {route.kind==="profile"&&<Profile open={id=>go({kind:"post",id})} secret={()=>go({kind:"private"})}/>} 
    {route.kind==="user"&&<UserProfile name={route.name} open={id=>go({kind:"post",id})}/>} 
    {route.kind==="private"&&<PrivateArea entries={investigationPrivateEntries} unlocked={privateUnlocked} onUnlock={()=>setPrivateUnlocked(true)} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>} 
    {route.kind==="history"&&<HistoryPage open={id=>go({kind:"post",id})} me={()=>go({kind:"profile"})} search={search}/>} 
    {route.kind==="search"&&<Results q={route.q} read={read} open={id=>go({kind:"post",id})} openUser={openUser}/>} 
   </>}
  </div></div>
'''
s=between(s,' return <div className="browser">','}\nfunction ForumHeader',new_browser_return,'browser render')
new_header='''function ForumHeader({q,setQ,search,home,me,switchAccount}:{q:string;setQ:(x:string)=>void;search:(x?:string)=>void;home:()=>void;me:()=>void;switchAccount:()=>void}){return <><header className="forum-head"><button onClick={home} className="brand"><i>烛</i><span><b>烛阴旧闻</b><small>民俗 · 旧闻 · 城市记忆</small></span></button><div style={{display:"flex",alignItems:"center",gap:8}}><button onClick={me}><i className="bird">候</i><span><b>候鸟第七年</b><small>当前登录账号</small></span></button><button onClick={switchAccount} style={{height:34,padding:"0 10px",border:"1px solid #d8d3c8",borderRadius:6,background:"#f7f4ee",color:"#6b675f",fontSize:11}}>登录其他账号</button></div></header>
 <nav className="forum-nav"><button onClick={home}><Home/>论坛首页</button><button onClick={me}>我的主页</button></nav>
 <form className="forum-search" onSubmit={e=>{e.preventDefault();search()}}><span><Search/><b>全站搜索</b><small>站内主题与用户</small></span><label><input value={q} onChange={e=>setQ(e.target.value)} placeholder="搜索帖子、用户或关键词"/><button>搜索</button></label></form></>}
'''
s=between(s,'function ForumHeader(','function ForumHome(',new_header,'forum header')
write(p,s)

# ---------------- content/gameDataFlowV2.ts ----------------
p='content/gameDataFlowV2.ts'
s=read(p)
admin_post='''const adminAccountPost:Post={
 id:"27614",title:"旧档员-03到底是一个人还是值班号？",author:"西楼",date:"2024-02-18 01:26",board:"站务区",views:3271,hidden:true,
 excerpt:"旧档整理账号半夜也在移动帖子，说话风格还不太一样。这个号到底几个人在用？",
 terms:["旧档员-03","值班号","旧档账号验证","旧版验证","登录"],highlights:["旧档员-03","多人轮用","旧档账号验证"],
 body:[
  "纯好奇。旧档员-03这个号经常凌晨两三点还在移动旧主题，而且有时候回复特别书面，有时候就一句话。我一直以为是机器人，后来又见它正常回人。",
  "站务以前说过这是值班账号，但我没找到更详细的说明。它到底是一个人、几个人轮用，还是自动任务和真人混着用？"
 ],
 replies:[
  reply("站务-槐序","01:44","多人轮用。旧档恢复也有自动任务，所以操作时间不代表某个具体成员在线。","版主"),
  reply("纸页边角","02:03","我有次点它头像，没进普通个人主页，跳到了一个旧登录页，写着“旧档账号验证”。我还以为网站坏了。"),
  reply("站务-槐序","02:17","早期迁移账号仍保留兼容认证页，属于历史功能。请勿反复尝试登录不属于自己的账号。","版主"),
  reply("西楼","02:31","懂了。那半夜移动也不稀奇，自动任务加值班一起跑。","楼主"),
  reply("旧档员-03","03:08","补一句：公开页面看到的是同一个账号名，不代表后台操作来源相同。")
 ],
 archive:"站务归档：2024-03-02；主题保留，停止回复。"
};

'''
s=once(s,'const patched=flowPosts.map(',admin_post+'const patched=flowPosts.map(','admin account post')
s=once(s,
'export const posts:Post[]=[...patched,posterMemory].sort((a,b)=>toRank(a.date)-toRank(b.date));',
'export const posts:Post[]=[...patched,posterMemory,adminAccountPost].sort((a,b)=>toRank(a.date)-toRank(b.date));',
'include admin post')
write(p,s)

# ---------------- app/InteractiveWechat.tsx ----------------
p='app/InteractiveWechat.tsx'
s=read(p)
s=once(s,
'type ReplyPart={text?:string;material?:SharedMaterial};\ntype MaterialRule=Record<string,ReplyPart[]|null>;',
'type ReplyPart={text?:string;material?:SharedMaterial};\ntype QuickReply={id:string;text:string;reply:ReplyPart[];next?:QuickReply[]};\ntype MaterialRule=Record<string,ReplyPart[]|null>;',
'quick reply type')
s=once(s,
'const scriptureComparePost=forumPost("11208","求辨《三门疏》流传页：黑底红字那张其实不是同一篇吧");',
'const scriptureComparePost=forumPost("11208","求辨《三门疏》流传页：黑底红字那张其实不是同一篇吧");\nconst adminAccountPost=forumPost("27614","旧档员-03到底是一个人还是值班号？");',
'admin forum material')
s=once(s,
'  sent:{} as Record<string,boolean>,\n};',
'  sent:{} as Record<string,boolean>,\n  quick:{} as Record<string,QuickReply[]>,\n};',
'persist quick replies')
s=once(s,
' sanmen:{zc:[],ly:[]},\n};',
' sanmen:{zc:[],ly:[]},\n "31002":{zc:[{text:"这个站务说明我见过。"},{text:"你是觉得旧档员-03有问题？"}],ly:[{text:"这个号我见过。迟迟那边的旧帖也被它动过。"}]},\n "27614":{zc:[{text:"对，就是这篇。"},{text:"当时大家最后都当普通值班号看了。"}],ly:[{text:"我以前没点进去看过。"}]},\n};',
'admin material rules')
quick_fn='''
const quickAfterMaterial=(contactId:string,materialId:string):QuickReply[]=>{
 if(contactId==="zc"&&materialId==="sanmen"){
  const hasPair=received("zc","10731")||(received("zc","09114")&&received("zc","09831"));
  return [{id:"zc-sanmen-body",text:"你觉得“舍”和“客”指什么？",reply:[{text:"硬按字面猜的话，“舍”像住的地方。"},{text:"如果前一句真是“身为舍，魂为客”，那舍就是身体，客就是……住进去的那个东西。"},{text:"我只是按中文意思说，不代表这东西真在讲这个。"}],next:[{id:"zc-sanmen-two",text:"那“二客相契，两门相应”呢？",reply:hasPair?[{text:"两个客，两个门。"},{text:"跟你前面那两个人放一起，我第一反应会是两边一起发生了什么。"},{text:"但我现在也只能到这。"}]:[{text:"两个客、两个门，大概至少不是只说一个人。"},{text:"再往下我没东西能对。"}]}]}];
 }
 if(contactId==="ly"&&materialId==="sanmen")return [{id:"ly-sanmen-memory",text:"“名可夺，忆可乱”这句你怎么看？",reply:[{text:"我不知道它原来想说什么。"},{text:"但“名”这个字让我不舒服。"},{text:"我小时候有一阵，别人喊我名字的时候，我真的会觉得他们叫错人了。"},{text:"现在想起来还是怪。"}]}];
 if(contactId==="zc"&&materialId==="verse")return [{id:"zc-verse-source",text:"所以黑底那张和《三门疏》不是一份？",reply:[{text:"至少那篇旧帖里的人是这么判断的。"},{text:"文件编号和扫描方式都不一样。"},{text:"后来为什么被塞进一个包里，就没人说得清。"}]}];
 if(contactId==="zc"&&materialId==="31002"){
  const hasRelevant=received("zc","09114")||received("zc","09831")||received("zc","10731")||received("zc","verse")||received("zc","sanmen")||received("zc","14692");
  if(hasRelevant)return [{id:"zc-admin-repeat",text:"我查的几篇怪帖子里总能看到它。",reply:[{text:"……那确实有点烦。"},{text:"我记得以前有人专门问过这个号到底是不是一个人。"},{material:adminAccountPost},{text:"应该是这篇。"}]}];
 }
 if(contactId==="zc"&&materialId==="27614")return [{id:"zc-admin-doubt",text:"多人轮用能解释它为什么到处出现吗？",reply:[{text:"能解释一部分。"},{text:"但如果你说的那几篇刚好都是同一类走失和旧抄本，我也会觉得巧得有点过头。"},{text:"我没有后台权限，只能看到公开操作记录。"}]}];
 return [];
};

'''
s=once(s,'const textReply=(contact:string,text:string):ReplyPart[]|null=>{',quick_fn+'const textReply=(contact:string,text:string):ReplyPart[]|null=>{','quick reply logic')
s=once(s,
' const [sent,setSent]=useState<Record<string,boolean>>(()=>({...wechatSession.sent}));',
' const [sent,setSent]=useState<Record<string,boolean>>(()=>({...wechatSession.sent}));\n const [quick,setQuick]=useState<Record<string,QuickReply[]>>(()=>({...wechatSession.quick}));',
'quick state')
old_delayed=''' const delayedParts=(contactId:string,parts:ReplyPart[]|null)=>{
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
'''
new_delayed=''' const setQuickFor=(contactId:string,items:QuickReply[])=>{
  wechatSession.quick={...wechatSession.quick,[contactId]:items};
  notifyWechat();
 };
 const delayedParts=(contactId:string,parts:ReplyPart[]|null,nextQuick:QuickReply[]=[] )=>{
  if(!parts?.length){setQuickFor(contactId,nextQuick);return;}
  let elapsed=1000+Math.floor(Math.random()*900);
  setTyping(prev=>({...prev,[contactId]:true}));
  parts.forEach((part,index)=>{
   const extraDelay=part.text?Math.min(2200,part.text.length*35):700;
   elapsed+=extraDelay+Math.floor(Math.random()*1000);
   window.setTimeout(()=>{
    if(part.material)appendFor(contactId,[{who:"对方",text:`[链接] ${part.material.title}`,material:part.material}]);
    else if(part.text)appendFor(contactId,[{who:"对方",text:part.text}]);
    if(index===parts.length-1){setTyping(prev=>({...prev,[contactId]:false}));setQuickFor(contactId,nextQuick)}
   },elapsed);
  });
 };
'''
s=once(s,old_delayed,new_delayed,'delayed replies with quick followup')
s=once(s,
'   setSent({...wechatSession.sent});\n  };',
'   setSent({...wechatSession.sent});\n   setQuick({...wechatSession.quick});\n  };',
'sync quick')
s=once(s,
'  const intro=ensureIntro(id);\n  appendFor(id,[...intro,{who:"沈妍",text}]);\n  setDraft("");\n  delayedParts(id,textReply(id,text));',
'  const intro=ensureIntro(id);\n  appendFor(id,[...intro,{who:"沈妍",text}]);\n  setQuickFor(id,[]);\n  setDraft("");\n  delayedParts(id,textReply(id,text));',
'clear quick on free text')
s=once(s,
'  setPicker(false);\n  delayedParts(id,reply);\n };\n const openMaterial=',
'  setPicker(false);\n  delayedParts(id,reply,quickAfterMaterial(id,material.id));\n };\n const sendQuick=(item:QuickReply)=>{\n  if(id==="x")return;\n  setQuickFor(id,[]);\n  appendFor(id,[{who:"沈妍",text:item.text}]);\n  delayedParts(id,item.reply,item.next||[]);\n };\n const openMaterial=',
'send quick replies')
quick_ui='''
   {!typing[id]&&(quick[id]||[]).length>0&&<div style={{flex:"0 0 auto",display:"flex",gap:8,flexWrap:"wrap",padding:"9px 14px 0",background:"#f7f7f7"}}>{(quick[id]||[]).map(item=><button key={item.id} onClick={()=>sendQuick(item)} style={{maxWidth:"100%",padding:"7px 11px",border:"1px solid #cfd8d2",borderRadius:15,background:"#fff",color:"#3c6250",fontSize:12,textAlign:"left"}}>{item.text}</button>)}</div>}

'''
s=once(s,'   <footer style={{flex:"0 0 auto",padding:"12px 14px",background:"#f7f7f7",borderTop:"1px solid #ddd"}}>',quick_ui+'   <footer style={{flex:"0 0 auto",padding:"12px 14px",background:"#f7f7f7",borderTop:"1px solid #ddd"}}>','quick UI')
write(p,s)

# simple assertions
page=read('app/page.tsx')
wx=read('app/InteractiveWechat.tsx')
data=read('content/gameDataFlowV2.ts')
for needle in ['AdminPortal','kind:"account"','登录其他账号','persistedForumIdentity']:
    assert needle in page, needle
for needle in ['QuickReply','你觉得“舍”和“客”指什么？','旧档员-03到底是一个人还是值班号？','quickAfterMaterial']:
    assert needle in wx, needle
for needle in ['id:"27614"','旧档账号验证']:
    assert needle in data, needle
print('v8.9.16 patch applied')
