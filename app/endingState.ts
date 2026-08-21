export type EndingKind="home"|"true"|"double"|null;

let ending:EndingKind=null;
let finalDecisionUnlocked=false;
const subscribers=new Set<(kind:EndingKind)=>void>();

const markThreatSeen=()=>{finalDecisionUnlocked=true};

if(typeof window!=="undefined"&&typeof MutationObserver!=="undefined"){
 const scan=()=>{
  const text=document.body?.innerText||"";
  if(text.includes("沈妍还在我们手里")||text.includes("我就是在威胁你"))markThreatSeen();
 };
 const start=()=>{
  scan();
  const root=document.body;
  if(!root)return;
  const observer=new MutationObserver(scan);
  observer.observe(root,{subtree:true,childList:true,characterData:true});
 };
 if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start,{once:true});
 else start();
}

export const getEnding=()=>ending;
export const subscribeEnding=(fn:(kind:EndingKind)=>void)=>{subscribers.add(fn);return ()=>{subscribers.delete(fn)}};
export const beginEnding=(kind:Exclude<EndingKind,null>)=>{
 if(ending)return false;
 // All three endings must come after the late Zhou Chuan threat beat.
 // Older Liang Yin quick replies may discuss calling police, but they can no longer
 // skip the hostile reveal and terminate the game early.
 if(!finalDecisionUnlocked)return false;
 ending=kind;
 subscribers.forEach(fn=>fn(ending));
 return true;
};
