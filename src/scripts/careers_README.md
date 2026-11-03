# TC OptRob careers page pipeline

Generates `src/careers.md` for the [tcoptrob.github.io](https://github.com/tcoptrob/tcoptrob.github.io)
site from recent robotics-worldwide mailing-list postings that match the
TC's keywords. See `career-page-design.md` (also in the Claude project) for the
full design writeup and current status.

## Layout (repo root = site repo)

```
mkdocs.yml                      docs_dir: src; add extra_css, nav entry, exclude_docs (below)
requirements.txt                pipeline dependencies
demo_run.py                     offline preview with synthetic data
.github/workflows/careers-page.yml
src/
  careers.md                    GENERATED page (cards)
  stylesheets/careers.css
  scripts/fetch_jobs.py
  data/keywords.yaml
  data/pis.yaml
  data/jobs_seen.json           GENERATED dedup ledger
  tests/test_pipeline.py
```

## How it works

1. `src/scripts/fetch_jobs.py` fetches recent messages (Sympa RSS first, HTML
   archive scrape as fallback -- see the module docstring).
2. A message is classified as a job posting only if its subject carries the
   list's `[jobs]` tag **and** contains a TC-relevance keyword (optimal
   control, robot learning, ...), both editable in `src/data/keywords.yaml`.
   Only the subject is used: the RSS feed has no message text, and the
   archive's message pages sit behind Sympa's anti-harvesting click-through,
   which this pipeline deliberately does not bypass.
3. Messages mentioning a name from `src/data/pis.yaml` are highlighted with an accent bar and the PI's name and affiliation.
4. Postings are kept for a rolling 365-day window from their post date, then
   dropped automatically (mailing lists don't reliably signal "closed", so
   one window covers both active and recently-closed postings).
5. The script regenerates `src/careers.md` (a scrollable list of HTML cards,
   styled by `src/stylesheets/careers.css`) and updates `src/data/jobs_seen.json`.
6. `.github/workflows/careers-page.yml` runs every Monday 06:00 UTC and opens
   a pull request with the diff -- nothing publishes without a committee
   member merging it.

## mkdocs.yml changes

```yaml
docs_dir: src

extra_css:
  - stylesheets/careers.css

nav:
  - Careers: careers.md      # add alongside existing entries

# Keep pipeline code and data out of the published site:
exclude_docs: |
  scripts/
  data/
  tests/
```

(Without `exclude_docs`, MkDocs copies every non-Markdown file under `src/`,
including the scripts and JSON, into the built site.)

## Setup in the site repo

1. Copy the files above into the repo root, keeping the layout.
2. Apply the `mkdocs.yml` changes.
3. Sanity-check locally from a normal network, from the repo root:
   ```
   pip install -r requirements.txt
   python src/scripts/fetch_jobs.py --dry-run
   ```
4. Preview the page without network: `python demo_run.py` (synthetic data,
   writes `demo_output/careers/index.md`), or `python demo_run.py --to-site` to
   overwrite `src/careers.md` with the demo page and view it in `mkdocs serve`
   (don't commit it; a real run replaces it).

## Before going live

- The RSS fetch has been checked against the live Sympa server (it returns
  titles, links and dates; no message text). The archive-scrape fallback is
  still unverified, and would hit the same anti-harvesting page as message
  links, so treat it as non-functional.
- The GitHub Action has not been run yet. It needs the workflow file added to
  the repo, and "Allow GitHub Actions to create and approve pull requests"
  enabled under Settings > Actions > General.
- Consider asking the robotics-worldwide moderators whether automated reads
  are fine, and whether full message text can be made available.
- EURON is out of scope (subscriber-only archive; no mailbox by design).

## Known limitations

Subject-only matching misses relevant postings whose subject names no TC
keyword (e.g. "Postdoctoral Position at Rice University"). Full text would
need the moderators' permission for automated access.

Keyword matching is plain substring matching with no negation handling, so
"no optimization focus" still counts as an "optimization" hit. Review the
weekly PRs for false positives.

## Data files

- `src/data/pis.yaml` -- 77 PIs seeded from the TC_Speakers roster (name /
  affiliation / keywords). Hand-editable.
- `src/data/keywords.yaml` -- job-signal and TC-relevance phrase lists.

## Tests

```
pip install -r requirements.txt pytest
python -m pytest src/tests/ -v
```
