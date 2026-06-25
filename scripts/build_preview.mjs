import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { marked } from "file:///C:/Users/mayan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js";


const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(scriptDir, "..");
const markdown = fs.readFileSync(path.join(root, "README.md"), "utf8");
const body = marked.parse(markdown, { gfm: true, breaks: false });

const html = `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Mayank Shringi · GitHub Profile Preview</title>
  <style>
    :root { color-scheme: dark; }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: #0d1117;
      color: #e6edf3;
      font: 16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    main { width: min(1012px, calc(100% - 32px)); margin: 0 auto; padding: 28px 0 72px; }
    h2 { margin-top: 42px; padding-bottom: 10px; border-bottom: 1px solid #212a3b; font-size: 1.5rem; }
    h3 { margin: 14px 0 8px; font-size: 1.06rem; }
    p { color: #c9d1d9; }
    a { color: #58a6ff; }
    img { max-width: 100%; }
    table { width: 100%; border-spacing: 10px; margin: 10px -10px 18px; }
    td { padding: 18px; border: 1px solid #273858; border-radius: 14px; background: linear-gradient(145deg, #0f1625, #0c1220); }
    code { padding: 3px 7px; border: 1px solid #273858; border-radius: 6px; background: #111a2c; color: #a9c3ff; }
    blockquote { margin: 12px 0; padding: 12px 18px; border-left: 3px solid #7c3aed; background: #111526; color: #c9d1d9; }
    details { margin: 18px 0; padding: 14px 18px; border: 1px solid #273858; border-radius: 12px; background: #0f1522; }
    summary { cursor: pointer; color: #dce7ff; }
    ul { padding-left: 22px; }
    @media (max-width: 680px) {
      main { width: min(100% - 20px, 1012px); padding-top: 10px; }
      table, tbody, tr, td { display: block; width: 100% !important; }
      table { margin: 8px 0 16px; border-spacing: 0; }
      td { margin-bottom: 10px; padding: 14px; }
      h2 { margin-top: 32px; }
    }
  </style>
</head>
<body><main>${body}</main></body>
</html>`;

fs.writeFileSync(path.join(root, "preview.html"), html);
console.log("Created preview.html");
