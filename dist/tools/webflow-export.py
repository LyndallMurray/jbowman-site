#!/usr/bin/env python3
"""
J BOWMAN -> Webflow exporter
============================

Turns the built static site into things you can get INTO Webflow:

  webflow/paste/<page>.json     Webflow Designer clipboard payloads.
                                Copy the file's contents, click the Webflow
                                canvas, press Cmd/Ctrl-V. Real Webflow
                                elements appear, carrying the site's class
                                names and the brand type/colour styles.

  webflow/custom-code-head.html Everything Webflow's style panel cannot
                                express: component internals, hover and
                                focus states, ground-dependent overrides,
                                the marquee animation, reduced-motion and
                                print rules. Paste into
                                Project Settings -> Custom Code -> Head.

  webflow/custom-code-footer.html  The click-to-load YouTube player.
                                Paste into Footer.

  webflow/README.md             Order of operations.

WHY A HYBRID
------------
Webflow's clipboard format carries a style as `styleLess`, which is raw CSS,
so a single-class rule converts exactly. Anything with a descendant
combinator, a pseudo-class or a pseudo-element has no home in the style
panel. Of this site's 275 rules, 112 are single-class and become editable
Webflow styles; the other 163 go into one stylesheet in custom code.

That split is deliberate: the layer a person will actually want to tweak
later -- type scale, colours, band padding -- lands in the panel, and the
fiddly component internals stay as CSS that cannot drift.

HONEST LIMITS
-------------
* The clipboard format is not a documented, versioned API. It is stable in
  practice and widely used, but Webflow could change it. If a paste does
  nothing, that is what happened, and nothing is broken -- fall back to the
  build sheet.
* Four element kinds are deliberately NOT exported, because a pasted
  imitation would be worse than the native thing:
      - the primary nav  -> use Webflow's Navbar component
      - the contact form -> use Webflow's Form Block
      - the showreel     -> use Webflow's Video element
      - the releases list-> use a CMS Collection List
  Each leaves a placeholder Block with its class name, so the slot is
  visible and correctly positioned.
* Images are exported with their relative `src`. Webflow has no asset for
  them yet, so they render as placeholders until you upload the files and
  re-point each one. That is one click per image.

Usage:  python3 tools/webflow-export.py        (run from dist/)
"""

import json
import os
import re
import sys
import uuid
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.dirname(HERE)
OUT = os.path.join(DIST, "webflow")

PAGES = [
    ("index.html", "home", "Home"),
    ("about.html", "about", "About"),
    ("work.html", "work", "Work"),
    ("services.html", "services", "Services"),
    ("journal.html", "journal", "Journal"),
    ("connect.html", "connect", "Connect"),
]

# ---------------------------------------------------------------------------
# 1. Tokens
# ---------------------------------------------------------------------------

def strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def read_tokens(path):
    """Pull the :root custom properties out of tokens.css."""
    css = strip_comments(open(path).read())
    m = re.search(r":root\s*\{(.*?)\n\}", css, flags=re.S)
    if not m:
        sys.exit("tokens.css: no :root block found")
    tokens = {}
    for decl in m.group(1).split(";"):
        decl = decl.strip()
        if not decl.startswith("--"):
            continue
        name, _, value = decl.partition(":")
        tokens[name.strip()] = value.strip()
    return tokens


VAR_RE = re.compile(r"var\(\s*(--[A-Za-z0-9-]+)\s*(?:,\s*([^()]*(?:\([^()]*\)[^()]*)*))?\)")


def resolve_vars(value, tokens, depth=0):
    """Replace var(--x) with its literal value, recursively.

    Webflow's styleLess is raw CSS but the pasted elements live in a project
    with no custom properties defined, so every var() has to be flattened or
    the declaration silently does nothing.
    """
    if depth > 12:
        return value

    def sub(m):
        name, fallback = m.group(1), m.group(2)
        if name in tokens:
            return resolve_vars(tokens[name], tokens, depth + 1)
        if fallback is not None:
            return resolve_vars(fallback.strip(), tokens, depth + 1)
        return ""

    out = VAR_RE.sub(sub, value)
    return resolve_vars(out, tokens, depth + 1) if VAR_RE.search(out) else out


# ---------------------------------------------------------------------------
# 2. CSS extraction
# ---------------------------------------------------------------------------

