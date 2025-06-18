#\!/usr/bin/env python3
"""Approve or request changes on a PR using GPT-o3."""
import os, subprocess, openai, sys, pathlib, textwrap, json

pr_diff = subprocess.check_output(["gh", "pr", "diff", "--color=never"]).decode()
task_row = os.environ.get("TASK_ROW", "")
openai.api_key = os.environ["OPENAI_API_KEY"]
model = os.getenv("ARCHITECT_MODEL", "gpt-o3")

prompt = textwrap.dedent(f"""
You are Architect-Reviewer. Original task row:
{task_row}

Review the diff below. If it satisfies the task, reply with JSON: {{"approve": true, "comment": "<one-line>"}}
Else reply {{ "approve": false, "comment": "<why>" }}.

DIFF:
```patch
{pr_diff}
""")

resp = openai.chat.completions.create(
model=model,
messages=[{"role":"user","content":prompt}],
max_tokens=256,
)
result = json.loads(resp.choices[0].message.content)
print(result)
if result.get("approve"):
    subprocess.run(["gh", "pr", "review", "--approve", "--body", result["comment"]], check=True)
    if os.getenv("AUTO_MERGE") == "true":
        subprocess.run(["gh", "pr", "merge", "--auto", "--squash"], check=True)
else:
    subprocess.run(["gh", "pr", "review", "--request-changes", "--body", result["comment"]], check=True)
