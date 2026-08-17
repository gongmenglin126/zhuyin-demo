# v8.9.12 investigation flow playtest

- 林楠 discovery no longer relies on compound queries such as “2004 九岁 姓林” or “岚棉三厂 走失”.
- The 三厂 old-resident reply surfaces the natural phrase “寻人启事”; searching that phrase leads to an old resident discussion, then to the 报刊索引 user's history, and only there to the old report that reveals 林楠.
- First private layer unlocks with 林楠 but excludes the deeper scripture mechanism note.
- The early private dream note is written as沈妍自己的凌晨记录，不再使用“先别补字/不要解释”之类作者教学语气；仅包含她实际记得的“楠楠/囡囡”和房间细节。
- 红铁皮盒 unlocks the local cache; the cache exposes the eight-character phrase 身非我身名非我名.
- The eight-character phrase cannot reveal the mechanism by itself: archive_0712.zip only appears inside the 林楠-unlocked private investigation layer.
- Material buttons derive their state from the shared collected-material list. If sanmen / verse / a private record is already collected, the source surface shows 已添加 instead of a stale 添加到材料 button.
- WeChat keeps a persistent list of collected materials and a persistent in-session conversation state. Switching from WeChat to Browser/Files and back does not erase sent messages, delayed NPC replies, introductions, or one-shot material-send state.
- Material sending is selective per contact and one-shot per material/contact pair; some valid sends intentionally receive no immediate reply.
- NPCs may only react to information contained in the material they actually received. Sending the early “楠楠” private note cannot make an NPC spontaneously know the later name 林楠.
- NPCs can return clickable forum-post cards when that is a natural response, rather than always explaining the next step in prose.
- The player explicitly chooses which eligible collected material to send.
- WeChat header and composer stay fixed while the message history scrolls independently.
