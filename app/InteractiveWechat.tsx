"use client";

import {FormEvent,useEffect,useMemo,useRef,useState} from "react";
import {Plus,Search,Send,X} from "lucide-react";

export type SharedMaterial={id:string;title:string;kind:string;url:string};
export type WechatNotice={contactId:string;name:string;text:string};
type Msg={time?:string;who:"沈妍"|"对方";text:string;material?:SharedMaterial};
type Contact={id:string;name:string;note:string;preview:string;messages:Msg[]};
type ReplyPart={text?:string;material?:SharedMaterial};
type QuickReply={id:string;text:string;reply:ReplyPart[];next?:QuickReply[]};
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
  activeId:"x",
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
 "admin-watchlist":{ly:[{text:"这么多人？"},{text:"……迟迟也在里面？"}],zc:[{text:"先留着。"},{text:"这至少能证明不是只围着沈妍一个人建的后台。"}]},
 "admin-shen-record":{ly:[{text:"这些时间都记得这么细？"},{text:"10月16号那几条……你先留好。"}],zc:[{text:"把19:49、20:52、21:06这三条单独记下来。"},{text:"转交、样本、状态变更是连续的。"}]},
 "admin-liang-record":{ly:[{text:"操。"},{text:"真的是我。"},{text:"这东西从什么时候开始记我的？"}],zc:[{text:"这是梁茵那份？"},{text:"今天18:42还在自动刷新，说明这系统现在还在跑。"}]},
 "admin-pair-2004":{ly:[{text:"等一下。"},{text:"‘舍’是身体，‘客’是魂，对吧？"},{text:"那这不就是……把她俩的魂换了吗？"}],zc:[{text:"这份比经文有用。"},{text:"至少它明确写了两边互换，而且执行完成。"}]},
 "admin-reswap-2026":{ly:[{text:"原来第二次根本不是冲沈妍来的。"},{text:"他们是在拿林楠那一侧做第二次换身体的试验。"},{text:"因为那边那个‘客’已经稳定活了二十多年，他们想看同一个人还能不能再换一次。"}],zc:[{text:"把试验目的和执行时间留着。"},{text:"这能解释他们为什么选一个旧案幸存者。"}]},
 "admin-sync-shen":{ly:[{text:"所以对上了。"},{text:"林楠那边第二次一换，沈妍这边才开始梦到那些不属于她的童年。"},{text:"他们抓沈妍，不是要再换她一次，是因为旧的那条联系重新有反应。"}],zc:[{text:"这条已经是他们自己的因果判断。"},{text:"先别管玄学真假，‘控制’和执行批次都留着。"}]},
 "admin-third-1907":{ly:[{text:"她一直说自己叫沈妍？"},{text:"……那2004年被换进林楠身体里的那个，到底是谁。"}],zc:[{text:"这人的身份陈述值得单独留。"},{text:"如果报警，别只报沈妍一个。"}]},
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
  if(hasAnomaly)return [{text:"我看不懂。"},{text:"但“忆可乱”这几个字看着很不舒服。"},{text:"跟我小时候那些事放一起更不舒服。"}];
  return [{text:"看不懂。"},{text:"你从哪找到的？"}];
 }
 return materialRules[materialId]?.[contactId]??null;
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
  return [{id:"zc-admin-repeat",text:"但我刚才查的几篇里都有这个号。",reply:hasBothReports?[{text:"等等。"},{text:"你前面发我的那两条旧报，也是它恢复的？"},{text:"……这么放一起确实挺巧。"}]:[{text:"哪几篇？"},{text:"你把链接留着，我也翻翻。"}]}];
 }
 if(contactId==="ly"&&materialId==="admin-pair-2004")return [{id:"ly-pair-question",text:"我也是这么想的。",reply:[{text:"可是不对。"},{text:"如果她们小时候已经换完一次了——"},{text:"他们现在为什么又要抓沈妍？"}]}];
 if(contactId==="ly"&&materialId==="admin-reswap-2026")return [{id:"ly-reswap-next",text:"那沈妍为什么也会有反应？",reply:[{text:"对，我也在想这个。"},{text:"你看它最后那句，‘原对契 0712-4471 出现同步异常’。"},{text:"后台应该还有沈妍这一侧的关联记录。"}]}];
 if(contactId==="ly"&&materialId==="admin-sync-shen")return [{id:"ly-sync-now",text:"所以她是被抓回来控制这个异常？",reply:[{text:"我看就是。"},{text:"第二次试验是林楠那边。"},{text:"沈妍是那次试验把二十年前那条旧联系重新扯醒以后，才被他们抓回去的。"},{text:"现在最要紧的是她在哪。"}]}];
 if(contactId==="ly"&&materialId==="admin-third-1907")return [{id:"ly-third-identity",text:"她还要求联系徐宁。",reply:[{text:"……"},{text:"这就更不像随口胡说了。"},{text:"先把这份也留好。真找到地方的话，这个人也得一起报。"}]}];
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
  if(/昨晚|见面|去哪|在哪/.test(t))return [{text:"昨晚是见到了。"},{text:"后来她说胃不舒服，我就先走了。"},{text:"她没跟我说后面去哪。"}];
  if(/林楠/.test(t))return [{text:"真没听过这个名字。"}];
 }
 if(contact==="zc"){
  if(/后台|管理系统|管理后台/.test(t))return [{text:"什么后台？"},{text:"先把时间、操作人和原始字段留着。"},{text:"状态词先别急着按字面信。"}];
  if(/已控制|转交|血样/.test(t))return [{text:"先看时间。"},{text:"能不能跟她昨晚的行程对上？"}];
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

const introText=(contactId:string)=>{
 if(contactId==="yq")return "你好，我是徐宁，沈妍朋友。她今天一直联系不上，我现在在她家。你们昨晚是不是见过？她走的时候有说去哪吗？";
 if(contactId==="zc")return "你好，我是徐宁，沈妍朋友。她今天一直联系不上。我现在在她家，她电脑微信还登着。看到你们最近有聊天，方便问你两句吗？";
 if(contactId==="ly")return "你好，我是徐宁，沈妍朋友。她今天一直联系不上。我现在在她家，她电脑微信还登着。看到你们最近有聊天，方便问你两句吗？";
 return "你好，我是徐宁，沈妍朋友。她今天一直联系不上，我现在在她家。";
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
 const scrollRef=useRef<HTMLElement|null>(null);
 const contact=contacts.find(x=>x.id===id)!;
 const visible=contacts.filter(x=>(x.name+x.note+x.preview).includes(q));
 const messages=useMemo(()=>[...contact.messages,...(extra[id]||[])],[contact,extra,id]);
 const previewFor=(c:Contact)=>{const added=extra[c.id]||[];return added.length?added[added.length-1].text:c.preview};
 const sendable=useMemo(()=>materials.filter(m=>Object.prototype.hasOwnProperty.call(materialRules[m.id]||{},id)&&!sent[`${id}:${m.id}`]),[materials,id,sent]);
 const appendFor=(contactId:string,items:Msg[])=>{
  wechatSession.extra={...wechatSession.extra,[contactId]:[...(wechatSession.extra[contactId]||[]),...items]};
  const incoming=[...items].reverse().find(x=>x.who==="对方"&&!!x.text);
  if(incoming?.text)emitWechatNotice(contactId,incoming.text);
  notifyWechat();
 };
 const ensureIntro=(contactId:string):Msg[]=>{
  if(contactId==="x"||wechatSession.introduced[contactId])return [];
  wechatSession.introduced={...wechatSession.introduced,[contactId]:true};
  notifyWechat();
  return [{who:"沈妍",text:introText(contactId)}];
 };
 const setQuickFor=(contactId:string,items:QuickReply[])=>{
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

 useEffect(()=>{
  const sync=()=>{
   setExtra({...wechatSession.extra});
   setIntroduced({...wechatSession.introduced});
   setSent({...wechatSession.sent});
   setQuick({...wechatSession.quick});
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
 useEffect(()=>setPicker(false),[id]);

 const sendText=(e:FormEvent)=>{
  e.preventDefault();
  const text=draft.trim(); if(!text||id==="x")return;
  const intro=ensureIntro(id);
  appendFor(id,[...intro,{who:"沈妍",text}]);
  setQuickFor(id,[]);
  setDraft("");
  delayedParts(id,textReply(id,text));
 };
 const sendMaterial=(material:SharedMaterial)=>{
  const rules=materialRules[material.id];
  if(!rules||!Object.prototype.hasOwnProperty.call(rules,id))return;
  const reply=materialReply(id,material.id);
  const intro=ensureIntro(id);
  appendFor(id,[...intro,{who:"沈妍",text:`[分享] ${material.title}`,material}]);
  wechatSession.sent={...wechatSession.sent,[`${id}:${material.id}`]:true};
  notifyWechat();
  setPicker(false);
  delayedParts(id,reply,quickAfterMaterial(id,material.id));
 };
 const sendQuick=(item:QuickReply)=>{
  if(id==="x")return;
  setQuickFor(id,[]);
  appendFor(id,[{who:"沈妍",text:item.text}]);
  delayedParts(id,item.reply,item.next||[]);
 };
 const openMaterial=(material:SharedMaterial)=>{
  if(material.kind==="论坛帖子"&&/^\d+$/.test(material.id)&&onOpenPost)onOpenPost(material.id);
 };

 return <div className="wechat" style={{height:"calc(100% - 39px)",minHeight:0,overflow:"hidden"}}>
  <aside style={{height:"100%",minHeight:0,overflowY:"auto"}}><header><i>妍</i><span><b>沈妍</b><small>微信已登录</small></span></header><label><Search/><input value={q} onChange={e=>setQ(e.target.value)} placeholder="搜索联系人和消息"/></label>{visible.map(x=><button className={x.id===id?"active":""} onClick={()=>setId(x.id)} key={x.id}><i>{x.name[0]}</i><span style={{minWidth:0}}><b>{x.name}</b><small style={{display:"block",marginTop:2,color:"#7f8783",whiteSpace:"nowrap",overflow:"hidden",textOverflow:"ellipsis"}}>{x.note}</small><small style={{display:"block",marginTop:3,whiteSpace:"nowrap",overflow:"hidden",textOverflow:"ellipsis"}}>{previewFor(x)}</small></span></button>)}</aside>
  <main style={{height:"100%",minHeight:0,display:"flex",flexDirection:"column",overflow:"hidden",position:"relative"}}>
   <header style={{flex:"0 0 auto"}}><b>{contact.name}</b><small>{typing[id]?"正在输入…":contact.note}</small></header>
   <section ref={scrollRef} style={{flex:"1 1 auto",minHeight:0,overflowY:"auto",overscrollBehavior:"contain"}}>{messages.map((m,i)=><div key={i}>{m.time&&<time>{m.time}</time>}<article className={m.who==="沈妍"?"mine":""}><i>{m.who==="沈妍"?"妍":contact.name[0]}</i>{m.material?<button type="button" onClick={()=>openMaterial(m.material!)} style={{maxWidth:360,padding:"11px 12px",border:"1px solid #d7d7d7",borderRadius:8,background:"#fff",textAlign:"left",cursor:m.material.kind==="论坛帖子"?"pointer":"default"}}><small style={{display:"block",color:"#888",marginBottom:5}}>{m.material.kind}</small><b style={{display:"block",fontSize:13,fontWeight:600,lineHeight:1.45}}>{m.material.title}</b><small style={{display:"block",marginTop:7,color:"#999",wordBreak:"break-all"}}>{m.material.url}</small>{m.material.kind==="论坛帖子"&&<small style={{display:"block",marginTop:7,color:"#3b7a57"}}>打开帖子</small>}</button>:<p>{m.text}</p>}</article></div>)}</section>

   {picker&&<div style={{position:"absolute",left:12,right:12,bottom:76,zIndex:8,maxHeight:"42%",overflowY:"auto",padding:8,border:"1px solid #cfcfcf",borderRadius:9,background:"#fff",boxShadow:"0 10px 35px #0003"}}>
    <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"5px 6px 8px"}}><b style={{fontSize:13}}>发送文件</b><button onClick={()=>setPicker(false)} style={{width:28,height:28,border:0,borderRadius:6,background:"#f2f2f2",display:"grid",placeItems:"center"}}><X size={14}/></button></div>
    {sendable.length?sendable.map(m=><button key={m.id} onClick={()=>sendMaterial(m)} style={{width:"100%",display:"block",padding:"10px",border:0,borderTop:"1px solid #eee",background:"#fff",textAlign:"left"}}><small style={{display:"block",color:"#999",marginBottom:3}}>{m.kind}</small><b style={{fontSize:13,fontWeight:500}}>{m.title}</b></button>):<p style={{margin:0,padding:"18px 10px",borderTop:"1px solid #eee",color:"#999",fontSize:12,textAlign:"center"}}>暂无可发送文件</p>}
   </div>}

   {!typing[id]&&(quick[id]||[]).length>0&&<div style={{flex:"0 0 auto",display:"flex",gap:8,flexWrap:"wrap",padding:"9px 14px 0",background:"#f7f7f7"}}>{(quick[id]||[]).map(item=><button key={item.id} onClick={()=>sendQuick(item)} style={{maxWidth:"100%",padding:"7px 11px",border:"1px solid #cfd8d2",borderRadius:15,background:"#fff",color:"#3c6250",fontSize:12,textAlign:"left"}}>{item.text}</button>)}</div>}

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
