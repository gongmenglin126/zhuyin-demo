import {
  chats,
  history,
  posts as flowPosts,
  privateEntries as flowPrivateEntries,
  profile as flowProfile,
} from "./gameDataFlow";
import type {Attachment,Post,PrivateEntry,Reply} from "./gameDataFlow";

export type {Attachment,Post,PrivateEntry,Reply};
export {chats,history};

const reply=(user:string,time:string,text:string,role?:string):Reply=>({user,time,text,role});

const dreamBase=flowPosts.find(post=>post.id==="20847")!;
const dreamPost:Post={
  ...dreamBase,
  terms:(dreamBase.terms||[]).map(term=>term==="红色糖盒"?"红铁皮盒":term),
  highlights:(dreamBase.highlights||[]).map(mark=>mark==="红色铁皮糖盒"?"红铁皮盒":mark),
  body:dreamBase.body.map((text,index)=>index===2?text.replace("红色铁皮糖盒","红铁皮盒"):text),
  replies:dreamBase.replies.map(item=>({...item,text:item.text.replace("红铁皮糖盒","红色盒子")})),
};

const redBoxBase=flowPosts.find(post=>post.id==="30177")!;
const redBoxPost:Post={
  ...redBoxBase,
  terms:[...(redBoxBase.terms||[]),"红铁皮盒","一格胶片","旧厂房"],
  highlights:[...new Set([...(redBoxBase.highlights||[]),"红铁皮盒","打开前会卡一下"])],
  replies:[
    ...redBoxBase.replies,
    reply("一格胶片","23:18","这种红色套盖铁皮盒以前太常见了，地方糕点、茶叶、糖果都装，光看颜色认不出牌子。我前阵子拍旧厂房时好像见过一个形制很像的，当时没特意拍。下次再碰到我帮你留意盒盖边缘。"),
    reply("候鸟第七年","23:31","麻烦了。主要想确认这种东西是不是现实里真常见，不急。","楼主"),
  ],
};

const cottonBase=flowPosts.find(post=>post.id==="33897")!;
const cottonYard:Post={
  ...cottonBase,
  author:"一格胶片",
  date:"2026-07-09 22:14",
  excerpt:"岚棉三厂旧家属区的一组窗户和走廊照片。评论里有老住户补充旧房型。",
  terms:["岚棉三厂","旧址","家属区","4栋","窗户","走廊","寻人启事"],
  highlights:["岚棉三厂","4栋","寻人启事"],
  body:[
    "上周路过岚棉三厂旧家属区，拍了几张还没封死的外墙和窗户。主要想留老单位房改造前后的样子，不做灵异讨论。",
    "第二组是4栋东侧。能看见走廊窗和厨房外墙，部分门窗应该后来换过。第二张窗边还压着一个红色盒子，看着像旧住户留下的杂物。",
    "如果有以前住过这里的人，欢迎补充哪几年改过窗、厨房门和公共走廊。"
  ],
  replies:[
    reply("胶卷过期","22:37","第二张右下角那个红色铁皮盒挺显眼，是你摆的吗？"),
    reply("一格胶片","22:49","不是，隔着窗拍到的。我拍的是窗和房型，没进去动东西。","楼主"),
    reply("三厂老住户","07-10 09:18","4栋我小时候住过。你第二张应该就是东侧那排，厨房门确实往走廊开。"),
    reply("候鸟第七年","07-10 09:42","请问这种门和窗大概是哪几年改的？我最近在核一个老房型。"),
    reply("三厂老住户","07-10 10:03","具体年份记不清了。只记得04年暑假这边贴过一阵寻人启事，我妈还帮着贴过。后来听说孩子找回来了。"),
    reply("候鸟第七年","07-10 10:16","是4栋这边的孩子吗？"),
    reply("三厂老住户","07-10 10:31","哪栋我真记不清了，隔太久。反正就是这片家属区。"),
    reply("旧纸鸢","07-10 11:08","我记得站里以前有人专门问过那张寻人启事，帖子应该还在，就是标题很普通。"),
  ],
};

