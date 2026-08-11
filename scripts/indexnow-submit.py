#!/usr/bin/env python3
"""
Submit zhouzk.com homepage URLs to IndexNow (Bing / Yandex / Naver / Seznam).

Reads sitemap.xml and submits:
  - default: URLs whose <lastmod> == today (changed pages)
  - --all:   every URL in the sitemap

Key resolution: env INDEXNOW_KEY first, then the documented active key in
AGENTS.md. The key file is public (served at /{key}.txt), so a hardcoded
fallback is fine; use the GitHub secret to rotate without editing code.
"""

import argparse
import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SITEMAP = ROOT / "sitemap.xml"
DEFAULT_KEY = os.environ.get("INDEXNOW_KEY") or "6eb66562bfae2661cfc2854418b6ae19"
HOST = "zhouzk.com"
ENDPOINT = "https://api.indexnow.org/indexnow"
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def load_urls(submit_all: bool) -> list:
    if not SITEMAP.exists():
        print(f"Error: sitemap not found: {SITEMAP}", file=sys.stderr)
        sys.exit(1)
    root = ET.parse(SITEMAP).getroot()
    today = date.today().isoformat()
    urls = []
    for url in root.findall("sm:url", NS):
        loc = url.findtext("sm:loc", "", NS).strip()
        lastmod = url.findtext("sm:lastmod", "", NS).strip()[:10]
        if submit_all or lastmod == today:
            urls.append(loc)
    return urls


def submit(key: str, urls: list) -> None:
    payload = {
        "host": HOST,
        "key": key,
        "keyLocation": f"https://{HOST}/{key}.txt",
        "urlList": urls,
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            print(f"OK {resp.status}: {body or '(accepted)'}")
            print(f"Submitted {len(urls)} URLs to {ENDPOINT}")
    except urllib.error.HTTPError as e:
        print(f"FAIL {e.code}: {e.read().decode('utf-8', errors='replace')}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Submit homepage URLs to IndexNow")
    parser.add_argument("--all", action="store_true", help="Submit every sitemap URL")
    parser.add_argument("--key", default=DEFAULT_KEY, help="IndexNow key")
    args = parser.parse_args()

    urls = load_urls(args.all)
    if not urls:
        print("No URLs with today's lastmod found — nothing to submit.")
        return
    submit(args.key, urls)


if __name__ == "__main__":
    main()
