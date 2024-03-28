#!/usr/bin/env python3
""" 12-log_stats """

from pymongo import MongoClient
from typing import Tuple, Dict


def log_stats(mongo_collection) -> Tuple[int, Dict[str, int], int]:
    """
    Log stats from a MongoDB collection.

    Args:
        mongo_collection (pymongo.collection.Collection):
        The MongoDB collection to log stats from.
    """
    total_logs: int = mongo_collection.count_documents({})

    methods: Tuple[str, ...] = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_count: Dict[str, int] = {method: mongo_collection.count_documents(
        {"method": method}) for method in methods}

    status_count: int = mongo_collection.count_documents({"method": "GET",
                                                          "path": "/status"})

    return total_logs, method_count, status_count


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    total_logs, method_count, status_count = log_stats(collection)

    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_count.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_count} status check")
