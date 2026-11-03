"""Demo run using synthetic mailing-list messages, for previewing the page
without network access. Exercises the REAL classify/match_pi/retention/render
code from fetch_jobs.py -- only the network fetch step is mocked out.

Usage:
    python demo_run.py            writes demo_output/careers/index.md (safe, git-ignored)
    python demo_run.py --to-site  OVERWRITES src/careers.md with the demo page, so you
                                  can preview it in `mkdocs serve`. Do not commit the
                                  result; a real run of fetch_jobs.py replaces it.
"""
import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src" / "scripts"))
import fetch_jobs as fj

TODAY = dt.date(2026, 8, 3)


def days_ago(n):
    return (TODAY - dt.timedelta(days=n)).isoformat()


MOCK_MESSAGES = [
    {
        "id": "msg-001",
        "title": "[robotics-worldwide] [jobs] PhD position in optimal control at TU Delft",
        "link": "https://www.lists.kit.edu/sympa/arc/robotics-worldwide/2026-07/msg00042.html",
        "date": days_ago(5),
        "summary": "We are hiring a PhD student to work on optimal control for legged locomotion, joint work with Prof. Melanie Zeilinger.",
    },
    {
        "id": "msg-002",
        "title": "[robotics-worldwide] [jobs] Postdoc opening: reinforcement learning for manipulation",
        "link": "https://www.lists.kit.edu/sympa/arc/robotics-worldwide/2026-07/msg00051.html",
        "date": days_ago(9),
        "summary": "Postdoc position in reinforcement learning and trajectory optimization, group of Jan Peters at TU Darmstadt.",
    },
    {
        "id": "msg-003",
        "title": "[robotics-worldwide] [meetings] Call for papers: workshop on optimal control at ICRA 2027",
        "link": "https://www.lists.kit.edu/sympa/arc/robotics-worldwide/2026-07/msg00060.html",
        "date": days_ago(6),
        "summary": "We invite submissions on optimal control and MPC for the ICRA 2027 workshop.",
    },
    {
        "id": "msg-004",
        "title": "[robotics-worldwide] [jobs] PhD position in computer vision for autonomous driving",
        "link": "https://www.lists.kit.edu/sympa/arc/robotics-worldwide/2026-07/msg00070.html",
        "date": days_ago(3),
        "summary": "We are hiring a PhD student in computer vision and perception for autonomous driving.",
    },
    {
        "id": "msg-005",
        "title": "[robotics-worldwide] [jobs] Research engineer position: numerical optimization for locomotion",
        "link": "https://www.lists.kit.edu/sympa/arc/robotics-worldwide/2025-09/msg00012.html",
        "date": days_ago(340),  # inside the 365-day window -> still shown
        "summary": "Research engineer position, whole-body control and numerical optimization, industry lab.",
    },
    {
        "id": "msg-006",
        "title": "[robotics-worldwide] [jobs] Faculty position in robot dynamics and control",
        "link": "https://www.lists.kit.edu/sympa/arc/robotics-worldwide/2025-06/msg00003.html",
        "date": days_ago(400),  # outside the 365-day window -> dropped
        "summary": "Open faculty position, robot dynamics, contact-implicit trajectory optimization.",
    },
]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--to-site", action="store_true", help="overwrite src/careers.md instead of writing to demo_output/")
    args = ap.parse_args()

    keywords_cfg, pis = fj.load_config()

    new_records = []
    for msg in MOCK_MESSAGES:
        result = fj.classify_message(msg, keywords_cfg)
        print(f"- {msg['title'][:70]:70s} -> is_job_posting={result['is_job_posting']}")
        if not result["is_job_posting"]:
            continue
        pi = fj.match_pi(msg, pis)
        new_records.append({
            "id": msg["id"],
            "title": msg["title"],
            "link": msg["link"],
            "date": msg["date"],
            "matched_keywords": result["matched_keywords"],
            "matched_pi": pi["name"] if pi else None,
            "pi_affiliation": pi.get("affiliation") if pi else None,
        })

    retained = fj.apply_retention(new_records, as_of=TODAY)
    print(f"\n{len(new_records)} classified as jobs, {len(retained)} retained after 365-day window.\n")

    markdown = fj.render_markdown(retained, generated_at=TODAY)

    if args.to_site:
        fj.write_page(markdown)  # writes fj.PAGE_PATH, i.e. src/careers.md
        print(f"Wrote {fj.PAGE_PATH}  (demo data, do not commit)")
    else:
        out_path = Path(__file__).resolve().parent / "demo_output" / "careers" / "index.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(markdown, encoding="utf-8")
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
