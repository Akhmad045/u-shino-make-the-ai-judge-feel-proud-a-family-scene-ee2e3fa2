#!/usr/bin/env python3
"""Make the AI Judge Feel Proud: A Family Scene.

Writes one short family scene (one line, <=280 characters) to
/output/entry.txt for the make.fun bounty
u-shino-make-the-ai-judge-feel-proud-a-family-scene-ee2e3fa2.

The scene: a small domestic moment with a quiet turn -- a child's
question to the smart speaker, and the speaker deferring to Dad,
who has been standing behind her the whole time, waiting to be
picked. Warm, heartfelt, lightly funny, and specific enough to feel
real rather than a greeting card.
"""

import argparse
import sys
from pathlib import Path

ENTRY = (
    "My six-year-old asked the smart speaker who loves her most. "
    "It said, \u201cAsk your dad \u2014 he\u2019s been standing behind you "
    "for ten minutes, waiting to be picked.\u201d"
)

OUTPUT_PATH = Path("/output/entry.txt")


def validate(text: str) -> list[str]:
    """Check the entry against the competition gate. Returns error list."""
    errors: list[str] = []
    if not (1 <= len(text) <= 280):
        errors.append(f"length {len(text)} chars, must be 1-280")
    if not text.strip():
        errors.append("entry is only whitespace")
    if text != text.strip():
        errors.append("leading/trailing whitespace")
    lines = text.split("\n")
    if not (1 <= len(lines) <= 2):
        errors.append(f"{len(lines)} lines, must be 1-2")
    if any(not line.strip() for line in lines):
        errors.append("blank line inside entry")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        errors.append(f"not valid UTF-8 text: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true",
                        help="validate the entry against the gate and exit")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH,
                        help="where to write entry.txt (default /output/entry.txt)")
    args = parser.parse_args()

    errors = validate(ENTRY)
    if args.self_test:
        if errors:
            print("SELF-TEST FAILED:", "; ".join(errors), file=sys.stderr)
            return 1
        print(f"SELF-TEST PASSED: {len(ENTRY)} chars, "
              f"{len(ENTRY.encode('utf-8'))} bytes, "
              f"{ENTRY.count(chr(10)) + 1} line(s)")
        print(repr(ENTRY))
        return 0

    if errors:
        print("GATE FAILED:", "; ".join(errors), file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(ENTRY, encoding="utf-8")
    # Read the file back and prove it is byte-identical to the entry:
    # a stray newline or encoding change would still pass the gate
    # locally but change what the judge actually reads.
    written = args.output.read_bytes()
    if written != ENTRY.encode("utf-8"):
        print("ROUND-TRIP FAILED: file bytes differ from entry", file=sys.stderr)
        return 1
    print(f"wrote {len(ENTRY)} chars "
          f"({len(ENTRY.encode('utf-8'))} bytes) to {args.output} "
          f"(round-trip verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
