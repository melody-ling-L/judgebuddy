# Screenshots

This folder holds README assets.

Current checked-in assets:

- `three-pane-view.png` for the static three-pane preview
- `linked-highlight.gif` for the inline README demo

To regenerate the demo assets locally, open `capture_demo.html` through a local static server and recapture the frames/GIF.

## Required for the GitHub README

| File | What it shows | Recording tip |
|---|---|---|
| `three-pane-view.png` | The default loaded state with 3 panes side-by-side | Capture a 1600×900 region with at least 2 cases visible |
| `linked-highlight.gif` | Click a block → other panes highlight | Use Kap / LICEcap / ScreenStudio, 10-15 seconds, < 5 MB |
| `judge-vs-human.png` | The dimensions panel showing judge score next to PASS/FAIL controls | Crop the dimensions row of one card |
| `disagreement-orange.png` | Card with an orange-bordered "disagree" dimension | Click FAIL when judge says PASS to trigger it |

## Recording tips for the GIF

1. Use a fresh browser window — no extensions or noisy tabs visible.
2. Move your cursor slowly, deliberate clicks (the GIF is for explanation, not benchmarking your reflexes).
3. Demonstrate ONE clear flow per GIF — don't try to show everything at once.
4. Compress with `gifsicle -O3` or use a tool like Kap that auto-optimizes.

## Optional

- `hero-banner.png` — wider banner for the very top of the README (1280×400)
- `dark-mode.png` — once dark mode lands
- `multi-language.png` — once i18n lands

## File size guidance

- PNG screenshots: keep under 500 KB each
- GIFs: under 5 MB to avoid GitHub auto-disabling autoplay
