import xml.etree.ElementTree as ET
import json
import re
from pathlib import Path
from datetime import datetime, timezone
from xml.sax.saxutils import escape

BASE_DIR = Path(__file__).resolve().parent
XML_FILE = BASE_DIR / "modified_sms_v2.xml"
JSON_FILE = BASE_DIR / "modified_sms_v2.json"


def classify(body: str) -> str:
    """Decide the transaction type from the message text."""
    b = body.lower()
    if "you have received" in b:
        return "received"
    if "your payment of" in b:
        return "payment"
    if "transferred to" in b:
        return "transfer"
    if "bank deposit" in b:
        return "deposit"
    if "withdrawn" in b:
        return "withdrawal"
    if "airtime" in b:
        return "airtime"
    return "other"


def parse_body(body: str) -> dict:
    """Pull amount, counterparty, txn id, balance out of the SMS text."""
    amount = re.search(r"([\d,]+)\s*RWF", body)
    txn_id = re.search(r"(?:Financial Transaction Id|TxId|Transaction Id)[:\s]*(\d+)", body, re.I)
    balance = re.search(r"new balance[:\s]*([\d,]+)\s*RWF", body, re.I)
    sender = re.search(r"received [\d,]+\s*RWF from ([A-Za-z .'-]+?)(?: \(|\s+on )", body)
    receiver = re.search(r"(?:transferred to|payment of [\d,]+\s*RWF to) ([A-Za-z0-9 .'-]+?)(?: \(|\s+\d|\s+has| at |\.)", body)
    time_in_body = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)

    to_int = lambda m: int(m.group(1).replace(",", "")) if m else None
    return {
        "amount": to_int(amount),
        "sender": sender.group(1).strip() if sender else None,
        "receiver": receiver.group(1).strip() if receiver else None,
        "transaction_id": txn_id.group(1) if txn_id else None,
        "balance": to_int(balance),
        "body_time": time_in_body.group(1) if time_in_body else None,
    }


def parse_xml(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        xml_text = f.read()

    xml_start = xml_text.find("<")
    if xml_start > 0:
        xml_text = xml_text[xml_start:]

    xml_text = re.sub(
        r'(body=")(.*?)(")',
        lambda m: m.group(1) + escape(m.group(2)) + m.group(3),
        xml_text,
        flags=re.DOTALL,
    )

    root = ET.fromstring(xml_text)
    records = []

    for i, sms in enumerate(root.iter("sms"), start=1):
        body = sms.get("body", "")
        ts_ms = sms.get("date")  # epoch milliseconds in standard SMS backups
        timestamp = (
            datetime.fromtimestamp(int(ts_ms) / 1000, tz=timezone.utc).isoformat()
            if ts_ms and ts_ms.isdigit() else None
        )
        parsed = parse_body(body)
        records.append({
            "id": i,
            "type": classify(body),
            "amount": parsed["amount"],
            "sender": parsed["sender"],
            "receiver": parsed["receiver"],
            "transaction_id": parsed["transaction_id"],
            "balance": parsed["balance"],
            "timestamp": timestamp or parsed["body_time"],
            "address": sms.get("address"),
            "body": body,
        })
    return records


if __name__ == "__main__":
    data = parse_xml(str(XML_FILE))
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Parsed {len(data)} records -> {JSON_FILE}")
    if data:
        print(json.dumps(data[0], indent=2))