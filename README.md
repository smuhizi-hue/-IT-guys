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
[Scrum Board](https://github.com/users/smuhizi-hue/projects/1)
i# Money Transaction Database

## Description

This project is a MySQL database for storing and managing Mobile Money transaction information.

The database is called money_transaction and contains information about users, transactions, system logs, and transaction categories.

## Tables

### USERS

Stores information about customers and merchants.

Main columns:

* user_id - unique ID for each user
* phone_number - user's phone number
* full_name - user's name
* user_type - customer or merchant

user_id is the primary key. An index is also created on phone_number to make searching easier.

### TRANSACTIONS

Stores information about money transactions.

It contains the transaction ID, Mobile Money transaction ID, sender, receiver, amount, fee, and transaction time.

transaction_id is the primary key. sender_id and receiver_id are foreign keys that reference the USERS table.

The database also checks that the amount is greater than zero and that the fee is not negative.

### SYSTEM_LOGS

Stores logs related to transactions.

It contains the log ID, transaction ID, log level, and message.

log_id is the primary key and transaction_id is a foreign key.

### TRANSACTION_CATEGORIES

Stores the different types of transactions, such as Transfer, Payment, Airtime, Withdrawal, and Deposit.

category_id is the primary key.

### TRANSACTION_CATEGORY_MAPPINGS

Connects transactions with their categories.

It uses transaction_id and category_id as a composite primary key. Both columns are also foreign keys.

## Database Setup


Open MySQL Workbench and run the database_setup.sql file.

The script will:

1. Create the money_transaction database.
2. Select the database.
3. Create all five tables.
4. Add primary keys, foreign keys, constraints, and an index.
5. Insert sample data.
6. Demonstrate basic CRUD operations.

## CRUD Operations


The project demonstrates:

* INSERT for adding data
* SELECT for viewing data
* UPDATE for changing data
* DELETE for removing data

## Technologies Used

* MySQL Workbench
* SQL
## Files

database_setup.sql contains the SQL code for creating and testing the database.
https://drive.google.com/file/d/1N-y6jFuu3LfvXRIu5Vk_WF1fEhGvAIga/view?usp=sharing
The Entity Relationship Diagram (ERD) models a relational database for processing MoMo SMS data, converting raw XML inputs into a structured system that ensures data integrity and high performance.
