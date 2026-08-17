from pathlib import Path


def replace_once(path, old, new, label):
    p=Path(path); s=p.read_text(encoding='utf-8')
    if old not in s:
        raise SystemExit(f'missing {label} in {path}')
    p.write_text(s.replace(old,new,1),encoding='utf-8')

# ---------------- page.tsx ----------------
page=Path('app/page.tsx')
s=page.read_text(encoding='utf-8')
s=s.replace('import AdminPortal from "./AdminPortal";','import AdminPortalOccult from "./AdminPortalOccult";',1)
s=s.replace('const SHAREABLE_POST_IDS=new Set(["33897","09114","09831","10731","14692","17428","11208","27614"]);','const SHAREABLE_POST_IDS=new Set(["33897","09114","09831","10731","14692","17428","11208","23109","27614"]);',1)
s=s.replace(' const [materials,setMaterials]=useState<SharedMaterial[]>([]);',' const [materials,setMaterials]=useState<SharedMaterial[]>([]);\n const [verseSeen,setVerseSeen]=useState(false);',1)
s=s.replace('openLink={()=>open("verse")}','openLink={()=>{setVerseSeen(true);open("verse")}}',1)
s=s.replace('onCopyMaterial={rememberMaterial} hasMaterial={id=>materials.some(m=>m.id===id)} initialPostId={wxPost}','onCopyMaterial={rememberMaterial} hasMaterial={id=>materials.some(m=>m.id===id)} verseSeen={verseSeen} initialPostId={wxPost}',1)
s=s.replace('function Browser({privateUnlocked,setPrivateUnlocked,onCopyMaterial,hasMaterial,initialPostId,onInitialPostConsumed}:{privateUnlocked:boolean;setPrivateUnlocked:(value:boolean)=>void;onCopyMaterial:(m:SharedMaterial)=>void;hasMaterial:(id:string)=>boolean;initialPostId:string|null;onInitialPostConsumed:()=>void}){','function Browser({privateUnlocked,setPrivateUnlocked,onCopyMaterial,hasMaterial,verseSeen,initialPostId,onInitialPostConsumed}:{privateUnlocked:boolean;setPrivateUnlocked:(value:boolean)=>void;onCopyMaterial:(m:SharedMaterial)=>void;hasMaterial:(id:string)=>boolean;verseSeen:boolean;initialPostId:string|null;onInitialPostConsumed:()=>void}){',1)
s=s.replace('{forumIdentity==="admin"?<AdminPortal loggedIn={true} onAdminLogin={()=>{}} onCancel={()=>{}}/>:route.kind==="account"?<AdminPortal loggedIn={false} onCancel={back} onAdminLogin={()=>{persistedForumIdentity="admin";setForumIdentity("admin");setStack([])}}/>:', '{forumIdentity==="admin"?<AdminPortalOccult loggedIn={true} canUseLegacy={true} onAdminLogin={()=>{}} onCancel={()=>{}}/>:route.kind==="account"?<AdminPortalOccult loggedIn={false} canUseLegacy={verseSeen&&read.includes("27614")&&read.includes("23109")} onCancel={back} onAdminLogin={()=>{persistedForumIdentity="admin";setForumIdentity("admin");setStack([])}}/>:',1)
s=s.replace('</Floor>{post.replies.map((x,i)=><Floor key={i}', '</Floor>{post.id==="23109"&&<RecoveredRitualAttachment/>}{post.replies.map((x,i)=><Floor key={i}',1)
marker='function Floor({user,time,no,role,children,openUser}:{user:string;time:string;no:string;role?:string;children:ReactNode;openUser:(name:string)=>void}){'
if marker not in s: raise SystemExit('missing Floor marker')
attachment='''function RecoveredRitualAttachment(){
 const [phase,setPhase]=useState<"closed"|"error"|"open">("closed");
 if(phase==="closed")return <section style={{margin:"18px 24px",padding:16,border:"1px solid #d5cabc",background:"#f2ede4"}}><b style={{display:"block",fontSize:13}}>失效附件缓存</b><small style={{display:"block",margin:"5px 0 12px",color:"#81766d"}}>thumb_2012_0712.jpg · 恢复状态异常</small><button onClick={()=>setPhase("error")} style={{padding:"7px 11px",border:"1px solid #b8afa5",background:"#fff",borderRadius:5}}>打开恢复附件</button></section>;
 if(phase==="error")return <button onClick={()=>setPhase("open")} style={{width:"calc(100% - 48px)",height:210,margin:"18px 24px",border:"1px solid #341312",background:"#050505",color:"#7d1716",font:"700 28px serif",letterSpacing:".28em"}}>门未闭。<small style={{display:"block",marginTop:20,color:"#655a56",font:"11px sans-serif",letterSpacing:0}}>缓存读取失败 · 点击重试</small></button>;
 return <figure style={{margin:"18px auto",width:"min(620px,90%)",padding:18,border:"1px solid #2b2420",background:"#100d0c"}}><div style={{position:"relative",height:330,overflow:"hidden",background:"radial-gradient(circle at 50% 55%,#341512 0,#16110f 44%,#080707 100%)",boxShadow:"inset 0 0 70px #000"}}><span style={{position:"absolute",left:"12%",bottom:45,width:12,height:72,background:"#8d201b",boxShadow:"0 -12px 24px #ff874b"}}/><span style={{position:"absolute",right:"12%",bottom:45,width:12,height:72,background:"#8d201b",boxShadow:"0 -12px 24px #ff874b"}}/><i style={{position:"absolute",left:"24%",bottom:70,width:68,height:120,display:"grid",placeItems:"center",background:"#c5b07a",color:"#761a16",clipPath:"polygon(35% 0,65% 0,72% 18%,100% 38%,82% 48%,75% 100%,25% 100%,18% 48%,0 38%,28% 18%)",font:"700 20px serif",fontStyle:"normal"}}>舍</i><i style={{position:"absolute",right:"24%",bottom:70,width:68,height:120,display:"grid",placeItems:"center",background:"#c5b07a",color:"#761a16",clipPath:"polygon(35% 0,65% 0,72% 18%,100% 38%,82% 48%,75% 100%,25% 100%,18% 48%,0 38%,28% 18%)",font:"700 20px serif",fontStyle:"normal"}}>舍</i><b style={{position:"absolute",left:"50%",top:55,transform:"translateX(-50%)",width:100,height:100,display:"grid",placeItems:"center",border:"2px solid #79221d",borderRadius:"50%",color:"#9f322a",font:"32px serif"}}>門</b><u style={{position:"absolute",left:"50%",bottom:30,transform:"translateX(-50%)",width:86,height:132,background:"#a98b4f",color:"#6d1b17",textDecoration:"none",boxShadow:"0 0 0 2px #76543d inset"}}/><em style={{position:"absolute",left:"18%",right:"18%",top:175,height:1,background:"#8d2822",transform:"rotate(8deg)",boxShadow:"0 28px 0 #6f221d"}}/><strong style={{position:"absolute",left:"50%",bottom:18,transform:"translateX(-50%)",width:92,height:24,border:"7px solid #271b18",borderRadius:"0 0 50% 50%",background:"#310808",boxShadow:"0 0 18px #771515"}}/></div><figcaption style={{padding:"12px 2px 0",color:"#b49a8c",fontSize:12}}>缩略图文字层残留：<b style={{color:"#a43a32"}}>赤烛照舍，黄符定名。</b>　其余字段损坏。</figcaption></figure>;
}
'''
s=s.replace(marker,attachment+marker,1)
start=s.find('function VersePage(')
if start<0: raise SystemExit('missing VersePage')
new_verse='''function VersePage({onCopyMaterial,hasMaterial}:{onCopyMaterial:(m:SharedMaterial)=>void;hasMaterial:(id:string)=>boolean}){const added=hasMaterial("verse");return <main className="verse-page" style={{minHeight:"100%",background:"#080606",color:"#ddd0c1"}}><header style={{borderBottom:"1px solid #2e1715",background:"#0d0b0a"}}><LockKeyhole/><span>www.zhuyinwen.cn/archive/cache/baishesong-1986.html</span><b>缓存页面</b></header><section style={{maxWidth:1040,margin:"0 auto",padding:"28px 30px 48px"}}><figure style={{width:"min(720px,100%)",margin:"0 auto",background:"#050404",border:"1px solid #321714",boxShadow:"0 24px 80px #000"}}><img src="assets/occult/huanzhen-scripture.webp" alt="无相还真会黑底朱字旧教页" style={{display:"block",width:"100%"}}/><figcaption style={{padding:"9px 12px",color:"#75645c",fontSize:11}}>scan_07_untitled.tif · 来源字段已删除 · 缓存于 2026-10-16 19:49</figcaption></figure><article style={{maxWidth:720,margin:"18px auto 0",padding:"22px 24px",border:"1px solid #3c1c18",background:"#120c0b",font:"15px serif",lineHeight:2,color:"#d8c4b1"}}><small style={{color:"#8d514a",letterSpacing:".14em"}}>恢复文字层</small><h2 style={{margin:"8px 0 16px",color:"#a82e28",font:"700 28px serif",letterSpacing:".12em"}}>无相还真</h2><p>无相还真，<strong style={{color:"#bd4b42"}}>舍身无量。</strong></p><p>赤烛照舍，黄符定名。</p><p>旧客退位，新客安门。</p><p style={{marginTop:22,fontSize:20,letterSpacing:".12em"}}><strong style={{color:"#c04b43"}}>身非我身，名非我名。</strong></p><p style={{color:"#77645c",fontSize:12}}>页脚残留同一句祝号，重复七次：舍身无量。</p><button disabled={added} onClick={()=>onCopyMaterial({id:"verse",title:"无相还真旧教页",kind:"缓存教页",url:"https://www.zhuyinwen.cn/archive/cache/baishesong-1986.html"})} style={{marginTop:8,border:"1px solid #69342f",background:"#201311",color:"#d6c0ae",borderRadius:4,padding:"8px 11px",fontSize:12,cursor:added?"default":"pointer",opacity:added?.55:1}}>{added?"已添加":"添加到材料"}</button></article></section></main>}
'''
s=s[:start]+new_verse+'\n'
page.write_text(s,encoding='utf-8')

