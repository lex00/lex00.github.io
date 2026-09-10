// Prose lint for posts, on the `sentences` trope ruleset - the AI-writing
// tells (em-dash density, colon reveals, tricolons, anaphora, bold-first
// bullets) that tropes.fyi catalogues.
//
//   node scripts/prose-lint.mjs content/posts/some-post.md
//   node scripts/prose-lint.mjs content/posts/*.md
//
// Needs `npm install sentences`. Only medium and high are worth acting on;
// candidate and low are leads, not verdicts.
import { readFileSync } from "node:fs";
import { RULES } from "sentences/lint/registry";
import { runRules } from "sentences/lint/engine";
import { buildDocAnalysis } from "sentences/lint/build-doc";
import { extractProse } from "sentences/lint/markdown-prose";

const ORDER = { high: 0, medium: 1, low: 2, candidate: 3 };

function lineOf(text, offset) {
  if (offset == null) return null;
  return text.slice(0, offset).split("\n").length;
}

let gated = 0;
for (const file of process.argv.slice(2)) {
  const raw = readFileSync(file, "utf8");
  // Strip YAML frontmatter and Hugo shortcodes before linting. Frontmatter
  // reads as colon-reveals and its `---` fences count as em dashes; a
  // figure's alt text is a transcription of a table, so its repetition is
  // the table's, not the prose's. Blank them out rather than delete, so
  // reported offsets still line up with the file.
  const text = raw
    .replace(/^---\n[\s\S]*?\n---\n/, (m) => m.replace(/[^\n]/g, " "))
    .replace(/\{\{<[\s\S]*?>\}\}/g, (m) => m.replace(/[^\n]/g, " "));
  const prose = extractProse(text);
  const doc = buildDocAnalysis(prose);
  const { findings, errors } = runRules(RULES, doc);
  if (errors?.length) console.error(`${file}: rule errors`, errors);

  const sorted = [...findings].sort(
    (a, b) => (ORDER[a.severity] ?? 9) - (ORDER[b.severity] ?? 9),
  );
  const counts = {};
  for (const f of sorted) counts[f.severity] = (counts[f.severity] ?? 0) + 1;
  gated += (counts.high ?? 0) + (counts.medium ?? 0);

  console.log(`\n${file}  ${JSON.stringify(counts)}`);
  for (const f of sorted) {
    if (f.severity === "candidate") continue;
    const ln = lineOf(raw, f.start ?? f.offset ?? f.index);
    const where = ln ? `${file}:${ln}` : file;
    console.log(`  [${f.severity}] ${f.ruleId ?? f.rule}  ${where}`);
    const snip = (f.excerpt ?? f.text ?? f.message ?? "").replace(/\s+/g, " ");
    if (snip) console.log(`      ${snip.slice(0, 150)}`);
  }
}
process.exitCode = gated ? 1 : 0;
