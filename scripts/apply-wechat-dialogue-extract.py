from pathlib import Path

p=Path("app/InteractiveWechat.tsx")
s=p.read_text()

imp='import {WECHAT_CONTACTS} from "../content/wechatDialogues";\n'
if imp not in s:
    anchor='import {Plus,Search,Send,X} from "lucide-react";\n'
    if anchor not in s:
        raise SystemExit("missing lucide import anchor")
    s=s.replace(anchor,anchor+imp,1)

start='const contacts:Contact[]=['
end='const wechatNoticeSubscribers=new Set<(notice:WechatNotice)=>void>();'
i=s.find(start)
j=s.find(end)
if i<0 or j<0 or j<=i:
    raise SystemExit("contacts block anchors not found")
s=s[:i]+'const contacts:Contact[]=WECHAT_CONTACTS;\n\n'+s[j:]
p.write_text(s)