# ---------------- PrivateArea.tsx ----------------
p=Path('app/PrivateArea.tsx'); s=p.read_text(encoding='utf-8')
s=s.replace('import DeepArchiveGate from "./DeepArchiveGate";\n','',1)
start=s.find(' const share=()=>{onCopyMaterial({')
end=s.find('\n\n return <main style={s.page}>',start)
if start<0 or end<0: raise SystemExit('missing private share block')
share=''' const materialId=active.id==="p2"?"sanmen":`private-${active.id}`;
 const share=()=>{onCopyMaterial({
  id:materialId,
  title:active.id==="p2"?"《三门疏》残页":active.title,
  kind:"沈妍私密记录",
  url:`local://private/${active.id}`,
 });};'''
s=s[:start]+share+s[end:]
s=s.replace('disabled={hasMaterial(`private-${active.id}`)} onClick={share} style={{...s.share,opacity:hasMaterial(`private-${active.id}`)?.55:1,cursor:hasMaterial(`private-${active.id}`)?"default":"pointer"}}><Link2 size={14}/>{hasMaterial(`private-${active.id}`)?"已添加":"添加到材料"}', 'disabled={hasMaterial(materialId)} onClick={share} style={{...s.share,opacity:hasMaterial(materialId)?.55:1,cursor:hasMaterial(materialId)?"default":"pointer"}}><Link2 size={14}/>{hasMaterial(materialId)?"已添加":"添加到材料"}',1)
s=s.replace('     {active.id==="p3"&&<DeepArchiveGate onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>} \n','',1)
p.write_text(s,encoding='utf-8')

