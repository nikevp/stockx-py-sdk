import datetime
import json
import requests
from stockxsdk.item import StockxItem
from stockxsdk.order import StockxOrder
from stockxsdk.product import StockxProduct

def now_plus_thirty():
    return (datetime.datetime.now() + datetime.timedelta(30)).strftime('%Y-%m-%d')

def now():
    return datetime.datetime.now().strftime('%Y-%m-%d')

class Stockx():
    API_BASE = 'https://stockx.com/api'

    def __init__(self):
        self.customer_id = None
        self.headers = None

    def __api_query(self, request_type, command, data=None):
        endpoint = self.API_BASE + command
        response = None
        if request_type == 'GET':
            response = requests.get(endpoint, params=data, headers=self.headers)
        elif request_type == 'POST':
            response = requests.post(endpoint, json=data, headers=self.headers)
        elif request_type == 'DELETE':
            response = requests.delete(endpoint, json=data, headers=self.headers)
        return response.json()

    def __get(self, command, data=None):
        return self.__api_query('GET', command, data)

    def __post(self, command, data=None):
        return self.__api_query('POST', command, data)

    def __delete(self, command, data=None):
        return self.__api_query('DELETE', command, data)

    def authenticate(self, email, password):
        endpoint = self.API_BASE + '/login'
        payload = {
            'email': email,
            'password': password
        }
        response = requests.post(endpoint, json=payload)
        customer = response.json().get('Customer', None)
        if customer is None:
            raise ValueError('Authentication failed, check username/password')
        self.customer_id = response.json()['Customer']['id']
        self.headers = {
            'JWT-Authorization': response.headers['jwt-authorization']
        }
        return True

    def me(self):
        command = '/users/me'
        return self.__get(command)

    def selling(self):
        command = '/customers/{0}/selling'.format(self.customer_id)
        response = self.__get(command)
        return [StockxItem(item_json) for item_json in response['PortfolioItems']]

    def buying(self):
        command = '/customers/{0}/buying'.format(self.customer_id)
        response = self.__get(command)
        return [StockxItem(item_json) for item_json in response['PortfolioItems']]

    def rewards(self):
        command = '/users/me/rewards'
        return self.__get(command)

    def stats(self):
        command = '/customers/{0}/collection/stats'.format(self.customer_id)
        return self.__get(command)

    def cop_list(self):
        command = '/customers/{0}/cop-list'.format(self.customer_id)
        response = self.__get(command)
        return [StockxItem(item_json) for item_json in response['PortfolioItems']]

    def add_product_to_follow(self, product_id):
        command = '/portfolio?a=1001'
        payload = {
            'timezone': 'America/Chicago',
            'PortfolioItem': {
                'amount': 0,
                'matchedWithDate': '',
                'condition': '2000',
                'skuUuid': product_id,
                'action': 1001
            }
        }
        response = self.__post(command, payload)
        success = response['PortfolioItem']['text'] == 'Following'
        return success

    def add_product_to_portfolio(self, product_id, purchase_price, condition='new', purchase_date=None):
        purchase_price = purchase_price or now()
        conditions = {
            'new': 2000,
            '9.5': 950,
            '9': 900,
            '8.5': 850,
            '8': 800,
            '7': 700,
            '6': 600,
            '5': 500,
            '4': 400,
            '3': 300,
            '2': 200,
            '1': 100
        }
        condition = conditions.get(condition, None)
        command = '/portfolio?a=1000'
        payload = {
            'timezone': 'America/Chicago',
            'PortfolioItem': {
                'amount': purchase_price,
                'matchedWithDate': '{0}T06:00:00+0000'.format(purchase_date),
                'condition': condition,
                'skuUuid': product_id,
                'action': '1000'
            }
        }
        response = self.__post(command, payload)
        success = response['PortfolioItem']['text'] == 'In Portfolio'
        return success
        
    def get_product(self, product_id):
        command = '/products/{0}'.format(product_id)
        product_json = self.__get(command)
        return StockxProduct(product_json)

    def __get_activity(self, product_id, activity_type):
        command = '/products/{0}/activity?state={1}'.format(product_id, activity_type)
        return self.__get(command)

    def get_asks(self, product_id):
        return [StockxOrder('bid', order) for order in self.__get_activity(product_id, 400)]

    def get_lowest_ask(self, product_id):
        return self.get_asks(product_id)[0]
    
    def get_bids(self, product_id):
        return [StockxOrder('bid', order) for order in self.__get_activity(product_id, 300)]

    def get_highest_bid(self, product_id):
        return self.get_bids(product_id)[0]

    def create_ask(self, product_id, price, expiry_date=None):
        expiry_date = expiry_date or now_plus_thirty()
        command = '/portfolio?a=ask'
        payload = {
            'PortfolioItem': {
                'amount': price,
                'expiresAt': '{0}T06:00:00+0000'.format(expiry_date),
                'skuUuid': product_id
            }
        }
        response = self.__post(command, payload)
        if response.get('error', None):
            raise ValueError(json.loads(response['message'])['description'])
        return response['PortfolioItem']['chainId']

    def update_ask(self, ask_id, new_price, expiry_date=None):
        expiry_date = expiry_date or now_plus_thirty()
        command = '/portfolio?a=ask'
        payload = {
            'PortfolioItem': {
                'amount': new_price,
                'expiresAt': '{0}T06:00:00+0000'.format(expiry_date),
                'chainId': ask_id
            }
        }
        response = self.__post(command, payload)
        success = response['PortfolioItem']['statusMessage'] == 'Ask Listed'
        return success

    def cancel_ask(self, ask_id):
        command = '/portfolio/{0}'.format(ask_id)
        payload = {
            'chain_id': ask_id,
            'notes': 'User Canceled Ask'
        }
        response = self.__delete(command, payload)
        success = response['PortfolioItem']['notes'] == 'User Canceled Ask'
        return success

    def create_bid(self, product_id, price, expiry_date=None):
        expiry_date = expiry_date or now_plus_thirty()
        command = '/portfolio?a=bid'
        payload = {
            'PortfolioItem': {
                'amount': price,
                'expiresAt': '{0}T06:00:00+0000'.format(expiry_date),
                'skuUuid': product_id,
                'meta': {
                    'sizePreferences': ''
                }
            }
        }
        response = self.__post(command, payload)
        if response.get('error', None):
            raise ValueError(json.loads(response['message']['description']))
        return response['PortfolioItem']['chainId']

    def update_bid(self, bid_id, new_price, expiry_date=None):
        expiry_date = expiry_date or now_plus_thirty()
        command = '/portfolio?a=bid'
        payload = {
            'PortfolioItem': {
                'amount': new_price,
                'expiresAt': '{0}T06:00:00+0000'.format(expiry_date),
                'chainId': bid_id,
                'meta': {
                    'sizePreferences': ''
                }
            }
        }
        response = self.__post(command, payload)
        success = response['PortfolioItem']['statusMessage'] == 'Bid Placed'
        return success

    def cancel_bid(self, bid_id):
        command = '/portfolio/{0}'.format(bid_id)
        payload = {
            'chain_id': bid_id,
            'notes': 'User Canceled Bid'
        }
        response = self.__delete(command, payload)
        success = response['PortfolioItem']['notes'] == 'User Canceled Bid'
        return success

    def search(self, query):
        endpoint = 'https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query'
        params = {
            'x-algolia-agent': 'Algolia for vanilla JavaScript 3.22.1',
            'x-algolia-application-id': 'XW7SBCT9V6',
            'x-algolia-api-key': '6bfb5abee4dcd8cea8f0ca1ca085c2b3'
        }
        payload = {
            'params': 'query={0}&hitsPerPage=20&facets=*'.format(query)
        }
        return requests.post(endpoint, json=payload, params=params).json()['hits']

    def get_first_product_id(self, query):
        return self.search(query)[0]['objectID']
