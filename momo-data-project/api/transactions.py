import json
import re
import xml.etree.ElementTree as ET
from http.server import BaseHTTPRequestHandler, HTTPServer
from xml.sax.saxutils import escape

# 1. Parse XML file to load transactions into memory
def parse_sms_xml(file_path):
    transactions_list = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        xml_start = content.find('<')
        if xml_start > 0:
            content = content[xml_start:]

        content = re.sub(
            r'(body=")([^"]*)(")',
            lambda m: m.group(1) + escape(m.group(2)) + m.group(3),
            content,
        )

        root = ET.fromstring(content)
        sms_nodes = root.findall('sms') if root.tag == 'smses' else root.findall('.//sms')

        tx_counter = 1
        for sms in sms_nodes:
            body = sms.get('body', '')

            # Basic SMS metadata structure
            tx_data = {
                "id": tx_counter,
                "raw_date": sms.get('readable_date'),
                "body": body,
                "amount": None,
                "recipient_or_sender": None,
                "type": "Unknown"
            }

            # Detect transaction type and extract details using Regular Expressions
            payment_match = re.search(r'Your payment of ([\d,]+) RWF to ([^0-9]+)', body)
            transfer_match = re.search(r'([\d,]+) RWF transferred to ([^\(]+)', body)
            received_match = re.search(r'You have received ([\d,]+) RWF from ([^\(]+)', body)
            deposit_match = re.search(r'bank deposit of ([\d,]+) RWF', body)

            if payment_match:
                tx_data["amount"] = payment_match.group(1) + " RWF"
                tx_data["recipient_or_sender"] = payment_match.group(2).strip()
                tx_data["type"] = "Payment"
            elif transfer_match:
                tx_data["amount"] = transfer_match.group(1) + " RWF"
                tx_data["recipient_or_sender"] = transfer_match.group(2).strip()
                tx_data["type"] = "Transfer"
            elif received_match:
                tx_data["amount"] = received_match.group(1) + " RWF"
                tx_data["recipient_or_sender"] = received_match.group(2).strip()
                tx_data["type"] = "Received"
            elif deposit_match:
                tx_data["amount"] = deposit_match.group(1) + " RWF"
                tx_data["recipient_or_sender"] = "Bank Deposit"
                tx_data["type"] = "Deposit"

            transactions_list.append(tx_data)
            tx_counter += 1

    except Exception as e:
        print(f"Error parsing XML file: {e}")

    return transactions_list

# Load initial data from XML file
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def find_xml_file():
    priority_names = [
        "modified_sms_v2.xml",
        "sms.xml",
        "transactions.xml",
    ]
    search_roots = [
        BASE_DIR,
        *BASE_DIR.parents,
        Path.cwd(),
        Path.home(),
        Path.home() / ".ssh",
    ]

    seen = set()
    for root in search_roots:
        if not root or not root.exists():
            continue
        for name in priority_names:
            candidate = root / name
            if candidate.exists() and str(candidate) not in seen:
                seen.add(str(candidate))
                return str(candidate)

    for root in search_roots:
        if not root or not root.exists():
            continue
        xml_matches = sorted(root.rglob("*.xml"))
        for match in xml_matches:
            if str(match) not in seen:
                seen.add(str(match))
                return str(match)

    return str(BASE_DIR / "sms.xml")


XML_FILE_PATH = find_xml_file()
transactions = parse_sms_xml(XML_FILE_PATH)
current_id = len(transactions) + 1 if transactions else 1


# 2. REST API Handler (http.server)
class RequestHandler(BaseHTTPRequestHandler):

    def _send_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))

    def _read_json_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return {}
        body = self.rfile.read(content_length)
        return json.loads(body.decode('utf-8'))

    # GET /transactions AND GET /transactions/{id}
    def do_GET(self):
        # GET /transactions -> List all SMS transactions
        if self.path == '/transactions':
            self._send_response(transactions)
            return

        # GET /transactions/{id} -> View one transaction
        match = re.match(r'^/transactions/(\d+)$', self.path)
        if match:
            transaction_id = int(match.group(1))
            transaction = next((t for t in transactions if t["id"] == transaction_id), None)
            if transaction:
                self._send_response(transaction)
            else:
                self._send_response({"error": "Transaction not found"}, status_code=404)
            return

        self._send_response({"error": "Route not found"}, status_code=404)
    def do_POST(self):
        # POST /transactions -> Create a new transaction
        if self.path == '/transactions':
            try:
                data = self._read_json_body()
                global current_id
                new_transaction = {
                    "id": current_id,
                    "raw_date": data.get("raw_date"),
                    "body": data.get("body"),
                    "amount": data.get("amount"),
                    "recipient_or_sender": data.get("recipient_or_sender"),
                    "type": data.get("type", "Unknown")
                }
                transactions.append(new_transaction)
                current_id += 1
                self._send_response(new_transaction, status_code=201)
            except Exception as e:
                self._send_response({"error": "Invalid JSON format"}, status_code=400)
            return

        self._send_response({"error": "Route not found"}, status_code=404)
    def do_PUT(self):
        # PUT /transactions/{id} -> Update an existing transaction
        match = re.match(r'^/transactions/(\d+)$', self.path)
        if match:
            transaction_id = int(match.group(1))
            transaction = next((t for t in transactions if t["id"] == transaction_id), None)
            if transaction:
                try:
                    data = self._read_json_body()
                    transaction.update({
                        "raw_date": data.get("raw_date", transaction["raw_date"]),
                        "body": data.get("body", transaction["body"]),
                        "amount": data.get("amount", transaction["amount"]),
                        "recipient_or_sender": data.get("recipient_or_sender", transaction["recipient_or_sender"]),
                        "type": data.get("type", transaction["type"])
                    })
                    self._send_response(transaction)
                except Exception as e:
                    self._send_response({"error": "Invalid JSON format"}, status_code=400)
            else:
                self._send_response({"error": "Transaction not found"}, status_code=404)
            return

        self._send_response({"error": "Route not found"}, status_code=404)

    def do_DELETE(self):
        # DELETE /transactions/{id} -> Delete a transaction
        match = re.match(r'^/transactions/(\d+)$', self.path)
        if match:
            transaction_id = int(match.group(1))
            transaction = next((t for t in transactions if t["id"] == transaction_id), None)
            if transaction:
                transactions.remove(transaction)
                self._send_response({"message": "Transaction deleted"})
            else:
                self._send_response({"error": "Transaction not found"}, status_code=404)
            return

        self._send_response({"error": "Route not found"}, status_code=404)


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    server = HTTPServer((host, port), RequestHandler)
    print(f"Serving transactions API on http://{host}:{port}")
    server.serve_forever()