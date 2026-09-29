# MoMo Transactions API Documentation

Base URL: http://127.0.0.1:5000

This API exposes parsed Mobile Money transaction records loaded from the XML transaction export. The server supports retrieving, creating, updating, and deleting transaction entries.

# Common Transaction Object

Each transaction is returned as a JSON object with the following fields:

```json
{
  "id": 1,
  "raw_date": "10 May 2024 4:30:58 PM",
  "body": "You have received 2000 RWF from Jane Smith ...",
  "amount": "2000 RWF",
  "recipient_or_sender": "Jane Smith",
  "type": "Received"
}
```

Supported transaction types include:
- Payment
- Transfer
- Received
- Deposit
- Unknown

---

 # 1. GET /transactions

 Endpoint & Method
- Method: GET
- URL: /transactions

# Request Example
```bash
curl http://127.0.0.1:5000/transactions
```

# Response Example
```json
[
  {
    "id": 1,
    "raw_date": "10 May 2024 4:30:58 PM",
    "body": "You have received 2000 RWF from Jane Smith ...",
    "amount": "2000 RWF",
    "recipient_or_sender": "Jane Smith",
    "type": "Received"
  },
  {
    "id": 2,
    "raw_date": "10 May 2024 4:31:46 PM",
    "body": "TxId: 73214484437. Your payment of 1,000 RWF to Jane Smith 12845 has been completed ...",
    "amount": "1,000 RWF",
    "recipient_or_sender": "Jane Smith",
    "type": "Payment"
  }
]
```

# Error Codes
- 200 OK: Request succeeded.
- 404 Not Found: Route does not exist.

---

# 2. GET /transactions/{id}

# Endpoint & Method
- Method: GET
- URL: /transactions/{id}

# Request Example
```bash
curl http://127.0.0.1:5000/transactions/1
```

# Response Example
```json
{
  "id": 1,
  "raw_date": "10 May 2024 4:30:58 PM",
  "body": "You have received 2000 RWF from Jane Smith ...",
  "amount": "2000 RWF",
  "recipient_or_sender": "Jane Smith",
  "type": "Received"
}
```

# Error Codes
- 200 OK: Record found.
- 404 Not Found: Transaction ID does not exist.
- 404 Not Found: Route is invalid.

---

# 3. POST /transactions

# Endpoint & Method
- Method: POST
- URL: /transactions

# Request Example
```bash
curl -X POST http://127.0.0.1:5000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "raw_date": "29 Sep 2026 10:00:00 AM",
    "body": "Your payment of 5000 RWF to Alice Doe ...",
    "amount": "5000 RWF",
    "recipient_or_sender": "Alice Doe",
    "type": "Payment"
  }'
```

# Response Example
```json
{
  "id": 1692,
  "raw_date": "29 Sep 2026 10:00:00 AM",
  "body": "Your payment of 5000 RWF to Alice Doe ...",
  "amount": "5000 RWF",
  "recipient_or_sender": "Alice Doe",
  "type": "Payment"
}
```

# Error Codes
- 201 Created: Transaction successfully created.
- 400 Bad Request: Invalid JSON payload or malformed request body.
- 404 Not Found: Route is invalid.

---

# 4. PUT /transactions/{id}

# Endpoint & Method
- Method: PUT
- URL: /transactions/{id}

# Request Example
```bash
curl -X PUT http://127.0.0.1:5000/transactions/1 \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "2500 RWF",
    "recipient_or_sender": "Jane Smith",
    "type": "Transfer"
  }'
```

# Response Example
```json
{
  "id": 1,
  "raw_date": "10 May 2024 4:30:58 PM",
  "body": "You have received 2000 RWF from Jane Smith ...",
  "amount": "2500 RWF",
  "recipient_or_sender": "Jane Smith",
  "type": "Transfer"
}
```

# Error Codes
- 200 OK: Transaction updated successfully.
- 400 Bad Request: Invalid JSON payload.
- 404 Not Found: Transaction ID does not exist.
- 404 Not Found: Route is invalid.

---

# 5. DELETE /transactions/{id}

# Endpoint & Method
- Method: DELETE
- URL: /transactions/{id}

# Request Example
```bash
curl -X DELETE http://127.0.0.1:5000/transactions/1
```

# Response Example
```json
{
  "message": "Transaction deleted"
}
```

# Error Codes
- 200 OK: Transaction deleted successfully.
- 404 Not Found: Transaction ID does not exist.
- 404 Not Found: Route is invalid.

---

# Common HTTP Status Codes

| Status Code | Meaning |
| --- | --- |
| 200 | Request completed successfully |
| 201 | New transaction was created |
| 400 | Bad request or invalid JSON |
| 404 | Resource not found or route not defined |

# Notes
- The server runs locally on port 5000 when started from the project entry point.
- The parser reads transaction data from the XML export and maps the content into standardized fields for easier downstream analysis.
