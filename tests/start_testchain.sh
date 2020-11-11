#!/bin/bash
# start_testchain.sh
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

docker run --rm -p 8545:8545 -p 8546:8546 -u="root" -w="/home/parity" --name="testchain" --entrypoint="/bin/sh" makerdao/testchain-pymaker:unit-testing-1.1.0 -c "/bin/parity --chain=/home/parity/config/parity-dev-constantinopole.json --tracing=on --pruning=archive --jsonrpc-interface=all --jsonrpc-hosts=all --jsonrpc-cors=all --base-path=/home/parity/.local/share/io.parity.ethereum/"