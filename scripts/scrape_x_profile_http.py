#!/usr/bin/env python3
"""Scrape a public X profile through the web client's GraphQL endpoints."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests


X_BASE = "https://x.com"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/135.0.0.0 Safari/537.36"
)
TAB_CONFIG = {
    "posts": {"path": "", "operation": "UserTweets"},
    "replies": {"path": "/with_replies", "operation": "UserTweetsAndReplies"},
    "media": {"path": "/media", "operation": "UserMedia"},
}
DISCOVERY_OPERATIONS = {
    "UserByScreenName",
    "UserTweets",
    "UserTweetsAndReplies",
    "UserMedia",
}


class XScrapeError(RuntimeError):
    """Raised when the X web flow cannot be scraped successfully."""


class TabUnavailableError(XScrapeError):
    """Raised when a requested timeline tab is unavailable."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape a public X profile without Playwright."
    )
    parser.add_argument("handle", help="Profile handle, with or without '@'.")
    parser.add_argument(
        "--tab",
        dest="tabs",
        action="append",
        choices=sorted(TAB_CONFIG),
        help="Timeline tab(s) to scrape. Default: posts",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=400,
        help="Maximum GraphQL page requests per tab. Default: 400",
    )
    parser.add_argument(
        "--max-scrolls",
        type=int,
        help="Backward-compatible alias for --max-pages.",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=40,
        help="Requested item count per timeline page. Default: 40",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=2.0,
        help="Delay between timeline page requests. Default: 2.0",
    )
    parser.add_argument(
        "--scroll-delay-ms",
        type=int,
        help="Backward-compatible alias for --sleep-seconds.",
    )
    parser.add_argument(
        "--status-limit",
        type=int,
        default=0,
        help="Maximum number of final statuses to write. 0 means no limit.",
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
    return f"{X_BASE}/{handle}{TAB_CONFIG[tab]['path']}"


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
    lowered = (url or "").lower()
    return lowered.startswith("https://x.com/") or lowered.startswith("https://twitter.com/")


def is_meaningful_article_link(status_url: str, href: str, handle: str) -> bool:
    normalized_status = (status_url or "").rstrip("/")
    normalized_href = (href or "").rstrip("/")
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


def compact_json(value: Any) -> str:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)


def extract_status_id(status_url: str) -> str | None:
    match = re.search(r"/status/(\d+)", status_url or "")
    return match.group(1) if match else None


def parse_x_datetime(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return parsedate_to_datetime(value).isoformat()
    except (TypeError, ValueError, IndexError):
        return None


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
            }
            cookies.append(cookie)
        return cookies

    if isinstance(data, dict):
        cookies = []
        if data.get("auth_token"):
            cookies.append(
                {
                    "name": "auth_token",
                    "value": data["auth_token"],
                    "domain": ".x.com",
                    "path": "/",
                }
            )
        if data.get("ct0"):
            cookies.append(
                {
                    "name": "ct0",
                    "value": data["ct0"],
                    "domain": ".x.com",
                    "path": "/",
                }
            )
        return cookies

    raise ValueError(f"unsupported cookie file format in {path}")


def build_session(cookies: list[dict[str, Any]]) -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "user-agent": DEFAULT_USER_AGENT,
            "accept-language": "en-US,en;q=0.9",
        }
    )
    for cookie in cookies:
        session.cookies.set(
            cookie["name"],
            cookie["value"],
            domain=cookie.get("domain", ".x.com"),
            path=cookie.get("path", "/"),
        )
    return session


def fetch_profile_html(session: requests.Session, handle: str) -> str:
    response = session.get(
        profile_url(handle),
        timeout=60,
        headers={
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "referer": X_BASE,
        },
    )
    response.raise_for_status()
    return response.text


