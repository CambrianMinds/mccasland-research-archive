from __future__ import annotations

import argparse
import json
import mimetypes
import re
import shutil
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/135.0.0.0 Safari/537.36"
)

MARKDOWN_IMAGE_RE = re.compile(r"!\[(?P<label>[^\]]*)\]\((?P<url>[^)]+)\)")
MARKDOWN_LINK_RE = re.compile(r"(?<!\!)\[(?P<label>[^\]]+)\]\((?P<url>[^)]+)\)")
BARE_URL_RE = re.compile(r"https?://[^\s)>\]`]+|archive\.org/details/[^\s)>\]`]+")


CURATED_REFERENCE_SOURCES: dict[str, list[dict[str, str]]] = {
    "Electrodynamics of Continuous Media": [
        {
            "title": "Open Library record",
            "url": "https://openlibrary.org/books/OL3182313M/Electrodynamics_of_continuous_media",
            "kind": "page",
        },
    ],
    "Shock Waves in Collisionless Plasmas": [
        {
            "title": "Internet Archive record",
            "url": "https://archive.org/details/shockwavesincoll00tidm",
            "kind": "page",
        },
    ],
    "Works by A.W. Trivelpiece (Slow Wave Propagation in Plasma Waveguides)": [
        {
            "title": "CaltechTHESIS landing page",
            "url": "https://thesis.library.caltech.edu/2799/",
            "kind": "page",
        },
        {
            "title": "Dissertation PDF",
            "url": "https://thesis.library.caltech.edu/2799/1/Trivelpiece_aw_1958.pdf",
            "kind": "paper",
        },
    ],
    "R.M. Bevensee - Electromagnetic Slow Wave Systems (1964)": [
        {
            "title": "Open Library record",
            "url": "https://openlibrary.org/books/OL5911516M/Electromagnetic_slow_wave_systems",
            "kind": "page",
        },
    ],
    "K. Tanaka (1989) - Glow Discharge Hydrogenated Amorphous Silicone": [
        {
            "title": "Springer record",
            "url": "https://link.springer.com/book/9780792303091",
            "kind": "page",
        },
    ],
    "Resonating Valence Bond Theory (Wikipedia overview)": [
        {
            "title": "Wikipedia article",
            "url": "https://en.wikipedia.org/wiki/Resonating_valence_bond_theory",
            "kind": "page",
        },
    ],
    "Very High Mach-Number Electrostatic Shocks in Collisionless Plasmas (2006 paper)": [
        {
            "title": "arXiv abstract",
            "url": "https://arxiv.org/abs/physics/0512231",
            "kind": "page",
        },
        {
            "title": "arXiv PDF",
            "url": "https://arxiv.org/pdf/physics/0512231.pdf",
            "kind": "paper",
        },
    ],
}


@dataclass
class DownloadTarget:
    title: str
    url: str
    kind: str
    local_path: str | None = None
    status: str = "pending"
    note: str | None = None
    content_type: str | None = None
    http_status: int | None = None


@dataclass
class ManifestEntry:
    slug: str
    title: str
    section: str
    source_type: str
    description: str | None = None
    targets: list[DownloadTarget] = field(default_factory=list)


def slugify(text: str) -> str:
    text = text.strip()
    text = text.replace("&", " and ")
    text = text.replace("/", " ")
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[_\s-]+", "-", text)
    return text.strip("-").lower() or "item"


def normalize_title(text: str) -> str:
    text = text.strip().replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", text)


def canonicalize_url(url: str) -> str:
    url = url.strip()
    if url.startswith("archive.org/details/"):
        return f"https://{url}"
    return url


def find_curated_reference_targets(bullet_title: str) -> list[DownloadTarget]:
    normalized = bullet_title.lower()
    rules: list[tuple[tuple[str, ...], str]] = [
        (("electrodynamics of continuous media",), "Electrodynamics of Continuous Media"),
        (("shock waves in collisionless plasmas",), "Shock Waves in Collisionless Plasmas"),
        (
            ("slow wave propagation in plasma waveguides", "trivelpiece"),
            "Works by A.W. Trivelpiece (Slow Wave Propagation in Plasma Waveguides)",
        ),
        (
            ("electromagnetic slow wave systems", "bevensee"),
            "R.M. Bevensee - Electromagnetic Slow Wave Systems (1964)",
        ),
        (
            ("glow discharge hydrogenated amorphous silicone", "tanaka"),
            "K. Tanaka (1989) - Glow Discharge Hydrogenated Amorphous Silicone",
        ),
        (
            ("resonating valence bond theory",),
            "Resonating Valence Bond Theory (Wikipedia overview)",
        ),
        (
            ("very high mach-number electrostatic shocks in collisionless plasmas",),
            "Very High Mach-Number Electrostatic Shocks in Collisionless Plasmas (2006 paper)",
        ),
    ]

    for fragments, canonical_key in rules:
        if any(fragment in normalized for fragment in fragments):
            return [
                DownloadTarget(
                    title=target["title"],
                    url=target["url"],
                    kind=target["kind"],
                )
                for target in CURATED_REFERENCE_SOURCES[canonical_key]
            ]
    return []


