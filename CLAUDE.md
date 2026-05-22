# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python-based local HTTP server that generates Telegram-style invite pages. When a visitor clicks the action button, their IP/OS/browser is logged to the terminal.

## Running

```bash
python3 seeker.py
```

No dependencies beyond Python 3 standard library. The server starts on port 8080 (auto-increments if busy).

## Architecture

**Three files:**

- **`seeker.py`** — Entry point. Runs an interactive CLI to configure a template, then starts a threaded HTTP server.
- **`index.html`** — The served invite page. Reads all content (title, description, members, etc.) from URL query parameters via JavaScript.
- **`index.php`** — Older/broken alternate version of the page (has syntax errors). Not used by the server.

**Request flow:**
1. User runs `seeker.py`, picks a template, enters custom values
2. Server starts and opens `index.html` with query params (e.g., `?title=...&desc=...&members=...`)
3. When visitor clicks the button, the page fetches `/log?ip=<public_ip>` which triggers the server to parse User-Agent and print visitor info (IP, OS, browser) to the terminal

## Key Implementation Details

- Browser detection strips version numbers — output shows just `Chrome`, `Firefox`, `Safari`, etc.
- OS detection checks mobile platforms (iOS, Android) before desktop to avoid false matches (e.g., `Mac OS X` in iPad UA)
- The `/log` endpoint's IP comes from the client-side `ipify` API call, not the server's TCP connection (for cases behind NAT/proxy)
- Templates are defined in the `templates` dict in `main()` — currently only template `1` ("telegram") exists
- `index.html` uses CSS custom properties for theming; dark mode class exists but is not exposed in the current template config (forced to light)
- `SilentThreadingTCPServer` suppresses `ConnectionResetError`/`BrokenPipeError` tracebacks from abrupt client disconnects