def discover_client_config(session: requests.Session, html: str) -> tuple[str, dict[str, str]]:
    script_urls = re.findall(
        r"https://abs\.twimg\.com/responsive-web/client-web/[^\"']+\.js",
        html,
    )
    script_urls = list(dict.fromkeys(script_urls))
    if not script_urls:
        raise XScrapeError("could not locate X web client bundles in profile HTML")

    bearer_token: str | None = None
    operations: dict[str, str] = {}
    operation_pattern = re.compile(
        r'queryId:"(?P<query_id>[^"]+)",operationName:"(?P<name>[^"]+)",operationType:"query"'
    )

    for script_url in script_urls:
        response = session.get(script_url, timeout=60)
        response.raise_for_status()
        source = response.text

        if bearer_token is None:
            match = re.search(r'Bearer (AAAAA[\w%\-]{20,})', source)
            if match:
                bearer_token = match.group(1)

        for match in operation_pattern.finditer(source):
            name = match.group("name")
            if name in DISCOVERY_OPERATIONS and name not in operations:
                operations[name] = match.group("query_id")

        if bearer_token and DISCOVERY_OPERATIONS.issubset(operations):
            break

    if not bearer_token:
        raise XScrapeError("could not discover the current X bearer token")

    missing = DISCOVERY_OPERATIONS - operations.keys()
    if missing:
        raise XScrapeError(
            f"could not discover all required GraphQL operations: {', '.join(sorted(missing))}"
        )

    return bearer_token, operations


def extract_guest_token(session: requests.Session, html: str) -> str | None:
    token = session.cookies.get("gt", domain=".x.com") or session.cookies.get("gt")
    if token:
        return token
    match = re.search(r"gt=([0-9]+)", html)
    return match.group(1) if match else None


def build_graphql_headers(
    session: requests.Session,
    handle: str,
    bearer_token: str,
    html: str,
) -> dict[str, str]:
    headers = {
        "authorization": f"Bearer {bearer_token}",
        "x-twitter-active-user": "yes",
        "x-twitter-client-language": "en",
        "referer": profile_url(handle),
    }

    auth_token = session.cookies.get("auth_token", domain=".x.com") or session.cookies.get("auth_token")
    ct0 = session.cookies.get("ct0", domain=".x.com") or session.cookies.get("ct0")
    if auth_token and ct0:
        headers["x-csrf-token"] = ct0
        headers["x-twitter-auth-type"] = "OAuth2Session"
        return headers

    guest_token = extract_guest_token(session, html)
    if not guest_token:
        raise XScrapeError("could not discover a guest token for unauthenticated requests")
    headers["x-guest-token"] = guest_token
    return headers


def graphql_get(
    session: requests.Session,
    headers: dict[str, str],
    operations: dict[str, str],
    operation_name: str,
    variables: dict[str, Any],
    *,
    features: dict[str, Any] | None = None,
    field_toggles: dict[str, Any] | None = None,
    max_attempts: int = 8,
) -> dict[str, Any]:
    query_id = operations.get(operation_name)
    if not query_id:
        raise XScrapeError(f"missing query id for operation {operation_name}")

    url = f"{X_BASE}/i/api/graphql/{query_id}/{operation_name}"
    params = {
        "variables": compact_json(variables),
        "features": compact_json(features or {}),
    }
    if field_toggles:
        params["fieldToggles"] = compact_json(field_toggles)

    last_error: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            response = session.get(url, headers=headers, params=params, timeout=60)
            if response.status_code == 404:
                raise TabUnavailableError(
                    f"{operation_name} is unavailable with query id {query_id}"
                )
            if response.status_code == 429:
                reset_at = response.headers.get("x-rate-limit-reset")
                wait_seconds = 60 * attempt
                if reset_at and reset_at.isdigit():
                    # X limits usually reset every 15 minutes; do not cap the wait time
                    wait_seconds = max(5, int(reset_at) - int(time.time()) + 5)
                print(
                    f"[rate-limit] {operation_name} hit HTTP 429; sleeping {wait_seconds}s",
                    flush=True,
                )
                time.sleep(wait_seconds)
                last_error = XScrapeError(
                    f"{operation_name} returned transient HTTP 429"
                )
                continue
            if response.status_code in {500, 502, 503, 504}:
                wait_seconds = min(60, attempt * 5)
                time.sleep(wait_seconds)
                last_error = XScrapeError(
                    f"{operation_name} returned transient HTTP {response.status_code}"
                )
                continue
            response.raise_for_status()
            payload = response.json()
            if payload.get("errors") and not payload.get("data"):
                raise XScrapeError(
                    f"{operation_name} returned errors: {compact_json(payload['errors'])}"
                )
            return payload
        except (requests.RequestException, ValueError, XScrapeError) as exc:
            last_error = exc
            if isinstance(exc, TabUnavailableError):
                raise
            if attempt == max_attempts:
                break
            time.sleep(min(8, attempt * 2))

    raise XScrapeError(str(last_error) if last_error else f"{operation_name} failed")


