#!/usr/bin/env python3
"""
J BOWMAN — post-launch verifier
===============================

Run this from your own machine AFTER connecting jbowmanmusic.com to Webflow
and publishing. It answers "did that actually work?" in one command, and
catches the handful of things that are wrong silently — a site can look
perfect in a browser while splitting its search ranking across two hosts or
serving a share card with no image.

    python3 verify-live.py
    python3 verify-live.py --domain jbowmanmusic.com --staging j-bowman.webflow.io

Standard library only, so there is nothing to install.

Exit code 0 if everything passes, 1 if anything failed.
"""

import argparse
import json
import re
import socket
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

PATHS = ["/", "/work", "/services", "/about", "/journal", "/connect"]

UA = "jbowman-site-check/1.0"

PASS, FAIL, WARN = "PASS", "FAIL", "WARN"
results = []


def record(status, check, detail=""):
    results.append((status, check, detail))
    mark = {PASS: "  ok ", FAIL: "FAIL", WARN: "warn"}[status]
    print(f"  [{mark}] {check}" + (f"\n         {detail}" if detail else ""))


def fetch(url, method="GET", redirect=True):
    """Return (status, headers, body_text, final_url)."""
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None

    handlers = [] if redirect else [NoRedirect]
    opener = urllib.request.build_opener(*handlers)
    req = urllib.request.Request(url, method=method,
                                 headers={"User-Agent": UA})
    try:
        with opener.open(req, timeout=20) as r:
            body = r.read(400_000)
            charset = r.headers.get_content_charset() or "utf-8"
            return r.status, dict(r.headers), body.decode(charset, "replace"), r.url
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), "", url
    except (urllib.error.URLError, socket.timeout, ssl.SSLError) as e:
        return None, {}, str(e), url


# ---------------------------------------------------------------------------

def check_dns(domain):
    print("\nDNS")
    for host in (domain, f"www.{domain}"):
        try:
            addrs = sorted({ai[4][0] for ai in socket.getaddrinfo(host, 443)})
            record(PASS, f"{host} resolves", ", ".join(addrs))
        except socket.gaierror as e:
            record(FAIL, f"{host} does not resolve",
                   f"{e}. DNS has not propagated, or the record is missing "
                   f"at GoDaddy.")


def check_tls(domain):
    print("\nTLS")
    for host in (domain, f"www.{domain}"):
        ctx = ssl.create_default_context()
        try:
            with socket.create_connection((host, 443), timeout=15) as sock:
                with ctx.wrap_socket(sock, server_hostname=host) as tls:
                    cert = tls.getpeercert()
            names = {v for k, v in cert.get("subject", [()])[0]} if cert else set()
            alt = {v for t, v in cert.get("subjectAltName", ()) if t == "DNS"}
            expires = datetime.strptime(cert["notAfter"],
                                        "%b %d %H:%M:%S %Y %Z").replace(
                tzinfo=timezone.utc)
            days = (expires - datetime.now(timezone.utc)).days
            covered = host in alt or f"*.{domain}" in alt
            if covered:
                record(PASS, f"{host} certificate valid",
                       f"expires in {days} days")
            else:
                record(FAIL, f"{host} certificate does not cover this name",
                       f"covers: {', '.join(sorted(alt)) or names}")
        except ssl.SSLCertVerificationError as e:
            record(FAIL, f"{host} certificate not valid yet", str(e.verify_message
                   if hasattr(e, "verify_message") else e))
        except (socket.gaierror, socket.timeout, OSError) as e:
            record(FAIL, f"{host} TLS connection failed", str(e))


