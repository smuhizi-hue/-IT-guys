### IT GUYS

**MEMBERS:**

  - MUHIZI Shaun
  - HAKIZIMANA Baraka Joel
  - NITEKA Morel Louange

**PROJECT STRUCTURE**
```
├── README.md
└── momo-data-project
    ├── api
    │   ├── __init__.py
    │   ├── app.py
    │   ├── db.py
    │   └── schemas.py
    ├── data
    │   ├── logs
    │   │   ├── dead_letter
    │   │   └── etl.log
    │   ├── processed
    │   │   └── dashboard.json
    │   └── raw
    ├── docs
    ├── etl
    │   ├── __init__.py
    │   ├── categorize.py
    │   ├── clean_normalize.py
    │   ├── config.py
    │   ├── load_db.py
    │   ├── parse_xml.py
    │   └── run.py
    ├── index.html
    ├── requirements.txt
    ├── scripts
    │   ├── export_json.sh
    │   ├── run_etl.sh
    │   └── serve_frontend.sh
    ├── tests
    │   ├── test_categorize.py
    │   ├── test_clean_normalize.py
    │   └── test_parse_xml.py
    └── web
        ├── assets
        ├── chart_handler.js
        └── styles.css
```