def unwrap_tweet_result(result: Any) -> dict[str, Any] | None:
    current = result
    while isinstance(current, dict):
        typename = current.get("__typename")
        if typename == "Tweet":
            return current
        if typename == "TweetWithVisibilityResults":
            current = current.get("tweet")
            continue
        if typename in {"TweetTombstone", "TweetUnavailable"}:
            return None
        if "tweet" in current and isinstance(current["tweet"], dict):
            current = current["tweet"]
            continue
        if current.get("legacy") and current.get("rest_id"):
            return current
        return None
    return None


def iter_tweets_from_entry(entry: dict[str, Any]) -> list[dict[str, Any]]:
    content = entry.get("content") or {}
    results: list[dict[str, Any]] = []

    direct = content.get("itemContent", {}).get("tweet_results", {}).get("result")
    tweet = unwrap_tweet_result(direct)
    if tweet:
        results.append(tweet)

    for item in content.get("items", []) or []:
        tweet_result = (
            item.get("item", {})
            .get("itemContent", {})
            .get("tweet_results", {})
            .get("result")
        )
        tweet = unwrap_tweet_result(tweet_result)
        if tweet:
            results.append(tweet)

    return results


def extract_bottom_cursor(payload: dict[str, Any]) -> str | None:
    instructions = (
        payload.get("data", {})
        .get("user", {})
        .get("result", {})
        .get("timeline", {})
        .get("timeline", {})
        .get("instructions", [])
    )
    entries: list[dict[str, Any]] = []
    for instruction in instructions:
        entries.extend(instruction.get("entries", []))
        if "entry" in instruction:
            entries.append(instruction["entry"])

    for entry in entries:
        content = entry.get("content") or {}
        if content.get("__typename") == "TimelineTimelineCursor" and content.get("cursorType") == "Bottom":
            return content.get("value")
    return None


def extract_tweets(payload: dict[str, Any]) -> list[dict[str, Any]]:
    instructions = (
        payload.get("data", {})
        .get("user", {})
        .get("result", {})
        .get("timeline", {})
        .get("timeline", {})
        .get("instructions", [])
    )
    entries: list[dict[str, Any]] = []
    for instruction in instructions:
        entries.extend(instruction.get("entries", []))
        if "entry" in instruction:
            entries.append(instruction["entry"])

    tweets: list[dict[str, Any]] = []
    for entry in entries:
        tweets.extend(iter_tweets_from_entry(entry))
    return tweets


def extract_entity_links(entity_set: dict[str, Any] | None) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    if not isinstance(entity_set, dict):
        return links

    for url in entity_set.get("urls", []) or []:
        href = url.get("expanded_url") or url.get("expandedUrl") or url.get("url")
        if not href:
            continue
        links.append(
            {
                "href": href,
                "text": url.get("display_url") or url.get("displayUrl") or url.get("url") or href,
            }
        )
    return links


def extract_media_items(tweet: dict[str, Any]) -> list[dict[str, Any]]:
    legacy = tweet.get("legacy") or {}
    entities = legacy.get("extended_entities") or legacy.get("entities") or {}
    media_entries = entities.get("media") or []
    items: list[dict[str, Any]] = []

    for media in media_entries:
        thumbnail = media.get("media_url_https") or media.get("media_url")
        variants = media.get("video_info", {}).get("variants") if isinstance(media.get("video_info"), dict) else []
        video_variants = [
            {
                "bitrate": item.get("bitrate"),
                "content_type": item.get("content_type"),
                "url": item.get("url"),
            }
            for item in (variants or [])
            if item.get("url")
        ]
        items.append(
            {
                "media_key": media.get("media_key"),
                "type": media.get("type"),
                "display_url": media.get("display_url"),
                "expanded_url": media.get("expanded_url"),
                "thumbnail_url": normalize_media_url(thumbnail) if thumbnail else None,
                "media_url": normalize_media_url(thumbnail) if thumbnail else None,
                "video_variants": video_variants,
                "width": media.get("original_info", {}).get("width"),
                "height": media.get("original_info", {}).get("height"),
            }
        )
    return items


def extract_card_links(tweet: dict[str, Any]) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    card = tweet.get("card") or {}
    legacy = card.get("legacy") or {}
    binding_values = legacy.get("binding_values") or []
    for binding in binding_values:
        value = binding.get("value") or {}
        if not isinstance(value, dict):
            continue
        candidate = value.get("string_value") if "string_value" in value else None
        if candidate and isinstance(candidate, str) and candidate.startswith(("http://", "https://")):
            links.append({"href": candidate, "text": binding.get("key") or candidate})
    return links


