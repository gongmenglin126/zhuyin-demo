from pathlib import Path

# Persist forum read state across app switches.
p=Path('app/page.tsx')
s=p.read_text(encoding='utf-8')
old='let persistedForumIdentity:"shenyan"|"admin"="shenyan";'
new='let persistedForumIdentity:"shenyan"|"admin"="shenyan";\nlet persistedForumRead:string[]=[];'
if old not in s: raise SystemExit('missing persisted identity')
s=s.replace(old,new,1)
old='const [route,setRoute]=useState<Route>(initialPostId?{kind:"post",id:initialPostId}:{kind:"home"}),[stack,setStack]=useState<Route[]>([]),[q,setQ]=useState(""),[read,setRead]=useState<string[]>(initialPostId?[initialPostId]:[]);'
new='const [route,setRoute]=useState<Route>(initialPostId?{kind:"post",id:initialPostId}:{kind:"home"}),[stack,setStack]=useState<Route[]>([]),[q,setQ]=useState(""),[read,setRead]=useState<string[]>(()=>[...new Set([...persistedForumRead,...(initialPostId?[initialPostId]:[])])]);'
if old not in s: raise SystemExit('missing browser state')
s=s.replace(old,new,1)
old='const go=(next:Route)=>{setStack([...stack,route]);setRoute(next);if(next.kind==="post")setRead([...new Set([...read,next.id])])};'
new='const go=(next:Route)=>{setStack([...stack,route]);setRoute(next);if(next.kind==="post"){const nextRead=[...new Set([...read,next.id])];persistedForumRead=nextRead;setRead(nextRead)}};'
if old not in s: raise SystemExit('missing go')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

# Keep the exact eight-character old oath exclusive to the recovered cult page;
# the public source-criticism thread should only describe the black page vaguely.
p=Path('content/gameDataFlowV2.ts')
s=p.read_text(encoding='utf-8')
s=s.replace('terms:["三门疏","身非我身","名非我名","黑底红字","白纸抄本","残页"],','terms:["三门疏","黑底红字","白纸抄本","残页","旧短偈"],',1)
s=s.replace('highlights:["身非我身，名非我名","《三门疏》","不是同一批扫描","来源字段都缺了"],','highlights:["《三门疏》","不是同一批扫描","来源字段都缺了"],',1)
old='一类是反相处理过的黑底页面，最清楚的只有“身非我身，名非我名”反复出现；另一类是普通白纸抄本，边角有一页能看见《三门疏》三个字。'
new='一类是反相处理过的黑底页面，像在反复抄一句很短的偈子，只能稳定认出“身”“名”几个字；另一类是普通白纸抄本，边角有一页能看见《三门疏》三个字。'
if old not in s: raise SystemExit('missing scripture public text')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

assert 'persistedForumRead' in Path('app/page.tsx').read_text(encoding='utf-8')
text=Path('content/gameDataFlowV2.ts').read_text(encoding='utf-8')
public=text[text.index('const scriptureComparePost'):text.index('const reportBase')]
assert '身非我身，名非我名' not in public
print('v9 gate persistence fixes applied')
