#!/usr/bin/env python3
"""
Local preview — renders the site without needing Ruby or Jekyll installed.

    python preview.py          # build into _site_preview/
    python preview.py --serve  # build, then serve at http://localhost:8000

This implements the small slice of Liquid this site uses — layouts, includes,
if/else, unless, for (with limit and else), assign, and a handful of filters —
with a real nesting-aware parser rather than regexes, plus enough Markdown for
the posts. It exists so you can eyeball a change before pushing.

GitHub Pages runs real Jekyll and is the source of truth. But if a tag leaks
through here or a page looks wrong, that is almost always a genuine template
bug worth fixing before it ships.
"""
from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import sys
import webbrowser
from datetime import datetime

try:
    import yaml
except ImportError:
    sys.exit("needs PyYAML:  pip install pyyaml")

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "_site_preview")
COPY_DIRS = ["assets", "css", "js"]
PAGES = ["index.html", "projects.html", "writing.html"]


# --- front matter -----------------------------------------------------------

def split_front_matter(text: str):
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not m:
        return {}, text
    try:
        return (yaml.safe_load(m.group(1)) or {}), text[m.end():]
    except yaml.YAMLError as e:
        raise SystemExit(f"bad front matter: {e}")


# --- Markdown (the subset the posts use) ------------------------------------

INLINE = [
    (re.compile(r"`([^`]+)`"), lambda m: f"<code>{html.escape(m.group(1))}</code>"),
    # non-greedy so bold survives emphasis nested inside it: **a *b* c**
    (re.compile(r"\*\*(.+?)\*\*", re.S), r"<strong>\1</strong>"),
    (re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)"), r"<em>\1</em>"),
    (re.compile(r"\[([^\]]+)\]\(([^)]+)\)"), r'<a href="\2">\1</a>'),
]


def inline(s: str) -> str:
    for pat, rep in INLINE:
        s = pat.sub(rep, s)
    return s


def markdown(text: str) -> str:
    out, buf, i = [], [], 0
    lines = text.split("\n")

    def flush():
        if buf:
            joined = " ".join(l.strip() for l in buf).strip()
            if joined:
                out.append(f"<p>{inline(joined)}</p>")
            buf.clear()

    while i < len(lines):
        line = lines[i]
        s = line.strip()

        if s.startswith("<") and not s.startswith("<!--"):
            flush()
            tag = re.match(r"<(\w+)", s)
            if tag:
                name, depth = tag.group(1), 0
                while i < len(lines):
                    l = lines[i]
                    depth += len(re.findall(rf"<{name}\b", l))
                    depth -= len(re.findall(rf"</{name}>", l))
                    out.append(l)
                    i += 1
                    if depth <= 0:
                        break
                continue
            out.append(line); i += 1; continue

        if not s:
            flush(); i += 1; continue
        if set(s) == {"-"} and len(s) >= 3:
            flush(); out.append("<hr>"); i += 1; continue

        h = re.match(r"^(#{1,4})\s+(.*)$", s)
        if h:
            flush(); lvl = len(h.group(1))
            out.append(f"<h{lvl}>{inline(h.group(2))}</h{lvl}>"); i += 1; continue

        if s.startswith(">"):
            flush(); q = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q.append(lines[i].strip().lstrip(">").strip()); i += 1
            out.append(f"<blockquote><p>{inline(' '.join(q))}</p></blockquote>"); continue

        if re.match(r"^[-*]\s+", s):
            flush(); items = []
            while i < len(lines):
                t = lines[i].strip()
                if re.match(r"^[-*]\s+", t):
                    items.append(re.sub(r"^[-*]\s+", "", t))
                elif t and lines[i].startswith("  ") and items:
                    items[-1] += " " + t
                else:
                    break
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
            continue

        buf.append(line); i += 1

    flush()
    return "\n".join(out)


# --- Liquid: tokenize -> parse -> render ------------------------------------

TOKEN = re.compile(r"(\{\{-?.*?-?\}\}|\{%-?.*?-?%\})", re.S)
TAG = re.compile(r"^\{%-?\s*(\w+)\s*(.*?)\s*-?%\}$", re.S)
OUTPUT = re.compile(r"^\{\{-?\s*(.*?)\s*-?\}\}$", re.S)

BLOCK_OPEN = {"if", "unless", "for", "comment", "raw"}
BLOCK_CLOSE = {"endif", "endunless", "endfor", "endcomment", "endraw"}


class Node:
    __slots__ = ("kind", "value", "children", "alt")

    def __init__(self, kind, value=None):
        self.kind = kind        # text | output | tag | if | unless | for
        self.value = value
        self.children = []
        self.alt = []           # else branch


