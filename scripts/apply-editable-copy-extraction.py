from pathlib import Path
import json
import re


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"missing source fragment: {label}")
    return text.replace(old, new, 1)


def extract_cn_strings(paths):
    seen = set()
    out = []
    pat = re.compile(r'"((?:\\.|[^"\\])*)"')
    for path in paths:
        text = Path(path).read_text()
        for raw in pat.findall(text):
            try:
                value = json.loads('"' + raw + '"')
            except Exception:
                continue
            if not re.search(r'[\u3400-\u9fff]', value):
                continue
            if value in seen:
                continue
            seen.add(value)
            out.append(value)
    return out


def write_map(path, const_name, fn_name, values, header, helpers=""):
    lines = [header, "", f"export const {const_name}:Record<string,string>={{"]
    for value in values:
        q = json.dumps(value, ensure_ascii=False)
        lines.append(f"  {q}:{q},")
    lines += ["};", "", f"export const {fn_name}=(text:string)=>{const_name}[text]??text;"]
    if helpers:
        lines += ["", helpers.rstrip()]
    lines.append("")
    Path(path).write_text("\n".join(lines))

# -----------------------------------------------------------------------------
# 1) WeChat live / interactive copy
# -----------------------------------------------------------------------------
wechat_values = extract_cn_strings(["app/InteractiveWechat.tsx"])
write_map(
    "content/wechatLiveDialogues.ts",
    "WECHAT_LIVE_DIALOGUES",
    "editWechatLive",
    wechat_values,
    "// 微信调查过程文案。左边原句不要改，只改冒号右边的新句子。\n// 这里覆盖快捷回复、材料回复、自我介绍、周川翻脸等运行中消息。",
)

p = Path("app/InteractiveWechat.tsx")
s = p.read_text()
imp = 'import {editWechatLive} from "../content/wechatLiveDialogues";\n'
if imp not in s:
    s = replace_once(s, 'import {WECHAT_CONTACTS} from "../content/wechatDialogues";\n', 'import {WECHAT_CONTACTS} from "../content/wechatDialogues";\n'+imp, "wechat live import")
s = replace_once(
    s,
    'const emitWechatNotice=(contactId:string,text:string)=>{const c=contacts.find(x=>x.id===contactId);if(c)wechatNoticeSubscribers.forEach(fn=>fn({contactId,name:c.name,text}))};',
    'const emitWechatNotice=(contactId:string,text:string)=>{const c=contacts.find(x=>x.id===contactId);if(c)wechatNoticeSubscribers.forEach(fn=>fn({contactId,name:c.name,text:editWechatLive(text)}))};',
    "wechat notice transform",
)
s = replace_once(
    s,
    ' const previewFor=(c:Contact)=>{const added=extra[c.id]||[];return added.length?added[added.length-1].text:c.preview};',
    ' const previewFor=(c:Contact)=>{const added=extra[c.id]||[];return editWechatLive(added.length?added[added.length-1].text:c.preview)};',
    "wechat preview transform",
)
s = replace_once(s, ':<p>{m.text}</p>', ':<p>{editWechatLive(m.text)}</p>', "wechat bubble transform")
s = replace_once(s, '}}>{item.text}</button>)}</div>}', '}}>{editWechatLive(item.text)}</button>)}</div>}', "wechat quick transform")
p.write_text(s)

