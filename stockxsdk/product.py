class StockxProduct(object):
    def __init__(self, product_json):
        product = product_json['Product']
        self.product_id = product['id']
        self.title = product['title']
        self.retail_price = product['retailPrice']
        self.style_id = product['styleId']
        self.brand = product['brand']
        self.image = product['media']['imageUrl']
        children = [product['children'][child] for child in product['children']]
        self.sizes = {child['shoeSize']: child['id'] for child in children}
