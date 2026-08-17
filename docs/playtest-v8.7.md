# v8.9.13 investigation flow playtest

- 林楠 discovery no longer relies on compound queries such as “2004 九岁 姓林” or “岚棉三厂 走失”.
- The 三厂 old-resident reply surfaces the natural phrase “寻人启事”; searching that phrase leads to an old resident discussion, then to the 报刊索引 user's history, and only there to the old report that reveals 林楠.
- First private layer unlocks with 林楠 but excludes the deeper scripture mechanism note.
- The early private dream note is written as 沈妍自己的凌晨记录，不再使用“先别补字/不要解释”之类作者教学语气；仅包含她实际记得的“楠楠/囡囡”和房间细节。
- The early dream note can no longer be sent to 梁茵. There is no supported logical bridge from that note to the “被找回来之前的家” forum thread.
- 红铁皮盒 unlocks the local cache; the cache exposes the eight-character phrase 身非我身名非我名.
- The eight-character phrase cannot reveal the mechanism by itself: archive_0712.zip only appears inside the 林楠-unlocked private investigation layer.
- Material buttons derive their state from the shared collected-material list. If sanmen / verse / a private record is already collected, the source surface shows 已添加 instead of a stale 添加到材料 button.
- WeChat keeps a persistent list of collected materials and a persistent in-session conversation state. Switching from WeChat to Browser/Files and back does not erase sent messages, delayed NPC replies, introductions, or one-shot material-send state.
- Material sending is selective per contact and one-shot per material/contact pair; some valid sends intentionally receive no immediate reply.
- WeChat material replies now depend on what that specific contact has actually received. 周川 only compares the 林楠 and 沈妍 childhood reports after both have been sent to him; the comparison works regardless of which one is sent first.
- NPCs may only react to information contained in the material they actually received or earlier material that the same player has already sent them. They no longer know unseen reports or later names by convenience.
- NPC-returned forum posts require an explicit bridge in the received text: private-p3's “另一个家” can remind 梁茵 of #14692, while its ordinary taste-change example can remind 周川 of #17428.
- 《三门疏》 responses are context-sensitive: without case context, contacts mostly say they do not understand it; only after the player has already supplied relevant paired-case/anomaly material do they cautiously connect wording across sources.
- The private anomaly note is now titled “9月11日，几条旧帖” and reads like a working note rather than a player instruction sheet.
- Tutorial-like forum chrome was reduced: the search box uses a normal site placeholder and the sidebar shows archive-migration information instead of telling the player how to investigate.
- The player explicitly chooses which eligible collected material to send.
- WeChat header and composer stay fixed while the message history scrolls independently.
