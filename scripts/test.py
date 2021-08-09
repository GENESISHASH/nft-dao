#!/usr/bin/python3

from brownie import PunkToken, USDToken, Vault, accounts

def main():

    # setup stablecoin and vault
    usd_token = USDToken.deploy("USDToken", "USDNFT", {'from':accounts[0]})
    vault = Vault.deploy("Vault", "VAULT", usd_token, {"from":accounts[0]})

    # add vault as stablecoin minter
    usd_token.addMinter(vault, {'from':accounts[0]})

    # deploy punk token
    punk_token = PunkToken.deploy("PunkToken", "PUNK", 10, {'from':accounts[0]})

    # set vault value of punks to 100
    vault.setTokenValue(punk_token, 100, {'from':accounts[0]})

    # claim a punk in account[5]
    punk_token.claim(accounts[5],{"from":accounts[5]})

    print("Claimed a punk under account 5, punk balance:", punk_token.balanceOf(accounts[5]))

    # deposit punk in account[1] to vault
    print('Depositing punk into vault from accounts[5]')

    punk_token.approve(vault,1,{"from":accounts[5]})
    vault.deposit(punk_token,1,{'from':accounts[5]})

    # check vault balance
    print('Punk balance of vault is now:', punk_token.balanceOf(vault))

    # check stablecoin balance
    print('USD balance of accounts[5] is now:', usd_token.balanceOf(accounts[5]))

    return True