const posterMemory:Post={
  id:"18362",
  title:"有人还记得小时候三厂家属区楼下贴过的那张寻人启事吗",
  author:"旧电扇",
  date:"2013-09-07 20:18",
  board:"旧闻考据",
  views:1638,
  hidden:true,
  excerpt:"老住户回忆小时候楼下贴过很久的一张寻人启事，只想确认是不是自己记错了年份。",
  terms:["寻人启事","三厂家属区","旧报","04年","暑假"],
  highlights:["寻人启事","04 年暑假","报刊索引"],
  body:[
    "小时候住三厂家属区，印象里有一年暑假楼道口和小卖部门口贴了很久一张寻人启事。后来好像听大人说孩子找回来了。",
    "最近和家里聊旧厂的事又想起来，但我已经分不清是03年还是04年，也记不得孩子叫什么。有没有老住户记得？",
    "不是要找当事人，就是想确认这段记忆到底有没有发生过。"
  ],
  replies:[
    reply("旧纸鸢","20:41","我也记得，应该更接近04年暑假。名字我完全没印象。"),
    reply("报刊索引","21:06","我以前整理过那几年岚州地方报的儿童寻人版，索引帖还在我账号的公开发言里。标题没写厂名，这帖也没有附件。"),
    reply("折柳","21:19","口述年份可能会漂，既然有原报索引就以原报为准，不必继续靠记忆补。"),
    reply("旧电扇","21:33","行，那我去翻你的历史。谢谢。","楼主"),
  ],
};

const scriptureComparePost:Post={
  id:"11208",
  title:"求辨《三门疏》流传页：黑底红字那张其实不是同一篇吧",
  author:"旧纸鸢",
  date:"2016-04-03 21:17",
  board:"旧闻考据",
  views:1864,
  hidden:true,
  excerpt:"一个旧转载包里混着两种完全不同的页面：黑底反相页和白纸抄本。来源字段都已经丢了。",
  terms:["三门疏","身非我身","名非我名","黑底红字","白纸抄本","残页"],
  highlights:["身非我身，名非我名","《三门疏》","不是同一批扫描","来源字段都缺了"],
  body:[
    "前几年存过一个民俗资料转载包，最近整理硬盘才发现里面其实混了两种东西。",
    "一类是反相处理过的黑底页面，最清楚的只有“身非我身，名非我名”反复出现；另一类是普通白纸抄本，边角有一页能看见《三门疏》三个字。",
    "两类文件的分辨率、压缩方式和编号都不一样，我倾向于不是同一批扫描，只是后来被人塞进了同一个压缩包。",
    "原网页已经没了，两个目录里的来源字段也都缺了。想问问有没有人见过更早的转载，至少能确认它们最初是不是一起出现的。"
  ],
  replies:[
    reply("旧档员-03","21:46","站内 2012 年前的附件索引不全，我只能确认这两组文件曾经在不同主题里出现过，原附件已失效。","版主"),
    reply("纸页边角","22:08","如果文件编号和压缩方式都不同，我不会先当成一篇。可能只是后来的整理者觉得内容像，顺手放一起了。"),
    reply("旧纸鸢","22:21","我也是这个意思。先把两组分开记，等找到更早来源再说。","楼主")
  ],
};

const reportBase=flowPosts.find(post=>post.id==="09114")!;
const linNanReport:Post={
  ...reportBase,
  author:"报刊索引",
  title:"【旧报摘录】九岁女童失踪十三日后异地找回",
  excerpt:"2004 年岚州地方报纸索引。姓名、年龄、失踪和找回日期完整。",
  terms:["2004","九岁","女童","姓林","林楠","十三天","失踪","找回","7月18日","7月31日"],
  highlights:["2004-07-18","九岁女童林楠","十三天后","2004-07-31","无法完整说明失踪期间经历"],
  body:[
    "岚州地方文献室索引：2004-07-18，九岁女童林楠在东浦区一处老厂职工宿舍附近失踪，家属当日报警，并在次日地方报刊登寻人信息。",
    "2004-07-31 的后续简讯记载，林楠在外市旧客运站附近被找到，距离失踪十三天。",
    "简讯只写到身体无明显外伤、意识清醒，但无法完整说明失踪期间经历。原报没有刊登后续采访。",
    "本条为旧报索引摘录；旧索引没有录入宿舍所属厂名。"
  ],
};

// 首页上的普通旧报不能提前命中“寻人启事”。
const wallBase=flowPosts.find(post=>post.id==="34049")!;
const wallPost:Post={
  ...wallBase,
  body:wallBase.body.map(text=>text.replace("天气和寻人启事","天气和商场促销")),
  highlights:(wallBase.highlights||[]).map(mark=>mark==="天气和寻人启事"?"天气和商场促销":mark),
};

