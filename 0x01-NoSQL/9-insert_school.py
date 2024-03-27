#!/usr/bin/env python3
""" 9-insert_school """


def insert_school(mongo_collection, **kwargs) -> str:
    """
    Insert a document in a collection based on kwargs.

    Args:
        mongo_collection (pymongo.collection.Collection):
        The MongoDB collection to insert the document into.
        **kwargs (dict): The document to insert.

    Returns:
        str: The new _id.
    """
    return mongo_collection.insert_one(kwargs).inserted_id
