#!/usr/bin/env python3
""" 10-update_topics """


def update_topics(mongo_collection, name, topics):
    """
    Update a document in a collection based on name.

    Args:
        mongo_collection (pymongo.collection.Collection):
        The MongoDB collection to update the document in.
        name (str): The name of the document to update.
        topics (list): The list of topics to update the document with.
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
