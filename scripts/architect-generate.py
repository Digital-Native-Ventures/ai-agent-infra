#\!/usr/bin/env python3
"""Generate tasks table in-place for planning/architect-plan.md."""
import os, sys, re, pathlib, anthropic, json

file = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "planning/architect-plan.md")
md   = file.read_text()

header = re.search(r"<\!-- ARCHITECT PROMPT[\\s\\S]*?-->", md)
if not header:
    raise SystemExit("Prompt header not found")

client  = anthropic.Client(api_key=os.environ["ANTHROPIC_API_KEY"])
reply   = client.messages.create(
    model="gpt-o3",
    system=header.group(0),
    messages=[{"role":"user", "content":md}],
    max_tokens=4096,
).content[0].text.strip()

# Preserve header, replace everything after it
new_md = header.group(0) + "\n\n" + reply
file.write_text(new_md)
print("✅  architect-plan.md updated")
