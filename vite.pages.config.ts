import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

const repositoryName = process.env.GITHUB_REPOSITORY?.split("/")[1] || "zhuyin-demo";
const base = `/${repositoryName}/`;

export default defineConfig({
  root: "pages-entry",
  base,
  publicDir: "../public",
  plugins: [
    {
      name: "github-pages-public-assets",
      enforce: "pre",
      transform(code, id) {
        if (!id.endsWith("app/globals.css")) return null;
        return code.replaceAll("url('/assets/", `url('${base}assets/`);
      },
    },
    react(),
  ],
  build: {
    outDir: "../pages-dist",
    emptyOutDir: true,
  },
});
