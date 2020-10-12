# Flap Auctions API (WIP)

This project expose an API to query and bid on Flap auctions

TODO:
- implement bid endpoint
- add paginated endpoints
- add endpoint for gas estimation
- add posibility to unlock and use multiple accounts / choose which account to bid with
- bundle UI to consume API
At a minimum UI should display list of active auctions, list of closed auctions and auctions registered account bid on

## Installation

This project uses *Python 3.6.6* and requires *virtualenv* to be installed.

In order to clone the project and install required third-party packages please execute:
```
git clone https://github.com/grandizzy/flap-auctions-ui.git
cd flap-auctions-ui
git submodule update --init --recursive
./install.sh
```

## Running

```
usage: flap-auctions-api [-h] --rpc-url RPC_URL [--rpc-timeout RPC_TIMEOUT]
                         --eth-from ETH_FROM [--http-address HTTP_ADDRESS]
                         [--http-port HTTP_PORT]
                         [--events-query-interval EVENTS_QUERY_INTERVAL]
```

## API

### `GET http://localhost:7777/api/flaps/?status=all|open|closed`

Returns ids and status for flaps auctions, filtered by status, e.g:

```
{"result": [{"auction_id": 1, "status": "closed"}, {"auction_id": 2, "status": "open"}]}
```

### `GET http://localhost:7777/api/flaps/?address=0x00...`

Returns all tends of specified address, e.g:

```
{"result": [{"auction_id": 13, "type": "tend", "bid": 1.1, "block": 11031171, "timestamp": 1602378715, "bidder": "0x0000....", "lot": 10000.0, "tx_hash": "0x...."}]}
```

### `GET http://localhost:7777/api/flaps/{id}`

Returns all events for auction with id {id}

### `POST http://localhost:7777/api/flaps/{id}`

Place a bid on auction with id {id}. JSON posted should contain MKR amount to bid, e.g. `{"mkr-amount": 16.56}`

## Sample startup script

```
#!/bin/bash

bin/flap-auctions \
    --rpc-url https://localhost:8545/ \
    --eth-from 0x0000....
```

