# pusd
a nifty collection of well thought out smart contracts

# @todo
- vault_cryptopunks.vy
  - get `show_position()` to work (msg.sender should not be required)
  - get `preview_position()` to work (not sure why it doesn't return atm)
  - ensure position closings work properly
  - add interest logic send to dao
  - add liquidation logic send to dao
  - add position cleanup for positions opened and no punk deposit made
- stable_token.vy
  - keep track of totalSupply

