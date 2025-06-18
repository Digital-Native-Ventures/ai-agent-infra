#\!/usr/bin/env python3
"""Mark a task row as completed ([x]) given its numeric ID."""
import re, pathlib, sys

task_id = sys.argv[1]  # e.g. "001"
queue   = pathlib.Path("tasks/task-queue.md")
md      = queue.read_text()

new_md, n = re.subn(
    rf"(\ < /dev/null |  \[) (\]) \| *{task_id} ",
    lambda m: m.group(0).replace("[ ]", "[x]"),
    md, count=1)

if n:
    queue.write_text(new_md)
    print(f"✓ Task {task_id} ticked")
else:
    print(f"No unchecked row for ID {task_id}")
