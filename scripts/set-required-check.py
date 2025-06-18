#\!/usr/bin/env python3
import os, sys, requests, json
check, owner, repo, branch = sys.argv[1:]
token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
url = f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks"
data = {"strict": True, "contexts": [check]}
r = requests.patch(url,
    headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    data=json.dumps(data))
r.raise_for_status()
print(f"✔ Required check '{check}' enabled on {branch}")
PY < /dev/null
