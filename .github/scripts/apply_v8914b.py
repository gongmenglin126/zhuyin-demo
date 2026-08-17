from pathlib import Path


def patch(path, replacements):
    p=Path(path)
    s=p.read_text(encoding='utf-8')
    for old,new,label in replacements:
        if old not in s:
            raise SystemExit(f'missing {label} in {path}')
        s=s.replace(old,new,1)
    p.write_text(s,encoding='utf-8')

patch('app/page.tsx',[
 ('<p>沈妍没有赴约。<br/>至少在今天中午时，你还只把它当成爽约。</p>','<p>沈妍没有赴约。<br/>电话关机，消息也没有回复。</p>','title mind-reading'),
 ('<div className="empty"><Search/><h3>没有找到完全匹配的公开内容</h3><p>试试更短的人名、地点、年份、原句或帖子编号。</p></div>','<div className="empty"><Search/><h3>没有找到匹配的公开内容</h3></div>','search tutorial'),
])
patch('app/InteractiveWechat.tsx',[
 ('{who:"对方",text:"那两个字还是听不清？"}','{who:"对方",text:"那声称呼还是听不清？"}','two-character assumption'),
 ('if(/名字不对|另一个家|回来以后不会/.test(t))return [{text:"我见过这种说法，不止一篇。"},{text:"具体哪篇我得翻一下。"}];','if(/名字不对|另一个家|回来以后不会/.test(t))return [{text:"我好像见过这种说法。"},{text:"站里走失帖不少，具体哪篇我记不清了。"}];','fake follow-up'),
])

page=Path('app/page.tsx').read_text(encoding='utf-8')
wx=Path('app/InteractiveWechat.tsx').read_text(encoding='utf-8')
for bad in ['你还只把它当成爽约','试试更短的人名','原句或帖子编号']:
    if bad in page: raise SystemExit('still present: '+bad)
for bad in ['那两个字还是听不清','具体哪篇我得翻一下']:
    if bad in wx: raise SystemExit('still present: '+bad)
print('second-pass cleanup passed')