def check_one_canonical_host(domain):
    """The single most valuable SEO check here: both hosts must not serve
    the same pages. One has to redirect to the other, or the pages compete
    with themselves."""
    print("\nCanonical host")
    apex = f"https://{domain}/"
    www = f"https://www.{domain}/"

    a_status, a_head, _, _ = fetch(apex, redirect=False)
    w_status, w_head, _, _ = fetch(www, redirect=False)

    a_loc = a_head.get("Location", "")
    w_loc = w_head.get("Location", "")

    if a_status in (301, 308) and "www." in a_loc:
        record(PASS, "apex redirects to www", f"{a_status} -> {a_loc}")
        primary = www
    elif w_status in (301, 308) and "www." not in w_loc.replace(f"//www.", "//"):
        record(PASS, "www redirects to apex", f"{w_status} -> {w_loc}")
        primary = apex
    elif a_status == 200 and w_status == 200:
        record(FAIL, "both apex and www serve 200",
               "Two hosts serving the same pages split their ranking. Set a "
               "default domain in Webflow: Site Settings -> Publishing.")
        primary = www
    elif a_status in (302, 307) or w_status in (302, 307):
        record(WARN, "redirect is temporary, not permanent",
               f"apex={a_status} www={w_status}. A 301/308 passes ranking; a "
               f"302 does not.")
        primary = www if a_status else apex
    else:
        record(FAIL, "neither host answers normally",
               f"apex={a_status} www={w_status}")
        primary = www

    # http must reach https
    h_status, h_head, _, _ = fetch(f"http://{domain}/", redirect=False)
    if h_status in (301, 308) and h_head.get("Location", "").startswith("https"):
        record(PASS, "http redirects to https", f"{h_status}")
    elif h_status == 200:
        record(FAIL, "http serves content without redirecting to https",
               "Turn on SSL in Webflow: Site Settings -> Publishing.")
    else:
        record(WARN, "http behaviour unclear", f"status={h_status}")

    return primary.rstrip("/")


def check_pages(base):
    print(f"\nPages ({base})")
    pages = {}
    for path in PATHS:
        url = base + path
        status, _, body, final = fetch(url)
        if status == 200:
            pages[path] = (url, body, final)
            record(PASS, f"{path or '/'} returns 200")
        else:
            record(FAIL, f"{path or '/'} returns {status}",
                   "Webflow serves extensionless paths; check the page's slug.")
    return pages


def check_canonicals(pages, base):
    print("\nCanonical tags")
    for path, (url, body, final) in pages.items():
        m = re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', body) \
            or re.search(r'<link[^>]+href="([^"]+)"[^>]+rel="canonical"', body)
        if not m:
            record(FAIL, f"{path} has no canonical tag")
            continue
        canon = m.group(1).rstrip("/") or "/"
        want = (base + path).rstrip("/") or base
        if canon.rstrip("/") == want.rstrip("/"):
            record(PASS, f"{path} canonical is self-referential")
        else:
            record(FAIL, f"{path} canonical points elsewhere",
                   f"says {canon}, should be {want}. A canonical naming "
                   f"another URL tells Google the real page is there.")


def check_share_cards(pages):
    print("\nShare cards")
    seen = set()
    for path, (url, body, _) in pages.items():
        m = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', body)
        if not m:
            record(FAIL, f"{path} has no og:image")
            continue
        img = m.group(1)
        if not img.startswith("http"):
            record(FAIL, f"{path} og:image is a relative path",
                   f"'{img}'. Open Graph requires an absolute URL; every "
                   f"share card renders with no image and nothing warns you.")
            continue
        if img in seen:
            continue
        seen.add(img)
        status, head, _, _ = fetch(img, method="HEAD")
        ctype = head.get("Content-Type", "")
        if status == 200 and ctype.startswith("image/"):
            record(PASS, "og:image is reachable", f"{ctype} — {img}")
        else:
            record(FAIL, "og:image is not reachable",
                   f"status={status} type={ctype or 'none'} — {img}")

        mu = re.search(r'<meta[^>]+property="og:url"[^>]+content="([^"]+)"', body)
        if not mu:
            record(WARN, f"{path} has no og:url")


