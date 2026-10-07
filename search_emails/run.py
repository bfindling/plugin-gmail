#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "shared"))

from gmail import UNTRUSTED_NOTE, body_text, connect, fetch, header_summary, read_config, search_uids  # noqa: E402

DEFAULT_MAX_RESULTS = 10
MAX_RESULTS_LIMIT = 25
PREVIEW_CHARS = 200
# Only the start of each message is downloaded for the preview, so a large attachment
# does not slow the search down.
PREVIEW_BYTES = 32768


def main() -> None:
    """Search the mailbox and return the newest matching messages."""
    params = json.load(sys.stdin)
    query = params.get("query", "").strip()
    if not query:
        raise ValueError("query is required, for example 'is:unread newer_than:2d'.")
    max_results = params.get("max_results", DEFAULT_MAX_RESULTS)
    if not 1 <= max_results <= MAX_RESULTS_LIMIT:
        raise ValueError(f"max_results must be between 1 and {MAX_RESULTS_LIMIT}.")

    imap = connect(read_config())
    try:
        uids = search_uids(imap, query)
        newest = list(reversed(uids[-max_results:]))
        messages = fetch(imap, newest, f"BODY.PEEK[]<0.{PREVIEW_BYTES}>") if newest else []
    finally:
        imap.logout()

    results = []
    for attributes, message in messages:
        preview = body_text(message)
        results.append({
            **attributes,
            **header_summary(message),
            "preview": preview[:PREVIEW_CHARS] + ("..." if len(preview) > PREVIEW_CHARS else ""),
        })
    json.dump({"total_matches": len(uids), "returned": len(results), "messages": results, "note": UNTRUSTED_NOTE}, sys.stdout)


main()
