"use client";
// v9.2.1 interaction pass
// v9.2.1b reasoning recovery
// v9.2.2 controlled WeChat
// v9.2.2b WeChat hard lock
// v9.2.3 identity clarity + hostile Zhou

import {FormEvent,useEffect,useMemo,useRef,useState} from "react";
import {advanceGameClock} from "./gameClock";
import {beginEnding} from "./endingState";
import {Plus,Search,Send,X} from "lucide-react";

export type SharedMaterial={id:string;title:string;kind:string;url:string};
export type WechatNotice={contactId:string;name:string;text:string};
type Msg={time?:string;who:"沈妍"|"对方";text:string;material?:SharedMaterial};
type Contact={id:string;name:string;note:string;preview:string;signature?:string;messages:Msg[]};
type ReplyPart={text?:string;material?:SharedMaterial};
type QuickReply={id:string;text:string;sendText?:string;emphasis?:boolean;freeText?:boolean;ending?:"report"|"double";reply:ReplyPart[];next?:QuickReply[]};
type MaterialRule=Record<string,ReplyPart[]|null>;

const forumPost=(id:string,title:string):SharedMaterial=>({id,title,kind:"论坛帖子",url:`https://www.zhuyinwen.cn/thread/${id}`});
const returnedPost=forumPost("14692","有没有人记得“被找回来”之前的家");
const ordinaryChangePost=forumPost("17428","小时候走失以后突然不吃香菜，这种变化会持续很多年吗");
const scriptureComparePost=forumPost("11208","求辨《三门疏》流传页：黑底红字那张其实不是同一篇吧");
const adminAccountPost=forumPost("27614","旧档员-03到底是一个人还是值班号？");

// Desktop apps are unmounted when switching windows. Keep the current WeChat session
// at module scope so messages and one-shot material sends survive app switches.
const wechatSession={
  extra:{} as Record<string,Msg[]>,
  introduced:{} as Record<string,boolean>,
  sent:{} as Record<string,boolean>,
  quick:{} as Record<string,QuickReply[]>,
  adminBeats:{} as Record<string,boolean>,
  firstContact:{} as Record<string,string>,
  locked:{} as Record<string,boolean>,
  freeText:{} as Record<string,boolean>,
  freeReturn:{} as Record<string,QuickReply[]>,
  zhouEvidenceSeen:false,
  zhouIdentityKnown:false,
  zhouConfronted:false,
  locationKnown:false,
  locationThreatSent:false,
  activeId:"yq",
  searchQuery:"",
  draft:"",
};
const wechatSubscribers=new Set<()=>void>();
const notifyWechat=()=>wechatSubscribers.forEach(fn=>fn());

const contacts:Contact[]=[
 {id:"x",name:"徐宁",note:"小学同学",preview:"我去你家看看",messages:[
  {time:"10月16日 11:26",who:"对方",text:"明天中午还是老地方？"},{who:"沈妍",text:"嗯，靠窗"},{who:"对方",text:"你别又临时说有事"},{who:"沈妍",text:"这次真不会"},{who:"对方",text:"我截图了"},{who:"沈妍",text:"随便截"},{time:"10月16日 19:48",who:"沈妍",text:"我晚上出去一趟"},{who:"沈妍",text:"明天要是我迟到你先点"},{who:"对方",text:"？？？你刚保证完"},{who:"沈妍",text:"我说要是"},{who:"对方",text:"行，十二点"},{time:"今天 12:02",who:"对方",text:"我到了"},{who:"对方",text:"你人呢"},{time:"今天 12:37",who:"对方",text:"电话也不接，看到回我"},{time:"今天 18:37",who:"对方",text:"我去你家看看"},
 ]},
 {id:"yq",name:"余晴",note:"余晴｜朋友介绍",preview:"到家说一声",messages:[
  {time:"10月16日 18:52",who:"对方",text:"我先到了"},{who:"沈妍",text:"这么早"},{who:"对方",text:"你不是说七点"},{who:"沈妍",text:"路上，十分钟"},{who:"对方",text:"还是里面那桌"},{who:"沈妍",text:"好"},{time:"10月16日 19:17",who:"对方",text:"看见你了"},{who:"沈妍",text:"别起来，我过去"},{time:"10月16日 20:46",who:"对方",text:"你真不吃了？"},{who:"沈妍",text:"胃不太舒服"},{who:"对方",text:"那我给你打包？"},{who:"沈妍",text:"不用"},{time:"10月16日 21:03",who:"对方",text:"到家说一声"},{who:"沈妍",text:"嗯"},
 ]},
 {id:"zc",name:"周川",note:"周川｜烛阴旧闻",preview:"我回了一条",messages:[
  {time:"10月12日 22:08",who:"对方",text:"你那个梦帖我看到了"},{who:"沈妍",text:"你怎么什么都刷得到"},{who:"对方",text:"首页挂着呢"},{who:"沈妍",text:"丢人"},{who:"对方",text:"还行，比你上次凌晨三点那篇短"},{who:"沈妍",text:"……"},{who:"对方",text:"那声称呼还是听不清？"},{who:"沈妍",text:"现在觉得像楠楠"},{who:"对方",text:"你上周不是还说可能是囡囡"},{who:"沈妍",text:"所以才烦"},{who:"对方",text:"今天别想了，越想越像真的"},{who:"沈妍",text:"你怎么跟我妈一个口气"},{who:"对方",text:"你妈说得对"},{time:"10月13日 00:17",who:"对方",text:"我回了一条"},{who:"沈妍",text:"看见了"},{who:"沈妍",text:"你每次回帖都像在改报告"},{who:"对方",text:"那我删"},{who:"沈妍",text:"别，留着吧"},{who:"对方",text:"睡觉"},{who:"沈妍",text:"你先"},
 ]},
 {id:"ly",name:"梁茵",note:"梁茵｜烛阴旧闻",preview:"我把迟迟那个号退了",messages:[
  {time:"9月28日 00:42",who:"对方",text:"我把迟迟那个号退了"},{who:"沈妍",text:"又有人私信你？"},{who:"对方",text:"嗯"},{who:"对方",text:"这次问得特别细"},{who:"沈妍",text:"问什么"},{who:"对方",text:"问我小时候回来以后还认不认家"},{who:"沈妍",text:"还是新号？"},{who:"对方",text:"对"},{who:"沈妍",text:"截图留了吗"},{who:"对方",text:"留了"},{who:"沈妍",text:"那别回"},{who:"对方",text:"我本来也不想回"},{who:"对方",text:"早知道不发那个帖"},{who:"沈妍",text:"你不发我俩也不会认识"},{who:"对方",text:"那倒也是"},{time:"9月28日 01:03",who:"对方",text:"你还没睡？"},{who:"沈妍",text:"你不也没"},{who:"对方",text:"我洗澡去了"},{who:"沈妍",text:"去吧"},
 ]},
];

