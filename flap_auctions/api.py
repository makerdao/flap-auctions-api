import tornado.web, tornado.escape
import logging
import datetime

from flap_auctions.utils import get_auctions_db
from tinydb import where

FLAPPER_TTL_MINUTES=30

class FlapAuctionsHandler(tornado.web.RequestHandler):
    logger = logging.getLogger()

    def get(self, id):
        self.logger.info(f"Querying for auction id {id}")
        with get_auctions_db() as db:
            if id:
                result = db.search(where('auction_id') == int(id))
                if not result:
                    self.send_error(404)
                else:
                    self.write({
                        'result': db.search(where('auction_id') == int(id))
                    })
            else:
                status = self.get_argument("status", "", True)
                if status == "all":
                    kicks = db.search((where('type') == 'kick'))
                    self.write({
                        'result': self.all_auction_response(kicks)
                    })
                elif status == "open":
                    current_time = datetime.datetime.now()
                    ttl_minutes_ago = int((current_time - datetime.timedelta(minutes=FLAPPER_TTL_MINUTES)).timestamp())
                    kicks = db.search((where('type') == 'kick') & (where('timestamp') > ttl_minutes_ago))
                    self.write({
                        'result': self.filtered_auction_response(kicks, 'open')
                    })
                elif status == "closed":
                    current_time = datetime.datetime.now()
                    ttl_minutes_ago = int((current_time - datetime.timedelta(minutes=FLAPPER_TTL_MINUTES)).timestamp())
                    kicks = db.search((where('type') == 'kick') & (where('timestamp') < ttl_minutes_ago))
                    self.write({
                        'result': self.filtered_auction_response(kicks, 'closed')
                    })

                address = self.get_argument("address", None, True)
                if address:
                    tends = db.search((where('type') == 'tend') & (where('bidder') == address))
                    self.write({
                        'result': tends
                    })

    def post(self, id):
        if id:
            data = tornado.escape.json_decode(self.request.body)
            if 'mkr-amount' in data:
                self.logger.info(f"bidding {data['mkr-amount']} on auction {id}")
                self.write("Bidding")
            else:
                self.send_error(400)

    @staticmethod
    def all_auction_response(kicks: []):
        current_time = datetime.datetime.now()
        ttl_minutes_ago = int((current_time - datetime.timedelta(minutes=FLAPPER_TTL_MINUTES)).timestamp())
        return list(map(lambda kick: {
            'auction_id': kick['auction_id'],
            'status': 'open' if kick['timestamp'] > ttl_minutes_ago else 'closed'
        }, kicks))

    @staticmethod
    def filtered_auction_response(kicks: [], status: str):
        return list(map(lambda kick: {
            'auction_id': kick['auction_id'],
            'status': status
        }, kicks))
