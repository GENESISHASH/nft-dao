#!/usr/bin/python3

import os
from brownie import GovernanceToken, PunksToken, StableToken, Vault, accounts

def main():
  publish_source = False
  account = accounts.load('devel')

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

  return True

