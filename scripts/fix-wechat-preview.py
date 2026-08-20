from pathlib import Path

p=Path("app/InteractiveWechat.tsx")
s=p.read_text()
old=' const previewFor=(c:Contact)=>{const added=extra[c.id]||[];return editWechatLive(added.length?added[added.length-1].text:c.preview)};'
new=' const previewFor=(c:Contact)=>{const added=extra[c.id]||[];const latest=added.length?added[added.length-1]:c.messages[c.messages.length-1];return editWechatLive(latest?.text||c.preview)};'
if old not in s:
    raise SystemExit("previewFor source line not found")
p.write_text(s.replace(old,new,1))
