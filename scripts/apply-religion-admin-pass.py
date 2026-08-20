from pathlib import Path


def replace_once(text, old, new, label):
    if old not in text:
        raise SystemExit(f"missing source fragment: {label}")
    return text.replace(old, new, 1)

# ---- Admin portal ----
p = Path("app/AdminPortalOccult.tsx")
s = p.read_text()

s = replace_once(s,
    'type Props={loggedIn:boolean;onAdminLogin:()=>void;onCancel:()=>void;canUseLegacy:boolean;onWechatIncoming?:()=>void;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean};',
    'type Props={loggedIn:boolean;onAdminLogin:()=>void;onCancel:()=>void;onExitAdmin?:()=>void;canUseLegacy:boolean;onWechatIncoming?:()=>void;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean};',
    'admin props')
s = replace_once(s,
    'type AdminTab="watch"|"users"|"candidates"|"ops"|"recycle";',
    'type AdminTab="watch"|"users"|"candidates"|"liturgy"|"ops"|"recycle";',
    'admin tabs')
s = replace_once(s,
    'const OLD_OATH="身非我身名非我名";',
    'const OLD_OATH="身非我身名非我名";\nconst REMEMBERED_ADMIN_KEY="zhuyin-admin-user";',
    'remembered admin key')
s = replace_once(s,
    'export default function AdminPortalOccult({loggedIn,onAdminLogin,onCancel,canUseLegacy,onWechatIncoming,onCopyMaterial,hasMaterial}:Props){',
    'export default function AdminPortalOccult({loggedIn,onAdminLogin,onCancel,onExitAdmin,canUseLegacy,onWechatIncoming,onCopyMaterial,hasMaterial}:Props){',
    'admin function props')
s = replace_once(s,
    ' const [filled,setFilled]=useState(false);\n\n if(loggedIn)return <AdminDesk onWechatIncoming={onWechatIncoming} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>;',
    ' const [filled,setFilled]=useState(false);\n useEffect(()=>{if(loggedIn)return;try{if(window.sessionStorage.getItem(REMEMBERED_ADMIN_KEY)===ADMIN_USER)setUser(ADMIN_USER)}catch{}},[loggedIn]);\n\n if(loggedIn)return <AdminDesk onExitAdmin={onExitAdmin} onWechatIncoming={onWechatIncoming} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>;',
    'remembered admin effect')
s = replace_once(s,
    '  if(user.trim()===ADMIN_USER&&pwd===ADMIN_TEMP_CODE){onAdminLogin();setError("");return;}',
    '  if(user.trim()===ADMIN_USER&&pwd===ADMIN_TEMP_CODE){try{window.sessionStorage.setItem(REMEMBERED_ADMIN_KEY,ADMIN_USER)}catch{};onAdminLogin();setError("");return;}',
    'remember account on login')
s = replace_once(s,
    '   <p style={s.muted}>当前浏览器保存了一个已登录会话。也可以使用其他账号登录。</p>',
    '   <p style={s.muted}>{user===ADMIN_USER?"已记住旧档账号。再次进入时只需要输入口令；忘记口令可以重新进行旧档验证。":"当前浏览器保存了一个已登录会话。也可以使用其他账号登录。"}</p>',
    'login remembered hint')
s = replace_once(s,
    '   {attemptedAdmin&&user.trim()===ADMIN_USER&&canUseLegacy&&<button onClick={()=>setMode("verify")} style={s.legacy}>',
    '   {(attemptedAdmin||user.trim()===ADMIN_USER)&&canUseLegacy&&<button onClick={()=>setMode("verify")} style={s.legacy}>',
    'legacy recovery visibility')
s = replace_once(s,
    '<p>临时口令仅用于本次旧档认证。</p><button onClick={onVerified} style={s.verifyButton}>返回登录并填入口令</button>',
    '<p>记住这个口令。账号会保留；以后只需输入口令。忘了就再做一次旧档验证。</p><button onClick={onVerified} style={s.verifyButton}>返回登录并填入口令</button>',
    'verification final hint')
s = replace_once(s,
    'function AdminDesk({onWechatIncoming,onCopyMaterial,hasMaterial}:{onWechatIncoming?:()=>void;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){',
    'function AdminDesk({onExitAdmin,onWechatIncoming,onCopyMaterial,hasMaterial}:{onExitAdmin?:()=>void;onWechatIncoming?:()=>void;onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean}){',
    'admin desk props')
