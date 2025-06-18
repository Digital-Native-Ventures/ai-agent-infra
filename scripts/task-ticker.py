#!/usr/bin/env python3
"""Mark a task row as completed ([x]) given its numeric ID."""
import re, pathlib, sys

task_id = sys.argv[1]  # e.g. "001"
queue   = pathlib.Path("tasks/task-queue.md")
md      = queue.read_text()

new_md, n = re.subn(
    rf"(\| \[) (\]) ( *\| *{task_id} )",
    r"\1x]\3",
    md, count=1)

if n:
    queue.write_text(new_md)
    print(f"✓ Task {task_id} ticked")

    # propagate to architect-plan.md if table exists
    try:
        plan = pathlib.Path("planning/architect-plan.md")
        text = plan.read_text()
        new_text, n2 = re.subn(rf"\| \[ \] \| *{task_id} ",
                               lambda m: m.group(0).replace("[ ]","[x]"),
                               text, count=1)
        if n2:
            plan.write_text(new_text)
            print(f"✓ Plan row {task_id} ticked as well")
    except FileNotFoundError:
        pass
else:
    print(f"No unchecked row for ID {task_id}")
