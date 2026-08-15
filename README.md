# Portfolio

Personal site — [chrisgoul.github.io/Portfolio](https://chrisgoul.github.io/Portfolio/)

Static site built with Jekyll, which GitHub Pages compiles automatically on push
to `main`. No build step to run locally, no framework, no CDN dependencies.

## Writing a new post

Drop a Markdown file in `_posts/` named `YYYY-MM-DD-slug.md`:

```markdown
---
title: "The title"
eyebrow: Machine learning
lede: >-
  One or two sentences. Shows under the title, and as the summary on the
  writing index and home page.
description: Used for the meta description and link previews.
date: 2026-08-15
tags: [llm, evaluation]
reading_time: 8 min read
---

Body goes here. Markdown, with raw HTML where you need it.
```

That's the whole workflow — the writing index, the home page list and the RSS
feed all pick it up automatically. The URL becomes `/writing/slug/`.

Useful classes when a post needs more than prose (all defined in `css/main.css`):

| Class | Use |
|---|---|
| `.tbl` wrapping a `<table>` | Data table that scrolls sideways on mobile instead of breaking the page |
| `.chartbox` wrapping an `<svg>` | Inline chart. Use the `.c-grid` / `.c-axis` / `.c-tick` / `.c-lab` classes so it themes correctly |
| `.samples` with `.s` rows | Model output or chat transcripts |
| `.full` on a figure | Lets a figure break out past the text measure |
| `.n` / `.good` / `.bad` / `.dim` on a `<td>` | Numeric and emphasis styling in tables |

## Previewing locally

GitHub Pages needs Ruby, which isn't installed here, so `preview.py` renders the
site with a small Liquid + Markdown implementation instead:

```bash
python preview.py --serve
```

It builds into `_site_preview/` (gitignored), mirrors the real `/Portfolio/`
URL prefix so links and CSS resolve exactly as they do live, and **exits
non-zero if any template tag failed to render** — which catches most Liquid
mistakes before they ship.

It is an approximation, not Jekyll. GitHub Pages is the source of truth; if the
two disagree on something subtle, believe Pages. But a page that breaks in the
preview is almost always genuinely broken.

## Layout

```
_config.yml        site settings, nav, author links
_includes/         head, nav, footer
_layouts/          default -> page / post
_posts/            blog posts (Markdown)
css/main.css       the whole design system
assets/            images, video, resume PDF
*.html             index (home), projects, writing
```

Colours, type and spacing are CSS custom properties at the top of `main.css`.
The site is light-only by design — there is no dark theme, so a reader with a
dark OS still gets the white page.

## Note on images

Several files in `assets/` are 3 MB+ straight off a phone camera
(`Limestone_Sample.jpg`, `Marble Jig.jpg`, `Jig_Bottom.jpg`, `20241107_173906.jpg`).
Pages lazy-load them, but resizing to ~1600px wide would cut page weight by
roughly 10× and is the single biggest speed win available here.