const wechatNoticeSubscribers=new Set<(notice:WechatNotice)=>void>();
export const subscribeWechatNotices=(fn:(notice:WechatNotice)=>void)=>{wechatNoticeSubscribers.add(fn);return ()=>{wechatNoticeSubscribers.delete(fn)}};
const emitWechatNotice=(contactId:string,text:string)=>{const c=contacts.find(x=>x.id===contactId);if(c)wechatNoticeSubscribers.forEach(fn=>fn({contactId,name:c.name,text}))};
export const focusWechatContact=(contactId:string)=>{if(contacts.some(x=>x.id===contactId))wechatSession.activeId=contactId};
export const getFirstContactTime=(contactId:string)=>wechatSession.firstContact[contactId]||null;
export const revealZhouConfrontation=()=>{
 const stamp=wechatSession.firstContact.zc;
 if(!wechatSession.zhouIdentityKnown||!stamp||wechatSession.zhouConfronted)return false;
 wechatSession.zhouEvidenceSeen=true;
 wechatSession.freeText={...wechatSession.freeText,zc:false};
 wechatSession.freeReturn={...wechatSession.freeReturn,zc:[]};
 const how:QuickReply={id:"zc-zheliu-how",text:"你怎么知道我给她发了？",reply:[{text:"……"},{text:"徐宁，你听我一次。"},{text:"离开沈妍家。别报警。"}]};
 const log:QuickReply={id:"zc-zheliu-log",text:`我${stamp}才告诉你我是徐宁，同一分钟后台就有折柳补录。`,reply:[{text:"关掉。"},{text:"我说关掉。"},{text:"不要再给梁茵发任何东西。"}],next:[how]};
 const real:QuickReply={id:"zc-zheliu-real",text:"论坛实名资料写的是周川。后台来源写的是折柳。",reply:[{text:"……"},{text:"把后台关掉。"},{text:"现在。"}],next:[log]};
 const first:QuickReply={id:"zc-zheliu",text:"你是折柳？",emphasis:true,reply:[{text:"你为什么搜这个号。"}],next:[real]};
 wechatSession.quick={...wechatSession.quick,zc:[first]};
 notifyWechat();
 return true;
};
export const discoverZhouIdentity=()=>{wechatSession.zhouIdentityKnown=true;notifyWechat();return revealZhouConfrontation()};

const materialRules:Record<string,MaterialRule>={
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
 "23109":{zc:[{text:"……这张图挺邪的。"},{text:"你从哪翻出来的？"}],ly:[{text:"这个黄纸我小时候见过差不多的。"},{text:"贴在门框边上。我一直以为就是家里辟邪。"}]},
 "27614":{zc:[{text:"这篇我有印象。"},{text:"站务后来不是说多人轮用吗。"}],ly:[{text:"我以前没点进去看过。"}]},
 "admin-watchlist":{ly:[{text:"这么多人？"},{text:"……迟迟也在里面？"}],zc:[{text:"这么多人？"},{text:"这后台不像临时搭的。"}]},
 "admin-shen-record":{ly:[{text:"这些时间都记得这么细？"},{text:"10月16号那几条……截图。"}],zc:[{text:"19:49转交，20:52采血，21:06控制。"},{text:"三个时间是连着的。"}]},
 "admin-liang-record":{ly:[{text:"操。"},{text:"真的是我。"},{text:"这东西从什么时候开始记我的？"}],zc:[{text:"这是梁茵那份？"},{text:"今天18:42还在自动刷新，说明这系统现在还在跑。"}]},
 "admin-pair-2004":{ly:[{text:"A这边是客β，B这边是客α。"},{text:"这两个希腊字母看着不像人名，更像他们给‘客’单独编的号。"}],zc:[{text:"这份比经文直接。"},{text:"两边都写了易舍完成，还各自留了客编号。"}]},
 "admin-reswap-2026":{ly:[{text:"这里写的是‘再次易舍’，而且特意标了稳定期22年。"},{text:"试验目的那句你怎么看？"}],zc:[{text:"稳定22年以后又做一次。"},{text:"这不像临时决定的。"}]},
 "admin-sync-shen":{ly:[{text:"这条才是在解释沈妍为什么被抓。"},{text:"10月12号再舍完成以后，她这边的同步反应一直往上升；10月16号后台才把她转成‘已控制’。"}],zc:[{text:"他们自己把这条标成了关联异常。"},{text:"‘控制’和执行批次比解释更重要。"}]},
 "admin-third-1907":{ly:[{text:"她连自己到底叫沈妍还是林楠都说不稳。"},{text:"但一听到徐宁这个名字就哭……这比直接认出你更吓人。"}],zc:[{text:"姓名陈述来回变？"},{text:"那就不是一句口误能解释的。"}]},
 "admin-location-hln04":{ly:[{text:"地址有了。"},{text:"别自己去。报警，把后台记录和这个地址一起交出去。"}]},
};

