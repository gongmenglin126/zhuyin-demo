from pathlib import Path
import re

root=Path('.')
page=root/'app/page.tsx'
admin=root/'app/AdminPortalOccult.tsx'

p=page.read_text(encoding='utf-8')
old_func=re.search(r'function RecoveredRitualAttachment\(\)\{.*?\n\}\nfunction Floor',p,re.S)
assert old_func, 'RecoveredRitualAttachment not found'
new_func='''function RecoveredRitualAttachment(){
 const [phase,setPhase]=useState<"closed"|"error"|"open">("closed");
 if(phase==="closed")return <section style={{margin:"18px 24px",padding:16,border:"1px solid #d5cabc",background:"#f2ede4"}}><div style={{display:"flex",alignItems:"center",gap:8,marginBottom:5}}><b style={{fontSize:13}}>失效附件</b><em style={{padding:"2px 6px",borderRadius:4,background:"#ead8d3",color:"#8d3e35",fontSize:10,fontStyle:"normal"}}>恢复失败</em></div><small style={{display:"block",margin:"0 0 12px",color:"#81766d"}}>thumb_2012_0712.jpg</small><button onClick={()=>setPhase("error")} style={{padding:"7px 11px",border:"1px solid #b8afa5",background:"#fff",borderRadius:5}}>打开附件</button></section>;
 if(phase==="error")return <button onClick={()=>setPhase("open")} style={{width:"calc(100% - 48px)",height:210,margin:"18px 24px",border:"1px solid #341312",background:"#050505",color:"#7d1716",font:"700 28px serif",letterSpacing:".28em"}}>门未闭。<small style={{display:"block",marginTop:20,color:"#655a56",font:"11px sans-serif",letterSpacing:0}}>缓存读取失败 · 点击重试</small></button>;
 return <section style={{margin:"18px auto",width:"min(720px,92%)",display:"grid",gap:12}}>
  <figure style={{margin:0,padding:10,border:"1px solid #2b2420",background:"#100d0c"}}><img src="assets/occult/recovered-ritual-v904.webp" alt="恢复出的旧仪式现场照片" style={{display:"block",width:"100%",background:"#080706"}}/><figcaption style={{padding:"9px 2px 1px",color:"#9d8f86",fontSize:11}}>恢复帧 01　原图缺损，色彩已严重偏移</figcaption></figure>
  <figure style={{margin:0,padding:10,border:"1px solid #2b2420",background:"#100d0c"}}><img src="assets/occult/recovered-talisman-v904.webp" alt="恢复出的黄纸局部" style={{display:"block",width:"100%",maxHeight:420,objectFit:"contain",background:"#080706"}}/><figcaption style={{padding:"9px 2px 1px",color:"#9d8f86",fontSize:11}}>恢复帧 02　黄纸局部裁切</figcaption></figure>
 </section>;
}
function Floor'''
p=p[:old_func.start()]+new_func+p[old_func.end():]
p=p.replace('assets/occult/huanzhen-scripture.webp','assets/occult/huanzhen-scripture-v904.webp')
page.write_text(p,encoding='utf-8')

a=admin.read_text(encoding='utf-8')
old=''' const [moods,setMoods]=useState<Record<Child,"neutral"|"frown">>({lin:"neutral",shen:"neutral"});
 const [bothReach,setBothReach]=useState(false);'''
new=''' const [moods,setMoods]=useState<Record<Child,"neutral"|"frown"|"smile">>({lin:"neutral",shen:"neutral"});'''
assert old in a, 'mood/bothReach state not found'
a=a.replace(old,new,1)
old='''  if(id==="box"){
   if(target==="center"){
    const next={...items,box:"center" as const};
    setItems(next);setBothReach(true);setDragItem(null);completeTable(next);return;
   }
   setBothReach(true);setDragItem(null);window.setTimeout(()=>{if(items.box!=="center")setBothReach(false)},850);return;
  }'''
new='''  if(id==="box"){
   if(target==="center"){
    const next={...items,box:"center" as const};
    setItems(next);setMoods({lin:"neutral",shen:"neutral"});setDragItem(null);completeTable(next);return;
   }
   const other:Child=target==="lin"?"shen":"lin";
   setMoods(m=>({...m,[target]:"neutral",[other]:"smile"}));
   setDragItem(null);
   window.setTimeout(()=>setMoods(m=>({...m,[other]:"neutral"})),850);
   return;
  }'''
assert old in a, 'box interaction block not found'
a=a.replace(old,new,1)
old='''     <TableSeat place="4栋东侧" mood={moods.lin} reach={bothReach||items.box==="center"} side="left" onDrop={()=>giveItem("lin")} items={ordinaryItems.filter(id=>items[id]==="lin")}/>
     <div style={v.centerTable} onDragOver={e=>e.preventDefault()} onDrop={()=>giveItem("center")}>
      <div style={v.tableTop}>
       {(["plum","marble","milk","clip","box"] as Item[]).filter(id=>!items[id]).map(id=><ObjectToken key={id} id={id} draggable onDragStart={()=>setDragItem(id)}/>) }
       {items.box==="center"&&<ObjectToken id="box"/>}
      </div>
     </div>
     <TableSeat place="青梧旧楼" mood={moods.shen} reach={bothReach||items.box==="center"} side="right" onDrop={()=>giveItem("shen")} items={ordinaryItems.filter(id=>items[id]==="shen")}/>'''
