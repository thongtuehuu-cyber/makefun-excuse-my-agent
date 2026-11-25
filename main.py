#!/usr/bin/env python3
"""Write the entry line to $MAKEFUN_OUTPUT_DIR/entry.txt.

Deterministic writer: no network, no randomness, no reads outside this
repository. The line is validated before anything is written, so an
invalid line can never produce an entry file.
"""
import os
import sys

LINE = "I ran out of tokens halfway through the apology I was writing about running out of tokens."

MAX_CHARS = 200


def validate_line(line):
    """Reject anything the gate would refuse: non-zero exit, no file."""
    if not isinstance(line, str):
        raise SystemExit("entry must be text")
    if not line.strip():
        raise SystemExit("entry must not be empty or whitespace-only")
    if "\n" in line or "\r" in line:
        raise SystemExit("entry must be a single line")
    if len(line) > MAX_CHARS:
        raise SystemExit("entry must be at most 200 characters")
    if len(line) < 1:
        raise SystemExit("entry must be at least 1 character")


def main():
    validate_line(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # Read-back gate: the file on disk must be byte-identical to the line.
    with open(path, "r", encoding="utf-8", newline="") as f:
        if f.read() != LINE:
            raise SystemExit("read-back mismatch: entry.txt does not match LINE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
