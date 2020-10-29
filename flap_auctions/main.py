import argparse
import logging
import sys
import tornado.ioloop
import tornado.web

from web3 import Web3, HTTPProvider

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

        self.web3 = kwargs['web3'] if 'web3' in kwargs else Web3(HTTPProvider(endpoint_uri=self.arguments.rpc_url,
                                                                              request_kwargs={"timeout": self.arguments.rpc_timeout}))

        self.adapter = DbAdapterFactory.get_db_adapter(self.arguments)

    def main(self):

        if self.arguments.resync:
            self.adapter.cleanup()

        self.logger.info("Starting events extractor thread")
        EventsExtractor(self.web3, self.adapter, self.arguments.events_query_interval)

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
