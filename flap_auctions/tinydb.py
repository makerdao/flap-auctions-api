import os
import errno

from appdirs import user_cache_dir
from tinydb import TinyDB, JSONStorage
from tinydb.middlewares import CachingMiddleware

from tinydb import where

from flap_auctions.db_access import DbAdapter


def get_auctions_db(db_folder):
    db_file = os.path.join(db_folder, "auctions.txdb")
    return TinyDB(db_file, storage=CachingMiddleware(JSONStorage))


def get_block_file(db_folder):
    return os.path.join(db_folder, "last_block.txt")


class TinyDbAdapter(DbAdapter):

    def __init__(self, intial_block: int):

        self.db_folder = user_cache_dir("flaps", "maker")
        self.intial_block = intial_block

        try:
            os.makedirs(self.db_folder)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        self.block_file = get_block_file(self.db_folder)
        if not os.path.isfile(self.block_file):
            block_file = open(self.block_file, "w")
            block_file.write(str(intial_block))
            block_file.close()

    def cleanup(self):
        os.remove(os.path.join(user_cache_dir("flaps", "maker"), "auctions.txdb"))

        block_file = open(self.block_file, "w")
        block_file.write(str(self.intial_block))
        block_file.close()

    def get_last_block(self) -> int:
        block_file = open(self.block_file, "r")
        return int(block_file.read())

    def save_queried_block(self, block: int):
        block_file = open(self.block_file, "r+")
        block_file.seek(0)
        block_file.write(str(block))
        block_file.truncate()

    def get_events(self, auction_id: int):
        with get_auctions_db(self.db_folder) as db:
            return db.search(where('auctionId') == auction_id)

    def get_all_events(self, days_ago: int):
        with get_auctions_db(self.db_folder) as db:
            return db.search(where('timestamp') > days_ago)

    def insert_events(self, events: []):
        with get_auctions_db(self.db_folder) as db:
            db.insert_multiple(events)
            db.close()

    def get_all_kicks(self):
        with get_auctions_db(self.db_folder) as db:
            return db.search((where('type') == 'Kick'))

    def get_kicks(self, minutes_ago: int, expired: bool):
        with get_auctions_db(self.db_folder) as db:
            if expired:
                return db.search((where('type') == 'Kick') & (where('timestamp') < minutes_ago))
            return db.search((where('type') == 'Kick') & (where('timestamp') > minutes_ago))

    def get_tends(self, address: str):
        with get_auctions_db(self.db_folder) as db:
            return db.search((where('type') == 'Tend') & (where('fromAddress') == address))
