# J BOWMAN — website handover

Everything needed to put this site live and keep it running. No prior context
required. Anyone comfortable with a web browser can do the first part; a
developer can do all of it in about fifteen minutes.

```
website/   the site itself — this folder IS the deployable site
tools/     four scripts (see "Tools" below)
webflow/   only if you ever want to rebuild this inside Webflow
```

The code also lives at **https://github.com/LyndallMurray/jbowman-site**
(branch `main`), already configured for Netlify.

---

## 1. Put it live — the fast way (3 minutes, no account setup)

1. Go to **https://app.netlify.com/drop**
2. Drag the **`website`** folder onto the page
3. Wait ~30 seconds

You get a URL like `melodic-crumble-a1b2c3.netlify.app`. That is the live site.

Rename it under **Site configuration → Change site name** if you want
something tidier, e.g. `jbowman-music`.

> Drag the **folder**, not its contents, and not a zip you made yourself.
> `netlify.toml` inside it configures redirects, caching and security headers
> automatically.

## 1b. Put it live — the durable way (better, needs a Netlify login)

Deploy from GitHub instead, and every future code change republishes itself.

1. **https://app.netlify.com/start/repos**
2. Click **GitHub**, authorise if asked
3. Pick **jbowman-site**
   - Not listed? The Netlify GitHub app needs access to it:
     **https://github.com/apps/netlify/installations/select_target**
     → grant access to `jbowman-site` → return to step 1
4. Change **nothing** on the settings screen — `netlify.toml` supplies it all.
   Confirm the branch is `main`.
5. **Deploy**

---

## 2. Connect jbowmanmusic.com

Do this only after step 1 works and you can load the site on its
`.netlify.app` address.

### First: kill the GoDaddy forward

The domain currently shows a GoDaddy parking page at `/lander`. That is
**domain forwarding**, which is on by default for new domains, and it
overrides DNS completely — correct records will do nothing until it is gone.

1. **GoDaddy → Domain Portfolio → jbowmanmusic.com → Domain Settings**
2. Find **Forwarding**. Delete every rule there.

### Then: point DNS at Netlify

1. In Netlify: **Domain management → Add a domain** → `jbowmanmusic.com`
2. Netlify prints the exact DNS records. **Use the values it shows you** —
   they change over time, so do not copy them from any guide, including this
   one.
3. **GoDaddy → DNS → DNS Records.** Delete:
   - the `A` record on `@` (GoDaddy often shows its value as **"Parked"**)
   - the default `CNAME` on `www`
4. Add Netlify's records. Set **TTL to 600** while cutting over.
5. **Leave every `MX` row alone.** Those route email, not web traffic.
6. Wait 10–30 minutes. In Netlify, **HTTPS → Verify DNS configuration** to
   issue the certificate. A browser warning before that is normal.

### Then: check the canonical host matches

The site's canonical URLs currently say `https://www.jbowmanmusic.com`.
Whichever host Netlify lists as **Primary domain** must match. If Netlify
makes the apex primary instead, run:

```
python3 tools/seo.py --write --site https://jbowmanmusic.com
```

and redeploy. Getting this wrong does not break the site; it quietly splits
its search ranking between two addresses.

---

## 3. Check it worked

```
python3 tools/verify-live.py
```

Python 3, no installation needed. It checks what a browser will not show you:
both hostnames competing for the same ranking, a temporary redirect where a
permanent one belongs, certificate coverage, canonical correctness, whether
the social-card image actually loads, and whether the structured data parses.

Add `--domain yoursite.netlify.app` to run it before the domain is connected.

---

## 4. The enquiry form

Submissions go to **hello@archausagency.com**.

On Netlify, the form is captured server-side: go to **Forms** in the site
dashboard, confirm an **`enquiry`** form is listed, and add that address as a
notification recipient. Anywhere else, the form falls back to opening the
visitor's email app with the enquiry pre-filled — it still works, it just
depends on them having mail set up.

---

## Tools

| Script | What it does |
| --- | --- |
| `tools/verify-live.py` | Checks the live site. Python 3, nothing to install. |
| `tools/seo.py` | Owns canonicals, og: tags, descriptions, structured data, sitemap, robots. Dry run by default; `--write` applies; `--site` sets the canonical host. |
| `tools/audit.js` | Contrast, brand rules, image upscaling, horizontal scroll at six widths. Needs Node and a local server on port 8140. |
| `tools/webflow-export.py` | Regenerates `webflow/` if the site changes. |

---

## Brand rules the site must keep

From the approved guidelines. Breaking these is how it stops looking like
itself.

1. **Never Orchid type on Bone. Never Plum type on Ink.** Both fail contrast.
   The accent follows the ground: Orchid on dark, Plum on light.
2. **One plum field per page, maximum.** Ink and bone carry about 90% of any
   composition; the signature colour is a mark, a hairline, a single word, or
   one full-bleed moment.
3. **Belleza is always weight 400.** It ships one weight — anything heavier is
   a browser-faked bold, and HTML headings default to bold, so it must be set
   explicitly.
4. **Belleza's fallback is a humanist sans, never a serif.**
5. **No image shown larger than its native pixel width.**
6. **No horizontal scrolling at any screen width.**

`tools/audit.js` enforces 1, 2, 5 and 6.

---

## Still outstanding

- **The four YouTube links in `website/assets/js/config.js` are unverified.**
  Each video ID came from a search result, not from opening the video — YouTube
  was unreachable from the machine that found them. Open each one and confirm
  it is the right song *and* an official artist or label upload.
  `JBM—003` ("Life Is Better With You") is the least certain. `JBM—005` is an
  album with no single video; leave it blank.
- **The journal has no entries.** The page, its four categories and the layout
  are built and waiting.
- **The showreel's title card** at about 35–38 seconds reads "JASON BOWMAN" in
  the wrong typeface, contradicting the approved J BOWMAN wordmark. The video
  is otherwise the supplied original, untouched.
- **Four supplied photographs carry burned-in Getty watermarks** and are
  **not used** in the site — nothing published has a watermark on it. If you
  want them, they need clean re-downloads against the licence.
- **Social links are unset** in `config.js`. They render as plain text rather
  than dead links. Setting them also unlocks the `sameAs` field in the
  structured data, deliberately left out while the URLs are unknown.

---

## Editing

Plain HTML and CSS. No build step, no framework, no dependencies.

```
python3 -m http.server --directory website 8000
```

`website/assets/css/tokens.css` is the single source of truth for every
colour, type size and spacing value. Change it there and the whole site
follows, including the brand guidelines page at `/brand/`.