def sniff_extension(url: str, content_type: str | None) -> str:
    parsed = urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".pdf", ".html", ".htm"}:
        return ".jpg" if suffix == ".jpeg" else suffix

    if content_type:
        base_type = content_type.split(";", 1)[0].strip().lower()
        if base_type == "text/html":
            return ".html"
        guessed = mimetypes.guess_extension(base_type)
        if guessed:
            return ".jpg" if guessed == ".jpe" else guessed

    return ".bin"


def safe_filename(label: str, fallback_url: str, content_type: str | None = None) -> str:
    stem = slugify(label)
    extension = sniff_extension(fallback_url, content_type)
    return f"{stem}{extension}"


def file_relative_to(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def request_bytes(url: str) -> tuple[bytes, int | None, str | None]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=45) as response:
        return response.read(), response.status, response.headers.get("Content-Type")


def download_to(url: str, destination: Path) -> tuple[int | None, str | None]:
    payload, status, content_type = request_bytes(url)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(payload)
    return status, content_type


def is_recommended_reading_section(line: str) -> bool:
    return line.lstrip().startswith("## Recommended Reading List")


def iter_markdown_bare_urls(line: str) -> Iterable[str]:
    for match in BARE_URL_RE.finditer(line):
        yield canonicalize_url(match.group(0))


def build_entries(markdown_text: str) -> list[ManifestEntry]:
    entries: list[ManifestEntry] = []
    seen_image_urls: set[str] = set()
    seen_page_urls: set[str] = set()
    current_section = "root"
    in_recommended_reading = False

    for raw_line in markdown_text.splitlines():
        line = raw_line.strip()

        if line.startswith("### "):
            current_section = normalize_title(line[4:])
            in_recommended_reading = False
        elif line.startswith("## "):
            current_section = normalize_title(line[3:])
            in_recommended_reading = is_recommended_reading_section(line)

        for match in MARKDOWN_IMAGE_RE.finditer(line):
            url = canonicalize_url(match.group("url"))
            if url in seen_image_urls:
                continue
            seen_image_urls.add(url)
            label = normalize_title(match.group("label") or Path(urlparse(url).path).stem)
            entries.append(
                ManifestEntry(
                    slug=slugify(label),
                    title=label,
                    section=current_section,
                    source_type="image",
                    targets=[DownloadTarget(title=label, url=url, kind="image")],
                )
            )

        for match in MARKDOWN_LINK_RE.finditer(line):
            url = canonicalize_url(match.group("url"))
            if url in seen_page_urls or url.startswith("https://pbs.twimg.com/"):
                continue
            seen_page_urls.add(url)
            label = normalize_title(match.group("label"))
            entries.append(
                ManifestEntry(
                    slug=slugify(label),
                    title=label,
                    section=current_section,
                    source_type="page",
                    targets=[DownloadTarget(title=label, url=url, kind="page")],
                )
            )

        if in_recommended_reading and line.startswith("- "):
            bullet = normalize_title(line[2:])
            bullet = bullet.strip("`")
            bullet_without_markup = bullet.replace("*", "").strip()
            targets: list[DownloadTarget] = []

            direct_urls = list(iter_markdown_bare_urls(line))
            if direct_urls:
                for url in direct_urls:
                    targets.append(
                        DownloadTarget(
                            title=bullet_without_markup,
                            url=url,
                            kind="page",
                        )
                    )

            targets.extend(find_curated_reference_targets(bullet_without_markup))
            deduped_targets: list[DownloadTarget] = []
            seen_urls: set[str] = set()
            for target in targets:
                if target.url in seen_urls:
                    continue
                seen_urls.add(target.url)
                deduped_targets.append(target)

            entries.append(
                ManifestEntry(
                    slug=slugify(bullet_without_markup),
                    title=bullet_without_markup,
                    section=current_section,
                    source_type="reference",
                    description="Recommended reading list entry from research-targets.md",
                    targets=deduped_targets or [],
                )
            )

        elif not line.startswith("- "):
            in_recommended_reading = is_recommended_reading_section(line)

    return entries


def resolve_destination_parent(root: Path, entry: ManifestEntry, target: DownloadTarget) -> Path:
    section_slug = slugify(entry.section)
    if target.kind == "image":
        return root / "media" / section_slug
    elif target.kind == "paper":
        return root / "papers" / slugify(entry.title)
    return root / "pages" / section_slug / slugify(entry.title)


