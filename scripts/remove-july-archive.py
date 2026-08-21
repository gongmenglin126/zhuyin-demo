from pathlib import Path

root = Path('.')

p = root / 'content/gameDataFlowV2.ts'
s = p.read_text(encoding='utf-8')

old_block = '''const julyBase=flowPosts.find(post=>post.id==="10731")!;
const julyArchive:Post={...julyBase,title:"2004 年 7 月两地地方报转载来源求考",replies:[reply("报刊索引","21:48","我核过目录号，不是重复转载。两条都有各自的首发版面。"),reply("纸页边角","22:03","差一天、同岁、都两周左右，难怪目录里看着像一条。"),reply("南站旧报摊","22:51","两地四百多公里，联系人也不一样，应该就是两起碰巧挨得很近。"),reply("折柳","23:02","这帖我当年看过。印象最深的就是两个“十三天”挨在一起。"),reply("地方志小王","23:07","对，我当时就是怕目录合并错了才发帖。","楼主")]};

'''
if old_block not in s:
    raise SystemExit('julyArchive block not found')
s = s.replace(old_block, '', 1)

old_patched = 'const patched=flowPosts.map(post=>post.id==="33897"?cottonYard:post.id==="09114"?linNanReport:post.id==="09831"?shenYanReport:post.id==="20847"?dreamPost:post.id==="30177"?redBoxPost:post.id==="34049"?wallPost:post.id==="14692"?returnedCase:post.id==="10731"?julyArchive:post.id==="17428"?traumaCase:post.id==="11208"?scriptureComparePost:post);'
new_patched = 'const patched=flowPosts.filter(post=>post.id!=="10731").map(post=>post.id==="33897"?cottonYard:post.id==="09114"?linNanReport:post.id==="09831"?shenYanReport:post.id==="20847"?dreamPost:post.id==="30177"?redBoxPost:post.id==="34049"?wallPost:post.id==="14692"?returnedCase:post.id==="17428"?traumaCase:post.id==="11208"?scriptureComparePost:post);'
if old_patched not in s:
    raise SystemExit('patched mapping target not found')
s = s.replace(old_patched, new_patched, 1)
p.write_text(s, encoding='utf-8')

q = root / 'app/page.tsx'
t = q.read_text(encoding='utf-8')
old_share = 'const SHAREABLE_POST_IDS=new Set(["33897","09114","09831","10731","14692","17428","11208","23109","27614"]);'
new_share = 'const SHAREABLE_POST_IDS=new Set(["33897","09114","09831","14692","17428","11208","23109","27614"]);'
if old_share not in t:
    raise SystemExit('shareable post ids target not found')
t = t.replace(old_share, new_share, 1)
q.write_text(t, encoding='utf-8')

print('removed July archive thread 10731 from active forum flow')
