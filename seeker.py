#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import threading
import time
import sys
import urllib.parse
import urllib.request
import json
import socket
import os
import ipaddress
import logging

def is_private_ip(ip_str: str) -> bool:
    try:
        return ipaddress.ip_address(ip_str).is_private
    except ValueError:
        return True  # Invalid IP → treat as private/skip

def lookup_ip(ip):
    # Skip lookup for local and loopback addresses
    if is_private_ip(ip):
        return {"status": "fail", "message": "Private/Local IP"}
    try:
        url = f"http://ip-api.com/json/{ip}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        return {"status": "fail", "message": str(e)}

def get_local_ip():
    try:
        # Create a dummy socket to detect preferred route IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            # Fallback to local hostname resolution for offline network
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"

def find_free_port(start_port=8080):
    port = start_port
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Set SO_REUSEADDR in case of rapid restarts
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(("", port))
                return port
        except OSError:
            port += 1


# ANSI terminal colors matching the cyberpunk/hacker style in screenshot
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
BOLD = '\033[1m'
RESET = '\033[0m'

class AppState:
    def __init__(self):
        self.trace_enabled: bool = False
        self._servers: list = []
        self._lock = threading.Lock()
    
    def add_server(self, httpd):
        with self._lock:
            self._servers.append(httpd)
            
    def remove_server(self, httpd):
        with self._lock:
            if httpd in self._servers:
                self._servers.remove(httpd)
    
    def stop_all(self):
        with self._lock:
            for httpd in self._servers:
                try:
                    httpd.shutdown()
                    httpd.server_close()
                except Exception as e:
                    logging.warning(f"Error stopping server: {e}")
            self._servers.clear()


