# J BOWMAN

The commercial website for J Bowman — songwriter, musician, composer, producer,
engineer. Static HTML/CSS/JS. No build step, no dependencies, no framework.

```
python3 -m http.server --directory dist 8000
```

Originally a Claude Design handoff bundle (`project/`, `chats/`); those stay as
source material and are not part of the site.

## Layout

```
dist/
  index.html about.html work.html services.html journal.html connect.html
  brand/index.html        the brand guidelines, eleven sections, noindex
  sitemap.xml robots.txt favicon.svg
  netlify.toml            for a drag-and-drop deploy (no [build] section)
  assets/css/tokens.css   SINGLE SOURCE OF TRUTH
  assets/css/base.css     shared primitives
  assets/css/site.css     public site (.s- prefix)
  assets/css/brand.css    guidelines (.gl- prefix)
  assets/js/config.js     contact address, social links, track videos
  assets/js/site.js       nav, reveal, form, facade YouTube players
  assets/fonts/           Belleza + Montserrat, self-hosted, SIL OFL
  assets/img/             photography
  assets/video/reel.mp4   the showreel, byte-identical to the supplied file
  tools/                  see below
  webflow/                paste payloads, if the site ever moves to Webflow
netlify.toml              for a Git-connected deploy (publish = "dist")
```

## The token layer

`tokens.css` holds every colour, the full type scale, space and motion. The
guidelines and the site both read it, so the two cannot drift: change a value
once and both move.

## Rules the build must not break

Written into the approved guidelines, or learned the hard way:

1. **Never Orchid type on Bone. Never Plum type on Ink.** Both fail contrast.
   The accent follows the ground: Orchid on dark, Plum on light. The two
   forbidden pairings are deliberately given no token.
2. **At most one plum field per page.** Ink and bone carry ~90% of any
   composition; the signature is a mark, a hairline, a word, or one full-bleed
   moment.
3. **Belleza is always weight 400.** It ships one weight — anything else is a
   browser-synthesised fake, and heading tags default to bold.
4. **Belleza's fallback is a humanist sans, never a serif.** Belleza is itself
   a sans; a serif fallback changes the page's character while the font loads.
5. **No image displayed above its native width.**
6. **No horizontal scroll at any width.**

`tools/audit.js` enforces 1, 2, 5 and 6 automatically.

## Tools

| Tool | What it does |
| --- | --- |
| `tools/audit.js` | Contrast, the contrast law, one-plum-field, image upscaling, horizontal pan at six widths. Needs a server on :8140. |
| `tools/seo.py` | Owns the site's web identity in one place — canonicals, og:url, og:image, descriptions, JSON-LD, sitemap, robots. Dry run by default; `--write` applies. `--site` changes the canonical host. |
| `tools/verify-live.py` | Run from a networked machine against the live site: competing hostnames, 301-vs-302, certificate coverage, canonical correctness, og:image reachability, JSON-LD parsing. Stdlib only. |
| `tools/webflow-export.py` | Regenerates `webflow/` — Webflow Designer clipboard payloads plus the CSS its style panel cannot hold. |

## Deploying

Drag `dist/` (or a zip of it) onto <https://app.netlify.com/drop>. `netlify.toml`
inside `dist/` handles the rest: `.html` → clean-URL 301s, cache headers, a CSP,
and a noindex header on `/brand/`.

Connected to Git instead, the root `netlify.toml` publishes `dist/`, and
`.github/workflows/pages.yml` publishes the same folder to GitHub Pages.

**The canonical host must match the host the site actually serves from.** It is
currently `https://www.jbowmanmusic.com`. If the apex is primary instead:

```
python3 dist/tools/seo.py --write --site https://jbowmanmusic.com
```

## Outstanding

- **The four YouTube URLs in `config.js` are unverified.** Each ID came from an
  indexed search result, not from opening the video — YouTube was unreachable
  from the session that found them. Confirm each is the right song *and* an
  official artist or label upload. `JBM—003` is the least certain. `JBM—005` is
  an album with no single video; leave it empty.
- **The journal has no entries.** Page, categories and CMS shape are built.
- **The showreel's title card** at ~35–38s reads "JASON BOWMAN" in a heavy
  grotesque, contradicting the approved wordmark and the Belleza-only rule. The
  file is otherwise untouched and byte-identical to the supplied original.
- **Four supplied photographs carry burned-in Getty watermarks** (`duo-live`,
  `group-three`, `seated-j`, `solo-seated`), `frame-e` carries "© ursula 2014",
  and `live-green` has Instagram chrome in frame. Written permission is held,
  but a comp's watermark is in the pixels, so these need clean re-downloads
  against the licence. **None of them are used in the build** — nothing ships
  with a watermark.
- **Social URLs are unset** in `config.js`. They render as plain text, never
  dead links. Setting them is also what unlocks `sameAs` in the Person schema,
  deliberately omitted while they are unknown.
