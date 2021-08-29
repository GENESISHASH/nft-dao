#!/usr/bin/python3

import os
import json
import time
import logging

from datetime import date

from dotenv import load_dotenv
load_dotenv()

from brownie import *

# ascii art
print(open('./.ascii.art','r').read())

# select deployment network
NETWORK = os.environ.get('NETWORK')

if not NETWORK:
  NETWORK = os.environ.get('default_network')

if NETWORK == 'mainnet':
  account = accounts.load('devel')
  publish_source = True
elif NETWORK == 'kovan':
  account = accounts.load('devel','oijoij')
  publish_source = False
elif NETWORK == 'localhost':
  account = accounts.load('devel','oijoij')
  publish_source = False
else:
  raise Exception("Unknown network")

# example punks
PUNK_INDEX_FLOOR = 2
PUNK_INDEX_APE = 372
PUNK_INDEX_ALIEN = 635

def print_json(x): return print(json.dumps(x,sort_keys=False,indent=2))

def main():
  print('Deploying on network:',NETWORK)

  _price_oracle = price_oracle.deploy(os.environ.get('contract_name_price_oracle'),{'from':account},publish_source=publish_source)

  if NETWORK == 'kovan':
    _price_oracle.set_chainlink_contract("0x9326BFA02ADD2366b30bacB125260Af641031331")
  elif NETWORK == 'mainnet':
    _price_oracle.set_chainlink_contract("0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419")

  _dao = dao.deploy(os.environ.get('contract_name_dao'),{'from':account},publish_source=publish_source)
  _cryptopunks = cryptopunks.deploy({'from':account},publish_source=publish_source)
  _stable_token = stable_token.deploy(os.environ.get('contract_name_stable_token'),"PUSD",{'from':account},publish_source=publish_source)
  _vault = vault_cryptopunks.deploy(os.environ.get('contract_name_vault_cryptopunks'),_stable_token,_cryptopunks,_dao,_price_oracle,{"from":account},publish_source=publish_source)
  _ico_token = ico_token.deploy(os.environ.get('contract_name_ico_token'),os.environ.get('ico_token_symbol'),int(os.environ.get('ico_token_supply')),{"from":account},publish_source=publish_source)

  _vault.set_compounding_interval_secs(1,{'from':account})

  _stable_token.addMinter(_vault,{'from':account})
  _stable_token.addMinter(_dao,{'from':account})
  _stable_token.mint(_dao,(2000000 * 10**18),{'from':account})

  _cryptopunks.getPunk(PUNK_INDEX_FLOOR,{'from':account})
  _cryptopunks.getPunk(PUNK_INDEX_APE,{'from':account})

  print('Preview for position for punk',PUNK_INDEX_APE)
  print_json(_vault.preview_position(PUNK_INDEX_APE,{'from':account}).dict())

  _vault.open_position(PUNK_INDEX_APE,{'from':account})

  # (ui waits for user to deposit punk into vault, here we do it manual)
  _cryptopunks.transferPunk(_vault,PUNK_INDEX_APE,{'from':account})

  _vault.tick()

  print('Position after deposit of punk',PUNK_INDEX_APE)
  print_json(_vault.show_position(PUNK_INDEX_APE).dict())

  borrow_amount = 1000000
  repay_amount = 250000

  # borrow money against the position
  print('Borrowing PUSD',borrow_amount)
  _vault.borrow(PUNK_INDEX_APE,(borrow_amount * 10**18),{'from':account})

  _vault.tick()

  # print position
  print('Position after borrow')
  print_json(_vault.show_position(PUNK_INDEX_APE).dict())

  # add some interest to this thing
  _vault.tick()

  # make a payment against my position
  print('Repay PUSD',repay_amount)
  _vault.repay(PUNK_INDEX_APE,(repay_amount * 10**18),{'from':account})

  # print position
  print('Position after repayment')
  print_json(_vault.show_position(PUNK_INDEX_APE).dict())

  # liquidate position
  # print('Liquidating the position:')
  # _vault.liquidate(PUNK_INDEX_APE,{'from':account})

  # print vault status
  print('Vault status')
  print_json(_vault.show_status().dict())

  # @todo: currently working on this
  # print(_vault.show_all_positions(account))

  # @todo: attempt to close position
  # print('Attempting to close the position..')
  # _vault.close_position(PUNK_INDEX_FLOOR,{'from':account})

  #####################################

  # output details
  prefix = ':\n  '

  if NETWORK == 'mainnet':
    prefix += 'https://etherscan.io/address/'
  if NETWORK == 'kovan':
    prefix += 'https://kovan.etherscan.io/address/'
  if NETWORK == 'ropsten':
    prefix += 'https://ropsten.etherscan.io/address/'

  print('\n=================================================\n')

  bulk = ''
  bulk += (NETWORK + ' deploy ' + str(date.today()))
  bulk += "\n```"
  bulk += ("\nwallet" + prefix + str(account))
  bulk += ("\nvault" + prefix + str(_vault))
  bulk += ("\ndao" + prefix + str(_dao))
  bulk += ("\nstable_token" + prefix + str(_stable_token))
  bulk += ("\ncryptopunks" + prefix + str(_cryptopunks))
  bulk += ("\nprice_oracle" + prefix + str(_price_oracle))
  bulk += ("\nico_token" + prefix + str(_ico_token))
  bulk += "\n```"

  print('\n' + bulk + '\n')

  print('Finished')
  return True