# -----------------------------------------------------------------------------
# 2) Forum copy: current forum data still owns clue/search structure; this file
#    only changes visible prose. That means dialogue polish is low-risk.
# -----------------------------------------------------------------------------
forum_values = extract_cn_strings([
    "content/gameData.ts",
    "content/gameDataFlow.ts",
    "content/gameDataFlowV2.ts",
])
forum_helpers = '''export const applyForumPost=<T extends {title:string;excerpt:string;body:string[];replies:Array<{text:string}>;archive?:string}>(post:T):T=>({
  ...post,
  title:editForumText(post.title),
  excerpt:editForumText(post.excerpt),
  body:post.body.map(editForumText),
  replies:post.replies.map(reply=>({...reply,text:editForumText(reply.text)})),
  archive:post.archive?editForumText(post.archive):post.archive,
});

export const applyPrivateEntry=<T extends {title:string;body:string[]}>(entry:T):T=>({
  ...entry,
  title:editForumText(entry.title),
  body:entry.body.map(editForumText),
});'''
write_map(
    "content/forumDialogues.ts",
    "FORUM_DIALOGUES",
    "editForumText",
    forum_values,
    "// 论坛可见文案。左边原句不要改，只改右边。\n// 覆盖帖子标题、摘要、正文、楼层回复、存档说明，以及私密主题正文。\n// 搜索关键词/ID/触发逻辑仍留在原数据文件，不会因为润色一句话被误删。",
    forum_helpers,
)

p = Path("app/page.tsx")
s = p.read_text()
forum_imp = 'import {applyForumPost,applyPrivateEntry} from "../content/forumDialogues";\n'
if forum_imp not in s:
    s = replace_once(s, 'import {history,Post,posts,privateEntries,profile} from "../content/gameDataFlowV2";\n', 'import {history,Post,posts,privateEntries,profile} from "../content/gameDataFlowV2";\n'+forum_imp, "forum copy import")
s = replace_once(s, 'const investigationPosts=posts;', 'const investigationPosts=posts.map(applyForumPost);', "forum posts transform")
s = replace_once(s, 'const investigationPrivateEntries=privateEntries;', 'const investigationPrivateEntries=privateEntries.map(applyPrivateEntry);', "forum private transform")
p.write_text(s)

# -----------------------------------------------------------------------------
# 3) Admin record copy
# -----------------------------------------------------------------------------
admin_values = extract_cn_strings(["app/AdminPortalOccult.tsx"])
write_map(
    "content/adminDialogues.ts",
    "ADMIN_DIALOGUES",
    "editAdminText",
    admin_values,
    "// 管理员后台档案/记录文案。左边原句不要改，只改右边。\n// Record 卡片中的标题、状态说明和正文都会走这里。",
)

p = Path("app/AdminPortalOccult.tsx")
s = p.read_text()
admin_imp = 'import {editAdminText} from "../content/adminDialogues";\n'
if admin_imp not in s:
    s = replace_once(s, 'import {childLin} from "./adminPortraits/childLin";\n', 'import {childLin} from "./adminPortraits/childLin";\n'+admin_imp, "admin copy import")
s = replace_once(s, '<b>{title}</b><small style={metaStrong?', '<b>{editAdminText(title)}</b><small style={metaStrong?', "admin record title")
s = replace_once(s, '>{meta}</small><p>{text}</p></span></div>}', '>{editAdminText(meta)}</small><p>{editAdminText(text)}</p></span></div>}', "admin record body")
s = s.replace('text={`申请原文：${text}`}', 'text={`申请原文：${editAdminText(text)}`}')
# Liturgy lines and its one-off system message.
s = s.replace('}}>{text}</p>;\n return <><div style={s.sectionTitle}>诵录</div>', '}}>{editAdminText(text)}</p>;\n return <><div style={s.sectionTitle}>诵录</div>')
s = s.replace('>访问者徐宁，未登记候舍编号。</div>', '>{editAdminText("访问者徐宁，未登记候舍编号。")}</div>')
p.write_text(s)

# -----------------------------------------------------------------------------
# 4) Ending copy
# -----------------------------------------------------------------------------
ending_values = extract_cn_strings(["app/GameEnding.tsx"])
write_map(
    "content/endingDialogues.ts",
    "ENDING_DIALOGUES",
    "editEndingText",
    ending_values,
    "// 三个结局的可见文案。左边原句不要改，只改右边。",
)

