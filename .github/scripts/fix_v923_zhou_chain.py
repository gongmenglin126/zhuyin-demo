from pathlib import Path
p=Path('app/InteractiveWechat.tsx')
s=p.read_text()
start=s.index('export const revealZhouConfrontation=()=>{')
end=s.index('\nexport const discoverZhouIdentity=',start)
new='''export const revealZhouConfrontation=()=>{\n const stamp=wechatSession.firstContact.zc;\n if(!wechatSession.zhouIdentityKnown||!stamp||wechatSession.zhouConfronted)return false;\n wechatSession.zhouEvidenceSeen=true;\n wechatSession.freeText={...wechatSession.freeText,zc:false};\n wechatSession.freeReturn={...wechatSession.freeReturn,zc:[]};\n const how:QuickReply={id:"zc-zheliu-how",text:"你怎么知道我给她发了？",reply:[{text:"……"},{text:"徐宁，你听我一次。"},{text:"离开沈妍家。别报警。"}]};\n const log:QuickReply={id:"zc-zheliu-log",text:`我${stamp}才告诉你我是徐宁，同一分钟后台就有折柳补录。`,reply:[{text:"关掉。"},{text:"我说关掉。"},{text:"不要再给梁茵发任何东西。"}],next:[how]};\n const real:QuickReply={id:"zc-zheliu-real",text:"论坛实名资料写的是周川。后台来源写的是折柳。",reply:[{text:"……"},{text:"把后台关掉。"},{text:"现在。"}],next:[log]};\n const first:QuickReply={id:"zc-zheliu",text:"你是折柳？",emphasis:true,reply:[{text:"你为什么搜这个号。"}],next:[real]};\n wechatSession.quick={...wechatSession.quick,zc:[first]};\n notifyWechat();\n return true;\n};'''
s=s[:start]+new+s[end:]
p.write_text(s)
print('Fixed v9.2.3 Zhou chain syntax')