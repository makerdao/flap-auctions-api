# Local testchain and starting auctions

To create surplus for kicking flap auctions see:
- install project using `./install-dev.sh` script from root dir
- run `./start_testchain.sh` from tests dir
- run `./start_test_api.sh` from tests dir
- run `./simulate_flap.sh` from tests dir (as many auctions you want to kick)
- to mint and send MKR to specific address run `./mint_mkr.sh {ADDRESS} {AMOUNT}`  
e.g. `./mint_mkr.sh 0x50FF810797f75f6bfbf2227442e0c961a8562F4C 100`
