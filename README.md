# stockx-py-sdk

Stockx Python3 API Wrapper

## Notes

This is an *unofficial* StockX SDK for Python3. This project is currently *not* unit tested and is likely full of bugs. It not recommended to use this SDK in production applications unless you really know what you're doing. Pull requests, issues, and requests for features are welcome. SDK documentation will come as features are finished.

This SDK does *not* (currently) support accounts registered with Facebook or Twitter.

## Prerequisites

You'll need to create an account on [StockX](https://stockx.com). Please make sure to register with an email+password (*not* Facebook or Twitter) at the moment.

## Basic Usage

```python
from stockxsdk import Stockx

stockx = Stockx()

email = 'YOUR_EMAIL'
password = 'YOUR_PASSWORD'
stockx.authenticate(email, password)

product_id = stockx.get_first_product_id('BB1234')

highest_bid = stockx.get_highest_bid(product_id)
print(highest_bid.shoe_size, highest_bid.order_price)

lowest_ask = stockx.get_lowest_ask(product_id)
print(lowest_ask.shoe_size, lowest_ask.order_price)
```

## SDK Documentation

### `stockx.authenticate`

    stockx.authenticate(email, password)

Authenticates the SDK to make requests on your behalf. You must authenticate the SDK to retrieve info about your account or place new asks/bids.

#### Parameters
1. `string` - Email for the account
2. `string` - Password for the account

#### Returns
`bool` Success of the login operation

#### Example
```python
email = 'example@test.com'
password = 'example123'
logged_in = stockx.authenticate(email, password)
print(logged_in) # `True`, hopefully
```

### `stockx.me`

    stock.me()

Returns information about your account.

#### Parameters
none

#### Returns
`Object` - Account info as a JSON object

#### Example
```python
me = stock.me()
print(me) # some huge JSON object
```

### `stockx.selling`

    stockx.selling()

Returns information about what you're currently selling (asks, pending, sold).

#### Parameters
none

#### Returns
`list<StockxItem>` - A list of StockxItem objects

#### Example
```python
selling = stockx.selling()
for item in selling:
    print(item.item_type, item.item_id, item.item_price)
```

#### `stockx.buying()`
Returns information about what you're currently buying (bids, pending, bought).

#### Parameters
none

#### Returns
`list<StockxItem>` - A list of StockxItem objects

#### Example
```python
buying = stockx.buying()
for item in buying:
    print(item.item_type, item.item_id, item.item_price)
```

#### `stockx.rewards()`
Returns information about your seller level

#### `stockx.stats()`
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