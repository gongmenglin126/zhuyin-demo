from pathlib import Path
import json


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"missing target: {label}")
    return text.replace(old, new, 1)


def replace_map_value(text: str, key: str, new_value: str, label: str) -> str:
    qk=json.dumps(key,ensure_ascii=False)
    old=f"  {qk}:{qk},"
    new=f"  {qk}:{json.dumps(new_value,ensure_ascii=False)},"
    if old not in text:
        raise SystemExit(f"missing map target: {label}: {key}")
    return text.replace(old,new,1)

# ---------------------------------------------------------------------------
# 1. Forum: allegory for 再舍者，故门有声 + faceless devotional image post
# ---------------------------------------------------------------------------
p=Path('content/gameDataFlowV2.ts')
s=p.read_text()

old='''  terms:["三门疏","黑底红字","白纸抄本","残页","旧短偈"],\n  highlights:["《三门疏》","不是同一批扫描","来源字段都缺了"],'''
new='''  terms:["三门疏","黑底红字","白纸抄本","残页","旧短偈","再舍者","故门有声"],\n  highlights:["《三门疏》","不是同一批扫描","来源字段都缺了","再舍者，故门有声"],'''
s=replace_once(s,old,new,'scripture terms')

old='''  replies:[\n    reply("旧档员-03","21:46","站内 2012 年前的附件索引不全，我只能确认这两组文件曾经在不同主题里出现过，原附件已失效。","版主"),\n    reply("纸页边角","22:08","如果文件编号和压缩方式都不同，我不会先当成一篇。可能只是后来的整理者觉得内容像，顺手放一起了。"),\n    reply("旧纸鸢","22:21","我也是这个意思。先把两组分开记，等找到更早来源再说。","楼主")\n  ],\n};'''
new='''  replies:[\n    reply("旧档员-03","21:46","站内 2012 年前的附件索引不全，我只能确认这两组文件曾经在不同主题里出现过，原附件已失效。","版主"),\n    reply("纸页边角","22:08","如果文件编号和压缩方式都不同，我不会先当成一篇。可能只是后来的整理者觉得内容像，顺手放一起了。另一个白纸残本边上还能辨出一句：‘再舍者，故门有声。’我一直没弄明白这里的‘故门’指什么。"),\n    reply("旧灶台","22:16","这句让我想起我外婆讲过的一个小故事。两个人借住两间旧屋，临走时互换了钥匙。很多年后，其中一个又搬进第三间屋；人明明已经走远了，第一回留下的那扇旧门却半夜自己响。外婆讲到这里总说‘人换了屋，旧门还认得旧客’。我看到‘再舍者，故门有声’第一反应就是这个。可能纯属我硬串，听个意思就行。"),\n    reply("旧纸鸢","22:29","这个比我硬拆字顺多了。先记在这里吧，至少能解释为什么写的是‘故门’，不是‘新门’。至于原文是不是这个意思，还是等更完整的页。","楼主")\n  ],\n};'''
s=replace_once(s,old,new,'scripture allegory replies')

idol_post='''\n\nconst facelessIdolPost:Post={\n  id:"32617",\n  title:"岚棉三厂4栋后面杂物间里这个没脸的木像是什么",\n  author:"一格胶片",\n  date:"2024-05-11 19:42",\n  board:"旧闻考据",\n  views:3112,\n  hidden:true,\n  excerpt:"拍旧厂房时在废弃杂物间门口看到一尊半米高的无面木像，旁边有烧剩的红蜡和几张翻扣的旧照片。",\n  terms:["岚棉三厂","4栋","杂物间","木像","神像","无面","红蜡","旧照片"],\n  highlights:["脸是平的","一层层刮痕","红蜡","旧照片","像门框的刻痕"],\n  body:[\n    "去年拍岚棉三厂旧家属区的时候，在4栋后面一排快塌的杂物间里看到这个。门只开了一条缝，我站在外面拍的，没进去。",\n    "东西大概四五十厘米高，看着像木头，也可能外面糊过黑泥。脸那里不是摔坏的，整块是平的，凑近能看见一层层刮痕，像原来刻过什么又反复磨掉。",\n    "身上缠了好几层已经发黑的旧布，每层领口的位置还不太一样。底下有两截烧剩的红蜡，旁边压着几张旧照片，全部反扣着。我没翻。",\n    "底座正面有一道很浅的刻痕，看着有点像门框，旁边像还有字，但原图放大也糊。以前厂区有人会在这种杂物间里供东西吗？我主要想问来源，不打算进去探险。"\n  ],\n  images:[{src:"assets/occult/factory-faceless-idol.svg",caption:"附件：IMG_20240511_1937.jpg · 4栋后侧杂物间门口"}],\n  replies:[\n    reply("三厂老住户","20:03","我小时候没见过。4栋后面那排以前就是堆煤球、扫帚和破桌椅的，谁家缺地方都往里塞东西。"),\n    reply("旧纸鸢","20:18","无面像不是一个固定神名，各地自制的供物太多了。单看这张照片认不出来。"),\n    reply("灰浆桶","20:31","我觉得最怪的不是没脸，是那张脸像雕过又磨掉。旁边那几张照片也挺膈应。"),\n    reply("一格胶片","20:44","对，我现场也觉得像磨过。就拍了这一张，里面太黑，而且地板已经塌了一块。","楼主"),\n    reply("旧档员-03","2016-02-12 02:11","如补传旧照片，请遮挡可识别的人脸与姓名。","版主")\n  ],\n};\n'''
s=replace_once(s,'\nconst reportBase=flowPosts.find(post=>post.id==="09114")!;',idol_post+'\nconst reportBase=flowPosts.find(post=>post.id==="09114")!;','insert faceless idol post')

