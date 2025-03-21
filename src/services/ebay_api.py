import requests
from typing import Dict, List
from datetime import datetime

class EbayAPI:
    def __init__(self, app_id: str, cert_id: str, dev_id: str):
        self.app_id = app_id
        self.cert_id = cert_id
        self.dev_id = dev_id
        self.endpoint = 'https://api.ebay.com/shopping'
        self.finding_endpoint = 'https://svcs.ebay.com/services/search/FindingService/v1'

    def search_products(self, keyword: str, page_number: int = 1) -> List[Dict]:
        """搜索商品"""
        headers = {
            'X-EBAY-SOA-SECURITY-APPNAME': self.app_id,
            'X-EBAY-SOA-OPERATION-NAME': 'findItemsByKeywords',
            'X-EBAY-SOA-SERVICE-VERSION': '1.13.0',
            'X-EBAY-SOA-GLOBAL-ID': 'EBAY-US',
            'X-EBAY-SOA-REQUEST-DATA-FORMAT': 'JSON',
            'X-EBAY-SOA-RESPONSE-DATA-FORMAT': 'JSON'
        }

        params = {
            'keywords': keyword,
            'paginationInput.pageNumber': page_number,
            'paginationInput.entriesPerPage': 20,
            'OPERATION-NAME': 'findItemsByKeywords',
            'SERVICE-VERSION': '1.13.0',
            'SECURITY-APPNAME': self.app_id,
            'RESPONSE-DATA-FORMAT': 'JSON',
            'REST-PAYLOAD': True,
            'sortOrder': 'BestMatch'
        }

        try:
            response = requests.get(self.finding_endpoint, headers=headers, params=params)
            data = response.json()
            
            if 'findItemsByKeywordsResponse' not in data:
                return []
                
            items = data['findItemsByKeywordsResponse'][0]['searchResult'][0]['item']
            
            return [{
                'itemId': item['itemId'][0],
                'title': item['title'][0],
                'price': item['sellingStatus'][0]['currentPrice'][0]['__value__'],
                'currency': item['sellingStatus'][0]['currentPrice'][0]['@currencyId'],
                'image': item['galleryURL'][0] if 'galleryURL' in item else '',
                'url': item['viewItemURL'][0],
                'location': item['location'][0] if 'location' in item else '',
                'condition': item['condition'][0]['conditionDisplayName'][0] if 'condition' in item else ''
            } for item in items]
        except Exception as e:
            print(f"eBay搜索API调用失败: {str(e)}")
            return []

    def get_product_details(self, item_id: str) -> Dict:
        """获取商品详情"""
        headers = {
            'X-EBAY-API-APP-ID': self.app_id,
            'X-EBAY-API-CALL-NAME': 'GetSingleItem',
            'X-EBAY-API-VERSION': '967',
            'X-EBAY-API-REQUEST-ENCODING': 'XML',
            'X-EBAY-API-RESPONSE-ENCODING': 'XML',
            'X-EBAY-API-SITE-ID': '0'
        }

        params = {
            'ItemID': item_id,
            'IncludeSelector': 'Description,ItemSpecifics,Variations,Details'
        }

        try:
            response = requests.get(f'{self.endpoint}?callname=GetSingleItem', headers=headers, params=params)
            data = response.json()
            
            if 'Item' not in data:
                return {}
                
            item = data['Item']
            
            return {
                'itemId': item['ItemID'],
                'title': item['Title'],
                'price': item['CurrentPrice']['Value'],
                'currency': item['CurrentPrice']['CurrencyID'],
                'condition': item.get('ConditionDisplayName', ''),
                'description': item.get('Description', ''),
                'image': item.get('PictureURL', [None])[0],
                'location': item.get('Location', ''),
                'seller': {
                    'username': item['Seller']['UserID'],
                    'feedback_score': item['Seller']['FeedbackScore'],
                    'positive_feedback_percent': item['Seller']['PositiveFeedbackPercent']
                },
                'shipping': {
                    'cost': item.get('ShippingCostSummary', {}).get('ShippingServiceCost', {}).get('Value', 0),
                    'currency': item.get('ShippingCostSummary', {}).get('ShippingServiceCost', {}).get('CurrencyID', '')
                }
            }
        except Exception as e:
            print(f"获取eBay商品详情失败: {str(e)}")
            return {}