from pathlib import Path

# trigger: apply Liang return-to-nest reaction
p=Path('app/InteractiveWechat.tsx')
s=p.read_text()
old='"admin-watchlist":{ly:[{text:"这么多人？"},{text:"……迟迟也在里面？"}],zc:[{text:"这么多人？"},{text:"这后台不像临时搭的。"}]},'
new='"admin-watchlist":{ly:[{text:"……"},{text:"我早就知道。"},{text:"我早就知道这个论坛不正常。"},{text:"我以前还以为只是这里怪人多。"},{text:"原来不是我们碰巧聚到一起。"},{text:"是它一直在等我们自己搜回来。"}],zc:[{text:"这么多人？"},{text:"这后台不像临时搭的。"}]},'
if old not in s:
    raise SystemExit('admin-watchlist target not found')
s=s.replace(old,new,1)
p.write_text(s)
