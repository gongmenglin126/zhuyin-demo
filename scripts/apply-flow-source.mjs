import {readFile,writeFile} from "node:fs/promises";

const path="app/page.tsx";
let source=await readFile(path,"utf8");
source=source.replace('from "../content/gameData";','from "../content/gameDataFlow";');

const marker=/const contextPosts:Post\[\]=\[[\s\S]*?\n\];\n\nconst investigationPosts=\[\.\.\.posts,\.\.\.contextPosts\];\nconst investigationPrivateEntries=privateEntries\.map\(entry=>\{[\s\S]*?\n\}\);\n\nexport default function Page\(\)\{/;

if(marker.test(source)){
  source=source.replace(marker,`const contextPosts:Post[]=[];\nconst investigationPosts=posts;\nconst investigationPrivateEntries=privateEntries;\n\nexport default function Page(){`);
}

await writeFile(path,source);
console.log("Applied knowledge-driven forum flow layer to v8 page.");
// v9.2 admin storyflow trigger