def extract_note_tweet_text(tweet: dict[str, Any]) -> tuple[str, dict[str, Any] | None]:
    note = tweet.get("note_tweet", {}).get("note_tweet_results", {}).get("result", {})
    if not isinstance(note, dict):
        return "", None
    text = note.get("text") or ""
    entity_set = note.get("entity_set")
    return text, entity_set if isinstance(entity_set, dict) else None


def extract_author(tweet: dict[str, Any]) -> tuple[str | None, str | None]:
    user_result = tweet.get("core", {}).get("user_results", {}).get("result", {})
    legacy = user_result.get("legacy") or {}
    core = user_result.get("core") or {}
    screen_name = legacy.get("screen_name") or core.get("screen_name")
    display_name = core.get("name") or legacy.get("name")
    return display_name, screen_name


def tweet_to_post(tweet: dict[str, Any], *, source_tab: str, pinned_ids: set[str]) -> dict[str, Any]:
    legacy = tweet.get("legacy") or {}
    display_name, screen_name = extract_author(tweet)
    status_id = tweet.get("rest_id") or legacy.get("id_str")
    status_url = f"{X_BASE}/{screen_name}/status/{status_id}" if screen_name and status_id else None

    note_text, note_entities = extract_note_tweet_text(tweet)
    text = note_text or legacy.get("full_text") or ""
    text_links = extract_entity_links(note_entities) if note_text else extract_entity_links(legacy.get("entities"))
    media_items = extract_media_items(tweet)
    media_urls = [item["media_url"] for item in media_items if item.get("media_url")]
    visible_image_urls = [item["thumbnail_url"] for item in media_items if item.get("thumbnail_url")]

    all_links: list[dict[str, str]] = []
    seen_links: set[tuple[str, str]] = set()
    for link in text_links + extract_card_links(tweet):
        href = link.get("href") or ""
        text_value = link.get("text") or ""
        key = (href, text_value)
        if href and key not in seen_links:
            all_links.append({"href": href, "text": text_value})
            seen_links.add(key)

    for item in media_items:
        href = item.get("expanded_url") or ""
        text_value = item.get("display_url") or href
        key = (href, text_value)
        if href and key not in seen_links:
            all_links.append({"href": href, "text": text_value})
            seen_links.add(key)

    post = {
        "status_id": status_id,
        "status_url": status_url,
        "created_at": parse_x_datetime(legacy.get("created_at")),
        "display_time": legacy.get("created_at"),
        "display_name": display_name,
        "handle": f"@{screen_name}" if screen_name else None,
        "text": clean_string(text) or "",
        "preview_text": clean_string(text) or "",
        "text_links": text_links,
        "all_links": all_links,
        "external_links": [item for item in all_links if item.get("href") and not is_internal_x_link(item["href"])],
        "media_urls": media_urls,
        "media_items": media_items,
        "visible_links": [item.get("href") for item in text_links if item.get("href")],
        "visible_image_urls": visible_image_urls,
        "source_tabs": [source_tab],
        "is_pinned": bool(status_id and status_id in pinned_ids),
        "metrics": {
            "reply_count": legacy.get("reply_count"),
            "retweet_count": legacy.get("retweet_count"),
            "favorite_count": legacy.get("favorite_count"),
            "quote_count": legacy.get("quote_count"),
            "bookmark_count": legacy.get("bookmark_count"),
        },
        "lang": legacy.get("lang"),
        "article_text": clean_string(text) or "",
        "raw_created_at": legacy.get("created_at"),
    }
    return clean_payload(post)


