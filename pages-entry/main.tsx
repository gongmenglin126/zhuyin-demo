import React from "react";
import { createRoot } from "react-dom/client";
import Home from "../app/page";
import V9 from "../app/v9/page";
import "../app/globals.css";

const params = new URLSearchParams(window.location.search);
const Root = params.get("play") === "v9" ? V9 : Home;

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Root />
  </React.StrictMode>,
);
