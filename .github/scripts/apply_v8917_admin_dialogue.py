from pathlib import Path

p=Path('app/InteractiveWechat.tsx')
s=p.read_text(encoding='utf-8')
old='"27614":{zc:[{text:"对，就是这篇。"},{text:"当时大家最后都当普通值班号看了。"}],ly:[{text:"我以前没点进去看过。"}]},'
new='"27614":{zc:[{text:"这篇我有印象。"},{text:"站务后来不是说多人轮用吗。"}],ly:[{text:"我以前没点进去看过。"}]},'
if old not in s: raise SystemExit('missing 27614 material reply')
s=s.replace(old,new,1)
old2='if(contactId==="zc"&&materialId==="27614")return [{id:"zc-admin-doubt",text:"多人轮用能解释它为什么到处出现吗？",reply:[{text:"能解释一部分。"},{text:"但如果你说的那几篇刚好都是同一类走失和旧抄本，我也会觉得巧得有点过头。"},{text:"我没有后台权限，只能看到公开操作记录。"}]}];'
new2='if(contactId==="zc"&&materialId==="27614")return [{id:"zc-admin-repeat",text:"但我刚才查的几篇里都有这个号。",reply:[{text:"哪几篇？"},{text:"你前面发我的那两条旧报里也有？"},{text:"……那确实挺巧。"}]}];'
if old2 not in s: raise SystemExit('missing 27614 quick reply')
s=s.replace(old2,new2,1)
p.write_text(s,encoding='utf-8')
assert '你是觉得旧档员-03有问题' not in s
assert '多人轮用能解释它为什么到处出现吗' not in s
print('admin dialogue naturalized')
