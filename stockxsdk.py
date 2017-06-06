import requests
import datetime

class Stockx():
    API_BASE = 'https://stockx.com/api'

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
        self.customer_id = response.json()['Customer']['id']
        self.headers = {
            'JWT-Authorization': response.headers['jwt-authorization']
        }

    def me(self):
        command = '/users/me'
        return self.__get(command)

    def get_selling(self):
        command = '/users/me/selling'
        return self.__get(command)

    def get_buying(self):
        command = '/users/me/buying'
        return self.__get(command)
        
    def get_rewards(self):
        command = '/users/me/rewards'
        return self.__get(command)

    def get_stats(self):
        command = '/customers/{0}/stats'.format(self.customer_id)
        
    def get_cop_list(self):
        command = '/customers/{0}/cop-list'.format(self.customer_id)
        return self.__get(command)

    def add_product_to_follow(self, product_id):
        command = '/portfolio?a=1001'
        payload = {
            "timezone": "America/Chicago",
            "PortfolioItem": {
                "amount": 0,
                "matchedWithDate": "",
                "condition": "2000",
                "skuUuid": product_id,
                "action": 1001
            }
        }
        return self.__post(command, payload)

    def add_product_to_portfolio(self, product_id, purchase_price, condition):
        command = '/portfolio?a=1000'
        payload = {
            "timezone": "America/Chicago",
            "PortfolioItem": {
                "amount": purchase_price,
                "matchedWithDate": "2015-03-01T06:00:00+0000",
                "condition": condition, # 2000 (NEW), 950, 900, 850, 800, 700, 600 ... 100
                "skuUuid": product_id,
                "action": "1000"
            }
        }
        return self.__post(command, payload)
        
    def get_product(self, product_id):
        command = '/products/{0}'.format(product_id)
        return self.__get(command)

    def get_all_sorts(self):
        command = '/products/sorts?all=true'
        return self.__get(command)

    def get_all_filters(self):
        command = '/products/filters?all=true'
        return self.__get(command)

    def __browse(self, params):
        command = '/browse/'
        return self.__get(command, params)

    def get_new_releases(self):
        params = {
            'page': 1,
            'limit': 1000,
            'category': 152,
            'focus': 'new_releases',
            'release_date': datetime.datetime.now().strftime('%y-%m-%d')
        }
        return self.__browse(params)

    def get_related_products(self, product_id):
        command = '/products/{0}/related'.format(product_id)
        return self.__get(command)

    def get_activity(self, product_id, activity_type):
        command = '/products/{0}/activity?state={1}'.format(product_id, activity_type)
        return self.__get(command)

    def get_asks(self, product_id):
        return self.get_activity(product_id, 400)

    def get_lowest_ask(self, product_id):
        return self.get_asks(product_id)[0]
    
    def get_bids(self, product_id):
        return self.get_activity(product_id, 300)

    def get_highest_bid(self, product_id):
        return self.get_bids(product_id)[0]

    def create_ask(self, price, expires_at, product_id):
        command = '/portfolio?a=ask'
        payload = {
            "PortfolioItem": {
                "amount": price,
                "expiresAt": "2017-07-06T18:23:59+0000",
                "skuUuid": product_id
            }
        }
        return self.__post(command, payload)

    def update_ask(self, price, expires_at, ask_id):
        command = '/portfolio?a=ask'
        payload = {
            "PortfolioItem": {
                "amount": price,
                "expiresAt": "2017-07-06T18:26:41+0000",
                "chainId": ask_id
            }
        }
        return self.__post(command, payload)

    def cancel_ask(self, ask_id):
        command = '/portfolio/{0}'.format(ask_id)
        payload = {
            "chain_id": ask_id,
            "notes": "User Canceled Ask"
        }
        return self.__delete(command, payload)

    def create_bid(self, price, expires_at, product_id):
        command = '/portfolio?a=bid'
        payload = {
            "PortfolioItem": {
                "amount": price,
                "expiresAt": "2017-07-06T18:28:36+0000",
                "skuUuid": product_id,
                "meta": {
                    "sizePreferences": ""
                }
            }
        }
        return self.__post(command, payload)

    def update_bid(self, price, expires_at, bid_id):
        command = '/portfolio?a=bid'
        payload = {
            "PortfolioItem": {
                "amount": price,
                "expiresAt": "2017-07-06T18:29:07+0000",
                "chainId": bid_id,
                "meta": {
                    "sizePreferences": ""
                }
            }
        }
        return self.__post(command, payload)

    def cancel_bid(self, bid_id):
        command = '/portfolio/{0}'.format(bid_id)
        payload = {
            "chain_id": bid_id,
            "notes": "User Canceled Bid"
        }
        return self.__delete(command, payload)
    
    def search(self, query):
        endpoint = 'https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query'
        params = {
            'x-algolia-agent': 'Algolia for vanilla JavaScript 3.22.1',
            'x-algolia-application-id': 'XW7SBCT9V6',
            'x-algolia-api-key': '6bfb5abee4dcd8cea8f0ca1ca085c2b3'
        }
        payload = {
            "params": 'query={0}&hitsPerPage=20&facets=*'.format(query)
        }
        return requests.post(endpoint, json=payload, params=params).json()['hits']

    def get_first_product(self, query):
        return self.search(query)[0]
