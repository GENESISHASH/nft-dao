#!/usr/bin/python3

import os
from brownie import GovernanceToken, PunksToken, StableToken, Vault, accounts

def main():

    account = accounts.load('devel')
    publish_source = False

    gov_token = GovernanceToken.deploy("Governance", "GOV", 1000000, {'from':account}, publish_source=publish_source)
    stable_token = StableToken.deploy("PUSD Stablecoin", "PUSD", {'from':account}, publish_source=publish_source)
    punks_token = PunksToken.deploy("FakePunks", "FPUNK", 100, {'from':account}, publish_source=publish_source)
    vault = Vault.deploy("Vault", stable_token, {"from":account}, publish_source=publish_source)

    stable_token.add_minter(vault,{'from':account})
    vault.set_token_value(punks_token,30000)

    punks_token.claim(account,{'from':account})
    punks_token.approve(vault,1,{'from':account})

    vault.open_position(punks_token,1,{'from':account})
    vault.borrow(1,15000,{'from':account})
    vault.payment(1,5000,{'from':account})

    print('-------------------------------------------')

    prefix = ''

    if os.environ.get('NETWORK') == 'kovan':
        prefix = 'https://kovan.etherscan.io/address/'
    if os.environ.get('NETWORK') == 'ropsten':
        prefix = 'https://ropsten.etherscan.io/address/'
    else:
        prefix = 'https://etherscan.io/address/'

    print("Governance:", prefix + gov_token)
    print("Stablecoin:", prefix + stable_token)
    print("FakePunks:", prefix + punks_token)
    print("Vault:", prefix + vault)
    print("Wallet:", prefix + account.address)

    return True

