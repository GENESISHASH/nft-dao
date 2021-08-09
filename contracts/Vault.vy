# @version ^0.2.0

"""
@title Vault
"""

from vyper.interfaces import ERC20

name: public(String[64])
symbol: public(String[32])
owner: public(address)

balances: HashMap[address, uint256]

@external
def __init__(_name: String[64], _symbol: String[32]):
    self.name = _name
    self.symbol = _symbol
    self.owner = msg.sender

@external
def receive(_token_addr: address, _amount: uint256) -> bool:
    ERC20(_token_addr).approve(self,_amount)
    ERC20(_token_addr).transferFrom(msg.sender,self,_amount)
    self.balances[_token_addr] += _amount
    return True

@view
@external
def balanceOf(_token_addr: address) -> uint256:
    return self.balances[_token_addr]

