import threading
import time
import logging
import os

from web3 import Web3
from pymaker.deployment import DssDeployment, Flapper
from flap_auctions.utils import get_auctions_db


class EventsExtractor(object):

    logger = logging.getLogger()

    def __init__(self, web3: Web3, interval=1):
        self.web3 = web3
        self.mcd = DssDeployment.from_node(web3=self.web3)
        self.flapper = self.mcd.flapper
        self.interval = interval

        if not os.path.isfile('./last_block.txt'):
            block_file = open("./last_block.txt", "w")
            block_file.write("10769102")
            block_file.close()

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):

        block_file = open("./last_block.txt", "r+")
        first_block = int(block_file.read())
        self.logger.warning(f"las queried block is {first_block}")

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
                            'id': log.id,
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
                            'id': log.id,
                            'type': 'deal',
                            'block': log.block,
                            'timestamp': self.web3.eth.getBlock(log.block).timestamp,
                            'dealer': log.usr.address,
                            'tx_hash': log.tx_hash
                        }
                    elif isinstance(log, Flapper.KickLog):
                        event = {
                            'id': log.id,
                            'type': 'kick',
                            'bid': float(log.bid),
                            'block': log.block,
                            'timestamp': self.web3.eth.getBlock(log.block).timestamp,
                            'lot': float(log.lot),
                            'tx_hash': log.tx_hash
                        }

                    if event:
                        events.append(event)

                self.logger.info(f"Events between {first_block} and {last_block} are: {events}")
                with get_auctions_db() as db:
                    db.insert_multiple(events)
                    db.close()

                block_file.seek(0)
                block_file.write(str(last_block))
                block_file.truncate()

                first_block = last_block
                time.sleep(self.interval)
