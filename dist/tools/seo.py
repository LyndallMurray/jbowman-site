#!/usr/bin/env python3
"""
J BOWMAN — SEO pass
===================

One place that owns the site's identity on the web, so canonical URLs,
social cards and structured data cannot drift apart.

Run:  python3 tools/seo.py          (report only, changes nothing)
      python3 tools/seo.py --write  (apply, and regenerate sitemap/robots)

WHAT IT FIXES

1. The canonical domain. Canonicals said jbowman.com; the domain actually
   registered is jbowmanmusic.com. A canonical pointing at a domain you do
   not control tells Google the real page is somewhere else, which is the
   single most damaging thing in this file.

2. og:image was a RELATIVE path. Open Graph requires an absolute URL —
   Facebook, LinkedIn, iMessage, Slack and WhatsApp all fail to render a
   card with a relative one, silently. Every page had this.

3. og:url was missing entirely.

4. Two meta descriptions ran past the ~155 characters search results show,
   so they were being cut mid-sentence.

5. No sitemap.xml and no robots.txt existed.

6. Structured data was on the homepage only, and carried the wrong domain.

Canonicals stay self-referential and keep the .html extension, so they are
correct for this static build however it is hosted. Webflow serves
extensionless paths, so when the site moves there the canonical for
/about.html becomes /about — see SELF_VS_WEBFLOW at the bottom.
"""

import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.dirname(HERE)

# The canonical host, including www or not. This MUST match the host the site
# actually serves from — whichever one Netlify lists as the Primary domain.
# The other host redirects to it, so naming the redirecting one in a canonical
# tells Google the real page is somewhere it isn't.
#
# Override without editing this file:  python3 tools/seo.py --write \
#                                        --site https://jbowmanmusic.com
SITE = "https://www.jbowmanmusic.com"
OLD_SITE = "https://jbowman.com"
SHARE_IMAGE = "/assets/img/portrait.jpg"   # 1080x1080

# path on the live site -> (file, priority)
#
# The paths are EXTENSIONLESS and the files keep their .html names. Both
# Netlify and Webflow serve /about from about.html, and both treat the
# extensionless form as the real URL. Canonicals therefore have to name the
# extensionless path, or every page claims a canonical URL that redirects —
# which is the same self-defeating signal as naming the wrong domain.
# netlify.toml 301s the .html form to the clean one so there is exactly one
# URL per page.
PAGES = {
    "/": ("index.html", "1.0"),
    "/work": ("work.html", "0.9"),
    "/services": ("services.html", "0.9"),
    "/about": ("about.html", "0.8"),
    "/connect": ("connect.html", "0.8"),
    "/journal": ("journal.html", "0.6"),
}

# Descriptions that overran what search results display. Rewritten to keep
# the first, load-bearing clause and land under ~155 characters.
DESCRIPTIONS = {
    "index.html": (
        "J BOWMAN — multi-platinum, Grammy-nominated songwriter, musician "
        "and producer/engineer working across records, film, television, "
        "advertising and culture."
    ),
    "about.html": (
        "Multi-platinum, Grammy-nominated songwriter, musician, composer and "
        "producer/engineer. From Chicago to the Bay Area, and from records "
        "to the screen."
    ),
    "services.html": (
        "Commissioning pathways with J Bowman: records, score and picture, "
        "brands and culture, podcast and spoken audio. Songwriting, "
        "production, mixing and sync."
    ),
}

# Photographs carrying real information. An empty alt tells a screen reader
# and a crawler the image is decorative; these are not. The hero portrait is
# the page's primary image and is fetched at high priority — leaving it
# unnamed forfeits image search for the one picture that matters most.
ALTS = {
    "portrait-blend.png": "J Bowman, songwriter and producer, in portrait",
    "truck-jump.jpg": "J Bowman mid-jump from the back of a pickup truck on a "
                      "desert road",
}

