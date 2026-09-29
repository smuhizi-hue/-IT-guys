"""
DSA Integration for the MoMo project: Linear Search vs Dictionary Lookup.

Each record looks like:
  {"id": 1, "type": "received", "amount": 2000, "sender": "Jane Smith",
   "transaction_id": "76662021700", "balance": 2000, "timestamp": "...", ...}
"""

import json
import random
import time
from pathlib import Path

JSON_FILE = Path(__file__).resolve().parent / "modified_sms_v2.json"


def load_transactions(path=JSON_FILE):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------
# 1. Linear search -> O(n)
# ---------------------------------------------------------------
def linear_search(transactions, target_id):
    """Scan the list from the start until a record with this id is found."""
    for txn in transactions:
        if txn["id"] == target_id:
            return txn
    return None


# ---------------------------------------------------------------
# 2. Dictionary lookup -> O(1) average
# ---------------------------------------------------------------
def build_dict(transactions):
     # One-time O(n) step: build {id: transaction}.
      return {txn["id"]: txn for txn in transactions}


def dict_lookup(txn_dict, target_id):
    return txn_dict.get(target_id)


# ---------------------------------------------------------------
# Bonus: Binary search on a list sorted by id -> O(log n)
# ---------------------------------------------------------------
def binary_search(sorted_txns, target_id):
    low, high = 0, len(sorted_txns) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_id = sorted_txns[mid]["id"]
        if mid_id == target_id:
            return sorted_txns[mid]
        if mid_id < target_id:
            low = mid + 1
        else:
            high = mid - 1
    return None


# ---------------------------------------------------------------
# Testing and comparing performance
# ---------------------------------------------------------------
def avg_time_us(func, args_list, repeats=20):
   #Average microseconds per search across many target ids
    start = time.perf_counter()
    for _ in range(repeats):
        for args in args_list:
            func(*args)
    elapsed = time.perf_counter() - start
    return elapsed / (repeats * len(args_list)) * 1_000_000


def benchmark(all_txns, n):
    txns = all_txns[:n]                       # first n real records
    txn_dict = build_dict(txns)
    sorted_txns = sorted(txns, key=lambda t: t["id"])

    # Searching for EVERY id in the subset (average case) 
    all_ids = [t["id"] for t in txns]
    # ... and for the last id only (worst case for linear search)
    worst_id = txns[-1]["id"]

    # Correctness checking: all three methods must agree
    for tid in all_ids:
        assert linear_search(txns, tid) is dict_lookup(txn_dict, tid) \
            is binary_search(sorted_txns, tid)

    reps = max(1, 2000 // n)
    row = {"n": n}
    for label, targets in (("avg", [(i,) for i in all_ids]),
                           ("worst", [(worst_id,)])):
        row[f"lin_{label}"] = avg_time_us(
            linear_search, [(txns, *a) for a in targets], repeats=reps)
        row[f"bin_{label}"] = avg_time_us(
            binary_search, [(sorted_txns, *a) for a in targets], repeats=reps)
        row[f"dic_{label}"] = avg_time_us(
            dict_lookup, [(txn_dict, *a) for a in targets], repeats=reps)
    return row


if __name__ == "__main__":
    data = load_transactions()
    print(f"Loaded {len(data)} MoMo transactions from {JSON_FILE.name}\n")

    #Demo on the first 20 records (minimum requirement)
    first20 = data[:20]
    d20 = build_dict(first20)
    target = 17
    print(f"Demo (20 records) - find id={target}")
    print("  Linear :", linear_search(first20, target)["type"],
          linear_search(first20, target)["amount"], "RWF")
    print("  Dict   :", dict_lookup(d20, target)["type"],
          dict_lookup(d20, target)["amount"], "RWF")
    print("  Missing id 99999 ->", linear_search(first20, 99999),
          dict_lookup(d20, 99999), "\n")

    # Searching and comparing
    sizes = [20, 100, 500, 1000, len(data)]
    print("Average time per search in microseconds (µs)")
    print(f"{'Records':>8} | {'Lin avg':>9} {'Lin worst':>10} | "
          f"{'Bin avg':>8} | {'Dict avg':>9} {'Dict worst':>10} | "
          f"{'Lin/Dict (avg)':>14}")
    print("-" * 88)
    for n in sizes:
        r = benchmark(data, n)
        print(f"{r['n']:>8} | {r['lin_avg']:>9.3f} {r['lin_worst']:>10.3f} | "
              f"{r['bin_avg']:>8.3f} | {r['dic_avg']:>9.3f} {r['dic_worst']:>10.3f} | "
              f"{r['lin_avg'] / r['dic_avg']:>13.1f}x")