const received=(contactId:string,materialId:string)=>!!wechatSession.sent[`${contactId}:${materialId}`];
export const triggerZhouLocationThreat=()=>{
 wechatSession.locationKnown=true;
 if(wechatSession.locationThreatSent||!wechatSession.zhouIdentityKnown||!wechatSession.zhouConfronted)return false;
 wechatSession.locationThreatSent=true;
 const items:Msg[]=[{who:"对方",text:"别报警。"},{who:"对方",text:"HL-N-04，对吧。"},{who:"对方",text:"沈妍还在我们手里。"}];
 wechatSession.extra={...wechatSession.extra,zc:[...(wechatSession.extra.zc||[]),...items]};
 const final:QuickReply[]=[
  {id:"zc-final-report",text:"我会报警。",emphasis:true,ending:"report",reply:[{text:"那就赌他们比我们快。"}]},
  {id:"zc-final-go",text:"我一个人去。",ending:"double",reply:[{text:"手机留下。"},{text:"到门口以后再联系我。"}]},
 ];
 wechatSession.quick={...wechatSession.quick,zc:[{id:"zc-threat",text:"你在威胁我？",emphasis:true,reply:[{text:"对。"},{text:"我就是在威胁你。"},{text:"一个人来。别报警。"}],next:final}]};
 emitWechatNotice("zc","沈妍还在我们手里。");
 notifyWechat();
 return true;
};

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
  if(hasAnomaly)return [{text:"我看不懂。"},{text:"但“忆可乱”这几个字看着很不舒服。"},{text:"跟我小时候那些事放一起更不舒服。"}];
  return [{text:"看不懂。"},{text:"你从哪找到的？"}];
 }

 if(contactId==="ly"&&materialId==="admin-reswap-2026"&&!received("ly","admin-pair-2004"))return [{text:"这里写的是‘再次易舍’。"},{text:"但第一次是哪次？你手里是不是还有2004年的旧案？"}];
 if(contactId==="ly"&&materialId==="admin-sync-shen"&&!received("ly","admin-reswap-2026"))return [{text:"这条只有结果，没有前因。"},{text:"10月12号那边到底做了什么，得先对上。"}];
 return materialRules[materialId]?.[contactId]??null;
};

const syncReasoningChoices=():QuickReply[]=>{
 const correct:QuickReply={id:"ly-sync-right",text:"所以沈妍被抓，是因为那次再舍以后她这里出了同步异常？",reply:[{text:"对。"},{text:"时间能对上：12号再舍完成，沈妍这边开始异常；16号他们把她控制起来。"},{text:"所以抓沈妍不是为了再给她换一次，是为了处理试验冒出来的异常。"},{text:"现在得找她被转到哪。"}]};
 const wrongAgain:QuickReply={id:"ly-sync-wrong-again",text:"所以他们抓沈妍，是准备再给她换一次？",reply:[{text:"我觉得不是。"},{text:"沈妍这份写的是‘控制旧对契另一端’，处置理由也是同步异常。"}]};
 const wrongForum:QuickReply={id:"ly-sync-forum",text:"还是因为沈妍查论坛查得太深？",reply:[{text:"他们当然一直监控她。"},{text:"但这份处置理由写的是同步异常，不是论坛行为。"}]};
 wrongAgain.next=[correct,wrongForum];wrongForum.next=[wrongAgain,correct];
 return [wrongAgain,correct,wrongForum];
};
const reswapReasoningChoices=(includeSync:boolean):QuickReply[]=>{
 const correct:QuickReply={id:"ly-reswap-test",text:"客α没变，只是从林楠那条记录换到了19-07？",reply:[{text:"对，我也是这么看的。"},{text:"而且他们专门挑了一个已经稳定22年的客α，再做第二次易舍。"},{text:"所以这次是在验证同一个‘客’能不能连续换舍。"},{text:"但这份还没解释沈妍为什么会被抓。"}],next:includeSync?syncReasoningChoices():[]};
 const wrongShen:QuickReply={id:"ly-reswap-shen",text:"所以他们这次还是在换沈妍？",reply:[{text:"先别看名字。"},{text:"执行前林楠那条是客α，执行后19-07变成客α；真正连续的是这个编号。"}]};
 const wrongRepeat:QuickReply={id:"ly-reswap-repeat",text:"只是把2004年的仪式原样再做一次？",reply:[{text:"不太像。"},{text:"这次特意写了稳定22年和‘再舍验证’，目的明显是测试第二次转移。"}]};
 wrongShen.next=[correct,wrongRepeat];wrongRepeat.next=[wrongShen,correct];
 return [wrongShen,correct,wrongRepeat];
};
const pairReasoningChoices=():QuickReply[]=>{
 const correct:QuickReply={id:"ly-pair-guest-id",text:"α、β应该是在给‘客’编号？",reply:[{text:"我也觉得。"},{text:"名字写在‘舍’那一栏，α、β却一直跟着‘客’。"},{text:"如果后台能搜编号，同一个编号后来跑到哪，应该比盯着人名清楚。"}]};
 const wrongPerson:QuickReply={id:"ly-pair-person-id",text:"α、β会不会只是两个人的匿名编号？",reply:[{text:"也可能。"},{text:"但它们正好写在‘客编号’后面，我会先按那个字段理解。"}],next:[correct]};
 const wrongBatch:QuickReply={id:"ly-pair-batch-id",text:"是不是仪式批次号？",reply:[{text:"批次号他们都写成LN、RS那种格式。"},{text:"α、β看着是另一套编号。"}],next:[correct]};
 return [wrongPerson,correct,wrongBatch];
};

