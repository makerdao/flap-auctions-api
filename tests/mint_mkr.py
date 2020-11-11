# mint_mkr.py
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
from web3 import Web3, HTTPProvider
import sys

from pymaker import Address
from pymaker.deployment import DssDeployment
from pymaker.keys import register_keys
from pymaker.numeric import Wad
from tests.test_dss import mint_mkr

web3 = Web3(HTTPProvider(endpoint_uri="http://0.0.0.0:8545"))
web3.eth.defaultAccount = "0x50FF810797f75f6bfbf2227442e0c961a8562F4C"
register_keys(web3,
              ["key_file=../lib/pymaker/tests/config/keys/UnlimitedChain/key1.json,pass_file=/dev/null",
               "key_file=../lib/pymaker/tests/config/keys/UnlimitedChain/key2.json,pass_file=/dev/null",
               "key_file=../lib/pymaker/tests/config/keys/UnlimitedChain/key3.json,pass_file=/dev/null",
               "key_file=../lib/pymaker/tests/config/keys/UnlimitedChain/key4.json,pass_file=/dev/null",
               "key_file=../lib/pymaker/tests/config/keys/UnlimitedChain/key.json,pass_file=/dev/null"])
mcd = DssDeployment.from_node(web3)

mint_mkr(mcd.mkr, Address(sys.argv[1]), Wad.from_number(sys.argv[2]))
print(f"MKR balance for {sys.argv[1]} is {mcd.mkr.balance_of(Address(sys.argv[1]))}")
