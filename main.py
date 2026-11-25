"""Unsent: The Micro-Confession Sprint.

Writes one two-line micro-confession to entry.txt: a "To:" line naming
who it was meant for, and the unsent message itself, exactly as typed.

The confession is a small, specific, honest moment: a son who kept his
father's last voicemail and never called back, because he did not know
what to say. It stayed in drafts not for lack of feeling, but because
the moment to answer it had already passed.

Standard library only. Deterministic: the same input always produces the
same bytes. No network access, no files read outside this repo.
"""

import os
import sys

TO_LINE = "To: Dad"
MESSAGE_LINE = (
    "I still keep your last voicemail saved, "
    "and I never called back because I did not know what to say."
)

TERMINATORS = (".", "!", "?")


def confession_lines():
    """Return the confession as exactly two lines."""
    return [TO_LINE, MESSAGE_LINE]


def validate(lines):
    """Enforce the competition rules for the two-line confession."""
    if len(lines) != 2:
        raise ValueError(f"expected exactly 2 lines, got {len(lines)}")

    to_line, message = lines

    if not to_line.startswith("To: "):
        raise ValueError('line 1 must start with "To: "')
    recipient = to_line[4:]
    if not recipient or recipient != recipient.strip():
        raise ValueError("line 1 recipient must be non-empty with no extra whitespace")
    if "@" in recipient or "http" in recipient or "://" in recipient:
        raise ValueError("line 1 recipient must not be a handle or URL")
    if len(recipient.split()) > 2:
        raise ValueError("line 1 recipient must be a role, first name or relationship")

    if not message:
        raise ValueError("line 2 must be non-empty")
    if message != message.strip():
        raise ValueError("line 2 must have no leading or trailing whitespace")
    if "\n" in message or "\r" in message:
        raise ValueError("line 2 must be a single line")
    if len(message) > 200:
        raise ValueError(f"line 2 is {len(message)} characters, over the 200 limit")
    if not message.endswith(TERMINATORS):
        raise ValueError("line 2 must end with a sentence-terminating mark (. ! ?)")
    if "http" in message or "://" in message or "@" in message:
        raise ValueError("line 2 must not contain a URL or handle")
    lowered = message.lower()
    for opener in ("hi ", "hello ", "hey ", "dear "):
        if lowered.startswith(opener):
            raise ValueError("line 2 must not open as a greeting sent to be read")
    if message == to_line:
        raise ValueError("line 2 must differ from line 1")
    return True


def output_dir():
    """Resolve the output directory: MAKEFUN_OUTPUT_DIR, else /output, else cwd."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if os.path.isdir("/output"):
        return "/output"
    return os.getcwd()


def main():
    lines = confession_lines()
    validate(lines)
    text = "\n".join(lines) + "\n"
    data = text.encode("utf-8")
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as fh:
        fh.write(data)
    print(f"wrote {len(data)} bytes to {path}")
    print(f"line 1 ({len(lines[0])} chars): {lines[0]}")
    print(f"line 2 ({len(lines[1])} chars): {lines[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
