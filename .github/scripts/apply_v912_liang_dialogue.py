from pathlib import Path

p=Path('app/InteractiveWechat.tsx')
s=p.read_text(encoding='utf-8')

old=''' "admin-liang-record":{ly:[{text:"操。"},{text:"真的是我。"},{text:"你先别往下猜，最早那条是什么时候？"}],zc:[{text:"这是梁茵那份？"},{text:"今天18:42还在自动刷新，说明这系统现在还在跑。"}]},'''
new=''' "admin-liang-record":{ly:[{text:"操。"},{text:"真的是我。"},{text:"这东西从什么时候开始记我的？"}],zc:[{text:"这是梁茵那份？"},{text:"今天18:42还在自动刷新，说明这系统现在还在跑。"}]},'''
assert old in s
s=s.replace(old,new,1)

old=''' if(contactId==="zc"&&materialId==="27614"){
  const hasBothReports=received("zc","09114")&&received("zc","09831");
  return [{id:"zc-admin-repeat",text:"但我刚才查的几篇里都有这个号。",reply:hasBothReports?[{text:"等等。"},{text:"你前面发我的那两条旧报，也是它恢复的？"},{text:"……这么放一起确实挺巧。"}]:[{text:"哪几篇？"},{text:"你把链接留着，我也翻翻。"}]}];
 }
 return [];
};'''
new=''' if(contactId==="zc"&&materialId==="27614"){
  const hasBothReports=received("zc","09114")&&received("zc","09831");
  return [{id:"zc-admin-repeat",text:"但我刚才查的几篇里都有这个号。",reply:hasBothReports?[{text:"等等。"},{text:"你前面发我的那两条旧报，也是它恢复的？"},{text:"……这么放一起确实挺巧。"}]:[{text:"哪几篇？"},{text:"你把链接留着，我也翻翻。"}]}];
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
};'''
assert old in s
s=s.replace(old,new,1)

old=''' if(contact==="ly"){
  if(/后台|管理系统|管理后台/.test(t))return [{text:"……后台？"},{text:"能查账号吗？"},{text:"那你搜一下我。"},{text:"搜“迟迟”就行。"}];
  if(/有你|搜到你|你的记录|梁茵/.test(t))return [{text:"操"},{text:"真的有？"},{text:"你先别概括。"},{text:"最早那条是什么时候？"}];
  if(/2021|三月|第一次线下接触/.test(t))return [{text:"等一下。"},{text:"2021年三月我确实见过一个论坛里认识的女的。"},{text:"就吃了顿饭。她一直问我小时候走失那阵的事。"},{text:"我当时真以为就是网友聊天。"}];'''
new=''' if(contact==="ly"){
  if(/后台|管理系统|管理后台/.test(t))return [{text:"……后台？"},{text:"能查账号吗？"},{text:"那你搜一下我。"},{text:"搜“迟迟”就行。"}];
  if(/有你|搜到你|你的记录|梁茵/.test(t))return [{text:"操"},{text:"真的有？"},{text:"这东西从什么时候开始记我的？"}];
  if(/2017|最早|加入观察名单/.test(t))return [{text:"2017？"},{text:"我那年才刚开始在论坛里写小时候那些事。"},{text:"所以不是我后来跟沈妍聊上以后，他们才盯我的。"}];
  if(/2021|三月|第一次线下接触/.test(t))return [{text:"等一下。"},{text:"2021年三月我确实见过一个论坛里认识的女的。"},{text:"就吃了顿饭。她一直问我小时候走失那阵的事。"},{text:"我当时真以为就是网友聊天。"}];'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('v9.1.2 Liang dialogue patch applied')
