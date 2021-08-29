# nftdao

## @todo: contracts
- [x] add minimum time interval to interest adding logic
- [x] optimize `tick()` to be less gas-intensive
- [x] implement chainlink pricefeed oracle including eth feed and floor prices for punks
- [x] implement chainlink keeper to call `contract.tick()`
- [x] add vault burn functionality for principal repayments
- [x] add setters and owner to manually set apr and collateralization rate
- [x] fix usd calculations
- [x] vault should be able to disable lending completely at will
- [x] vault should be able to disable interest accumulation on existing positions at will
- [x] refine deployment scripts, incorporate dotenv file configuration
- [x] fix positions structure within the vault so they are iteratable publicly
- [ ] implement position cleanup inside `tick()` for positions opened without punk deposit made within 12hrs
- [ ] (wip) fully implement liquidation logic
  - [x] `contract.tick()` marks positions positions for liquidationsbased on health score  by setting `position.flagged = true`
  - [x] `contract.liquidate()` should allow for admins to call manually
  - [ ] liquidation tweaks and adjustments
    - punk collateral must be transferred to dao instead of vault on liquidate
    - position must be closed and marked as liquidated
- [ ] add exception for dao to open position within the vault using a stablecoin
- [ ] create ico contract

## @todo: frontend
- [ ] create react prototype app.erc247.com (tld domain tbd)
- [ ] integrate web3 to allow for position previews based on punks in connected wallet
  - [ ] allow opening of a position
- [ ] design work completed for ico 1-pager (outsource)
  - [ ] converted responsive html assets (outsource: htmlburger)

## @todo: misc
- [x] create bytecode slicing utility to make contract verification easier

