#!/usr/bin/env python3
""" 11-schools_by_topic """


def schools_by_topic(mongo_collection, topic):
    """
    Return the list of school having a specific topic.

    Args:
        mongo_collection (pymongo.collection.Collection):
        The MongoDB collection to query.
        topic (str): The topic to search for.

    Returns:
        list: The list of school having the specified topic.
    """
    return mongo_collection.find({"topics": topic})
