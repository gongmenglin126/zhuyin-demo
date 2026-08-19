from pathlib import Path
p=Path('app/page.tsx')
s=p.read_text()
old='''<button onClick={()=>forumIdentity==="shenyan"&&go({kind:"history"})}><HistoryIcon/></button>'''
new='''{forumIdentity==="admin"?<button onClick={()=>{persistedForumIdentity="shenyan";setForumIdentity("shenyan");setRoute({kind:"home"});setStack([])}} style={{width:"auto",padding:"0 10px",fontSize:11}}>返回论坛</button>:<button onClick={()=>go({kind:"history"})}><HistoryIcon/></button>}'''
assert old in s
s=s.replace(old,new,1)
p.write_text(s)
print('Added return-to-forum bridge')