from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

DATA_FILE = Path(__file__).resolve().parent / "destinations.json"

def load_destinations():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
   


class BharatSetuHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

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

        elif self.path == "/api/destinations":
            destinations = load_destinations()

            self.send_json({
               "status": "success",
               "destinations": destinations
    })

        else:
            self.send_json({
                "status": "error",
                "message": "Route not found"
            }, 404)

    def do_POST(self):
        if self.path != "/api/plan":
            self.send_json({
                "status": "error",
                "message": "Route not found"
            }, 404)
            return

        length = int(self.headers.get("Content-Length", 0))
        raw_data = self.rfile.read(length)

        try:
            data = json.loads(raw_data)

            destination = data.get("destination", "Jaipur")
            duration = int(data.get("duration", 1))
            budget = float(data.get("budget", 0))
            interest = data.get("interest", "Heritage")
        except Exception:
            self.send_json({"status": "error", "message": "Invalid JSON data"}, 400)
            return    
        destinations = load_destinations()

        matches = [
            place for place in destinations
            if place["category"].lower() == interest.lower()
        ]

        if not matches:
            matches = destinations

            response = {
                "status": "success",
                "destination": destination,
                "duration": duration,
                "budget": budget,
                "interest": interest,
                "recommended_places": matches,
                "message": "Personalized suggestions generated"
            }

            self.send_json(response)

        


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), BharatSetuHandler)

    print("BharatSetu backend running at http://localhost:8000")

    server.serve_forever()
def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
