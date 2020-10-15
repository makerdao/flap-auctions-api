import pymongo
import json

from bson import ObjectId
from flap_auctions.db_access import DbAdapter


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class MongoDbAdapter(DbAdapter):

    def __init__(self, mongo_url: str):
        mongo_client = pymongo.MongoClient(mongo_url)
        db = mongo_client["auctions"]
        self.flaps_collection = db["flaps"]
        self.block_collection = db["block"]

    def get_last_block(self) -> int:
        block = self.block_collection.find_one()
        if not block:
            self.block_collection.insert({'id': 1, 'block': 10769102})
            return 10769102
        return block['block']

    def save_queried_block(self, block: int):
        self.block_collection.find_one_and_replace({'id': 1}, {'id': 1, 'block': block})

    def get_events(self, auction_id: int):
        cursor = self.flaps_collection.find({'auction_id': auction_id}, {'_id': 0})
        if cursor:
            return json.loads(JSONEncoder().encode(list(cursor)))

    def insert_events(self, events: []):
        self.flaps_collection.insert_many(events)

    def get_all_kicks(self):
        return self.flaps_collection.find({'type': 'kick'}, {'_id': 0})

    def get_kicks(self, minutes_ago: int, expired: bool):
        return self.flaps_collection.find({'$and': [{'type': 'kick'}, {'timestamp': {'$lt' if expired else '$gt': minutes_ago}}]}, {'_id': 0})

    def get_tends(self, address: str):
        cursor = self.flaps_collection.find({'$and': [{'type': 'tend'}, {'bidder': address}]}, {'_id': 0})
        if cursor:
            return json.loads(JSONEncoder().encode(list(cursor)))