def parse(src: str):
    parts = TOKEN.split(src)
    pos = 0

    def walk(stop_on=None):
        nonlocal pos
        nodes = []
        cur = nodes
        node_for_else = None
        while pos < len(parts):
            chunk = parts[pos]; pos += 1
            if not chunk:
                continue
            m = TAG.match(chunk)
            if m:
                name, rest = m.group(1), m.group(2)
                if stop_on and name in stop_on:
                    return nodes, name, node_for_else
                if name == "else":
                    node_for_else = True
                    cur = []
                    nodes = (nodes, cur) if not isinstance(nodes, tuple) else nodes
                    continue
                if name in ("if", "unless"):
                    n = Node(name, rest)
                    body, _, had_else = walk({"endif", "endunless"})
                    _assign_branches(n, body)
                    cur.append(n); continue
                if name == "for":
                    n = Node("for", rest)
                    body, _, had_else = walk({"endfor"})
                    _assign_branches(n, body)
                    cur.append(n); continue
                if name in BLOCK_CLOSE:
                    return nodes, name, node_for_else
                cur.append(Node("tag", (name, rest))); continue
            o = OUTPUT.match(chunk)
            if o:
                cur.append(Node("output", o.group(1))); continue
            cur.append(Node("text", chunk))
        return nodes, None, node_for_else

    def _assign_branches(node, body):
        if isinstance(body, tuple):
            node.children, node.alt = body[0], body[1]
        else:
            node.children, node.alt = body, []

    tree, _, _ = walk()
    return tree[0] if isinstance(tree, tuple) else tree


# --- evaluation -------------------------------------------------------------

class Ctx(dict):
    def path(self, p):
        cur = self
        for part in p.split("."):
            # Liquid exposes .size / .first / .last on arrays and strings
            if part in ("size", "first", "last") and isinstance(cur, (list, tuple, str)):
                if part == "size":
                    cur = len(cur)
                else:
                    cur = cur[0] if (cur and part == "first") else (cur[-1] if cur else None)
            elif isinstance(cur, dict):
                cur = cur.get(part)
            else:
                cur = getattr(cur, part, None)
            if cur is None:
                return None
        return cur


def resolve(tok, ctx):
    tok = tok.strip()
    if (tok[:1], tok[-1:]) in (("'", "'"), ('"', '"')):
        return tok[1:-1]
    if re.fullmatch(r"-?\d+", tok):
        return int(tok)
    return ctx.path(tok)


def apply_filters(val, filters, site):
    for f in filters:
        f = f.strip()
        name, _, arg = f.partition(":")
        name, arg = name.strip(), arg.strip().strip("'\"")
        if name == "default":
            if not val:
                val = arg
        elif name == "relative_url":
            v = str(val or "")
            val = site.get("baseurl", "") + v if v.startswith("/") else v
        elif name == "absolute_url":
            v = str(val or "")
            val = site.get("url", "") + site.get("baseurl", "") + v
        elif name == "date":
            fmt = arg
            if isinstance(val, str):
                try:
                    val = datetime.fromisoformat(val)
                except ValueError:
                    pass
            if hasattr(val, "strftime"):
                dash = "%-d" in fmt or "%-m" in fmt
                out = fmt.replace("%-d", "%d").replace("%-m", "%m")
                out = val.strftime(out)
                if dash:
                    out = re.sub(r"\b0(\d)", r"\1", out)
                val = out
        elif name == "truncate":
            s = str(val or ""); n = int(arg or 80)
            val = s if len(s) <= n else s[:n].rstrip() + "…"
        elif name == "strip_html":
            val = re.sub(r"<[^>]+>", "", str(val or ""))
        elif name == "strip_newlines":
            val = " ".join(str(val or "").split())
    return val


def truthy(expr, ctx):
    """Boolean operators bind loosest, so they have to be split off before the
    comparisons — otherwise `a and b != c` splits on != and evaluates nonsense."""
    expr = expr.strip()
    if expr.startswith("not "):
        return not truthy(expr[4:], ctx)
    for op in (" or ", " and "):
        if op in expr:
            l, r = expr.split(op, 1)
            return (truthy(l, ctx) or truthy(r, ctx)) if op == " or " \
                else (truthy(l, ctx) and truthy(r, ctx))
    for op in (" contains ", " == ", " != ", " >= ", " <= ", " > ", " < "):
        if op in expr:
            l, r = expr.split(op, 1)
            a, b = resolve(l, ctx), resolve(r, ctx)
            if op == " contains ":
                return str(b) in str(a or "")
            if op == " == ":
                return str(a) == str(b)
            if op == " != ":
                return str(a) != str(b)
            try:
                a, b = float(a or 0), float(b or 0)
            except (TypeError, ValueError):
                return False
            return {" >= ": a >= b, " <= ": a <= b, " > ": a > b, " < ": a < b}[op]
    return bool(resolve(expr, ctx))


