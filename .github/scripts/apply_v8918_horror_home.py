from pathlib import Path


def replace_once(path, old, new, label):
    p=Path(path); s=p.read_text(encoding='utf-8')
    if old not in s: raise SystemExit(f'missing {label}')
    p.write_text(s.replace(old,new,1),encoding='utf-8')

# Curate the forum homepage: ordinary/noise posts plus one early Shen Yan dream post.
page='app/page.tsx'
replace_once(page,
'const SHAREABLE_POST_IDS=new Set(["33897","09114","09831","10731","14692","17428","11208","27614"]);\nlet persistedForumIdentity:',
'const SHAREABLE_POST_IDS=new Set(["33897","09114","09831","10731","14692","17428","11208","27614"]);\nconst HOME_POST_IDS=["34091","34086","34080","34064","34055","34049","20847","34043","33992","33981"];\nlet persistedForumIdentity:',
'home post ids')
replace_once(page,
'const visible=investigationPosts.filter(p=>!p.hidden).slice(0,10);const shown=board==="全部"?visible:visible.filter(p=>p.board===board);',
'const visible=HOME_POST_IDS.map(pid=>investigationPosts.find(p=>p.id===pid)).filter((p):p is Post=>!!p);const shown=board==="全部"?visible:visible.filter(p=>p.board===board);',
'forum home visibility')

admin='app/AdminPortal.tsx'
replace_once(admin,
'    <p style={s.verse}>二客各有所舍。</p>\n    <div style={s.doors}>',
'    <p style={s.verse}>二客各有所舍。</p>\n    <RitualAltar/>\n    <div style={s.doors}>',
'altar insertion')
replace_once(admin,
'    <p style={s.help}>让两边仍能被门外的人认出来。</p>',
'    <p style={s.help}>门外仍呼旧名。</p>',
'stage1 text')
replace_once(admin,
'    <p style={s.help}>交换后，记忆没有整齐地跟着任何一边。</p>',
'    <p style={s.help}>有些东西回不到原处。</p>',
'stage2 text')
replace_once(admin,
'   {stage===3&&<div style={s.success}>\n    <ShieldCheck size={34}/>',
'   {stage===3&&<div style={s.success}>\n    <p style={s.afterVerse}>身非我身　名非我名</p>\n    <ShieldCheck size={34}/>',
'success verse')

marker='function Door({title,name,guests,selected,onSelect,onDrop}:{title:string;name:string;guests:Guest[];selected:Guest|null;onSelect:(g:Guest)=>void;onDrop:()=>void}){'
altar_component='''function RitualAltar(){return <div style={s.altar} aria-hidden="true">
 <span style={{...s.candle,left:42}}/><span style={{...s.candle,right:42}}/>
 <span style={s.threadA}/><span style={s.threadB}/>
 <div style={s.altarRing}><b>門</b><small>身非我身</small></div>
 <div style={s.altarTable}><span>甲</span><em>名非我名</em><span>乙</span></div>
</div>}

'''
replace_once(admin,marker,altar_component+marker,'ritual altar component')

old_recycle='function Recycle(){return <><h2>回收记录</h2><div style={s.adminPanel}><Record date="2026-10-16 18:31" title="未发布草稿" meta="候鸟第七年 · 私密草稿 · 已删除" text="照骨问的问题不是随机的。它在不同人的帖子下面问的是同一套东西。旧档员-03也反复碰过这些帖。先把账号记下来。"/></div></>}'
new_recycle='''function Recycle(){return <><h2>回收记录</h2><div style={s.adminPanel}><Record date="2026-10-16 18:31" title="未发布草稿" meta="候鸟第七年 · 私密草稿 · 已删除" text="照骨问的问题不是随机的。它在不同人的帖子下面问的是同一套东西。旧档员-03也反复碰过这些帖。先把账号记下来。"/><Record date="2026-10-16 20:47" title="附件缓存" meta="旧档员-03 · 已删除" text="IMG_1016_2047.jpg · 原始来源字段缺失 · 仅恢复缩略图"/><RitualThumbnail/></div></>}
function RitualThumbnail(){return <figure style={s.photo}><div style={s.photoRoom}><span style={s.photoCandleL}/><span style={s.photoCandleR}/><i style={s.photoChairL}/><i style={s.photoChairR}/><b style={s.photoTableMark}>門</b><em style={s.photoLine}/></div><figcaption style={s.photoCaption}>IMG_1016_2047.jpg　恢复 14%</figcaption></figure>}
'''
replace_once(admin,old_recycle,new_recycle,'recycle ritual thumbnail')

