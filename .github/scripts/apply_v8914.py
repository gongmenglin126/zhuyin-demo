from pathlib import Path
import re


def load(path):
    return Path(path).read_text(encoding='utf-8')


def save(path, text):
    Path(path).write_text(text, encoding='utf-8')


def one(s, old, new, label):
    if old not in s:
        raise SystemExit(f'missing pattern: {label}')
    return s.replace(old, new, 1)


def block(s, start, end, replacement, label):
    a=s.find(start)
    if a < 0:
        raise SystemExit(f'missing start: {label}')
    b=s.find(end, a)
    if b < 0:
        raise SystemExit(f'missing end: {label}')
    return s[:a] + replacement + s[b:]

# ---------- app/page.tsx ----------
p='app/page.tsx'; s=load(p)
s=one(s,'import {FormEvent,ReactNode,useEffect,useMemo,useState} from "react";','import {ReactNode,useEffect,useMemo,useState} from "react";','page react import')
s=one(s,'import {ArrowLeft,ChevronRight,Clock3,ExternalLink,Globe2,History as HistoryIcon,Home,LockKeyhole,Maximize2,MessageCircle,Minimize2,NotebookPen,RefreshCw,Search,Wifi,X} from "lucide-react";','import {ArrowLeft,ChevronRight,Clock3,Globe2,History as HistoryIcon,Home,LockKeyhole,Maximize2,MessageCircle,Minimize2,NotebookPen,RefreshCw,Search,Wifi,X} from "lucide-react";','page lucide import')
s=one(s,'import {chats,history,Post,posts,privateEntries,profile} from "../content/gameDataFlowV2";','import {history,Post,posts,privateEntries,profile} from "../content/gameDataFlowV2";','page data import')
s=one(s,'<small>一段发生在朋友电脑里的调查</small>','<small>河临 · 2026年10月17日</small>','title meta')
s=one(s,'<em>现在还没有理由把这件事说成犯罪。你只是想先确认，她昨天离开后原本打算去哪里。</em>','<em>屋里很安静，电脑屏幕还亮着。</em>','intro author voice')
s=one(s,'<small>支持用户名、短语、年份、帖子编号</small>','<small>站内主题与用户</small>','search tutorial')
s=one(s,'>复制帖子链接</button>','>复制链接</button>','copy label')
s=one(s,'<div className="reply"><h3>回复主题</h3><p>该账号近期没有在公开区继续发言。</p></div>','<div className="reply"><h3>回复主题</h3><p>该主题已归档，暂不开放回复。</p></div>','thread footer')
s=one(s,'<section className="panel searches"><h3>账号信息</h3><p style={{padding:"12px",margin:0}}>最近搜索不在主页直接展示。需要从浏览器本地历史里判断她最近查过什么。</p></section>','','profile tutorial')
new_history='''function HistoryPage({open,me,search}:{open:(id:string)=>void;me:()=>void;search:(q:string)=>void}){const natural=[history[0],{title:"河临明日天气",info:"天气 · 多云转小雨"},history[1],{title:"胶片冲洗店 营业时间",info:"本地生活 · 页面已关闭"},{title:"老电影里常见的红铁皮盒是哪家出的",info:"烛阴旧闻 · #30177",id:"30177"},{title:"睡眠门诊 反复梦境",info:"澄川搜索 · 10月12日"},{title:"旧帖合并、原链接与存档编号说明",info:"烛阴旧闻 · #31002",id:"31002"},{title:"旧单位房 厨房门 朝走廊",info:"图片搜索 · 页面已关闭"}];return <main className="history"><header><HistoryIcon/><span><h2>浏览记录</h2><p>沈妍的本地记录</p></span></header><section>{natural.map((x:any,i)=><button key={i} onClick={()=>x.id?open(x.id):x.profile?me():x.query?search(x.query):undefined}><time>{i<4?"昨天":"10月15日"}</time><span><b>{x.title}</b><small>{x.info}</small></span><ChevronRight/></button>)}</section></main>}
'''
s=block(s,'function HistoryPage(','function Results(',new_history,'history page')
if 'function Notes(' in s:
    s=block(s,'function Notes(','function VersePage(','','legacy Notes')
