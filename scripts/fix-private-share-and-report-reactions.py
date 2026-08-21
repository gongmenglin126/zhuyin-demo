from pathlib import Path

root=Path('.')
p=root/'app/InteractiveWechat.tsx'
s=p.read_text(encoding='utf-8')

old=''' "09114":{yq:[{text:"林楠？"},{text:"没听她提过。"}],zc:[],ly:[{text:"林楠？"},{text:"不认识。"},{text:"沈妍怎么会查到她的？"}]},\n "09831":{zc:[],ly:[{text:"这是沈妍？"},{text:"她没跟我说过小时候这件事。"}]},'''
new=''' "09114":{yq:[{text:"林楠？"},{text:"没听她提过。"}],zc:[{text:"不认识。"},{text:"……你为什么在找这个？"},{text:"这跟沈妍有关系吗？"}],ly:[{text:"林楠？"},{text:"不认识。"}]},\n "09831":{zc:[{text:"这是沈妍小时候？"},{text:"她从来没提过。"}],ly:[{text:"这是沈妍？"},{text:"她没跟我说过小时候这件事。"}]},'''
if old not in s: raise SystemExit('material rule block not found')
s=s.replace(old,new,1)

anchor=''' "private-p3":{yq:null,zc:[{text:"她把这些都存一起了？"},{text:"里面那个“突然不吃某种味道”我有印象。"},{text:"有篇旧帖就这样。"},{material:ordinaryChangePost},{text:"好像就是这个。"}],ly:[{text:"“另一个家”这几个字我见过。"},{text:"有个旧帖里也这么写。"},{material:returnedPost},{text:"我以前看过，不一定是一回事。"}]},'''
insert=anchor+'''\n "private-p4":{yq:null,zc:[{text:"她连这个也记下来了？"},{text:"这篇比前面的梦境记录具体多了。"}],ly:[{text:"前面的记录还只是一些零碎的梦。"},{text:"这篇突然清楚了很多。"}]},'''
if anchor not in s: raise SystemExit('private-p3 anchor not found')
s=s.replace(anchor,insert,1)

old_dyn=''' if(contactId==="zc"&&materialId==="09114"){\n  if(received("zc","09831"))return [{text:"等等。"},{text:"这条也是九岁？"},{text:"也是十三天。"},{text:"日期还挨着……这也太巧了。"}];\n  return [{text:"林楠？"},{text:"这个名字她没跟我说过。"},{text:"九岁，失踪十三天。挺久的。"}];\n }\n if(contactId==="zc"&&materialId==="09831"){\n  if(received("zc","09114"))return [{text:"这是沈妍？"},{text:"等会儿，林楠那条也是九岁。"},{text:"都是十三天？"},{text:"这也太巧了。"}];\n  return [{text:"这是沈妍小时候？"},{text:"她从来没提过。"}];\n }'''
new_dyn=''' if(contactId==="ly"&&materialId==="09114"&&received("ly","09831")){\n  return [{text:"等等。"},{text:"这条也是九岁？"},{text:"也是十三天。"},{text:"日期还挨着……这也太巧了。"}];\n }'''
if old_dyn not in s: raise SystemExit('old report dynamic block not found')
s=s.replace(old_dyn,new_dyn,1)
p.write_text(s,encoding='utf-8')

q=root/'content/wechatLiveDialogues.ts'
w=q.read_text(encoding='utf-8')
marker='''  "不认识。":"不认识。",'''
addition='''  "不认识。":"不认识。",\n  "……你为什么在找这个？":"……你为什么在找这个？",\n  "这跟沈妍有关系吗？":"这跟沈妍有关系吗？",'''
if marker not in w: raise SystemExit('wechat dialogue marker not found')
w=w.replace(marker,addition,1)
marker2='''  "她把这些都存一起了？":"她把这些都整理到一起了？",'''
addition2='''  "她把这些都存一起了？":"她把这些都整理到一起了？",\n  "她连这个也记下来了？":"她连这个也记下来了？",\n  "这篇比前面的梦境记录具体多了。":"这篇比前面的梦境记录具体多了。",\n  "前面的记录还只是一些零碎的梦。":"前面的记录还只是一些零碎的梦。",\n  "这篇突然清楚了很多。":"这篇突然清楚了很多。",'''
if marker2 not in w: raise SystemExit('private dialogue marker not found')
w=w.replace(marker2,addition2,1)
q.write_text(w,encoding='utf-8')
print('patched private-p4 sharing and conditional report reactions')
