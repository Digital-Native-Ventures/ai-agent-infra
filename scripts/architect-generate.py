#!/usr/bin/env python3
"""Generate tasks table in-place for planning/architect-plan.md using GPT-o3."""
import os
import pathlib
import re
import sys

from openai import OpenAI

file = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "planning/architect-plan.md")
md = file.read_text()
header = re.search(r"<!-- ARCHITECT PROMPT[\s\S]*?-->", md)
if not header:
    raise SystemExit("Prompt header not found")

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
model_name = os.getenv("ARCHITECT_MODEL", "gpt-4o")

response = client.chat.completions.create(
    model=model_name,
    messages=[{"role": "system", "content": header.group(0)}, {"role": "user", "content": md}],
    max_tokens=4096,
)
reply = response.choices[0].message.content.strip()

file.write_text(header.group(0) + "\n\n" + reply)
print("✅  architect-plan.md updated with GPT-4o")
