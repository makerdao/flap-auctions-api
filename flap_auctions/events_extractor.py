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

                try:

                    history = self.flapper.past_logs(first_block, int(last_block))

                    events = []
                    for log in history:

                        event = None

                        if isinstance(log, Flapper.TendLog):
                            event = {
                                'auctionId': log.id,
                                'type': 'Tend',
                                'hash': log.tx_hash,
                                'fromAddress': log.guy.address,
                                'lot': float(log.lot),
                                'bid': float(log.bid),
                                'timestamp': self.web3.eth.getBlock(log.block).timestamp,
                                'block': log.block
                            }
                        elif isinstance(log, Flapper.DealLog):
                            event = {
                                'auctionId': log.id,
                                'type': 'Deal',
                                'hash': log.tx_hash,
                                'fromAddress': log.usr.address,
                                'timestamp': self.web3.eth.getBlock(log.block).timestamp,
                                'block': log.block
                            }
                        elif isinstance(log, Flapper.KickLog):
                            tx_details = self.web3.eth.getTransaction(log.tx_hash)
                            event = {
                                'auctionId': log.id,
                                'type': 'Kick',
                                'hash': log.tx_hash,
                                'fromAddress': tx_details['from'] if tx_details else "",
                                'lot': float(log.lot),
                                'bid': float(log.bid),
                                'timestamp': self.web3.eth.getBlock(log.block).timestamp,
                                'block': log.block
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

                except Exception:
                    self.logger.error("Exception in events extractor, retry", exc_info=True)

                time.sleep(self.interval)
