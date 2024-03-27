#!/usr/bin/env python3
"""
This module provides a function to list all documents in a MongoDB collection.
"""


def list_all(mongo_collection) -> list:
    """
    Retrieve all documents from a MongoDB collection.

    Args:
        mongo_collection (pymongo.collection.Collection):
        The MongoDB collection to retrieve documents from.

    Returns:
        list: A list of all documents in the collection.
    """
    return mongo_collection.find()
