#!/usr/bin/env python3
"""Serve the static site locally."""
import http.server
import socket
import socketserver
import webbrowser
from pathlib import Path

DEFAULT_PORT = 8080
ROOT = Path(__file__).resolve().parent.parent


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def find_port(start: int = DEFAULT_PORT, attempts: int = 10) -> int:
    for port in range(start, start + attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("", port))
                return port
            except OSError:
                continue
    raise OSError(f"Nenhuma porta livre entre {start} e {start + attempts - 1}")


def main():
    port = find_port()
    with ReusableTCPServer(("", port), Handler) as httpd:
        url = f"http://localhost:{port}/"
        print("Mentes Criativas — site estático")
        print(f"Servindo em: {url}")
        if port != DEFAULT_PORT:
            print(f"(porta {DEFAULT_PORT} ocupada, usando {port})")
        print(f"Pasta: {ROOT}")
        print("Pressione Ctrl+C para parar.\n")
        try:
            webbrowser.open(url)
        except OSError:
            pass
        httpd.serve_forever()


if __name__ == "__main__":
    main()
