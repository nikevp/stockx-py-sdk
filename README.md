# stockx-py-sdk

This is an unofficial StockX Python3 SDK. This is currently not unit tested and likely full of bugs. Do not use this SDK in production applications. Pull requests are welcome. Issues and requests for new features are welcome. SDK documentation will come as features are finished. 

This SDK currently does not support accounts registered with Facebook or Twitter. StockX does not provide an official API, so tokens are retrieved by making a request to the `/login/` endpoint.

Typical usage is 
```python
from stockxsdk import Stockx
stockx = Stockx()
stockx.authenticate('YOURUSERNAME', 'YOURPASSWORD')
product_id = stockx.get_first_product('BB1234')['objectID']
highest_bid = stockx.get_highest_bid(product_id)
print(highest_bid)
lowest_ask = stockx.get_lowest_ask(product_id)
print(lowest_ask)
```

## TODO

- Classes to abstract the StockX return values
- Handling dates so they're usable