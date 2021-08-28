# nftdao

## @todo: contracts
- [x] add minimum time interval to interest adding logic
- [x] implement chainlink pricefeed oracle
- [x] implement chainlink keeper to call `contract.tick()`
- [x] add vault burn functionality for principal repayments
- [x] add setters and owner to manually set apr and collateralization rate
- [x] fix usd calculations
- [x] vault should be able to disable lending completely at will
- [x] vault should be able to disable interest accumulation on existing positions at will
- [ ] implement position cleanup inside `contract.tick()` for positions opened and no punk deposit made within 12hrs
- [ ] (wip) fully implement liquidation logic
  - [x] `contract.tick()` marks positions positions for liquidationsbased on health score  by setting `position.flagged = true`
  - [ ] `contract.liquidate()` should allow for admins to call manually
  - [ ] total vault debt on liquidation is recalculated upon each successful liquidation
    - punk collateral must be transferred to dao
    - position must be closed and marked as liquidated
- [ ] add exception for dao to open position within the vault using a stablecoin

## @todo: frontend
- [ ] create prototype
- [ ] prelim design work completed for app.\* subdomain 
- [ ] design work completed for ico 1-pager