old='export const posts:Post[]=[...patched,posterMemory,linSnackPost,linMarblePost,shenCandyPost,thresholdNamePost,ritualFragmentPost,adminAccountPost].sort((a,b)=>toRank(a.date)-toRank(b.date));'
new='export const posts:Post[]=[...patched,posterMemory,linSnackPost,linMarblePost,shenCandyPost,thresholdNamePost,ritualFragmentPost,adminAccountPost,facelessIdolPost].sort((a,b)=>toRank(a.date)-toRank(b.date));'
s=replace_once(s,old,new,'append faceless idol post')
p.write_text(s)

# SVG: deliberately looks like a dim old-phone photo, not an authoritative portrait.
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="640" viewBox="0 0 960 640">
<defs>
  <radialGradient id="v" cx="48%" cy="44%" r="72%"><stop offset="0" stop-color="#44433d"/><stop offset=".52" stop-color="#232421"/><stop offset="1" stop-color="#080909"/></radialGradient>
  <linearGradient id="wood" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#49352b"/><stop offset=".5" stop-color="#211a17"/><stop offset="1" stop-color="#0c0b0a"/></linearGradient>
  <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".72" numOctaves="3" seed="17"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="table" tableValues="0 .16"/></feComponentTransfer></filter>
  <filter id="blur"><feGaussianBlur stdDeviation="2.4"/></filter>
