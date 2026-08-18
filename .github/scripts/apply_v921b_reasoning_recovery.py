from pathlib import Path
import re
p=Path('app/InteractiveWechat.tsx')
s=p.read_text()
MARK='// v9.2.1b reasoning recovery'
if MARK in s:
    print('v9.2.1b already applied')
    raise SystemExit(0)
s=s.replace('// v9.2.1 interaction pass','// v9.2.1 interaction pass\n'+MARK,1)
s=s.replace('  activeId:"x",','  activeId:"yq",',1)
s=s.replace('/后来|别人|谁来|还有人|介绍/.test(t)','/后来|别人|谁来|还有人|介绍|交给|转交/.test(t)',1)
start=s.index('const quickAfterMaterial=(contactId:string,materialId:string):QuickReply[]=>{')
end=s.index('\n if(contactId==="ly"&&materialId==="admin-liang-record")return [',start)
head=s[:start]
tail=s[end:]
helpers=r'''const syncReasoningChoices=():QuickReply[]=>{
 const correct:QuickReply={id:"ly-sync-right",text:"林楠第二次易舍，把2004年的另一端也重新影响了？",reply:[{text:"我也是这么对上的。"},{text:"沈妍不是第二次试验的目标，她是旧对契重新有反应以后被控制的。"},{text:"现在得找她被转到哪。"}]};
 const wrongAgain:QuickReply={id:"ly-sync-wrong-again",text:"所以他们也准备再给沈妍换一次？",reply:[{text:"可沈妍那份写的是‘控制旧对契另一端’，不是再舍对象。"}]};
 const wrongForum:QuickReply={id:"ly-sync-forum",text:"还是因为沈妍查论坛查得太深？",reply:[{text:"他们当然一直监控她。"},{text:"但这份处置理由写的是同步异常，不是论坛行为。"}]};
 wrongAgain.next=[correct,wrongForum];wrongForum.next=[wrongAgain,correct];
 return [wrongAgain,correct,wrongForum];
};
const reswapReasoningChoices=(includeSync:boolean):QuickReply[]=>{
 const correct:QuickReply={id:"ly-reswap-test",text:"他们在测试同一个魂能不能连续换身体？",reply:[{text:"对。"},{text:"稳定22年、再次易舍、主体稳定——这几个字段放一起就是这个意思。"}],next:includeSync?syncReasoningChoices():[]};
 const wrongShen:QuickReply={id:"ly-reswap-shen",text:"他们是想接着给沈妍也换一次？",reply:[{text:"但这份执行对象写的是B侧和19-07。"},{text:"沈妍不在这次执行名单里。"}]};
 const wrongRepeat:QuickReply={id:"ly-reswap-repeat",text:"只是把2004年的仪式重新做一遍？",reply:[{text:"不太像。"},{text:"这次特意写‘长期样本’和‘第二次更换舍’，目的变了。"}]};
 wrongShen.next=[correct,wrongRepeat];wrongRepeat.next=[wrongShen,correct];
 return [wrongShen,correct,wrongRepeat];
};
const pairReasoningChoices=():QuickReply[]=>{
 const nextAfterCorrect:QuickReply[]=received("ly","admin-reswap-2026")?reswapReasoningChoices(received("ly","admin-sync-shen")):[{id:"ly-pair-why",text:"那既然换过了，为什么现在又抓沈妍？",reply:[{text:"对。这个才是现在的问题。"},{text:"2004那份解释不了2026。得看林楠后来又发生了什么。"}]}];
 const correct:QuickReply={id:"ly-pair-swap",text:"舍是身体，客是魂……所以她们互换了？",reply:[{text:"……我也是这么看的。"},{text:"那‘易舍’就是换魂。"}],next:nextAfterCorrect};
 const wrongLink:QuickReply={id:"ly-pair-link",text:"只是两个人的档案互相挂靠？",reply:[{text:"可A、B两边都写了‘易舍完成’。"},{text:"只做档案关联没必要写客源。"}]};
 const wrongHeld:QuickReply={id:"ly-pair-held",text:"也可能只是两个人一起被关过？",reply:[{text:"可能，但还是解释不了为什么‘客源’互相写对方。"},{text:"我会先把‘舍’和‘客’的意思对上。"}]};
 wrongLink.next=[correct,wrongHeld];wrongHeld.next=[wrongLink,correct];
 return [wrongLink,correct,wrongHeld];
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
 if(contactId==="ly"&&materialId==="admin-third-1907")return [{id:"ly-third-identity",text:"她还要求联系徐宁。",reply:[{text:"……"},{text:"那就不能只当身份混乱看了。"},{text:"真找到地点，这个人也得告诉警方。"}]}];
'''
s=head+helpers+tail
p.write_text(s)
print('Applied v9.2.1b reasoning recovery')
