from pathlib import Path
p=Path('app/InteractiveWechat.tsx')
s=p.read_text(encoding='utf-8')
old='export const subscribeWechatNotices=(fn:(notice:WechatNotice)=>void)=>{wechatNoticeSubscribers.add(fn);return ()=>wechatNoticeSubscribers.delete(fn)};'
new='export const subscribeWechatNotices=(fn:(notice:WechatNotice)=>void)=>{wechatNoticeSubscribers.add(fn);return ()=>{wechatNoticeSubscribers.delete(fn)}};'
assert old in s
p.write_text(s.replace(old,new,1),encoding='utf-8')
print('fixed notice cleanup')
