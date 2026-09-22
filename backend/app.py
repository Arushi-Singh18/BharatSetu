
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class BharatSetuHandler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/health":
            self.send_json({
                "status": "success",
                "message": "BharatSetu backend is running"
            })
        else:
            self.send_json({
                "status": "error",
                "message": "Route not found"
            }, 404)

    def do_POST(self):
        if self.path == "/api/plan":

            length = int(self.headers.get("Content-Length", 0))
            raw_data = self.rfile.read(length)

            try:
                data = json.loads(raw_data)

                destination = data.get("destination", "Unknown")
                duration = data.get("duration", 1)
                budget = data.get("budget", 0)
                interest = data.get("interest", "Heritage")

                response = {
                    "status": "success",
                    "destination": destination,
                    "duration": duration,
                    "budget": budget,
                    "interest": interest,
                    "message": "Your travel plan request was received!",
                    "suggestion": (
                        f"Explore {destination} for {duration} day(s) "
                        f"with a budget of ₹{budget}, focusing on {interest}."
                    )
                }

                self.send_json(response)

            except (json.JSONDecodeError, ValueError):
                self.send_json({
                    "status": "error",
                    "message": "Invalid JSON request"
                }, 400)

        else:
            self.send_json({
                "status": "error",
                "message": "Route not found"
            }, 404)


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), BharatSetuHandler)

    print("BharatSetu backend running at http://localhost:8000")

    server.serve_forever()