</defs>
<rect width="960" height="640" fill="url(#v)"/>
<path d="M0 420 L960 395 L960 640 L0 640Z" fill="#111210"/>
<path d="M82 0v421M117 0v418M840 0v405" stroke="#080909" stroke-width="17" opacity=".7"/>
<path d="M73 96H345M702 112h183" stroke="#6c6a5f" stroke-width="9" opacity=".22"/>
<path d="M162 155h176v194H162z" fill="#161715" stroke="#555148" opacity=".5"/>
<path d="M725 170h105v202H725z" fill="#10110f" stroke="#4b4a43" opacity=".45"/>
<!-- pedestal -->
<path d="M363 507h239l31 63H332z" fill="#171311" stroke="#554339" stroke-width="3"/>
<path d="M391 468h184l28 46H364z" fill="#2a211c" stroke="#6c5141" stroke-width="3"/>
<!-- layered robe -->
<path d="M438 286c-34 48-49 121-42 185h174c8-68-10-140-48-186z" fill="#161414" stroke="#463532" stroke-width="5"/>
<path d="M418 346c43 17 105 17 145-3" fill="none" stroke="#403332" stroke-width="15" opacity=".7"/>
<path d="M407 393c53 18 118 17 168-5" fill="none" stroke="#292525" stroke-width="17" opacity=".9"/>
<path d="M404 437c58 14 122 13 176-7" fill="none" stroke="#3b2f2e" stroke-width="13" opacity=".75"/>
<!-- neck + faceless head -->
<path d="M462 286v-31h62v32" fill="#2b211c" stroke="#513d32" stroke-width="4"/>
<path d="M431 176c9-52 109-58 126-2 12 40 0 102-53 112-52 10-88-42-73-110z" fill="url(#wood)" stroke="#5c4438" stroke-width="5"/>
<!-- erased-face scratches -->
<path d="M452 199c34-11 58-9 84-2M445 215c39-8 69-8 96 0M447 233c37-4 64-3 90 4M458 249c27-3 46-1 65 5" fill="none" stroke="#826657" stroke-width="4" opacity=".38"/>
<path d="M469 183l-10 78M493 178l-6 91M520 181l-14 82" stroke="#1a1412" stroke-width="3" opacity=".55"/>
<!-- door-like mark on base -->
<path d="M447 486v-31h72v31M459 486v-21h48v21" fill="none" stroke="#765446" stroke-width="4" opacity=".72"/>
<!-- red wax stubs -->
<path d="M336 471h23l4 58h-31zM605 465h22l7 62h-33z" fill="#5b1415"/>
<path d="M338 469c8-6 14-5 20 0M607 463c7-5 13-5 19 0" stroke="#a33d34" stroke-width="5"/>
<ellipse cx="348" cy="461" rx="8" ry="18" fill="#8f3b28" opacity=".45" filter="url(#blur)"/>
<!-- face-down old photos -->
<g opacity=".8" transform="rotate(-8 300 535)"><rect x="248" y="508" width="74" height="52" fill="#b1aa94"/><rect x="254" y="514" width="62" height="40" fill="#777263"/></g>
<g opacity=".72" transform="rotate(11 662 540)"><rect x="626" y="512" width="78" height="54" fill="#aaa38e"/><rect x="632" y="518" width="66" height="42" fill="#6d6a5e"/></g>
<g opacity=".55" transform="rotate(-2 700 494)"><rect x="671" y="475" width="58" height="43" fill="#908a78"/></g>
<!-- foreground door crack -->
<path d="M0 0h106v640H0zM875 0h85v640h-85z" fill="#050606" opacity=".88"/>
<rect width="960" height="640" filter="url(#grain)" opacity=".9"/>
<rect x="8" y="8" width="944" height="624" fill="none" stroke="#000" stroke-width="16" opacity=".35"/>
<text x="735" y="607" fill="#d7d7c6" opacity=".42" font-family="monospace" font-size="18">2024/05/11 19:37</text>
</svg>'''
asset=Path('public/assets/occult/factory-faceless-idol.svg')
asset.parent.mkdir(parents=True,exist_ok=True)
asset.write_text(svg)

# ---------------------------------------------------------------------------
# 2. Forum dialogue tone audit: soften unnecessary command-list cadence.
# ---------------------------------------------------------------------------
p=Path('content/forumDialogues.ts')
s=p.read_text()
forum_changes={
"先画结构，不要急着给梦里的人起名字。看稳定的是空间关系，还是你已经写进记录里的叙述。":"我会更看重结构。名字这块很容易被提示带着走，空间关系反而比较值得记。",
"“楠楠”也不一定是名字，可能是囡囡。音节先原样记，不要补汉字。":"“楠楠”也不一定真是名字，听成“囡囡”也说得通。最好把音节原样记下来，过几天再看。",
"如果只是做记录，可以慢慢来，不需要今晚得到结论。":"只是做记录的话慢慢来也行，这种东西今晚想不明白也正常。",
"模糊音别先写成字，直接记音节。":"这种模糊音我会直接记音节，写成字以后反而容易越看越像。",
"任何私信说认识你的人，都先核实公开记录。":"这种帖子私信会很多。真有人说认识你，公开记录能对上再聊比较稳。",
"先查事实，别被都市传说带偏。":"我觉得事实线更有用，都市传说一多很容易把人带跑。",
"把问题拆开：发生过什么、当时怎么描述、现在记得什么。三栏不要互相补答案。":"我会拆成三栏：发生过什么、当时怎么描述、现在记得什么。分开写比较不容易互相污染。",
"如果找到报纸，先拍整版，不要只截标题。":"如果真翻到报纸，整版一起拍下来吧。只留标题以后很难判断上下文。",
"别因为家人回避就默认他们有恶意。":"家里人回避也可能只是害怕重提，不一定能直接说明他们有恶意。",
"先找得到的物证，别先给感受下结论。":"能找到的物证更好用。感受先记着，等有东西能对上再判断。",
"先去楼顶看看水箱和增压泵。泵启动时楼板传声，听起来真像椅子腿。":"楼顶要是有水箱和增压泵可以看看。泵启动时楼板传声，听起来真挺像椅子腿。",
"手机会自动压掉持续低频，别拿‘录不到’当证据。床脚垫块毛巾试试。":"手机对持续低频经常会自动压掉，所以录不到也说明不了什么。床脚垫块毛巾倒是可以试试。",
"八成。先别自己撬，排线比故事贵。":"八成。真想拆最好找会修的，老机器的排线可比这个故事贵。",
"样张能发吗？别压缩，我想看是不是 CCD 偏色。":"样张方便发一张吗？最好留原尺寸，我想看看是不是 CCD 偏色。",
"市图地方文献室，不一定数字化。带原图去，别只拿手机截图。":"市图地方文献室可能有，未必数字化。要去的话把原图也带上，手机截图细节不太够。",
"别在群里骂，骂了他们确认这个号是活人。截图群主、收款方、订阅页一起投诉。":"我反而不建议在群里骂，骂了等于告诉他们这个号是活人。群主、收款方和订阅页一起截图投诉比较省事。",
"先别喷水、别熨。连着墙灰一起用硬纸板托起来，夹无酸纸，平放阴干。":"这纸一碰就碎的话，喷水和熨烫风险都挺大。最好连墙灰一起用硬纸板托起来，夹无酸纸平放阴干。",
"分块可以，至少别把文字图当照片二次压缩。":"分块可以，文字图如果还按照片二次压缩就真看不清了。",
"晾衣架，根本承不了人。别照论坛传言写成逃生梯。":"那就是晾衣架，根本承不了人。论坛里传成逃生梯大概是后来加戏。",
"体重别涨太快，按医生给的量喂。尾巴盖脸不用治疗，人换个方向即可。":"体重控制一下，按医生给的量喂就行。尾巴盖脸不用治疗，人换个方向即可。",
"最靠谱的还是纸表。软件自动判断入睡没你想的准，半夜醒了也别开手机。":"最靠谱的还是纸表。软件自动判断入睡没你想的准，半夜醒了越看手机越清醒。",
"消费明细没戏。发卡面和路线经过的地标吧，别把完整卡号拍出来。":"消费明细没戏。发卡面和路线经过的地标吧，卡号记得遮住。",
}
for k,v in forum_changes.items():
    s=replace_map_value(s,k,v,'forum tone')
# new post / allegory copy entries kept centralized for later tweaking
new_forum_strings=[
"另一个白纸残本边上还能辨出一句：‘再舍者，故门有声。’我一直没弄明白这里的‘故门’指什么。",
"这句让我想起我外婆讲过的一个小故事。两个人借住两间旧屋，临走时互换了钥匙。很多年后，其中一个又搬进第三间屋；人明明已经走远了，第一回留下的那扇旧门却半夜自己响。外婆讲到这里总说‘人换了屋，旧门还认得旧客’。我看到‘再舍者，故门有声’第一反应就是这个。可能纯属我硬串，听个意思就行。",
"这个比我硬拆字顺多了。先记在这里吧，至少能解释为什么写的是‘故门’，不是‘新门’。至于原文是不是这个意思，还是等更完整的页。",
"岚棉三厂4栋后面杂物间里这个没脸的木像是什么",
"拍旧厂房时在废弃杂物间门口看到一尊半米高的无面木像，旁边有烧剩的红蜡和几张翻扣的旧照片。",
"去年拍岚棉三厂旧家属区的时候，在4栋后面一排快塌的杂物间里看到这个。门只开了一条缝，我站在外面拍的，没进去。",
"东西大概四五十厘米高，看着像木头，也可能外面糊过黑泥。脸那里不是摔坏的，整块是平的，凑近能看见一层层刮痕，像原来刻过什么又反复磨掉。",
"身上缠了好几层已经发黑的旧布，每层领口的位置还不太一样。底下有两截烧剩的红蜡，旁边压着几张旧照片，全部反扣着。我没翻。",
"底座正面有一道很浅的刻痕，看着有点像门框，旁边像还有字，但原图放大也糊。以前厂区有人会在这种杂物间里供东西吗？我主要想问来源，不打算进去探险。",
"我小时候没见过。4栋后面那排以前就是堆煤球、扫帚和破桌椅的，谁家缺地方都往里塞东西。",
"无面像不是一个固定神名，各地自制的供物太多了。单看这张照片认不出来。",
"我觉得最怪的不是没脸，是那张脸像雕过又磨掉。旁边那几张照片也挺膈应。",
"对，我现场也觉得像磨过。就拍了这一张，里面太黑，而且地板已经塌了一块。",
"如补传旧照片，请遮挡可识别的人脸与姓名。",
"附件：IMG_20240511_1937.jpg · 4栋后侧杂物间门口",
]
insert=''.join(f'  {json.dumps(x,ensure_ascii=False)}:{json.dumps(x,ensure_ascii=False)},\n' for x in new_forum_strings)
s=replace_once(s,'};\n\nexport const editForumText',insert+'};\n\nexport const editForumText','forum new copy map')
p.write_text(s)

# ---------------------------------------------------------------------------
# 3. WeChat tone audit: keep threats hard; soften friendly/helper command cadence.
# ---------------------------------------------------------------------------
p=Path('content/wechatLiveDialogues.ts')
s=p.read_text()
wechat_changes={
"别自己去。报警，把后台记录和这个地址一起交出去。":"地址有了。报警吧，把后台记录和这个地址一起交出去。你一个人过去太危险了。",
"先别看名字。":"名字先放一边，我觉得客编号更关键。",
"对。两个人都报。别自己过去。":"对，两个人都报。你自己过去我不放心。",
"对。两个人都报。你别自己去。":"对，两个人都报。你自己过去我不放心。",
"好。截图别漏，地址和批次都给他们。":"好。地址、批次和截图一起给他们，省得漏信息。",
"你继续看，别停。":"你继续看，我这边没事。",
"那先别管我这边。":"我这边先不用管，你找沈妍。",
}
for k,v in wechat_changes.items():
    s=replace_map_value(s,k,v,'wechat tone')
p.write_text(s)

# ---------------------------------------------------------------------------
# 4. Admin: true-name attack, stronger True Lord purpose, liturgy devotion line.
# ---------------------------------------------------------------------------
p=Path('app/AdminPortalOccult.tsx')
s=p.read_text()

old=''' const [detail,setDetail]=useState<AdminDetail>(()=>adminDeskSession.detail);\n const [caseLevel,setCaseLevel]=useState(()=>adminCaseLevel);'''
new=''' const [detail,setDetail]=useState<AdminDetail>(()=>adminDeskSession.detail);\n const [caseLevel,setCaseLevel]=useState(()=>adminCaseLevel);\n const [trueNameAttack,setTrueNameAttack]=useState(false);\n useEffect(()=>{if(!trueNameAttack)return;const timer=window.setTimeout(()=>setTrueNameAttack(false),4200);return ()=>window.clearTimeout(timer)},[trueNameAttack]);'''
s=replace_once(s,old,new,'admin true name state')

old=''' const doSearch=(e?:FormEvent)=>{e?.preventDefault();const raw=q.trim();const t=raw.replace(/客|编号|[-_\\s]/g,"");setSearched(true);if(/^LN20040718$/i.test(t))'''
new=''' const doSearch=(e?:FormEvent)=>{e?.preventDefault();const raw=q.trim();const t=raw.replace(/客|编号|[-_\\s]/g,"");if(/无相真君/.test(raw)){setDetail(null);setSearched(false);setTrueNameAttack(true);return}setSearched(true);if(/^LN20040718$/i.test(t))'''
s=replace_once(s,old,new,'admin true name search hook')

old='''   </section>\n  </div>\n </main>;\n}\n\nlet liturgyBurned=false;'''
attack='''   </section>\n  </div>\n  {trueNameAttack&&<TrueNameAttack/>}\n </main>;\n}\n\nfunction TrueNameAttack(){\n const words=Array.from({length:38},(_,i)=>({left:`${3+(i*37)%92}%`,top:`${2+(i*53)%94}%`,size:18+(i%7)*8,rot:-16+(i%9)*4,delay:(i%11)*-.07}));\n return <section style={{position:"fixed",inset:0,zIndex:12000,overflow:"hidden",background:"radial-gradient(circle at 50% 50%,#220000 0,#090000 42%,#000 82%)",cursor:"default"}}>\n  <style>{`@keyframes trueNameHit{0%{opacity:.12;filter:blur(2px);transform:translate(-50%,-50%) scale(.82)}45%{opacity:.96;filter:blur(0);transform:translate(-50%,-50%) scale(1.12)}100%{opacity:.32;filter:blur(.7px);transform:translate(-50%,-50%) scale(.98)}}`}</style>\n  {words.map((w,i)=><span key={i} style={{position:"absolute",left:w.left,top:w.top,color:i%5===0?"#f0d8d3":"#9f1118",fontFamily:'STKaiti,KaiTi,"FangSong",serif',fontSize:w.size,fontWeight:900,whiteSpace:"nowrap",letterSpacing:".08em",textShadow:"0 0 12px #b00000,2px 2px 0 #240000",rotate:`${w.rot}deg`,animation:`trueNameHit .62s ${w.delay}s infinite alternate`}}>{editAdminText("误呼吾主真名")}</span>)}\n  <strong style={{position:"absolute",left:"50%",top:"50%",transform:"translate(-50%,-50%)",width:"100%",textAlign:"center",color:"#d8c1ba",font:'900 clamp(34px,7vw,104px) STKaiti,KaiTi,"FangSong",serif',letterSpacing:".16em",textShadow:"0 0 35px #c00000,5px 5px 0 #220000"}}>{editAdminText("误呼吾主真名")}</strong>\n </section>;\n}\n\nlet liturgyBurned=false;'''
s=replace_once(s,old,attack,'insert true name attack component')

old='''   window.setTimeout(()=>setStep(5),5900),\n   window.setTimeout(()=>{liturgyBurned=true;setStep(99)},7600),'''
new='''   window.setTimeout(()=>setStep(5),5900),\n   window.setTimeout(()=>setStep(6),6900),\n   window.setTimeout(()=>{liturgyBurned=true;setStep(99)},8400),'''
s=replace_once(s,old,new,'liturgy timing')

old='''  {step>=5&&<><div style={{position:"absolute",inset:0,background:"#000e",boxShadow:"inset 0 0 220px #000",transition:"background .18s ease"}}/><div style={{position:"absolute",left:"50%",top:"50%",transform:"translate(-50%,-50%)",width:"min(980px,90vw)",padding:"12px 18px",boxSizing:"border-box",color:"#eeeeee",font:"700 clamp(18px,2.2vw,30px) ui-monospace,SFMono-Regular,Consolas,monospace",letterSpacing:".075em",lineHeight:1.5,textAlign:"center",textShadow:"0 0 16px #ffffff21"}}>{editAdminText("访问者徐宁，未登记候舍编号。")}</div></>}'''
new='''  {step===5&&<><div style={{position:"absolute",inset:0,background:"#000e",boxShadow:"inset 0 0 220px #000",transition:"background .18s ease"}}/><div style={{position:"absolute",left:"50%",top:"50%",transform:"translate(-50%,-50%)",width:"min(980px,90vw)",padding:"12px 18px",boxSizing:"border-box",color:"#eeeeee",font:"700 clamp(18px,2.2vw,30px) ui-monospace,SFMono-Regular,Consolas,monospace",letterSpacing:".075em",lineHeight:1.5,textAlign:"center",textShadow:"0 0 16px #ffffff21"}}>{editAdminText("访问者徐宁，未登记候舍编号。")}</div></>}\n  {step>=6&&step!==99&&<><div style={{position:"absolute",inset:0,background:"#000f",boxShadow:"inset 0 0 240px #000"}}/><div style={{position:"absolute",left:"50%",top:"50%",transform:"translate(-50%,-50%) rotate(-1deg)",width:"min(1100px,92vw)",color:"#b3131b",font:'900 clamp(34px,6.4vw,94px) STKaiti,KaiTi,"FangSong",serif',letterSpacing:".12em",textAlign:"center",textShadow:"0 0 9px #e019206e,3px 3px 0 #310000"}}>{editAdminText("一切献给无相真君。")}</div></>}'''
s=replace_once(s,old,new,'liturgy devotion line')

old=''' <section style={s.adminPanel}><h4>归真序列 · 阶段 II</h4><Record date="前置验证" title="长期客二次再舍稳定" meta="RS-2026-1012" text="客α作为当前长期样本。二次再舍已完成；旧对契异常尚未关闭。"/><Record date="候舍池" title="来源充足" meta="匹配可用 37 / 待执行 12" text="现阶段不批准以强制方式补充普通候舍。"/><Record date="真君序列" title="暂缓启用" meta="待长期客验证通过" text="连续再舍稳定性未达到启用条件。旧客验证完成后重新评估。"/></section>'''
new=''' <section style={s.adminPanel}><h4>归真序列 · 阶段 II</h4><Record date="序列目标" title="无相真君连续更舍" meta="真君无相，不应有定身" text="验证同一客在多具舍之间连续迁移后，记忆与主体能否维持；若成立，则建立供无相真君反复更舍的长期序列。"/><Record date="前置验证" title="长期客二次再舍稳定" meta="RS-2026-1012" text="客α作为当前长期样本。二次再舍已完成；旧对契异常尚未关闭。"/><Record date="候舍池" title="来源充足" meta="匹配可用 37 / 待执行 12" text="现阶段不批准以强制方式补充普通候舍。"/><Record date="真君序列" title="暂缓启用" meta="待长期客验证通过" text="连续再舍稳定性未达到启用条件。旧客验证完成后重新评估。"/></section>'''
s=replace_once(s,old,new,'true lord sequence purpose')
p.write_text(s)

# Admin centralized strings
p=Path('content/adminDialogues.ts')
s=p.read_text()
admin_new=[
"误呼吾主真名",
"一切献给无相真君。",
"序列目标",
"无相真君连续更舍",
"真君无相，不应有定身",
"验证同一客在多具舍之间连续迁移后，记忆与主体能否维持；若成立，则建立供无相真君反复更舍的长期序列。",
]
insert=''.join(f'  {json.dumps(x,ensure_ascii=False)}:{json.dumps(x,ensure_ascii=False)},\n' for x in admin_new)
s=replace_once(s,'};\n\nexport const editAdminText',insert+'};\n\nexport const editAdminText','admin new copy map')
p.write_text(s)

# ---------------------------------------------------------------------------
# 5. Endings: every ending opens with a local news report before subjective coda.
# ---------------------------------------------------------------------------
p=Path('app/GameEnding.tsx')
s=p.read_text()
old='''export default function GameEnding({kind}:{kind:Exclude<EndingKind,null>}){\n const [step,setStep]=useState(0);\n useEffect(()=>delaySteps(setStep,kind==="home"?8:kind==="true"?11:10,kind==="true"?1350:1500),[kind]);\n return <div style={s.cover}>{kind==="home"?<HomeEnding step={step}/>:kind==="true"?<TrueEnding step={step}/>:<DoubleEnding step={step}/>}</div>;\n}'''
new='''export default function GameEnding({kind}:{kind:Exclude<EndingKind,null>}){\n const [step,setStep]=useState(0);\n const [newsOpen,setNewsOpen]=useState(true);\n useEffect(()=>{if(newsOpen)return;return delaySteps(setStep,kind==="home"?8:kind==="true"?11:10,kind==="true"?1350:1500)},[kind,newsOpen]);\n return <div style={s.cover}>{newsOpen?<IncidentNews kind={kind} onClose={()=>setNewsOpen(false)}/>:kind==="home"?<HomeEnding step={step}/>:kind==="true"?<TrueEnding step={step}/>:<DoubleEnding step={step}/>}</div>;\n}'''
s=replace_once(s,old,new,'ending news gate')

old='''function DesktopShell({children,date="10月20日 周二 22:41"}:{children:ReactNode;date?:string}){\n return <div style={s.desktop}><div style={s.sys}><span><b>●</b> 微信</span><span>Wi‑Fi　80%　{date}</span></div>{children}</div>;\n}\nfunction WechatFrame'''
news_component='''function DesktopShell({children,date="10月20日 周二 22:41"}:{children:ReactNode;date?:string}){\n return <div style={s.desktop}><div style={s.sys}><span><b>●</b> 微信</span><span>Wi‑Fi　80%　{date}</span></div>{children}</div>;\n}\n\nconst endingNews={\n home:{date:"2026年10月18日",headline:"北郊仓储区一处非法拘禁点被查处　一名失联女子获救",lead:"警方根据市民提供的网络记录与场地编号，于17日晚对河临北郊第三仓储区4号库展开处置。",body:"现场救出一名此前失联的成年女性，并查获多台电脑、身份档案、采样器材及大量旧纸质资料。警方称案件仍在调查，暂未公布涉案人员身份及具体案情。获救人员已接受检查，家属已取得联系。"},\n true:{date:"2026年10月18日",headline:"北郊仓储区非法拘禁案：两名被控制人员获救",lead:"警方在4号库及相邻隔离间发现两名成年女性，其中一人的登记身份与现场档案存在异常。",body:"两人均无生命危险。警方同时带走多台终端和纸质档案，并表示将核查更多历史记录。因其中一名获救者目前无法稳定陈述姓名与经历，相关身份信息暂不公开。"},\n double:{date:"2026年10月20日",headline:"两名短暂失联女子已自行返家　警方终止公开寻人",lead:"此前先后失联的两名成年女性于20日返回住处，并分别与亲友取得联系。",body:"两人均表示离开期间未遭限制人身自由，也不愿继续接受媒体采访。警方称现阶段未发现需要继续公开协查的情况。有关网络传言暂无证据支持。"},\n} as const;\nfunction IncidentNews({kind,onClose}:{kind:Exclude<EndingKind,null>;onClose:()=>void}){\n const item=endingNews[kind];\n return <div style={s.newsStage}><article style={s.newsPaper}>\n  <header style={s.newsTop}><span>{editEndingText(item.date)}　星期日</span><span>河临 · 电子版</span></header>\n  <div style={s.newsMast}>{editEndingText("河临晚报")}</div>\n  <div style={s.newsSection}>{editEndingText("社会 · 本地")}</div>\n  <h1 style={s.newsHeadline}>{editEndingText(item.headline)}</h1>\n  <p style={s.newsLead}>{editEndingText(item.lead)}</p>\n  <div style={s.newsRule}/>\n  <p style={s.newsBody}>{editEndingText(item.body)}</p>\n  <small style={s.newsSource}>{editEndingText("来源：河临晚报电子版 · 案件信息以警方后续通报为准")}</small>\n  <button onClick={onClose} style={s.newsClose}>{editEndingText("关闭报道")}</button>\n </article></div>;\n}\nfunction WechatFrame'''
s=replace_once(s,old,news_component,'insert incident news')

old='''const s:Record<string,CSSProperties>={\n cover:{position:"fixed",inset:0,zIndex:10000,background:"#050505",color:"#eee",userSelect:"none"},'''
new='''const s:Record<string,CSSProperties>={\n cover:{position:"fixed",inset:0,zIndex:10000,background:"#050505",color:"#eee",userSelect:"none"},\n newsStage:{position:"absolute",inset:0,display:"grid",placeItems:"center",padding:"4vh 5vw",boxSizing:"border-box",background:"radial-gradient(circle at 50% 28%,#403d36 0,#1b1a18 46%,#090909 100%)"},\n newsPaper:{position:"relative",width:"min(880px,92vw)",maxHeight:"88vh",overflow:"auto",boxSizing:"border-box",padding:"26px 38px 34px",background:"#eee9dc",color:"#1b1b18",border:"1px solid #aaa28f",boxShadow:"0 28px 100px #000c",fontFamily:'Georgia,"Songti SC","SimSun",serif'},\n newsTop:{display:"flex",justifyContent:"space-between",paddingBottom:8,borderBottom:"1px solid #8d8779",fontSize:11,color:"#666052"},\n newsMast:{padding:"13px 0 8px",borderBottom:"4px double #37352f",textAlign:"center",fontSize:42,fontWeight:900,letterSpacing:".26em"},\n newsSection:{marginTop:18,fontSize:12,fontWeight:800,letterSpacing:".16em",color:"#736b5e"},\n newsHeadline:{margin:"10px 0 12px",fontSize:"clamp(28px,4vw,46px)",lineHeight:1.18,fontWeight:900,letterSpacing:".02em"},\n newsLead:{margin:"0 0 15px",fontSize:16,lineHeight:1.75,fontWeight:700,color:"#3b3934"},\n newsRule:{height:1,background:"#908878",margin:"15px 0"},\n newsBody:{margin:0,fontSize:15,lineHeight:2,textAlign:"justify",color:"#34322e"},\n newsSource:{display:"block",marginTop:22,paddingTop:11,borderTop:"1px solid #c2bbab",fontSize:10,color:"#847c6d"},\n newsClose:{position:"sticky",float:"right",bottom:0,marginTop:20,padding:"8px 15px",border:"1px solid #797266",background:"#24231f",color:"#f4efe3",fontSize:12,fontWeight:700,cursor:"pointer"},'''
s=replace_once(s,old,new,'ending news styles')
p.write_text(s)

# Ending centralized text
p=Path('content/endingDialogues.ts')
s=p.read_text()
ending_new=[
"河临晚报","社会 · 本地","关闭报道","来源：河临晚报电子版 · 案件信息以警方后续通报为准",
"2026年10月18日","2026年10月20日",
"北郊仓储区一处非法拘禁点被查处　一名失联女子获救",
"警方根据市民提供的网络记录与场地编号，于17日晚对河临北郊第三仓储区4号库展开处置。",
"现场救出一名此前失联的成年女性，并查获多台电脑、身份档案、采样器材及大量旧纸质资料。警方称案件仍在调查，暂未公布涉案人员身份及具体案情。获救人员已接受检查，家属已取得联系。",
"北郊仓储区非法拘禁案：两名被控制人员获救",
"警方在4号库及相邻隔离间发现两名成年女性，其中一人的登记身份与现场档案存在异常。",
"两人均无生命危险。警方同时带走多台终端和纸质档案，并表示将核查更多历史记录。因其中一名获救者目前无法稳定陈述姓名与经历，相关身份信息暂不公开。",
"两名短暂失联女子已自行返家　警方终止公开寻人",
"此前先后失联的两名成年女性于20日返回住处，并分别与亲友取得联系。",
"两人均表示离开期间未遭限制人身自由，也不愿继续接受媒体采访。警方称现阶段未发现需要继续公开协查的情况。有关网络传言暂无证据支持。",
]
insert=''.join(f'  {json.dumps(x,ensure_ascii=False)}:{json.dumps(x,ensure_ascii=False)},\n' for x in ending_new)
s=replace_once(s,'};\n\nexport const editEndingText',insert+'};\n\nexport const editEndingText','ending new copy map')
p.write_text(s)

# ---------------------------------------------------------------------------
# 6. Canon: lock the new presentation decisions without defining True Lord ontology.
# ---------------------------------------------------------------------------
p=Path('docs/CANON_v3.0_世界观与游戏设定唯一权威集.md')
s=p.read_text()
old='''- 管理员后台从首次进入起即可看到“**诵录**”入口。首次打开时经文逐句高亮，最后由系统字体插入：**访问者徐宁，未登记候舍编号。** 随后仅“诵录”页面黑屏并永久失效；观察名单、用户查询、候舍库、操作记录、删除记录等后台主线功能必须继续可用；'''
new='''- 管理员后台从首次进入起即可看到“**诵录**”入口。首次打开时经文逐句高亮，系统字体插入：**访问者徐宁，未登记候舍编号。** 随后追加信徒式短句：**一切献给无相真君。** 再仅使“诵录”页面黑屏并永久失效；观察名单、用户查询、候舍库、操作记录、删除记录等后台主线功能必须继续可用；\n- 管理员后台主动搜索 **无相真君** 时，不返回普通档案结果，而以满屏重复的 **误呼吾主真名** 短暂覆盖后台；该效果只承担宗教压迫感，不新增超自然规则或支线；'''
s=replace_once(s,old,new,'canon liturgy/search')

old='''玩家只需确认：现代组织确实在为“真君连续再舍”做长期验证。'''
new='''玩家只需确认：现代组织确实在为“真君连续再舍”做长期验证。\n\n游戏后台必须把实验目的明确露出：验证同一“客”能否在多具“舍”之间连续迁移并尽量保持记忆与主体连续；若验证成立，则用于建立供无相真君反复更舍的长期序列。\n\n组织现行供奉图像允许使用**无面人形像**：脸部像被反复刮除、磨平，外裹多层旧布，可伴随红蜡、翻扣旧照片与门形刻痕。岚棉三厂普通旧闻帖可出现一尊此类旧像。该图像是教团的供奉符号，**不等于确认无相真君真实外貌**。'''
s=replace_once(s,old,new,'canon true lord iconography')

needle='''6. **整部游戏包括三个结局都只能通过沈妍这台电脑呈现。** 不切徐宁手机、19-07设备、警方现场、医院现场或上帝视角。'''
repl=needle+'\n7. 三个最终结局在进入人物主观余波前，先通过沈妍电脑显示一则河临本地新闻/案件报道，确认当次事件在现实社会中的外部结果；随后再进入微信、草稿、录音等结局主体。'
s=replace_once(s,needle,repl,'canon ending news')
p.write_text(s)

print('final polish patch applied')
