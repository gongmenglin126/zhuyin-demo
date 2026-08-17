from pathlib import Path

page=Path('app/page.tsx')
p=page.read_text(encoding='utf-8')
start=p.find('function VersePage')
assert start>=0, 'VersePage not found'
fig=p.find('<figure',start)
article=p.find('<article',fig)
assert fig>=0 and article>fig, 'VersePage figure/article boundary not found'
new_figure='''<figure style={{width:"min(720px,100%)",margin:"0 auto",padding:10,background:"#080606",border:"1px solid #321714",boxShadow:"0 24px 80px #000",textAlign:"center"}}><img src="assets/occult/huanzhen-scripture-v904.webp" alt="无相还真黑底朱字旧教页" style={{display:"block",width:"100%",maxHeight:780,objectFit:"contain"}}/><figcaption style={{padding:"12px 12px 4px",color:"#75645c",fontSize:11}}>scan_07_untitled.tif · 来源字段已删除 · 缓存于 2026-10-16 19:49</figcaption></figure>'''
p=p[:fig]+new_figure+p[article:]
page.write_text(p,encoding='utf-8')

exec(compile(Path('.github/scripts/apply_v904_occult_images_and_feedback.py').read_text(encoding='utf-8'),'.github/scripts/apply_v904_occult_images_and_feedback.py','exec'),{})
