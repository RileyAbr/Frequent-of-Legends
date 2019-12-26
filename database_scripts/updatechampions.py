import requests, json
import pymongo
from DBKEYS import database_client

# MongoDB database info
mongoclient = pymongo.MongoClient(database_client)
db = mongoclient.pythoninsert
col = db.championdata
cursor = col.find({}).sort("key", 1)

def json_print(json_str):
    text = json.dumps(json_str, sort_keys=True, indent=4)
    print(text)

count = 0

champ_key = 1

# Updates the key value in each champion listing with a new column for the numerical key value
for document in cursor:
    champ_key_str = document["key"]
    champ_key_int = int(champ_key_str)

    col.update_one({
        "key": champ_key_str
    }, {
        "$set": {
        "num_key": champ_key_int}
    }, upsert=False)

    count += 1

for document in cursor:
    print(document["key"])
    print()

print(str(count) + " champions")