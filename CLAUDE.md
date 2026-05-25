# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview
A Python-based local HTTP server that generates Telegram-style invite pages. Visitors clicking action buttons log their IP/OS/browser to the terminal. Core components:
- **`seeker.py`**: Main script handling server setup, template customization, and visitor logging
- **`index.html`**: Dynamic invite page generated with query parameters
- **`index.php`**: Broken alternate version (not used)

## Common Commands
- `python3 seeker.py`: Start server and launch template configuration
- `Ctrl+C` in terminal: Stop active server and return to home

## Key Architecture
1. **Template System**: Server presents pre-configured templates (currently only "telegram") with customizable fields
2. **Dynamic Content**: `index.html` generates pages using URL query parameters (title, description, members)
3. **Visitor Tracking**: `/log` endpoint fetches public IP via ipify API and logs geolocation data
4. **Security**: Filters private IP ranges and sanitizes user-agent data

## Implementation Notes
- Browser/OS detection uses User-Agent parsing
- Trace mode enables detailed IP geolocation lookup
- Error handling suppresses connection-related exceptions
- Templates use CSS custom properties for theming (currently limited to light mode)

## Development Workflow

### Development Commands
- **Run server (default mode):** `python3 seeker.py`
- **Enable trace mode:** select option `1` at the startup menu, then follow prompts to lookup IPs.
- **Stop server:** press **Enter** when prompted (`Waiting for Client...`) or use `Ctrl+C`.
- **Run server on a specific port:** set `PORT` env var or modify `find_free_port` default in code.
- **Run a quick lint check:** `python -m py_compile $(git ls-files "*.py")`
- **Run a single test (if tests added):** `python -m unittest path/to/test_module.py`

### High-level Architecture
- **seeker.py** – Entry point; sets up a threaded HTTP server, handles CLI configuration, and manages server lifecycle.
- **CustomHTTPRequestHandler** – Serves `index.html`, redirects root requests, and handles `/log` endpoint where visitor IP, OS, and browser are extracted from query parameters.
- **IP lookup** – `lookup_ip` contacts `ip-api.com` (unless the IP is private) and, when trace mode is enabled, prints detailed geolocation info.
- **Template system** – Query parameters are used to populate `index.html` with customizable fields (title, description, member counts, etc.).
- **Server utilities** – Helpers for finding a free port, obtaining the local IP address, and cleanly shutting down active servers.
- **Trace mode flag** – Global `trace_enabled` toggles verbose logging of visitor details.

1. Run `python3 seeker.py` to start server on random port (default 8080)
2. Configure template values via CLI interface
3. Visit generated URL to test invite page
4. Monitor terminal for visitor logs
