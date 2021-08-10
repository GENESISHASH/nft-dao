#!/usr/bin/python3

from brownie import GovernanceToken, PunksToken, StableToken, Vault, accounts

def main():

    account = accounts.load('devel')
    publish_source = False

    gov_token = GovernanceToken.deploy("Governance", "GOV", 1000000, {'from':account}, publish_source=publish_source)
    stable_token = StableToken.deploy("PUSD Stablecoin", "PUSD", {'from':account}, publish_source=publish_source)
    punks_token = PunksToken.deploy("FakePunks", "FPUNK", 100, {'from':account}, publish_source=publish_source)
    vault = Vault.deploy("Vault", stable_token, {"from":account}, publish_source=publish_source)

    stable_token.add_minter(vault,{'from':account})
    vault.set_token_value(punks_token,10000)

    punks_token.claim(account,{'from':account})
    punks_token.approve(vault,1,{'from':account})

    vault.open_position(punks_token,1,{'from':account})
    vault.borrow(1,5000,{'from':account})
    vault.payment(1,500,{'from':account})

    print(vault.positions(account,1))

    print("Governance:", gov_token)
    print("Stablecoin:", stable_token)
    print("FakePunks:", punks_token)
    print("Vault:", vault)

    return True

