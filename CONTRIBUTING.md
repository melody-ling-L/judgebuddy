# Contributing to JudgeBuddy

Thanks for considering a contribution! JudgeBuddy is designed to keep the
contribution barrier low.

## Project Principles

These shape every PR decision:

1. **Zero dependencies.** Open `index.html`, it works. No npm install. No CDN
   call required at runtime (CDN allowed only for optional libraries like
   PapaParse — and only if they degrade gracefully).
2. **Single file by default.** Until the app exceeds ~2000 lines, keep all
   HTML/CSS/JS in `index.html`. After that, splitting is fine but no bundler.
3. **Local-first.** No network calls unless explicitly opt-in by the user.
4. **One purpose.** JudgeBuddy is a calibration UI, not an eval runner, not a
   tracing platform, not a project management system.

## What we welcome

| Contribution type | Effort | Difficulty |
|---|---|---|
| Bug reports with reproduction CSV | low | easy |
| Domain template (preset DIMENSIONS) | low | easy |
| Native importer (OpenAI Evals / Braintrust / etc) | medium | medium |
| UI improvement (dark mode, keyboard nav) | medium | medium |
| Statistics helper (Cohen's kappa, IAA) | medium | medium |
| i18n translation | low | easy |
| New eval domain examples in README | low | easy |

## What we won't merge

- New runtime dependencies that aren't degradable
- Account systems / multi-tenancy infrastructure (use Label Studio if you need this)
- Anything that requires running a server
- Features that store labels somewhere other than the user's browser by default

## How to contribute

```bash
# 1. Fork & clone
git clone https://github.com/your-fork/judgebuddy
cd judgebuddy

# 2. Open the app
open index.html

# 3. Test with the included demo CSV
# (Load demo/sample_eval.csv from the in-app file picker)

# 4. Make changes
# Edit index.html directly. Comment your changes liberally.

# 5. Test again with multiple CSV shapes if your change affects parsing

# 6. Open PR
# Describe: what changed + which user scenario it improves
```

## Code style

- Use ES2020+ vanilla JS.
- Indentation: 2 spaces (HTML/CSS/JS).
- Variable naming: camelCase for JS, kebab-case for CSS classes.
- Comment **why**, not **what**.
- Keep functions under 50 lines when possible.

## Reporting bugs

Please include:

1. Browser + version (Chrome 120, Safari 17, etc.)
2. A minimal CSV that reproduces the issue (paste 1-2 rows)
3. Expected vs actual behavior
4. Console errors if any (F12 → Console)

## Suggesting features

Open a GitHub Issue with the label `enhancement`. Describe:

- The eval workflow you're trying to support
- How the current JudgeBuddy doesn't fit
- Sketch of the change

We prefer issues over speculative PRs for non-trivial features.

## License

By contributing, you agree that your contributions will be licensed under the
MIT License (see `LICENSE`).
