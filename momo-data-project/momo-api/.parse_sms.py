import argparse
import json
import logging
from pathlib import Path
from lxml import etree

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def parse_sms_backup(xml_path: Path) -> list[dict]:
    """Parse SMS backup XML files, handling unescaped control characters."""
    # lxml recover=True safely handles unescaped <, >, & inside message bodies
    parser = etree.XMLParser(recover=True, encoding="utf-8")
    
    try:
        tree = etree.parse(str(xml_path), parser)
    except Exception as e:
        logging.error(f"Failed to read XML file {xml_path}: {e}")
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
    for elem in tree.iter("sms"):
        records.append({field: elem.get(field) for field in fields})

    return records


def main():
    parser = argparse.ArgumentParser(description="Extract SMS records from XML backup.")
    parser.add_argument(
        "file",
        nargs="?",
        default="modified_sms_v2.xml",
        type=Path,
        help="Path to the XML file",
    )
    args = parser.parse_args()

    xml_file = args.file.resolve()
    if not xml_file.is_file():
        logging.error(f"File not found: {xml_file}")
        return

    sms_records = parse_sms_backup(xml_file)
    logging.info(f"Successfully extracted {len(sms_records)} records from {xml_file.name}")

    # Inspect first few records
    print(json.dumps(sms_records[:5], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()