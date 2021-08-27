# pusd
a nifty collection of well thought out smart contracts

# @todo
[x] - add minimum time interval to interest adding logic
[x] - implement chainlink pricefeed oracle
[x] - add vault burn functionality for principal payments
[x] - add setters and owner to manually set apr and collateralization rate
[x] - fix usd calculations
[ ] - add position cleanup inside tick() for positions opened and no punk deposit made
[ ] - implement liquidation logic
  - only flag positions for liquidation initially
  - add function to set automatic liquidations in the future without gov wallet approvals
  - initially gov wallet needs to approve liquidations of any position
    - admin web3 interface allows for execution liquidations manually
      - interface will show any position flagged for liquidation, age and healthscore
      - allow option to run liquidate() on it in a single click
  - total vault debt on liquidation is recalculated upon each successful liquidation
    - burn outstanding pusd value of position (-vault.total_debt)
    - minus updated punk type value as defined by chainlink (-vault.total_debt)
    - punk transferred to dao (any interest payments have already been transferred to dao at this point)
[ ] - add ability for dao to open position within the vault using a stablecoin
[ ] - vault needs to have initial debt limit in pusd
  - function to change this value by gov wallet
  - if debt limit exceeded a new position's pusd value, opening that new position will fail temporarily

## @questions
- what happens if the user has transferred their PUSD into another coin
  - we can't burn what they have left, we're fine just taking the colatteral in that case?
  - liquidation should function like this:
    - colatteral goes to the dao
    - any pusd they control should be burned

# notes
```
Compiler Version: v0.4.26+commit.4563c3fc
Optimization Enabled: 1
Runs: 200
`sicall``

