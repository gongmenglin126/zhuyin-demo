from pathlib import Path

p=Path('app/InteractiveWechat.tsx')
s=p.read_text()
MARK='// v9.2.2 controlled WeChat'
if MARK in s:
    print('v9.2.2 controlled WeChat already applied')
    raise SystemExit(0)

s=s.replace('// v9.2.1b reasoning recovery\n','// v9.2.1b reasoning recovery\n'+MARK+'\n')

old='type QuickReply={id:string;text:string;sendText?:string;emphasis?:boolean;reply:ReplyPart[];next?:QuickReply[]};'
new='type QuickReply={id:string;text:string;sendText?:string;emphasis?:boolean;freeText?:boolean;reply:ReplyPart[];next?:QuickReply[]};'
assert old in s
s=s.replace(old,new,1)

old='''  firstContact:{} as Record<string,string>,\n  zhouEvidenceSeen:false,\n  zhouConfronted:false,'''
new='''  firstContact:{} as Record<string,string>,\n  locked:{} as Record<string,boolean>,\n  freeText:{} as Record<string,boolean>,\n  freeReturn:{} as Record<string,QuickReply[]>,\n  zhouEvidenceSeen:false,\n  zhouConfronted:false,'''
assert old in s
s=s.replace(old,new,1)

old=''' wechatSession.zhouEvidenceSeen=true;\n wechatSession.quick={...wechatSession.quick,zc:[{id:"zc-zheliu",text:"你是折柳？",emphasis:true,reply:[{text:"你在哪看到这个号的？"}],next:[{id:"zc-zheliu-admin",text:"后台。",reply:[{text:"……"},{text:"你现在还在沈妍家？"}],next:[{id:"zc-zheliu-answer",text:"你还没回答我。",reply:[{text:"是。"}],next:[{id:"zc-zheliu-time",text:`我${stamp}才第一次联系你。后台同一分钟就有折柳的记录。`,reply:[{text:"……"},{text:"你先从她家出来。"}],next:[{id:"zc-zheliu-why",text:"为什么？",reply:[{text:"现在别问这个。"},{text:"先出去。"}]}]}]}]}]}]};'''
new=''' wechatSession.zhouEvidenceSeen=true;\n wechatSession.freeText={...wechatSession.freeText,zc:false};\n wechatSession.freeReturn={...wechatSession.freeReturn,zc:[]};\n wechatSession.quick={...wechatSession.quick,zc:[{id:"zc-zheliu",text:"你是折柳？",emphasis:true,reply:[{text:"你在哪看到这个号的？"}],next:[{id:"zc-zheliu-admin",text:"后台。",reply:[{text:"……"},{text:"你现在还在沈妍家？"}],next:[{id:"zc-zheliu-answer",text:"你还没回答我。",reply:[{text:"是。"}],next:[{id:"zc-zheliu-time",text:`我${stamp}才第一次联系你。后台同一分钟就有折柳的记录。`,reply:[{text:"……"},{text:"你先从她家出来。"}],next:[{id:"zc-zheliu-why",text:"为什么？",reply:[{text:"现在别问这个。"},{text:"先出去。"}]}]}]}]}]}]};'''
assert old in s
s=s.replace(old,new,1)

anchor='''const introText=(contactId:string)=>{'''
fallback='''const fallbackReply=(contact:string):ReplyPart[]=>{\n if(contact==="yq")return [{text:"这个我真不知道。"},{text:"你如果是问昨晚的事，可以直接问我。"}];\n if(contact==="zc")return [{text:"这我没法接。"},{text:"你是查到什么了？"}];\n if(contact==="ly")return [{text:"等下，我有点没跟上。"},{text:"你说具体一点，是沈妍还是论坛里的事？"}];\n return [{text:"我不知道。"}];\n};\n\n'''
assert anchor in s
s=s.replace(anchor,fallback+anchor,1)