def person():
    """Built at call time, not import time, so --site can change the host."""
    return {
    "@context": "https://schema.org",
    "@type": "Person",
    "@id": f"{SITE}/#person",
    "name": "J Bowman",
    "alternateName": "J BOWMAN",
    "url": f"{SITE}/",
    "image": f"{SITE}{SHARE_IMAGE}",
    "jobTitle": ["Songwriter", "Musician", "Composer", "Producer",
                 "Audio Engineer"],
    "knowsAbout": ["Songwriting", "Music production", "Recording",
                   "Mixing", "Audio engineering", "Film scoring",
                   "Television music", "Music synchronisation", "Guitar"],
    "description": ("Multi-platinum, Grammy-nominated songwriter, musician, "
                    "composer and producer/engineer working across records, "
                    "film, television, advertising and culture."),
    # No sameAs yet: the social profile URLs are still unset in config.js.
    # An empty or guessed sameAs is worse than none — it is how a knowledge
    # panel gets attached to the wrong person.
    }


def website():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": f"{SITE}/#website",
        "url": f"{SITE}/",
        "name": "J BOWMAN",
        "publisher": {"@id": f"{SITE}/#person"},
        "inLanguage": "en",
    }


def breadcrumbs(label, path):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",
             "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": label,
             "item": f"{SITE}{path}"},
        ],
    }


def ld(obj):
    return ('<script type="application/ld+json">\n'
            + json.dumps(obj, separators=(",", ":")) + "\n</script>")


def process(path, filename, html):
    """Return (new_html, [changes])."""
    changes = []

    # --- 1. canonical domain -------------------------------------------
    if OLD_SITE in html:
        n = html.count(OLD_SITE)
        html = html.replace(OLD_SITE, SITE)
        changes.append(f"canonical domain: {n}x jbowman.com -> jbowmanmusic.com")

    canonical = f"{SITE}{path}"
    html, k = re.subn(r'<link rel="canonical" href="[^"]*">',
                      f'<link rel="canonical" href="{canonical}">', html)
    if k:
        changes.append(f"canonical -> {canonical}")

    # --- 2. og:image absolute ------------------------------------------
    # Always SET it. An earlier version only rewrote a RELATIVE value, so
    # changing the canonical host left og:image pointing at the old one —
    # the same non-idempotency bug as og:url had, and just as quiet.
    want_image = f"{SITE}{SHARE_IMAGE}"
    m = re.search(r'<meta property="og:image" content="([^"]*)">', html)
    if m and m.group(1) != want_image:
        was = "relative" if not m.group(1).startswith("http") else m.group(1)
        html = html.replace(m.group(0),
                            f'<meta property="og:image" content="{want_image}">')
        changes.append(f"og:image -> {want_image} (was {was})")
    # Dimensions let a scraper lay the card out before fetching the file.
    if 'property="og:image:width"' not in html:
        html = html.replace(
            f'<meta property="og:image" content="{want_image}">',
            f'<meta property="og:image" content="{want_image}">\n'
            '<meta property="og:image:width" content="1080">\n'
            '<meta property="og:image:height" content="1080">\n'
            '<meta property="og:image:alt" content="Portrait of J Bowman">')
        changes.append("og:image dimensions + alt added")

    # --- 3. og:url ------------------------------------------------------
    # Always SET it, never just add it. An earlier version only inserted
    # og:url when absent, so a second run left a stale value behind while
    # reporting success — og:url and the canonical disagreed, which is the
    # same contradictory signal this script exists to prevent.
    if 'property="og:url"' in html:
        html, k = re.subn(r'<meta property="og:url" content="[^"]*">',
                          f'<meta property="og:url" content="{canonical}">', html)
        if k:
            changes.append(f"og:url -> {canonical}")
    else:
        html = html.replace('<meta property="og:type"',
                            f'<meta property="og:url" content="{canonical}">\n'
                            '<meta property="og:type"', 1)
        changes.append(f"og:url added -> {canonical}")

    # --- 4. description length ------------------------------------------
    if filename in DESCRIPTIONS:
        m = re.search(r'<meta name="description" content="([^"]*)">', html)
        if m and len(m.group(1)) > 160:
            new = DESCRIPTIONS[filename]
            html = html.replace(m.group(0),
                                f'<meta name="description" content="{new}">')
            html = re.sub(r'(<meta property="og:description" content=")[^"]*(">)',
                          rf'\g<1>{new}\g<2>', html)
            changes.append(f"description {len(m.group(1))} -> {len(new)} chars")

    # --- 5. image alt text ----------------------------------------------
    for src, alt in ALTS.items():
        pattern = re.compile(r'(<img src="[^"]*' + re.escape(src) + r'"[^>]*?)alt=""')
        html, k = pattern.subn(rf'\g<1>alt="{alt}"', html)
        if k:
            changes.append(f"alt text added for {src}")

    # --- 6. structured data ---------------------------------------------
    html = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', "",
                  html, flags=re.S)
    if path == "/":
        block = ld(person()) + "\n" + ld(website())
        changes.append("JSON-LD: Person + WebSite")
    else:
        label = re.search(r"<title>([^<]*?)\s*—", html)
        label = label.group(1).strip() if label else filename
        block = ld(breadcrumbs(label, path))
        changes.append(f"JSON-LD: BreadcrumbList ({label})")
    html = html.replace("</head>", block + "\n</head>", 1)

    return html, changes


