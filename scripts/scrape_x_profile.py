#!/usr/bin/env python3
"""Scrape a public X profile without using the X API.

This script uses Playwright to render the public profile timeline, scrolls to
collect status URLs, then revisits each status page to extract:

- full post text
- timestamp
- inline/external links
- photo and thumbnail URLs
- basic engagement labels

Optional media downloading is supported for image URLs exposed in the DOM.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


X_BASE = "https://x.com"
TAB_PATHS = {
    "posts": "",
    "replies": "/with_replies",
    "media": "/media",
}

TIMELINE_JS = r"""
() => {
  const asAbsolute = (value) => {
    if (!value) return null;
    try {
      return new URL(value, window.location.origin).href;
    } catch {
      return value;
    }
  };

  const articles = Array.from(document.querySelectorAll('article[data-testid="tweet"]'));
  if (articles.length) {
    return articles.map((article) => {
      const timeAnchor = article.querySelector('a[href*="/status/"] time')?.parentElement;
      const socialContext = article.querySelector('[data-testid="socialContext"]')?.innerText || '';
      const replyTo = Array.from(article.querySelectorAll('div[data-testid="User-Name"] a[href^="/"]'))
        .map((a) => a.getAttribute('href'))
        .filter(Boolean);
      return {
        status_url: asAbsolute(timeAnchor?.getAttribute('href')),
        created_at: article.querySelector('time')?.dateTime || null,
        preview_text: article.querySelector('[data-testid="tweetText"]')?.innerText || '',
        is_pinned: /pinned/i.test(socialContext),
        visible_image_urls: Array.from(article.querySelectorAll('img[src*="pbs.twimg.com/"]'))
          .map((img) => img.getAttribute('src'))
          .filter((src) => /pbs\.twimg\.com\/(media|ext_tw_video_thumb|amplify_video_thumb|tweet_video_thumb)\//.test(src))
          .filter(Boolean),
        visible_links: Array.from(article.querySelectorAll('[data-testid="tweetText"] a[href]'))
          .map((a) => asAbsolute(a.getAttribute('href')))
          .filter(Boolean),
        conversation_context: replyTo,
      };
    });
  }

  const cells = Array.from(document.querySelectorAll('[data-testid="cellInnerDiv"]'));
  const seen = new Map();
  for (const cell of cells) {
    const anchors = Array.from(cell.querySelectorAll('a[href*="/status/"]'));
    const statusLinks = anchors
      .map((a) => a.getAttribute('href'))
      .filter(Boolean)
      .map((href) => href.replace(/\/analytics$/, '').replace(/\/photo\/\d+$/, ''))
      .filter((href) => /\/status\/\d+$/.test(href));
    for (const href of statusLinks) {
      const statusUrl = asAbsolute(href);
      if (!statusUrl || seen.has(statusUrl)) {
        continue;
      }
      seen.set(statusUrl, {
        status_url: statusUrl,
        created_at: null,
        preview_text: '',
        is_pinned: false,
        visible_image_urls: Array.from(cell.querySelectorAll('img[src*="pbs.twimg.com/"]'))
          .map((img) => img.getAttribute('src'))
          .filter((src) => /pbs\.twimg\.com\/(media|ext_tw_video_thumb|amplify_video_thumb|tweet_video_thumb)\//.test(src))
          .filter(Boolean),
        visible_links: [],
        conversation_context: [],
      });
    }
  }
  return Array.from(seen.values());
}
"""

DETAIL_JS = r"""
(targetUrl) => {
  const normalize = (value) => {
    if (!value) return null;
    try {
      const absolute = new URL(value, window.location.origin).href;
      return absolute.replace(/\/analytics$/, '');
    } catch {
      return value;
    }
  };

  const target = normalize(targetUrl);
  const articles = Array.from(document.querySelectorAll('article[data-testid="tweet"]'));
  let article = articles.find((node) => {
    const hrefs = Array.from(node.querySelectorAll('a[href*="/status/"]'))
      .map((anchor) => normalize(anchor.getAttribute('href')))
      .filter(Boolean)
      .map((href) => href.replace(/\/analytics$/, '').replace(/\/photo\/\d+$/, ''));
    return hrefs.includes(target);
  });
  if (!article) {
    article = articles[0] || null;
  }
  if (!article) {
    return null;
  }

  const asAbsolute = (value) => {
    if (!value) return null;
    try {
      return new URL(value, window.location.origin).href;
    } catch {
      return value;
    }
  };

  const tweetText = article.querySelector('[data-testid="tweetText"]');
  const metricsLabel = article.querySelector('[role="group"][aria-label]')?.getAttribute('aria-label') || null;
  const userName = article.querySelector('[data-testid="User-Name"]');
  const handleNode = Array.from(userName?.querySelectorAll('span') || []).find((node) =>
    (node.innerText || '').trim().startsWith('@')
  ) || null;
  const timeNode = article.querySelector('time');
  const displayNameNode = Array.from(userName?.querySelectorAll('a[href^="/"]') || []).find((node) => {
    const text = (node.innerText || '').trim();
    return text && !text.startsWith('@');
  }) || null;

  const rawImages = Array.from(article.querySelectorAll('img[src*="pbs.twimg.com/"]'))
    .map((img) => img.getAttribute('src'))
    .filter(Boolean);

  const mediaUrls = rawImages.filter((src) =>
    /pbs\.twimg\.com\/(media|ext_tw_video_thumb|amplify_video_thumb|tweet_video_thumb)\//.test(src)
  );

  const allAnchors = Array.from(article.querySelectorAll('a[href]')).map((a) => ({
    href: asAbsolute(a.getAttribute('href')),
    text: a.innerText || '',
  })).filter((item) => item.href);

  return {
    status_url: target,
    created_at: timeNode?.dateTime || null,
    display_time: timeNode?.innerText || null,
    display_name: displayNameNode?.innerText || null,
    handle: handleNode?.innerText || null,
    text: tweetText?.innerText || '',
    text_links: Array.from(tweetText?.querySelectorAll('a[href]') || []).map((a) => ({
      href: asAbsolute(a.getAttribute('href')),
      text: a.innerText || '',
    })).filter((item) => item.href),
    all_links: allAnchors,
    media_urls: mediaUrls,
    metrics_label: metricsLabel,
    article_text: article.innerText || '',
  };
}
"""


class TabUnavailableError(RuntimeError):
    """Raised when a profile tab is not publicly accessible to a guest session."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape a public X profile without using the X API."
    )
    parser.add_argument("handle", help="Profile handle, with or without '@'.")
    parser.add_argument(
        "--tab",
        dest="tabs",
        action="append",
        choices=sorted(TAB_PATHS),
        help="Timeline tab(s) to scrape. Default: posts",
    )
    parser.add_argument(
        "--max-scrolls",
        type=int,
        default=400,
        help="Maximum scroll steps per tab. Default: 400",
    )
    parser.add_argument(
        "--idle-scrolls",
        type=int,
        default=10,
        help="Stop a tab after this many scrolls with no new statuses. Default: 10",
    )
    parser.add_argument(
        "--scroll-delay-ms",
        type=int,
        default=2000,
        help="Delay after each scroll in milliseconds. Default: 2000",
    )
    parser.add_argument(
        "--status-limit",
        type=int,
        default=0,
        help="Maximum number of statuses to revisit. 0 means no limit.",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("artifacts/x-scrape"),
        help="Output directory root. Default: artifacts/x-scrape",
    )
    parser.add_argument(
        "--cookies-file",
        type=Path,
        default=Path("secrets/x-cookies.json"),
        help="Optional JSON cookie file for an authenticated X session. Default: secrets/x-cookies.json",
    )
    parser.add_argument(
        "--download-media",
        action="store_true",
        help="Download discovered image/media thumbnails into the output bundle.",
    )
    parser.add_argument(
        "--headful",
        action="store_true",
        help="Run Chromium in headed mode for debugging.",
    )
    return parser.parse_args()


def normalize_handle(handle: str) -> str:
    return handle.lstrip("@").strip()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def profile_url(handle: str, tab: str = "posts") -> str:
    return f"{X_BASE}/{handle}{TAB_PATHS[tab]}"


def normalize_media_url(url: str) -> str:
    if not url or "pbs.twimg.com/" not in url:
        return url
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    if "/media/" in parts.path:
        query["name"] = "orig"
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def infer_extension(url: str) -> str:
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    if "format" in query:
        return f".{query['format']}"
    suffix = Path(parts.path).suffix
    return suffix or ".bin"


def safe_stem(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-")
    return cleaned or "item"


def is_internal_x_link(url: str) -> bool:
    lowered = url.lower()
    return lowered.startswith("https://x.com/") or lowered.startswith("https://twitter.com/")


def is_meaningful_article_link(status_url: str, href: str, handle: str) -> bool:
    normalized_status = status_url.rstrip("/")
    normalized_href = href.rstrip("/")
    handle_root = f"{X_BASE}/{handle}".rstrip("/")
    if normalized_href == handle_root:
        return False
    if normalized_href == normalized_status:
        return False
    if normalized_href.startswith(f"{normalized_status}/analytics"):
        return False
    if re.search(r"/photo/\d+$", normalized_href):
        return False
    return True


def clean_string(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.replace("\xa0", " ").replace("\r\n", "\n").strip()
    cleaned = cleaned.replace("\u00c2\u00b7", "\u00b7")
    return cleaned


def clean_payload(payload: Any) -> Any:
    if isinstance(payload, dict):
        return {key: clean_payload(value) for key, value in payload.items()}
    if isinstance(payload, list):
        return [clean_payload(item) for item in payload]
    if isinstance(payload, str):
        return clean_string(payload)
    return payload


def load_x_cookies(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.exists():
        return []

    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        cookies: list[dict[str, Any]] = []
        for item in data:
            if not isinstance(item, dict) or "name" not in item or "value" not in item:
                continue
            cookie = {
                "name": item["name"],
                "value": item["value"],
                "domain": item.get("domain", ".x.com"),
                "path": item.get("path", "/"),
                "secure": bool(item.get("secure", True)),
                "httpOnly": bool(item.get("httpOnly", False)),
            }
            if item.get("sameSite") in {"Lax", "None", "Strict"}:
                cookie["sameSite"] = item["sameSite"]
            if item.get("expires"):
                cookie["expires"] = item["expires"]
            cookies.append(cookie)
        return cookies

    if isinstance(data, dict):
        cookies = []
        auth_token = data.get("auth_token")
        ct0 = data.get("ct0")
        if auth_token:
            cookies.append(
                {
                    "name": "auth_token",
                    "value": auth_token,
                    "domain": ".x.com",
                    "path": "/",
                    "secure": True,
                    "httpOnly": True,
                    "sameSite": "Lax",
                }
            )
        if ct0:
            cookies.append(
                {
                    "name": "ct0",
                    "value": ct0,
                    "domain": ".x.com",
                    "path": "/",
                    "secure": True,
                    "httpOnly": False,
                    "sameSite": "Lax",
                }
            )
        return cookies

    raise ValueError(f"unsupported cookie file format in {path}")


def flatten_links(posts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for post in posts:
        seen: set[tuple[str, str]] = set()
        handle = (post.get("handle") or "").lstrip("@")
        for entry in post.get("text_links", []):
            href = entry.get("href") or ""
            key = ("text", href)
            if href and key not in seen:
                rows.append(
                    {
                        "status_id": post.get("status_id"),
                        "status_url": post.get("status_url"),
                        "link_context": "text",
                        "link_text": entry.get("text") or "",
                        "href": href,
                        "is_external": not is_internal_x_link(href),
                    }
                )
                seen.add(key)
        for entry in post.get("all_links", []):
            href = entry.get("href") or ""
            if not href:
                continue
            if not is_meaningful_article_link(post.get("status_url") or "", href, handle):
                continue
            key = ("all", href)
            if key in seen:
                continue
            rows.append(
                {
                    "status_id": post.get("status_id"),
                    "status_url": post.get("status_url"),
                    "link_context": "article",
                    "link_text": entry.get("text") or "",
                    "href": href,
                    "is_external": not is_internal_x_link(href),
                }
            )
            seen.add(key)
    return rows


def flatten_media(posts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for post in posts:
        for media_url in post.get("media_urls", []):
            rows.append(
                {
                    "status_id": post.get("status_id"),
                    "status_url": post.get("status_url"),
                    "media_url": media_url,
                    "normalized_media_url": normalize_media_url(media_url),
                }
            )
    return rows


def extract_status_id(status_url: str) -> str | None:
    match = re.search(r"/status/(\d+)", status_url)
    return match.group(1) if match else None


def scrape_profile_metadata(page, handle: str) -> dict[str, Any]:
    page.goto(profile_url(handle), wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(4000)
    avatar = page.locator('img[src*="profile_images"]').first
    banner = page.locator('a[href$="/header_photo"] img').first
    metadata = {
        "handle": handle,
        "url": profile_url(handle),
        "title": page.title(),
        "display_name": page.locator('main [data-testid="UserName"] div[dir="ltr"]').first.inner_text()
        if page.locator('main [data-testid="UserName"] div[dir="ltr"]').count()
        else None,
        "bio": page.locator('main [data-testid="UserDescription"]').first.inner_text()
        if page.locator('main [data-testid="UserDescription"]').count()
        else None,
        "avatar_url": avatar.get_attribute("src") if avatar.count() else None,
        "banner_url": banner.get_attribute("src") if banner.count() else None,
    }
    return clean_payload(metadata)


def page_looks_missing(page) -> bool:
    title = page.title().lower()
    if "page not found" in title:
        return True
    body_text = page.locator("body").inner_text(timeout=10000)
    missing_markers = [
        "Hmm...this page doesn’t exist.",
        "Hmm...this page doesn't exist.",
        "Try searching for something else.",
    ]
    return any(marker in body_text for marker in missing_markers)


def page_needs_retry(page) -> bool:
    body_text = page.locator("body").inner_text(timeout=10000)
    retry_markers = [
        "Something went wrong. Try reloading.",
        "Retry",
        "Rate limit exceeded",
        "This page is down",
    ]
    return any(marker in body_text for marker in retry_markers)


def wait_for_detail_content(page, timeout_ms: int = 25000) -> None:
    deadline = time.time() + (timeout_ms / 1000)
    while time.time() < deadline:
        article_count = page.locator('article[data-testid="tweet"]').count()
        status_link_count = page.locator('a[href*="/status/"]').count()
        if article_count or status_link_count:
            return
        if page_looks_missing(page):
            raise TabUnavailableError("tweet page resolved to a missing-page shell")
        page.wait_for_timeout(1000)
    raise PlaywrightTimeoutError("Timed out waiting for tweet/status content to render")


def open_timeline_tab(page, handle: str, tab: str) -> None:
    url = profile_url(handle, tab)
    print(f"[timeline] opening {url}", flush=True)
    page.goto(url, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(4000)
    if tab != "posts" and page_looks_missing(page):
        raise TabUnavailableError(
            f"guest access to the '{tab}' tab is blocked or unavailable at {url}"
        )


def collect_statuses_from_tab(page, handle: str, tab: str, max_scrolls: int, idle_scrolls: int, delay_ms: int) -> dict[str, dict[str, Any]]:
    open_timeline_tab(page, handle, tab)
    try:
        if tab == "media":
            page.wait_for_selector('article[data-testid="tweet"], [data-testid="cellInnerDiv"] a[href*="/status/"]', timeout=15000)
        else:
            page.wait_for_selector('article[data-testid="tweet"]', timeout=15000)
    except PlaywrightTimeoutError as exc:
        if page_looks_missing(page):
            raise TabUnavailableError(
                f"guest access to the '{tab}' tab is blocked or unavailable"
            ) from exc
        raise
    page.wait_for_timeout(2000)

    collected: dict[str, dict[str, Any]] = {}
    idle_count = 0

    for step in range(max_scrolls):
        before = len(collected)
        visible = page.evaluate(TIMELINE_JS)
        for item in visible:
            status_url = item.get("status_url")
            if not status_url:
                continue
            record = collected.setdefault(
                status_url,
                {
                    "status_url": status_url,
                    "status_id": extract_status_id(status_url),
                    "created_at": item.get("created_at"),
                    "preview_text": item.get("preview_text") or "",
                    "source_tabs": [],
                    "is_pinned": bool(item.get("is_pinned")),
                    "visible_links": [],
                    "visible_image_urls": [],
                },
            )
            if tab not in record["source_tabs"]:
                record["source_tabs"].append(tab)
            if item.get("created_at") and not record.get("created_at"):
                record["created_at"] = item["created_at"]
            if item.get("preview_text") and len(item["preview_text"]) > len(record.get("preview_text", "")):
                record["preview_text"] = item["preview_text"]
            record["is_pinned"] = record["is_pinned"] or bool(item.get("is_pinned"))
            for link in item.get("visible_links", []):
                if link not in record["visible_links"]:
                    record["visible_links"].append(link)
            for image_url in item.get("visible_image_urls", []):
                if image_url not in record["visible_image_urls"]:
                    record["visible_image_urls"].append(image_url)

        if len(collected) == before:
            idle_count += 1
        else:
            idle_count = 0

        print(
            f"[timeline] tab={tab} step={step + 1} statuses={len(collected)} idle={idle_count}",
            flush=True,
        )

        if idle_count >= idle_scrolls:
            break

        page.mouse.wheel(0, 6000)
        page.wait_for_timeout(delay_ms)

    return collected


def scrape_status(detail_page, status_url: str) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(1, 4):
        try:
            detail_page.goto(status_url, wait_until="domcontentloaded", timeout=120000)
            wait_for_detail_content(detail_page, timeout_ms=25000)
            detail_page.wait_for_timeout(2500 + (attempt - 1) * 1500)

            payload = detail_page.evaluate(DETAIL_JS, status_url)
            if not payload:
                raise RuntimeError(f"could not find target tweet in conversation for {status_url}")

            payload = clean_payload(payload)
            payload["status_id"] = extract_status_id(status_url)
            payload["media_urls"] = [normalize_media_url(url) for url in payload.get("media_urls", [])]
            payload["external_links"] = [
                entry
                for entry in payload.get("all_links", [])
                if entry.get("href") and not is_internal_x_link(entry["href"])
            ]
            return payload
        except (PlaywrightError, PlaywrightTimeoutError, RuntimeError) as exc:
            last_error = exc
            print(
                f"[detail] retry {attempt}/3 for {status_url}: {exc}",
                file=sys.stderr,
                flush=True,
            )
            if attempt == 3:
                break
            try:
                if page_needs_retry(detail_page):
                    detail_page.reload(wait_until="domcontentloaded", timeout=120000)
                    detail_page.wait_for_timeout(3000 * attempt)
            except Exception:
                pass
            detail_page.wait_for_timeout(3000 * attempt)

    raise RuntimeError(str(last_error) if last_error else f"failed to scrape {status_url}")


def download_media(rows: list[dict[str, Any]], media_dir: Path) -> list[dict[str, Any]]:
    ensure_dir(media_dir)
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            )
        }
    )

    downloads: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        url = row["normalized_media_url"]
        status_id = row.get("status_id") or "unknown"
        stem = safe_stem(f"{status_id}-{index}")
        target = media_dir / f"{stem}{infer_extension(url)}"
        try:
            with session.get(url, timeout=60, stream=True) as response:
                response.raise_for_status()
                with target.open("wb") as fh:
                    for chunk in response.iter_content(chunk_size=65536):
                        if chunk:
                            fh.write(chunk)
            downloads.append(
                {
                    "status_id": status_id,
                    "status_url": row.get("status_url"),
                    "source_url": url,
                    "local_path": str(target),
                }
            )
            print(f"[media] downloaded {target.name}", flush=True)
        except requests.RequestException as exc:
            print(f"[media] failed {url}: {exc}", file=sys.stderr, flush=True)
    return downloads


def main() -> int:
    args = parse_args()
    handle = normalize_handle(args.handle)
    tabs = args.tabs or ["posts"]
    cookies = load_x_cookies(args.cookies_file)

    run_dir = args.outdir / handle / time.strftime("%Y%m%d-%H%M%S")
    ensure_dir(run_dir)

    print(f"[setup] output -> {run_dir}", flush=True)
    print(f"[setup] tabs -> {', '.join(tabs)}", flush=True)
    if cookies:
        print(f"[setup] using authenticated session from {args.cookies_file}", flush=True)

    errors: list[dict[str, str]] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=not args.headful)
        context = browser.new_context(viewport={"width": 1440, "height": 2400})
        if cookies:
            context.add_cookies(cookies)
        timeline_page = context.new_page()
        detail_page = context.new_page()

        try:
            profile = scrape_profile_metadata(timeline_page, handle)
            write_json(run_dir / "profile.json", profile)
            print(f"[profile] {profile.get('title')}", flush=True)

            collected: dict[str, dict[str, Any]] = {}
            for tab in tabs:
                try:
                    tab_records = collect_statuses_from_tab(
                        timeline_page,
                        handle,
                        tab,
                        max_scrolls=args.max_scrolls,
                        idle_scrolls=args.idle_scrolls,
                        delay_ms=args.scroll_delay_ms,
                    )
                except TabUnavailableError as exc:
                    print(f"[timeline] skipping tab '{tab}': {exc}", flush=True)
                    continue
                for status_url, record in tab_records.items():
                    merged = collected.setdefault(status_url, record)
                    if merged is not record:
                        for source_tab in record.get("source_tabs", []):
                            if source_tab not in merged["source_tabs"]:
                                merged["source_tabs"].append(source_tab)
                        for link in record.get("visible_links", []):
                            if link not in merged["visible_links"]:
                                merged["visible_links"].append(link)
                        for image_url in record.get("visible_image_urls", []):
                            if image_url not in merged["visible_image_urls"]:
                                merged["visible_image_urls"].append(image_url)
                        if record.get("preview_text") and len(record["preview_text"]) > len(merged.get("preview_text", "")):
                            merged["preview_text"] = record["preview_text"]
                        merged["is_pinned"] = merged["is_pinned"] or record.get("is_pinned", False)

            status_queue = list(collected.values())
            status_queue.sort(key=lambda item: (item.get("created_at") or "", item.get("status_id") or ""))
            if args.status_limit > 0:
                status_queue = status_queue[: args.status_limit]

            write_json(run_dir / "timeline-index.json", status_queue)
            print(f"[timeline] collected {len(status_queue)} statuses for detail scrape", flush=True)

            posts: list[dict[str, Any]] = []
            for index, item in enumerate(status_queue, start=1):
                status_url = item["status_url"]
                try:
                    detail = scrape_status(detail_page, status_url)
                    detail["source_tabs"] = item.get("source_tabs", [])
                    detail["preview_text"] = item.get("preview_text", "")
                    detail["is_pinned"] = item.get("is_pinned", False)
                    detail["visible_links"] = item.get("visible_links", [])
                    detail["visible_image_urls"] = [normalize_media_url(url) for url in item.get("visible_image_urls", [])]
                    posts.append(detail)
                    print(
                        f"[detail] {index}/{len(status_queue)} {detail.get('status_id')} "
                        f"links={len(detail.get('all_links', []))} media={len(detail.get('media_urls', []))}",
                        flush=True,
                    )
                except (PlaywrightError, PlaywrightTimeoutError, RuntimeError) as exc:
                    errors.append({"status_url": status_url, "error": str(exc)})
                    print(f"[detail] failed {status_url}: {exc}", file=sys.stderr, flush=True)

        finally:
            context.close()
            browser.close()

    links = flatten_links(posts)
    media = flatten_media(posts)
    downloads: list[dict[str, Any]] = []

    write_json(run_dir / "posts.json", posts)
    write_json(run_dir / "links.json", links)
    write_json(run_dir / "media.json", media)
    write_json(run_dir / "errors.json", errors)

    write_csv(
        run_dir / "links.csv",
        links,
        fieldnames=["status_id", "status_url", "link_context", "link_text", "href", "is_external"],
    )
    write_csv(
        run_dir / "media.csv",
        media,
        fieldnames=["status_id", "status_url", "media_url", "normalized_media_url"],
    )

    if args.download_media and media:
        downloads = download_media(media, run_dir / "downloaded-media")
        write_json(run_dir / "downloads.json", downloads)

    summary = {
        "handle": handle,
        "run_dir": str(run_dir),
        "tabs": tabs,
        "post_count": len(posts),
        "link_count": len(links),
        "media_count": len(media),
        "download_count": len(downloads),
        "error_count": len(errors),
    }
    write_json(run_dir / "summary.json", summary)

    print("[done]", json.dumps(summary, indent=2), flush=True)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
