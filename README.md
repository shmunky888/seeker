# SeeYou

A local HTTP server that generates Telegram-style invite pages and logs visitor information (IP, OS, browser) when they interact with the page.

## Requirements

- Python 3 (no external dependencies)

## Usage

```bash
python3 seeker.py
```

1. Select a template (currently only "telegram")
2. Customize the group title, description, member counts, and optional avatar
3. The server starts and provides two URLs:
   - **Local Access URL** — opens automatically in your browser
   - **Network Access URL** — share this with others on the same network
4. When a visitor clicks the action button, their info is printed to your terminal:
   ```
   [+] Public IP: 1.2.3.4
   [+] OS: iOS
   [+] Browser: Safari
   ```

## How It Works

- `seeker.py` — Starts a threaded HTTP server on port 8080 (auto-increments if busy)
- `index.html` — The invite page; content is driven entirely by URL query parameters

The page fetches the visitor's public IP via [ipify](https://www.ipify.org/) before sending it to the `/log` endpoint, which parses the User-Agent and prints visitor details.

## URL Parameters

| Parameter   | Description              | Default                          |
|-------------|--------------------------|----------------------------------|
| `title`     | Group/channel name       | telegram VIP Signals              |
| `desc`      | Group description        | Official telegram channel...     |
| `members`   | Member count display     | 185,420                          |
| `online`    | Online count display     | 4,219                            |
| `avatar`    | Image URL for avatar     | (initials from title)            |
| `verified`  | Show verified badge      | 1 (set to 0 to hide)             |
| `platform`  | Theme/mode               | tg_light                         |