def split_at_rules(css):
    """Return (top_level_css, [(at_rule_prelude, inner_css), ...])."""
    at_blocks, out, i = [], [], 0
    while i < len(css):
        if css.startswith("@media", i) or css.startswith("@supports", i):
            try:
                brace = css.index("{", i)
            except ValueError:
                break
            depth, k = 1, brace + 1
            while depth and k < len(css):
                if css[k] == "{":
                    depth += 1
                elif css[k] == "}":
                    depth -= 1
                k += 1
            at_blocks.append((css[i:brace].strip(), css[brace + 1:k - 1]))
            i = k
            continue
        out.append(css[i])
        i += 1
    return "".join(out), at_blocks


RULE_RE = re.compile(r"([^{}]+)\{([^{}]*)\}")
SINGLE_CLASS_RE = re.compile(r"^\.([A-Za-z0-9_-]+)$")


def extract_rules(css):
    """[(selector, declarations)] for one level of CSS, at-rules removed."""
    rules = []
    for m in RULE_RE.finditer(css):
        sel, decls = m.group(1).strip(), m.group(2).strip()
        if not sel or sel.startswith("@") or not decls:
            continue
        rules.append((sel, decls))
    return rules


def classify(rules, tokens):
    """Split rules into {class: declarations} and a list of leftover CSS."""
    simple, leftover = {}, []
    for sel, decls in rules:
        parts = [p.strip() for p in sel.split(",") if p.strip()]
        singles = [SINGLE_CLASS_RE.match(p) for p in parts]
        if len(parts) == 1 and singles[0]:
            cls = singles[0].group(1)
            simple.setdefault(cls, []).append(resolve_vars(decls, tokens))
        else:
            leftover.append((sel, resolve_vars(decls, tokens)))
    return simple, leftover


# 60rem = 960px. Webflow's `medium` breakpoint is max-width 991px, so a rule
# written for 960 and below is applied slightly early, over 961-991px. That
# 31px window is the one place this conversion is not exact, and it only
# affects the handful of rules inside that media query.
MEDIA_TO_VARIANT = {"(max-width: 60rem)": "medium"}


def html_classes():
    """Every class used in the markup.

    A class with no single-class rule still has to exist as a Webflow style,
    or the node loses the class name and the custom CSS -- which targets it
    through a descendant selector -- can never match. Those become styles
    with an empty styleLess: a name in the project, styled from custom code.
    """
    found = set()
    for filename, _, _ in PAGES:
        html = re.sub(r"<!--.*?-->", "",
                      open(os.path.join(DIST, filename)).read(), flags=re.S)
        for m in re.finditer(r'class="([^"]+)"', html):
            found.update(m.group(1).split())
    return found - DROP_CLASSES


def build_styles(tokens, extra_classes=frozenset()):
    """Return (webflow_styles, custom_css_text)."""
    base = strip_comments(open(os.path.join(DIST, "assets/css/base.css")).read())
    site = strip_comments(open(os.path.join(DIST, "assets/css/site.css")).read())

    all_simple, all_leftover, variant_simple, raw_media = {}, [], {}, []

    for css in (base, site):
        top, at_blocks = split_at_rules(css)
        simple, leftover = classify(extract_rules(top), tokens)
        for cls, decls in simple.items():
            all_simple.setdefault(cls, []).extend(decls)
        all_leftover.extend(leftover)

        for prelude, inner in at_blocks:
            query = prelude[len("@media"):].strip() if prelude.startswith("@media") else prelude
            variant = MEDIA_TO_VARIANT.get(query)
            m_simple, m_leftover = classify(extract_rules(inner), tokens)
            if variant:
                for cls, decls in m_simple.items():
                    variant_simple.setdefault(cls, {}).setdefault(variant, []).extend(decls)
                if m_leftover:
                    raw_media.append((prelude, m_leftover))
            else:
                # prefers-reduced-motion, print: no Webflow variant exists.
                raw_media.append((prelude, list(m_simple.items()) and
                                  [(f".{c}", " ".join(d)) for c, d in m_simple.items()] or []))
                raw_media[-1] = (prelude, raw_media[-1][1] + m_leftover)

    styles, style_ids = [], {}
    for cls in sorted(all_simple):
        sid = str(uuid.uuid4())
        style_ids[cls] = sid
        style = {
            "_id": sid,
            "fake": False,
            "type": "class",
            "name": cls,
            "namespace": "",
            "comb": "",
            "styleLess": normalise(" ".join(all_simple[cls])),
            "variants": {},
            "children": [],
            "createdBy": "jbowman-export",
            "origin": None,
            "selector": None,
        }
        for variant, decls in variant_simple.get(cls, {}).items():
            style["variants"][variant] = {"styleLess": normalise(" ".join(decls))}
        styles.append(style)

    # Classes that only ever appear inside a media query still need an id.
    for cls in sorted(variant_simple):
        if cls in style_ids:
            continue
        sid = str(uuid.uuid4())
        style_ids[cls] = sid
        styles.append({
            "_id": sid, "fake": False, "type": "class", "name": cls,
            "namespace": "", "comb": "", "styleLess": "",
            "variants": {v: {"styleLess": normalise(" ".join(d))}
                         for v, d in variant_simple[cls].items()},
            "children": [], "createdBy": "jbowman-export",
            "origin": None, "selector": None,
        })

    # Classes used in the markup but styled only through descendant rules.
    for cls in sorted(extra_classes):
        if cls in style_ids:
            continue
        sid = str(uuid.uuid4())
        style_ids[cls] = sid
        styles.append({
            "_id": sid, "fake": False, "type": "class", "name": cls,
            "namespace": "", "comb": "", "styleLess": "", "variants": {},
            "children": [], "createdBy": "jbowman-export",
            "origin": None, "selector": None,
        })

    custom = render_custom_css(all_leftover, raw_media)
    return styles, style_ids, custom


