from pathlib import Path


def replace_once(path, old, new, label):
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    if old not in s:
        raise SystemExit(f"missing {label} in {path}")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")

page = "app/page.tsx"
replace_once(
    page,
    'const investigationPrivateEntries=privateEntries;\nlet persistedForumIdentity:',
    'const investigationPrivateEntries=privateEntries;\nconst SHAREABLE_POST_IDS=new Set(["33897","09114","09831","10731","14692","17428","11208","27614"]);\nlet persistedForumIdentity:',
    "shareable post ids",
)
replace_once(
    page,
    '{route.kind==="post"&&<Thread post={investigationPosts.find(x=>x.id===route.id)!} openUser={openUser} onCopyMaterial={onCopyMaterial}/>} ',
    '{route.kind==="post"&&<Thread post={investigationPosts.find(x=>x.id===route.id)!} openUser={openUser} onCopyMaterial={onCopyMaterial} hasMaterial={hasMaterial}/>} ',
    "thread invocation",
)
replace_once(
    page,
    'function Thread({post,openUser,onCopyMaterial}:{post:Post;openUser:(name:string)=>void;onCopyMaterial:(m:SharedMaterial)=>void}){',
    'function Thread({post,openUser,onCopyMaterial,hasMaterial}:{post:Post;openUser:(name:string)=>void;onCopyMaterial:(m:SharedMaterial)=>void;hasMaterial:(id:string)=>boolean}){',
    "thread signature",
)
old_button = '<button onClick={()=>onCopyMaterial({id:post.id,title:post.title,kind:"论坛帖子",url:"https://www.zhuyinwen.cn/thread/"+post.id})} style={{marginTop:8,border:"1px solid #b8afa5",background:"#fff",borderRadius:5,padding:"6px 10px",fontSize:12,cursor:"pointer"}}>复制链接</button>'
new_button = '{SHAREABLE_POST_IDS.has(post.id)&&<button disabled={hasMaterial(post.id)} onClick={()=>onCopyMaterial({id:post.id,title:post.title,kind:"论坛帖子",url:"https://www.zhuyinwen.cn/thread/"+post.id})} style={{marginTop:8,border:"1px solid #b8afa5",background:"#fff",borderRadius:5,padding:"6px 10px",fontSize:12,cursor:hasMaterial(post.id)?"default":"pointer",opacity:hasMaterial(post.id)?.55:1}}>{hasMaterial(post.id)?"已添加":"添加到材料"}</button>}'
replace_once(page, old_button, new_button, "thread material button")

wx = "app/InteractiveWechat.tsx"
p = Path(wx)
s = p.read_text(encoding="utf-8")
old_rules = ' "31002":{zc:[{text:"这个站务说明我见过。"},{text:"你是觉得旧档员-03有问题？"}],ly:[{text:"这个号我见过。迟迟那边的旧帖也被它动过。"}]},\n'
if old_rules not in s:
    raise SystemExit("missing 31002 material rule")
s = s.replace(old_rules, "", 1)
start = s.find(' if(contactId==="zc"&&materialId==="31002"){')
if start < 0:
    raise SystemExit("missing 31002 quick reply block")
end = s.find(' if(contactId==="zc"&&materialId==="27614")', start)
if end < 0:
    raise SystemExit("missing 27614 quick reply marker")
s = s[:start] + s[end:]
p.write_text(s, encoding="utf-8")

# Guardrails: ordinary station posts must not offer the material action, while evidence posts do.
page_text = Path(page).read_text(encoding="utf-8")
assert 'SHAREABLE_POST_IDS=new Set(["33897","09114","09831","10731","14692","17428","11208","27614"])' in page_text
assert 'hasMaterial(post.id)?"已添加":"添加到材料"' in page_text
wx_text = Path(wx).read_text(encoding="utf-8")
assert '"31002":{zc:' not in wx_text
assert 'materialId==="31002"' not in wx_text
print("v8.9.17 material scope patch applied")
