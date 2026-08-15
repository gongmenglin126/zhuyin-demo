import {
  chats,
  history,
  posts as flowPosts,
  privateEntries,
  profile,
} from "./gameDataFlow";
import type {Attachment,Post,PrivateEntry,Reply} from "./gameDataFlow";

export type {Attachment,Post,PrivateEntry,Reply};
export {chats,history,privateEntries,profile};

const reply=(user:string,time:string,text:string,role?:string):Reply=>({user,time,text,role});

const cottonBase=flowPosts.find(post=>post.id==="33897")!;
const cottonYard:Post={
  ...cottonBase,
  author:"一格胶片",
  date:"2026-07-09 22:14",
  excerpt:"岚棉三厂旧家属区的一组窗户和走廊照片。评论里有老住户补充旧房型。",
  terms:["岚棉三厂","旧址","家属区","4栋","窗户","走廊","2004","走失","姓林","九岁"],
  highlights:["岚棉三厂","4栋","2004 年","孩子走失","九岁","姓林"],
  body:[
    "上周路过岚棉三厂旧家属区，拍了几张还没封死的外墙和窗户。主要想留老单位房改造前后的样子，不做灵异讨论。",
    "第二组是4栋东侧。能看见走廊窗和厨房外墙，部分门窗应该后来换过。",
    "如果有以前住过这里的人，欢迎补充哪几年改过窗、厨房门和公共走廊。"
  ],
  replies:[
    reply("三厂老住户","07-10 09:18","4栋我小时候住过。你第二张应该就是东侧那排，厨房门确实往走廊开。"),
    reply("候鸟第七年","07-10 09:42","请问这种门和窗大概是哪几年改的？我最近在核一个老房型。"),
    reply("三厂老住户","07-10 10:03","具体年份记不清，只记得2004年这边出过一次孩子走失，我妈当年还帮着贴过寻人启事。"),
    reply("候鸟第七年","07-10 10:16","这个现在还能查到旧报吗？"),
    reply("三厂老住户","07-10 10:31","市图应该能查。印象里是个九岁左右的小女孩，姓林，后来找回来了。名字我是真想不起来。"),
    reply("旧纸鸢","07-10 11:08","岚州2004年的地方报还有缩微索引。年份、年龄、姓氏这些比猜名字好用。"),
  ],
};

const reportBase=flowPosts.find(post=>post.id==="09114")!;
const linNanReport:Post={
  ...reportBase,
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

const patched=flowPosts.map(post=>post.id==="33897"?cottonYard:post.id==="09114"?linNanReport:post);

const toRank=(date:string)=>{
  const full=date.match(/(20\d{2})-(\d{2})-(\d{2})(?:\s+(\d{2}):(\d{2}))?/);
  if(full)return Number(full[1])*1e8+Number(full[2])*1e6+Number(full[3])*1e4+Number(full[4]||0)*100+Number(full[5]||0);
  const md=date.match(/(\d{1,2})月(\d{1,2})日(?:\s+(\d{1,2}):(\d{2}))?/);
  if(md)return 2026e8+Number(md[1])*1e6+Number(md[2])*1e4+Number(md[3]||0)*100+Number(md[4]||0);
  if(date.includes("今天"))return 202610170000;
  if(date.includes("昨天"))return 202610160000;
  return 0;
};

export const posts:Post[]=[...patched].sort((a,b)=>toRank(a.date)-toRank(b.date));
