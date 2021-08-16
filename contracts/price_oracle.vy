# @version ^0.2.15

# price_oracle.vy

from vyper.interfaces import ERC20

name: public(String[64])
owner: public(address)

chainlink_contract: public(address)

eth_usd: public(int128)
last_update_time: public(uint256)
last_update_remote: public(bool)

interface ChainLink:
  def latestAnswer() -> int128: view

@external
def __init__(_name:String[64]):
  self.name = _name
  self.owner = msg.sender

  self.eth_usd = (3100 * 10**8)
  self.last_update_time = block.timestamp
  self.last_update_remote = False

@internal
def _update() -> bool:
  if self.chainlink_contract == ZERO_ADDRESS:
    self.eth_usd = (3100 * 10**8)
    self.last_update_time = block.timestamp
    self.last_update_remote = False
    return True

  self.eth_usd = ChainLink(self.chainlink_contract).latestAnswer()
  self.last_update_time = block.timestamp
  self.last_update_remote = True
  return True

@external
def update() -> bool:
  return self._update()

@external
def set_chainlink_contract(_addr:address) -> bool:
  assert msg.sender == self.owner, 'unauthorized'
  self.chainlink_contract = _addr
  self._update()
  return True

