import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape


def read_sms_xml(file_path):
    text = file_path.read_text(encoding="utf-8", errors="replace")
    text = text[text.find("<"):]  # remove anything before the XML start

    # Fix XML issues caused by SMS text like < and > in message bodies.
    text = re.sub(
        r'([A-Za-z_:-]+)="([^"]*)"',
        lambda m: f'{m.group(1)}="{escape(m.group(2), {"\"": "&quot;"})}"',
        text,
    )

    return ET.fromstring(text)


xml_file = Path(__file__).resolve().parent / "modified_sms_v2.xml"
root = read_sms_xml(xml_file)

sms_records = []
for sms in root.findall(".//sms"):
    sms_records.append({
        "protocol": sms.get("protocol"),
        "address": sms.get("address"),
        "date": sms.get("date"),
        "type": sms.get("type"),
        "body": sms.get("body"),
        "service_center": sms.get("service_center"),
        "readable_date": sms.get("readable_date"),
    })

print(f"Parsed {len(sms_records)} SMS records")
print(json.dumps(sms_records[:5], indent=4, ensure_ascii=False))