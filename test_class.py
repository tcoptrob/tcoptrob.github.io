import sys, requests
sys.path.insert(0, "src/scripts")
import fetch_jobs as fj

msgs = fj.fetch_via_rss(days=14)
for m in msgs[:2]:
    r = requests.get(m["link"], headers={"User-Agent": fj.USER_AGENT}, timeout=20)
    print(m["link"])
    print(r.status_code, r.headers.get("content-type"), len(r.text))
    print(r.text[:400].replace("\n", " "))
    print("---")
