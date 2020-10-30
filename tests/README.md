# Local testchain

Use `./start_testchain.sh` command to start a local testchain.

Sample script to connect flap auction API to local testchain:

```
#!/bin/bash

bin/flap-auctions \
    --rpc-url http://localhost:8545/ \
    --sync-from-block 0 \
    --resync

```

To create surplus for kicking flap auctions see:
https://github.com/makerdao/pymaker/blob/master/tests/test_auctions.py#L32
