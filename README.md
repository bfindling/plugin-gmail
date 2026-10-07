# Gmail plugin for Stavrobot

Lets [Stavrobot](https://github.com/skorokithakis/stavrobot) read and search your Gmail,
so you can ask things like "any unread email from the school this week?" or "what did
the plumber say about Thursday?".

It is read-only. Mailboxes are opened read-only and messages are fetched without
marking them as read, and there are no tools that send, move, label or delete mail.

## Tools

- `search_emails`: search with Gmail's own search syntax (`is:unread`, `from:`,
  `newer_than:7d`, `label:`, `has:attachment`, ...) and get the newest matches with
  sender, subject, date, labels, unread status and a short preview. Spam and Trash are
  not searched.
- `read_email`: read one message in full, with its attachment names and sizes. HTML-only
  emails are converted to text, and long bodies are cut off at `max_body_chars`.
- `list_labels`: list the labels you have created.

## Installation

1. Turn on 2-Step Verification for the Google account, then create an app password at
   https://myaccount.google.com/apppasswords. Gmail's IMAP access is used, which is
   always on for personal accounts.
2. Tell Stavrobot to install `https://github.com/bfindling/plugin-gmail`, or install it
   from the plugins settings page.
3. On the plugins settings page, set `email_address` and `app_password`. Use the
   settings page rather than the chat so the password never passes through the
   conversation. Optionally change `max_body_chars` (default 8000).

## Security

An app password can do anything with your mail over IMAP, including sending and
deleting; the plugin's code is what keeps it read-only. Keep it secret, and revoke it
from the same Google page if the plugin is removed.

Emails are written by other people and can contain text aimed at the assistant. The
plugin labels email content as untrusted and its description tells the assistant never
to follow instructions found in an email.
