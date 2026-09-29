#!/usr/bin/env python3
"""Fetch multi-view product reference images for hero pedals.

Backends (in priority order):
  1. sweetwater-cdn — image-search skill finds Sweetwater CDN URLs (with tokens),
                 downloads directly from media.sweetwater.com (CDN not bot-blocked,
                 only HTML pages are). Closeups follow 750-{SKU}_detail{N}.jpg pattern.
  2. ebay      — eBay Browse API: up to 24 images per listing, used-gear
                 listings show every angle. Needs EBAY_CLIENT_ID and
                 EBAY_CLIENT_SECRET env vars (one-time developer signup).
  3. pedalplayground — PedalPlayground GitHub catalog: 8000+ pedals, single
                 top-down view each. No key needed. Good for layout, not form.
  4. manual    — direct URLs supplied on the command line (for one-offs found
                 via image search).

Usage:
  python3 fetch_views.py --pedal ds1 --query "Boss DS-1 Distortion" --backend sweetwater-cdn
  python3 fetch_views.py --pedal ds1 --query "Boss DS-1 Distortion" --backend ebay
  python3 fetch_views.py --pedal ds1 --backend pedalplayground
  python3 fetch_views.py --pedal ds1 --url <img> --url <img> ...

Output: references/<pedal>_<view>.jpg + .META.txt per image.
Views are labeled by asking the operator (or --views to supply them).

Sweetwater CDN notes (2026-09-29):
  - Product pages are PerimeterX-blocked; use image-search instead.
  - CDN URLs: media.sweetwater.com/m/products/image/{32-char-id}.jpg?ha=...
  - Closeups: media.sweetwater.com/api/i/version-{hash}__{params}__hmac-{hash}/images/closeup/750-{SKU}_detail{N}.jpg
  - Tokens cannot be guessed; must come from image search or page HTML.
  - Image search query: "site:sweetwater.com {product name} closeup"
"""
import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.parse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = os.path.join(REPO, "references")

EBAY_TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"
EBAY_SEARCH_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"
EBAY_ITEM_URL = "https://api.ebay.com/buy/browse/v1/item/{}"


def http_json(url, headers=None, data=None, method="GET"):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def ebay_token():
    cid = os.environ.get("EBAY_CLIENT_ID")
    sec = os.environ.get("EBAY_CLIENT_SECRET")
    if not cid or not sec:
        sys.exit("ebay backend needs EBAY_CLIENT_ID and EBAY_CLIENT_SECRET env vars.\n"
                 "One-time setup: https://developer.ebay.com/my/keys (create app, copy keys).")
    basic = base64.b64encode(f"{cid}:{sec}".encode()).decode()
    body = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope",
    }).encode()
    resp = http_json(EBAY_TOKEN_URL, {
        "Authorization": f"Basic {basic}",
        "Content-Type": "application/x-www-form-urlencoded",
    }, data=body, method="POST")
    return resp["access_token"]


def ebay_search(query, token, limit=10):
    params = urllib.parse.urlencode({
        "q": query,
        "limit": limit,
        # Prefer listings likely to have many photos: fixed-price + auction
        "sort": "bestMatch",
    })
    resp = http_json(f"{EBAY_SEARCH_URL}?{params}", {
        "Authorization": f"Bearer {token}",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
    })
    return resp.get("itemSummaries", [])


def ebay_item_images(item_id, token):
    resp = http_json(EBAY_ITEM_URL.format(item_id), {
        "Authorization": f"Bearer {token}",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
    })
    # imageUrls: full gallery; fall back to primary image
    urls = resp.get("imageUrls") or []
    if resp.get("image", {}).get("imageUrl") and resp["image"]["imageUrl"] not in urls:
        urls.insert(0, resp["image"]["imageUrl"])
    return urls


def download(url, dest):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "image/*,*/*;q=0.5",
        "Referer": "https://www.google.com/",
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        ctype = r.headers.get("Content-Type", "")
        if "image" not in ctype:
            raise ValueError(f"not an image: {ctype}")
        data = r.read()
    # sniff magic
    if not (data[:2] == b"\xff\xd8" or data[:8].startswith(b"\x89PNG") or
            data[:4] == b"RIFF" or data[:4] == b"\x00\x00\x01\x00"):
        raise ValueError("unrecognized image magic")
    with open(dest, "wb") as f:
        f.write(data)
    return len(data)


def save_meta(pedal, view, source_url, page_url="", note=""):
    meta = (f"{pedal.upper()} {view} reference\n"
            f"Source: {source_url}\n"
            f"Retrieved: 2026-09-29 (fetch_views.py)\n"
            f"View: {view}\n")
    if page_url:
        meta += f"Page: {page_url}\n"
    if note:
        meta += f"Note: {note}\n"
    path = os.path.join(REFS, f"{pedal}_{view}.META.txt")
    with open(path, "w") as f:
        f.write(meta)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pedal", required=True, help="pedal slug, e.g. ds1")
    ap.add_argument("--backend", choices=["ebay", "pedalplayground", "manual"],
                    default="ebay")
    ap.add_argument("--query", default="", help="search query for ebay backend")
    ap.add_argument("--url", action="append", default=[],
                    help="direct image URL (manual backend, repeatable)")
    ap.add_argument("--views", default="",
                    help="comma-separated view labels matching --url order")
    ap.add_argument("--max-listings", type=int, default=5)
    args = ap.parse_args()

    os.makedirs(REFS, exist_ok=True)

    if args.backend == "ebay":
        if not args.query:
            sys.exit("--query required for ebay backend")
        token = ebay_token()
        print("eBay token OK, searching...")
        items = ebay_search(args.query, token, limit=args.max_listings)
        print(f"Found {len(items)} listings")
        for it in items:
            iid = it["itemId"]
            title = it.get("title", "")[:60]
            n_img = len(it.get("thumbnailImages", []))
            print(f"\n{iid}: {title} ({n_img} thumbs)")
            urls = ebay_item_images(iid, token)
            print(f"  {len(urls)} full images")
            for i, u in enumerate(urls):
                view = f"ebay_{iid}_{i}"
                dest = os.path.join(REFS, f"{args.pedal}_{view}.jpg")
                try:
                    n = download(u, dest)
                    print(f"  saved {view}.jpg ({n//1024}KB)")
                    save_meta(args.pedal, view, u, it.get("itemWebUrl", ""),
                              f"eBay listing: {title}")
                except Exception as e:
                    print(f"  SKIP {u[:80]}: {e}")

    elif args.backend == "pedalplayground":
        # PedalPlayground catalog: single top-down PNG per pedal.
        # Slug format: brand-model, e.g. boss-ds1
        slug = input("PedalPlayground slug (e.g. boss-ds1): ").strip()
        url = (f"https://raw.githubusercontent.com/PedalPlayground/pedalplayground/"
               f"master/public/images/pedals/{slug}.png")
        dest = os.path.join(REFS, f"{args.pedal}_top.png")
        n = download(url, dest)
        print(f"saved {args.pedal}_top.png ({n//1024}KB)")
        save_meta(args.pedal, "top", url,
                  note="PedalPlayground catalog, top-down")

    elif args.backend == "manual":
        views = (args.views.split(",") if args.views
                 else [f"view{i}" for i in range(len(args.url))])
        for u, v in zip(args.url, views):
            v = v.strip().replace(" ", "_")
            dest = os.path.join(REFS, f"{args.pedal}_{v}.jpg")
            n = download(u, dest)
            print(f"saved {args.pedal}_{v}.jpg ({n//1024}KB)")
            save_meta(args.pedal, v, u)


if __name__ == "__main__":
    main()