def sitemap():
    today = date.today().isoformat()
    rows = "\n".join(
        f"  <url>\n    <loc>{SITE}{p}</loc>\n"
        f"    <lastmod>{today}</lastmod>\n"
        f"    <priority>{prio}</priority>\n  </url>"
        for p, (_, prio) in PAGES.items())
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9">\n'
            f"{rows}\n</urlset>\n".replace("www.sitemap.org", "www.sitemaps.org"))


def robots():
    return (
        "# J BOWMAN\n"
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        "# Internal brand reference, not for search.\n"
        "Disallow: /brand/\n"
        "\n"
        f"Sitemap: {SITE}/sitemap.xml\n"
    )


SELF_VS_WEBFLOW = """
WHEN THIS MOVES TO WEBFLOW
--------------------------
Webflow serves extensionless paths, so set each page's canonical in
Page Settings to the extensionless form:

    /about.html     ->  https://jbowmanmusic.com/about
    /work.html      ->  https://jbowmanmusic.com/work
    /services.html  ->  https://jbowmanmusic.com/services
    /journal.html   ->  https://jbowmanmusic.com/journal
    /connect.html   ->  https://jbowmanmusic.com/connect
    /               ->  https://jbowmanmusic.com/

Webflow generates sitemap.xml itself — turn it on in
Project Settings -> SEO -> Sitemap, and do NOT also upload the file this
script writes, or you will have two sitemaps disagreeing.

og:image must be the Webflow CDN URL of the uploaded portrait, not a path
on this build. Set it per page under Page Settings -> Open Graph.

Paste the JSON-LD from the homepage into
Project Settings -> Custom Code -> Head, and the per-page BreadcrumbList
into each page's own Page Settings -> Custom Code -> Head.
"""


def main():
    global SITE
    write = "--write" in sys.argv
    if "--site" in sys.argv:
        SITE = sys.argv[sys.argv.index("--site") + 1].rstrip("/")
    print(f"canonical host: {SITE}")
    total = 0
    for path, (filename, _) in PAGES.items():
        full = os.path.join(DIST, filename)
        original = open(full).read()
        updated, changes = process(path, filename, original)
        print(f"\n{filename}")
        for c in changes:
            print(f"   {c}")
        if not changes:
            print("   (nothing to do)")
        total += len(changes)
        if write and updated != original:
            open(full, "w").write(updated)

    if write:
        open(os.path.join(DIST, "sitemap.xml"), "w").write(sitemap())
        open(os.path.join(DIST, "robots.txt"), "w").write(robots())
        print(f"\nwrote sitemap.xml ({len(PAGES)} URLs) and robots.txt")
        print(f"applied {total} changes across {len(PAGES)} pages")
    else:
        print(f"\n{total} changes pending. Re-run with --write to apply.")
    print(SELF_VS_WEBFLOW)
    return 0


if __name__ == "__main__":
    sys.exit(main())
