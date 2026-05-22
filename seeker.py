#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import threading
import time
import sys
import urllib.parse
import socket
import os

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
        
    def do_GET(self):
        # Log visitor IP when they click the button (requests /log endpoint)
        parsed_url = urllib.parse.urlparse(self.path)
        if parsed_url.path == "/log":
            parsed_qs = urllib.parse.parse_qs(parsed_url.query)
            client_ip = parsed_qs.get('ip', [self.client_address[0]])[0]
            ua = self.headers.get('User-Agent', '')
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

            print(f"\n{GREEN}[+] Public IP: {YELLOW}{client_ip}{RESET}")
            print(f"{GREEN}[+] OS: {YELLOW}{os_info}{RESET}")
            print(f"{GREEN}[+] Browser: {YELLOW}{browser}{RESET}")
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
            return

        # If accessing the root path "/", redirect it to "/index.html" with query parameters
        if parsed_url.path == "/" or parsed_url.path == "":
            query = parsed_url.query
            new_path = "/index.html"
            if query:
                new_path += f"?{query}"
            self.send_response(302)
            self.send_header('Location', new_path)
            self.end_headers()
            return

        # Otherwise serve files normally
        super().do_GET()

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

def run_server(port, target_url):
    handler = CustomHTTPRequestHandler
    
    try:
        with SilentThreadingTCPServer(("", port), handler) as httpd:
            # Auto-open browser in a separate thread after 0.5s
            def open_browser():
                time.sleep(0.5)
                webbrowser.open(target_url)
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            httpd.serve_forever()
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

def main():
    # Force working directory to the directory where seeker.py resides
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print(BANNER)
    
    print(f"{YELLOW}[!] Select a Template :{RESET}\n")
    print(f"{GREEN}[1]{RESET} shmunky (Default)")

    
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
        1: {"name": "shmunky", "platform": "tg_light", "title": "shmunky VIP Signals", "desc": "Official shmunky channel. Join for daily high-potential group access and insider signals.", "members": "185,420", "online": "4,219"},
    }
    
    selected = templates[choice]
    print(f"\n{GREEN}[+]{RESET} Loading {YELLOW}{selected['name']}{RESET} Template...")
    
    # Prompt user for parameters
    title = get_input(f"Group Title : ", selected["title"])
    avatar = get_input(f"Image Path / URL (Enter to skip) : ", "")
    desc = get_input(f"Group Description : ", selected["desc"])
    members = get_input(f"Number of Members : ", selected["members"])
    online = get_input(f"Number of Members Online : ", selected["online"])
    
    # Choose theme style - Forced to Light
    platform = selected["platform"]
            
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
    server_thread = threading.Thread(target=run_server, args=(port, target_url))
    server_thread.daemon = True
    server_thread.start()
    
    # Give server a fraction of a second to spin up
    time.sleep(0.3)
    
    print(f"\n{GREEN}[*] Local Access URL:   {YELLOW}{target_url}{RESET}")
    print(f"{GREEN}[*] Network Access URL: {YELLOW}{lan_url}{RESET}")
    print(f"{GREEN}[+] Waiting for Client...[ctrl+c to exit]{RESET}")
    
    # Hold the server thread active until manual keyboard interrupt
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n\n{RED}[🛑] Local server stopped. Goodbye!{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
