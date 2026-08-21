// 微信历史聊天文案集中区。
//
// 你以后想把台词改得更“像人”，优先改这个文件即可。
// - id：程序识别联系人用，尽量不要改。
// - name：联系人显示名，可以改。
// - note：微信联系人备注/副标题，可以改。
// - preview：微信左侧会话列表里的“最近消息摘要”，不会作为聊天气泡发出来。
// - time：聊天里的时间分隔，可以改。
// - text：真正显示在聊天气泡里的台词，放心改中文内容。
//
// 注意：尽量只改引号里的文字，不要删掉逗号、括号、引号等代码符号。

export type WechatDialogueMessage={
  time?:string;
  who:"沈妍"|"对方";
  text:string;
};

export type WechatDialogueContact={
  id:string;
  name:string;
  note:string;
  preview:string;
  signature?:string;
  messages:WechatDialogueMessage[];
};

export const WECHAT_CONTACTS:WechatDialogueContact[]=[
 {id:"x",name:"徐宁",note:"小学同学",preview:"我去你家看看",messages:[
  {time:"10月16日 11:26",who:"对方",text:"明天中午还是老地方？"},{who:"沈妍",text:"嗯嗯，想你了"},{who:"对方",text:"你别又把我鸽咯，大忙人"},{who:"沈妍",text:"这次真不会啦，放心~"},{who:"对方",text:"我已截图为证"},{who:"沈妍",text:"随便截"},{time:"10月16日 19:48",who:"沈妍",text:"我晚上得出去一趟"},{who:"沈妍",text:"明天有个事情跟你说"},{who:"对方",text:"这么神秘"},{who:"沈妍",text:"这个事情纠缠我很久啦，我希望今天晚上有个结果"},{who:"对方",text:"好，明天听你好消息"},{time:"今天 12:02",who:"对方",text:"我到了"},{who:"对方",text:"你人呢"},{time:"今天 12:37",who:"对方",text:"电话也不接，你还好吗？？"},{time:"今天 18:37",who:"对方",text:"我去你家看看"},
 ]},
 {id:"yq",name:"余晴",note:"余晴｜朋友介绍",preview:"嗯",messages:[
  {time:"10月16日 18:52",who:"对方",text:"我先到了"},{who:"沈妍",text:"这么早"},{who:"对方",text:"我们约的七点呀"},{who:"沈妍",text:"路上，十分钟"},{who:"对方",text:"还是最里面那桌"},{who:"沈妍",text:"好"},{time:"10月16日 19:17",who:"对方",text:"看见你了"},{who:"沈妍",text:"别起来，我过去"},{time:"10月16日 20:46",who:"对方",text:"你不吃了？"},{who:"沈妍",text:"胃不太舒服"},{who:"对方",text:"那我给你打包？"},{who:"沈妍",text:"不用"},{time:"10月16日 21:03",who:"对方",text:"到家说一声"},{who:"沈妍",text:"嗯"},
 ]},
 {id:"zc",name:"周川",note:"周川｜烛阴旧闻",preview:"那说明阿姨说的对。",messages:[
  {time:"10月12日 22:08",who:"对方",text:"你还在被你的梦困扰？"},{who:"沈妍",text:"你看到我的帖子了？"},{who:"对方",text:"首页挂着呢。"},{who:"沈妍",text:"好吧，有点尴尬哈哈"},{who:"对方",text:"还行，多倾诉一点方便我帮你解梦。"},{who:"沈妍",text:"我谢谢您嘞"},{who:"对方",text:"你说有没有可能你是把电影的记忆记成你自己的了？"},{who:"沈妍",text:"我也不清楚，但是这些片段太真实，声音太清晰，我无法忽视..."},{who:"对方",text:"理解，我支持你。"},{who:"沈妍",text:"谢谢你一直陪着我"},{who:"对方",text:"今天别想那么多了，早点睡吧。"},{who:"沈妍",text:"你怎么跟我妈一个口气"},{who:"对方",text:"那说明阿姨说的对。"},
 ]},
 {id:"ly",name:"梁茵",note:"梁茵｜烛阴旧闻",preview:"这也要跟我报备嘛",messages:[
  {time:"9月28日 00:42",who:"对方",text:"又有人私信我"},{who:"沈妍",text:"怎么说？"},{who:"对方",text:"我早晚要把迟迟这个号注销"},{who:"对方",text:"他把我帖子里每句话都拿出来详细展开问我"},{who:"沈妍",text:"噗"},{who:"对方",text:"我是有点记忆不好，也没必要把我当犯人审问吧，好不适"},{who:"沈妍",text:"这个论坛是神人有点多，我之前也被经常问"},{who:"对方",text:"他们闲得慌，关注我的日常干啥"},{who:"沈妍",text:"感觉在记录我们的生活一样"},{who:"对方",text:"是呀"},{who:"沈妍",text:"你别理他了"},{who:"对方",text:"已经拉黑了"},{who:"对方",text:"早知道不发帖子了"},{who:"沈妍",text:"你不发我俩也不会认识"},{who:"对方",text:"那倒也是"},
 ]},
];
