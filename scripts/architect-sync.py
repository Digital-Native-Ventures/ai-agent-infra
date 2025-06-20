#!/usr/bin/env python3
import pathlib
import re
import sys

PLAN = pathlib.Path("planning/architect-plan.md")
QUEUE = pathlib.Path("tasks/task-queue.md")

md = PLAN.read_text()
m = re.search(r"\| Status \| ID .*?\n(\|.*\n)+", md)
if not m:
    raise SystemExit("Task table not found in plan")

table = m.group(0).strip() + "\n"
if QUEUE.exists() and QUEUE.read_text() == table:
    print("Queue already up-to-date")
    sys.exit(0)

QUEUE.write_text(table)
print("Queue synced from plan")
