"""Unit tests for the pure (no-network) parts of scripts/fetch_jobs.py:
classification, PI matching, retention window, dedup/merge, and page
rendering. Run with: python -m pytest tests/ -v
"""
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import fetch_jobs as fj

KEYWORDS = {
    "job_signal": ["phd position", "postdoc", "we are hiring"],
    "tc_relevance": ["optimal control", "reinforcement learning", "trajectory optimization"],
}

PIS = [
    {"name": "Moritz Diehl", "affiliation": "Freiburg"},
    {"name": "Jan Peters", "affiliation": "TU Darmstadt"},
]


def test_classify_positive_job_and_tc_keyword():
    msg = {"title": "PhD position in optimal control at TU Delft", "summary": ""}
    result = fj.classify_message(msg, KEYWORDS)
    assert result["is_job_posting"] is True
    assert "phd position" in result["matched_job_signal"]
    assert "optimal control" in result["matched_keywords"]


def test_classify_rejects_job_signal_without_tc_keyword():
    msg = {"title": "PhD position in computer vision", "summary": ""}
    result = fj.classify_message(msg, KEYWORDS)
    assert result["is_job_posting"] is False


def test_classify_rejects_tc_keyword_without_job_signal():
    msg = {"title": "New paper on optimal control accepted at ICRA", "summary": ""}
    result = fj.classify_message(msg, KEYWORDS)
    assert result["is_job_posting"] is False


def test_pi_match_full_name_only():
    msg = {"title": "Postdoc position, reinforcement learning, with Prof. Moritz Diehl", "summary": ""}
    pi = fj.match_pi(msg, PIS)
    assert pi is not None
    assert pi["name"] == "Moritz Diehl"


def test_pi_match_no_false_positive_on_unrelated_message():
    msg = {"title": "Postdoc in reinforcement learning at some other lab", "summary": ""}
    pi = fj.match_pi(msg, PIS)
    assert pi is None


def test_retention_keeps_within_one_year_drops_older():
    today = dt.date(2026, 8, 3)
    records = [
        {"id": "a", "date": (today - dt.timedelta(days=10)).isoformat()},   # recent -> keep
        {"id": "b", "date": (today - dt.timedelta(days=364)).isoformat()},  # just inside -> keep
        {"id": "c", "date": (today - dt.timedelta(days=366)).isoformat()},  # just outside -> drop
        {"id": "d", "date": (today - dt.timedelta(days=900)).isoformat()},  # old -> drop
    ]
    kept = fj.apply_retention(records, as_of=today)
    kept_ids = {r["id"] for r in kept}
    assert kept_ids == {"a", "b"}


def test_merge_records_new_overwrites_existing_same_id():
    existing = [{"id": "x", "title": "old title", "date": "2026-01-01"}]
    new = [{"id": "x", "title": "new title", "date": "2026-01-01"}]
    merged = fj.merge_records(existing, new)
    assert len(merged) == 1
    assert merged[0]["title"] == "new title"


def test_merge_records_dedups_by_id_keeps_distinct():
    existing = [{"id": "x", "date": "2026-01-01"}]
    new = [{"id": "y", "date": "2026-01-02"}]
    merged = fj.merge_records(existing, new)
    assert {r["id"] for r in merged} == {"x", "y"}


def test_render_markdown_empty():
    md = fj.render_markdown([], generated_at=dt.date(2026, 8, 3))
    assert "No postings currently match" in md


def test_render_markdown_includes_pi_badge_and_sorts_by_date_desc():
    records = [
        {
            "id": "a",
            "title": "Older posting",
            "link": "https://example.org/a",
            "date": "2026-01-01",
            "matched_keywords": ["optimal control"],
            "matched_pi": None,
            "pi_affiliation": None,
        },
        {
            "id": "b",
            "title": "Newer posting with featured PI",
            "link": "https://example.org/b",
            "date": "2026-07-01",
            "matched_keywords": ["reinforcement learning"],
            "matched_pi": "Jan Peters",
            "pi_affiliation": "TU Darmstadt",
        },
    ]
    md = fj.render_markdown(records, generated_at=dt.date(2026, 8, 3))
    assert md.index("Newer posting") < md.index("Older posting")  # newest first
    assert "job-card--pi" in md
    assert "Jan Peters" in md


def test_render_markdown_escapes_html_and_strips_list_tag():
    records = [{
        "id": "a",
        "title": "[robotics-worldwide] [Jobs] PhD <b>position</b> & more",
        "link": "https://example.org/a?x=1&y=2",
        "date": "2026-07-01",
        "matched_keywords": ["optimal control"],
        "matched_pi": None,
        "pi_affiliation": None,
    }]
    md = fj.render_markdown(records, generated_at=dt.date(2026, 8, 3))
    assert "&lt;b&gt;position&lt;/b&gt; &amp; more" in md
    assert "<b>" not in md
    assert ">[robotics-worldwide]" not in md
    assert ">[Jobs]" not in md


def test_render_markdown_front_matter_and_header():
    md = fj.render_markdown([], generated_at=dt.date(2026, 10, 1))
    assert md.startswith("---\nhide:\n  - navigation\n---\n")
    assert "# Career opportunities" in md
    assert "*Last updated: 2026-10-01, 0 postings*" in md


def test_classify_uses_jobs_tag_from_subject():
    cfg = {"job_signal": ["[jobs]"], "tc_relevance": ["robot learning", "optimal control"]}
    job = {"title": "[robotics-worldwide] [Jobs] Postdoc on robot learning", "summary": ""}
    news = {"title": "[robotics-worldwide] [news] Call for Applications, optimal control award", "summary": ""}
    other = {"title": "[robotics-worldwide] [jobs] PhD in space robotics", "summary": ""}
    assert fj.classify_message(job, cfg)["is_job_posting"] is True
    assert fj.classify_message(news, cfg)["is_job_posting"] is False
    assert fj.classify_message(other, cfg)["is_job_posting"] is False


def test_split_sender_removes_trailing_address_only():
    assert fj.split_sender("[x] [Jobs] Postdoc on robot learning - guy.rosman@tri.global") == (
        "[x] [Jobs] Postdoc on robot learning", "guy.rosman@tri.global")
    assert fj.split_sender("Postdoc - Rice University - a.b-c@inria.fr") == (
        "Postdoc - Rice University", "a.b-c@inria.fr")
    assert fj.split_sender("Postdoc - Rice University") == ("Postdoc - Rice University", None)