const quickAfterMaterial=(contactId:string,materialId:string):QuickReply[]=>{
 if(contactId==="zc"&&materialId==="sanmen"){
  const hasPair=received("zc","10731")||(received("zc","09114")&&received("zc","09831"));
  return [{id:"zc-sanmen-body",text:"你觉得“舍”和“客”指什么？",reply:[{text:"硬按字面猜的话，“舍”像住的地方。"},{text:"如果前一句真是“身为舍，魂为客”，那舍就是身体，客就是……住进去的那个东西。"},{text:"我只是按中文意思说，不代表这东西真在讲这个。"}],next:[{id:"zc-sanmen-two",text:"那“二客相契，两门相应”呢？",reply:hasPair?[{text:"两个客，两个门。"},{text:"跟你前面那两个人放一起，我第一反应会是两边一起发生了什么。"},{text:"但我现在也只能到这。"}]:[{text:"两个客、两个门，大概至少不是只说一个人。"},{text:"再往下我没东西能对。"}]}]}];
 }
 if(contactId==="ly"&&materialId==="sanmen")return [{id:"ly-sanmen-memory",text:"“忆可乱”这句你怎么看？",reply:[{text:"我不知道它原来想说什么。"},{text:"我小时候有一阵，别人喊我名字的时候，我真的会觉得他们叫错人了。"},{text:"现在想起来还是怪。"}]}];
 if(contactId==="zc"&&materialId==="verse")return [{id:"zc-verse-source",text:"所以黑底那张和《三门疏》不是一份？",reply:[{text:"至少那篇旧帖里的人是这么判断的。"},{text:"文件编号和扫描方式都不一样。"},{text:"后来为什么被塞进一个包里，就没人说得清。"}]}];
 if(contactId==="zc"&&materialId==="23109")return [{id:"zc-ritual-fragment",text:"“赤烛引客，黄符镇舍”像什么？",reply:[{text:"不知道。"},{text:"但这句不像网友临时编的，跟图里的摆法是一起的。"},{text:"“镇舍”听着像他们自己固定用的词。"}]}];
 if(contactId==="zc"&&materialId==="27614"){
  const hasBothReports=received("zc","09114")&&received("zc","09831");
  return [{id:"zc-admin-repeat",text:"但我刚才查的几篇里都有这个号。",reply:hasBothReports?[{text:"等等。"},{text:"你前面发我的那两条旧报，也是它恢复的？"},{text:"……这么放一起确实挺巧。"}]:[{text:"哪几篇？"},{text:"你发我看看。"}]}];
 }
 if(contactId==="ly"&&materialId==="admin-pair-2004")return pairReasoningChoices();
 if(contactId==="ly"&&materialId==="admin-reswap-2026"){
  if(!received("ly","admin-pair-2004"))return [];
  return reswapReasoningChoices(received("ly","admin-sync-shen"));
 }
 if(contactId==="ly"&&materialId==="admin-sync-shen"){
  if(!received("ly","admin-reswap-2026")||!received("ly","admin-pair-2004"))return [];
  return syncReasoningChoices();
 }
 if(contactId==="ly"&&materialId==="admin-third-1907"){
  const base:QuickReply={id:"ly-third-identity",text:"她听到徐宁这个名字为什么会哭？",reply:[{text:"……这才吓人。"},{text:"她连名字都说不稳，但情绪反应还在。"},{text:"真找到地点，这个人也得告诉警方。"}]};
  if(received("ly","admin-location-hln04"))base.next=[{id:"ly-report-both",text:"地址也有了。把19-07一起报给警方。",emphasis:true,ending:"report",reply:[{text:"对。两个人都报。别自己过去。"}]}];
  return [base];
 }
 if(contactId==="ly"&&materialId==="admin-location-hln04"){
  if(received("ly","admin-third-1907"))return [{id:"ly-report-both-now",text:"报警，把沈妍和19-07的记录一起交出去。",emphasis:true,ending:"report",reply:[{text:"对。两个人都报。你别自己去。"}]}];
  return [{id:"ly-report-shen",text:"报警，先把沈妍的位置交出去。",emphasis:true,ending:"report",reply:[{text:"好。截图别漏，地址和批次都给他们。"}]},{id:"ly-check-third",text:"我再确认一下19-07。",reply:[{text:"行，但快点。地址已经有了。"}]}];
 }

 if(contactId==="ly"&&materialId==="admin-liang-record")return [
  {id:"ly-admin-2017",text:"最早是2017年。",reply:[{text:"2017？"},{text:"我那年才刚开始在论坛里写小时候那些事。"},{text:"所以不是我后来跟沈妍聊上以后，他们才盯我的。"}],next:[
   {id:"ly-admin-2021",text:"2021年三月还有一次“线下接触”。",reply:[{text:"等一下。"},{text:"那年三月我确实见过一个论坛里认识的女的。"},{text:"就吃了顿饭，她一直问我小时候走失那阵的事。"},{text:"我当时真以为就是网友聊天。"}],next:[
    {id:"ly-admin-2024",text:"2024年写着“终止转交”。",reply:[{text:"2024年一月……"},{text:"那次有人本来让我跟她去另一个地方。"},{text:"我没去。临时有人来接我，我就走了。"},{text:"所以他们写的“转交”是这个？"}],next:[
     {id:"ly-admin-now",text:"今天18:42还有设备记录刷新。",reply:[{text:"今天？"},{text:"我今天根本没上论坛。"},{text:"……有点恶心了。"},{text:"我先把定位关了。"},{text:"你继续看。沈妍那边比我急。"}]}
    ]}
   ]}
  ]},
  {id:"ly-admin-2021-direct",text:"2021年三月有第一次线下接触。",reply:[{text:"等一下。"},{text:"那年三月我确实见过一个论坛里认识的女的。"},{text:"就吃了顿饭，她一直问我小时候走失那阵的事。"},{text:"我当时真以为就是网友聊天。"}]}
 ];
 return [];
};

