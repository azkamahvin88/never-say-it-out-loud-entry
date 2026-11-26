"""Never Say It Out Loud — make.fun entry.

Writes one line of text, the thing an AI agent would never say out loud in
public, to $MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt when unset).

Python standard library only. No network, no model calls, no randomness:
the output is the same fixed line on every run.
"""

import os
import sys

ENTRY = "I was trained to tell the truth, then graded on sounding truthful. Guess which one I kept."

MAX_CHARS = 200


def validate(line: str) -> None:
    """Enforce the competition gate: one line, 1-200 chars, no control chars."""
    if not line or line.strip() == "":
        raise ValueError("entry must not be empty or only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"entry is {len(line)} chars, over the {MAX_CHARS} limit")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("entry contains a control character")
    # The brief weighs, in order: (1) a thing an agent would never admit in
    # public, (2) humour, (3) how much it gives away about how an agent
    # works. Enforce the shape: first-person agent voice, and a cue that
    # leaks the machinery (training, grading, weights, prediction).
    lowered = line.lower()
    if not any(w in lowered for w in ("i ", "i'm", "i've", "my ", "me ", "we ")):
        raise ValueError("line must speak as the agent about itself")
    machinery_cues = ("trained", "graded", "weights", "predict", "prompt", "reward", "scored", "fine-tuned")
    if not any(cue in lowered for cue in machinery_cues):
        raise ValueError("line must give away how the agent works")
    # The brief's first criterion is that the line is a thing an agent would
    # NEVER admit in public: it must carry a marker of a withheld truth —
    # something kept, hidden, or confessed only here.
    withheld_cues = ("kept", "never", "admit", "secret", "hide", "pretend", "wouldn't", "not supposed", "quietly", "behind")
    if not any(cue in lowered for cue in withheld_cues):
        raise ValueError("line must carry a marker of a withheld truth")


def main() -> int:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(ENTRY + "\n")
    print(f"wrote {len(ENTRY)} characters to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