// 这个真实案例留到“名字不对 / 另一个家”阶段再被搜到，不抢“寻人启事”入口。
const returnedBase=flowPosts.find(post=>post.id==="14692")!;
const returnedCase:Post={
  ...returnedBase,
  terms:(returnedBase.terms||[]).filter(term=>term!=="寻人启事"),
  highlights:(returnedBase.highlights||[]).filter(mark=>mark!=="寻人启事"),
  replies:[
    ...returnedBase.replies.map(item=>({...item,text:item.text.replace(/寻人启事/g,"当年的寻人材料")})),
    reply("照骨","2020-01-13 00:18","回来以后除了名字和另一个家，有没有突然怕以前不怕的东西，或者以前会做、后来突然不会的事？没有也可以写没有。"),
    reply("夜班公交","00:31","@照骨 你这套问题我是不是在别的走失帖也见过？有点眼熟。"),
    reply("照骨","00:44","类似自述我都按差不多的顺序问，免得把几种变化混成一个。"),
  ],
};

const julyBase=flowPosts.find(post=>post.id==="10731")!;
const julyArchive:Post={
  ...julyBase,
  title:"2004 年 7 月两地地方报转载来源求考",
};

const traumaBase=flowPosts.find(post=>post.id==="17428")!;
const traumaCase:Post={
  ...traumaBase,
  replies:[
    ...traumaBase.replies,
    reply("纸页边角","19:14","折柳这个 ID 我好像在另一个走失帖也见过。你很关注这种帖子？"),
    reply("折柳","19:22","旧闻区类似问题不少。原则一样：事实是真的，不代表原因就自动成立。"),
    reply("照骨","19:41","除了香菜，还有没有觉得名字不对、认错家，或者突然不会以前会的东西？没有也算信息。"),
    reply("雨衣口袋","19:53","这些都没有。就是香菜，其他生活一直正常。","楼主"),
  ],
};

const patched=flowPosts.map(post=>
  post.id==="33897"?cottonYard:
  post.id==="09114"?linNanReport:
  post.id==="20847"?dreamPost:
  post.id==="30177"?redBoxPost:
  post.id==="34049"?wallPost:
  post.id==="14692"?returnedCase:
  post.id==="10731"?julyArchive:
  post.id==="17428"?traumaCase:
  post
);

const toRank=(date:string)=>{
  const full=date.match(/(20\d{2})-(\d{2})-(\d{2})(?:\s+(\d{2}):(\d{2}))?/);
  if(full)return Number(full[1])*1e8+Number(full[2])*1e6+Number(full[3])*1e4+Number(full[4]||0)*100+Number(full[5]||0);
  const md=date.match(/(\d{1,2})月(\d{1,2})日(?:\s+(\d{1,2}):(\d{2}))?/);
  if(md)return 2026e8+Number(md[1])*1e6+Number(md[2])*1e4+Number(md[3]||0)*100+Number(md[4]||0);
  if(date.includes("今天"))return 202610170000;
  if(date.includes("昨天"))return 202610160000;
  return 0;
};

export const posts:Post[]=[...patched,posterMemory,scriptureComparePost].sort((a,b)=>toRank(a.date)-toRank(b.date));

export const privateEntries:PrivateEntry[]=flowPrivateEntries
  .filter(entry=>entry.id!=="p2")
  .map(entry=>{
    if(entry.id==="p1")return {
      ...entry,
      highlights:(entry.highlights||[]).map(mark=>mark==="红色铁皮糖盒"?"红铁皮盒":mark),
      body:entry.body.map((text,index)=>index===0?text.replace("红色铁皮糖盒","红铁皮盒"):text),
    };
    if(entry.id==="p3")return {
      ...entry,
      title:"9月11日，几条旧帖",
      highlights:["名字不对","另一个家","回来以后不会以前会的东西了","某种味道"],
      body:[
        "这两个月陆续存了几条。旧报、报警回执、当年的寻人材料能对上的我才留，剩下的先删了。",
        "有的人回来以后只是突然讨厌某种味道；也有人原话就是‘名字不对’、‘我记得另一个家’、‘回来以后不会以前会的东西了’。单看都能解释，挨着放又有点怪。",
        "我把年龄、走失多久、找回后的第一条异常和出处记在一张表里。今晚先到这，眼睛疼。"
      ],
    };
    return entry;
  });

export const profile={
  ...flowProfile,
  topics:flowProfile.topics.filter(id=>posts.some(post=>post.id===id&&post.author==="候鸟第七年")),
};
