#!/usr/bin/env python3
"""
ReconMail - Web UI Server & API Backend
Author: Imran Pasha (https://github.com/Imranpasha30)
"""

import sys
import os
import json
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver
from datetime import datetime

# Import core scanning functions from run.py & config.py
import config
from run import run_domain_recon, run_single_email_check, check_dns_records

PORT = 5050
WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")


class ReconMailAPIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        # Route root to index.html
        if self.path == "/" or self.path == "":
            self.path = "/index.html"
            return super().do_GET()

        # Health endpoint
        if self.path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "online", "version": config.VERSION}).encode())
            return

        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/scan":
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length).decode("utf-8")
            
            try:
                payload = json.loads(post_body)
                target = payload.get("target", "").strip()
                mode = payload.get("mode", "domain")  # "domain" or "email"
                sources = payload.get("sources", ["all"])
                
                if not target:
                    self._send_json({"error": "Target domain or email is required."}, status=400)
                    return

                # Execute requested scan
                if mode == "domain":
                    available_sources = list(config.SEARCH_ENGINES.keys()) + ["pgp"]
                    if "all" in sources:
                        selected_sources = available_sources
                    else:
                        selected_sources = [s for s in sources if s in available_sources]
                    
                    recon_results = run_domain_recon(target, selected_sources, verbose=False)
                    response_data = {
                        "status": "success",
                        "mode": "domain",
                        "target": target,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "data": recon_results
                    }
                else:
                    breach_check = payload.get("breach_check", True)
                    email_results = run_single_email_check(target, breach_check, verbose=False)
                    response_data = {
                        "status": "success",
                        "mode": "email",
                        "target": target,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "data": email_results
                    }

                self._send_json(response_data)
            except Exception as e:
                self._send_json({"error": f"Internal scan error: {str(e)}"}, status=500)
            return

        self.send_error(404, "Endpoint Not Found")

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))


class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True


def start_server():
    os.makedirs(WEB_DIR, exist_ok=True)
    server_address = ("127.0.0.1", PORT)
    httpd = ThreadedHTTPServer(server_address, ReconMailAPIHandler)
    print(f"\n==================================================")
    print(f"  🔍 RECONMAIL OSINT DASHBOARD SERVER")
    print(f"  Author: Imran Pasha")
    print(f"  UI URL: http://localhost:{PORT}")
    print(f"==================================================\n")
    print(f"[*] Serving web interface from: {WEB_DIR}")
    print(f"[*] Press Ctrl + C to stop the server.\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Shutting down ReconMail Web Server cleanly...")
        httpd.server_close()


if __name__ == "__main__":
    start_server()
