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
1. Run `python3 seeker.py` to start server on random port (default 8080)
2. Configure template values via CLI interface
3. Visit generated URL to test invite page
4. Monitor terminal for visitor logs
