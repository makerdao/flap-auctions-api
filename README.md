# Flap Auctions API (WIP)

This project expose an API to query and bid on Flap auctions

TODO:
- implement bid endpoint
- add paginated endpoints
- add query string param to flaps endpoint for retrieving only active / closed auctions
- add query string param to flaps endpoint for retrieving auctions bidded from a specific account
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

### `GET http://localhost:7777/api/flaps/`

Returns all events for all flaps auctions

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

