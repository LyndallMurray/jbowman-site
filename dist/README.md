# J BOWMAN

Two deliverables, one design system, one deployable folder.

```
python3 -m http.server --directory dist 8000
```

- **`dist/`** — the public site: Home, About, Work, Journal, Connect
- **`dist/brand/`** — the brand guidelines, all eleven sections (`noindex`)
- **`dist/assets/css/tokens.css`** — the single source of truth both read

Static HTML/CSS/JS. No build step, no dependencies.

## The token layer

`tokens.css` holds every colour, the full type scale, space and motion. Both
the guidelines and the site read it, so the two cannot drift: change a value
once and both move.

Every value is lifted from the approved guidelines, not invented — the five
neutrals, Bruised Plum with its deep and tint, and the type scale verbatim
(Display 1 at clamp 3.4–8.5rem, tracking 0.04em, line-height 0.92, and so on).

| Token | Value | Use |
| --- | --- | --- |
| `--ink` | `#0B0A0C` | Primary ground |
| `--smoke` | `#3A3540` | Secondary surface, dividers on dark |
| `--bone` | `#F1ECE1` | Primary light ground, type on ink |
| `--warm-white` | `#FBF8F3` | Paper, print stock, framed fields |
| `--shell` | `#E3D9C6` | Tertiary surface, packaging |
| `--plum` | `#6E2A5C` | The signature |
| `--plum-deep` | `#2B1226` | Depth beneath the signature |
| `--orchid` | `#B984B0` | The tint |

## What "optimised" means here

Reading the guidelines properly surfaced three rules the earlier build was
quietly breaking. They are now enforced, and `tools/audit.js` checks them.

**One plum field per page.** The guidelines reserve the signature for "a mark,
a hairline, a single word, or one full-bleed moment per piece — never as a
background for text-heavy layouts." Plum had been a CTA band on three pages at
once. Now: Home has one, Work has one, About, Journal and Connect have none.

**The signature type moment, once per composition.** The upright Belleza with
one Montserrat italic is the identity's type signature; using it twice spends
it. Each page now carries exactly one.

**The contrast law.** Bone on Plum and Plum on Bone clear 4.5:1. Orchid on Bone
and Plum on Ink do not. Neither forbidden pairing is given a token, so breaking
the rule takes a deliberate hand-written value rather than a slip.

One gap found in the guidelines themselves: the contrast law covers ink and
bone but is silent on smoke. Measured, Orchid on Smoke is **3.96:1** — below AA
for small text. On a smoke ground the accent token now resolves to bone, so any
accent use there degrades safely. Worth adding to the guidelines at the next
revision.

## Audit

```
node tools/audit.js        # expects the site served on :8140
```

Checks, against a real browser: WCAG 2.2 AA contrast for every text node
composited against its actual background with alpha blended; the guidelines'
contrast law; one plum field per page; one signature type moment per page; no
image rendered above native resolution; no horizontal pan at 1600 / 1280 / 900
/ 600 / 390 / 320 px.

All six pages currently pass.

Two things the audit deliberately excludes. Colour specimens carry
`data-specimen` — a swatch showing plum is documentation of the palette, not
compositional use of it. And `aria-hidden` decorative specimens are skipped:
the "Negative space" plate and the blind-emboss mark are *demonstrating* low
contrast, and their captions carry the meaning.

## Before this goes live

**Set the contact email.** `dist/assets/js/config.js` is the only file to edit.
Fill in `contactEmail` and the Connect form works; add `formEndpoint`
(Formspree, Basin, Netlify) and it posts without leaving the page. Until then
the form says it is not connected rather than swallowing enquiries, and the
Direct Contact block still reads `[Insert management or contact email]`.
Social URLs live in the same file; anything left empty renders as plain text,
never a dead link.

**Replace the photography.** See below.

**Write the first Journal entries.** The page has its four categories and
states plainly that the first pieces are being written. It invents nothing.

## Photography

Written permission is held for the supplied photography, so licensing is
settled. What follows is about the files.

In use, all free of burned-in marks: `portrait-blend` and `portrait`
(1080×1080), `desert-tall` (399×501), `truck-jump` (518×386), plus `stage`,
`live`, `stage-fragment`, `performance` and `desert-square` in the guidelines'
contact sheet.

Small originals are capped at their native width (`.s-plate--*`) so the layout
cannot scale them up into softness. The audit fails the build if any image
renders above native. When a larger original replaces one, raise the cap.

**Not used, because of marks burned into the pixels:** `frame-e` ("© ursula
2014"), `live-green` (Instagram avatar), and the four Getty comp files
`duo-live`, `group-three`, `seated-j`, `solo-seated`. A Getty licence entitles
you to the clean download; a comp cannot be retouched into a licensed asset.
Also unused: `frame-d`, an older card using a `J.BOWMAN` logo with a full stop,
which conflicts with the approved wordmark.

**The studio-console shot is still missing** and is the strongest asset seen —
it evidences the producer/engineer claim the copy makes and nothing else
currently proves. It never reached this machine. A commissioned shoot remains
the real answer: hero landscape, portrait, close detail, negative-space crops,
monochrome options.

## Wordmark

`J BOWMAN`. Never "Jay Bowman Music", never `J.BOWMAN`. In both heroes it is
set `white-space: nowrap` so it cannot break across two lines at any viewport,
verified 320–1600px.

## Not built

No CMS, no analytics, no privacy notice, no sitemap or robots.txt, no
individual Journal entry template. Canonical URLs and Open Graph tags assume
`https://jbowman.com/`. The Open Graph image points at the portrait; a
dedicated 1200×630 card would be better.
