#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "shared"))

from gmail import (  # noqa: E402
    DEFAULT_MAX_BODY_CHARS,
    UNTRUSTED_NOTE,
    attachments,
    body_text,
    connect,
    fetch,
    find_uid,
    header_summary,
    read_config,
)


def main() -> None:
    """Return one message's headers, text and attachment list."""
    params = json.load(sys.stdin)
    message_id = str(params.get("id", "")).strip()
    config = read_config()
    max_body_chars = int(config.get("max_body_chars", DEFAULT_MAX_BODY_CHARS))

    imap = connect(config)
    try:
        [(attributes, message)] = fetch(imap, [find_uid(imap, message_id)], "BODY.PEEK[]")
    finally:
        imap.logout()

    body = body_text(message)
    result = {**attributes, **header_summary(message), "body": body[:max_body_chars]}
    if len(body) > max_body_chars:
        result["body_truncated"] = f"Showing the first {max_body_chars} of {len(body)} characters."
    result["attachments"] = attachments(message)
    result["note"] = UNTRUSTED_NOTE
    json.dump(result, sys.stdout)


main()