if 'function Wechat(){' in s:
    s=s[:s.index('function Wechat(){')].rstrip()+'\n'
save(p,s)

# ---------- private/password surfaces ----------
p='app/PrivateArea.tsx'; s=load(p)
s=one(s,'<label style={s.label}>访问口令 <span style={s.labelHint}>2 个汉字</span></label>','<label style={s.label}>访问口令</label>','private length hint')
s=one(s,'aria-label="两个字访问口令"','aria-label="访问口令"','private aria')
save(p,s)

p='app/LocalVault.tsx'; s=load(p)
s=one(s,'<p style={styles.copy}>一条被单独锁起来的本地记录。</p>','<p style={styles.copy}>已保存的离线页面。</p>','vault copy')
s=one(s,'<span><b>口令提示</b>　打开前会卡一下</span>\n        <small>4 个汉字</small>','<span><b>口令提示</b>　打开前会卡一下</span>','vault length')
s=one(s,'aria-label="四个字访问口令"','aria-label="访问口令"','vault aria')
s=one(s,'placeholder="输入 4 个汉字"','placeholder="输入口令"','vault placeholder')
save(p,s)

p='app/DeepArchiveGate.tsx'; s=load(p)
s=one(s,'<small style={{color:"#837a71"}}>这份附件只出现在沈妍的私密记录里</small>','<small style={{color:"#837a71"}}>加密压缩包 · 本地文件</small>','archive meta')
save(p,s)

