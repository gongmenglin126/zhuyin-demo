export type EndingKind="home"|"true"|"double"|null;

let ending:EndingKind=null;
const subscribers=new Set<(kind:EndingKind)=>void>();

export const getEnding=()=>ending;
export const subscribeEnding=(fn:(kind:EndingKind)=>void)=>{subscribers.add(fn);return ()=>{subscribers.delete(fn)}};
export const beginEnding=(kind:Exclude<EndingKind,null>)=>{
 if(ending)return false;
 ending=kind;
 subscribers.forEach(fn=>fn(ending));
 return true;
};
