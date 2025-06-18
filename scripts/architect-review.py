#!/usr/bin/env python3
"""Approve or request changes on a PR using GPT-4o."""
import os, subprocess, sys, pathlib, textwrap, json
from openai import OpenAI

pr_number = os.environ.get("GITHUB_REF_NAME", "").replace("refs/pull/", "").split("/")[0]
if not pr_number:
    # fallback: get PR number from branch name or github context
    pr_number = subprocess.check_output(["gh", "pr", "list", "--head", os.environ.get("GITHUB_HEAD_REF", ""), "--json", "number", "--jq", ".[0].number"]).decode().strip()

pr_diff = subprocess.check_output(["gh", "pr", "diff", pr_number, "--color=never"]).decode()
task_row = os.environ.get("TASK_ROW", "")
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
model = os.getenv("ARCHITECT_MODEL", "gpt-4o")

prompt = textwrap.dedent(f"""
You are Architect-Reviewer. Original task row:
{task_row}

Review the diff below. If it satisfies the task, reply with JSON: {{"approve": true, "comment": "<one-line>"}}
Else reply {{ "approve": false, "comment": "<why>" }}.

DIFF:
```patch
{pr_diff}
""")

resp = client.chat.completions.create(
    model=model,
    messages=[{"role":"user","content":prompt}],
    max_tokens=256,
)
result = json.loads(resp.choices[0].message.content)
print(result)
if result.get("approve"):
    subprocess.run(["gh", "pr", "review", pr_number, "--approve", "--body", result["comment"]], check=True)
    if os.getenv("AUTO_MERGE") == "true":
        subprocess.run(["gh", "pr", "merge", pr_number, "--auto", "--squash"], check=True)
else:
    subprocess.run(["gh", "pr", "review", pr_number, "--request-changes", "--body", result["comment"]], check=True)