def merge_post(existing: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    for tab in incoming.get("source_tabs", []):
        if tab not in existing["source_tabs"]:
            existing["source_tabs"].append(tab)

    if incoming.get("created_at") and not existing.get("created_at"):
        existing["created_at"] = incoming["created_at"]
    if incoming.get("text") and len(incoming["text"]) > len(existing.get("text", "")):
        existing["text"] = incoming["text"]
        existing["preview_text"] = incoming.get("preview_text", incoming["text"])
        existing["article_text"] = incoming.get("article_text", incoming["text"])
    if incoming.get("display_name") and not existing.get("display_name"):
        existing["display_name"] = incoming["display_name"]
    if incoming.get("handle") and not existing.get("handle"):
        existing["handle"] = incoming["handle"]

    existing["is_pinned"] = existing.get("is_pinned", False) or incoming.get("is_pinned", False)

    for field in ["visible_links", "visible_image_urls", "media_urls"]:
        for value in incoming.get(field, []):
            if value not in existing[field]:
                existing[field].append(value)

    for field in ["text_links", "all_links", "external_links", "media_items"]:
        existing_items = existing.get(field, [])
        seen = {compact_json(item) for item in existing_items}
        for item in incoming.get(field, []):
            key = compact_json(item)
            if key not in seen:
                existing_items.append(item)
                seen.add(key)
        existing[field] = existing_items

    if not existing.get("metrics") and incoming.get("metrics"):
        existing["metrics"] = incoming["metrics"]

    return existing


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
        for item in post.get("media_items", []):
            media_url = item.get("media_url")
            if not media_url:
                continue
            rows.append(
                {
                    "status_id": post.get("status_id"),
                    "status_url": post.get("status_url"),
                    "media_type": item.get("type"),
                    "media_url": media_url,
                    "normalized_media_url": normalize_media_url(media_url),
                    "expanded_url": item.get("expanded_url"),
                }
            )
    return rows


def resolve_short_links(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    session = requests.Session()
    session.headers.update({"User-Agent": DEFAULT_USER_AGENT})
    cache: dict[str, str] = {}

    for row in rows:
        href = row.get("href") or ""
        if not href.startswith("https://t.co/"):
            continue
        if href not in cache:
            try:
                with session.get(href, timeout=20, allow_redirects=True, stream=True) as response:
                    cache[href] = response.url or href
            except requests.RequestException:
                cache[href] = href
        row["href"] = cache[href]
    return rows


def download_media(rows: list[dict[str, Any]], media_dir: Path) -> list[dict[str, Any]]:
    ensure_dir(media_dir)
    session = requests.Session()
    session.headers.update({"User-Agent": DEFAULT_USER_AGENT})

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


def scrape_profile_metadata(
    session: requests.Session,
    headers: dict[str, str],
    operations: dict[str, str],
    handle: str,
) -> dict[str, Any]:
    payload = graphql_get(
        session,
        headers,
        operations,
        "UserByScreenName",
        {"screen_name": handle},
    )
    result = payload["data"]["user"]["result"]
    legacy = result.get("legacy") or {}
    core = result.get("core") or {}
    screen_name = core.get("screen_name") or handle
    display_name = core.get("name") or legacy.get("name")
    avatar = result.get("avatar", {}).get("image_url") or legacy.get("profile_image_url_https")
    banner = legacy.get("profile_banner_url")
    profile = {
        "handle": screen_name,
        "url": profile_url(screen_name),
        "title": f"{display_name} (@{screen_name}) / X" if display_name else f"@{screen_name} / X",
        "display_name": display_name,
        "bio": legacy.get("description"),
        "avatar_url": avatar,
        "banner_url": banner,
        "followers_count": legacy.get("followers_count"),
        "friends_count": legacy.get("friends_count"),
        "statuses_count": legacy.get("statuses_count"),
        "media_count": legacy.get("media_count"),
        "rest_id": result.get("rest_id"),
        "pinned_tweet_ids_str": legacy.get("pinned_tweet_ids_str") or [],
    }
    return clean_payload(profile)


def collect_statuses_from_tab(
    session: requests.Session,
    headers: dict[str, str],
    operations: dict[str, str],
    handle: str,
    run_dir: Path,
    user_id: str,
    tab: str,
    *,
    pinned_ids: set[str],
    max_pages: int,
    page_size: int,
    sleep_seconds: float,
) -> dict[str, dict[str, Any]]:
    operation_name = TAB_CONFIG[tab]["operation"]
    collected: dict[str, dict[str, Any]] = {}
    cursor: str | None = None
    seen_cursors: set[str] = set()
    idle_pages = 0

    state_file = run_dir / f"state_{tab}.json"
    if state_file.exists():
        try:
            state = json.loads(state_file.read_text(encoding="utf-8"))
            if isinstance(state, dict) and "cursor" in state:
                cursor = state.get("cursor")
                if cursor:
                    print(f"[resume] found cursor for tab={tab}, resuming", flush=True)
        except (json.JSONDecodeError, TypeError):
            pass  # Ignore invalid state file

    for page_index in range(max_pages):
        variables: dict[str, Any] = {
            "userId": user_id,
            "count": page_size,
            "includePromotedContent": False,
            "withQuickPromoteEligibilityTweetFields": True,
            "withVoice": True,
        }
        if cursor:
            variables["cursor"] = cursor

        payload = graphql_get(session, headers, operations, operation_name, variables)
        tweets = extract_tweets(payload)
        before = len(collected)
        for tweet in tweets:
            post = tweet_to_post(tweet, source_tab=tab, pinned_ids=pinned_ids)
            status_url = post.get("status_url")
            if not status_url:
                continue
            existing = collected.get(status_url)
            if existing:
                merge_post(existing, post)
            else:
                collected[status_url] = post

        cursor = extract_bottom_cursor(payload)
        try:
            # Persist the next cursor to allow for resumption
            write_json(state_file, {"cursor": cursor, "updated_at": time.time()})
        except Exception as exc:
            print(f"[state] failed to save cursor for tab={tab}: {exc}", file=sys.stderr, flush=True)

        print(
            f"[timeline] tab={tab} page={page_index + 1} statuses={len(collected)} "
            f"new={len(collected) - before}",
            flush=True,
        )

        if len(collected) == before:
            idle_pages += 1
        else:
            idle_pages = 0

        if idle_pages >= 2:
            break
        if not cursor or cursor in seen_cursors:
            break
        seen_cursors.add(cursor)
        if sleep_seconds > 0:
            time.sleep(sleep_seconds)

    return collected


def main() -> int:
    args = parse_args()
    handle = normalize_handle(args.handle)
    tabs = args.tabs or ["posts"]
    max_pages = args.max_scrolls if args.max_scrolls is not None else args.max_pages
    sleep_seconds = (args.scroll_delay_ms / 1000.0) if args.scroll_delay_ms is not None else args.sleep_seconds
    cookies = load_x_cookies(args.cookies_file)

    run_dir = args.outdir / handle / time.strftime("%Y%m%d-%H%M%S")
    ensure_dir(run_dir)

    print(f"[setup] output -> {run_dir}", flush=True)
    print(f"[setup] tabs -> {', '.join(tabs)}", flush=True)
    if cookies:
        print(f"[setup] using cookie file -> {args.cookies_file}", flush=True)

    errors: list[dict[str, str]] = []
    session = build_session(cookies)

    try:
        html = fetch_profile_html(session, handle)
        bearer_token, operations = discover_client_config(session, html)
        headers = build_graphql_headers(session, handle, bearer_token, html)
        profile = scrape_profile_metadata(session, headers, operations, handle)
        write_json(run_dir / "profile.json", profile)
        print(f"[profile] {profile.get('title')}", flush=True)

        user_id = profile.get("rest_id")
        if not user_id:
            raise XScrapeError("profile response did not include rest_id")
        pinned_ids = set(profile.get("pinned_tweet_ids_str") or [])

        collected: dict[str, dict[str, Any]] = {}
        for tab in tabs:
            try:
                tab_records = collect_statuses_from_tab(
                    session,
                    headers,
                    operations,
                    handle,
                    user_id,
                    run_dir,
                    tab,
                    pinned_ids=pinned_ids,
                    max_pages=max_pages,
                    page_size=args.page_size,
                    sleep_seconds=sleep_seconds,
                )
            except TabUnavailableError as exc:
                errors.append({"tab": tab, "error": str(exc)})
                print(f"[timeline] skipping tab '{tab}': {exc}", flush=True)
                continue

            for status_url, record in tab_records.items():
                existing = collected.get(status_url)
                if existing:
                    merge_post(existing, record)
                else:
                    collected[status_url] = record

    except Exception as exc:
        print(f"[fatal] {exc}", file=sys.stderr, flush=True)
        errors.append({"stage": "fatal", "error": str(exc)})
        write_json(run_dir / "errors.json", errors)
        return 1

    posts = list(collected.values())
    posts.sort(key=lambda item: (item.get("created_at") or "", item.get("status_id") or ""))
    if args.status_limit > 0:
        posts = posts[: args.status_limit]

    timeline_index = [
        {
            "status_url": post.get("status_url"),
            "status_id": post.get("status_id"),
            "created_at": post.get("created_at"),
            "preview_text": post.get("preview_text") or "",
            "source_tabs": post.get("source_tabs", []),
            "is_pinned": post.get("is_pinned", False),
            "visible_links": post.get("visible_links", []),
            "visible_image_urls": post.get("visible_image_urls", []),
        }
        for post in posts
    ]

    links = resolve_short_links(flatten_links(posts))
    media = flatten_media(posts)
    downloads: list[dict[str, Any]] = []

    write_json(run_dir / "timeline-index.json", timeline_index)
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
        fieldnames=["status_id", "status_url", "media_type", "media_url", "normalized_media_url", "expanded_url"],
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