def normalise(decls):
    """Tidy a declaration run into one line, ending with a semicolon."""
    parts = [p.strip() for p in decls.split(";") if p.strip()]
    return "; ".join(parts) + ";" if parts else ""


def render_custom_css(leftover, raw_media):
    lines = []
    for sel, decls in leftover:
        lines.append(f"{sel} {{ {normalise(decls)} }}")
    for prelude, rules in raw_media:
        if not rules:
            continue
        lines.append(f"{prelude} {{")
        for sel, decls in rules:
            lines.append(f"  {sel} {{ {normalise(decls)} }}")
        lines.append("}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 3. HTML -> Webflow nodes
# ---------------------------------------------------------------------------

VOID = {"img", "input", "source", "link", "meta", "br", "hr"}

# Subtrees replaced by a native Webflow element, because a pasted imitation
# would be worse than the real thing: the navbar needs Webflow's menu
# interaction, the form needs to actually submit, the video needs Webflow's
# player. The placeholder keeps the slot visible and correctly positioned.
PLACEHOLDER = {
    "form": "Use Webflow's Form Block here",
    "video": "Use Webflow's Video element here (poster: reel-poster.jpg)",
}


def placeholder_for(tag, classes):
    """The primary nav is replaced by Webflow's Navbar. The footer's <nav>
    is only a row of links, so it is exported as ordinary elements."""
    if tag == "nav" and "nav" in classes:
        return "Use Webflow's Navbar component here"
    return PLACEHOLDER.get(tag)

# Dropped outright: no visual role, or a JS hook Webflow replaces.
DROP_TAGS = {"script", "style", "link", "meta", "title", "head", "source", "noscript"}
DROP_CLASSES = {"reveal", "hp"}

# Unwrapped: the element itself has no visual role, but its children do, so
# they attach to its parent. <picture> exists only to offer a WebP <source>,
# which Webflow replaces with its own responsive images.
TRANSPARENT = {"picture"}

HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
BLOCKISH = {"div", "header", "footer", "main", "article", "aside", "figure",
            "figcaption", "span", "em", "strong", "i", "b", "picture", "label"}


class Converter(HTMLParser):
    def __init__(self, style_ids):
        super().__init__(convert_charrefs=True)
        self.style_ids = style_ids
        self.nodes = []
        self.roots = []
        # One frame per open non-void tag, so start and end tags always
        # balance however the tag is treated.
        self.stack = []          # [{"tag", "node", "mode"}]
        self.in_body = False
        self.used_classes = set()
        self.notes = []

    # -- helpers ----------------------------------------------------------
    @property
    def skipping(self):
        return any(f["mode"] == "skip" for f in self.stack)

    def parent(self):
        """Nearest open frame that owns a node; transparent frames are
        stepped over so their children attach to the grandparent."""
        for frame in reversed(self.stack):
            if frame["node"] is not None:
                return frame["node"]
        return None

    def new(self, node):
        self.nodes.append(node)
        parent = self.parent()
        if parent is not None:
            parent["children"].append(node["_id"])
        else:
            self.roots.append(node["_id"])
        return node

    def classes_for(self, attrs):
        raw = (attrs.get("class") or "").split()
        keep = [c for c in raw if c not in DROP_CLASSES]
        ids = []
        for c in keep:
            if c in self.style_ids:
                ids.append(self.style_ids[c])
                self.used_classes.add(c)
            else:
                self.notes.append(f"class '{c}' has no single-class rule; "
                                  "it is styled from custom code only")
        return ids

    # -- parser hooks -----------------------------------------------------
    def push(self, tag, node, mode):
        if tag not in VOID:
            self.stack.append({"tag": tag, "node": node, "mode": mode})

    def handle_starttag(self, tag, attrlist):
        attrs = dict(attrlist)

        if not self.in_body:
            if tag == "body":
                self.in_body = True
            return

        # Inside a skipped subtree: keep the frame so end tags balance.
        if self.skipping:
            self.push(tag, None, "skip")
            return

        if tag in DROP_TAGS:
            self.push(tag, None, "skip")
            return

        if tag in TRANSPARENT:
            self.push(tag, None, "transparent")
            return

        note = placeholder_for(tag, (attrs.get("class") or "").split())
        if note:
            self.new({
                "_id": str(uuid.uuid4()), "type": "Block", "tag": "div",
                "classes": self.classes_for(attrs), "children": [],
                "data": {"tag": "div", "xattr": [
                    {"name": "data-placeholder", "value": note}]},
            })
            self.notes.append(f"<{tag}> -> placeholder: {note}")
            self.push(tag, None, "skip")
            return

        if tag == "nav":
            tag_node = self.make_node("div", attrs)
            self.push(tag, tag_node, "normal")
            return

        node = self.make_node(tag, attrs)
        self.push(tag, node, "normal")

    def make_node(self, tag, attrs):
        cls = self.classes_for(attrs)
        nid = str(uuid.uuid4())

        if tag in HEADINGS:
            return self.new({"_id": nid, "type": "Heading", "tag": tag,
                             "classes": cls, "children": [],
                             "data": {"tag": tag}})
        if tag == "p":
            return self.new({"_id": nid, "type": "Paragraph", "tag": "p",
                             "classes": cls, "children": []})
        if tag == "ul" or tag == "ol":
            return self.new({"_id": nid, "type": "List", "tag": tag,
                             "classes": cls, "children": [],
                             "data": {"tag": tag}})
        if tag == "li":
            return self.new({"_id": nid, "type": "ListItem", "tag": "li",
                             "classes": cls, "children": [],
                             "data": {"tag": "li"}})
        if tag == "a":
            href = attrs.get("href", "#")
            link = ({"mode": "external", "url": href}
                    if href.startswith(("http", "mailto:", "tel:", "#"))
                    else {"mode": "external", "url": "/" + page_slug(href)})
            return self.new({"_id": nid, "type": "Link", "tag": "a",
                             "classes": cls, "children": [],
                             "data": {"link": link, "block": ""}})
        if tag == "img":
            return self.new({"_id": nid, "type": "Image", "tag": "img",
                             "classes": cls, "children": [],
                             "data": {"attr": {
                                 "src": attrs.get("src", ""),
                                 "alt": attrs.get("alt", ""),
                                 "loading": attrs.get("loading", "lazy")}}})
        if tag == "section":
            return self.new({"_id": nid, "type": "Section", "tag": "section",
                             "classes": cls, "children": [],
                             "data": {"tag": "section"}})
        if tag == "button":
            # A button with no form behind it is a styled block.
            return self.new({"_id": nid, "type": "Block", "tag": "div",
                             "classes": cls, "children": [],
                             "data": {"tag": "div"}})
        if tag in BLOCKISH:
            htag = tag if tag in ("span", "em", "strong", "i", "b",
                                  "header", "footer", "figure",
                                  "figcaption", "label", "article",
                                  "aside", "main") else "div"
            return self.new({"_id": nid, "type": "Block", "tag": htag,
                             "classes": cls, "children": [],
                             "data": {"tag": htag}})
        # Anything unrecognised becomes a plain block rather than vanishing.
        return self.new({"_id": nid, "type": "Block", "tag": "div",
                         "classes": cls, "children": [],
                         "data": {"tag": "div"}})

    def handle_endtag(self, tag):
        if tag == "body":
            self.in_body = False
            return
        if tag in VOID:
            return
        # Close back to the matching frame. The source is well-formed, so
        # this normally pops exactly one.
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        if self.skipping or self.parent() is None:
            return
        text = re.sub(r"\s+", " ", data)
        if not text.strip():
            return
        tid = str(uuid.uuid4())
        self.nodes.append({"_id": tid, "text": True, "v": text.strip()})
        self.parent()["children"].append(tid)


def page_slug(href):
    name = href.split("#")[0].split("?")[0]
    if name in ("index.html", "", "./"):
        return ""
    return name.replace(".html", "")


# ---------------------------------------------------------------------------
# 4. Payload assembly + validation
# ---------------------------------------------------------------------------

def validate(payload):
    """Referential integrity. Catches the mistakes this script could make;
    says nothing about whether Webflow accepts the schema."""
    nodes = {n["_id"]: n for n in payload["payload"]["nodes"]}
    styles = {s["_id"] for s in payload["payload"]["styles"]}
    problems = []

    if len(nodes) != len(payload["payload"]["nodes"]):
        problems.append("duplicate node ids")

    for n in payload["payload"]["nodes"]:
        for child in n.get("children", []):
            if child not in nodes:
                problems.append(f"node {n['_id']} references missing child {child}")
        for sid in n.get("classes", []):
            if sid not in styles:
                problems.append(f"node {n['_id']} references missing style {sid}")
        if n.get("text") and "v" not in n:
            problems.append(f"text node {n['_id']} has no value")

    # Every node reachable exactly once from a root.
    seen = {}
    def walk(nid, path):
        if nid in seen:
            problems.append(f"node {nid} reached twice")
            return
        seen[nid] = path
        for c in nodes.get(nid, {}).get("children", []):
            walk(c, path + [nid])
    for r in payload["payload"].get("_roots", []):
        walk(r, [])
    orphans = set(nodes) - set(seen)
    if orphans and payload["payload"].get("_roots"):
        problems.append(f"{len(orphans)} orphan node(s)")
    return problems


def build_payload(nodes, roots, styles):
    # Only ship the styles this page actually uses, plus nothing else:
    # a paste that carries unused classes clutters the project's class list.
    used = set()
    for n in nodes:
        used.update(n.get("classes", []))
    page_styles = [s for s in styles if s["_id"] in used]
    return {
        "type": "@webflow/XscpData",
        "payload": {
            "nodes": nodes,
            "styles": page_styles,
            "assets": [],
            "ix1": [],
            "ix2": {"interactions": [], "events": [], "actionLists": []},
            "_roots": roots,
        },
        "meta": {
            "unlinkedSymbolCount": 0,
            "droppedLinks": 0,
            "dynBindRemovedCount": 0,
            "dynListBindRemovedCount": 0,
            "paginationRemovedCount": 0,
        },
    }


def main():
    tokens = read_tokens(os.path.join(DIST, "assets/css/tokens.css"))
    styles, style_ids, custom_css = build_styles(tokens, html_classes())

    os.makedirs(os.path.join(OUT, "paste"), exist_ok=True)

    report = []
    all_notes = {}
    for filename, slug, label in PAGES:
        html = open(os.path.join(DIST, filename)).read()
        html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
        conv = Converter(style_ids)
        conv.feed(html)

        payload = build_payload(conv.nodes, conv.roots, styles)
        problems = validate(payload)
        # _roots is ours, not Webflow's: drop it before writing.
        payload["payload"].pop("_roots", None)

        path = os.path.join(OUT, "paste", f"{slug}.json")
        with open(path, "w") as fh:
            json.dump(payload, fh, separators=(",", ":"))

        elements = sum(1 for n in conv.nodes if not n.get("text"))
        text = sum(1 for n in conv.nodes if n.get("text"))
        report.append((label, slug, elements, text,
                       len(payload["payload"]["styles"]),
                       os.path.getsize(path), problems))
        all_notes[label] = sorted(set(conv.notes))

    head = HEAD_TEMPLATE.format(css=custom_css)
    open(os.path.join(OUT, "custom-code-head.html"), "w").write(head)
    open(os.path.join(OUT, "custom-code-footer.html"), "w").write(FOOTER_CODE)

    print(f"{'Page':<10} {'elements':>9} {'text':>6} {'styles':>7} {'size':>9}  issues")
    ok = True
    for label, slug, el, tx, st, size, problems in report:
        print(f"{label:<10} {el:>9} {tx:>6} {st:>7} {size/1024:>8.1f}K  "
              f"{'-' if not problems else problems[0]}")
        if problems:
            ok = False
            for p in problems[1:]:
                print(f"{'':<10} {'':>9} {'':>6} {'':>7} {'':>9}  {p}")
    print(f"\n{len(styles)} Webflow styles generated; "
          f"{len(custom_css.splitlines())} lines of custom CSS.")
    print(f"written to {OUT}")
    return 0 if ok else 1


HEAD_TEMPLATE = """<!-- =====================================================================
     J BOWMAN - styles Webflow's panel cannot hold
     Paste into: Project Settings -> Custom Code -> Head

     These are the rules with a descendant combinator, a pseudo-class or a
     pseudo-element: component internals, hover and focus states, the
     ground-dependent colour overrides that keep the contrast law, the
     marquee animation, and the reduced-motion and print rules.

     The single-class rules are NOT here - those came across as real
     Webflow styles and are editable in the Designer.
     ================================================================== -->
<style>
/* Font fallbacks. Belleza is a humanist SANS; a serif fallback would change
   the page's character in the moment before the webfont lands. */
.display-1,.display-2,.display-3,.row__label,.s-credit__title,
.s-discipline__name,.s-marquee__track li,.nav__mark,.s-foot__mark {{
  font-family: Belleza, Optima, "Gill Sans", "Gill Sans MT", "Trebuchet MS", "Segoe UI", sans-serif;
  font-weight: 400;  /* Belleza ships ONE weight. Anything else is a fake. */
}}

{css}
</style>
"""

FOOTER_CODE = """<!-- =====================================================================
     J BOWMAN - click-to-load YouTube player
     Paste into: Project Settings -> Custom Code -> Footer

     In the Releases Collection Item, add an HTML Embed containing:
         <div class="jb-yt" data-url="{{ YouTube URL }}"></div>
     using Webflow's field picker for the field reference.

     Nothing is requested from YouTube until the visitor clicks: no cookie,
     no third-party connection on page load. A release with no URL removes
     its own embed, so the page is never half-built.
     ================================================================== -->
<style>
.jb-yt__btn{font-family:Montserrat,sans-serif;font-weight:500;font-size:9.6px;
  letter-spacing:.22em;text-transform:uppercase;color:#b984b0;
  background:none;border:1px solid rgba(185,132,176,.5);
  padding:.7em 1.2em;cursor:pointer}
.jb-yt__btn:hover{background:#b984b0;color:#0b0a0c}
.jb-yt__frame{position:relative;aspect-ratio:16/9;margin-top:1.2rem;background:#000}
.jb-yt__frame iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
</style>
<script>
(function(){
  var ID=/^[A-Za-z0-9_-]{11}$/;
  function idFrom(v){
    v=(v||'').trim(); if(!v) return '';
    if(ID.test(v)) return v;
    var m=v.match(/(?:youtube(?:-nocookie)?\\.com\\/(?:watch\\?(?:.*&)?v=|embed\\/|shorts\\/|live\\/)|youtu\\.be\\/)([A-Za-z0-9_-]{11})/);
    return m?m[1]:'';
  }
  Array.prototype.forEach.call(document.querySelectorAll('.jb-yt'),function(host){
    var id=idFrom(host.getAttribute('data-url'));
    if(!id){ if(host.parentNode) host.parentNode.removeChild(host); return; }
    var btn=document.createElement('button');
    btn.type='button'; btn.className='jb-yt__btn';
    btn.textContent='\\u25B6 Watch';
    btn.setAttribute('aria-label','Watch this track on YouTube');
    host.appendChild(btn);
    btn.addEventListener('click',function(){
      var frame=document.createElement('div'); frame.className='jb-yt__frame';
      var ifr=document.createElement('iframe');
      ifr.src='https://www.youtube-nocookie.com/embed/'+id+
        '?rel=0&modestbranding=1&playsinline=1&autoplay=1';
      ifr.title='YouTube video player';
      ifr.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
      ifr.setAttribute('allowfullscreen','');
      frame.appendChild(ifr);
      host.replaceChild(frame,btn);
    });
  });
})();
</script>
"""


if __name__ == "__main__":
    sys.exit(main())
