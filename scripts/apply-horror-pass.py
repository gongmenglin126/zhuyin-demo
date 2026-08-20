from pathlib import Path


def replace_between(text, start, end, replacement, label):
    i = text.find(start)
    if i < 0:
        raise SystemExit(f"missing start marker: {label}")
    j = text.find(end, i)
    if j < 0:
        raise SystemExit(f"missing end marker: {label}")
    return text[:i] + replacement + text[j:]


def replace_once(text, old, new, label):
    if old not in text:
        raise SystemExit(f"missing source fragment: {label}")
    return text.replace(old, new, 1)


# ---- Admin liturgy: visible immediately, burns only itself ----
p = Path("app/AdminPortalOccult.tsx")
s = p.read_text()
new_liturgy = r'''let liturgyBurned=false;
function Liturgy(){
 const [step,setStep]=useState(()=>liturgyBurned?99:0);
 useEffect(()=>{
  if(liturgyBurned)return;
  const timers=[
   window.setTimeout(()=>setStep(1),700),
   window.setTimeout(()=>setStep(2),1700),
   window.setTimeout(()=>setStep(3),2700),
   window.setTimeout(()=>setStep(4),3700),
   window.setTimeout(()=>setStep(5),5000),
   window.setTimeout(()=>{liturgyBurned=true;setStep(99)},6500),
  ];
  return ()=>timers.forEach(id=>window.clearTimeout(id));
 },[]);
 if(step===99)return <section style={{minHeight:520,display:"grid",placeItems:"center",margin:"-28px -34px",background:"#000",color:"#111",boxShadow:"inset 0 0 120px #000"}}><span style={{font:"11px ui-monospace,monospace",letterSpacing:".12em"}}>ERR_ARCHIVE_410</span></section>;
 const line=(n:number,text:string)=><p style={{margin:"12px 0",fontSize:20,letterSpacing:".14em",color:step===n?"#d8d0c3":"#56443f",textShadow:step===n?"0 0 18px #c546384f":"none",transition:".35s"}}>{text}</p>;
 return <><div style={s.sectionTitle}>诵录</div><p style={{margin:"0 0 14px",color:"#707872",fontSize:12}}>内部日课 · 归真序列阶段 II</p><section style={{maxWidth:760,minHeight:420,display:"grid",alignContent:"center",padding:"34px 36px",border:"1px solid #3b2926",borderRadius:8,background:"radial-gradient(circle at 50% 8%,#2b1513,#100c0b 60%,#070606)",boxShadow:"0 18px 44px #0003",color:"#d7c6b5",fontFamily:"serif",textAlign:"center"}}><small style={{color:"#80534d",letterSpacing:".2em"}}>晚课 · 第七录</small><h2 style={{margin:"10px 0 22px",color:"#8e302b",font:"700 27px serif",letterSpacing:".18em"}}>无相还真</h2>{line(1,"身为舍。")}{line(2,"魂为客。")}{line(3,"名可弃。")}{line(4,"舍可更。")}{step>=5&&<div style={{marginTop:28,padding:"13px 15px",borderTop:"1px solid #382220",borderBottom:"1px solid #382220",background:"#070707",color:"#d4d4d4",font:"700 14px ui-monospace,SFMono-Regular,Consolas,monospace",letterSpacing:".05em"}}>访问者徐宁，未登记候舍编号。</div>}</section></>;
}

'''
s = replace_between(s, 'function Liturgy(){', 'function CandidateLibrary(){', new_liturgy + 'function CandidateLibrary(){', 'liturgy function')

new_recycle = r'''function DeletedRescuePost(){
 const [open,setOpen]=useState(false);
 return <section style={{borderTop:"1px solid #eceeec",background:"#fbfbf8"}}><button onClick={()=>setOpen(v=>!v)} style={{width:"100%",display:"grid",gridTemplateColumns:"150px 1fr",gap:16,padding:"14px 16px",border:0,background:"transparent",textAlign:"left",cursor:"pointer",color:"inherit"}}><time style={{fontSize:11,color:"#8b8f8c"}}>2011-08-25 00:41</time><span><b style={{display:"block",fontSize:12}}>《救救我》</b><small style={{display:"block",marginTop:3,color:"#767b77"}}>小雨伞 · 已删除 · 镜像完整</small><p style={{margin:"5px 0 0",fontSize:12,color:"#565b57"}}>原帖发布 3 分钟后删除。点击查看恢复内容。</p></span></button>{open&&<div style={{margin:"0 16px 16px 166px",padding:"16px 18px",border:"1px solid #c8c5bd",background:"#f5f2eb",fontSize:13,lineHeight:1.85,color:"#312f2c"}}><small style={{display:"block",marginBottom:10,color:"#8a514b",fontFamily:"ui-monospace,monospace"}}>RECOVERED / UID 1184-0711</small><p>我不是开玩笑。昨天晚上又来了两个人，爸妈让我坐在客厅，不许回房间。</p><p>他们把我以前的照片都收走了，还让我不要回答别人叫我的名字。妈妈说过几天就好了，说以后我会明白。</p><p>我说我要去找老师，我爸把门锁了。我的手机也被拿走了。我现在用旧电脑发的。</p><p style={{fontWeight:800}}>救救我。我真的很害怕。</p><div style={{marginTop:14,paddingTop:10,borderTop:"1px solid #d4cec3",color:"#777",fontSize:11}}>删除操作：旧档员-03　·　公开区后续发言：0　·　内部标签：低龄 / 家庭接触中</div></div>}</section>
}
function Recycle(){return <><h2>删除记录</h2><div style={s.adminPanel}><Record date="2026-10-16 18:31" title="未发布草稿" meta="候鸟第七年 · 已删除" text="原始内容已删除；镜像保留。"/><Record date="2026-10-16 20:47" title="IMG_1016_2047.jpg" meta="现场终端 03" text="上传 20:47；原始文件已删除；缓存缩略图可用。"/><RitualPhoto/><DeletedRescuePost/><Record date="2013-07-09 03:14" title="旧教页缓存" meta="旧档恢复 · 已删除" text="页面文件已删除；缓存图像与文字层仍可读。"/><figure style={s.scripture}><img src="assets/occult/huanzhen-scripture-v904.webp" alt="无相还真会黑底朱字旧教页"/></figure></div></>}
'''
s = replace_between(s, 'function Recycle(){', 'function RitualPhoto(){', new_recycle + 'function RitualPhoto(){', 'recycle with deleted rescue post')
p.write_text(s)


