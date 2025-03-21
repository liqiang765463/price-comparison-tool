import time
import hmac
import hashlib
import base64
import urllib.parse
from typing import Dict, List
import requests
from datetime import datetime
import xml.etree.ElementTree as ET

class AmazonAPI:
    def __init__(self, access_key: str, secret_key: str, associate_tag: str, region: str = 'com'):
        self.access_key = access_key
        self.secret_key = secret_key
        self.associate_tag = associate_tag
        self.region = region
        self.endpoint = f'webservices.amazon.{region}'
        self.uri = '/onca/xml'

    def _generate_signature(self, params: Dict) -> str:
        """生成Amazon API签名"""
        # 按字典序排序参数
        ordered_params = sorted(params.items())
        # 构造规范化请求字符串
        canonical_querystring = '&'.join(['%s=%s' % (k, urllib.parse.quote(str(v))) for k, v in ordered_params])
        
        # 构造用于签名的字符串
        string_to_sign = f'GET\n{self.endpoint}\n{self.uri}\n{canonical_querystring}'
        
        # 计算HMAC签名
        h = hmac.new(self.secret_key.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha256)
        signature = base64.b64encode(h.digest()).decode('utf-8')
        
        return signature

    def search_products(self, keyword: str, search_index: str = 'All') -> List[Dict]:
        """搜索商品"""
        params = {
            'Service': 'AWSECommerceService',
            'Operation': 'ItemSearch',
            'AWSAccessKeyId': self.access_key,
            'AssociateTag': self.associate_tag,
            'SearchIndex': search_index,
            'Keywords': keyword,
            'Timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'Version': '2013-08-01'
        }
        
        # 添加签名
        params['Signature'] = self._generate_signature(params)
        
        try:
            url = f'https://{self.endpoint}{self.uri}?{urllib.parse.urlencode(params)}'
            response = requests.get(url)
            
            # 解析XML响应
            root = ET.fromstring(response.content)
            
            items = []
            for item in root.findall('.//Item'):
                item_data = {
                    'asin': item.find('ASIN').text,
                    'title': item.find('ItemAttributes/Title').text,
                    'price': item.find('OfferSummary/LowestNewPrice/Amount').text,
                    'currency': item.find('OfferSummary/LowestNewPrice/CurrencyCode').text,
                }
                if item.find('LargeImage/URL') is not None:
                    item_data['image'] = item.find('LargeImage/URL').text
                items.append(item_data)
            
            return items
        except Exception as e:
            print(f"Amazon API调用失败: {str(e)}")
            return []

    def get_product_details(self, asin: str) -> Dict:
        """获取商品详情"""
        params = {
            'Service': 'AWSECommerceService',
            'Operation': 'ItemLookup',
            'AWSAccessKeyId': self.access_key,
            'AssociateTag': self.associate_tag,
            'ItemId': asin,
            'ResponseGroup': 'Large',
            'Timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'Version': '2013-08-01'
        }
        
        params['Signature'] = self._generate_signature(params)
        
        try:
            url = f'https://{self.endpoint}{self.uri}?{urllib.parse.urlencode(params)}'
            response = requests.get(url)
            
            root = ET.fromstring(response.content)
            item = root.find('.//Item')
            
            if item is None:
                return {}
                
            return {
                'asin': item.find('ASIN').text,
                'title': item.find('ItemAttributes/Title').text,
                'brand': item.find('ItemAttributes/Brand').text if item.find('ItemAttributes/Brand') is not None else '',
                'price': item.find('OfferSummary/LowestNewPrice/Amount').text,
                'currency': item.find('OfferSummary/LowestNewPrice/CurrencyCode').text,
                'image': item.find('LargeImage/URL').text if item.find('LargeImage/URL') is not None else '',
                'description': item.find('EditorialReviews/EditorialReview/Content').text if item.find('EditorialReviews/EditorialReview/Content') is not None else '',
            }
        except Exception as e:
            print(f"获取商品详情失败: {str(e)}")
            return {}