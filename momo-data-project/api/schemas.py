from typing import TypedDict, Literal

# Core Schemas
class User(TypedDict):
    user_id: int
    phone_number: str
    full_name: str
    user_type: Literal["customer", "merchant"]


class Category(TypedDict):
    category_id: int
    category_name: str


class SystemLog(TypedDict):
    log_id: int
    transaction_id: int
    log_level: Literal["INFO", "WARN", "ERROR"]
    message: str


class Transaction(TypedDict):
    transaction_id: int
    momo_tx_id: str
    sender_id: int
    receiver_id: int
    amount: float
    fee: float
    time_stamp: str


# Nested API Response Model
class TransactionDetail(TypedDict):
    transaction_id: int
    momo_tx_id: str
    amount: float
    fee: float
    time_stamp: str
    sender: User
    receiver: User
    categories: list[Category]
    logs: list[SystemLog]


# Dummy Data / Fixtures
sample_user: User = {
    "user_id": 101,
    "phone_number": "+250788123456",
    "full_name": "Jean Claude Uwimana",
    "user_type": "customer",
}

sample_category: Category = {
    "category_id": 1,
    "category_name": "P2P Transfer",
}

# Complete API response preview
complex_transaction: TransactionDetail = {
    "transaction_id": 501,
    "momo_tx_id": "18492039481",
    "amount": 5000.0,
    "fee": 50.0,
    "time_stamp": "2026-09-14T14:30:00Z",
    "sender": sample_user,
    "receiver": {
        "user_id": 102,
        "phone_number": "+250791987654",
        "full_name": "Aline Mukamana",
        "user_type": "customer",
    },
    "categories": [sample_category],
    "logs": [
        {
            "log_id": 9001,
            "transaction_id": 501,
            "log_level": "INFO",
            "message": "SMS payload parsed and validated successfully",
        }
    ],
}