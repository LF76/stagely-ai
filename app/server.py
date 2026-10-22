import http.server
import socketserver
import webbrowser
import os

PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

print(f"==================================================")
print(f"  Stagely AI - Local Development Studio Running   ")
print(f"  Open in Browser: http://localhost:{PORT}       ")
print(f"==================================================")

try:
    webbrowser.open(f"http://localhost:{PORT}")
except Exception:
    pass

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