s = replace_once(s,
    '<header style={s.adminHead}><strong style={{fontSize:14,fontWeight:700}}>旧档管理</strong><span style={s.adminAccount}>旧档员-03</span></header>',
    '<header style={s.adminHead}><strong style={{fontSize:14,fontWeight:700}}>旧档管理</strong><span style={{display:"flex",alignItems:"center",gap:8}}><span style={s.adminAccount}>旧档员-03</span>{onExitAdmin&&<button onClick={onExitAdmin} style={{height:32,padding:"0 11px",border:"1px solid #758981",borderRadius:6,background:"#f5f8f6",color:"#2d493e",fontSize:11,fontWeight:700,cursor:"pointer"}}>返回论坛</button>}</span></header>',
    'admin return forum button')
s = replace_once(s,
    '<button className={tab==="candidates"?"active":""} onClick={()=>{setTab("candidates");setDetail(null)}}>候舍库</button><button className={tab==="ops"?"active":""}',
    '<button className={tab==="candidates"?"active":""} onClick={()=>{setTab("candidates");setDetail(null)}}>候舍库</button><button className={tab==="liturgy"?"active":""} onClick={()=>{setTab("liturgy");setDetail(null)}}>诵录</button><button className={tab==="ops"?"active":""}',
    'liturgy nav')
s = replace_once(s,
    '    {tab==="candidates"&&<CandidateLibrary/>}\n    {tab==="ops"&&<Operations/>}',
    '    {tab==="candidates"&&<CandidateLibrary/>}\n    {tab==="liturgy"&&<Liturgy/>}\n    {tab==="ops"&&<Operations/>}',
    'liturgy render')
s = replace_once(s,
    'function CandidateLibrary(){',
    '''function Liturgy(){return <><div style={s.sectionTitle}>诵录</div><p style={{margin:"0 0 14px",color:"#707872",fontSize:12}}>内部日课 · 归真序列阶段 II</p><section style={{maxWidth:760,padding:"28px 30px",border:"1px solid #3b2926",borderRadius:8,background:"radial-gradient(circle at 50% 10%,#2b1513,#110d0c 62%,#090807)",boxShadow:"0 18px 44px #0002",color:"#d7c6b5",fontFamily:"serif",lineHeight:2,textAlign:"center"}}><small style={{color:"#8f5f57",letterSpacing:".18em"}}>晚课 · 第七录</small><h2 style={{margin:"10px 0 18px",color:"#a93d35",font:"700 27px serif",letterSpacing:".18em"}}>无相还真</h2><p style={{fontSize:18}}>无相还真，舍身无量。</p><p>真君无相，不应有定身。</p><p>身为舍，魂为客。</p><div style={{width:70,height:1,margin:"20px auto",background:"#60312c"}}/><p style={{margin:0,color:"#b8a393"}}>今日所验，不在一舍之成；<br/>所验者，是客历舍而其续不绝。</p><p style={{margin:"18px 0 0",color:"#8f7468",fontSize:12}}>长客再舍未稳，归真序列不得启。</p></section><section style={s.adminPanel}><h4>诵录旁注</h4><Record date="归真目标" title="建立可重复的连续换舍路径" meta="内部目的" text="验证同一客能在多具舍之间连续迁移，并尽可能保持记忆与主体连续。"/><Record date="当前前置" title="长期客二次再舍稳定" meta="RS-2026-1012" text="客α的第二次再舍是现阶段关键验证；旧对契异常尚未关闭。"/><Record date="真君序列" title="待前置验证通过" meta="阶段 II" text="若连续再舍稳定性达到条件，流程将进入无相真君序列。真君原始身份不在本页登记。"/></section></>}

function CandidateLibrary(){''',
    'insert liturgy page')
p.write_text(s)

# ---- Forum shell / return flow ----
p = Path("app/page.tsx")
s = p.read_text()
s = replace_once(s,
    'const HOME_POST_IDS=["34091","34086","34080","34064","34055","34049","20847","34043","33992","33981"];',
    'const HOME_POST_IDS=["34106","34091","34086","34080","34064","34055","34049","20847","34043","33992","33981"];',
    'home post list')
