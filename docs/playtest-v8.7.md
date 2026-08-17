# v8.9.14 investigation flow playtest

- 林楠 discovery still follows the natural chain: red tin box → 一格胶片 → 岚棉三厂 → 寻人启事 → 报刊索引 → old report. Browser history no longer leaks the 三厂 photo thread or the later “被找回来之前的家” anomaly thread.
- Player-facing author/tutorial voice was audited across the desktop, forum, local records, private area and archive surfaces. The opening no longer tells the player what 徐宁 thinks; the profile no longer instructs the player to inspect browser history; zero-result search no longer suggests puzzle-specific query strategies.
- The deprecated `0407` / edition-number Notes implementation and the unused static WeChat implementation were removed from `app/page.tsx` so old puzzle logic cannot resurface accidentally.
- Password UI no longer announces answer lengths such as “2 个汉字” or “4 个汉字”. Diegetic clues remain in the material itself.
- The early dream-thread replies were rewritten to sound like ordinary forum conversation instead of a cluster of investigation tutorials such as “先画结构 / 不要补名字 / 从某类关键词入手”.
- 林楠、沈妍旧报 replies no longer carry the deprecated edition-number puzzle or methodological directions aimed at the player.
- #14692 and #17428 now keep only plausible lived-experience discussion plus the repeated 照骨 questionnaire pattern. Repetition can be noticed by the player without a narrator announcing it.
- #11208 has one canonical visible implementation in the V2 post set: a provenance/version-comparison thread. The older mechanism-explaining duplicate is replaced rather than appended.
- WeChat historical conversations were rewritten as actual relationship history rather than exposition dialogue. 徐宁/沈妍 have ordinary appointment banter; 余晴's history establishes the previous night's meeting through dinner chat; 周川's forum connection appears through casual talk about a dream post; 梁茵 naturally mentions retiring the `迟迟` account after intrusive private messages.
- WeChat contact notes are short contextual remarks (`小学同学`, `周川｜烛阴旧闻`, `梁茵｜烛阴旧闻`, etc.) rather than role/function descriptions.
- WeChat material replies remain one-shot and contact-state-aware. A contact may compare two reports only after that same contact has actually received both. The early “楠楠” private note is still not sendable to 梁茵.
- NPC-returned forum cards require a textual association in material the NPC actually received; they are not used merely to ferry the player to the next plot node.
- Switching between WeChat and Browser/Files preserves sent messages, delayed replies, introductions and one-shot material state.
