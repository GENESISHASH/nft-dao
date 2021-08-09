#!/usr/bin/python3

from brownie import GovernanceToken, PunkToken, USDToken, Vault, accounts

def main():

    # deploy contracts
    gov_token = GovernanceToken.deploy("GovernanceToken", "GOV", 10, 500000, {'from':accounts[0]})
    punk_token = PunkToken.deploy("PunkToken", "PUNK", 10, {'from':accounts[0]})
    usd_token = USDToken.deploy("USDToken", "USDNFT", {'from':accounts[0]})
    vault = Vault.deploy("Vault","VAULT",{"from":accounts[4]})

    # claim all punk tokens
    claim_punks(punk_token)

    # create some usd tokens
    mint_usd(usd_token)

    # deposit punk into the vault
    print('Getting allowance')
    punk_token.approve(vault,1,{"from":accounts[1]})
    vault.receive(punk_token,1,{"from":accounts[1]})

    # confirm balances
    print("Punk balance of account 1 after deposit:", punk_token.balanceOf(accounts[1]))
    print("Punk balance of vault", vault.balanceOf(punk_token))

    return True

def claim_punks(punk_token):
    print("Claiming Punk tokens")

    punk_token.claim(accounts[1],{"from":accounts[1]})
    punk_token.claim(accounts[1],{"from":accounts[1]})
    punk_token.claim(accounts[1],{"from":accounts[1]})
    punk_token.claim(accounts[1],{"from":accounts[1]})
    punk_token.claim(accounts[2],{"from":accounts[2]})
    punk_token.claim(accounts[2],{"from":accounts[2]})
    punk_token.claim(accounts[2],{"from":accounts[2]})
    punk_token.claim(accounts[3],{"from":accounts[3]})
    punk_token.claim(accounts[3],{"from":accounts[3]})
    punk_token.claim(accounts[3],{"from":accounts[3]})

    print("Punk balance of account 0:", punk_token.balanceOf(accounts[0]))
    print("Punk balance of account 1:", punk_token.balanceOf(accounts[1]))
    print("Punk balance of account 2:", punk_token.balanceOf(accounts[2]))
    print("Punk balance of account 3:", punk_token.balanceOf(accounts[3]))

    return True

def mint_usd(usd_token):
    print("Minting USD coins")
    usd_token.mint(accounts[0],10000,{'from':accounts[0]})

    total_supply = usd_token.totalSupply({'from':accounts[1]})
    print("Total USD supply", total_supply)

    return True

