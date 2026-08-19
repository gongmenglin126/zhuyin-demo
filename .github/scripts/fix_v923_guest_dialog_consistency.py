from pathlib import Path

p=Path('app/AdminPortalOccult.tsx')
s=p.read_text()
# Remove remaining B-side labels now that guest IDs carry continuity.
s=s.replace('<p style={s.subtle}>B侧长期样本 / 候舍对象 19-07</p>','<p style={s.subtle}>长期样本 / 候舍对象 19-07</p>',1)
s=s.replace('label="B侧 · 林楠登记身体"','label="林楠 · 执行记录"',1)
s=s.replace('meta="B侧再次易舍后 51 分钟"','meta="再舍完成后 51 分钟"',1)
# Guest alpha points to the second execution without prematurely spelling out its destination.
s=s.replace('["2026-10-12","再舍后所在","19-07"]','["2026-10-12","关联再舍","RS-2026-1012"]',1)
p.write_text(s)

p=Path('app/InteractiveWechat.tsx')
s=p.read_text()
# Material response reflects IDs, not the removed 客源 fields.
s=s.replace('''"admin-pair-2004":{ly:[{text:"A、B两边的‘客源’为什么正好写的是对方？"},{text:"这两个字段得跟前面那几句经文一起看。"}],zc:[{text:"这份比经文直接。"},{text:"A、B两边都写了易舍完成。"}]},''',
'''"admin-pair-2004":{ly:[{text:"A这边是客β，B这边是客α。"},{text:"这两个希腊字母看着不像人名，更像他们给‘客’单独编的号。"}],zc:[{text:"这份比经文直接。"},{text:"两边都写了易舍完成，还各自留了客编号。"}]},''',1)

# Replace the first-stage reasoning: recognize the database schema, don't auto-solve the swap.
start=s.index('const pairReasoningChoices=():QuickReply[]=>{')
end=s.index('\n\nconst quickAfterMaterial=',start)
new_pair='''const pairReasoningChoices=():QuickReply[]=>{\n const correct:QuickReply={id:"ly-pair-guest-id",text:"α、β应该是在给‘客’编号？",reply:[{text:"我也觉得。"},{text:"名字写在‘舍’那一栏，α、β却一直跟着‘客’。"},{text:"如果后台能搜编号，同一个编号后来跑到哪，应该比盯着人名清楚。"}]};\n const wrongPerson:QuickReply={id:"ly-pair-person-id",text:"α、β会不会只是两个人的匿名编号？",reply:[{text:"也可能。"},{text:"但它们正好写在‘客编号’后面，我会先按那个字段理解。"}],next:[correct]};\n const wrongBatch:QuickReply={id:"ly-pair-batch-id",text:"是不是仪式批次号？",reply:[{text:"批次号他们都写成LN、RS那种格式。"},{text:"α、β看着是另一套编号。"}],next:[correct]};\n return [wrongPerson,correct,wrongBatch];\n};'''
s=s[:start]+new_pair+s[end:]

# Replace sync reasoning to eliminate remaining B-side tutorial language.
start=s.index('const syncReasoningChoices=():QuickReply[]=>{')
end=s.index('\nconst reswapReasoningChoices=',start)
new_sync='''const syncReasoningChoices=():QuickReply[]=>{\n const correct:QuickReply={id:"ly-sync-right",text:"所以沈妍被抓，是因为那次再舍以后她这里出了同步异常？",reply:[{text:"对。"},{text:"时间能对上：12号再舍完成，沈妍这边开始异常；16号他们把她控制起来。"},{text:"所以抓沈妍不是为了再给她换一次，是为了处理试验冒出来的异常。"},{text:"现在得找她被转到哪。"}]};\n const wrongAgain:QuickReply={id:"ly-sync-wrong-again",text:"所以他们抓沈妍，是准备再给她换一次？",reply:[{text:"我觉得不是。"},{text:"沈妍这份写的是‘控制旧对契另一端’，处置理由也是同步异常。"}]};\n const wrongForum:QuickReply={id:"ly-sync-forum",text:"还是因为沈妍查论坛查得太深？",reply:[{text:"他们当然一直监控她。"},{text:"但这份处置理由写的是同步异常，不是论坛行为。"}]};\n wrongAgain.next=[correct,wrongForum];wrongForum.next=[wrongAgain,correct];\n return [wrongAgain,correct,wrongForum];\n};'''
s=s[:start]+new_sync+s[end:]

# Rework second-swap choices around guest alpha continuity.
start=s.index('const reswapReasoningChoices=(includeSync:boolean):QuickReply[]=>{')
end=s.index('\nconst pairReasoningChoices=',start)
new_reswap='''const reswapReasoningChoices=(includeSync:boolean):QuickReply[]=>{\n const correct:QuickReply={id:"ly-reswap-test",text:"客α没变，只是从林楠那条记录换到了19-07？",reply:[{text:"对，我也是这么看的。"},{text:"而且他们专门挑了一个已经稳定22年的客α，再做第二次易舍。"},{text:"所以这次是在验证同一个‘客’能不能连续换舍。"},{text:"但这份还没解释沈妍为什么会被抓。"}],next:includeSync?syncReasoningChoices():[]};\n const wrongShen:QuickReply={id:"ly-reswap-shen",text:"所以他们这次还是在换沈妍？",reply:[{text:"先别看名字。"},{text:"执行前林楠那条是客α，执行后19-07变成客α；真正连续的是这个编号。"}]};\n const wrongRepeat:QuickReply={id:"ly-reswap-repeat",text:"只是把2004年的仪式原样再做一次？",reply:[{text:"不太像。"},{text:"这次特意写了稳定22年和‘再舍验证’，目的明显是测试第二次转移。"}]};\n wrongShen.next=[correct,wrongRepeat];wrongRepeat.next=[wrongShen,correct];\n return [wrongShen,correct,wrongRepeat];\n};'''
s=s[:start]+new_reswap+s[end:]

# 19-07 no longer 'requests to contact Xu Ning'; it has a fragmented emotional response to the name.
s=s.replace('''if(contactId==="ly"&&materialId==="admin-third-1907")return [{id:"ly-third-identity",text:"她还要求联系徐宁。",reply:[{text:"……"},{text:"那就不能只当身份混乱看了。"},{text:"真找到地点，这个人也得告诉警方。"}]}];''',
'''if(contactId==="ly"&&materialId==="admin-third-1907")return [{id:"ly-third-identity",text:"她听到徐宁这个名字为什么会哭？",reply:[{text:"……这才吓人。"},{text:"她连名字都说不稳，但情绪反应还在。"},{text:"真找到地点，这个人也得告诉警方。"}]}];''',1)
p.write_text(s)
print('Aligned Liang reasoning and labels with guest-ID model')