BANNER = f"""{RED}{BOLD}
      .---.
     /     \\
     \\_.._/
     | || |
  _.-| || |-._
.'   | || |   '.
|    | || |    |
|    | || |    |
'.   | || |   .'
  '-.| || |.-'
     |_||_|
     | || |
     | || |
     | || |
{RESET}{CYAN}      [ SEER INVITE TEMPLATE TOOL ]{RESET}
"""


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler that silences standard terminal logs for a clean console,
    and automatically redirects the root path '/' to '/index.html' while preserving query params."""
    def log_message(self, format, *args):
        pass

    @property
    def _routes(self):
        return {
            "/log": self._handle_log,
            "/": self._handle_root
        }
        
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        handler = self._routes.get(parsed.path, self._serve_file)
        handler(parsed)

    def _handle_log(self, parsed):
        client_ip = self._extract_ip(parsed)
        ua = self.headers.get("User-Agent", "")
        self.server.on_visitor(client_ip, ua)
        self._respond(200, "text/plain", b"OK")

    def _handle_root(self, parsed):
        target = f"/index.html?{parsed.query}" if parsed.query else "/index.html"
        self.send_response(302)
        self.send_header("Location", target)
        self.end_headers()

    def _serve_file(self, parsed):
        super().do_GET()

    def _extract_ip(self, parsed) -> str:
        parsed_qs = urllib.parse.parse_qs(parsed.query)
        return parsed_qs.get('ip', [self.client_address[0]])[0]

    def _respond(self, code: int, content_type: str, body: bytes):
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.end_headers()
        self.wfile.write(body)

class SilentThreadingTCPServer(socketserver.ThreadingTCPServer):
    """Threading TCP Server that suppresses noisy ConnectionResetError exceptions
    caused by abrupt client network drops or browser socket closures."""
    allow_reuse_address = True

    def handle_error(self, request, client_address):
        exc_type, _, _ = sys.exc_info()
        if exc_type and issubclass(exc_type, (ConnectionResetError, BrokenPipeError, ConnectionAbortedError)):
            return
        # Suppress other connection-related traceback printouts to maintain a clean console
        pass

    def on_visitor(self, client_ip: str, ua: str):
        # Detect OS from User-Agent (mobile checks first to avoid false matches)
        if 'iPhone' in ua or 'iPad' in ua:
            os_info = 'iOS'
        elif 'Android' in ua:
            os_info = 'Android'
        elif 'Windows' in ua:
            os_info = 'Windows'
        elif 'Mac OS X' in ua:
            os_info = 'macOS'
        elif 'Linux' in ua:
            os_info = 'Linux'
        else:
            os_info = 'Unknown'

        # Detect browser and version from User-Agent
        def extract_version(token):
            start = ua.find(token)
            if start == -1:
                return token
            end = ua.find(' ', start)
            if end == -1:
                end = len(ua)
            return ua[start:end].strip(';')

        if 'Edg/' in ua:
            browser = extract_version('Edg/').split('/')[0]
        elif 'OPR/' in ua:
            browser = extract_version('OPR/').split('/')[0]
        elif 'Opera/' in ua:
            browser = extract_version('Opera/').split('/')[0]
        elif 'Chrome/' in ua and 'Edg/' not in ua and 'OPR/' not in ua:
            browser = extract_version('Chrome/').split('/')[0]
        elif 'Firefox/' in ua:
            browser = extract_version('Firefox/').split('/')[0]
        elif 'Safari/' in ua and 'Chrome/' not in ua:
            browser = 'Safari'
        else:
            browser = 'Unknown'

        # Safely check if trace is enabled in the server's state
        state_obj = getattr(self, 'state', None)
        trace_enabled = state_obj.trace_enabled if state_obj else False
        if trace_enabled:
            print(f"\n{GREEN}[+] Public IP: {YELLOW}{client_ip}{RESET}")
            
            # Perform IP Geolocation Lookup
            geo = lookup_ip(client_ip)
            if geo and geo.get("status") == "success":
                country = geo.get("country", "Unknown")
                country_code = geo.get("countryCode", "")
                region = geo.get("regionName", "Unknown")
                city = geo.get("city", "Unknown")
                isp = geo.get("isp", "Unknown")
                
                country_str = f"{country} ({country_code})" if country_code else country
                print(f"{GREEN}[+] Location:  {YELLOW}{city}, {region}, {country_str}{RESET}")
                print(f"{GREEN}[+] ISP:       {YELLOW}{isp}{RESET}")
            else:
                msg = geo.get("message", "Lookup failed / Private IP") if geo else "Lookup failed"
                print(f"{RED}[!] IP Lookup:  {YELLOW}{msg}{RESET}")
                
            print(f"{GREEN}[+] OS:        {YELLOW}{os_info}{RESET}")
            print(f"{GREEN}[+] Browser:   {YELLOW}{browser}{RESET}")
        else:
            # Default mode: print a clean, single-line notification
            print(f"\n{GREEN}[+] Visitor connected from IP: {YELLOW}{client_ip}{RESET} ({os_info}, {browser})")

def run_server(port, target_url, state):
    handler = CustomHTTPRequestHandler
    
    try:
        with SilentThreadingTCPServer(("", port), handler) as httpd:
            httpd.state = state
            state.add_server(httpd)
            # Auto-open browser in a separate thread after 0.5s
            def open_browser():
                time.sleep(0.5)
                webbrowser.open(target_url)
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            try:
                httpd.serve_forever()
            finally:
                state.remove_server(httpd)
    except OSError:
        # Port already in use, fail gracefully in background
        pass

def get_input(prompt, default_value=""):
    try:
        user_input = input(f"{GREEN}[+]{RESET} {prompt}")
        if not user_input.strip():
            return default_value
        return user_input.strip()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{RED}[!] Exiting...{RESET}")
        sys.exit(0)

def select_menu() -> str:
    print(f"{YELLOW}[!] Trace Mode :{RESET}\n")
    print(f"{GREEN}[1]{RESET} Trace")
    print(f"{GREEN}[2]{RESET} seeker mode")
    print(f"{GREEN}[3]{RESET} Exit Program")

    while True:
        try:
            trace_input = input(f"{GREEN}[>]{RESET} ")
            cleaned_trace = trace_input.strip()
            if cleaned_trace == "" or cleaned_trace == "2":
                return "seeker"
            elif cleaned_trace == "1":
                return "trace"
            elif cleaned_trace == "3":
                return "exit"
            else:
                print(f"{RED}[!] Invalid choice. Select [1], [2], or [3].{RESET}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n{RED}[!] Exiting...{RESET}")
            sys.exit(0)

def run_trace_mode():
    print(f"\n{YELLOW}[!] Trace Mode Enabled - IP Geolocation Lookup{RESET}")
    while True:
        target_ip = get_input("Enter Target IP Address : ")
        if not target_ip:
            break
            
        print(f"\n{GREEN}[*] Performing lookup for: {YELLOW}{target_ip}{RESET}")
        geo = lookup_ip(target_ip)
        if geo and geo.get("status") == "success":
            country = geo.get("country", "Unknown")
            country_code = geo.get("countryCode", "")
            region = geo.get("regionName", "Unknown")
            city = geo.get("city", "Unknown")
            zip_code = geo.get("zip", "Unknown")
            isp = geo.get("isp", "Unknown")
            lat = geo.get("lat", "Unknown")
            lon = geo.get("lon", "Unknown")
            timezone = geo.get("timezone", "Unknown")
            
            country_str = f"{country} ({country_code})" if country_code else country
            print(f"{GREEN}[+] Location:   {YELLOW}{city}, {region}, {country_str}{RESET}")
            print(f"{GREEN}[+] Lat/Lon:    {YELLOW}{lat}, {lon}{RESET}")
            print(f"{GREEN}[+] ISP:        {YELLOW}{isp}{RESET}")
            print(f"{GREEN}[+] Timezone:   {YELLOW}{timezone}{RESET}")
            print(f"{GREEN}[+] Zip Code:   {YELLOW}{zip_code}{RESET}\n")
        else:
            msg = geo.get("message", "Lookup failed") if geo else "Lookup failed"
            print(f"{RED}[!] IP Lookup:   {YELLOW}{msg}{RESET}\n")

def run_seeker_mode(state):
    print(f"\n{YELLOW}[!] Select a Template :{RESET}\n")
    print(f"{GREEN}[1]{RESET} telegram (Default)")

    # Selection prompt
    while True:
        try:
            choice_str = input(f"{GREEN}[>]{RESET} ")
            cleaned_choice = choice_str.strip()
            if cleaned_choice == "" or cleaned_choice == "1":
                choice = 1
                break
            print(f"{RED}[!] Invalid choice. Select [1] or press Enter.{RESET}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n{RED}[!] Exiting...{RESET}")
            sys.exit(0)

    # Template mapping setups
    templates = {
        1: {"name": "telegram", "platform": "tg_light", "title": "telegram VIP Signals", "desc": "Official telegram channel. Join for daily high-potential group access and insider signals.", "members": "185,420", "online": "4,219"},
    }
    
    selected = templates[choice]
    print(f"\n{GREEN}[+]{RESET} Loading {YELLOW}{selected['name']}{RESET} Template...")
    
    title = get_input(f"Group Title : ", selected["title"])
    avatar = get_input(f"Image Path / URL (Enter to skip) : ", "")
    desc = get_input(f"Group Description : ", selected["desc"])
    members = get_input(f"Number of Members : ", selected["members"])
    online = get_input(f"Number of Members Online : ", selected["online"])
    
    # Choose theme style - Forced to Light
    platform = selected["platform"]
    # Store trace setting for later use
    state.trace_enabled = False
            
    port = find_free_port(8080)
        
    # Generate the query parameter URL pointing to the local python server
    params = {
        "platform": platform,
        "title": title,
        "desc": desc,
        "members": members,
        "online": online,
        "verified": "1"
    }
    if avatar:
        params["avatar"] = avatar
        
    query_string = urllib.parse.urlencode(params)
    local_ip = get_local_ip()
    target_url = f"http://localhost:{port}/index.html?{query_string}"
    lan_url = f"http://{local_ip}:{port}/index.html?{query_string}"
    
    print(f"\n{GREEN}[+]{RESET} Port : {port}")
    print(f"{GREEN}[+]{RESET} Starting Local Server...{GREEN}[ ✔ ]{RESET}")
    
    # Spawn Python HTTP Server in background thread
    server_thread = threading.Thread(target=run_server, args=(port, target_url, state))
    server_thread.daemon = True
    server_thread.start()
    
    # Give server a fraction of a second to spin up
    time.sleep(0.3)
    
    print(f"\n{GREEN}[*] Local Access URL:   {YELLOW}{target_url}{RESET}")
    print(f"{GREEN}[*] Network Access URL: {YELLOW}{lan_url}{RESET}")
    # Hold the server thread active until Enter is pressed or manual keyboard interrupt
    try:
        input(f"\n{GREEN}[+] Waiting for Client... [Press Enter to go to home / Ctrl+C to exit]{RESET}\n")
        print(f"\n{YELLOW}[!] Stopping server and returning to home...{RESET}")
        state.stop_all()
        time.sleep(0.5)
    except (KeyboardInterrupt, EOFError):
        print(f"\n\n{RED}Local server stopped. Goodbye!{RESET}")
        state.stop_all()
        sys.exit(0)

def main():
    # Force working directory to the directory where seeker.py resides
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    state = AppState()
    
    while True:                         # ← flat loop
        print(BANNER)
        choice = select_menu()
        
        if choice == "exit":
            state.stop_all()
            print(f"\n{RED}[🛑] Exiting... Goodbye!{RESET}")
            break
        elif choice == "trace":
            run_trace_mode()
        elif choice == "seeker":
            run_seeker_mode(state)
            
    sys.exit(0)

if __name__ == "__main__":
    main()
