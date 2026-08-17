from pathlib import Path
p=Path('app/InteractiveWechat.tsx')
s=p.read_text(encoding='utf-8')
old='if(contactId==="zc"&&materialId==="27614")return [{id:"zc-admin-repeat",text:"但我刚才查的几篇里都有这个号。",reply:[{text:"哪几篇？"},{text:"你前面发我的那两条旧报里也有？"},{text:"……那确实挺巧。"}]}];'
new='''if(contactId==="zc"&&materialId==="27614"){
  const hasBothReports=received("zc","09114")&&received("zc","09831");
  return [{id:"zc-admin-repeat",text:"但我刚才查的几篇里都有这个号。",reply:hasBothReports?[{text:"等等。"},{text:"你前面发我的那两条旧报，也是它恢复的？"},{text:"……这么放一起确实挺巧。"}]:[{text:"哪几篇？"},{text:"你把链接留着，我也翻翻。"}]}];
 }'''
if old not in s: raise SystemExit('missing admin quick reply')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('admin context reply patched')
