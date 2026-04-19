from __future__ import annotations

import argparse
import json
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import quote_plus, urlparse
from urllib.request import Request, urlopen


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/135.0.0.0 Safari/537.36"
)

ALLOWED_HOST_SUFFIXES = (
    "archive.org",
    "ia800.us.archive.org",
    "ia801.us.archive.org",
    "ia802.us.archive.org",
    "ia803.us.archive.org",
    "ia804.us.archive.org",
    "ia600.us.archive.org",
    "ia601.us.archive.org",
    "ia602.us.archive.org",
    "ia803100.us.archive.org",
    "arxiv.org",
    "springer.com",
    "link.springer.com",
    "nasa.gov",
    "ntrs.nasa.gov",
    "dtic.mil",
    "osti.gov",
    "gov",
    "edu",
)

COVER_SUFFIX = "-book-cover"
TIMESTAMP_PREFIX_RE = re.compile(r"^\d{8}_\d{6}_")

CURATED_URLS: dict[str, list[str]] = {
    "works by aw trivelpiece slow wave propagation in plasma waveguides": [
        "https://thesis.library.caltech.edu/2799/1/Trivelpiece_aw_1958.pdf",
    ],
    "very high mach number electrostatic shocks in collisionless plasmas": [
        "https://arxiv.org/pdf/physics/0512231.pdf",
    ],
}


@dataclass
class Result:
    title: str
    source_cover: str
    status: str
    pdf_url: str | None = None
    local_path: str | None = None
    note: str | None = None


def normalize_title(raw: str) -> str:
    name = Path(raw).stem
    name = TIMESTAMP_PREFIX_RE.sub("", name)
    if name.endswith(COVER_SUFFIX):
        name = name[: -len(COVER_SUFFIX)]
    name = name.replace("_", "-").strip("-")
    return name.replace("-", " ")


def canonical_key(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def is_allowed_host(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    return any(host == suffix or host.endswith(f".{suffix}") for suffix in ALLOWED_HOST_SUFFIXES)


def fetch_text(url: str) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=25) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fetch_json(url: str) -> dict:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def search_archive_pdf_links(title: str, limit: int = 5) -> list[str]:
    query = f'title:("{title}") AND mediatype:texts'
    search_url = (
        "https://archive.org/advancedsearch.php?"
        f"q={quote_plus(query)}&fl[]=identifier&rows={limit}&output=json"
    )
    results = fetch_json(search_url)
    docs = results.get("response", {}).get("docs", [])
    pdf_links: list[str] = []
    for doc in docs:
        identifier = doc.get("identifier")
        if not identifier:
            continue
        try:
            metadata = fetch_json(f"https://archive.org/metadata/{identifier}")
        except Exception:  # noqa: BLE001
            continue
        files = metadata.get("files", [])
        pdf_candidates = []
        for file_entry in files:
            name = file_entry.get("name", "")
            if name.lower().endswith(".pdf"):
                size = int(file_entry.get("size") or 0)
                pdf_candidates.append((size, name))
        if not pdf_candidates:
            continue
        pdf_candidates.sort(reverse=True)
        pdf_name = pdf_candidates[0][1]
        pdf_links.append(f"https://archive.org/download/{identifier}/{pdf_name}")
    return pdf_links


def try_download_pdf(url: str, destination: Path) -> bool:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=35) as resp:
        content_type = resp.headers.get("Content-Type", "").lower()
        if "pdf" not in content_type and not url.lower().endswith(".pdf"):
            return False
        data = resp.read()
    if not data.startswith(b"%PDF"):
        return False
    destination.write_bytes(data)
    return True


def candidate_urls_for_title(title: str) -> Iterable[str]:
    key = canonical_key(title)
    for url in CURATED_URLS.get(key, []):
        yield url
    try:
        for url in search_archive_pdf_links(title):
            if is_allowed_host(url):
                yield url
    except Exception:  # noqa: BLE001
        pass


def main() -> int:
    parser = argparse.ArgumentParser(description="Find openly accessible PDFs for book covers.")
    parser.add_argument("--covers-dir", default="assets/categorized/book-covers")
    parser.add_argument("--output-dir", default="sources/downloads/books")
    args = parser.parse_args()

    covers_dir = Path(args.covers_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    results: list[Result] = []
    for cover in sorted(covers_dir.iterdir()):
        if not cover.is_file():
            continue
        title = normalize_title(cover.name)
        pdf_name = re.sub(r"[^a-z0-9]+", "-", canonical_key(title)).strip("-") or "book"
        pdf_path = output_dir / f"{pdf_name}.pdf"

        status = "not_found"
        found_url: str | None = None
        note: str | None = None

        for candidate in candidate_urls_for_title(title):
            try:
                if try_download_pdf(candidate, pdf_path):
                    status = "downloaded"
                    found_url = candidate
                    note = None
                    break
            except Exception as exc:  # noqa: BLE001
                note = str(exc)
                continue

        if status != "downloaded" and pdf_path.exists():
            pdf_path.unlink()

        results.append(
            Result(
                title=title,
                source_cover=str(cover),
                status=status,
                pdf_url=found_url,
                local_path=str(pdf_path) if status == "downloaded" else None,
                note=note,
            )
        )
        time.sleep(0.2)

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps([asdict(result) for result in results], indent=2),
        encoding="utf-8",
    )

    summary_lines = [
        "# Book PDF Search Results",
        "",
        f"- Covers scanned: {len(results)}",
        f"- PDFs downloaded: {sum(1 for item in results if item.status == 'downloaded')}",
        "",
        "## Results",
        "",
    ]
    for item in results:
        summary_lines.append(f"### {item.title}")
        summary_lines.append(f"- Status: {item.status}")
        if item.pdf_url:
            summary_lines.append(f"- PDF URL: {item.pdf_url}")
        if item.local_path:
            summary_lines.append(f"- Local file: `{item.local_path}`")
        if item.note and item.status != "downloaded":
            summary_lines.append(f"- Note: {item.note}")
        summary_lines.append("")
    (output_dir / "README.md").write_text("\n".join(summary_lines), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