# ---------------- gameDataFlowV2.ts ----------------
p=Path('content/gameDataFlowV2.ts'); s=p.read_text(encoding='utf-8')
start=s.find('const adminAccountPost:Post={')
end=s.find('\n\nconst patched=',start)
if start<0 or end<0: raise SystemExit('missing adminAccountPost block')
new_posts='''const adminAccountPost:Post={
 id:"27614",title:"旧档员-03到底是一个人还是值班号？",author:"西楼",date:"2024-02-18 01:26",board:"站务区",views:3271,hidden:true,
 excerpt:"旧档整理账号半夜也在移动帖子，说话风格还不太一样。这个号到底几个人在用？",
 terms:["旧档员-03","值班号","迁移账号","旧版账号","登录"],highlights:["旧档员-03","多人轮用","迁移账号"],
 body:["纯好奇。旧档员-03这个号经常凌晨两三点还在移动旧主题，而且有时候回复特别书面，有时候就一句话。我一直以为是机器人，后来又见它正常回人。","站务以前说过这是值班账号，但我没找到更详细的说明。它到底是一个人、几个人轮用，还是自动任务和真人混着用？"],
 replies:[reply("站务","01:44","多人轮用。旧档恢复也有自动任务，所以操作时间不代表某个具体成员在线。","版主"),reply("纸页边角","02:03","我有次点它头像，跳到一个特别旧的认证页。标题像是‘迁移账号’，页面没加载全，我就退了。"),reply("站务","02:17","早期迁移账号仍保留兼容认证，属于历史功能。请勿反复尝试登录不属于自己的账号。","版主"),reply("西楼","02:31","懂了。那半夜移动也不稀奇，自动任务加值班一起跑。","楼主"),reply("旧档员-03","03:08","公开页面看到的是同一个账号名，不代表后台操作来源相同。")],
 archive:"站务归档：2024-03-02；主题保留，停止回复。"
};

const ritualFragmentPost:Post={
 id:"23109",title:"老帖附件只恢复出黄纸和两个纸人，有人认得吗",author:"纸页边角",date:"2016-02-11 23:18",board:"旧闻考据",views:2419,hidden:true,
 excerpt:"旧图床缓存只剩一张模糊缩略图：黄纸、红烛、两个纸偶和一条残句。",
 terms:["旧档员-03","黄符","红蜡烛","纸偶","纸人","赤烛照舍","黄符定名","旧档恢复"],highlights:["赤烛照舍，黄符定名","黄纸","红蜡烛","两个纸偶"],
 body:["清旧收藏时碰到一个2012年的失效附件。原帖正文已经没了，旧图床只吐出一张很小的缩略图。","能看清的东西不多：两张黄纸、两支红蜡烛、两个面对面的纸偶，中间像画了个门。黄纸边上好像有暗红手印。","OCR残留只认出一句：‘赤烛照舍，黄符定名。’ 不知道是民俗道具、电影美术，还是哪种民间教派的东西。"],
 replies:[reply("旧纸鸢","23:42","不像常见镇宅符。至少‘定名’这个说法我没见过。"),reply("夜航船","00:03","两个纸人面对面摆着挺瘆人的，像拿来替人的。"),reply("旧档员-03","2016-02-12 02:11","附件从旧图床缓存恢复，原始上传者字段已丢失。请勿据缩略图判断来源。","版主"),reply("纸页边角","02:26","收到。我只留图和能看清的字，不给它编出处。","楼主")],
 archive:"旧档恢复记录：2016-02-12；执行账号“旧档员-03”。原始附件已失效。"
};'''
s=s[:start]+new_posts+s[end:]
s=s.replace('export const posts:Post[]=[...patched,posterMemory,adminAccountPost].sort', 'export const posts:Post[]=[...patched,posterMemory,ritualFragmentPost,adminAccountPost].sort',1)
start=s.find('export const privateEntries:PrivateEntry[]=')
end=s.find('\n\nexport const profile=',start)
if start<0 or end<0: raise SystemExit('missing privateEntries block')
new_private='''const privateP1=flowPrivateEntries.find(entry=>entry.id==="p1")!;
const privateP3=flowPrivateEntries.find(entry=>entry.id==="p3")!;
const sanmenPrivate:PrivateEntry={
 id:"p2",title:"7月12日，白纸上能抄下来的几句",date:"2026-07-12 01:26",
 highlights:["身为舍，魂为客","形可易，名可夺，忆可乱","二客相契，两门相应","再舍者，故门有声"],
 body:["夹墙白纸和旧转载里的版本对不上，我把目前能重复辨认的原句单独抄在这里，不再往里补解释。","身为舍，魂为客。","形可易，名可夺，忆可乱；客不可凭一门自证。","二客相契，两门相应。","再舍者，故门有声。","这些句子到底在说什么，我现在没有证据。先留原文。"],
 images:[{src:"assets/sanmen-shenyan-annotations-v1.webp",caption:"附件：沈妍保存的《三门疏》残页；只圈出处与异文"}]
};
export const privateEntries:PrivateEntry[]=[
 {...privateP1,highlights:(privateP1.highlights||[]).map(mark=>mark==="红色铁皮糖盒"?"红铁皮盒":mark),body:privateP1.body.map((text,index)=>index===0?text.replace("红色铁皮糖盒","红铁皮盒"):text)},
 {...privateP3,title:"9月11日，几条旧帖",highlights:["名字不对","另一个家","回来以后不会以前会的东西了","某种味道"],body:["这两个月陆续存了几条。旧报、报警回执、当年的寻人材料能对上的我才留，剩下的先删了。","有的人回来以后只是突然讨厌某种味道；也有人原话就是‘名字不对’、‘我记得另一个家’、‘回来以后不会以前会的东西了’。单看都能解释，挨着放又有点怪。","我把年龄、走失多久、找回后的第一条异常和出处记在一张表里。今晚先到这，眼睛疼。"]},
 sanmenPrivate,
];'''
s=s[:start]+new_private+s[end:]
p.write_text(s,encoding='utf-8')