start=s.index('const introReply=(contactId:string):{parts:ReplyPart[];next:QuickReply[]}=>{')
end=s.index('\n\nexport const triggerAdminWechatBeat=', start)
new_intro='''const introReply=(contactId:string):{parts:ReplyPart[];next:QuickReply[]}=>{\n if(contactId==="yq"){\n  const after:QuickReply={id:"yq-after-person",text:"她后来还见了别人吗？",reply:[{text:"……后来确实有人过来了一下。"},{text:"是之前跟她聊过旧事的一个女的。"},{text:"我跟那个人也不熟，就是以前介绍她们认识。"}]};\n  const when:QuickReply={id:"yq-left-when",text:"你们昨晚几点分开的？",reply:[{text:"我九点左右先走的。"},{text:"21:03那句‘到家说一声’就是我走以后发的。"}],next:[after]};\n  const free:QuickReply={id:"yq-free-intro",text:"自己问一句…",freeText:true,reply:[],next:[when]};\n  return {parts:[{text:"你是徐宁？沈妍提过你。"},{text:"她今天还没回你？昨晚我们确实见过。"}],next:[when,free]};\n }\n if(contactId==="zc"){\n  const recent:QuickReply={id:"zc-recent",text:"她最近跟你说过什么？",reply:[{text:"还是那个梦。"},{text:"她前几天开始觉得里面有人叫‘楠楠’。"},{text:"我让她别半夜一直翻旧帖。"}]};\n  const free:QuickReply={id:"zc-free-intro",text:"自己问一句…",freeText:true,reply:[],next:[recent]};\n  return {parts:[{text:"徐宁？她提过你。"},{text:"她今天一直没回？电话也不通？"}],next:[recent,free]};\n }\n if(contactId==="ly"){\n  const know:QuickReply={id:"ly-how-know",text:"你和沈妍怎么认识的？",reply:[{text:"论坛。"},{text:"我以前发过小时候走失以后的一些事，她私信过我。"},{text:"后来才慢慢聊熟。"}]};\n  const free:QuickReply={id:"ly-free-intro",text:"自己问一句…",freeText:true,reply:[],next:[know]};\n  return {parts:[{text:"徐宁？我知道你，沈妍提过。"},{text:"她怎么了？"}],next:[know,free]};\n }\n return {parts:[],next:[]};\n};'''
s=s[:start]+new_intro+s[end:]

old=''' const [typing,setTyping]=useState<Record<string,boolean>>({});\n const [sent,setSent]=useState<Record<string,boolean>>(()=>({...wechatSession.sent}));\n const [quick,setQuick]=useState<Record<string,QuickReply[]>>(()=>({...wechatSession.quick}));'''
new=''' const [typing,setTyping]=useState<Record<string,boolean>>({});\n const [sent,setSent]=useState<Record<string,boolean>>(()=>({...wechatSession.sent}));\n const [quick,setQuick]=useState<Record<string,QuickReply[]>>(()=>({...wechatSession.quick}));\n const [locked,setLocked]=useState<Record<string,boolean>>(()=>({...wechatSession.locked}));\n const [freeText,setFreeText]=useState<Record<string,boolean>>(()=>({...wechatSession.freeText}));'''
assert old in s
s=s.replace(old,new,1)

old=''' const messages=useMemo(()=>[...contact.messages,...(extra[id]||[])],[contact,extra,id]);\n const previewFor=(c:Contact)=>{const added=extra[c.id]||[];return added.length?added[added.length-1].text:c.preview};\n const sendable=useMemo(()=>id==="x"||!introduced[id]?[]:materials.filter(m=>Object.prototype.hasOwnProperty.call(materialRules[m.id]||{},id)&&!sent[`${id}:${m.id}`]),[materials,id,sent,introduced]);'''
new=''' const messages=useMemo(()=>[...contact.messages,...(extra[id]||[])],[contact,extra,id]);\n const previewFor=(c:Contact)=>{const added=extra[c.id]||[];return added.length?added[added.length-1].text:c.preview};\n const actionLocked=!!locked[id]||!!typing[id];\n const hasQuick=(quick[id]||[]).length>0;\n const canFreeText=id!=="x"&&!!introduced[id]&&!!freeText[id]&&!actionLocked&&!hasQuick;\n const canPickMaterial=id!=="x"&&!!introduced[id]&&!actionLocked&&!hasQuick&&!freeText[id];\n const sendable=useMemo(()=>id==="x"||!introduced[id]?[]:materials.filter(m=>Object.prototype.hasOwnProperty.call(materialRules[m.id]||{},id)&&!sent[`${id}:${m.id}`]),[materials,id,sent,introduced]);'''
assert old in s
s=s.replace(old,new,1)

