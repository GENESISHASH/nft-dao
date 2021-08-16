#!/usr/bin/python3

import os
from brownie import (
    accounts,
    price_oracle,
)

def main():
  publish_source = False
  account = accounts.load('devel')

  mainnet = "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"
  kovan = "0x9326BFA02ADD2366b30bacB125260Af641031331"

  # deploy oracle
  _oracle = price_oracle.deploy('Oracle',{'from':account},publish_source=publish_source)
  #_oracle.set_chainlink_contract(kovan)
  #_oracle.update()

  print('eth_usd',_oracle.eth_usd())
  print('eth_usd',_oracle.eth_usd_18())
  print('last_update_time',_oracle.last_update_time())
  print('last_update_remote',_oracle.last_update_remote())

  #####################################

  # output details
  prefix = 'https://etherscan.io/address/'
  if os.environ.get('NETWORK') == 'kovan':
    prefix = 'https://kovan.etherscan.io/address/'
  if os.environ.get('NETWORK') ==  'ropsten':
    prefix = 'https://ropsten.etherscan.io/address/'

  print("\n\n")

  print("wallet", prefix + str(account))
  print("_oracle", prefix + str(_oracle))

  print("\n\n")

  return True

