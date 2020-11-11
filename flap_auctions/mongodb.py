# mongodb.py
# Copyright (C) 2020 Maker Ecosystem Growth Holdings, INC.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
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

    def __init__(self, mongo_url: str, intial_block: int):
        mongo_client = pymongo.MongoClient(mongo_url)
        db = mongo_client["auctions"]
        self.intial_block = intial_block
        self.flaps_collection = db["flaps"]
        self.block_collection = db["block"]

    def cleanup(self):
        self.flaps_collection.drop()
        self.block_collection.drop()

    def get_last_block(self) -> int:
        block = self.block_collection.find_one()
        if not block:
            self.block_collection.insert({'id': 1, 'block': self.intial_block})
            return self.intial_block
        return block['block']

    def save_queried_block(self, block: int):
        self.block_collection.find_one_and_replace({'id': 1}, {'id': 1, 'block': block})

    def get_events(self, auction_id: int):
        cursor = self.flaps_collection.find({'auctionId': auction_id}, {'_id': 0})
        if cursor:
            return json.loads(JSONEncoder().encode(list(cursor)))

    def get_all_events(self, days_ago: int):
        cursor = self.flaps_collection.find({'timestamp': {'$gt': days_ago}}, {'_id': 0})
        if cursor:
            return json.loads(JSONEncoder().encode(list(cursor)))

    def insert_events(self, events: []):
        self.flaps_collection.insert_many(events)

    def get_all_kicks(self):
        return self.flaps_collection.find({'type': 'Kick'}, {'_id': 0})

    def get_kicks(self, minutes_ago: int, expired: bool):
        return self.flaps_collection.find({'$and': [{'type': 'Kick'}, {'timestamp': {'$lt' if expired else '$gt': minutes_ago}}]}, {'_id': 0})

    def get_tends(self, address: str):
        cursor = self.flaps_collection.find({'$and': [{'type': 'Tend'}, {'fromAddress': address}]}, {'_id': 0})
        if cursor:
            return json.loads(JSONEncoder().encode(list(cursor)))
