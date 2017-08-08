class StockxItem(object):
    def __init__(self, item_json):
        self.item_type = item_json['text']
        self.item_price = item_json['amount']
        self.item_id = item_json['chainId']
