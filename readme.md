# nft-contracts
a nifty collection of well thought out smart contracts

# @todo
- deploy Punks clone on Ropsten for testing
- Vault.vy
  - add new hybrid hashmap called `positions`
    - ethereum addresses can each have multiple "positions" open
  - `deposit()`
    - create a position
    - change to create credit instead of minting
    - credit determined based on the asset being deposited into the vault
  - `borrow()`
    - borrow usd against a position's available credit
    - mint stablecoin based on available credit
  - `repay(int)`
    - burn an amount of minted stablecoin for a position
    - can be any amount, doesn't need to be full amount
  - `heartbeat()`
    - facilitates liquidations and reassessing position health
    - implement pricefeed oracle
    - implement interest accrual logic
    - calculate health score of all positions
- DAO.vy
  - contract accumulates interest and liquidated assets from defaulted positions

