### IT GUYS

**MEMBERS:**

  - MUHIZI Shaun
  - HAKIZIMANA Baraka Joel
  - NITEKA Morel Louange

**PROJECT DESCRIPTION**

This project is a full-stack MoMo SMS data processing and analytics application. It is designed to process Mobile Money (MoMo) transaction messages stored in XML format, clean and normalize the data, categorize different types of transactions, and store the processed information in a relational database.

The application will provide a frontend dashboard where users can analyze and visualize transaction data through statistics, charts, and tables. The system will help transform raw MoMo SMS data into organized and meaningful information that can be used for analysis and decision-making.

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
[Google Drive link](https://drive.google.com/file/d/16kzjM9FzY3iCG_MnS6oz049an5WkH_cc/view?usp=sharing)

## Project Management 
[Scrum Board](htttps://github.com/users/smuhizi-hue/projects/1)

