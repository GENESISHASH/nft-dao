#!/usr/bin/python3

from brownie import DAO, PunksToken, StableToken, Vault, accounts

def main():

  """
  # setup dao
  print('Deploying DAO')
  dao = DAO.deploy("DAO",{'from':accounts[0]})
  """

  # setup stablecoin and vault
  stablecoin = StableToken.deploy("Stablecoin", "USDS", {'from':accounts[0]})
  vault = Vault.deploy("Vault", stablecoin, {"from":accounts[0]})

  # add vault as stablecoin minter
  stablecoin.addMinter(vault, {'from':accounts[0]})

  # deploy and claim a punk token
  punk_token = PunksToken.deploy("PunkToken", "PUNK", 10, {'from':accounts[0]})
  punk_token.claim(accounts[5],{"from":accounts[5]})

  print("Claimed a punk under account 5, punk balance:", punk_token.balanceOf(accounts[5]))

  # set a value for punk tokens
  vault.set_token_value(punk_token, 5000, {'from':accounts[0]})

  # deposit punk into vault, opening a position
  print('Depositing punk into vault from accounts[5]')

  punk_token.approve(vault,1,{"from":accounts[5]})
  position_id = vault.deposit(punk_token,1,{'from':accounts[5]})

  print("Position ID", position_id)

  # check vault balance
  print('Punk balance of vault is now:', punk_token.balanceOf(vault))

  return False

  # borrow stablecoin against position
  vault.borrow(position_id, 100)

  # check stablecoin balance
  print('Stablecoin balance of accounts[5] is now:', stablecoin.balanceOf(accounts[5]))

  return True

