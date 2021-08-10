# @version ^0.2.8

# Governance token

from vyper.interfaces import ERC20

implements: ERC20

event Approval:
    owner: indexed(address)
    spender: indexed(address)
    value: uint256

event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    value: uint256

name: public(String[64])
symbol: public(String[32])
decimals: public(uint256)
totalSupply: public(uint256)
balances: HashMap[address, uint256]
allowances: HashMap[address, HashMap[address, uint256]]

@external
def __init__(_name:String[64],_symbol:String[32],_supply:uint256):
    self.decimals = 4
    init_supply: uint256 = _supply * 10 ** self.decimals

    self.name = _name
    self.symbol = _symbol
    self.totalSupply = init_supply
    self.balances[self] = self.totalSupply
    log Transfer(ZERO_ADDRESS,self,self.totalSupply)

@view
@external
def balanceOf(_owner:address) -> uint256:
    return self.balances[_owner]

@view
@external
def allowance(_owner:address, _spender:address) -> uint256:
    return self.allowances[_owner][_spender]

@external
def approve(_spender:address, _value:uint256) -> bool:
    self.allowances[msg.sender][_spender] = _value
    log Approval(msg.sender, _spender, _value)
    return True

@internal
def _transfer(_from:address, _to:address, _value:uint256):
    assert self.balances[_from] >= _value, "Insufficient balance"
    self.balances[_from] -= _value
    self.balances[_to] += _value
    log Transfer(_from, _to, _value)

@external
def transfer(_to:address, _value:uint256) -> bool:
    self._transfer(msg.sender, _to, _value)
    return True

@external
def transferFrom(_from:address, _to:address, _value:uint256) -> bool:
    assert self.allowances[_from][msg.sender] >= _value, "Insufficient allowance"
    self.allowances[_from][msg.sender] -= _value
    self._transfer(_from, _to, _value)
    return True

