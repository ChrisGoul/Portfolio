# Portfolio

Personal site — [chrisgoul.github.io/Portfolio](https://chrisgoul.github.io/Portfolio/)

Static site built with Jekyll, which GitHub Pages compiles automatically on push
to `main`. No build step to run locally, no framework, no CDN dependencies.

## Adding a project

Every project is one document in `_projects/`. The home page is just a list of
links to them. Create `_projects/my-project.md`:

```markdown
---
title: My Project
order: 9              # position in the home-page list, low numbers first
lede: >-
  One or two sentences, shown under the title.
description: Used for the meta description and link previews.
meta: ["Tag", "Another tag"]   # the small grey text on the home page
---

Body goes here. Markdown, with raw HTML where you need it.
```

The URL becomes `/projects/my-project/`. Nothing else needs editing.

Useful classes when a project needs more than prose (all in `css/main.css`):

| Class | Use |
|---|---|
| `.tbl` wrapping a `<table>` | Data table that scrolls sideways on mobile instead of breaking the page |
| `.chartbox` wrapping an `<svg>` | Inline chart; use `.c-grid` / `.c-axis` / `.c-tick` / `.c-lab` so it themes correctly |
| `.samples` with `.s` rows | Model output or transcripts |
| `.full` on a figure | Lets a figure break past the text measure |
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
_layouts/          default -> page / project
_projects/         one Markdown file per project
css/main.css       the whole design system
assets/            images, video, resume PDF
index.html         the only page: bio, career, project links
```

Colours, type and spacing are CSS custom properties at the top of `main.css`.
The site is light-only by design — there is no dark theme, so a reader with a
dark OS still gets the white page.

## Note on images

Several files in `assets/` are 3 MB+ straight off a phone camera
(`Limestone_Sample.jpg`, `Marble Jig.jpg`, `Jig_Bottom.jpg`, `20241107_173906.jpg`).
Pages lazy-load them, but resizing to ~1600px wide would cut page weight by
roughly 10× and is the single biggest speed win available here.
