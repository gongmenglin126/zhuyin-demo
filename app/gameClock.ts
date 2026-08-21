let minutes=19*60+6;
const subscribers=new Set<(time:string)=>void>();
const format=(value:number)=>`${String(Math.floor(value/60)%24).padStart(2,"0")}:${String(value%60).padStart(2,"0")}`;
export const getGameClock=()=>format(minutes);
export const advanceGameClock=(amount=1)=>{minutes+=Math.max(0,amount);const time=format(minutes);subscribers.forEach(fn=>fn(time));return time};
export const subscribeGameClock=(fn:(time:string)=>void)=>{subscribers.add(fn);fn(format(minutes));return()=>subscribers.delete(fn)};
