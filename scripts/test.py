#!/usr/bin/python3

from brownie import DAO, PunksToken, StableToken, Vault, accounts

def main():

  # setup stablecoin and vault
  stablecoin = StableToken.deploy("Stablecoin", "PUSDDEV", {'from':accounts[0]})
  vault = Vault.deploy("Vault", stablecoin, {"from":accounts[0]})

  # add vault as stablecoin minter
  stablecoin.add_minter(vault, {'from':accounts[0]})

  # deploy and claim a punk token
  punk_token = PunksToken.deploy("PunkToken", "PUNK", 10, {'from':accounts[0]})
  punk_token.claim(accounts[5],{"from":accounts[5]})

  # set a value for punk tokens
  print("Setting token value for punk")
  vault.set_token_value(punk_token,10000,{'from':accounts[0]})

  # deposit punk into vault, opening a position
  print('Borrowing 5000 Stablecoin for my 1 PUNK')
  punk_token.approve(vault,1,{"from":accounts[5]})
  vault.open_position(punk_token,1,{'from':accounts[5]})

  vault.borrow(1,1000,{'from':accounts[5]})

  # check stablecoin balance
  print('Stablecoin balance of accounts[5] is now:', stablecoin.balanceOf(accounts[5]))

  print('Paying back half the position')
  vault.payment(1,1000,{'from':accounts[5]})

  print('Stablecoin balance of accounts[5] is now:', stablecoin.balanceOf(accounts[5]))
  print('Stablecoin balance of vault is now:', stablecoin.balanceOf(vault))

  return True

