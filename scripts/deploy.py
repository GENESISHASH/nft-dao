#!/usr/bin/python3

import os
from brownie import (
    accounts,
    cryptopunks,
    ico_token,
    erc20_token,
    stable_token,
    vault_erc20,
    vault_cryptopunks,
    dao
)

# example punks
PUNK_INDEX_FLOOR = 2
PUNK_INDEX_APE = 635
PUNK_INDEX_ALIEN = 372

def main():
  publish_source = False
  account = accounts.load('devel')

  print("Account:",str(account))
  print('-------------------------------------------')

  # deploy cryptopunks contract and claim punks
  _cryptopunks = cryptopunks.deploy({'from':account},publish_source=publish_source)
  _cryptopunks.getPunk(PUNK_INDEX_FLOOR,{'from':account})
  _cryptopunks.getPunk(PUNK_INDEX_APE,{'from':account})
  _cryptopunks.getPunk(PUNK_INDEX_ALIEN,{'from':account})

  print("Cryptobunks balance:",_cryptopunks.balanceOf(account))

  # deploy stablecoin and vault
  _stable_token = stable_token.deploy("PUSD Stablecoin","PUSD",0,{'from':account},publish_source=publish_source)
  _vault = vault_cryptopunks.deploy("Vault",_stable_token,_cryptopunks,{"from":account},publish_source=publish_source)

  # add the vault as a minter for the stablecoin
  _stable_token.add_minter(_vault,{'from':account})

  # set punk prices
  #_vault.set_punk_value('floor',100000,{'from':account})
  #_vault.set_punk_value('ape',5000000,{'from':account})
  #_vault.set_punk_value('alien',10000000,{'from':account})

  # get loan terms for my ape
  print('Loan terms:',_vault.preview_position(PUNK_INDEX_APE,{'from':account}).return_value)

  # open a new position with my ape
  _vault.open_position(PUNK_INDEX_APE,{'from':account})

  # ..ui waits for deposit before borrow() is able to be called
  # ui can actually call _vault.get_punk_owner() until it's the vault address

  # deposit the punk into the vault
  _cryptopunks.transferPunk(_vault,PUNK_INDEX_APE,{'from':account})

  # borrow some stablecoin against it, this fails if we don't own the punk
  _vault.borrow(PUNK_INDEX_APE,100,{'from':account})

  # position summary
  print('My position:',_vault.show_position(PUNK_INDEX_APE,{'from':account}).return_value)

  """
  vault.open_position(punks_token,1,{'from':account})
  vault.borrow(1,15000,{'from':account})
  vault.payment(1,5000,{'from':account})

  print('-------------------------------------------')

  prefix = 'https://etherscan.io/address/'

  if os.environ.get('NETWORK') == 'kovan':
    prefix = 'https://kovan.etherscan.io/address/'
  if os.environ.get('NETWORK') ==  'ropsten':
    prefix = 'https://ropsten.etherscan.io/address/'

  print("Governance:", prefix + str(gov_token))
  print("Stablecoin:", prefix + str(stable_token))
  print("FakePunks:", prefix + str(punks_token))
  print("Vault:", prefix + str(vault))
  print("Wallet:", prefix + str(account))
  """

  return True

