import argparse
import json
import logging
from pathlib import Path

from lxml import etree

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def parse_sms_backup(xml_path: Path) -> list[dict]:
    parser = etree.XMLParser(recover=True, encoding="utf-8")

    try:
        tree = etree.parse(str(xml_path), parser)
    except Exception as exc:
        logging.error("Failed to read XML file %s: %s", xml_path, exc)
        return []

    fields = (
        "protocol",
        "address",
        "date",
        "type",
        "body",
        "service_center",
        "readable_date",
    )

    records = []
    for sms in tree.iter("sms"):
        records.append({field: sms.get(field) for field in fields})

    return records


def main():
    parser = argparse.ArgumentParser(description="Extract SMS records from an XML backup.")
    parser.add_argument(
        "file",
        nargs="?",
        default="modified_sms_v2.xml",
        type=Path,
        help="XML file to parse",
    )
    args = parser.parse_args()

    xml_file = args.file.resolve()
    if not xml_file.is_file():
        logging.error("File not found: %s", xml_file)
        return

    sms_records = parse_sms_backup(xml_file)
    logging.info("Extracted %s records from %s", len(sms_records), xml_file.name)
    print(json.dumps(sms_records[:5], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()