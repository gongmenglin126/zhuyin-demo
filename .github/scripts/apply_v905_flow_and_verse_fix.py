from pathlib import Path

page = Path('app/page.tsx')
admin = Path('app/AdminPortalOccult.tsx')

p = page.read_text(encoding='utf-8')
old_gate = 'canUseLegacy={verseSeen&&read.includes("27614")&&read.includes("23109")}'
assert old_gate in p, 'legacy gate not found'
p = p.replace(old_gate, 'canUseLegacy={verseSeen}', 1)

old_main = '<main className="verse-page" style={{minHeight:"100%",background:"#080606",color:"#ddd0c1"}}>'
new_main = '<main className="verse-page" style={{height:"100%",minHeight:"100%",overflowY:"auto",background:"#080606",color:"#ddd0c1"}}>'
assert old_main in p, 'VersePage main not found'
p = p.replace(old_main, new_main, 1)

old_section = '<section style={{maxWidth:1040,margin:"0 auto",padding:"28px 30px 48px"}}>'
new_section = '<section style={{maxWidth:1040,margin:"0 auto",padding:"28px 30px 110px"}}>'
assert old_section in p, 'VersePage section not found'
p = p.replace(old_section, new_section, 1)

old_img = '<img src="assets/occult/huanzhen-scripture-v904.webp" alt="无相还真黑底朱字旧教页" style={{display:"block",width:"100%",maxHeight:780,objectFit:"contain"}}/>'
new_img = '<img src="assets/occult/huanzhen-scripture-v904.webp" alt="无相还真黑底朱字旧教页" style={{display:"block",width:"100%",maxHeight:520,objectFit:"contain",objectPosition:"center top"}}/>'
assert old_img in p, 'VersePage image not found'
p = p.replace(old_img, new_img, 1)

old_article = '<article style={{maxWidth:720,margin:"18px auto 0",padding:"22px 24px",border:"1px solid #3c1c18",background:"#120c0b",font:"15px serif",lineHeight:2,color:"#d8c4b1"}}>'
new_article = '<article style={{maxWidth:720,margin:"18px auto 0",padding:"24px 24px 42px",border:"1px solid #3c1c18",background:"#120c0b",font:"15px serif",lineHeight:2,color:"#d8c4b1",overflow:"visible"}}>'
assert old_article in p, 'VersePage article not found'
p = p.replace(old_article, new_article, 1)

page.write_text(p, encoding='utf-8')

a = admin.read_text(encoding='utf-8')
old_submit = '''  if(user.trim()===ADMIN_USER){setAttemptedAdmin(true);setError("账号或密码错误。");return;}'''
new_submit = '''  if(user.trim()===ADMIN_USER){
   setAttemptedAdmin(true);
   if(canUseLegacy){setMode("verify");setError("");return;}
   setError("账号或密码错误。");return;
  }'''
assert old_submit in a, 'admin failed-login block not found'
a = a.replace(old_submit, new_submit, 1)
admin.write_text(a, encoding='utf-8')

# self-checks
p2 = page.read_text(encoding='utf-8')
a2 = admin.read_text(encoding='utf-8')
assert 'canUseLegacy={verseSeen}' in p2
assert 'read.includes("27614")&&read.includes("23109")' not in p2
assert 'overflowY:"auto"' in p2
assert 'maxHeight:520' in p2
assert 'if(canUseLegacy){setMode("verify")' in a2
print('v9.0.5 flow + verse display fixes applied')
