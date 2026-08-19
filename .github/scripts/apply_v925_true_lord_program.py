from pathlib import Path

p=Path('app/AdminPortalOccult.tsx')
s=p.read_text()

repls={
'["24-11","女 / 26","申请 3 次","选我。现在就做。我不要这具身体。谁进来都行。"]':'["24-11","女 / 26","申请 3 次","选我。现在就做。我不要这具身体。谁进来都行。如果进真君序列，不用再问我。"]',
'["21-16","男 / 42","申请 5 次","我等了六年。下一次必须是我。换进去的是谁都行。别再让我醒回这具舍里。"]':'["21-16","男 / 42","申请 5 次","我等了六年。下一次必须是我。普通客也行，真君更好。别再让我醒回这具舍里。"]',
'["19-03","女 / 28","申请 2 次","不用通知外面。执行完把我现在的东西全清掉。别留退路。"]':'["19-03","女 / 28","申请 2 次","不用通知外面。执行完把我现在的东西全清掉。真君需要就直接用，别留退路。"]',
'["18-02","男 / 39","申请 6 次","现在就能做。谁需要这具舍就给谁。不要再问我愿不愿意。"]':'["18-02","男 / 39","申请 6 次","现在就能做。谁需要这具舍就给谁。真君要用的话，不要再问我愿不愿意。"]',
}
for old,new in repls.items():
    assert old in s, old
    s=s.replace(old,new,1)

old='''<Record date="去名训练" title="仅保留候舍编号" meta="入库前连续30日" text="停止使用原名；不看旧照片；减少原家庭接触；问询时只对候舍编号作答。完成后原姓名字段从候舍库移除。"/><Record date="现行" title="候舍来源充足，无需强制补充" meta="旧契样本另行处置" text="常规候舍优先从奉舍申请中匹配。旧契样本不可替代；出现同步、返契异常时优先回收。"/></section>
 <section style={s.adminPanel}><h4>近期奉舍申请</h4>'''
new='''<Record date="去名训练" title="仅保留候舍编号" meta="入库前连续30日" text="停止使用原名；不看旧照片；减少原家庭接触；问询时只对候舍编号作答。完成后原姓名字段从候舍库移除。"/><Record date="现行" title="候舍来源充足，无需强制补充" meta="旧契样本另行处置" text="常规候舍优先从奉舍申请中匹配。旧契样本不可替代；出现同步、返契异常时优先回收。"/></section>
 <section style={s.adminPanel}><h4>归真序列 · 阶段 II</h4><Record date="前置验证" title="长期客二次再舍稳定" meta="RS-2026-1012" text="客α作为当前长期样本。二次再舍已完成；旧对契异常尚未关闭。"/><Record date="候舍池" title="来源充足" meta="匹配可用 37 / 待执行 12" text="现阶段不批准以强制方式补充普通候舍。"/><Record date="真君序列" title="暂缓启用" meta="待长期客验证通过" text="连续再舍稳定性未达到启用条件。旧客验证完成后重新评估。"/></section>
 <section style={s.adminPanel}><h4>近期奉舍申请</h4>'''
assert old in s
s=s.replace(old,new,1)

p.write_text(s)
print('Applied True Lord program details to candidate library')
