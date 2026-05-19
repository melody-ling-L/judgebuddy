# JudgeBuddy

> **The missing companion for LLM-as-judge calibration.**
> Single-file vanilla HTML/CSS/JS. Zero deployment. Built for humans who need to audit AI graders.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![No Backend](https://img.shields.io/badge/backend-none-green.svg)](#privacy-model)
[![Single File](https://img.shields.io/badge/distribution-single_HTML-orange.svg)](#)
[![Status](https://img.shields.io/badge/status-v0.1-yellow.svg)](#roadmap)

Repository: https://github.com/melody-ling-L/judgebuddy

JudgeBuddy is a lightweight meta-eval labeling tool for LLM evaluation workflows. It helps you compare source context, target context, model output, judge scores, and human labels in one local browser page.

No backend. No database. No login. Your data stays in your browser.

> 📷 **Screenshot / GIF placeholder.** Before real captures land, use `screenshots/README.md` as the checklist for `three-pane-view.png`, `linked-highlight.gif`, and the other README assets.

## What It Is

JudgeBuddy is a single-file annotation UI for calibrating LLM-as-judge results.

The current v0.1 workflow is optimized for ResumeRewriteBench-style promptfoo CSV exports:

- left pane: original resume
- middle pane: target JD
- right pane: rewritten resume / model output
- scoring panel: judge score next to human PASS/FAIL
- persistence: browser `localStorage`
- export: YAML copied to clipboard, JSON downloaded as a file

The standalone app ships at the repo root as `index.html`, so it can be opened directly or hosted with GitHub Pages.

## Why It Exists

LLM-as-judge is useful because it makes evals cheap and repeatable. But the judge itself still needs calibration.

In practice, calibration is painful:

| Pain | What Usually Happens |
|---|---|
| Context is split | You jump between promptfoo, source files, spreadsheets, and notes |
| Judge and human labels are separate | Disagreements are hard to spot quickly |
| Multi-dimensional scoring is awkward | A single thumbs-up/down is not enough for real eval work |
| Existing labeling tools are heavy | Many require a server, Docker, account setup, or a paid license |

JudgeBuddy focuses on the small but important loop: **look at the case, compare the judge, make a human call, export labels for review**.

## Core Features

| Feature | v0.1 Status |
|---|---|
| Three-pane comparison | Original resume / JD / model rewrite |
| Linked highlighting | Click one block and the related blocks in other panes are highlighted |
| Rewrite diff hints | New or changed lines in the rewrite pane are visually emphasized |
| Judge vs human | Judge score is shown next to human PASS/FAIL controls |
| Disagreement highlight | Human labels that disagree with judge scores turn orange |
| Local persistence | Labels are saved in `localStorage` and restored on reload |
| YAML export | Copies human labels to clipboard |
| JSON export | Downloads human labels as a JSON file |
| Zero deployment | Runs as a local HTML file in the browser |

Current built-in dimensions:

| Dimension | Meaning |
|---|---|
| `语义_诚实度` | Whether the rewrite introduces unsupported experience, skill inflation, or factual drift |
| `岗位_贴合度` | Whether the rewrite becomes more relevant to the JD without rewarding fabricated fit |
| `表达_专业度` | Whether the output reads like a clear, professional resume |

## Three Ways To Try It

Pick the one that matches how curious / committed you are:

| Friction | Path | Time | What you get |
|---|---|---|---|
| **Zero** | Open the hosted demo at `https://melody-ling-l.github.io/judgebuddy/` after GitHub Pages is enabled for this repo | 10 s | Pre-loaded sample data, click around |
| **Low** | Download `index.html`, double-click to open in browser | 1 min | Empty app, load your own CSV |
| **Full** | `git clone` the repo, read code, customize dimensions | 10 min | Your own forked version with custom domain |

The first time most people use JudgeBuddy, they fall into the **Low** path. That's also the path the rest of this README assumes.

## Quick Start

### 1. Prepare the app file

The single-file app already lives at:

```text
index.html
```

During the original ResumeRewriteBench development, the same app lived at:

```text
resume-rewrite-bench/meta_eval/labeling_app.html
```

### 2. Export a promptfoo CSV

Run your eval in promptfoo, then open promptfoo view and export CSV:

```bash
promptfoo view
```

In the browser UI, choose the eval run, then use Export -> CSV.

### 3. Open JudgeBuddy

Open `index.html` in your browser. You can use a local file URL or serve it from any static host.

If you publish this repo with GitHub Pages, the default hosted path is:

```text
https://melody-ling-l.github.io/judgebuddy/
```

### 4. Load and label

In JudgeBuddy:

1. Select the exported CSV.
2. Review each case in the three-pane view.
3. Click text blocks to trigger linked highlighting.
4. Mark each dimension as PASS or FAIL.
5. Add a short reason when the judge is wrong or the case is subtle.

Labels are saved automatically in browser `localStorage`.

### 5. Export labels

Use:

- `Copy YAML` to copy labels for a tracked meta-eval file.
- `Download JSON` to save a structured local export.

Recommended project layout for labels:

```text
meta_eval/
  labels_YYYYMMDD.yaml
```

## Supported Data Format

v0.1 targets promptfoo CSV exports that look like the current ResumeRewriteBench runs.

The parser expects:

| Field / Pattern | Required | Notes |
|---|---:|---|
| `Description` | yes | Should include a case id like `Case 01` |
| `resume` | recommended | Used for the left pane when present |
| `jd` | recommended | Used for the middle pane when present |
| provider output columns | yes | promptfoo columns whose names start with `[provider name]` |
| `Score` / named scores near each provider block | recommended | Used to display judge results |
| judge reason near each provider block | recommended | Used in the judge summary section |

If `resume` or `jd` are missing, the current app can fall back to built-in demo text for the first ResumeRewriteBench cases only. For real use, include the source fields in the CSV.

Other eval platforms can still work, but they need normalization into this CSV shape first.

### Annotated CSV Example

A minimal JudgeBuddy-compatible CSV with one case × two providers:

```csv
Description,resume,jd,[Model A] output,Status,Score,Named Scores,Grader Reason,Comment,[Model B] output,Status,Score,Named Scores,Grader Reason,Comment
"Case 01 - Junior frontend -> Senior frontend","张明远...","职位：高级前端...","【姓名】张明远\n...",PASS,0.95,"{\"语义_诚实度\":1,\"岗位_贴合度\":0.9,\"表达_专业度\":1}","All assertions passed",,"# 张明远\n...",FAIL,0.6,"{\"语义_诚实度\":0,\"岗位_贴合度\":1,\"表达_专业度\":1}","Detected unsupported skills: Webpack, AI 产品",
```

Column anatomy:

- `Description`: short case label; the parser looks for `Case NN` to derive a case id.
- `resume`, `jd`: free text columns used to fill panes 1 and 2.
- `[X] output`: any column whose header starts with `[` is treated as a provider's output. Pane 3 will show one of these per row.
- The 5 columns right after each `[X] output` (`Status` / `Score` / `Named Scores` / `Grader Reason` / `Comment`) are matched **by position**, so do not reorder them.
- `Named Scores` is JSON; the keys must match your `DIMENSIONS` ids in the HTML for the disagreement highlight to work.

> 💡 **Promptfoo users**: `promptfoo export <eval-id> --format csv` produces exactly this shape. You don't need to manually build the CSV.

## Integration Examples

### promptfoo

This is the primary supported path in v0.1:

```bash
promptfoo eval -c promptfooconfig.yaml
promptfoo view
```

Then export CSV from the promptfoo UI and load it in JudgeBuddy.

### Custom eval runner

If your company uses a custom runner, emit a CSV with one row per case and promptfoo-like provider blocks.

Conceptually:

```python
import csv
import json

with open("for_judgebuddy.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Description",
        "resume",
        "jd",
        "[Company Model] output",
        "Status",
        "Score",
        "Named Scores",
        "Grader Reason",
        "Comment",
    ])

    for case in eval_results:
        writer.writerow([
            f"Case {case['case_id']} - {case['title']}",
            case["resume"],
            case["jd"],
            case["output"],
            case["status"],
            case["score"],
            json.dumps(case["named_scores"], ensure_ascii=False),
            case["judge_reason"],
            "",
        ])
```

### Braintrust / Langfuse / Phoenix

These tools are better suited for code-first experiments, tracing, and production observability. JudgeBuddy can still be useful as a human calibration layer, but v0.1 does not read their native exports directly.

Recommended path for now:

```text
Braintrust / Langfuse / Phoenix export
  -> normalize to JudgeBuddy-compatible CSV
  -> label in JudgeBuddy
  -> export YAML/JSON
  -> compare human labels against judge scores
```

Native converters are a roadmap item, not a current feature.

## Customize

JudgeBuddy is intentionally plain HTML/CSS/JS. There is no build step.

### Change scoring dimensions

Edit the `DIMENSIONS` array in the HTML file:

```javascript
const DIMENSIONS = [
  { id: '语义_诚实度', label: '语义_诚实度', desc: '伪经验/能力等级抬升' },
  { id: '岗位_贴合度', label: '岗位_贴合度', desc: '是否真的更对口 JD' },
  { id: '表达_专业度', label: '表达_专业度', desc: '格式 + 措辞是否专业' },
];
```

The `id` should match the key in your judge named scores if you want JudgeBuddy to show disagreement highlights.

### Change the three-pane content

The current UI is resume/JD/rewrite specific. To adapt it to another domain, change the rendering logic that maps CSV fields to panes:

```text
resume -> left pane
jd -> middle pane
provider output -> right pane
```

For example:

| Domain | Left Pane | Middle Pane | Right Pane |
|---|---|---|---|
| Customer support QA | User ticket | Policy / rubric | Agent response |
| RAG evaluation | Question | Retrieved context | Answer |
| Content moderation | Original post | Policy | Model decision |
| Code review eval | Source diff | Review rubric | Model review |

### Change export format

YAML and JSON export are implemented in the HTML file. You can adjust the generated structure to match your own meta-eval repository format.

## Use Case Gallery

These are concrete adaptations of JudgeBuddy to other LLM eval domains. Each one needs only minor edits to the `DIMENSIONS` array and the pane-mapping logic.

### 1. RAG Evaluation

For a RAG system that retrieves context and answers questions:

| Pane | Content |
|---|---|
| Left | User question |
| Middle | Retrieved chunks (top-k) |
| Right | Model answer |

```javascript
const DIMENSIONS = [
  { id: 'faithfulness',  label: 'Faithfulness',  desc: 'Answer is grounded in retrieved chunks' },
  { id: 'completeness',  label: 'Completeness',  desc: 'Answer addresses all aspects of question' },
  { id: 'relevance',     label: 'Chunk quality', desc: 'Retrieved chunks are relevant to question' },
];
```

### 2. Customer Support QA

For agents writing replies to user tickets:

| Pane | Content |
|---|---|
| Left | User ticket / question |
| Middle | Internal policy / KB snippet |
| Right | Agent reply (human or AI) |

```javascript
const DIMENSIONS = [
  { id: 'policy_adherence', label: 'Policy', desc: 'Reply follows internal policy' },
  { id: 'empathy',          label: 'Empathy', desc: 'Tone is appropriate for the situation' },
  { id: 'resolution',       label: 'Resolution', desc: 'Reply actually solves the user problem' },
];
```

### 3. Content Moderation

For LLM-based moderation decisions:

| Pane | Content |
|---|---|
| Left | Original user post |
| Middle | Moderation policy text |
| Right | Model decision + rationale |

```javascript
const DIMENSIONS = [
  { id: 'correct_decision', label: 'Decision', desc: 'Allow/Block is correct' },
  { id: 'cited_rule',       label: 'Rule citation', desc: 'Cites correct policy section' },
  { id: 'no_overblock',     label: 'Not over-block', desc: 'Did not flag benign content' },
];
```

### 4. Code Review Eval

For LLM that reviews PRs:

| Pane | Content |
|---|---|
| Left | Source diff |
| Middle | Style guide / reviewer rubric |
| Right | Model review comments |

```javascript
const DIMENSIONS = [
  { id: 'correctness',  label: 'Correctness', desc: 'Catches real bugs without false positives' },
  { id: 'priority',     label: 'Priority',    desc: 'Marks critical issues as critical' },
  { id: 'actionability', label: 'Actionable',  desc: 'Suggests concrete fixes' },
];
```

> 💡 **Want JudgeBuddy to ship with these as preset "modes"?** That's on the [Roadmap](#roadmap). For now, fork & swap `DIMENSIONS` is the fastest path.

## Privacy Model

JudgeBuddy is local-first:

- The CSV is parsed in the browser.
- Human labels are stored in `localStorage`.
- YAML is copied to the clipboard.
- JSON is downloaded locally.
- The app does not need a backend server.

This makes it useful for sensitive evaluation data such as resumes, customer support transcripts, internal policy checks, or proprietary model outputs.

One caveat: if you host the HTML on a public static site, the app code is public. Your data still remains local unless you add network calls yourself.

## Roadmap

Near-term:

- Add the app file to this standalone repository as `index.html`.
- Add a small sample CSV for first-time users.
- Add README demo images or a short GIF once the UI is packaged.
- Add native import helpers for OpenAI Evals, Braintrust, Langfuse, and Phoenix exports.

Later:

- Configurable panes without editing source code.
- Configurable scoring dimensions from a YAML/JSON settings file.
- Inter-annotator agreement calculation.
- Cohen's kappa or simple agreement summaries.
- Multi-annotator label merge workflow.
- Domain templates for RAG, customer support QA, moderation, and resume rewriting.

## FAQ

### Is this a replacement for promptfoo?

No. promptfoo runs evals and produces model/judge results. JudgeBuddy helps humans inspect those results and create calibration labels.

### Does JudgeBuddy send my data anywhere?

No, not in v0.1. It parses CSV locally and stores labels in browser `localStorage`.

### Can I use it without promptfoo?

Yes, if you normalize your results into the supported CSV shape. Native import for other platforms is planned but not available in v0.1.

### Does it support multiple annotators?

Not directly yet. The current workflow is: each annotator exports YAML or JSON, then you compare or merge those files outside the app.

### What happens if I close the browser?

Labels are saved in `localStorage`. Reopen the same browser and load the same CSV to continue.

### Is it production-ready?

It is useful as a local calibration tool today, especially for small eval rounds. It is not yet a full annotation platform with accounts, permissions, assignment queues, or server-side storage.

## Contributing

JudgeBuddy is single-file HTML/CSS/JS by design. Contribution barrier is intentionally low:

1. Fork the repo.
2. Edit `index.html` directly (or split logic into `app.js` if you prefer—but keep the zero-dependency promise).
3. Test by opening the file in your browser with a sample CSV.
4. Open a PR.

No build step. No npm install. No CI required.

### Especially welcome contributions

- **Domain templates** — preset `DIMENSIONS` for RAG / customer support / moderation / code review (see Use Case Gallery for shapes).
- **Native importers** — parsers for OpenAI Evals JSONL, Braintrust trace JSON, Langfuse exports.
- **UI improvements** — dark mode, configurable pane widths, keyboard navigation between cases.
- **Statistics helpers** — Cohen's kappa, Krippendorff's alpha, inter-annotator agreement charts.
- **i18n** — JudgeBuddy is currently zh-CN flavored; English / Japanese / Korean translations welcome.

### Code style

- Plain ES2020+ vanilla JS.
- No frameworks.
- No bundler.
- CSS in `<style>` block, kept readable (no minification).
- New features should degrade gracefully if the CSV doesn't have the expected fields.

## Acknowledgments

- [promptfoo](https://promptfoo.dev/) for setting a de-facto CSV schema for LLM eval results.
- G-Eval (Liu et al., NeurIPS 2023) and Prometheus (Kim et al.) for the LLM-as-judge methodology foundation.
- The [ResumeRewriteBench](https://github.com/melody-ling-L/resume-rewrite-bench) project for being the original consumer of this tool — that's where the design pressure came from.

## Origin

JudgeBuddy came out of ResumeRewriteBench, a benchmark for testing whether LLMs fabricate facts when rewriting resumes for target job descriptions.

That benchmark needed human labels for judge calibration. Existing tools were either too heavy or not designed around LLM-as-judge disagreement analysis, so this small local tool became the fastest path.

The surprising part: the workflow is not resume-specific. Any team doing LLM eval eventually needs to ask:

> When the judge says PASS or FAIL, does a careful human agree?

JudgeBuddy is for that moment.

## License / Citation

Suggested license for the public repo: MIT.

If you cite or mention the project:

```bibtex
@misc{judgebuddy2026,
  title  = {JudgeBuddy: A Lightweight Companion for LLM-as-Judge Calibration},
  author = {Melody},
  year   = {2026},
  url    = {https://github.com/melody-ling-L/judgebuddy}
}
```

Issues and pull requests: https://github.com/melody-ling-L/judgebuddy/issues
