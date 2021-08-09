# @version ^0.2.0

"""
@title Vault
"""

from vyper.interfaces import ERC20

name: public(String[64])
symbol: public(String[32])
owner: public(address)

stablecoin: public(address)

balances: HashMap[address, uint256]
balances_accounts: HashMap[address, HashMap[address, uint256]]

@external
def __init__(_name:String[64], _symbol:String[32], _stablecoin_addr:address):
    self.name = _name
    self.symbol = _symbol
    self.stablecoin = _stablecoin_addr
    self.owner = msg.sender

@external
def receive(_token_addr: address, _amount: uint256) -> bool:
    assert ERC20(_token_addr).transferFrom(msg.sender,self,_amount)

    self.balances[_token_addr] += _amount
    self.balances_accounts[msg.sender][_token_addr] += _amount

    return True

@view
@external
def balanceOf(_token_addr: address) -> uint256:
    return self.balances[_token_addr]

