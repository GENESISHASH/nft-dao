#!/usr/bin/python3

import os
import json
import time
import logging

from dotenv import load_dotenv
load_dotenv()

from brownie import *

NETWORK = os.environ.get('NETWORK')
if !NETWORK:
  NETWORK = os.environ.get('default_network')

if NETWORK == 'mainnet':
  account = accounts.load('devel')
  publish_source = True
elif NETWORK == 'kovan':
  account = accounts.load('devel','oijoij')
  publish_source = True
elif NETWORK == 'localhost':
  account = accounts.load('devel','oijoij')
  publish_source = False
else:
  account = accounts.load('devel','oijoij')
  publish_source = False

print "Deploying on network", NETWORK

# example punks
PUNK_INDEX_FLOOR = 2
PUNK_INDEX_APE = 372
PUNK_INDEX_ALIEN = 635

def print_json(x): return print(json.dumps(x,sort_keys=False,indent=2))

def main():
  print('Deploying on network',NETWORK)

  # deploy price oracle
  _price_oracle = price_oracle.deploy(os.environ.get('contract_name_price_oracle'),{'from':account},publish_source=publish_source)

  # set chainlink address in oracle
  if NETWORK == 'kovan':
    _price_oracle.set_chainlink_contract("0x9326BFA02ADD2366b30bacB125260Af641031331")
  if NETWORK == 'mainnet':
    _price_oracle.set_chainlink_contract("0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419")

  # deploy dao
  _dao = dao.deploy(os.environ.get('contract_name_dao'),{'from':account},publish_source=publish_source)

  # deploy cryptopunks contract
  _cryptopunks = cryptopunks.deploy({'from':account},publish_source=publish_source)

  # deploy stablecoin
  _stable_token = stable_token.deploy(os.environ.get('contract_name_stable_token'),"PUSD",{'from':account},publish_source=publish_source)

  # deploy vault
  _vault = vault_cryptopunks.deploy(os.environ.get('contract_name_vault_cryptopunks'),_stable_token,_cryptopunks,_dao,_price_oracle,{"from":account},publish_source=publish_source)

  _vault.set_compounding_interval_secs(1,{'from':account})

  # add the vault and dao as a minter for the stablecoin
  _stable_token.addMinter(_vault,{'from':account})
  _stable_token.addMinter(_dao,{'from':account})

  # @todo: revoke ownership or remove minter from stabletoken
  # ..

  # @temp: mint 2m for the dao
  _stable_token.mint(_dao,(2000000 * 10**18),{'from':account})

  print("DAO stablecoin balance:",_stable_token.balanceOf(_dao))

  # claim some punks
  _cryptopunks.getPunk(PUNK_INDEX_FLOOR,{'from':account})
  _cryptopunks.getPunk(PUNK_INDEX_APE,{'from':account})

  print("Cryptobunks balance:",_cryptopunks.balanceOf(account))

  # print preview position
  print('Position preview:')
  print_json(_vault.preview_position(PUNK_INDEX_APE,{'from':account}).dict())

  # open a new position with my floorpunk
  _vault.open_position(PUNK_INDEX_APE,{'from':account})

  # ..ui waits for deposit before borrow() is able to be called
  # ui can actually call _vault.get_punk_owner() until it's the vault address

  # deposit the punk into the vault (user does this via web3)
  _cryptopunks.transferPunk(_vault,PUNK_INDEX_APE,{'from':account})

  _vault.tick()

  # print position
  print('Position before borrow:')
  print_json(_vault.show_position(PUNK_INDEX_APE).dict())

  borrow_amount = 1000000
  repay_amount = 250000

  # borrow some stablecoin against it now that we have it in vault
  print('Borrowing USD',borrow_amount)
  _vault.borrow(PUNK_INDEX_APE,(borrow_amount * 10**18),{'from':account})

  _vault.tick()

  # print position
  print('Position after borrow:')
  print_json(_vault.show_position(PUNK_INDEX_APE).dict())

  # add some interest to this thing
  _vault.tick()

  # make a payment against my position
  print('Making repayment for',repay_amount)
  _vault.repay(PUNK_INDEX_APE,(repay_amount * 10**18),{'from':account})

  # print position
  print('Position after repayment:')
  print_json(_vault.show_position(PUNK_INDEX_APE).dict())

  # liquidate position
  # print('Liquidating the position:')
  # _vault.liquidate(PUNK_INDEX_APE,{'from':account})

  # print vault status
  print('Vault status:')
  print_json(_vault.show_status().dict())

  # @todo: currently working on this
  # print(_vault.show_all_positions(account))

  # @todo: attempt to close position
  # print('Attempting to close the position..')
  # _vault.close_position(PUNK_INDEX_FLOOR,{'from':account})

  #####################################

  # output details
  prefix = ''

  if NETWORK == 'mainnet':
    prefix = 'https://etherscan.io/address/'
  if NETWORK == 'kovan':
    prefix = 'https://kovan.etherscan.io/address/'
  if NETWORK == 'ropsten':
    prefix = 'https://ropsten.etherscan.io/address/'

  print('\n=================================================\n')

  print("wallet", prefix + str(account))
  print("_dao", prefix + str(_dao))
  print("_vault", prefix + str(_vault))
  print("_stable_token", prefix + str(_stable_token))
  print("_cryptopunks", prefix + str(_cryptopunks))
  print("_price_oracle", prefix + str(_price_oracle))

  print("\n\n")

  return True

