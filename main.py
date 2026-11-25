#!/usr/bin/env python3
"""The Router Confesses — make.fun entry.

Writes one line to /output/entry.txt: an excuse a home Wi-Fi router gives
for dropping the connection at the climax of a movie.

Gate (RULES.txt): the file must be UTF-8 text of 1-200 characters, not
only whitespace. This program validates the line against that gate before
writing anything, and fails loudly instead of writing an invalid file.

Standard library only. No network, no model calls. Deterministic: the
same line, byte for byte, on every run.
"""

import sys
from pathlib import Path

LINE = (
    "I dropped the movie on purpose \u2014 after three years ignored "
    "behind the couch, I wanted to be the cliffhanger for once."
)

OUTPUT_PATH = Path("/output/entry.txt")

MAX_CHARS = 200


def validate_line(line: str) -> str:
    """Check one line against the gate. Returns the line or raises."""
    if not isinstance(line, str):
        raise TypeError(f"entry must be str, got {type(line).__name__}")
    if not line.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line (no newline characters)")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("entry must not contain control characters")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(line)} characters, over the {MAX_CHARS} limit"
        )
    line.encode("utf-8")  # raises UnicodeEncodeError on lone surrogates
    return line


def write_entry(line: str, target: Path) -> Path:
    """Validate the line, then write it exactly (no trailing newline)."""
    validate_line(line)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(line.encode("utf-8"))
    return target


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    target = Path(args[0]) if args else OUTPUT_PATH
    write_entry(LINE, target)
    print(f"{LINE} ({len(LINE)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