old = '{forumIdentity==="admin"?<AdminPortalOccult loggedIn={true} canUseLegacy={true} onAdminLogin={()=>{}} onCancel={()=>{}} onWechatIncoming={()=>setWxRead(false)} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>:route.kind==="account"?'
new = '{forumIdentity==="admin"?<AdminPortalOccult loggedIn={true} canUseLegacy={true} onAdminLogin={()=>{}} onCancel={()=>{}} onExitAdmin={()=>{persistedForumIdentity="shenyan";setForumIdentity("shenyan");setRoute({kind:"home"});setStack([])}} onWechatIncoming={()=>setWxRead(false)} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>:route.kind==="account"?'
s = replace_once(s, old, new, 'admin exit handler')
p.write_text(s)

# ---- Public forum post ----
p = Path("content/gameDataFlowV2.ts")
s = p.read_text()
insert = '''
const thresholdNamePost:Post={
 id:"34106",title:"搬家第一晚不能在门口喊全名？我外婆这个说法是哪儿的",author:"白粥配蛋",date:"2026-10-16 23:37",board:"闲聊灌水",views:286,excerpt:"整理老人旧笔记翻到一句很怪的搬家忌讳：过门以后先认屋，再认名。有人家里也这么说吗？",terms:["搬家","门槛","全名","过门","名字","旧俗"],highlights:[],
 body:["整理外婆留下来的杂记，看到一条我小时候听过但早忘了的规矩：搬家第一晚，站在门里不要喊家里人的全名。","她解释得很怪，大意是‘门先认住进来的人，名字慢慢再认’，还写了一句：人换屋，名也跟着换地方。小时候我一直当她吓小孩。","搜了一圈没找到完全一样的说法。有人家里也讲过这种‘过门以后别急着叫名’的禁忌吗？"],
 replies:[reply("旧纸鸢","23:51","像是搬家忌讳、叫魂和避名几种说法混在一起了。老人家口传几代，很容易串。"),reply("南门摆摊","00:06","我老家只讲进门别回头，没听过不能叫全名。"),reply("折柳","00:18","这种家里话很难追固定出处。记下来就行，别因为一句怪话硬往某个教门上套。"),reply("白粥配蛋","00:25","行，我主要是觉得那句‘先认屋再认名’太怪了，记着玩。","楼主")]
};

'''
s = replace_once(s, 'const ritualFragmentPost:Post={', insert + 'const ritualFragmentPost:Post={', 'insert public cult-adjacent post')
s = replace_once(s,
    'export const posts:Post[]=[...patched,posterMemory,linSnackPost,linMarblePost,shenCandyPost,ritualFragmentPost,adminAccountPost].sort((a,b)=>toRank(a.date)-toRank(b.date));',
    'export const posts:Post[]=[...patched,posterMemory,linSnackPost,linMarblePost,shenCandyPost,thresholdNamePost,ritualFragmentPost,adminAccountPost].sort((a,b)=>toRank(a.date)-toRank(b.date));',
    'export public cult-adjacent post')
p.write_text(s)

# ---- Canon ----
p = Path("docs/CANON_v3.0_世界观与游戏设定唯一权威集.md")
s = p.read_text()
anchor = '- 新增 NPC 前先问：**现有人物能不能承担这个功能？**\n\n---'
addition = '''- 新增 NPC 前先问：**现有人物能不能承担这个功能？**

### 2.1 宗教露出与后台回访

- 公共论坛首页允许出现少量**表面是普通地方旧俗、实际与无相还真会教义同构**的帖子；前期不直接点名组织，不把论坛写成邪教群聊；
- 管理员后台增加“**诵录**”入口，用宗教日课形式呈现固定祝号与现行研究目标；
- 后台可明确：**真君无相，不应有定身**；现阶段的技术目标是验证同一客可在多具舍之间连续迁移并尽量保持记忆与主体连续，从而建立可重复的换舍路径；
- 仍不回答无相真君的原始身份、是否为同一古老魂、或是否只是宗教职位；
- 管理员后台内部提供“返回论坛”入口；首次成功登录后只记住账号 `旧档员-03`，**不保存密码**。再次进入时玩家只需自行输入 `gumen-0712`；若忘记，可重新走旧档兼容认证小游戏取得口令。

---'''
s = replace_once(s, anchor, addition, 'canon religion/admin UX section')
p.write_text(s)
