#!/usr/bin/env python3
import os, sys, re, pathlib, anthropic
file = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "planning/architect-plan.md")
md   = file.read_text()
header = re.search(r"<!-- ARCHITECT PROMPT[\s\S]*?-->", md)
if not header: raise SystemExit("Prompt header not found")
client = anthropic.Client(api_key=os.environ["ANTHROPIC_API_KEY"])
reply  = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    system=header.group(0),
    messages=[{"role":"user","content":md}],
    max_tokens=4096,
).content[0].text.strip()
file.write_text(header.group(0) + "\n\n" + reply)
print("✅  architect-plan.md updated")
