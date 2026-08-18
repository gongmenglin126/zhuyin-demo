from pathlib import Path
p=Path('app/InteractiveWechat.tsx')
s=p.read_text()
MARK='// v9.2.2b WeChat hard lock'
if MARK in s:
    print('hard lock already applied')
    raise SystemExit(0)
s=s.replace('// v9.2.2 controlled WeChat\n','// v9.2.2 controlled WeChat\n'+MARK+'\n',1)

old=''' const sendable=useMemo(()=>id==="x"||!introduced[id]?[]:materials.filter(m=>Object.prototype.hasOwnProperty.call(materialRules[m.id]||{},id)&&!sent[`${id}:${m.id}`]),[materials,id,sent,introduced]);'''
new=''' const sendable=useMemo(()=>id==="x"||!introduced[id]?[]:materials.filter(m=>{const rules=materialRules[m.id];return !!rules&&Object.prototype.hasOwnProperty.call(rules,id)&&rules[id]!==null&&!sent[`${id}:${m.id}`]}),[materials,id,sent,introduced]);'''
assert old in s
s=s.replace(old,new,1)

s=s.replace('''  const text=draft.trim(); if(!text||!canFreeText)return;''','''  const text=draft.trim(); if(!text||!canFreeText||wechatSession.locked[id]||!wechatSession.freeText[id])return;''',1)
s=s.replace('''  if(!canPickMaterial)return;''','''  if(!canPickMaterial||wechatSession.locked[id])return;''',1)
s=s.replace('''  if(id==="x"||actionLocked)return;''','''  if(id==="x"||actionLocked||wechatSession.locked[id])return;''',1)

old=''' useEffect(()=>setPicker(false),[id]);'''
new=''' useEffect(()=>{setPicker(false);setDraft("")},[id]);'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)
print('Applied v9.2.2b WeChat hard lock safeguards')
