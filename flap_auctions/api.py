import tornado.web, tornado.escape
import logging

from flap_auctions.utils import get_auctions_db
from tinydb import where


class FlapAuctionsHandler(tornado.web.RequestHandler):
    logger = logging.getLogger()

    def get(self, id):
        self.logger.warning(f"Querying for id {id}")
        with get_auctions_db() as db:
            if id:
                self.write({
                    'result': db.search(where('id') == int(id))
                })
            else:
                self.write({
                    'result': db.all()
                })

    def post(self, id):
        if id:
            data = tornado.escape.json_decode(self.request.body)
            if 'mkr-amount' in data:
                self.logger.warning(f"bidding {data['mkr-amount']} on auction {id}")
                self.write("Bidding")
            else:
                self.write_error(400)
