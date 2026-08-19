from pathlib import Path

# Admin: keep a natural breadcrumb, use searchable guest IDs for identity continuity.
p=Path('app/AdminPortalOccult.tsx')
s=p.read_text()

s=s.replace('type AdminDetail="pair2004"|"lin"|"reswap"|"third"|"sync"|null;',
'''type AdminDetail="pair2004"|"lin"|"reswap"|"third"|"sync"|"guestA"|"guestB"|"guestG"|null;''',1)

old=''' const items=[
  {label:"沈妍",sub:"徐宁认识的朋友 · A侧登记身体",go:openShen},
  {label:"2004旧案",sub:"LN-2004-0718 · A/B双向易舍",go:()=>openDetail("pair2004")},
  {label:"林楠",sub:"B侧登记身体",go:()=>openDetail("lin")},
  {label:"2026再舍",sub:"RS-2026-1012 · B侧 / 19-07",go:()=>openDetail("reswap")},
  {label:"同步异常",sub:"AN-0712-1012 · 沈妍A侧",go:()=>openDetail("sync")},
  {label:"19-07",sub:"第三名成年候舍对象",go:()=>openDetail("third")},
 ];
 return <section style={s.caseTrail}><b style={s.caseTitle}>关联对象</b><div style={s.caseGrid}>{items.filter((_,i)=>i<=level).map((x,i)=><button key={x.label} onClick={x.go} style={s.caseButton}><strong>{x.label}</strong><small>{x.sub}</small></button>)}</div>{level>=2&&<div style={s.identityLegend}><b>对象口径</b><span><strong>沈妍</strong>＝A侧登记身体／徐宁认识的朋友</span><span><strong>林楠</strong>＝B侧登记身体</span><span><strong>19-07</strong>＝第三名成年候舍对象</span><small>后台页面标题按“舍”的登记身份命名；“客源”单独记录，不等于页面标题里的姓名。</small></div>}</section>'''
new=''' const items=[
  {label:"沈妍",sub:"用户档案 · 0712-4471",go:openShen},
  {label:"2004旧案",sub:"LN-2004-0718",go:()=>openDetail("pair2004")},
  {label:"林楠",sub:"关联对象",go:()=>openDetail("lin")},
  {label:"2026再舍",sub:"RS-2026-1012",go:()=>openDetail("reswap")},
  {label:"同步异常",sub:"AN-0712-1012",go:()=>openDetail("sync")},
  {label:"19-07",sub:"候舍对象",go:()=>openDetail("third")},
 ];
 return <section style={s.caseTrail}><b style={s.caseTitle}>已查到的关联记录</b><div style={s.caseGrid}>{items.filter((_,i)=>i<=level).map(x=><button key={x.label} onClick={x.go} style={s.caseButton}><strong>{x.label}</strong><small>{x.sub}</small></button>)}</div></section>'''
assert old in s
s=s.replace(old,new,1)

# Search accepts guest identifiers.
old=''' const doSearch=(e?:FormEvent)=>{e?.preventDefault();const t=q.trim();setSearched(true);if(/^LN-2004-0718$/i.test(t)){setDetail("pair2004");raise(2);return}if(/^RS-2026-1012$/i.test(t)){setDetail("reswap");raise(5);return}if(/^AN-0712-1012$/i.test(t)){setDetail("sync");raise(5);return}if(/^19-07$/i.test(t)){setDetail("third");raise(5);return}setDetail(null);if(/候鸟第七年|沈妍|0712-4471/.test(t)){raise(1);fireShenBeat()}if(/林楠/.test(t))raise(3)};'''
new=''' const doSearch=(e?:FormEvent)=>{e?.preventDefault();const raw=q.trim();const t=raw.replace(/客|编号|[-_\\s]/g,"");setSearched(true);if(/^LN20040718$/i.test(t)){setDetail("pair2004");raise(2);return}if(/^RS20261012$/i.test(t)){setDetail("reswap");raise(5);return}if(/^AN07121012$/i.test(t)){setDetail("sync");raise(5);return}if(/^1907$/i.test(t)){setDetail("third");raise(5);return}if(t==="α"){setDetail("guestA");raise(5);return}if(t==="β"){setDetail("guestB");raise(5);return}if(t==="γ"){setDetail("guestG");raise(5);return}setDetail(null);if(/候鸟第七年|沈妍|07124471/.test(t)){raise(1);fireShenBeat()}if(/林楠/.test(t))raise(3)};'''
assert old in s
s=s.replace(old,new,1)
s=s.replace('placeholder="姓名 / UID / 记录编号"','placeholder="姓名 / UID / 记录编号 / 客编号"',1)

# Guest record routing.
old=''' if(detail==="third")return <ThirdRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>;
 return <SyncRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>;'''
new=''' if(detail==="third")return <ThirdRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>;
 if(detail==="guestA")return <GuestRecord id="α"/>;
 if(detail==="guestB")return <GuestRecord id="β"/>;
 if(detail==="guestG")return <GuestRecord id="γ"/>;
 return <SyncRecord onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>;'''
