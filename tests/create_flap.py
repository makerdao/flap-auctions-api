from web3 import Web3, HTTPProvider

from pymaker import Address
from pymaker.deployment import DssDeployment
from pymaker.keys import register_keys
from pymaker.numeric import Wad
from tests.test_dss import wrap_eth, frob

web3 = Web3(HTTPProvider(endpoint_uri="http://0.0.0.0:8545"))
web3.eth.defaultAccount = "0x50FF810797f75f6bfbf2227442e0c961a8562F4C"
register_keys(web3,
              ["key_file=../lib/pymaker/tests/config/keys/UnlimitedChain/key1.json,pass_file=/dev/null",
               "key_file=../lib/pymaker/tests/config/keys/UnlimitedChain/key2.json,pass_file=/dev/null",
               "key_file=../lib/pymaker/tests/config/keys/UnlimitedChain/key3.json,pass_file=/dev/null",
               "key_file=../lib/pymaker/tests/config/keys/UnlimitedChain/key4.json,pass_file=/dev/null",
               "key_file=../lib/pymaker/tests/config/keys/UnlimitedChain/key.json,pass_file=/dev/null"])
mcd = DssDeployment.from_node(web3)
deployment_address = Address("0x00a329c0648769A73afAc7F9381E08FB43dBEA72")

joy = mcd.vat.dai(mcd.vow.address)

if joy < mcd.vow.hump() + mcd.vow.bump():
    # Create a CDP with surplus
    print('Creating a CDP with surplus')
    collateral = mcd.collaterals['ETH-B']
    wrap_eth(mcd, deployment_address, Wad.from_number(0.1))
    collateral.approve(deployment_address)
    assert collateral.adapter.join(deployment_address, Wad.from_number(0.1)).transact(
        from_address=deployment_address)
    frob(mcd, collateral, deployment_address, dink=Wad.from_number(0.1), dart=Wad.from_number(10))
    assert mcd.jug.drip(collateral.ilk).transact(from_address=deployment_address)
    joy = mcd.vat.dai(mcd.vow.address)
    assert joy >= mcd.vow.hump() + mcd.vow.bump()
else:
    print(f'Surplus of {joy} already exists; skipping CDP creation')

mcd.vow.flap().transact()
kick = mcd.flapper.kicks()
print(f"There are {kick} flap auctions kicked")
