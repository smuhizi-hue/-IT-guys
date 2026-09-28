import base64
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

AUTH_CONFIG = {
    "admin": "12345",
}


class MoMoApiHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code, payload):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def _send_unauthorized(self, message="Unauthorized access"):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="MoMo API"')
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "error", "message": message}).encode("utf-8"))

    def _is_authenticated(self):
        auth_header = self.headers.get("Authorization", "")
        if not auth_header or not auth_header.lower().startswith("basic "):
            return False

        try:
            raw_token = auth_header.split(" ", 1)[1]
            decoded = base64.b64decode(raw_token).decode("utf-8")
            username, password = decoded.split(":", 1)
            return AUTH_CONFIG.get(username) == password
        except (ValueError, TypeError, UnicodeDecodeError):
            return False

    def do_GET(self):
        if not self._is_authenticated():
            self._send_unauthorized("Invalid or missing Basic Auth credentials.")
            return

        self._send_json(200, {
            "status": "success",
            "message": "Welcome to the MoMo API.",
        })


def run_server(host="127.0.0.1", port=8000):
    httpd = HTTPServer((host, port), MoMoApiHandler)
    print(f"[*] MoMo API Server listening on http://{host}:{port}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down server gracefully...")
        httpd.server_close()


if __name__ == "__main__":
    run_server()