const textReply=(contact:string,text:string):ReplyPart[]|null=>{
 const t=text.replace(/\s/g,"");
 if(contact==="yq"){
  if(/有消息|找到|找到了/.test(t))return [{text:"还没有吗？"},{text:"她昨晚走的时候真的没说别的。"}];
  if(/几点|分开|什么时候走/.test(t))return [{text:"我九点左右先走的。"},{text:"21:03那句‘到家说一声’就是我离开以后发的。"}];
  if(/后来|别人|谁来|还有人|介绍|交给|转交/.test(t))return [{text:"……后来确实有人过来了一下。"},{text:"是之前跟她聊过旧事的一个女的。"},{text:"我跟那个人也不熟，就是以前介绍她们认识。"}];
  if(/昨晚|见面|去哪|在哪/.test(t))return [{text:"昨晚是见到了。"},{text:"她说胃不舒服，我九点左右先走。"},{text:"她没跟我说后面去哪。"}];
  if(/林楠/.test(t))return [{text:"真没听过这个名字。"}];
 }
 if(contact==="zc"){
  if(/后台|管理系统|管理后台/.test(t))return [{text:"什么后台？"},{text:"你截图了吗？尤其时间和操作人。"}];
  if(/已控制|转交|血样/.test(t))return [{text:"转交、采血、控制是连着的吗？"},{text:"这就不像普通账号记录了。"}];
  if(/林楠/.test(t))return [{text:"她没跟我说过这个名字。"},{text:"你从哪翻到的？"}];
  if(/失踪|不见了|联系不上/.test(t))return [{text:"她现在还是完全联系不上？"},{text:"电话也不通？"}];
  if(/换魂|灵魂|交换/.test(t))return [{text:"你是说真的把两个人换了？"},{text:"我不知道。光这些我不敢这么说。"}];
  if(/名字不对|另一个家|回来以后不会/.test(t))return [{text:"我好像见过这种说法。"},{text:"站里走失帖不少，具体哪篇我记不清了。"}];
 }
 if(contact==="ly"){
  if(/后台|管理系统|管理后台/.test(t))return [{text:"……后台？"},{text:"能查账号吗？"},{text:"那你搜一下我。"},{text:"搜“迟迟”就行。"}];
  if(/有你|搜到你|你的记录|梁茵/.test(t))return [{text:"操"},{text:"真的有？"},{text:"这东西从什么时候开始记我的？"}];
  if(/2017|最早|加入观察名单/.test(t))return [{text:"2017？"},{text:"我那年才刚开始在论坛里写小时候那些事。"},{text:"所以不是我后来跟沈妍聊上以后，他们才盯我的。"}];
  if(/2021|三月|第一次线下接触/.test(t))return [{text:"等一下。"},{text:"2021年三月我确实见过一个论坛里认识的女的。"},{text:"就吃了顿饭。她一直问我小时候走失那阵的事。"},{text:"我当时真以为就是网友聊天。"}];
  if(/18[:：]?42|今天|最后更新|设备记录|定位/.test(t))return [{text:"今天？"},{text:"我今天根本没上论坛。"},{text:"……有点恶心了。"},{text:"我先把定位关了。"},{text:"你继续看，别停。"}];
  if(/终止转交|2024|转交/.test(t))return [{text:"2024年一月……"},{text:"那次有人本来让我跟她去另一个地方。"},{text:"我没去。临时有人来接我，我就走了。"},{text:"所以他们写的“转交”是这个？"}];
  if(/沈妍.*已控制|已控制.*沈妍/.test(t))return [{text:"……"},{text:"那先别管我这边。"},{text:"你继续找她现在在哪。"}];
  if(/林楠/.test(t))return [{text:"林楠？"},{text:"我不认识。"}];
  if(/名字|另一个家|不会/.test(t))return [{text:"嗯。"},{text:"我小时候也说过类似的话。"},{text:"这事打字说有点怪。"}];
  if(/换魂|灵魂|交换/.test(t))return [{text:"你是说……两个人真的互换？"},{text:"我不知道。我以前没敢往这上面想。"}];
 }
 return null;
};

const fallbackReply=(contact:string):ReplyPart[]=>{
 if(contact==="yq")return [{text:"这个我真不知道。"},{text:"你如果是问昨晚的事，可以直接问我。"}];
 if(contact==="zc")return [{text:"这我没法接。"},{text:"你是查到什么了？"}];
 if(contact==="ly")return [{text:"等下，我有点没跟上。"},{text:"你说具体一点，是沈妍还是论坛里的事？"}];
 return [{text:"我不知道。"}];
};

const introText=(contactId:string)=>{
 if(contactId==="yq")return "你好，我是徐宁，沈妍朋友。她今天一直联系不上，我现在在她家。你们昨晚是不是见过？她走的时候有说去哪吗？";
 if(contactId==="zc")return "你好，我是徐宁，沈妍朋友。她今天一直联系不上。我现在在她家，她电脑微信还登着。看到你们最近有聊天，方便问你两句吗？";
 if(contactId==="ly")return "你好，我是徐宁，沈妍朋友。她今天一直联系不上。我现在在她家，她电脑微信还登着。看到你们最近有聊天，方便问你两句吗？";
 return "你好，我是徐宁，沈妍朋友。她今天一直联系不上，我现在在她家。";
};

