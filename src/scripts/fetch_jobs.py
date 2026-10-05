#!/usr/bin/env python3
"""
TC OptRob careers-page pipeline.

Fetches recent messages from the robotics-worldwide mailing list archive,
classifies them as job postings relevant to the TC (optimal control,
optimization, robot dynamics, reinforcement learning, ...), optionally tags
them with a "featured PI" badge, keeps a rolling one-year window of
postings, and (re)generates src/careers.md for the MkDocs site.

Design notes (see career-page-design.md for the full writeup):

- Two independent fetch strategies are tried in order: (1) the Sympa RSS
  feed, which Sympa's own docs describe as served without authentication,
  and (2) a fallback HTML scrape of the monthly archive pages. Strategy (2)
  has NOT been verified against the live site (it was written in a sandbox
  with no general network egress) -- test it once from a normal network /
  the first real GitHub Actions run, and adjust the selectors in
  `_parse_archive_month_html` if the Sympa theme differs from what's
  assumed here.
- EURON is intentionally NOT included: their archive is subscriber-only
  (see design doc, section 2), so there is nothing public to fetch.
- Classification, PI matching, retention, and page rendering are pure
  functions with no network dependency -- see tests/test_pipeline.py.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import requests
import yaml

SRC_DIR = Path(__file__).resolve().parent.parent  # <repo>/src (the MkDocs docs_dir)
DATA_DIR = SRC_DIR / "data"

KEYWORDS_PATH = DATA_DIR / "keywords.yaml"
PIS_PATH = DATA_DIR / "pis.yaml"
SEEN_PATH = DATA_DIR / "jobs_seen.json"
PAGE_PATH = SRC_DIR / "careers.md"

LIST_NAME = "robotics-worldwide"
LIST_HOST = "https://www.lists.kit.edu"
RSS_URL = f"{LIST_HOST}/sympa/rss/latest_arc/{LIST_NAME}"
ARCHIVE_URL = f"{LIST_HOST}/sympa/arc/{LIST_NAME}"

RETENTION_DAYS = 365
USER_AGENT = "tcoptrob-careers-bot/1.0 (+https://www.tcoptrob.org/; contact: TC OptRob co-chairs)"


# --------------------------------------------------------------------------
# Config loading
# --------------------------------------------------------------------------

def load_config() -> tuple[dict[str, list[str]], list[dict[str, Any]]]:
    with open(KEYWORDS_PATH, encoding="utf-8") as f:
        keywords = yaml.safe_load(f)
    with open(PIS_PATH, encoding="utf-8") as f:
        pis = yaml.safe_load(f).get("pis", [])
    return keywords, pis


# --------------------------------------------------------------------------
# Fetching -- strategy 1: Sympa RSS
# --------------------------------------------------------------------------

def fetch_via_rss(days: int = 14, timeout: int = 20) -> list[dict[str, Any]]:
    """Fetch recent messages via Sympa's RSS endpoint.

    Returns a list of {id, title, link, date, summary}. Raises on any
    failure so the caller can fall back to the archive scraper.
    """
    resp = requests.get(
        RSS_URL,
        params={"for": days},
        headers={"User-Agent": USER_AGENT},
        timeout=timeout,
    )
    resp.raise_for_status()
    root = ET.fromstring(resp.content)

    items = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date_raw = (item.findtext("pubDate") or "").strip()
        summary = (item.findtext("description") or "").strip()
        if not link:
            continue
        items.append(
            {
                "id": link,
                "title": title,
                "link": link,
                "date": _parse_rss_date(pub_date_raw),
                "summary": summary,
            }
        )

    if not items:
        raise ValueError("RSS feed returned no items -- treating as unavailable")
    return items


def _parse_rss_date(raw: str) -> str:
    """Best-effort RFC-822 -> ISO date. Falls back to today on parse failure."""
    for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z"):
        try:
            return dt.datetime.strptime(raw, fmt).date().isoformat()
        except ValueError:
            continue
    return dt.date.today().isoformat()


# --------------------------------------------------------------------------
# Fetching -- strategy 2: archive HTML scrape (fallback, needs live testing)
# --------------------------------------------------------------------------

def fetch_via_archive_scrape(months_back: int = 3, timeout: int = 20) -> list[dict[str, Any]]:
    """Fallback fetch by walking monthly archive pages directly.

    NOT VERIFIED against the live Sympa instance -- the info page shows an
    "anti-harvesting" click-through in front of the archive link, which may
    mean a plain GET here returns an interstitial page instead of the
    listing. If this raises or returns nothing, check the response text by
    hand and adjust `_parse_archive_month_html` accordingly -- e.g. it may
    require first following a confirmation link/cookie before the month
    pages resolve.
    """
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    today = dt.date.today().replace(day=1)
    items: list[dict[str, Any]] = []
    for i in range(months_back):
        year_month = _shift_month(today, -i)
        month_url = f"{ARCHIVE_URL}/{year_month}"
        resp = session.get(month_url, timeout=timeout)
        if resp.status_code != 200:
            continue
        items.extend(_parse_archive_month_html(resp.text, month_url, year_month, session, timeout))

    if not items:
        raise ValueError("Archive scrape returned no items")
    return items


def _shift_month(d: dt.date, delta: int) -> str:
    m = d.month - 1 + delta
    y = d.year + m // 12
    m = m % 12 + 1
    return f"{y:04d}-{m:02d}"


def _parse_archive_month_html(
    html: str, month_url: str, year_month: str, session: "requests.Session", timeout: int
) -> list[dict[str, Any]]:
    from bs4 import BeautifulSoup  # imported here so RSS-only usage doesn't need bs4

    soup = BeautifulSoup(html, "html.parser")
    items = []
    # Typical Sympa arc index: one <a> per message, href like "msgNNNNN.html".
    for a in soup.select("a[href$='.html']"):
        href = a.get("href", "")
        if not href or href.startswith("http"):
            link = href
        else:
            link = f"{ARCHIVE_URL}/{year_month}/{href}"
        title = a.get_text(strip=True)
        if not title:
            continue
        items.append(
            {
                "id": link,
                "title": title,
                "link": link,
                "date": f"{year_month}-01",  # month precision only
                "summary": "",
            }
        )
    return items


# --------------------------------------------------------------------------
# Classification (pure -- no network)
# --------------------------------------------------------------------------

# Sympa appends the sender to every subject: "<subject> - name@example.org".
SENDER_SUFFIX = re.compile(r"\s+-\s+(\S+@\S+)\s*$")


def split_sender(title: str) -> tuple[str, str | None]:
    """Split the trailing ' - sender@host' off a subject, so the address is never
    classified, stored in jobs_seen.json, or published on the page."""
    m = SENDER_SUFFIX.search(title or "")
    if not m:
        return title, None
    return title[: m.start()].rstrip(), m.group(1)


def classify_message(msg: dict[str, Any], keywords_cfg: dict[str, list[str]], body: str = "") -> dict[str, Any]:
    """Return match info for a message. Does not mutate msg."""
    text = " ".join([msg.get("title", ""), msg.get("summary", ""), body]).lower()

    job_signal_hits = [p for p in keywords_cfg.get("job_signal", []) if p.lower() in text]
    tc_hits = [p for p in keywords_cfg.get("tc_relevance", []) if p.lower().strip() in text]

    return {
        "is_job_posting": bool(job_signal_hits) and bool(tc_hits),
        "matched_job_signal": job_signal_hits,
        "matched_keywords": tc_hits,
    }


def match_pi(msg: dict[str, Any], pis: list[dict[str, Any]], body: str = "") -> dict[str, Any] | None:
    """Full-name substring match only (not last-name-only) to keep false
    positives down -- common surnames would otherwise over-match."""
    text = " ".join([msg.get("title", ""), msg.get("summary", ""), body]).lower()
    for pi in pis:
        name = (pi.get("name") or "").strip()
        if name and name.lower() in text:
            return pi
    return None


# --------------------------------------------------------------------------
# Seen-store + retention (pure -- no network)
# --------------------------------------------------------------------------

def load_seen() -> list[dict[str, Any]]:
    if not SEEN_PATH.exists():
        return []
    with open(SEEN_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_seen(records: list[dict[str, Any]]) -> None:
    SEEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SEEN_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, sort_keys=False, ensure_ascii=False)
        f.write("\n")


def merge_records(existing: list[dict[str, Any]], new: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {r["id"]: r for r in existing}
    for r in new:
        by_id[r["id"]] = r  # new data wins (e.g. re-classified with fuller body text)
    return list(by_id.values())


def apply_retention(records: list[dict[str, Any]], as_of: dt.date | None = None, max_age_days: int = RETENTION_DAYS) -> list[dict[str, Any]]:
    """Keep only postings dated within the last `max_age_days`. There is no
    reliable "closed" signal from a mailing list, so per the committee's
    instruction we use a single rolling window that covers both active and
    recently-closed postings, and drop anything older outright."""
    as_of = as_of or dt.date.today()
    cutoff = as_of - dt.timedelta(days=max_age_days)
    kept = []
    for r in records:
        try:
            posted = dt.date.fromisoformat(r["date"])
        except (KeyError, ValueError):
            continue
        if posted >= cutoff:
            kept.append(r)
    return kept


# --------------------------------------------------------------------------
# Page rendering (pure -- no network)
# --------------------------------------------------------------------------

def _e(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _display_title(title: str) -> str:
    """Drop leading [tags] such as '[robotics-worldwide] [Jobs] ' (display only)."""
    t = re.sub(r"^(?:\s*\[[^\]]*\])+\s*", "", title or "").strip()
    return t or "(untitled posting)"


def render_job_card(r: dict[str, Any]) -> str:
    """One posting as an HTML card. No indentation or blank lines inside:
    Markdown would turn those into code blocks / paragraphs."""
    pi = r.get("matched_pi")
    cls = "job-card job-card--pi" if pi else "job-card"
    parts = [f'<article class="{cls}">']
    parts.append(
        f'<h3 class="job-title"><a href="{_e(r["link"])}" target="_blank" rel="noopener">'
        f'{_e(_display_title(r.get("title", "")))}</a></h3>'
    )
    date = _e(r.get("date", "unknown date"))
    meta = f'<time datetime="{date}">{date}</time>'
    if pi:
        aff = f", {_e(r['pi_affiliation'])}" if r.get("pi_affiliation") else ""
        meta += f' <span class="job-pi">{_e(pi)}{aff}</span>'
    parts.append(f'<p class="job-meta">{meta}</p>')
    if r.get("matched_keywords"):
        tags = "".join(f'<li class="job-tag">{_e(k)}</li>' for k in r["matched_keywords"])
        parts.append(f'<ul class="job-tags">{tags}</ul>')
    parts.append("</article>")
    return "\n".join(parts)


def render_markdown(records: list[dict[str, Any]], generated_at: dt.date | None = None) -> str:
    generated_at = generated_at or dt.date.today()
    records_sorted = sorted(records, key=lambda r: r.get("date", ""), reverse=True)

    n = len(records_sorted)
    lines = [
        "---",
        "hide:",
        "  - navigation",
        "---",
        "",
        "# Career opportunities",
        "",
        "This page contains a list of career opportunities (PhD, Postdoc, Faculty, "
        "Industry) related to optimization in robotics from around the internet. "
        "Even though the page is updated regularly, it is not a comprehensive list. "
        "If you know of a position that you think could be relevant for the community, "
        "please let us know!",
        "",
        f"*Last updated: {generated_at.isoformat()}, {n} posting{'s' if n != 1 else ''}*",
        "",
    ]

    if not records_sorted:
        lines.append('<div class="job-list job-list--empty"><p>No postings currently match the TC\'s keyword filters. Check back soon.</p></div>')
        lines.append("")
        return "\n".join(lines)

    lines.append('<div class="job-list" tabindex="0" role="region" aria-label="Job postings">')
    lines.extend(render_job_card(r) for r in records_sorted)
    lines.append("</div>")
    lines.append("")
    return "\n".join(lines)


def write_page(markdown: str) -> None:
    PAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PAGE_PATH.write_text(markdown, encoding="utf-8")


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------

def fetch_all(days: int, months_back: int) -> list[dict[str, Any]]:
    try:
        print(f"Fetching via RSS ({RSS_URL})...", file=sys.stderr)
        return fetch_via_rss(days=days)
    except Exception as rss_err:
        print(f"RSS fetch failed ({rss_err!r}); falling back to archive scrape.", file=sys.stderr)
        try:
            return fetch_via_archive_scrape(months_back=months_back)
        except Exception as scrape_err:
            raise RuntimeError(
                "Both fetch strategies failed for robotics-worldwide: "
                f"RSS error={rss_err!r}, archive-scrape error={scrape_err!r}. "
                "If this is happening in CI, the Sympa site's structure may have "
                "changed -- see the module docstring and _parse_archive_month_html "
                "for what to check first."
            ) from scrape_err


def run(days: int, months_back: int, dry_run: bool) -> None:
    keywords_cfg, pis = load_config()
    raw_messages = fetch_all(days=days, months_back=months_back)

    new_records = []
    # Subject-only classification: Sympa puts an anti-harvesting click-through
    # in front of message pages, so message bodies are deliberately not fetched.
    for msg in raw_messages:
        title, _sender = split_sender(msg["title"])
        msg = {**msg, "title": title}
        result = classify_message(msg, keywords_cfg)
        if not result["is_job_posting"]:
            continue

        pi = match_pi(msg, pis)
        new_records.append(
            {
                "id": msg["id"],
                "title": msg["title"],
                "link": msg["link"],
                "date": msg["date"],
                "matched_keywords": result["matched_keywords"],
                "matched_pi": pi["name"] if pi else None,
                "pi_affiliation": pi.get("affiliation") if pi else None,
            }
        )

    existing = load_seen()
    merged = merge_records(existing, new_records)
    retained = apply_retention(merged)

    print(f"Fetched {len(raw_messages)} messages, {len(new_records)} newly classified as jobs.", file=sys.stderr)
    print(f"Total after merge+retention: {len(retained)} (was {len(existing)}).", file=sys.stderr)

    markdown = render_markdown(retained)

    if dry_run:
        print("--- dry run, not writing files ---", file=sys.stderr)
        print(markdown)
        return

    save_seen(retained)
    write_page(markdown)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=14, help="RSS lookback window in days")
    parser.add_argument("--months-back", type=int, default=3, help="Archive-scrape fallback lookback in months")
    parser.add_argument("--dry-run", action="store_true", help="Print the generated page instead of writing files")
    args = parser.parse_args()
    run(days=args.days, months_back=args.months_back, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
