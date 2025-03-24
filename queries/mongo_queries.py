def q1(db):
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}]
    result = db.films.aggregate(pipeline)
    return list(result)

def q2(db):
    pipeline = {"year": {"$gt": 1999}}
    result = db.films.count_documents(pipeline)
    return result

