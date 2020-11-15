# Flap Auctions API (WIP)

This project expose an API to query and bid on Flap auctions.
By default it saves data in TinyDb database. If started with `--mongo-url` switch then it use MongoDb to store flaps events.

A simple way to stand up a mongodb test instance locally is running in Docker: `docker run -p 27017:27017 --name flaps-mongo -d mongo`.
To make use of it pass `--mongo-url 'mongodb://localhost:27017/'` to startup script.


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
usage: flap-auctions-api [-h] --rpc-url RPC_URL
                         [--backup-rpc-url BACKUP_RPC_URL]
                         [--rpc-timeout RPC_TIMEOUT]
                         [--http-address HTTP_ADDRESS] [--http-port HTTP_PORT]
                         [--events-query-interval EVENTS_QUERY_INTERVAL]
                         [--sync-from-block SYNC_FROM_BLOCK] [--resync]
                         [--mongo-url MONGO_URL] [--tinydb]

optional arguments:
  -h, --help            show this help message and exit
  --rpc-url RPC_URL     JSON-RPC host URL
  --backup-rpc-url BACKUP_RPC_URL
                        JSON-RPC backup host URL. If not specified process
                        will retry to connect to JSON-RPC host URL
  --rpc-timeout RPC_TIMEOUT
                        JSON-RPC timeout (in seconds, default: 10)
  --http-address HTTP_ADDRESS
                        Address of the Flap API
  --http-port HTTP_PORT
                        Port of the Flap API (default: 7777)
  --events-query-interval EVENTS_QUERY_INTERVAL
                        time window to wait and recheck for events (in
                        seconds, default: 30)
  --sync-from-block SYNC_FROM_BLOCK
                        Block to start syncing from (default: 10769102)
  --resync              Resync all events from the sync-from-block value to
                        current block. Existing entries in db will be removed
  --mongo-url MONGO_URL
                        MongoDb connection string
  --tinydb              Use Tinydb
```

##### For building and running as Docker image:
- clone repo and run `git submodule update --init --recursive`
- build image: `docker build -t makerdao/flaps-api .`  
- run container: `docker run -p 7777:7777 --name="flaps-api" makerdao/flaps-api --rpc-url http://localhost:8545/ --sync-from-block 11238000`


## API

### `GET http://localhost:7777/api/flaps/?status=all|open|closed`

Returns ids and status for flaps auctions, filtered by status, e.g:

```
[
   {
      "auctionId":1,
      "status":"closed"
   },
   {
      "auctionId":2,
      "status":"open"
   }
]
```

### `GET http://localhost:7777/api/flaps/{id}`

Returns all events for auction with id {id}

E.g. for http://localhost:7777/api/flaps/1

```
[
   {
      "auctionId":1,
      "type":"Kick",
      "hash":"0xc92d3b834d2a9aadd4286293949763a164427627fe407ea10872c7984640788b",
      "fromAddress":"0xblah...",
      "lot":10000.0,
      "bid":0.0,
      "timestamp":1602249472,
      "block":11021478,
      "id":1
   },
   {
      "auctionId":1,
      "type":"Tend",
      "hash":"0x88fe223ef0fa0901474ddf445f933096f2768508e07eed812ea6a7aa22eea2dc",
      "fromAddress":"0xblah...",
      "lot":10000.0,
      "bid":17.465431115615726,
      "timestamp":1602249566,
      "block":11021490,
      "id":2
   },
   {
      "auctionId":1,
      "type":"Tend",
      "hash":"0xc6489fbc1e6aee5df75c4c5a8c15ebb551f897dd762e831c36809a07c585303e",
      "fromAddress":"0xblah...",
      "lot":10000.0,
      "bid":17.816486281,
      "timestamp":1602251290,
      "block":11021620,
      "id":3
   },
   {
      "auctionId":1,
      "type":"Deal",
      "hash":"0x40e8182e20f4b03ecd05fd0ff4122cdea055c6d984546730769baa6decb3cc0c",
      "fromAddress":"0xblah...",
      "timestamp":1602253145,
      "block":11021768,
      "id":4
   }
]

```