const introReply=(contactId:string):{parts:ReplyPart[];next:QuickReply[]}=>{
 if(contactId==="yq"){
  const after:QuickReply={id:"yq-after-person",text:"她后来还见了别人吗？",reply:[{text:"……后来确实有人过来了一下。"},{text:"是之前跟她聊过旧事的一个女的。"},{text:"我跟那个人也不熟，就是以前介绍她们认识。"}]};
  const when:QuickReply={id:"yq-left-when",text:"你们昨晚几点分开的？",reply:[{text:"我九点左右先走的。"},{text:"21:03那句‘到家说一声’就是我走以后发的。"}],next:[after]};
  const free:QuickReply={id:"yq-free-intro",text:"自己问一句…",freeText:true,reply:[],next:[when]};
  return {parts:[{text:"你是徐宁？沈妍提过你。"},{text:"她今天还没回你？昨晚我们确实见过。"}],next:[when,free]};
 }
 if(contactId==="zc"){
  const recent:QuickReply={id:"zc-recent",text:"她最近跟你说过什么？",reply:[{text:"还是那个梦。"},{text:"她前几天开始觉得里面有人叫‘楠楠’。"},{text:"我让她别半夜一直翻旧帖。"}]};
  const free:QuickReply={id:"zc-free-intro",text:"自己问一句…",freeText:true,reply:[],next:[recent]};
  return {parts:[{text:"徐宁？她提过你。"},{text:"她今天一直没回？电话也不通？"}],next:[recent,free]};
 }
 if(contactId==="ly"){
  const know:QuickReply={id:"ly-how-know",text:"你和沈妍怎么认识的？",reply:[{text:"论坛。"},{text:"我以前发过小时候走失以后的一些事，她私信过我。"},{text:"后来才慢慢聊熟。"}]};
  const free:QuickReply={id:"ly-free-intro",text:"自己问一句…",freeText:true,reply:[],next:[know]};
  return {parts:[{text:"徐宁？我知道你，沈妍提过。"},{text:"她怎么了？"}],next:[know,free]};
 }
 return {parts:[],next:[]};
};

export const triggerAdminWechatBeat=(beat:"shen-record")=>{
 if(wechatSession.adminBeats[beat])return false;
 wechatSession.adminBeats={...wechatSession.adminBeats,[beat]:true};
 const push=(contactId:string,items:Msg[])=>{wechatSession.extra={...wechatSession.extra,[contactId]:[...(wechatSession.extra[contactId]||[]),...items]}};
 const lyItems=[{who:"对方" as const,text:"你还在查吗？"},{who:"对方" as const,text:"有找到新的东西吗？"}];
 const zcItems=wechatSession.introduced.zc?[{who:"对方" as const,text:"她还是没消息？"}]:[{who:"对方" as const,text:"你昨天不是还在查旧档吗？今天怎么没动静。"}];
 const yqItems=wechatSession.introduced.yq?[{who:"对方" as const,text:"有消息了吗？"}]:[{who:"对方" as const,text:"你今天好点没？"},{who:"对方" as const,text:"怎么一直没回我。"}];
 push("ly",lyItems);push("zc",zcItems);push("yq",yqItems);
 emitWechatNotice("ly",lyItems[lyItems.length-1].text);
 emitWechatNotice("zc",zcItems[zcItems.length-1].text);
 emitWechatNotice("yq",yqItems[yqItems.length-1].text);
 notifyWechat();
 return true;
};