old=''' const sendIntroduction=(contactId:string)=>{\n  if(contactId==="x"||wechatSession.introduced[contactId])return;\n  const intro=ensureIntro(contactId);\n  appendFor(contactId,intro);\n  const start=introReply(contactId);\n  delayedParts(contactId,start.parts,start.next);\n };\n const setQuickFor=(contactId:string,items:QuickReply[])=>{\n  wechatSession.quick={...wechatSession.quick,[contactId]:items};\n  notifyWechat();\n };'''
new=''' const sendIntroduction=(contactId:string)=>{\n  if(contactId==="x"||wechatSession.introduced[contactId]||wechatSession.locked[contactId])return;\n  setLockedFor(contactId,true);\n  const intro=ensureIntro(contactId);\n  appendFor(contactId,intro);\n  const start=introReply(contactId);\n  delayedParts(contactId,start.parts,start.next);\n };\n const setQuickFor=(contactId:string,items:QuickReply[])=>{\n  wechatSession.quick={...wechatSession.quick,[contactId]:items};\n  notifyWechat();\n };\n const setLockedFor=(contactId:string,value:boolean)=>{\n  wechatSession.locked={...wechatSession.locked,[contactId]:value};\n  notifyWechat();\n };\n const setFreeTextFor=(contactId:string,value:boolean,returnQuick:QuickReply[]=[])=>{\n  wechatSession.freeText={...wechatSession.freeText,[contactId]:value};\n  wechatSession.freeReturn={...wechatSession.freeReturn,[contactId]:returnQuick};\n  notifyWechat();\n };'''
assert old in s
s=s.replace(old,new,1)

old=''' const delayedParts=(contactId:string,parts:ReplyPart[]|null,nextQuick:QuickReply[]=[] )=>{\n  if(!parts?.length){setQuickFor(contactId,nextQuick);return;}'''
new=''' const delayedParts=(contactId:string,parts:ReplyPart[]|null,nextQuick:QuickReply[]=[] )=>{\n  if(!parts?.length){setLockedFor(contactId,false);setQuickFor(contactId,nextQuick);return;}'''
assert old in s
s=s.replace(old,new,1)

old='''    if(index===parts.length-1){setTyping(prev=>({...prev,[contactId]:false}));setQuickFor(contactId,nextQuick)}'''
new='''    if(index===parts.length-1){setTyping(prev=>({...prev,[contactId]:false}));setLockedFor(contactId,false);setQuickFor(contactId,nextQuick)}'''
assert old in s
s=s.replace(old,new,1)

old='''   setSent({...wechatSession.sent});\n   setQuick({...wechatSession.quick});'''
new='''   setSent({...wechatSession.sent});\n   setQuick({...wechatSession.quick});\n   setLocked({...wechatSession.locked});\n   setFreeText({...wechatSession.freeText});'''
assert old in s
s=s.replace(old,new,1)

old=''' const sendText=(e:FormEvent)=>{\n  e.preventDefault();\n  const text=draft.trim(); if(!text||id==="x")return;\n  const intro=ensureIntro(id);\n  appendFor(id,[...intro,{who:"沈妍",text}]);\n  setQuickFor(id,[]);\n  setDraft("");\n  delayedParts(id,textReply(id,text));\n };'''
new=''' const sendText=(e:FormEvent)=>{\n  e.preventDefault();\n  const text=draft.trim(); if(!text||!canFreeText)return;\n  const returnQuick=wechatSession.freeReturn[id]||[];\n  setLockedFor(id,true);\n  setFreeTextFor(id,false,[]);\n  appendFor(id,[{who:"沈妍",text}]);\n  setDraft("");\n  delayedParts(id,textReply(id,text)??fallbackReply(id),returnQuick);\n };'''
assert old in s
s=s.replace(old,new,1)

