from pathlib import Path

page=Path('app/page.tsx')
p=page.read_text(encoding='utf-8')

old='''<Floor user={post.author} time={post.date} no="楼主" role="楼主" openUser={openUser}><>{post.body.map((x,i)=><p key={i}><MarkedText text={x} marks={post.highlights}/></p>)}{!!media.length&&<div className="attachments">{media.map(x=><figure key={x.src}><button onClick={()=>setZoom(x)} title="点击查看原图"><img src={x.src} alt={x.caption}/><span><Maximize2/>查看原图</span></button><figcaption>{x.caption}</figcaption></figure>)}</div>}</></Floor>{post.id==="23109"&&<RecoveredRitualAttachment/>}'''
new='''<Floor user={post.author} time={post.date} no="楼主" role="楼主" openUser={openUser}><>{post.body.map((x,i)=><p key={i}><MarkedText text={x} marks={post.highlights}/></p>)}{!!media.length&&<div className="attachments">{media.map(x=><figure key={x.src}><button onClick={()=>setZoom(x)} title="点击查看原图"><img src={x.src} alt={x.caption}/><span><Maximize2/>查看原图</span></button><figcaption>{x.caption}</figcaption></figure>)}</div>}{post.id==="23109"&&<RecoveredRitualAttachment/>}</></Floor>'''
assert old in p, 'Thread attachment placement pattern not found'
p=p.replace(old,new,1)

p=p.replace('margin:"18px 24px",padding:16,border:"1px solid #d5cabc",background:"#f2ede4"','margin:"18px 0",width:"min(620px,100%)",boxSizing:"border-box",padding:16,border:"1px solid #d5cabc",background:"#f2ede4"',1)
p=p.replace('width:"calc(100% - 48px)",height:210,margin:"18px 24px",border:"1px solid #341312"','width:"min(620px,100%)",height:210,margin:"18px 0",display:"block",boxSizing:"border-box",border:"1px solid #341312"',1)
p=p.replace('margin:"18px auto",width:"min(720px,92%)",display:"grid",gap:12','margin:"18px 0",width:"min(620px,100%)",boxSizing:"border-box",display:"grid",gap:12',1)
p=p.replace('margin:0,padding:10,border:"1px solid #2b2420",background:"#100d0c"','margin:0,padding:10,boxSizing:"border-box",overflow:"hidden",border:"1px solid #2b2420",background:"#100d0c"',2)

page.write_text(p,encoding='utf-8')

final=page.read_text(encoding='utf-8')
assert 'post.id==="23109"&&<RecoveredRitualAttachment/>}</></Floor>' in final
assert 'width:"min(620px,100%)"' in final
assert 'width:"calc(100% - 48px)"' not in final
print('v9.0.6 attachment width fix applied')
