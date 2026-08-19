from pathlib import Path

# Admin navigation: keep orientation, remove author explanation.
p=Path('app/AdminPortalOccult.tsx')
s=p.read_text()
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
# Do not explain the ontology in the records. Keep the cult's raw A/B fields where they naturally occur.
s=s.replace('''<Record date="A侧" title="登记身体：沈妍" meta="客源：林楠" text="易舍完成；页面仍按登记身体‘沈妍’归档。"/><Record date="B侧" title="登记身体：林楠" meta="客源：沈妍" text="易舍完成；页面仍按登记身体‘林楠’归档。"/>''',
'''<Record date="A" title="舍：沈妍" meta="客源：林楠" text="易舍完成；返家后持续观察。"/><Record date="B" title="舍：林楠" meta="客源：沈妍" text="易舍完成；返家后持续观察。"/>''',1)
s=s.replace('''<Record date="选择" title="B侧：林楠登记身体" meta="旧客稳定期 22 年" text="2004年后B侧长期稳定；候舍对象19-07为第三名成年对象，匹配通过。"/>''',
'''<Record date="选择" title="旧客连续样本" meta="稳定期 22 年" text="2004年易舍后长期稳定；候舍对象19-07匹配通过。"/>''',1)
s=s.replace('''<Record date="结果" title="执行完成" meta="2026-10-12 22:13" text="B侧旧客转入19-07舍；19-07原客转入B侧舍。随后A侧沈妍出现原对契同步异常。"/>''',
'''<Record date="结果" title="执行完成" meta="2026-10-12 22:13" text="两侧生命体征稳定；原对契随后出现同步异常。"/>''',1)
s=s.replace('''<Record date="处置理由" title="控制A侧：沈妍" meta="执行 HN-1016-02" text="B侧（林楠登记身体）完成再舍后，A侧沈妍同步反应持续升高，可能影响试验稳定性；因此控制沈妍。沈妍不是本次再舍对象。"/>''',
'''<Record date="处置理由" title="控制旧对契另一端" meta="对象：0712-4471 · 沈妍" text="10月12日再舍完成后，该对象同步反应持续升高，可能影响试验稳定性；10月16日转入控制。"/>''',1)
p.write_text(s)

# Liang should answer the player's actual question without teaching A/B/body terminology.
p=Path('app/InteractiveWechat.tsx')
s=p.read_text()
s=s.replace('''"admin-sync-shen":{ly:[{text:"这份写得很清楚：被控制的是沈妍。"},{text:"触发原因是B侧再舍完成后，沈妍这边出现同步异常。别把‘谁做了第二次易舍’和‘谁被抓’混成一个人。"}],zc:[{text:"他们自己把这条标成了关联异常。"},{text:"‘控制’和执行批次比解释更重要。"}]},''',
'''"admin-sync-shen":{ly:[{text:"这条才是在解释沈妍为什么被抓。"},{text:"10月12号再舍完成以后，她这边的同步反应一直往上升；10月16号后台才把她转成‘已控制’。"}],zc:[{text:"他们自己把这条标成了关联异常。"},{text:"‘控制’和执行批次比解释更重要。"}]},''',1)
s=s.replace('''const correct:QuickReply={id:"ly-sync-right",text:"所以沈妍被抓，是因为B侧再舍后她这个旧对契另一端出了异常？",reply:[{text:"对。"},{text:"抓的是沈妍；做第二次易舍的是B侧‘林楠’那具登记身体。两件事不是同一个人。"},{text:"沈妍不是第二次试验的目标，她是试验后出现的异常，所以才被控制。"},{text:"现在得找沈妍被转到哪。"}]};''',
'''const correct:QuickReply={id:"ly-sync-right",text:"所以沈妍被抓，是因为那次再舍以后她这里出了同步异常？",reply:[{text:"对。"},{text:"这才对上了：10月12号做完再舍，她的异常开始升；10月16号他们把她控制起来。"},{text:"所以抓沈妍不是为了再给她换一次，是为了处理这次试验冒出来的异常。"},{text:"现在得找她被转到哪。"}]};''',1)
s=s.replace('''const wrongAgain:QuickReply={id:"ly-sync-wrong-again",text:"所以他们抓沈妍，是准备再给沈妍换一次？",reply:[{text:"不是。沈妍这份写的是‘控制A侧旧对契另一端’，本次再舍对象在B侧。"}]};''',
'''const wrongAgain:QuickReply={id:"ly-sync-wrong-again",text:"所以他们抓沈妍，是准备再给她换一次？",reply:[{text:"我觉得不是。"},{text:"沈妍这份写的是‘控制旧对契另一端’，而且处置理由就是同步异常。"}]};''',1)
s=s.replace('''const nextAfterCorrect:QuickReply[]=received("ly","admin-reswap-2026")?reswapReasoningChoices(received("ly","admin-sync-shen")):[{id:"ly-pair-why",text:"那为什么2026年又把沈妍抓走？",reply:[{text:"对，这才是现在的问题。"},{text:"先分清：沈妍是A侧登记身体，林楠是B侧登记身体。2004只解释她们为什么有关联，还解释不了沈妍这次为什么被控制。"},{text:"要看B侧2026年的执行，再看沈妍自己的同步异常。"}]}];''',
'''const nextAfterCorrect:QuickReply[]=received("ly","admin-reswap-2026")?reswapReasoningChoices(received("ly","admin-sync-shen")):[{id:"ly-pair-why",text:"那为什么2026年又把沈妍抓走？",reply:[{text:"对，这才是现在的问题。"},{text:"2004这份只能说明她和林楠为什么会被绑在一起，还解释不了这次抓人。"},{text:"后面得找2026年的执行记录，再看沈妍自己出了什么异常。"}]}];''',1)
s=s.replace('''const correct:QuickReply={id:"ly-reswap-test",text:"他们在测试同一个‘客’能不能连续换身体？",reply:[{text:"对。"},{text:"而且这里做第二次易舍的是B侧，也就是‘林楠’这具登记身体，不是沈妍。"},{text:"稳定22年、再次易舍、主体稳定——这几个字段放一起就是这个意思。"}],next:includeSync?syncReasoningChoices():[]};''',
'''const correct:QuickReply={id:"ly-reswap-test",text:"他们在测试同一个‘客’能不能连续换身体？",reply:[{text:"对。"},{text:"稳定22年、再次易舍、主体稳定——这几个字段放一起就是这个意思。"},{text:"但这份还没解释沈妍为什么会被抓。"}],next:includeSync?syncReasoningChoices():[]};''',1)
p.write_text(s)

# When logged into admin, browser tab should not repeat 烛 / 烛阴旧闻 / 旧档管理.
p=Path('app/page.tsx')
s=p.read_text()
old=''' return <div className="browser"><div className="tabs"><span>烛</span><b>烛阴旧闻</b></div><div className="bar">'''
new=''' return <div className="browser"><div className="tabs"><span>{forumIdentity==="admin"?"档":"烛"}</span><b>{forumIdentity==="admin"?"内部资料库":"烛阴旧闻"}</b></div><div className="bar">'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)
print('Removed author-style identity legend and simplified Liang explanation')