# ---- Public forum: ordinary child-help post, no cult vocabulary ----
p = Path("content/gameDataFlowV2.ts")
s = p.read_text()
new_public = r'''const thresholdNamePost:Post={
 id:"34106",title:"我爸妈最近有点奇怪，是我想太多了吗",author:"小雨伞",date:"2011-08-23 22:16",board:"生活求助",views:1942,excerpt:"楼主说父母最近突然收起旧照片、不太叫自己的名字，晚上家里还会来不认识的人。版主认为暂时看不出灵异因素。",terms:["爸妈","害怕","照片","名字","陌生人","生活求助"],highlights:[],
 body:["我今年初一。不知道发这里对不对，先别笑我。最近我爸妈突然变得很奇怪。","他们把家里以前的照片都收起来了，连我小时候的相册也不让我碰。最近也很少叫我名字，喊我过去的时候就说‘过来’。我问为什么，他们说只是家里的规矩。","这几天晚上总有人来我家，我不认识。他们把客厅灯关得很暗，让我回房间。有一次我出来喝水，听见他们一直重复一句话，但是我没听清。","我妈发现我以后特别生气，后来又抱着我说不要怕，说‘过段时间你就不会害怕了’。我现在一到晚上就不想回家。这个真的只是我想多了吗？"],
 replies:[reply("雨棚下","22:28","先别自己吓自己。大人突然收东西也可能是家里出了别的事。你有没有能信得过的亲戚？"),reply("夜班公交","22:34","如果你真的是未成年人，别在公开论坛发学校、住址和真名。觉得不安全就先找老师。"),reply("旧档员-03","22:41","目前描述看不出与灵异事件有关。不要公开个人信息；如果家里的情况让你持续害怕，优先联系老师、亲属或其他可信任的成年人。","版主"),reply("小雨伞","22:47","好。我明天去找老师问问。谢谢。","楼主")]
};

'''
s = replace_between(s, 'const thresholdNamePost:Post={', 'const ritualFragmentPost:Post={', new_public + 'const ritualFragmentPost:Post={', 'replace public child-help post')
p.write_text(s)


# ---- Canon ----
p = Path("docs/CANON_v3.0_世界观与游戏设定唯一权威集.md")
s = p.read_text()
old = '''### 2.1 宗教露出与后台回访

- 公共论坛首页允许出现少量**表面是普通地方旧俗、实际与无相还真会教义同构**的帖子；前期不直接点名组织，不把论坛写成邪教群聊；
- 管理员后台增加“**诵录**”入口，用宗教日课形式呈现固定祝号与现行研究目标；
- 后台可明确：**真君无相，不应有定身**；现阶段的技术目标是验证同一客可在多具舍之间连续迁移并尽量保持记忆与主体连续，从而建立可重复的换舍路径；
- 仍不回答无相真君的原始身份、是否为同一古老魂、或是否只是宗教职位；
- 管理员后台内部提供“返回论坛”入口；首次成功登录后只记住账号 `旧档员-03`，**不保存密码**。再次进入时玩家只需自行输入 `gumen-0712`；若忘记，可重新走旧档兼容认证小游戏取得口令。
'''
new = '''### 2.1 宗教露出与后台回访

- 公共论坛不直接用“舍 / 客 / 无相还真会”等术语提示教义。可以出现看似普通的旧求助帖，例如未成年人描述父母突然收走旧照片、减少呼名、夜间接待陌生人；版主在公开区以正常、克制的口吻建议其联系可信任成年人；
- 后台“删除记录”可以翻出同一账号随后被删除的《救救我》，从而让玩家意识到前台被正常化处理的求助背后存在真实危险；
- 管理员后台从首次进入起即可看到“**诵录**”入口。首次打开时经文逐句高亮，最后由系统字体插入：**访问者徐宁，未登记候舍编号。** 随后仅“诵录”页面黑屏并永久失效；观察名单、用户查询、候舍库、操作记录、删除记录等后台主线功能必须继续可用；
- 候舍库与后台其他记录继续承担组织目的说明：**真君无相，不应有定身**；现阶段技术目标是验证同一客可在多具舍之间连续迁移并尽量保持记忆与主体连续，从而建立可重复的换舍路径；
- 仍不回答无相真君的原始身份、是否为同一古老魂、或是否只是宗教职位；
- 管理员后台内部提供“返回论坛”入口；首次成功登录后只记住账号 `旧档员-03`，**不保存密码**。再次进入时玩家只需自行输入 `gumen-0712`；若忘记，可重新走旧档兼容认证小游戏取得口令。
'''
s = replace_once(s, old, new, 'canon horror rules')
p.write_text(s)
