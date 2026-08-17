from pathlib import Path

repls={
 'content/gameDataFlowV2.ts':[
  ('"赤烛照舍"','"赤烛引客"'),
  ('至少‘定名’这个说法我没见过','至少‘镇舍’这个说法我没见过'),
 ],
 'app/page.tsx':[
  ('赤烛照舍，黄符定名。','赤烛引客，黄符镇舍。'),
 ],
 'app/AdminPortalOccult.tsx':[
  ('type Guest="甲客"|"乙客";\ntype DoorState={left:Guest[];right:Guest[]};\ntype MemorySide="舍"|"客";\n',''),
 ],
}
for path, pairs in repls.items():
 p=Path(path); s=p.read_text()
 for a,b in pairs: s=s.replace(a,b)
 p.write_text(s)

# Guard live code against old name-as-mechanic wording.
for path in ['app/AdminPortalOccult.tsx','app/page.tsx','content/gameDataFlowV2.ts']:
 s=Path(path).read_text()
 for banned in ['名可夺','名不随客','守原名','随客易名','黄符定名']:
  if banned in s:
   raise SystemExit(f'{path}: banned live wording remains: {banned}')