assert old in s
s=s.replace(old,new,1)

# 2004 post-swap record uses stable guest IDs.
s=s.replace('''<Record date="A侧" title="登记身体：沈妍" meta="客源：林楠" text="易舍完成；页面仍按登记身体‘沈妍’归档。"/><Record date="B侧" title="登记身体：林楠" meta="客源：沈妍" text="易舍完成；页面仍按登记身体‘林楠’归档。"/>''',
'''<Record date="A" title="舍：沈妍" meta="客编号：β" text="易舍完成；返家后持续观察。"/><Record date="B" title="舍：林楠" meta="客编号：α" text="易舍完成；返家后持续观察。"/>''',1)

# Lin record preserves guest alpha continuity.
s=s.replace('''<Record date="2004-07" title="双向易舍" meta="LN-2004-0718" text="B侧长期观察；稳定期 22 年。"/><Record date="2026-10-12" title="执行记录" meta="RS-2026-1012" text="状态：完成。"/>''',
'''<Record date="2004-07" title="双向易舍" meta="客编号：α" text="易舍后长期观察；稳定期 22 年。"/><Record date="2026-10-12" title="再舍记录" meta="RS-2026-1012" text="客α再次转移；状态：完成。"/>''',1)

# 2026 record is a clean before/after ledger.
s=s.replace('''<Record date="选择" title="B侧：林楠登记身体" meta="旧客稳定期 22 年" text="2004年后B侧长期稳定；候舍对象19-07为第三名成年对象，匹配通过。"/>''',
'''<Record date="执行前" title="林楠" meta="客编号：α" text="该客自2004年起持续稳定22年；列入连续易舍样本。"/><Record date="执行前" title="19-07" meta="客编号：γ" text="候舍对象；匹配通过。"/>''',1)
s=s.replace('''<Record date="结果" title="执行完成" meta="2026-10-12 22:13" text="B侧旧客转入19-07舍；19-07原客转入B侧舍。随后A侧沈妍出现原对契同步异常。"/>''',
'''<Record date="执行后" title="林楠" meta="客编号：γ" text="生命体征稳定。"/><Record date="执行后" title="19-07" meta="客编号：α" text="生命体征稳定；随后出现身份陈述异常。"/><Record date="结果" title="再舍完成" meta="2026-10-12 22:13" text="原对契随后出现同步异常。"/>''',1)

# Sync page answers why Shen Yan was captured, without an author tutorial.
s=s.replace('''<Record date="处置理由" title="控制A侧：沈妍" meta="执行 HN-1016-02" text="B侧（林楠登记身体）完成再舍后，A侧沈妍同步反应持续升高，可能影响试验稳定性；因此控制沈妍。沈妍不是本次再舍对象。"/>''',
'''<Record date="处置理由" title="控制旧对契另一端" meta="对象：0712-4471 · 沈妍" text="10月12日再舍完成后，该对象同步反应持续升高，可能影响试验稳定性；10月16日转入控制。"/>''',1)

# 19-07 carries alpha after the second transfer.
s=s.replace('''<header style={s.userHead}><i>19</i><span><h3>候舍对象 19-07</h3><small>成人候舍库 · 自愿对象</small></span><em>隔离</em></header>''',
'''<header style={s.userHead}><i>19</i><span><h3>候舍对象 19-07</h3><small>当前客编号：α · 成人候舍库</small></span><em>隔离</em></header>''',1)

# Searchable guest ledger. It records continuity but does not label a metaphysical 'real identity'.
anchor='''function SyncRecord({onCopyMaterial,hasMaterial}:{onCopyMaterial?:(m:SharedMaterial)=>void;hasMaterial?:(id:string)=>boolean})'''
assert anchor in s
guest='''function GuestRecord({id}:{id:"α"|"β"|"γ"}){\n const rows=id==="α"?[\n  ["2004-07-17","初始登记","沈妍"],["2004-07","易舍后所在","林楠"],["2026-10-12","再舍后所在","19-07"],\n ]:id==="β"?[\n  ["2004-07-18","初始登记","林楠"],["2004-07","易舍后所在","沈妍"],["2026-10-17","当前索引","沈妍"],\n ]:[\n  ["2026-09-28","初始登记","19-07"],["2026-10-12","再舍后所在","林楠"],["2026-10-17","当前索引","林楠"],\n ];\n return <article style={s.userRecord}><h2 style={{marginTop:0}}>客编号：{id}</h2><p style={s.subtle}>客档索引 · 仅记录登记与转移位置</p><section style={s.adminPanel}><h4>迁移记录</h4>{rows.map(([date,title,text])=><Record key={date+title} date={date} title={title} meta={`客 ${id}`} text={text}/>)}</section></article>\n}\n\n'''
s=s.replace(anchor,guest+anchor,1)

p.write_text(s)

