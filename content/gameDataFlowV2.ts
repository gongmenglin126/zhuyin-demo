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
    reply("一格胶片","23:18","这种红色套盖铁皮盒以前太常见了，地方糕点、茶叶、糖果都装，光看颜色认不出牌子。我上个月拍岚州一处旧厂房时，窗边也有个形制很像的。"),
    reply("候鸟第七年","23:31","有侧面或者盒盖边缘吗？我想确认是不是套盖。","楼主"),
    reply("一格胶片","23:44","原图里只能看到一角，我主要拍窗和走廊。那组照片我发过站里，没特写盒子。"),
  ],
};

const cottonBase=flowPosts.find(post=>post.id==="33897")!;
const cottonYard:Post={
  ...cottonBase,
  author:"一格胶片",
  date:"2026-07-09 22:14",
  excerpt:"岚棉三厂旧家属区的一组窗户和走廊照片。评论里有老住户补充旧房型。",
  terms:["岚棉三厂","旧址","家属区","4栋","窗户","走廊","红铁皮盒","寻人启事"],
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

const patched=flowPosts.map(post=>post.id==="33897"?cottonYard:post.id==="09114"?linNanReport:post.id==="20847"?dreamPost:post.id==="30177"?redBoxPost:post);

const toRank=(date:string)=>{
  const full=date.match(/(20\d{2})-(\d{2})-(\d{2})(?:\s+(\d{2}):(\d{2}))?/);
  if(full)return Number(full[1])*1e8+Number(full[2])*1e6+Number(full[3])*1e4+Number(full[4]||0)*100+Number(full[5]||0);
  const md=date.match(/(\d{1,2})月(\d{1,2})日(?:\s+(\d{1,2}):(\d{2}))?/);
  if(md)return 2026e8+Number(md[1])*1e6+Number(md[2])*1e4+Number(md[3]||0)*100+Number(md[4]||0);
  if(date.includes("今天"))return 202610170000;
  if(date.includes("昨天"))return 202610160000;
  return 0;
};

export const posts:Post[]=[...patched,posterMemory].sort((a,b)=>toRank(a.date)-toRank(b.date));

export const privateEntries:PrivateEntry[]=flowPrivateEntries
  .filter(entry=>entry.id!=="p2")
  .map(entry=>entry.id!=="p1"?entry:{
    ...entry,
    highlights:(entry.highlights||[]).map(mark=>mark==="红色铁皮糖盒"?"红铁皮盒":mark),
    body:entry.body.map((text,index)=>index===0?text.replace("红色铁皮糖盒","红铁皮盒"):text),
  });

export const profile={
  ...flowProfile,
  topics:flowProfile.topics.filter(id=>posts.some(post=>post.id===id&&post.author==="候鸟第七年")),
};