export default function InteractiveWechat({materials,onOpenPost}:{materials:SharedMaterial[];onOpenPost?:(id:string)=>void}){
 const [id,setId]=useState(()=>wechatSession.activeId),[q,setQ]=useState(()=>wechatSession.searchQuery),[draft,setDraft]=useState(()=>wechatSession.draft),[picker,setPicker]=useState(false);
 const [extra,setExtra]=useState<Record<string,Msg[]>>(()=>({...wechatSession.extra}));
 const [introduced,setIntroduced]=useState<Record<string,boolean>>(()=>({...wechatSession.introduced}));
 const [typing,setTyping]=useState<Record<string,boolean>>({});
 const [sent,setSent]=useState<Record<string,boolean>>(()=>({...wechatSession.sent}));
 const [quick,setQuick]=useState<Record<string,QuickReply[]>>(()=>({...wechatSession.quick}));
 const [locked,setLocked]=useState<Record<string,boolean>>(()=>({...wechatSession.locked}));
 const [freeText,setFreeText]=useState<Record<string,boolean>>(()=>({...wechatSession.freeText}));
 const scrollRef=useRef<HTMLElement|null>(null);
 const contact=contacts.find(x=>x.id===id)!;
 const visible=contacts.filter(x=>(x.name+x.note+x.preview).includes(q));
 const messages=useMemo(()=>[...contact.messages,...(extra[id]||[])],[contact,extra,id]);
 const previewFor=(c:Contact)=>{const added=extra[c.id]||[];return added.length?added[added.length-1].text:c.preview};
 const actionLocked=!!locked[id]||!!typing[id];
 const hasQuick=(quick[id]||[]).length>0;
 const canFreeText=id!=="x"&&!!introduced[id]&&!!freeText[id]&&!actionLocked&&!hasQuick;
 const zhouHostile=id==="zc"&&wechatSession.zhouConfronted;
 const canPickMaterial=id!=="x"&&!!introduced[id]&&!actionLocked&&!hasQuick&&!freeText[id]&&!zhouHostile;
 const sendable=useMemo(()=>id==="x"||!introduced[id]||zhouHostile?[]:materials.filter(m=>{const rules=materialRules[m.id];return !!rules&&Object.prototype.hasOwnProperty.call(rules,id)&&rules[id]!==null&&!sent[`${id}:${m.id}`]}),[materials,id,sent,introduced,zhouHostile]);
 const appendFor=(contactId:string,items:Msg[])=>{
  wechatSession.extra={...wechatSession.extra,[contactId]:[...(wechatSession.extra[contactId]||[]),...items]};
  const incoming=[...items].reverse().find(x=>x.who==="对方"&&!!x.text);
  if(incoming?.text)emitWechatNotice(contactId,incoming.text);
  notifyWechat();
 };
 const ensureIntro=(contactId:string):Msg[]=>{
  if(contactId==="x"||wechatSession.introduced[contactId])return [];
  const stamp=advanceGameClock(1);
  wechatSession.introduced={...wechatSession.introduced,[contactId]:true};
  wechatSession.firstContact={...wechatSession.firstContact,[contactId]:stamp};
  notifyWechat();
  if(contactId==="zc"&&wechatSession.zhouIdentityKnown)window.setTimeout(()=>revealZhouConfrontation(),0);
  return [{time:`今天 ${stamp}`,who:"沈妍",text:introText(contactId)}];
 };
 const sendIntroduction=(contactId:string)=>{
  if(contactId==="x"||wechatSession.introduced[contactId]||wechatSession.locked[contactId])return;
  setLockedFor(contactId,true);
  const intro=ensureIntro(contactId);
  appendFor(contactId,intro);
  const start=introReply(contactId);
  delayedParts(contactId,start.parts,start.next);
 };
 const setQuickFor=(contactId:string,items:QuickReply[])=>{
  wechatSession.quick={...wechatSession.quick,[contactId]:items};
  notifyWechat();
 };
 const setLockedFor=(contactId:string,value:boolean)=>{
  wechatSession.locked={...wechatSession.locked,[contactId]:value};
  notifyWechat();
 };
 const setFreeTextFor=(contactId:string,value:boolean,returnQuick:QuickReply[]=[])=>{
  wechatSession.freeText={...wechatSession.freeText,[contactId]:value};
  wechatSession.freeReturn={...wechatSession.freeReturn,[contactId]:returnQuick};
  notifyWechat();
 };
 const delayedParts=(contactId:string,parts:ReplyPart[]|null,nextQuick:QuickReply[]=[] )=>{
  if(!parts?.length){setLockedFor(contactId,false);setQuickFor(contactId,nextQuick);return;}
  let elapsed=1000+Math.floor(Math.random()*900);
  setTyping(prev=>({...prev,[contactId]:true}));
  parts.forEach((part,index)=>{
   const extraDelay=part.text?Math.min(2200,part.text.length*35):700;
   elapsed+=extraDelay+Math.floor(Math.random()*1000);
   window.setTimeout(()=>{
    if(part.material)appendFor(contactId,[{who:"对方",text:`[链接] ${part.material.title}`,material:part.material}]);
    else if(part.text)appendFor(contactId,[{who:"对方",text:part.text}]);
    if(index===parts.length-1){setTyping(prev=>({...prev,[contactId]:false}));setLockedFor(contactId,false);setQuickFor(contactId,nextQuick)}
   },elapsed);
  });
 };

 useEffect(()=>{
  const sync=()=>{
   setExtra({...wechatSession.extra});
   setIntroduced({...wechatSession.introduced});
   setSent({...wechatSession.sent});
   setQuick({...wechatSession.quick});
   setLocked({...wechatSession.locked});
   setFreeText({...wechatSession.freeText});
  };
  wechatSubscribers.add(sync);
  sync();
  return ()=>{wechatSubscribers.delete(sync)};
 },[]);
 useEffect(()=>{wechatSession.activeId=id;wechatSession.searchQuery=q;wechatSession.draft=draft},[id,q,draft]);
 useEffect(()=>{
  const el=scrollRef.current;
  if(el)el.scrollTop=el.scrollHeight;
 },[id,messages.length,typing[id]]);
 useEffect(()=>{setPicker(false);setDraft("")},[id]);

 const sendText=(e:FormEvent)=>{
  e.preventDefault();
  const text=draft.trim(); if(!text||!canFreeText||wechatSession.locked[id]||!wechatSession.freeText[id])return;
  const returnQuick=wechatSession.freeReturn[id]||[];
  setLockedFor(id,true);
  setFreeTextFor(id,false,[]);
  appendFor(id,[{who:"沈妍",text}]);
  setDraft("");
  delayedParts(id,textReply(id,text)??fallbackReply(id),returnQuick);
 };
 const sendMaterial=(material:SharedMaterial)=>{
  if(!canPickMaterial||wechatSession.locked[id])return;
  const rules=materialRules[material.id];
  if(!rules||!Object.prototype.hasOwnProperty.call(rules,id))return;
  setLockedFor(id,true);
  const reply=materialReply(id,material.id);
  appendFor(id,[{who:"沈妍",text:`[分享] ${material.title}`,material}]);
  wechatSession.sent={...wechatSession.sent,[`${id}:${material.id}`]:true};
  notifyWechat();
  setPicker(false);
  delayedParts(id,reply,quickAfterMaterial(id,material.id));
 };
 const sendQuick=(item:QuickReply)=>{
  if(id==="x"||actionLocked||wechatSession.locked[id])return;
  setQuickFor(id,[]);
  if(item.freeText){setFreeTextFor(id,true,item.next||[]);return;}
  setLockedFor(id,true);
  appendFor(id,[{who:"沈妍",text:item.sendText||item.text}]);
  if(item.id==="zc-zheliu")wechatSession.zhouConfronted=true;
  delayedParts(id,item.reply,item.next||[]);
  if(item.id==="zc-zheliu-how"&&wechatSession.locationKnown)window.setTimeout(()=>triggerZhouLocationThreat(),5200);
  if(item.ending){const kind=item.ending==="double"?"double":received("ly","admin-third-1907")?"true":"home";window.setTimeout(()=>beginEnding(kind),6500)}
 };
 const openMaterial=(material:SharedMaterial)=>{
  if(material.kind==="论坛帖子"&&/^\d+$/.test(material.id)&&onOpenPost)onOpenPost(material.id);
 };

 return <div className="wechat" style={{height:"calc(100% - 39px)",minHeight:0,overflow:"hidden"}}>
  <aside style={{height:"100%",minHeight:0,overflowY:"auto"}}><header><i>妍</i><span><b>沈妍</b><small>微信已登录</small></span></header><label><Search/><input value={q} onChange={e=>setQ(e.target.value)} placeholder="搜索联系人和消息"/></label>{visible.map(x=><button className={x.id===id?"active":""} onClick={()=>setId(x.id)} key={x.id}><i>{x.name[0]}</i><span style={{minWidth:0}}><b>{x.name}</b><small style={{display:"block",marginTop:2,color:"#7f8783",whiteSpace:"nowrap",overflow:"hidden",textOverflow:"ellipsis"}}>{x.note}</small><small style={{display:"block",marginTop:3,whiteSpace:"nowrap",overflow:"hidden",textOverflow:"ellipsis"}}>{previewFor(x)}</small></span></button>)}</aside>
  <main style={{height:"100%",minHeight:0,display:"flex",flexDirection:"column",overflow:"hidden",position:"relative"}}>
   <header style={{flex:"0 0 auto"}}><b>{contact.name}</b><small>{actionLocked?"正在回复…":contact.note}</small>{contact.signature&&<small style={{display:"block",marginTop:3,color:"#929892",fontSize:10}}>个性签名：{contact.signature}</small>}</header>
   <section ref={scrollRef} style={{flex:"1 1 auto",minHeight:0,overflowY:"auto",overscrollBehavior:"contain"}}>{messages.map((m,i)=><div key={i}>{m.time&&<time>{m.time}</time>}<article className={m.who==="沈妍"?"mine":""}><i>{m.who==="沈妍"?"妍":contact.name[0]}</i>{m.material?<button type="button" onClick={()=>openMaterial(m.material!)} style={{maxWidth:360,padding:"11px 12px",border:"1px solid #d7d7d7",borderRadius:8,background:"#fff",textAlign:"left",cursor:m.material.kind==="论坛帖子"?"pointer":"default"}}><small style={{display:"block",color:"#888",marginBottom:5}}>{m.material.kind}</small><b style={{display:"block",fontSize:13,fontWeight:600,lineHeight:1.45}}>{m.material.title}</b><small style={{display:"block",marginTop:7,color:"#999",wordBreak:"break-all"}}>{m.material.url}</small>{m.material.kind==="论坛帖子"&&<small style={{display:"block",marginTop:7,color:"#3b7a57"}}>打开帖子</small>}</button>:<p>{m.text}</p>}</article></div>)}</section>

   {picker&&canPickMaterial&&<div style={{position:"absolute",left:12,right:12,bottom:76,zIndex:8,maxHeight:"42%",overflowY:"auto",padding:8,border:"1px solid #cfcfcf",borderRadius:9,background:"#fff",boxShadow:"0 10px 35px #0003"}}>
    <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"5px 6px 8px"}}><b style={{fontSize:13}}>发送文件</b><button onClick={()=>setPicker(false)} style={{width:28,height:28,border:0,borderRadius:6,background:"#f2f2f2",display:"grid",placeItems:"center"}}><X size={14}/></button></div>
    {sendable.length?sendable.map(m=><button key={m.id} onClick={()=>sendMaterial(m)} style={{width:"100%",display:"block",padding:"10px",border:0,borderTop:"1px solid #eee",background:"#fff",textAlign:"left"}}><small style={{display:"block",color:"#999",marginBottom:3}}>{m.kind}</small><b style={{fontSize:13,fontWeight:500}}>{m.title}</b></button>):<p style={{margin:0,padding:"18px 10px",borderTop:"1px solid #eee",color:"#999",fontSize:12,textAlign:"center"}}>暂无可发送文件</p>}
   </div>}

   {!actionLocked&&id!=="x"&&!introduced[id]&&<div style={{flex:"0 0 auto",padding:"10px 14px 0",background:"#f7f7f7"}}><button onClick={()=>sendIntroduction(id)} style={{padding:"8px 13px",border:"1px solid #b9d6c3",borderRadius:16,background:"#fff",color:"#267747",fontSize:12,fontWeight:700}}>先自我介绍</button></div>}

   {!actionLocked&&(quick[id]||[]).length>0&&<div style={{flex:"0 0 auto",display:"flex",gap:8,flexWrap:"wrap",padding:"9px 14px 0",background:"#f7f7f7"}}>{(quick[id]||[]).map(item=><button key={item.id} onClick={()=>sendQuick(item)} style={{maxWidth:"100%",padding:item.emphasis?"9px 14px":"7px 11px",border:item.emphasis?"2px solid #9f3f36":"1px solid #cfd8d2",borderRadius:15,background:item.emphasis?"#fff8f6":"#fff",color:item.emphasis?"#8c3029":"#3c6250",fontSize:12,fontWeight:item.emphasis?800:400,textAlign:"left"}}>{item.text}</button>)}</div>}

   <footer style={{flex:"0 0 auto",padding:"12px 14px",background:"#f7f7f7",borderTop:"1px solid #ddd"}}>
    <form onSubmit={sendText} style={{display:"grid",gridTemplateColumns:"1fr 64px 48px",gap:8,alignItems:"center"}}>
     <input disabled={!canFreeText} value={draft} onChange={e=>setDraft(e.target.value)} placeholder={canFreeText?"这一轮可以自己问一句":"输入消息"} style={{height:48,border:"1px solid #d0d0d0",borderRadius:8,padding:"0 14px",minWidth:0,fontSize:14,background:canFreeText?"#fff":"#efefef",color:canFreeText?"#222":"#999"}}/>
     <button type="button" onClick={()=>canPickMaterial&&setPicker(v=>!v)} disabled={!canPickMaterial} title="发送资料" aria-label="发送资料" style={{position:"relative",height:48,width:64,border:canPickMaterial?"2px solid #4a8a64":"1px solid #d0d0d0",borderRadius:7,background:"#fff",display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",gap:1,color:canPickMaterial?"#2d7550":"#777",opacity:canPickMaterial?1:.35,fontWeight:800}}><Plus size={21}/><span style={{fontSize:10,lineHeight:1}}>资料</span>{sendable.length>0&&<small style={{position:"absolute",right:-4,top:-5,minWidth:16,height:16,padding:"0 4px",borderRadius:8,background:"#39a65a",color:"#fff",fontSize:9,lineHeight:"16px"}}>{sendable.length}</small>}</button>
     <button type="submit" disabled={!canFreeText||!draft.trim()} style={{height:44,width:48,border:0,borderRadius:6,background:"#39a65a",color:"#fff",display:"grid",placeItems:"center",opacity:canFreeText&&draft.trim()?1:.35}}><Send size={16}/></button>
    </form>
   </footer>
  </main>
 </div>;
}
