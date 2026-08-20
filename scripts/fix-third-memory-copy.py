from pathlib import Path

p=Path('content/adminDialogues.ts')
s=p.read_text()
old='  "能描述不属于登记身份的旧屋细节；听到‘徐宁’时持续哭泣，随后反问‘她是谁，为什么我知道这个名字？’":"能描述不属于登记身份的旧屋细节；听到‘徐宁’时持续哭泣，随后反问‘她是谁，为什么我知道这个名字？’",'
new='  "能描述不属于登记身份的旧屋细节；听到‘徐宁’时持续哭泣，随后反问‘她是谁，为什么我知道这个名字？’":"能说出少量与沈妍童年相符的记忆片段；人物、地点与时间顺序无法连续对应。听到‘徐宁’时有短暂熟悉反应，但无法说明是谁。",'
if old not in s:
    raise SystemExit('target line not found')
p.write_text(s.replace(old,new,1))

# trigger workflow
