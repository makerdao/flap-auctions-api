#!/bin/bash

docker run --rm -p 8545:8545 -u="root" -w="/home/parity" --name="testchain" makerdao/testchain-pymaker:unit-testing-1.1.0