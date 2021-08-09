#!/usr/bin/python3

from brownie import GovernanceToken, PunkToken, USDToken, Vault, accounts

def main():

    account = accounts.load('taky')

    gov_token = GovernanceToken.deploy("Governance", "GOV", 1000000, {'from':account},publish_source=False)
    usd_token = USDToken.deploy("USDG Stablecoin", "USDG", {'from':account},publish_source=False)
    vault = Vault.deploy("Vault", "VAULT", usd_token, {"from":account},publish_source=False)
    punk_token = PunkToken.deploy("FakePunks", "FPUNK", 10000, {'from':account},publish_source=False)

    print("Governance:", gov_token)
    print("Stablecoin:", usd_token)
    print("Vault:", vault)
    print("FakePunks:", punk_token)

    return True