style_old='verifyPage:{minHeight:"calc(100% - 39px)",display:"grid",placeItems:"center",padding:24,background:"#171a18",color:"#e9ece9"},verifyShell:{width:"min(780px,96%)",minHeight:540,border:"1px solid #3c443f",borderRadius:10,background:"#202522",boxShadow:"0 30px 90px #0008",overflow:"hidden"},'
style_new='verifyPage:{minHeight:"calc(100% - 39px)",display:"grid",placeItems:"center",padding:24,background:"radial-gradient(circle at 50% 54%,#351616 0,#171a18 46%,#090b0a 100%)",color:"#e9ece9"},verifyShell:{width:"min(780px,96%)",minHeight:540,border:"1px solid #4b3a38",borderRadius:10,background:"#1d211f",boxShadow:"0 30px 90px #000, inset 0 0 90px #5b15151c",overflow:"hidden"},'
replace_once(admin,style_old,style_new,'verify horror background')

style_marker='ritual:{padding:"42px 54px",textAlign:"center"},verse:{font:"18px serif",letterSpacing:".12em",color:"#e4ded1"},'
style_insert='''ritual:{padding:"34px 54px 42px",textAlign:"center"},verse:{font:"18px serif",letterSpacing:".12em",color:"#e4ded1"},altar:{position:"relative",height:154,maxWidth:520,margin:"22px auto 6px",borderBottom:"1px solid #6b4a42",background:"radial-gradient(circle at 50% 45%,#6c2a1a33 0,#181b19 58%,#111311 100%)",overflow:"hidden"},candle:{position:"absolute",bottom:28,width:8,height:34,background:"#9b8060",boxShadow:"0 -10px 16px #e48a4e99,0 -5px 4px #ffc079",borderRadius:"2px 2px 0 0"},threadA:{position:"absolute",left:90,right:90,top:76,height:1,background:"#6b2525",transform:"rotate(12deg)",transformOrigin:"center"},threadB:{position:"absolute",left:90,right:90,top:76,height:1,background:"#6b2525",transform:"rotate(-12deg)",transformOrigin:"center"},altarRing:{position:"absolute",left:"50%",top:22,transform:"translateX(-50%)",width:86,height:86,border:"1px solid #7e3d36",borderRadius:"50%",display:"grid",placeItems:"center",background:"#1d1716cc",boxShadow:"0 0 28px #6f201f44",color:"#b99283"},altarTable:{position:"absolute",left:"50%",bottom:0,transform:"translateX(-50%)",width:220,height:34,display:"flex",alignItems:"center",justifyContent:"space-between",padding:"0 18px",border:"1px solid #493633",background:"#171311",color:"#8e756a",font:"12px serif"},afterVerse:{margin:"0 0 18px",color:"#9f6b65",font:"15px serif",letterSpacing:".22em"},'''
replace_once(admin,style_marker,style_insert,'altar styles')

style_tail='record:{display:"grid",gridTemplateColumns:"150px 1fr",gap:16,padding:"14px 16px",borderTop:"1px solid #eceeec"},\n};'
style_tail_new='''record:{display:"grid",gridTemplateColumns:"150px 1fr",gap:16,padding:"14px 16px",borderTop:"1px solid #eceeec"},photo:{margin:"0",padding:"16px",borderTop:"1px solid #eceeec",background:"#f6f6f3"},photoRoom:{position:"relative",height:220,maxWidth:520,margin:"0 auto",overflow:"hidden",border:"8px solid #222",background:"radial-gradient(circle at 50% 58%,#665042 0,#2a2724 32%,#111 72%)",filter:"grayscale(.65) contrast(1.18)",boxShadow:"inset 0 0 65px #000"},photoCandleL:{position:"absolute",left:"24%",bottom:48,width:5,height:26,background:"#c4aa7f",boxShadow:"0 -8px 12px #ffc06b"},photoCandleR:{position:"absolute",right:"24%",bottom:48,width:5,height:26,background:"#c4aa7f",boxShadow:"0 -8px 12px #ffc06b"},photoChairL:{position:"absolute",left:"13%",bottom:42,width:58,height:78,border:"5px solid #171717",borderBottom:0,transform:"rotate(4deg)"},photoChairR:{position:"absolute",right:"13%",bottom:42,width:58,height:78,border:"5px solid #171717",borderBottom:0,transform:"rotate(-4deg)"},photoTableMark:{position:"absolute",left:"50%",bottom:52,transform:"translateX(-50%)",width:110,height:42,display:"grid",placeItems:"center",border:"1px solid #6c5548",background:"#1a1512",color:"#8e7769",font:"22px serif"},photoLine:{position:"absolute",left:"15%",right:"15%",bottom:30,height:1,background:"#766255",boxShadow:"0 -58px 0 #4d3c34",transform:"rotate(-2deg)"},photoCaption:{display:"block",maxWidth:520,margin:"8px auto 0",color:"#777",fontSize:11},\n};'''
replace_once(admin,style_tail,style_tail_new,'photo styles')

# Basic guardrails.
pt=Path(page).read_text(encoding='utf-8')
assert 'HOME_POST_IDS' in pt and '14692' not in pt.split('HOME_POST_IDS=')[1].split('];')[0]
at=Path(admin).read_text(encoding='utf-8')
assert '<RitualAltar/>' in at and 'IMG_1016_2047.jpg' in at and '身非我身　名非我名' in at
print('v8.9.18 horror/home patch applied')