# ---------- WeChat ----------
p='app/InteractiveWechat.tsx'; s=load(p)
contacts='''const contacts:Contact[]=[
 {id:"x",name:"徐宁",note:"小学同学",preview:"我去你家看看",messages:[
  {time:"10月16日 11:26",who:"对方",text:"明天中午还是老地方？"},{who:"沈妍",text:"嗯，靠窗"},{who:"对方",text:"你别又临时说有事"},{who:"沈妍",text:"这次真不会"},{who:"对方",text:"我截图了"},{who:"沈妍",text:"随便截"},{time:"10月16日 19:48",who:"沈妍",text:"我晚上出去一趟"},{who:"沈妍",text:"明天要是我迟到你先点"},{who:"对方",text:"？？？你刚保证完"},{who:"沈妍",text:"我说要是"},{who:"对方",text:"行，十二点"},{time:"今天 12:02",who:"对方",text:"我到了"},{who:"对方",text:"你人呢"},{time:"今天 12:37",who:"对方",text:"电话也不接，看到回我"},{time:"今天 18:37",who:"对方",text:"我去你家看看"},
 ]},
 {id:"yq",name:"余晴",note:"余晴｜朋友介绍",preview:"到家说一声",messages:[
  {time:"10月16日 18:52",who:"对方",text:"我先到了"},{who:"沈妍",text:"这么早"},{who:"对方",text:"你不是说七点"},{who:"沈妍",text:"路上，十分钟"},{who:"对方",text:"还是里面那桌"},{who:"沈妍",text:"好"},{time:"10月16日 19:17",who:"对方",text:"看见你了"},{who:"沈妍",text:"别起来，我过去"},{time:"10月16日 20:46",who:"对方",text:"你真不吃了？"},{who:"沈妍",text:"胃不太舒服"},{who:"对方",text:"那我给你打包？"},{who:"沈妍",text:"不用"},{time:"10月16日 21:03",who:"对方",text:"到家说一声"},{who:"沈妍",text:"嗯"},
 ]},
 {id:"zc",name:"周川",note:"周川｜烛阴旧闻",preview:"我回了一条",messages:[
  {time:"10月12日 22:08",who:"对方",text:"你那个梦帖我看到了"},{who:"沈妍",text:"你怎么什么都刷得到"},{who:"对方",text:"首页挂着呢"},{who:"沈妍",text:"丢人"},{who:"对方",text:"还行，比你上次凌晨三点那篇短"},{who:"沈妍",text:"……"},{who:"对方",text:"那两个字还是听不清？"},{who:"沈妍",text:"现在觉得像楠楠"},{who:"对方",text:"你上周不是还说可能是囡囡"},{who:"沈妍",text:"所以才烦"},{who:"对方",text:"今天别想了，越想越像真的"},{who:"沈妍",text:"你怎么跟我妈一个口气"},{who:"对方",text:"你妈说得对"},{time:"10月13日 00:17",who:"对方",text:"我回了一条"},{who:"沈妍",text:"看见了"},{who:"沈妍",text:"你每次回帖都像在改报告"},{who:"对方",text:"那我删"},{who:"沈妍",text:"别，留着吧"},{who:"对方",text:"睡觉"},{who:"沈妍",text:"你先"},
 ]},
 {id:"ly",name:"梁茵",note:"梁茵｜烛阴旧闻",preview:"我把迟迟那个号退了",messages:[
  {time:"9月28日 00:42",who:"对方",text:"我把迟迟那个号退了"},{who:"沈妍",text:"又有人私信你？"},{who:"对方",text:"嗯"},{who:"对方",text:"这次问得特别细"},{who:"沈妍",text:"问什么"},{who:"对方",text:"问我小时候回来以后还认不认家"},{who:"沈妍",text:"还是新号？"},{who:"对方",text:"对"},{who:"沈妍",text:"截图留了吗"},{who:"对方",text:"留了"},{who:"沈妍",text:"那别回"},{who:"对方",text:"我本来也不想回"},{who:"对方",text:"早知道不发那个帖"},{who:"沈妍",text:"你不发我俩也不会认识"},{who:"对方",text:"那倒也是"},{time:"9月28日 01:03",who:"对方",text:"你还没睡？"},{who:"沈妍",text:"你不也没"},{who:"对方",text:"我洗澡去了"},{who:"沈妍",text:"去吧"},
 ]},
 {id:"f",name:"方嘉",note:"方嘉｜公司",preview:"周一的表我先帮你交？",messages:[
  {time:"昨天 16:22",who:"对方",text:"甲方又改表头了"},{who:"沈妍",text:"哪一版"},{who:"对方",text:"我发群里了"},{who:"沈妍",text:"你先别动，我明早统一"},{who:"对方",text:"好"},{who:"对方",text:"你今天是不是又没吃晚饭"},{who:"沈妍",text:"吃了"},{who:"对方",text:"你这个句号很可疑"},{time:"今天 09:14",who:"对方",text:"你今天来不来？"},{time:"今天 14:05",who:"对方",text:"周一的表我先帮你交？"},
 ]},
 {id:"p",name:"爸妈",note:"爸妈",preview:"别又熬太晚",messages:[
  {time:"10月15日 18:44",who:"对方",text:"周末回来吃饭吗"},{who:"沈妍",text:"看情况"},{who:"对方",text:"你爸买排骨了"},{who:"沈妍",text:"那更得看情况"},{who:"对方",text:"少贫"},{who:"沈妍",text:"哈哈哈哈"},{time:"10月16日 08:15",who:"对方",text:"这两天降温，晚上出门加件外套"},{who:"沈妍",text:"知道了"},{who:"对方",text:"别又熬太晚"},
 ]},
];

'''
s=block(s,'const contacts:Contact[]=[','const materialRules:',contacts,'wechat contacts')
replies='''const materialRules:Record<string,MaterialRule>={
 "33897":{yq:[{text:"这是哪儿？"},{text:"没去过。昨晚她也没跟我说这个。"}],zc:[{text:"这个我看过。"},{text:"她当时还在下面问那扇门怎么开的。"},{text:"照片跟她画的确实有点像。"}]},
 "09114":{yq:[{text:"林楠？"},{text:"没听她提过。"}],zc:[],ly:[{text:"林楠？"},{text:"不认识。"},{text:"沈妍怎么会查到她的？"}]},
 "09831":{zc:[],ly:[{text:"这是沈妍？"},{text:"她没跟我说过小时候这件事。"}]},
 "10731":{zc:[],ly:[{text:"这篇我看过。"},{text:"两条都十三天那段我有印象。"}]},
 "14692":{zc:[{text:"这帖我记得。"},{text:"楼主后来没怎么更新。"}],ly:[{text:"这篇我看过。"},{text:"他说别人叫名字时会慢半拍，那段我记得。"}]},
 "17428":{zc:[{text:"这个我也回过。"},{text:"就香菜，别的没啥。"}],ly:[{text:"这个跟我不太像。"}]},
 "private-p1":{yq:[{text:"她是说过最近总梦见同一间屋。"},{text:"盒子这些细节没跟我讲过。"}],zc:[{text:"这是她自己存的？"},{text:"这版她没给我看过。"},{text:"原来她后来一直觉得是“楠楠”。"}]},
 "private-p3":{yq:null,zc:[{text:"她把这些都存一起了？"},{text:"里面那个“突然不吃某种味道”我有印象。"},{text:"有篇旧帖就这样。"},{material:ordinaryChangePost},{text:"好像就是这个。"}],ly:[{text:"“另一个家”这几个字我见过。"},{text:"有个旧帖里也这么写。"},{material:returnedPost},{text:"我以前看过，不一定是一回事。"}]},
 verse:{zc:[{text:"这张黑底的我眼熟。"},{text:"以前有个帖子专门吵它跟白纸抄本是不是一套。"},{material:scriptureComparePost}],ly:[{text:"看不懂。"},{text:"这也是她电脑里的？"}]},
 sanmen:{zc:[],ly:[]},
};

const received=(contactId:string,materialId:string)=>!!wechatSession.sent[`${contactId}:${materialId}`];
const materialReply=(contactId:string,materialId:string):ReplyPart[]|null=>{
 if(contactId==="zc"&&materialId==="09114"){
  if(received("zc","09831"))return [{text:"等等。"},{text:"这条也是九岁？"},{text:"也是十三天。"},{text:"日期还挨着……这也太巧了。"}];
  return [{text:"林楠？"},{text:"这个名字她没跟我说过。"},{text:"九岁，失踪十三天。挺久的。"}];
 }
 if(contactId==="zc"&&materialId==="09831"){
  if(received("zc","09114"))return [{text:"这是沈妍？"},{text:"等会儿，林楠那条也是九岁。"},{text:"都是十三天？"},{text:"这也太巧了。"}];
  return [{text:"这是沈妍小时候？"},{text:"她从来没提过。"}];
 }
 if(contactId==="zc"&&materialId==="10731"){
  if(received("zc","09114")&&received("zc","09831"))return [{text:"哦。"},{text:"原来你前面发的就是这两条。"},{text:"我以前回过这帖，当时只觉得目录撞得离谱。"}];
  return [{text:"我记得这帖。"},{text:"以前看过，当时只觉得两条记录撞得巧。"}];
 }
 if(contactId==="zc"&&materialId==="sanmen"){
  const hasPair=received("zc","10731")||(received("zc","09114")&&received("zc","09831"));
  if(hasPair)return [{text:"……这几句跟你前面那两条放一起，确实会让人乱想。"},{text:"“二客”我第一眼也会当成两个人。"},{text:"但这东西连来源都没有，我不敢顺着往下说。"}];
  return [{text:"这什么意思。"},{text:"我真看不懂。"}];
 }
 if(contactId==="ly"&&materialId==="sanmen"){
  const hasAnomaly=received("ly","private-p3")||received("ly","14692")||received("ly","09831");
  if(hasAnomaly)return [{text:"我看不懂。"},{text:"但“名可夺，忆可乱”这句看着很不舒服。"},{text:"跟我小时候那些事放一起更不舒服。"}];
  return [{text:"看不懂。"},{text:"你从哪找到的？"}];
 }
 return materialRules[materialId]?.[contactId]??null;
};

const textReply=(contact:string,text:string):ReplyPart[]|null=>{
 const t=text.replace(/\s/g,"");
 if(contact==="yq"){
  if(/昨晚|见面|去哪|在哪/.test(t))return [{text:"昨晚是见到了。"},{text:"后来她说胃不舒服，我就先走了。"},{text:"她没跟我说后面去哪。"}];
  if(/林楠/.test(t))return [{text:"真没听过这个名字。"}];
 }
 if(contact==="zc"){
  if(/林楠/.test(t))return [{text:"她没跟我说过这个名字。"},{text:"你从哪翻到的？"}];
  if(/失踪|不见了|联系不上/.test(t))return [{text:"她现在还是完全联系不上？"},{text:"电话也不通？"}];
  if(/换魂|灵魂|交换/.test(t))return [{text:"你是说真的把两个人换了？"},{text:"我不知道。光这些我不敢这么说。"}];
  if(/名字不对|另一个家|回来以后不会/.test(t))return [{text:"我见过这种说法，不止一篇。"},{text:"具体哪篇我得翻一下。"}];
 }
 if(contact==="ly"){
  if(/林楠/.test(t))return [{text:"林楠？"},{text:"我不认识。"}];
  if(/名字|另一个家|不会/.test(t))return [{text:"嗯。"},{text:"我小时候也说过类似的话。"},{text:"这事打字说有点怪。"}];
  if(/换魂|灵魂|交换/.test(t))return [{text:"你是说……两个人真的互换？"},{text:"我不知道。我以前没敢往这上面想。"}];
 }
 if(contact==="f"&&/沈妍|联系不上|没来/.test(t))return [{text:"她今天也没回我。"},{text:"怎么了？"}];
 if(contact==="p"&&/沈妍|联系不上|没回/.test(t))return [{text:"她没跟我们说今天去哪。"},{text:"电话也打不通吗？"}];
 return null;
};

'''
s=block(s,'const materialRules:Record<string,MaterialRule>={','const introText=',replies,'wechat replies')
intro='''const introText=(contactId:string)=>{
 if(contactId==="yq")return "你好，我是徐宁，沈妍朋友。她今天一直联系不上，我现在在她家。你们昨晚是不是见过？她走的时候有说去哪吗？";
 if(contactId==="zc")return "你好，我是徐宁，沈妍朋友。她今天一直联系不上。我现在在她家，她电脑微信还登着。看到你们最近有聊天，方便问你两句吗？";
 if(contactId==="ly")return "你好，我是徐宁，沈妍朋友。她今天一直联系不上。我现在在她家，她电脑微信还登着。看到你们最近有聊天，方便问你两句吗？";
 if(contactId==="f")return "你好，我是徐宁，沈妍朋友。她今天没来，也联系不上。我现在在她家，她电脑微信还登着。你今天见过她吗？";
 if(contactId==="p")return "叔叔阿姨，我是徐宁。沈妍今天一直联系不上，我现在在她家。你们今天跟她联系过吗？";
 return "你好，我是徐宁，沈妍朋友。她今天一直联系不上，我现在在她家。";
};

'''
s=block(s,'const introText=','export default function',intro,'wechat intros')
save(p,s)

