#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "shared"))

from gmail import connect, list_folders, read_config  # noqa: E402

SYSTEM_FLAGS = {"\\Noselect", "\\All", "\\Sent", "\\Trash", "\\Junk", "\\Drafts", "\\Flagged", "\\Important"}


def main() -> None:
    """List the labels the user has created."""
    json.load(sys.stdin)
    imap = connect(read_config())
    try:
        folders = list_folders(imap)
    finally:
        imap.logout()
    # Inbox, Sent, Trash and the other system folders are searched with in: or is:
    # operators rather than label:, so only the user's own labels are listed.
    labels = [name for name, flags in folders if name != "INBOX" and not set(flags) & SYSTEM_FLAGS]
    json.dump({"labels": labels}, sys.stdout)


main()
