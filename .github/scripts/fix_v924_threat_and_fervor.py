from pathlib import Path

p=Path('app/AdminPortalOccult.tsx')
s=p.read_text()
s=s.replace('["24-11","女 / 26","申请 3 次","选我。现在就可以。我不要这个身体了。别再让我等。"]','["24-11","女 / 26","申请 3 次","选我。现在就做。我不要这具身体。谁进来都行。"]')
s=s.replace('["21-16","男 / 42","申请 5 次","我等了六年。下一次必须是我。换进去的是谁都行。执行以后不要把我退回来。"]','["21-16","男 / 42","申请 5 次","我等了六年。下一次必须是我。换进去的是谁都行。别再让我醒回这具舍里。"]')
s=s.replace('["19-03","女 / 28","申请 2 次","不用通知任何人，也不用保留我现在的身份。下一批有空位就把我排进去。"]','["19-03","女 / 28","申请 2 次","不用通知外面。执行完把我现在的东西全清掉。别留退路。"]')
s=s.replace('["22-08","男 / 35","申请 4 次","如果这具舍不合适就废掉。别取消我的资格。我必须完成一次易舍。"]','["22-08","男 / 35","申请 4 次","不合适就废舍。别把我退回来。失败也算我完成奉舍。"]')
s=s.replace('["23-14","女 / 31","申请 3 次","把我的姓名删掉。我不想再用它。执行后不要告诉我原来的住址，也不要让我回去。"]','["23-14","女 / 31","申请 3 次","编号就够了。旧照片、住址、关系都清掉。执行后不要让我再知道它们。"]')
s=s.replace('["18-02","男 / 39","申请 6 次","我准备好了。谁来都可以。把这具舍交出去，把我原来的资料清掉。"]','["18-02","男 / 39","申请 6 次","现在就能做。谁需要这具舍就给谁。不要再问我愿不愿意。"]')
old='''<Record date="2012修订" title="停止低龄优先" meta="成年自愿候舍纳入正式序列" text="长期样本证明年龄不是必要条件。改以对契匹配、去名训练与成年自愿对象为主。"/><Record date="现行"'''
new='''<Record date="2012修订" title="停止低龄优先" meta="成年自愿候舍纳入正式序列" text="长期样本证明年龄不是必要条件。改以对契匹配、去名训练与成年自愿对象为主。"/><Record date="去名训练" title="仅保留候舍编号" meta="入库前连续30日" text="停止使用原名；不看旧照片；减少原家庭接触；问询时只对候舍编号作答。完成后原姓名字段从候舍库移除。"/><Record date="现行"'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)

p=Path('app/InteractiveWechat.tsx')
s=p.read_text()
old='''  if(item.id==="zc-zheliu"){wechatSession.zhouConfronted=true;if(wechatSession.locationKnown)window.setTimeout(()=>triggerZhouLocationThreat(),100)}
  delayedParts(id,item.reply,item.next||[]);'''
new='''  if(item.id==="zc-zheliu")wechatSession.zhouConfronted=true;
  delayedParts(id,item.reply,item.next||[]);
  if(item.id==="zc-zheliu-how"&&wechatSession.locationKnown)window.setTimeout(()=>triggerZhouLocationThreat(),5200);'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)
print('Fixed threat ordering and made candidate applications more direct')