# ---------- content/gameDataFlowV2.ts ----------
p='content/gameDataFlowV2.ts'; s=load(p)
dream='''const dreamBase=flowPosts.find(post=>post.id==="20847")!;
const dreamPost:Post={
 ...dreamBase,
 terms:(dreamBase.terms||[]).map(term=>term==="红色糖盒"?"红铁皮盒":term),
 highlights:(dreamBase.highlights||[]).map(mark=>mark==="红色铁皮糖盒"?"红铁皮盒":mark),
 body:dreamBase.body.map((text,index)=>index===2?text.replace("红色铁皮糖盒","红铁皮盒"):text),
 replies:[
  reply("困得要命","02:03","我会反复梦见高中宿舍，但布局每次都变。你这个连门怎么开都固定，确实挺折磨人。"),
  reply("白粥配蛋","08:36","我奶奶家也有红铁皮盒，里面永远不是糖，是针线。你说话梅我第一反应还挺亲切。"),
  reply("一格胶片","09:12","这种老单位房我拍过不少，门窗长得都挺像。只看你这张图，我认不出地方。"),
  reply("候鸟第七年","09:25","我也是卡在这儿。细节很多，但没有一个能直接指到哪。","楼主"),
  reply("山雀","10:18","右边窗帘褪色倒是很生活，真住过的人才会嫌这种小事烦。也可能只是梦给自己补得太完整。"),
  reply("夜航船","19:18","有没有可能是某部电视剧的室内景？九十年代家庭剧布景都长得差不多。"),
  reply("折柳","次日 00:12","看完了。你这次记得比上次细很多。今天别再翻了，明天再看，越熬越容易把自己绕进去。"),
  reply("候鸟第七年","次日 00:31","你怎么跟我妈一个口气。睡了。","楼主"),
  reply("版务-青砖","06-20 19:22","已处理两条付费解梦广告。","版主"),
 ],
};

'''
s=block(s,'const dreamBase=','const redBoxBase=',dream,'dream')
cotton='''const cottonBase=flowPosts.find(post=>post.id==="33897")!;
const cottonYard:Post={
 ...cottonBase,author:"一格胶片",date:"2026-07-09 22:14",excerpt:"岚棉三厂旧家属区的一组窗户和走廊照片。评论里有老住户补充旧房型。",terms:["岚棉三厂","旧址","家属区","4栋","窗户","走廊","寻人启事"],highlights:["岚棉三厂","4栋","寻人启事"],
 body:["上周路过岚棉三厂旧家属区，拍了几张还没封死的外墙和窗户。主要想留老单位房改造前后的样子，不做灵异讨论。","第二组是4栋东侧。能看见走廊窗和厨房外墙，部分门窗应该后来换过。第二张窗边还压着一个红色盒子，看着像旧住户留下的杂物。","如果有以前住过这里的人，欢迎补充哪几年改过窗、厨房门和公共走廊。"],
 replies:[reply("胶卷过期","22:37","第二张右下角那个红色铁皮盒挺显眼，是你摆的吗？"),reply("一格胶片","22:49","不是，隔着窗拍到的。我拍的是窗和房型，没进去动东西。","楼主"),reply("三厂老住户","07-10 09:18","4栋我小时候住过。你第二张应该就是东侧那排，厨房门确实往走廊开。"),reply("候鸟第七年","07-10 09:42","请问这种门和窗大概是哪几年改的？我最近在核一个老房型。"),reply("三厂老住户","07-10 10:03","具体年份记不清了。只记得04年暑假这边贴过一阵寻人启事，我妈还帮着贴过。后来听说孩子找回来了。"),reply("候鸟第七年","07-10 10:16","是4栋这边的孩子吗？"),reply("三厂老住户","07-10 10:31","哪栋我真记不清了，隔太久。反正就是这片家属区。")],
};

'''
s=block(s,'const cottonBase=','const posterMemory:',cotton,'cotton')
poster='''const posterMemory:Post={id:"18362",title:"有人还记得小时候三厂家属区楼下贴过的那张寻人启事吗",author:"旧电扇",date:"2013-09-07 20:18",board:"旧闻考据",views:1638,hidden:true,excerpt:"老住户回忆小时候楼下贴过很久的一张寻人启事，只想确认是不是自己记错了年份。",terms:["寻人启事","三厂家属区","旧报","04年","暑假"],highlights:["寻人启事","04 年暑假","报刊索引"],body:["小时候住三厂家属区，印象里有一年暑假楼道口和小卖部门口贴了很久一张寻人启事。后来好像听大人说孩子找回来了。","最近和家里聊旧厂的事又想起来，但我已经分不清是03年还是04年，也记不得孩子叫什么。有没有老住户记得？","不是要找当事人，就是想确认这段记忆到底有没有发生过。"],replies:[reply("旧纸鸢","20:41","我也记得，应该更接近04年暑假。名字我完全没印象。"),reply("报刊索引","21:06","我那几年整理过岚州地方报的儿童寻人版，印象里录过这一条。太久了，标题我也记不住。"),reply("旧电扇","21:33","行，我自己翻翻。谢谢。","楼主")]};

'''
s=block(s,'const posterMemory:','const scriptureComparePost:',poster,'poster')
# Keep one provenance-oriented 11208 by replacing the base version in the patch map, not appending a duplicate.
reports='''const reportBase=flowPosts.find(post=>post.id==="09114")!;
const linNanReport:Post={...reportBase,author:"报刊索引",title:"【旧报摘录】九岁女童失踪十三日后异地找回",excerpt:"2004 年岚州地方报纸索引。姓名、年龄、失踪和找回日期完整。",terms:["2004","九岁","女童","姓林","林楠","十三天","失踪","找回","7月18日","7月31日"],highlights:["2004-07-18","九岁女童林楠","十三天后","2004-07-31","无法完整说明失踪期间经历"],body:["岚州地方文献室索引：2004-07-18，九岁女童林楠在东浦区一处老厂职工宿舍附近失踪，家属当日报警，并在次日地方报刊登寻人信息。","2004-07-31 的后续简讯记载，林楠在外市旧客运站附近被找到，距离失踪十三天。","简讯只写到身体无明显外伤、意识清醒，但无法完整说明失踪期间经历。原报没有刊登后续采访。","本条为旧报索引摘录；旧索引没有录入宿舍所属厂名。"],replies:[reply("旧纸鸢","16:28","我家里那份剪报记的也是31号找回，跟你这条一致。"),reply("报刊索引","16:41","谢谢，我补到正文里。原扫描实在太糊了。","楼主"),reply("旧档员-03","2023-09-02","本帖从旧索引分类恢复。","版主")]};
const shenYanBase=flowPosts.find(post=>post.id==="09831")!;
const shenYanReport:Post={...shenYanBase,replies:[reply("旧纸鸢","14:28","这条我有印象，南站那张简讯糊得厉害。"),reply("报刊索引","14:46","是，能确认的主要是日期、姓名和地点。","楼主"),reply("候鸟第七年","2026-08-21","请问图书馆现在还能调 7 月 17 日和 7 月 30 日前后的整卷吗？"),reply("报刊索引","2026-08-22","账号很久没用了。你可以直接问河临地方文献室。","楼主"),reply("旧档员-03","2023-09-02","本帖从失效分类恢复。","版主")]};

'''
s=block(s,'const reportBase=','// 首页上的普通旧报',reports,'reports')
returned='''const returnedBase=flowPosts.find(post=>post.id==="14692")!;
const returnedCase:Post={...returnedBase,terms:(returnedBase.terms||[]).filter(term=>term!=="寻人启事"),highlights:(returnedBase.highlights||[]).filter(mark=>mark!=="寻人启事"),replies:[reply("睡前一杯水","23:41","如果现在还会因为这些事难受，继续做咨询比在论坛找答案靠谱。"),reply("雨棚下","00:09","我四岁搬家后把旧家和幼儿园混在一起很多年。小孩的记忆真能串。"),reply("山羊胡","01:03","派出所也许还留过接警记录，不过年代这么久不一定查得到。"),reply("南门摆摊","11:32","有没有可能那几天有人临时照顾你？住过几天的地方后来被记成另一个家。"),reply("蓝色票根","04-12","我小时候一直说家门颜色不对，后来才知道那年真的重新刷过。"),reply("折柳","04-13","我第一反应还是走失以后记忆乱了。不过你写的这些细节确实挺具体。"),reply("照骨","2020-01-13 00:18","回来以后除了名字和另一个家，还有没有突然怕以前不怕的东西，或者以前会做、后来突然不会的事？没有也可以写没有。"),reply("夜班公交","00:31","@照骨 你怎么又问这一套，我好像在别的走失帖也见过。"),reply("照骨","00:44","类似帖子我都会问，省得每次漏掉东西。"),reply("版务-青砖","00:57","旧帖请勿频繁顶起。","版主")]};

'''
s=block(s,'const returnedBase=','const julyBase=',returned,'returned')
july='''const julyBase=flowPosts.find(post=>post.id==="10731")!;
const julyArchive:Post={...julyBase,title:"2004 年 7 月两地地方报转载来源求考",replies:[reply("报刊索引","21:48","我核过目录号，不是重复转载。两条都有各自的首发版面。"),reply("纸页边角","22:03","差一天、同岁、都两周左右，难怪目录里看着像一条。"),reply("南站旧报摊","22:51","两地四百多公里，联系人也不一样，应该就是两起碰巧挨得很近。"),reply("折柳","23:02","这帖我当年看过。印象最深的就是两个“十三天”挨在一起。"),reply("地方志小王","23:07","对，我当时就是怕目录合并错了才发帖。","楼主")]};

'''
s=block(s,'const julyBase=','const traumaBase=',july,'july')
trauma='''const traumaBase=flowPosts.find(post=>post.id==="17428")!;
const traumaCase:Post={...traumaBase,replies:[reply("营养科路过","18:52","会有这种可能，也可能只是儿童期口味刚好在那段时间改变。单凭时间前后真说不准。"),reply("雨衣口袋","19:02","我家里也是拿“走失回来以后变了”讲了二十多年，所以我自己也不知道是不是硬连在一起了。","楼主"),reply("折柳","19:14","你这篇我反而觉得挺普通的。除了香菜，别的生活都没变，对吧？"),reply("雨衣口袋","19:22","对，其他都正常。","楼主"),reply("照骨","19:41","那名字、家里房间、以前会做的事这些，有没有哪样突然觉得不对？"),reply("雨衣口袋","19:53","都没有。就是香菜。","楼主"),reply("纸页边角","20:07","照骨你是不是在别的走失帖也问过这几个问题？看着好眼熟。"),reply("照骨","20:16","问过，类似帖子我一般都这么问。")]};

'''
s=block(s,'const traumaBase=','const patched=',trauma,'trauma')
patched='''const patched=flowPosts.map(post=>post.id==="33897"?cottonYard:post.id==="09114"?linNanReport:post.id==="09831"?shenYanReport:post.id==="20847"?dreamPost:post.id==="30177"?redBoxPost:post.id==="34049"?wallPost:post.id==="14692"?returnedCase:post.id==="10731"?julyArchive:post.id==="17428"?traumaCase:post.id==="11208"?scriptureComparePost:post);

'''
s=block(s,'const patched=','const toRank=',patched,'patch map')
s=one(s,'export const posts:Post[]=[...patched,posterMemory,scriptureComparePost].sort((a,b)=>toRank(a.date)-toRank(b.date));','export const posts:Post[]=[...patched,posterMemory].sort((a,b)=>toRank(a.date)-toRank(b.date));','dedupe 11208')
save(p,s)

