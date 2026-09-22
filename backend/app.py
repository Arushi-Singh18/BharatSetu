
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class BharatSetuHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/api/health":
            response = {
                "status": "success",
                "message": "BharatSetu backend is running"
            }

            body = json.dumps(response).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

            self.wfile.write(body)

        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), BharatSetuHandler)

    print("BharatSetu backend running at:")
    print("http://localhost:8000")

    server.serve_forever()
