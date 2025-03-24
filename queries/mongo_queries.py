from queries.mongo_queries import *
from database.mongo import get_database

def q1(db):
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}]
    result = db.films.aggregate(pipeline)
    return list(result)

def q2(db):
    result = db.films.count_documents({"year": {"$gt": 1999}})
    return result

