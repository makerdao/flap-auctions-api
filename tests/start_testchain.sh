#!/bin/bash

docker run --rm -p 8545:8545 -p 8546:8546 -u="root" -w="/home/parity" --name="testchain" --entrypoint="/bin/sh" makerdao/testchain-pymaker:unit-testing-1.1.0 -c "/bin/parity --chain=/home/parity/config/parity-dev-constantinopole.json --tracing=on --pruning=archive --jsonrpc-interface=all --jsonrpc-hosts=all --jsonrpc-cors=all --base-path=/home/parity/.local/share/io.parity.ethereum/"