def render_readme(root: Path, entries: list[ManifestEntry]) -> str:
    successful = sum(
        1
        for entry in entries
        for target in entry.targets
        if target.status == "downloaded"
    )
    failed = sum(
        1
        for entry in entries
        for target in entry.targets
        if target.status == "failed"
    )
    unresolved = sum(1 for entry in entries if not entry.targets)

    lines = [
        "# Research Targets Downloads",
        "",
        "Generated from `research-targets.md`.",
        "",
        f"- Downloaded targets: {successful}",
        f"- Failed targets: {failed}",
        f"- Reference entries without public target URLs: {unresolved}",
        "",
        "## Inventory",
        "",
    ]

    for entry in entries:
        lines.append(f"### {entry.title}")
        lines.append(f"- Section: {entry.section}")
        lines.append(f"- Type: {entry.source_type}")
        if entry.description:
            lines.append(f"- Notes: {entry.description}")
        if not entry.targets:
            lines.append("- Status: recorded only, no public URL was embedded in the source file")
            lines.append("")
            continue

        for target in entry.targets:
            status_line = f"- {target.kind}: {target.status}"
            if target.local_path:
                status_line += f" -> `{target.local_path}`"
            lines.append(status_line)
            lines.append(f"  source: {target.url}")
            if target.note:
                lines.append(f"  note: {target.note}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def extract_embedded_markdown(source_markdown: str) -> str:
    match = re.search(r"```markdown\s*(.*?)```", source_markdown, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip() + "\n"
    return source_markdown


def write_local_guide(root: Path, source_markdown: str, entries: list[ManifestEntry]) -> None:
    replacements: dict[str, str] = {}
    for entry in entries:
        for target in entry.targets:
            if target.status != "downloaded" or not target.local_path:
                continue
            local_rel = target.local_path
            replacements[target.url] = local_rel

    local_text = extract_embedded_markdown(source_markdown)
    for remote, local in sorted(replacements.items(), key=lambda pair: -len(pair[0])):
        local_text = local_text.replace(f"({remote})", f"({local})")
        if remote.startswith("https://archive.org/"):
            local_text = local_text.replace(remote[len("https://") :], local)

    guide_path = root / "guide-local.md"
    guide_path.write_text(local_text, encoding="utf-8")


def run(markdown_path: Path, output_root: Path, pause_seconds: float) -> list[ManifestEntry]:
    source_text = markdown_path.read_text(encoding="utf-8", errors="replace")
    output_root.mkdir(parents=True, exist_ok=True)

    entries = build_entries(source_text)

    for entry in entries:
        for target in entry.targets:
            target.url = canonicalize_url(target.url)
            try:
                payload, http_status, content_type = request_bytes(target.url)
                destination = (
                    resolve_destination_parent(output_root, entry, target)
                    / safe_filename(target.title, target.url, content_type)
                )
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(payload)
                target.status = "downloaded"
                target.http_status = http_status
                target.content_type = content_type
                target.local_path = file_relative_to(destination, output_root)
            except (HTTPError, URLError, TimeoutError, OSError) as exc:
                target.status = "failed"
                target.note = str(exc)
            time.sleep(pause_seconds)

    manifest_path = output_root / "manifest.json"
    manifest_path.write_text(
        json.dumps([asdict(entry) for entry in entries], indent=2),
        encoding="utf-8",
    )

    readme_path = output_root / "README.md"
    readme_path.write_text(render_readme(output_root, entries), encoding="utf-8")

    source_copy_path = output_root / "source.md"
    shutil.copyfile(markdown_path, source_copy_path)
    write_local_guide(output_root, source_text, entries)

    return entries


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download and organize all direct items referenced by research-targets.md.",
    )
    parser.add_argument(
        "--input",
        default="research-targets.md",
        help="Path to the markdown guide to parse.",
    )
    parser.add_argument(
        "--output",
        default="research-targets",
        help="Directory where organized downloads should be written.",
    )
    parser.add_argument(
        "--pause-seconds",
        type=float,
        default=0.25,
        help="Delay between requests to avoid hammering hosts.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    entries = run(Path(args.input), Path(args.output), args.pause_seconds)

    downloaded = sum(
        1
        for entry in entries
        for target in entry.targets
        if target.status == "downloaded"
    )
    failed = sum(
        1
        for entry in entries
        for target in entry.targets
        if target.status == "failed"
    )
    recorded_only = sum(1 for entry in entries if not entry.targets)
    print(
        json.dumps(
            {
                "entries": len(entries),
                "downloaded_targets": downloaded,
                "failed_targets": failed,
                "recorded_only_entries": recorded_only,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
