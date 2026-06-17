#!/usr/bin/env node
/** Upload only oversized files (listed in r2-large-files.txt) to R2. */
import { readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { extname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
const BUCKET = "mentescriativas";
const MANIFEST = join(ROOT, "r2-large-files.txt");

const MIME = { ".pdf": "application/pdf" };

const lines = readFileSync(MANIFEST, "utf8")
  .split("\n")
  .map((l) => l.trim())
  .filter((l) => l && !l.startsWith("#"));

if (lines.length === 0) {
  console.log("No large files to upload.");
  process.exit(0);
}

console.log(`Uploading ${lines.length} large file(s) to R2...\n`);

for (const key of lines) {
  const filePath = join(ROOT, key.replace(/\//g, "\\"));
  const ext = extname(filePath).toLowerCase();
  const contentType = MIME[ext] ?? "application/octet-stream";
  console.log(`  ${key}`);
  execFileSync(
    "npx",
    [
      "wrangler",
      "r2",
      "object",
      "put",
      `${BUCKET}/${key}`,
      "--file",
      filePath,
      "--content-type",
      contentType,
      "--remote",
    ],
    { stdio: "inherit", cwd: ROOT, shell: true },
  );
}

console.log("\nDone.");
