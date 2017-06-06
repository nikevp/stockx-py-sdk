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


#### stockx.authenticate(email, password)
Authenticates the SDK to make requests on your behalf. You must authenticate the SDK to retrieve info about your account or place new asks/bids.

#### `stockx.me()`
Returns information about your acount.

#### `stockx.get_selling()`
Returns information about what you're currently selling.

#### `stockx.get_buying()`
Returns information about what you're currently buying

#### `stockx.get_rewards()`
Returns information about your seller level

#### `stockx.get_stats()`
Returns buying and selling statistics about your account

#### `stockx.get_cop_list()`
Returns your current cop list

#### `stockx.add_product_to_follow(product_id)`
Adds a new product to your cop list

#### `stockx.add_product_to_portfolio(product_id, purchase_price, purchase_date, condition)`
Adds a new product to your portfolio. `purchase_date` is a standard `YYYY-MM-DD` string. `condition` is one of: `new`, `9.5`, `9`, `8.5`, `8`, `7`, `6`, `5`, `4`, `3`, `2`, `1`.

#### `stockx.get_product(product_id)`
Returns the full StockX product object given a StockX objectID

#### `stockx.get_all_sorts()`
Returns all possible sorting functions

#### `stockx.get_all_filters()`
Returns all possible filters

#### `stockx.get_new_releases()`
Returns a list of the latest releases

#### `stockx.get_related_products(product_id)`
Returns a list of products related to a given product

#### `stockx.get_asks(product_id)`
Returns all asks for a given product

#### `stockx.get_lowest_ask(product_id)`
Returns the lowest ask for a given product

#### `stockx.get_bids(product_id)`
Returns all bids for a given product

#### `stockx.get_highest_bid(product_id)`
Returns the highest bid for a given product

#### `stockx.create_ask(price, expiry_date, product_id)`
Creates a new ask for a product at a given price to expire at a given date. Expiry date is a standard `YYYY-MM-DD` string.

#### `stockx.update_ask(price, expiry_date, ask_id)`
Updates an ask for a product at a given price to expire at a given date. Expiry date is a standard `YYYY-MM-DD` string. `ask_id` is the `chainId` for that ask returned by `stockx.get_selling()`.

#### `stockx.cancel_ask(price, ask_id)`
Cancels an ask for a product. `ask_id` is the `chainId` for that ask returned by `stockx.get_selling()`.

#### `stockx.create_bid(price, expiry_date, product_id)`
Creates a new bid for a product at a given price to expire at a given date. Expiry date is a standard `YYYY-MM-DD` string.

#### `stockx.update_bid(price, expiry_date, bid_id)`
Updates an bid for a product at a given price to expire at a given date. Expiry date is a standard `YYYY-MM-DD` string. `bid_id` is the `chainId` for that bid returned by `stockx.get_buying()`.

#### `stockx.cancel_bid(price, bid_id)`
Cancels an bid for a product. `bid_id` is the `chainId` for that bid returned by `stockx.get_buying()`.

#### `stockx.search(query)`
Searches StockX for a given query. Returns the first 20 results.

#### `stockx.get_first_product(query)`
Returns the first product for a given query.