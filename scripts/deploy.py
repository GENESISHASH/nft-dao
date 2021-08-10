#!/usr/bin/python3

from brownie import GovernanceToken, PunksToken, StableToken, Vault, accounts

def main():

    account = accounts.load('dev')
    publish_source = False

    gov_token = GovernanceToken.deploy("Governance", "GOV", 1000000, {'from':account}, publish_source=publish_source)
    stable_token = StableToken.deploy("PUSD Stablecoin", "PUSD", {'from':account}, publish_source=publish_source)
    punks_token = PunksToken.deploy("FakePunks", "FPUNK", 100, {'from':account}, publish_source=publish_source)
    vault = Vault.deploy("Vault", stable_token, {"from":account}, publish_source=publish_source)

    stable_token.addMinter(vault,{'from':account})
    vault.set_token_value(punks_token,9999)

    punks_token.claim(account,{'from':account})
    punks_token.approve(vault,1,{'from':account})

    print("Governance:", gov_token)
    print("Stablecoin:", stable_token)
    print("FakePunks:", punks_token)
    print("Vault:", vault)

    return True

