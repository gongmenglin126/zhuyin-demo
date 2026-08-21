import { execFileSync } from "node:child_process";
import { copyFile, mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const pagesDirectory = path.join(projectRoot, "pages-dist");
const outputDirectory = path.join(projectRoot, "single-dist");

execFileSync(process.platform === "win32" ? "npm.cmd" : "npm", ["run", "build:pages"], {
  cwd: projectRoot,
  stdio: "inherit",
});

const mimeTypes = new Map([
  [".css", "text/css"],
  [".gif", "image/gif"],
  [".jpeg", "image/jpeg"],
  [".jpg", "image/jpeg"],
  [".js", "text/javascript"],
  [".png", "image/png"],
  [".svg", "image/svg+xml"],
  [".webp", "image/webp"],
  [".woff", "font/woff"],
  [".woff2", "font/woff2"],
]);

async function listFiles(directory, prefix = "") {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    const relativePath = path.posix.join(prefix, entry.name);
    if (entry.isDirectory()) {
      files.push(...(await listFiles(path.join(directory, entry.name), relativePath)));
    } else {
      files.push(relativePath);
    }
  }

  return files;
}

function replaceAllLiteral(source, search, replacement) {
  return source.split(search).join(replacement);
}

let html = await readFile(path.join(pagesDirectory, "index.html"), "utf8");
const scriptMatch = html.match(/<script\b[^>]*\bsrc="([^"]+)"[^>]*><\/script>/);
const styleMatch = html.match(/<link\b[^>]*\brel="stylesheet"[^>]*\bhref="([^"]+)"[^>]*>/);

if (!scriptMatch || !styleMatch) {
  throw new Error("Could not locate the generated JavaScript and CSS assets.");
}

const assetPathFromUrl = (url) => url.replace(/^\/[^/]+\//, "").replace(/^\.\//, "");
let script = await readFile(path.join(pagesDirectory, assetPathFromUrl(scriptMatch[1])), "utf8");
let style = await readFile(path.join(pagesDirectory, assetPathFromUrl(styleMatch[1])), "utf8");

const generatedAssets = (await listFiles(pagesDirectory))
  .filter((relativePath) => relativePath !== "index.html")
  .filter((relativePath) => !relativePath.endsWith(".js") && !relativePath.endsWith(".css"));

for (const relativePath of generatedAssets) {
  const absolutePath = path.join(pagesDirectory, relativePath);
  const extension = path.extname(relativePath).toLowerCase();
  const mimeType = mimeTypes.get(extension) || "application/octet-stream";
  const dataUrl = `data:${mimeType};base64,${(await readFile(absolutePath)).toString("base64")}`;
  const candidates = [
    `/zhuyin-demo/${relativePath}`,
    `./${relativePath}`,
    relativePath,
  ];

  for (const candidate of candidates) {
    html = replaceAllLiteral(html, candidate, dataUrl);
    script = replaceAllLiteral(script, candidate, dataUrl);
    style = replaceAllLiteral(style, candidate, dataUrl);
  }
}

const inlineStyle = `<style>${style.replaceAll("</style", "<\\/style")}</style>`;
const inlineScript = `<script type="module">${script.replaceAll("</script", "<\\/script")}</script>`;

html = html
  .replace(styleMatch[0], () => inlineStyle)
  .replace(scriptMatch[0], () => inlineScript);

await mkdir(outputDirectory, { recursive: true });

// Keep a real copy of every non-JS/CSS asset alongside the single-file build.
// Most assets are inlined above, but runtime-generated/serialized paths can survive
// bundling as literal URLs. Publishing these files makes those paths reliable too.
for (const relativePath of generatedAssets) {
  const sourcePath = path.join(pagesDirectory, relativePath);
  const targetPath = path.join(outputDirectory, relativePath);
  await mkdir(path.dirname(targetPath), { recursive: true });
  await copyFile(sourcePath, targetPath);
}

await writeFile(path.join(outputDirectory, "index.html"), html);

console.log(`Single-file build written to ${path.join(outputDirectory, "index.html")}`);
console.log(`Copied ${generatedAssets.length} fallback assets into single-dist.`);