old=''' const sendMaterial=(material:SharedMaterial)=>{\n  const rules=materialRules[material.id];\n  if(!rules||!Object.prototype.hasOwnProperty.call(rules,id))return;\n  const reply=materialReply(id,material.id);\n  const intro=ensureIntro(id);\n  appendFor(id,[...intro,{who:"沈妍",text:`[分享] ${material.title}`,material}]);'''
new=''' const sendMaterial=(material:SharedMaterial)=>{\n  if(!canPickMaterial)return;\n  const rules=materialRules[material.id];\n  if(!rules||!Object.prototype.hasOwnProperty.call(rules,id))return;\n  setLockedFor(id,true);\n  const reply=materialReply(id,material.id);\n  appendFor(id,[{who:"沈妍",text:`[分享] ${material.title}`,material}]);'''
assert old in s
s=s.replace(old,new,1)

old=''' const sendQuick=(item:QuickReply)=>{\n  if(id==="x")return;\n  setQuickFor(id,[]);\n  appendFor(id,[{who:"沈妍",text:item.sendText||item.text}]);\n  if(item.id==="zc-zheliu")wechatSession.zhouConfronted=true;\n  delayedParts(id,item.reply,item.next||[]);\n };'''
new=''' const sendQuick=(item:QuickReply)=>{\n  if(id==="x"||actionLocked)return;\n  setQuickFor(id,[]);\n  if(item.freeText){setFreeTextFor(id,true,item.next||[]);return;}\n  setLockedFor(id,true);\n  appendFor(id,[{who:"沈妍",text:item.sendText||item.text}]);\n  if(item.id==="zc-zheliu")wechatSession.zhouConfronted=true;\n  delayedParts(id,item.reply,item.next||[]);\n };'''
assert old in s
s=s.replace(old,new,1)

old='''   <header style={{flex:"0 0 auto"}}><b>{contact.name}</b><small>{typing[id]?"正在输入…":contact.note}</small>{contact.signature&&<small style={{display:"block",marginTop:3,color:"#929892",fontSize:10}}>个性签名：{contact.signature}</small>}</header>'''
new='''   <header style={{flex:"0 0 auto"}}><b>{contact.name}</b><small>{actionLocked?"正在回复…":contact.note}</small>{contact.signature&&<small style={{display:"block",marginTop:3,color:"#929892",fontSize:10}}>个性签名：{contact.signature}</small>}</header>'''
assert old in s
s=s.replace(old,new,1)

old='''   {picker&&<div style={{position:"absolute",left:12,right:12,bottom:76,zIndex:8,maxHeight:"42%",overflowY:"auto",padding:8,border:"1px solid #cfcfcf",borderRadius:9,background:"#fff",boxShadow:"0 10px 35px #0003"}}>'''
new='''   {picker&&canPickMaterial&&<div style={{position:"absolute",left:12,right:12,bottom:76,zIndex:8,maxHeight:"42%",overflowY:"auto",padding:8,border:"1px solid #cfcfcf",borderRadius:9,background:"#fff",boxShadow:"0 10px 35px #0003"}}>'''
assert old in s
s=s.replace(old,new,1)