### `GET http://localhost:7777/api/flaps/events?daysAgo=10`

Returns all flap events (if `daysAgo` query parameter is not specified then it returns events for last 30 days)

E.g. for http://localhost:7777/api/flaps/events?daysAgo=2

```
[
   {
      "auctionId":140,
      "type":"Kick",
      "hash":"0xf0e245231d2120f34db04b52ed83999dd6255fe75c629cc9e5f7c87381549d70",
      "fromAddress":"0xblah...",
      "lot":10000.0,
      "bid":0.0,
      "timestamp":1603749259,
      "block":11134592,
      "id":1
   },
   {
      "auctionId":140,
      "type":"Tend",
      "hash":"0xf0e245231d2120f34db04b52ed83999dd6255fe75c629cc9e5f7c87381549d70",
      "fromAddress":"0xblah...",
      "lot":10000.0,
      "bid":17.2291027916172,
      "timestamp":1603749259,
      "block":11134592,
      "id":2
   },
   {
      "auctionId":140,
      "type":"Deal",
      "hash":"0x7444fe372926be6289c712e6ddc272e1b174f7c4319f0043dc30c8d8353ff92a",
      "fromAddress":"0xblah...",
      "timestamp":1603751223,
      "block":11134754,
      "id":3
   },
   {
      "auctionId":141,
      "type":"Kick",
      "hash":"0x6f2fadc8305cbc8710cc74325bb26b9f6e228a549b53fbd78df45b0cdc26b565",
      "fromAddress":"0xblah...",
      "lot":10000.0,
      "bid":0.0,
      "timestamp":1603759860,
      "block":11135409,
      "id":1
   },
   {
      "auctionId":141,
      "type":"Tend",
      "hash":"0x6f2fadc8305cbc8710cc74325bb26b9f6e228a549b53fbd78df45b0cdc26b565",
      "fromAddress":"0xblah...",
      "lot":10000.0,
      "bid":17.121354070553,
      "timestamp":1603759860,
      "block":11135409,
      "id":2
   },
   {
      "auctionId":141,
      "type":"Deal",
      "hash":"0xddace6c12cd015d36c4a5a6fc2e9450706a5c85e340ac93254f6db885781dcf4",
      "fromAddress":"0xblah...",
      "timestamp":1603761762,
      "block":11135560,
      "id":3
   }
]

```

### `GET http://localhost:7777/api/flaps/?address=0x00...`

Returns all tends of specified address, e.g for http://localhost:7777/api/flaps/?address=0xblah...:

```
[
   {
      "auctionId":109,
      "type":"Tend",
      "hash":"0x99f2245fbc689aa307c9ea4f0304b7bd64e37efe1044926dc291b5c48366c8bc",
      "fromAddress":"0xblah...",
      "lot":10000.0,
      "bid":16.4307099929803,
      "timestamp":1603421043,
      "block":11109925
   },
   {
      "auctionId":110,
      "type":"Tend",
      "hash":"0x3c7e05f8421d917c89a4bb482b415eef1466a21c37e7d8ee2473066434de20ab",
      "fromAddress":"0xblah...",
      "lot":10000.0,
      "bid":16.3548767241029,
      "timestamp":1603431809,
      "block":11110738
   }
]
```

## Sample startup scripts

Sync events from default block (10769102):

```
#!/bin/bash

bin/flap-auctions \
    --rpc-url https://mainnet.infura.io/v3/key
```

Sync events from default block using a JSON RPC backup url:

```
#!/bin/bash

bin/flap-auctions \
    --rpc-url https://mainnet.infura.io/v3/key \
    --backup-rpc-url http://localhost:8545/
```

Drop database and sync events from block 11065593:

```
#!/bin/bash

bin/flap-auctions \
    --rpc-url https://mainnet.infura.io/v3/key \
    --sync-from-block 11065593 \
    --resync
```

Sync events and store them in MongoDB:

```
#!/bin/bash

bin/flap-auctions \
    --rpc-url https://mainnet.infura.io/v3/key \
    --mongo-url 'mongodb://localhost:27017/'
```
