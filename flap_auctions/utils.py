import os
import errno

from appdirs import user_cache_dir
from tinydb import TinyDB, JSONStorage
from tinydb.middlewares import CachingMiddleware


def get_auctions_db():
    db_folder = user_cache_dir("flaps", "maker")

    try:
        os.makedirs(db_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    db_file = os.path.join(db_folder, "auctions.txdb")
    return TinyDB(db_file, storage=CachingMiddleware(JSONStorage))

