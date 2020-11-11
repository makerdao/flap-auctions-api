# db_access.py
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