def render_nodes(nodes, ctx) -> str:
    out = []
    for n in nodes:
        if n.kind == "text":
            out.append(n.value)
        elif n.kind == "output":
            parts = n.value.split("|")
            v = resolve(parts[0], ctx)
            v = apply_filters(v, parts[1:], ctx.get("site", {}))
            out.append("" if v is None else str(v))
        elif n.kind in ("if", "unless"):
            ok = truthy(n.value, ctx)
            if n.kind == "unless":
                ok = not ok
            out.append(render_nodes(n.children if ok else n.alt, ctx))
        elif n.kind == "for":
            m = re.match(r"(\w+)\s+in\s+([\w.]+)(?:\s+limit:\s*(\d+))?", n.value)
            if not m:
                continue
            var, coll, limit = m.groups()
            items = ctx.path(coll) or []
            if limit:
                items = items[: int(limit)]
            if not items:
                out.append(render_nodes(n.alt, ctx))
            else:
                for it in items:
                    sub = Ctx(ctx); sub[var] = it
                    out.append(render_nodes(n.children, sub))
        elif n.kind == "tag":
            name, rest = n.value
            if name == "include":
                fn = rest.split()[0] if rest else ""
                p = os.path.join(ROOT, "_includes", fn)
                if os.path.exists(p):
                    out.append(render(open(p, encoding="utf-8").read(), ctx))
            elif name == "assign":
                var, _, expr = rest.partition("=")
                parts = expr.split("|")
                v = resolve(parts[0], ctx)
                ctx[var.strip()] = apply_filters(v, parts[1:], ctx.get("site", {}))
            # feed_meta and anything else we don't implement: emit nothing
    return "".join(out)


def render(src: str, ctx: Ctx) -> str:
    return render_nodes(parse(src), ctx)


def apply_layout(name, content, page, site):
    seen = set()
    while name and name not in seen:
        seen.add(name)
        p = os.path.join(ROOT, "_layouts", f"{name}.html")
        if not os.path.exists(p):
            break
        fm, body = split_front_matter(open(p, encoding="utf-8").read())
        content = render(body, Ctx(site=site, page=page, content=content))
        name = fm.get("layout")
    return content


# --- build ------------------------------------------------------------------

def build(strict=True):
    site = yaml.safe_load(open(os.path.join(ROOT, "_config.yml"), encoding="utf-8"))
    site["time"] = datetime.now()

    posts = []
    pdir = os.path.join(ROOT, "_posts")
    if os.path.isdir(pdir):
        for fn in sorted(os.listdir(pdir)):
            if not fn.endswith((".md", ".markdown")):
                continue
            fm, body = split_front_matter(open(os.path.join(pdir, fn), encoding="utf-8").read())
            slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", fn).rsplit(".", 1)[0]
            fm.update(url=f"/writing/{slug}/", slug=slug, _body=body,
                      layout=fm.get("layout", "post"))
            d = fm.get("date")
            if isinstance(d, str):
                fm["date"] = datetime.fromisoformat(d)
            elif d is not None and not isinstance(d, datetime):
                fm["date"] = datetime(d.year, d.month, d.day)
            fm.setdefault("date", datetime.now())
            posts.append(fm)
    posts.sort(key=lambda p: p["date"], reverse=True)
    site["posts"] = posts

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    # The live site sits at /Portfolio/, so every URL carries that prefix. Mirror
    # it on disk and serve the parent, otherwise the preview loads with no CSS
    # and every internal link 404s — which is exactly the class of bug the
    # preview is supposed to catch.
    root_out = os.path.join(OUT, site.get("baseurl", "").strip("/")) if site.get("baseurl") else OUT
    os.makedirs(root_out, exist_ok=True)
    for d in COPY_DIRS:
        s = os.path.join(ROOT, d)
        if os.path.isdir(s):
            shutil.copytree(s, os.path.join(root_out, d))

    written = []
    for fn in PAGES:
        src = os.path.join(ROOT, fn)
        if not os.path.exists(src):
            continue
        fm, body = split_front_matter(open(src, encoding="utf-8").read())
        fm["url"] = "/" if fn == "index.html" else f"/{fn}"
        page = render(body, Ctx(site=site, page=fm))
        out = apply_layout(fm.get("layout", "default"), page, fm, site)
        path = os.path.join(root_out, fn)
        open(path, "w", encoding="utf-8").write(out)
        written.append(path)

    for post in posts:
        content = render(markdown(post["_body"]), Ctx(site=site, page=post))
        out = apply_layout(post.get("layout", "post"), content, post, site)
        d = os.path.join(root_out, "writing", post["slug"])
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, "index.html")
        open(path, "w", encoding="utf-8").write(out)
        written.append(path)

    leaked = []
    for p in written:
        txt = open(p, encoding="utf-8").read()
        n = len(re.findall(r"\{%|\{\{", txt))
        if n:
            leaked.append((os.path.relpath(p, OUT), n))

    print(f"built {len(written)} pages -> {OUT}")
    if leaked:
        print("\n!! unrendered Liquid left in output:")
        for f, n in leaked:
            print(f"   {f}: {n} tag(s)")
        if strict:
            sys.exit(1)
    else:
        print("no unrendered template tags")
    return site


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--serve", action="store_true")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--no-strict", action="store_true")
    args = ap.parse_args()
    site = build(strict=not args.no_strict)
    base = (site.get("baseurl") or "").rstrip("/")
    if args.serve:
        import http.server, socketserver, functools
        h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=OUT)
        with socketserver.TCPServer(("", args.port), h) as httpd:
            url = f"http://localhost:{args.port}{base}/index.html"
            print(f"serving {url}  (ctrl-c to stop)")
            webbrowser.open(url)
            httpd.serve_forever()
    else:
        print("open:", os.path.join(OUT, base.strip("/"), "index.html"))


if __name__ == "__main__":
    main()
