import threading
import time
import logging

from web3 import Web3
from pymaker.deployment import DssDeployment, Flapper

from flap_auctions.db_access import DbAdapter


class EventsExtractor(object):

    logger = logging.getLogger()

    def __init__(self, web3: Web3, adapter: DbAdapter, interval=1):
        self.web3 = web3
        self.mcd = DssDeployment.from_node(web3=self.web3)
        self.flapper = self.mcd.flapper
        self.interval = interval
        self.db = adapter

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):

        first_block = self.db.get_last_block()
        self.logger.warning(f"last queried block is {first_block}")

        while True:

            last_block = self.web3.eth.getBlock('latest').number

            if last_block > first_block:
                self.logger.info(f"Retrieving Events between {first_block} and {last_block}")

                history = self.flapper.past_logs(first_block, int(last_block))

                events = []
                for log in history:

                    event = None

                    if isinstance(log, Flapper.TendLog):
                        event = {
                            'auction_id': log.id,
                            'type': 'tend',
                            'bid': float(log.bid),
                            'block': log.block,
                            'timestamp': self.web3.eth.getBlock(log.block).timestamp,
                            'bidder': log.guy.address,
                            'lot': float(log.lot),
                            'tx_hash': log.tx_hash
                        }
                    elif isinstance(log, Flapper.DealLog):
                        event = {
                            'auction_id': log.id,
                            'type': 'deal',
                            'block': log.block,
                            'timestamp': self.web3.eth.getBlock(log.block).timestamp,
                            'dealer': log.usr.address,
                            'tx_hash': log.tx_hash
                        }
                    elif isinstance(log, Flapper.KickLog):
                        event = {
                            'auction_id': log.id,
                            'type': 'kick',
                            'bid': float(log.bid),
                            'block': log.block,
                            'timestamp': self.web3.eth.getBlock(log.block).timestamp,
                            'lot': float(log.lot),
                            'tx_hash': log.tx_hash
                        }

                    if event:
                        events.append(event)

                if events:
                    self.logger.info(f"Events between {first_block} and {last_block} are: {events}")
                    self.db.insert_events(events)
                else:
                    self.logger.info(f"No new events between {first_block} and {last_block}")

                self.db.save_queried_block(last_block + 1)

                first_block = last_block + 1
                time.sleep(self.interval)
