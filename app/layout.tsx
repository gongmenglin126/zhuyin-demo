import type { Metadata } from "next";
import "./globals.css";
import "./game.css";
import "./game-fixes.css";

export const metadata: Metadata = {
  title: "烛阴旧闻：第一阶段试玩",
  description: "在失踪朋友沈妍的电脑里，从一座普通论坛开始调查。",
  other: {
    "codex-preview": "development",
  },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