def check_robots_sitemap(base, domain):
    print("\nrobots.txt and sitemap")
    status, _, body, _ = fetch(f"{base}/robots.txt")
    if status == 200:
        record(PASS, "robots.txt served")
        sm = re.search(r"(?im)^\s*sitemap:\s*(\S+)", body)
        if sm:
            record(PASS, "robots.txt names a sitemap", sm.group(1))
        else:
            record(WARN, "robots.txt names no sitemap")
        if re.search(r"(?im)^\s*disallow:\s*/\s*$", body):
            record(FAIL, "robots.txt disallows the whole site",
                   "'Disallow: /' blocks every crawler.")
    else:
        record(WARN, "no robots.txt", f"status={status}")

    status, _, body, _ = fetch(f"{base}/sitemap.xml")
    if status == 200 and "<urlset" in body:
        locs = re.findall(r"<loc>([^<]+)</loc>", body)
        wrong = [l for l in locs if domain not in l]
        record(PASS, "sitemap.xml served", f"{len(locs)} URLs")
        if wrong:
            record(FAIL, "sitemap lists URLs on another domain",
                   ", ".join(wrong[:3]))
    else:
        record(FAIL, "no sitemap.xml",
               "Turn it on: Webflow Project Settings -> SEO -> Sitemap.")


def check_structured_data(pages):
    print("\nStructured data")
    for path, (_, body, _) in pages.items():
        blocks = re.findall(
            r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',
            body, re.S)
        if not blocks:
            record(WARN, f"{path} has no JSON-LD")
            continue
        types = []
        for b in blocks:
            try:
                o = json.loads(b)
            except json.JSONDecodeError as e:
                record(FAIL, f"{path} JSON-LD does not parse",
                       f"{e}. Google ignores the whole block.")
                break
            types.append(o.get("@type", "?"))
        else:
            record(PASS, f"{path} JSON-LD valid", ", ".join(map(str, types)))


def check_staging_not_indexed(staging):
    print("\nWebflow staging subdomain")
    if not staging:
        record(WARN, "staging subdomain not checked",
               "Pass --staging <name>.webflow.io to check it. If it is "
               "indexable it competes with the real site for the same words.")
        return
    url = f"https://{staging}/"
    status, head, body, _ = fetch(url)
    if status is None:
        record(PASS, "staging subdomain unreachable", staging)
        return
    robots_tag = head.get("X-Robots-Tag", "")
    meta = re.search(r'<meta[^>]+name="robots"[^>]+content="([^"]*)"', body)
    blocked = "noindex" in robots_tag.lower() or (
        meta and "noindex" in meta.group(1).lower())
    r_status, _, r_body, _ = fetch(f"https://{staging}/robots.txt")
    disallowed = r_status == 200 and re.search(r"(?im)^\s*disallow:\s*/\s*$", r_body)
    if blocked or disallowed:
        record(PASS, "staging subdomain is not indexable", staging)
    else:
        record(FAIL, "staging subdomain IS indexable",
               "Turn on 'Disable Webflow subdomain indexing' in Project "
               "Settings -> SEO, or it competes with the real site.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", default="jbowmanmusic.com")
    ap.add_argument("--staging", default=None,
                    help="e.g. j-bowman.webflow.io")
    args = ap.parse_args()

    print(f"Checking {args.domain}")
    check_dns(args.domain)
    if any(s == FAIL for s, c, _ in results if "resolve" in c):
        print("\nDNS is not resolving yet, so nothing below would be "
              "meaningful. Wait for propagation and run this again.")
        return 1

    check_tls(args.domain)
    base = check_one_canonical_host(args.domain)
    pages = check_pages(base)
    if pages:
        check_canonicals(pages, base)
        check_share_cards(pages)
        check_structured_data(pages)
    check_robots_sitemap(base, args.domain)
    check_staging_not_indexed(args.staging)

    failed = [r for r in results if r[0] == FAIL]
    warned = [r for r in results if r[0] == WARN]
    print(f"\n{'-' * 60}")
    print(f"{len(results) - len(failed) - len(warned)} passed, "
          f"{len(failed)} failed, {len(warned)} warnings")
    if failed:
        print("\nFailures:")
        for _, check, detail in failed:
            print(f"  - {check}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