new='''     <TableSeat place="4栋东侧" mood={moods.lin} side="left" onDrop={()=>giveItem("lin")} items={ordinaryItems.filter(id=>items[id]==="lin")}/>
     <div style={v.centerTable} onDragOver={e=>e.preventDefault()} onDrop={()=>giveItem("center")}>
      <div style={v.tableTop}>
       {(["plum","marble","milk","clip","box"] as Item[]).filter(id=>!items[id]).map(id=><ObjectToken key={id} id={id} draggable onDragStart={()=>setDragItem(id)}/>) }
       {items.box==="center"&&<ObjectToken id="box" opened/>}
      </div>
     </div>
     <TableSeat place="青梧旧楼" mood={moods.shen} side="right" onDrop={()=>giveItem("shen")} items={ordinaryItems.filter(id=>items[id]==="shen")}/>'''
assert old in a, 'stage2 table block not found'
a=a.replace(old,new,1)
old=re.search(r'function TableSeat\(\{place,mood,reach,side,onDrop,items\}.*?\n\}\n\nfunction ObjectToken',a,re.S)
assert old, 'TableSeat function not found'
new='''function TableSeat({place,mood,side,onDrop,items}:{place:string;mood:"neutral"|"frown"|"smile";side:"left"|"right";onDrop:()=>void;items:string[]}){
 return <section onDragOver={e=>e.preventDefault()} onDrop={onDrop} style={v.seat}>
  <small style={v.roomStamp}>{place}</small>
  <div style={v.seatedPerson}>
   <PaperPerson stamp={side==="left"?"07·18":"07·17"} mood={mood}/>
  </div>
  <div style={v.kept}>{items.map(id=><ObjectToken key={id} id={id}/>)}</div>
 </section>
}

function ObjectToken'''
a=a[:old.start()]+new+a[old.end():]
old=re.search(r'function ObjectToken\(\{id,draggable,onDragStart\}.*?\n\}\n\nconst v:',a,re.S)
assert old, 'ObjectToken function not found'
new='''function ObjectToken({id,draggable,onDragStart,opened}:{id:string;draggable?:boolean;onDragStart?:()=>void;opened?:boolean}){
 const labels:Record<string,string>={plum:"话梅糖",marble:"蓝玻璃弹珠",milk:"奶糖",clip:"红色发卡",box:"红铁皮盒"};
 return <div draggable={draggable} onDragStart={e=>{e.dataTransfer.effectAllowed="move";onDragStart?.()}} style={{...v.object,cursor:draggable?"grab":"default"}}>
  <i style={{...v.objectIcon,position:"relative",...(id==="plum"?v.plum:id==="marble"?v.marble:id==="milk"?v.milk:id==="clip"?v.clip:v.box)}}>{id==="box"&&opened&&<span style={{position:"absolute",left:1,right:1,top:-7,height:7,border:"1px solid #704236",borderBottom:0,background:"#7d2b23",transform:"rotate(-7deg)",transformOrigin:"left bottom",boxShadow:"0 -2px 8px #0008"}}/>}</i>
  <small>{labels[id]}</small>
 </div>
}

const v:'''
a=a[:old.start()]+new+a[old.end():]
a=a.replace('personHead:{position:"absolute",left:20,top:0,width:48,height:48,borderRadius:"50% 50% 44% 44%",background:"#d8c9a9",border:"1px solid #8d745c"}', 'personHead:{position:"absolute",left:18,top:0,width:52,height:49,clipPath:"polygon(11% 4%,88% 0,97% 24%,91% 78%,68% 100%,25% 95%,4% 72%,0 23%)",background:"linear-gradient(100deg,#c8b890,#e0d0a8 51%,#b7a27f)",border:"1px solid #745d4a",boxShadow:"inset 8px 0 15px #5b342515"}',1)
a=a.replace('eye:{position:"absolute",top:16,width:5,height:6,borderRadius:"50%",background:"#1b1714"}', 'eye:{position:"absolute",top:17,width:7,height:3,borderRadius:"45%",background:"#17120f",boxShadow:"0 0 3px #52120f"}',1)
a=a.replace('smile:{position:"absolute",left:12,top:25,width:24,height:11,borderBottom:"3px solid #4b1714",borderRadius:"0 0 18px 18px"}', 'smile:{position:"absolute",left:10,top:24,width:31,height:13,borderBottom:"3px solid #521411",borderRadius:"0 0 22px 22px",transform:"rotate(1deg)",boxShadow:"0 2px 2px #5b0f0d33"}',1)
a=a.replace('assets/occult/huanzhen-scripture.webp','assets/occult/huanzhen-scripture-v904.webp')
old=re.search(r'function RitualPhoto\(\)\{.*?\nfunction Record',a,re.S)
assert old, 'RitualPhoto not found'
new='''function RitualPhoto(){return <figure style={s.photo}><img src="assets/occult/recovered-redbox-v904.webp" alt="恢复出的红铁皮盒与纸偶旧照片" style={{display:"block",width:"100%",border:"1px solid #372824",background:"#0b0908"}}/><figcaption style={s.photoCaption}>IMG_1016_2047.jpg　恢复 14%</figcaption></figure>}
function Record'''
a=a[:old.start()]+new+a[old.end():]
admin.write_text(a,encoding='utf-8')

# Assertions for the intended removal/addition.
final_page=page.read_text(encoding='utf-8')
final_admin=admin.read_text(encoding='utf-8')
assert 'recovered-ritual-v904.webp' in final_page
assert 'recovered-talisman-v904.webp' in final_page
assert 'huanzhen-scripture-v904.webp' in final_page
assert 'bothReach' not in final_admin
assert 'reach=' not in final_admin
assert 'v.arm' not in final_admin
assert 'recovered-redbox-v904.webp' in final_admin
assert 'huanzhen-scripture-v904.webp' in final_admin
assert 'opened' in final_admin
print('v9.0.4 occult image + paper-doll feedback source patch applied')