old='''   {!typing[id]&&id!=="x"&&!introduced[id]&&<div style={{flex:"0 0 auto",padding:"10px 14px 0",background:"#f7f7f7"}}><button onClick={()=>sendIntroduction(id)} style={{padding:"8px 13px",border:"1px solid #b9d6c3",borderRadius:16,background:"#fff",color:"#267747",fontSize:12,fontWeight:700}}>先自我介绍</button></div>}\n\n   {!typing[id]&&(quick[id]||[]).length>0&&<div style={{flex:"0 0 auto",display:"flex",gap:8,flexWrap:"wrap",padding:"9px 14px 0",background:"#f7f7f7"}}>{(quick[id]||[]).map(item=><button key={item.id} onClick={()=>sendQuick(item)} style={{maxWidth:"100%",padding:item.emphasis?"9px 14px":"7px 11px",border:item.emphasis?"2px solid #9f3f36":"1px solid #cfd8d2",borderRadius:15,background:item.emphasis?"#fff8f6":"#fff",color:item.emphasis?"#8c3029":"#3c6250",fontSize:12,fontWeight:item.emphasis?800:400,textAlign:"left"}}>{item.text}</button>)}</div>}'''
new='''   {!actionLocked&&id!=="x"&&!introduced[id]&&<div style={{flex:"0 0 auto",padding:"10px 14px 0",background:"#f7f7f7"}}><button onClick={()=>sendIntroduction(id)} style={{padding:"8px 13px",border:"1px solid #b9d6c3",borderRadius:16,background:"#fff",color:"#267747",fontSize:12,fontWeight:700}}>先自我介绍</button></div>}\n\n   {!actionLocked&&(quick[id]||[]).length>0&&<div style={{flex:"0 0 auto",display:"flex",gap:8,flexWrap:"wrap",padding:"9px 14px 0",background:"#f7f7f7"}}>{(quick[id]||[]).map(item=><button key={item.id} onClick={()=>sendQuick(item)} style={{maxWidth:"100%",padding:item.emphasis?"9px 14px":"7px 11px",border:item.emphasis?"2px solid #9f3f36":"1px solid #cfd8d2",borderRadius:15,background:item.emphasis?"#fff8f6":"#fff",color:item.emphasis?"#8c3029":"#3c6250",fontSize:12,fontWeight:item.emphasis?800:400,textAlign:"left"}}>{item.text}</button>)}</div>}'''
assert old in s
s=s.replace(old,new,1)

old='''     <input disabled={id==="x"} value={draft} onChange={e=>setDraft(e.target.value)} placeholder={id==="x"?"":"输入消息"} style={{height:48,border:"1px solid #d0d0d0",borderRadius:8,padding:"0 14px",minWidth:0,fontSize:14}}/>\n     <button type="button" onClick={()=>setPicker(v=>!v)} disabled={id==="x"} title="文件" aria-label="文件" style={{position:"relative",height:44,width:44,border:"1px solid #d0d0d0",borderRadius:6,background:"#fff",display:"grid",placeItems:"center",color:"#555",opacity:id==="x"?.45:1}}><Plus size={19}/>{sendable.length>0&&<small style={{position:"absolute",right:-4,top:-5,minWidth:16,height:16,padding:"0 4px",borderRadius:8,background:"#39a65a",color:"#fff",fontSize:9,lineHeight:"16px"}}>{sendable.length}</small>}</button>\n     <button type="submit" disabled={id==="x"||!draft.trim()} style={{height:44,width:48,border:0,borderRadius:6,background:"#39a65a",color:"#fff",display:"grid",placeItems:"center",opacity:id!=="x"&&draft.trim()?1:.45}}><Send size={16}/></button>'''
new='''     <input disabled={!canFreeText} value={draft} onChange={e=>setDraft(e.target.value)} placeholder={canFreeText?"这一轮可以自己问一句":"输入消息"} style={{height:48,border:"1px solid #d0d0d0",borderRadius:8,padding:"0 14px",minWidth:0,fontSize:14,background:canFreeText?"#fff":"#efefef",color:canFreeText?"#222":"#999"}}/>\n     <button type="button" onClick={()=>canPickMaterial&&setPicker(v=>!v)} disabled={!canPickMaterial} title="文件" aria-label="文件" style={{position:"relative",height:44,width:44,border:"1px solid #d0d0d0",borderRadius:6,background:"#fff",display:"grid",placeItems:"center",color:"#555",opacity:canPickMaterial?1:.35}}><Plus size={19}/>{sendable.length>0&&<small style={{position:"absolute",right:-4,top:-5,minWidth:16,height:16,padding:"0 4px",borderRadius:8,background:"#39a65a",color:"#fff",fontSize:9,lineHeight:"16px"}}>{sendable.length}</small>}</button>\n     <button type="submit" disabled={!canFreeText||!draft.trim()} style={{height:44,width:48,border:0,borderRadius:6,background:"#39a65a",color:"#fff",display:"grid",placeItems:"center",opacity:canFreeText&&draft.trim()?1:.35}}><Send size={16}/></button>'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)
print('Applied v9.2.2 controlled WeChat interaction pass')
