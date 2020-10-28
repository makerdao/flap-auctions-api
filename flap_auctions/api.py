import tornado.web, tornado.escape
import logging
import datetime
import json

FLAPPER_TTL_MINUTES=30


class FlapAuctionsHandler(tornado.web.RequestHandler):
    logger = logging.getLogger()

    def initialize(self, database):
        self.db = database

    def get(self, id):
        self.logger.info(f"Querying for auction id {id}")

        if id:
            if id == 'events':
                days_ago_param = int(self.get_argument("daysAgo", 30, True))
                current_time = datetime.datetime.now()
                days_ago = int((current_time - datetime.timedelta(days=days_ago_param)).timestamp())
                result = self.db.get_all_events(days_ago)
                self.add_event_ids(result)
                self.write_result(result)
            else:
                result = self.db.get_events(int(id))
                if not result:
                    self.send_error(404)
                else:
                    self.add_event_ids(result)
                    self.write_result(result)
        else:
            status = self.get_argument("status", "", True)
            if status == "all":
                kicks = self.db.get_all_kicks()
                self.write_result(self.all_auction_response(kicks))
            elif status == "open":
                current_time = datetime.datetime.now()
                ttl_minutes_ago = int((current_time - datetime.timedelta(minutes=FLAPPER_TTL_MINUTES)).timestamp())
                kicks = self.db.get_kicks(ttl_minutes_ago, False)
                self.write_result(self.filtered_auction_response(kicks, 'open'))
            elif status == "closed":
                current_time = datetime.datetime.now()
                ttl_minutes_ago = int((current_time - datetime.timedelta(minutes=FLAPPER_TTL_MINUTES)).timestamp())
                kicks = self.db.get_kicks(ttl_minutes_ago, True)
                self.write_result(self.filtered_auction_response(kicks, 'closed'))

            address = self.get_argument("address", None, True)
            if address:
                tends = self.db.get_tends(address)
                self.write_result(tends)

    def write_result(self, result):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))

    @staticmethod
    def all_auction_response(kicks: []):
        current_time = datetime.datetime.now()
        ttl_minutes_ago = int((current_time - datetime.timedelta(minutes=FLAPPER_TTL_MINUTES)).timestamp())
        return list(map(lambda kick: {
            'auctionId': kick['auctionId'],
            'status': 'open' if kick['timestamp'] > ttl_minutes_ago else 'closed'
        }, kicks))

    @staticmethod
    def filtered_auction_response(kicks: [], status: str):
        return list(map(lambda kick: {
            'auctionId': kick['auctionId'],
            'status': status
        }, kicks))

    @staticmethod
    def add_event_ids(events: []):
        current_ids = {}
        for event in events:
            auction_id = event['auctionId']
            current_ids[auction_id] = current_ids.get(auction_id, 0) + 1
            event['id'] = current_ids[auction_id]