# ---------- content/gameDataFlow.ts safe history ----------
p='content/gameDataFlow.ts'; s=load(p)
s=s.replace('  history as baseHistory,\n','',1)
a=s.find('export const history=[')
if a<0: raise SystemExit('missing flow history')
s=s[:a]+'''export const history=[
 {title:"最近总梦见一间没住过的房子",info:"烛阴旧闻 · #20847",id:"20847"},
 {title:"候鸟第七年 - 用户主页",info:"烛阴旧闻 · 个人中心",profile:true},
 {title:"河临天气 - 未来七天",info:"澄川搜索 · 昨天 18:51"},
 {title:"胶片扫描店 营业时间",info:"澄川搜索 · 10月15日"},
 {title:"老电影里常见的红铁皮盒是哪家出的",info:"烛阴旧闻 · #30177",id:"30177"},
 {title:"旧帖合并、原链接与存档编号说明",info:"烛阴旧闻 · #31002",id:"31002"},
 {title:"睡眠门诊 反复梦境",info:"澄川搜索 · 10月12日"},
];
'''
save(p,s)

# Basic regression assertions
page=load('app/page.tsx')
wx=load('app/InteractiveWechat.tsx')
v2=load('content/gameDataFlowV2.ts')
for bad in ['function Notes(','0407','两个版号','需要从浏览器本地历史里判断','现在还没有理由把这件事说成犯罪','function Wechat(){']:
    if bad in page: raise SystemExit(f'page still contains: {bad}')
for bad in ['先画结构','不要急着给梦里的人起名字','音节先原样记','不用先猜名字']:
    if bad in v2: raise SystemExit(f'v2 still contains tutorial phrase: {bad}')
if v2.count('id:"11208"') != 1: raise SystemExit(f'expected one explicit 11208 object, got {v2.count("id:\"11208\"")}')
if '"private-p1":{yq:' not in wx or '"private-p1":{yq:' in wx and 'ly:' in wx[wx.index('"private-p1"'):wx.index('"private-p3"')]:
    raise SystemExit('private-p1 unexpectedly sendable to Liang Yin')
print('v8.9.14 patch assertions passed')