p = Path("app/GameEnding.tsx")
s = p.read_text()
ending_imp = 'import {editEndingText} from "../content/endingDialogues";\n'
if ending_imp not in s:
    s = replace_once(s, 'import {CSSProperties,ReactNode,useEffect,useState} from "react";\n', 'import {CSSProperties,ReactNode,useEffect,useState} from "react";\n'+ending_imp, "ending copy import")
s = replace_once(
    s,
    'function Bubble({mine=false,children}:{mine?:boolean;children:ReactNode}){return <div style={{...s.bubble,...(mine?s.mine:{})}}>{children}</div>}',
    'function Bubble({mine=false,children}:{mine?:boolean;children:ReactNode}){return <div style={{...s.bubble,...(mine?s.mine:{})}}>{typeof children==="string"?editEndingText(children):children}</div>}',
    "ending bubble transform",
)
s = s.replace('{draft||""}', '{draft?editEndingText(draft):""}')
s = s.replace('验证消息：{friendRequest.text}', '验证消息：{editEndingText(friendRequest.text)}')
s = s.replace('<span>{notice.text}</span>', '<span>{editEndingText(notice.text)}</span>')
s = s.replace('<p key={i}>{x}</p>', '<p key={i}>{editEndingText(x)}</p>')
s = replace_once(
    s,
    'function EndingTitle({title,sub}:{title:string;sub:string}){return <div style={s.ending}><small>{sub}</small><h1>《{title}》</h1></div>}',
    'function EndingTitle({title,sub}:{title:string;sub:string}){return <div style={s.ending}><small>{editEndingText(sub)}</small><h1>《{editEndingText(title)}》</h1></div>}',
    "ending title transform",
)
p.write_text(s)

# -----------------------------------------------------------------------------
# 5) Human editing guide
# -----------------------------------------------------------------------------
Path("content/README_EDIT_TEXT.md").write_text('''# 文案编辑区（给人直接改的）

当前开发分支：`agent/v8-forum-gameplay-rework`

## 最常改的文件

1. `wechatDialogues.ts`
   - 微信已有历史聊天。
   - `preview` 是左侧会话列表的最近消息摘要，不会变成聊天气泡。
   - `text` 是真正聊天内容。

2. `wechatLiveDialogues.ts`
   - 玩家调查过程中才出现的微信台词：快捷选择、发材料后的回复、自我介绍、周川翻脸等。
   - 格式是 `"原句":"显示的新句子"`。
   - **只改冒号右边。左边是程序查找键，不要改。**

3. `forumDialogues.ts`
   - 论坛标题、摘要、正文、楼层回复、存档说明、私密主题正文。
   - 同样只改冒号右边。
   - 线索关键词和帖子 ID 不在这里，所以润色正常不会把搜索链改坏。

4. `adminDialogues.ts`
   - 管理员后台档案 Record 的标题/状态/正文，以及候舍申请原话等。
   - 只改右边。

5. `endingDialogues.ts`
   - 《归家》《谁是我》《双归》的可见文案。
   - 只改右边。

## 例子

```ts
"你怎么知道我给她发了？":"你怎么知道我给她发了？？",
```

左边不要动；右边想怎么润都行。

## GitHub 网页编辑保存不了时

你对仓库有 admin / push 权限，所以一般不是权限问题。我们开发时机器人也会往同一分支提交；如果你打开编辑页以后分支又有新 commit，网页会变成旧版本，GitHub 可能拒绝直接提交。

处理方法：
1. 先确认左上角分支是 `agent/v8-forum-gameplay-rework`；
2. 刷新文件页面，再点铅笔重新编辑；
3. 我在你编辑期间不要同时往这个分支推代码；
4. 改完点 `Commit changes...`，直接提交到当前分支即可。

如果又报错，把 GitHub 那句红色报错原文发给我，我可以直接判断是哪一种。
''')

print("editable copy extraction applied")
