# main.py
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
import argparse
import logging
import sys
import tornado.ioloop
import tornado.web

from flap_auctions.db_access import DbAdapter
from flap_auctions.events_extractor import EventsExtractor
from flap_auctions.api import FlapAuctionsHandler

from flap_auctions.tinydb import TinyDbAdapter
from flap_auctions.mongodb import MongoDbAdapter


class FlapAuctions:

    logger = logging.getLogger()

    def __init__(self, args: list, **kwargs):
        parser = argparse.ArgumentParser(prog='flap-auctions-api')

        parser.add_argument("--rpc-url", type=str, required=True,
                            help="JSON-RPC host URL")

        parser.add_argument("--backup-rpc-url", type=str, required=False,
                            help="JSON-RPC backup host URL. "
                                 "If not specified process will retry to connect to JSON-RPC host URL")

        parser.add_argument("--rpc-timeout", type=int, default=10,
                            help="JSON-RPC timeout (in seconds, default: 10)")

        parser.add_argument("--http-address", type=str, default='0.0.0.0',
                            help="Address of the Flap API")

        parser.add_argument("--http-port", type=int, default=7777,
                            help="Port of the Flap API (default: 7777)")

        parser.add_argument("--events-query-interval", type=int, default=30,
                            help="time window to wait and recheck for events (in seconds, default: 30)")

        parser.add_argument("--sync-from-block", type=int, default=10769102,
                            help="Block to start syncing from (default: 10769102)")

        parser.add_argument("--resync", dest='resync', action='store_true', default=False,
                            help="Resync all events from the sync-from-block value to current block. "
                                 "Existing entries in db will be removed")

        parser.add_argument("--mongo-url", type=str, required=False,
                            help="MongoDb connection string")

        parser.add_argument("--tinydb", dest='tinydb', action='store_true', default=True,
                            help="Use Tinydb")

        self.arguments = parser.parse_args(args)

        self.adapter = DbAdapterFactory.get_db_adapter(self.arguments)

    def main(self):

        if self.arguments.resync:
            self.adapter.cleanup()

        self.logger.info("Starting events extractor thread")
        EventsExtractor(self.arguments, self.adapter)

        self.logger.info("Starting web app!!!")
        application = tornado.web.Application([
            (r"/api/flaps/([^/]*)", FlapAuctionsHandler, dict(database=self.adapter))
        ])
        application.listen(port=self.arguments.http_port, address=self.arguments.http_address)
        tornado.ioloop.IOLoop.current().start()


class DbAdapterFactory:
    @staticmethod
    def get_db_adapter(arguments) -> DbAdapter:
        if arguments.mongo_url:
            return MongoDbAdapter(arguments.mongo_url, arguments.sync_from_block)
        elif arguments.tinydb:
            return TinyDbAdapter(arguments.sync_from_block)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s', level=logging.INFO)
    FlapAuctions(sys.argv[1:]).main()
