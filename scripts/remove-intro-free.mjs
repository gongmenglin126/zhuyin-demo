import fs from 'node:fs';

// One-shot, idempotent cleanup for the three intro-only free-text shortcuts.
const path='app/InteractiveWechat.tsx';
let s=fs.readFileSync(path,'utf8');
const replacements=[
  [
    '  const free:QuickReply={id:"yq-free-intro",text:"自己问一句…",freeText:true,reply:[],next:[when]};\n  return {parts:[{text:"你是徐宁？沈妍提过你。"},{text:"她今天还没回你？昨晚我们确实见过。"}],next:[when,free]};',
    '  return {parts:[{text:"你是徐宁？沈妍提过你。"},{text:"她今天还没回你？昨晚我们确实见过。"}],next:[when]};'
  ],
  [
    '  const free:QuickReply={id:"zc-free-intro",text:"自己问一句…",freeText:true,reply:[],next:[recent]};\n  return {parts:[{text:"徐宁？她提过你。"},{text:"她今天一直没回？电话也不通？"}],next:[recent,free]};',
    '  return {parts:[{text:"徐宁？她提过你。"},{text:"她今天一直没回？电话也不通？"}],next:[recent]};'
  ],
  [
    '  const free:QuickReply={id:"ly-free-intro",text:"自己问一句…",freeText:true,reply:[],next:[know]};\n  return {parts:[{text:"徐宁？我知道你，沈妍提过。"},{text:"她怎么了？"}],next:[know,free]};',
    '  return {parts:[{text:"徐宁？我知道你，沈妍提过。"},{text:"她怎么了？"}],next:[know]};'
  ],
];
for(const [oldText,newText] of replacements){
  if(s.includes(oldText)) s=s.replace(oldText,newText);
  else if(s.includes('自己问一句…')) throw new Error('Expected intro free-text block not found; refusing partial edit');
}
if(s.includes('yq-free-intro')||s.includes('zc-free-intro')||s.includes('ly-free-intro')) throw new Error('Intro free-text shortcuts still present');
fs.writeFileSync(path,s);
