# events_extractor.py
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
import threading
import time
import logging
import requests

from web3 import Web3, HTTPProvider
from pymaker.deployment import DssDeployment, Flapper

from flap_auctions.db_access import DbAdapter


class EventsExtractor(object):

    logger = logging.getLogger()

    def __init__(self, arguments, adapter: DbAdapter):
        self.rpc_url = arguments.rpc_url
        self.backup_rpc_url = arguments.backup_rpc_url if arguments.backup_rpc_url else arguments.rpc_url
        self.rpc_timeout = arguments.rpc_timeout
        self.interval = arguments.events_query_interval
        self.db = adapter

        self.connect()

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def connect(self):

        try:
            primary_url = self.rpc_url
            backup_url = self.backup_rpc_url

            self.web3 = Web3(HTTPProvider(endpoint_uri=primary_url, request_kwargs={"timeout": self.rpc_timeout}))
            self.mcd = DssDeployment.from_node(web3=self.web3)
            self.flapper = self.mcd.flapper

            self.rpc_url = backup_url
            self.backup_rpc_url = primary_url
        except requests.exceptions.ConnectionError:
            self.logger.error(f"Failed to connect to node!")

    def run(self):
        first_block = self.db.get_last_block()
        self.logger.warning(f"last queried block is {first_block}")

        while True:

            try:

                last_block = self.web3.eth.getBlock('latest').number

                if last_block > first_block:
                    self.logger.info(f"Retrieving Events between {first_block} and {last_block}")

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

            except requests.exceptions.ConnectionError:
                self.logger.error(f"Connection to {self.backup_rpc_url} failed, reconnecting to {self.rpc_url}!")
                self.connect()
            except:
                self.logger.error("Exception in events extractor, retry", exc_info=True)

            time.sleep(self.interval)