# ---------------- InteractiveWechat.tsx ----------------
p=Path('app/InteractiveWechat.tsx'); s=p.read_text(encoding='utf-8')
s=s.replace(' "27614":{zc:[{text:"这篇我有印象。"},{text:"站务后来不是说多人轮用吗。"}],ly:[{text:"我以前没点进去看过。"}]},', ' "23109":{zc:[{text:"……这张图挺邪的。"},{text:"你从哪翻出来的？"}],ly:[{text:"这个黄纸我小时候见过差不多的。"},{text:"贴在门框边上。我一直以为就是家里辟邪。"}]},\n "27614":{zc:[{text:"这篇我有印象。"},{text:"站务后来不是说多人轮用吗。"}],ly:[{text:"我以前没点进去看过。"}]},',1)
needle=' if(contactId==="zc"&&materialId==="27614"){'
pos=s.find(needle)
if pos<0: raise SystemExit('missing 27614 quick reply')
extra=''' if(contactId==="zc"&&materialId==="23109")return [{id:"zc-ritual-fragment",text:"“赤烛照舍，黄符定名”像什么？",reply:[{text:"不知道。"},{text:"但这句不像网友临时编的，跟图里的摆法是一起的。"},{text:"“定名”听着像他们自己固定用的词。"}]}];
'''
s=s[:pos]+extra+s[pos:]
p.write_text(s,encoding='utf-8')

