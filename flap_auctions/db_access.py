class DbAdapter:
    """
    Define a common interface for database adapters
    """

    def cleanup(self) -> int:
        raise NotImplementedError()

    def get_last_block(self) -> int:
        raise NotImplementedError()

    def save_queried_block(self, block: int):
        raise NotImplementedError()

    def get_events(self, auction_id: int):
        raise NotImplementedError()

    def get_all_events(self, days_ago: int):
        raise NotImplementedError()

    def insert_events(self, events: []):
        raise NotImplementedError()

    def get_all_kicks(self):
        raise NotImplementedError()

    def get_kicks(self, minutes_ago: int, expired: bool):
        raise NotImplementedError()

    def get_tends(self, address: str):
        raise NotImplementedError()