# Liang: refer to repeated guest IDs, not A/B/body jargon.
p=Path('app/InteractiveWechat.tsx')
s=p.read_text()
s=s.replace('''"admin-sync-shen":{ly:[{text:"这份写得很清楚：被控制的是沈妍。"},{text:"触发原因是B侧再舍完成后，沈妍这边出现同步异常。别把‘谁做了第二次易舍’和‘谁被抓’混成一个人。"}],zc:[{text:"他们自己把这条标成了关联异常。"},{text:"‘控制’和执行批次比解释更重要。"}]},''',
'''"admin-sync-shen":{ly:[{text:"这条才是在解释沈妍为什么被抓。"},{text:"10月12号再舍完成以后，她这边的同步反应一直往上升；10月16号后台才把她转成‘已控制’。"}],zc:[{text:"他们自己把这条标成了关联异常。"},{text:"‘控制’和执行批次比解释更重要。"}]},''',1)
s=s.replace('''const correct:QuickReply={id:"ly-sync-right",text:"所以沈妍被抓，是因为B侧再舍后她这个旧对契另一端出了异常？",reply:[{text:"对。"},{text:"抓的是沈妍；做第二次易舍的是B侧‘林楠’那具登记身体。两件事不是同一个人。"},{text:"沈妍不是第二次试验的目标，她是试验后出现的异常，所以才被控制的。"},{text:"现在得找她被转到哪。"}]};''',
'''const correct:QuickReply={id:"ly-sync-right",text:"所以沈妍被抓，是因为那次再舍以后她这里出了同步异常？",reply:[{text:"对。"},{text:"时间能对上：12号再舍完成，沈妍这边开始异常；16号他们把她控制起来。"},{text:"所以抓沈妍不是为了再给她换一次，是为了处理试验冒出来的异常。"},{text:"现在得找她被转到哪。"}]};''',1)
s=s.replace('''const wrongAgain:QuickReply={id:"ly-sync-wrong-again",text:"所以他们抓沈妍，是准备再给沈妍换一次？",reply:[{text:"不是。沈妍这份写的是‘控制A侧旧对契另一端’，本次再舍对象在B侧。"}]};''',
'''const wrongAgain:QuickReply={id:"ly-sync-wrong-again",text:"所以他们抓沈妍，是准备再给她换一次？",reply:[{text:"我觉得不是。"},{text:"沈妍这份写的是‘控制旧对契另一端’，处置理由也是同步异常。"}]};''',1)
s=s.replace('''const nextAfterCorrect:QuickReply[]=received("ly","admin-reswap-2026")?reswapReasoningChoices(received("ly","admin-sync-shen")):[{id:"ly-pair-why",text:"那为什么2026年又把沈妍抓走？",reply:[{text:"对，这才是现在的问题。"},{text:"先分清：沈妍是A侧登记身体，林楠是B侧登记身体。2004只解释她们为什么有关联，还解释不了沈妍这次为什么被控制。"},{text:"要看B侧2026年的执行，再看沈妍自己的同步异常。"}]}];''',
'''const nextAfterCorrect:QuickReply[]=received("ly","admin-reswap-2026")?reswapReasoningChoices(received("ly","admin-sync-shen")):[{id:"ly-pair-why",text:"那为什么2026年又把沈妍抓走？",reply:[{text:"对，这才是现在的问题。"},{text:"2004这份只能说明她和林楠为什么会被绑在一起，还解释不了这次抓人。"},{text:"后面的再舍记录里客编号会重复出现，把那个编号对上就清楚多了。"}]}];''',1)
s=s.replace('''const correct:QuickReply={id:"ly-reswap-test",text:"他们在测试同一个‘客’能不能连续换身体？",reply:[{text:"对。"},{text:"而且这里做第二次易舍的是B侧，也就是‘林楠’这具登记身体，不是沈妍。"},{text:"稳定22年、再次易舍、主体稳定——这几个字段放一起就是这个意思。"}],next:includeSync?syncReasoningChoices():[]};''',
'''const correct:QuickReply={id:"ly-reswap-test",text:"他们在测试同一个‘客’能不能连续换身体？",reply:[{text:"对。"},{text:"2004林楠那页是客α，2026再舍以后19-07也变成客α。编号没变。"},{text:"稳定22年、再次易舍、主体稳定——这几个字段放一起就是这个意思。"},{text:"但这份还没解释沈妍为什么会被抓。"}],next:includeSync?syncReasoningChoices():[]};''',1)
p.write_text(s)

# Browser tab no longer repeats site branding over admin.
p=Path('app/page.tsx')
s=p.read_text()
old=''' return <div className="browser"><div className="tabs"><span>烛</span><b>烛阴旧闻</b></div><div className="bar">'''
new=''' return <div className="browser"><div className="tabs"><span>{forumIdentity==="admin"?"档":"烛"}</span><b>{forumIdentity==="admin"?"内部资料库":"烛阴旧闻"}</b></div><div className="bar">'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)
print('Applied guest-ID clarity model and removed author-style legend')