# ---------------- v2.1 supersession note ----------------
p=Path('docs/CANON_v2.1_人物与信息通道修订.md'); s=p.read_text(encoding='utf-8')
needle='生效日期：2026-08-15\n'
if needle in s and 'CANON v2.2' not in s[:500]:
    s=s.replace(needle,needle+'\n> **2026-08-17 补充：私密区/八字经文/管理员认证/无相还真会宗教视觉相关规则已由 `CANON_v2.2_无相还真会宗教感与管理员线修订.md` 覆盖。**\n',1)
p.write_text(s,encoding='utf-8')

# Guardrails
page_text=Path('app/page.tsx').read_text(encoding='utf-8')
assert 'AdminPortalOccult' in page_text
assert 'verseSeen&&read.includes("27614")&&read.includes("23109")' in page_text
assert 'RecoveredRitualAttachment' in page_text
assert 'assets/occult/huanzhen-scripture.webp' in page_text
priv=Path('app/PrivateArea.tsx').read_text(encoding='utf-8')
assert 'DeepArchiveGate' not in priv
assert 'active.id==="p2"?"sanmen"' in priv
data=Path('content/gameDataFlowV2.ts').read_text(encoding='utf-8')
assert 'id:"23109"' in data
assert 'const sanmenPrivate' in data
assert 'archive_0712.zip' not in priv
wx=Path('app/InteractiveWechat.tsx').read_text(encoding='utf-8')
assert 'materialId==="23109"' in wx
print('v9 occult gameplay rework applied')
