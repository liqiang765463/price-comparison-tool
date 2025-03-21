import hashlib
import time
import requests
from typing import Dict, List
import json

class TaobaoAPI:
    def __init__(self, app_key: str, app_secret: str):
        self.app_key = app_key
        self.app_secret = app_secret
        self.gateway_url = "https://eco.taobao.com/router/rest"

    def _generate_sign(self, params: Dict) -> str:
        """生成淘宝API签名"""
        # 按字典序排序参数
        ordered_params = sorted(params.items())
        # 拼接参数
        param_str = self.app_secret
        for k, v in ordered_params:
            param_str += k + str(v)
        param_str += self.app_secret
        # MD5加密
        return hashlib.md5(param_str.encode('utf-8')).hexdigest().upper()

    def search_products(self, keyword: str, page_size: int = 20) -> List[Dict]:
        """搜索商品"""
        params = {
            'method': 'taobao.tbk.item.get',
            'app_key': self.app_key,
            'timestamp': str(int(time.time())),
            'format': 'json',
            'v': '2.0',
            'sign_method': 'md5',
            'q': keyword,
            'page_size': page_size,
        }
        
        # 生成签名
        params['sign'] = self._generate_sign(params)
        
        try:
            response = requests.get(self.gateway_url, params=params)
            data = response.json()
            if 'error_response' in data:
                raise Exception(data['error_response']['msg'])
            return data['tbk_item_get_response']['results']['n_tbk_item']
        except Exception as e:
            print(f"淘宝API调用失败: {str(e)}")
            return []

    def get_product_details(self, num_iid: str) -> Dict:
        """获取商品详情"""
        params = {
            'method': 'taobao.tbk.item.info.get',
            'app_key': self.app_key,
            'timestamp': str(int(time.time())),
            'format': 'json',
            'v': '2.0',
            'sign_method': 'md5',
            'num_iids': num_iid,
        }
        
        params['sign'] = self._generate_sign(params)
        
        try:
            response = requests.get(self.gateway_url, params=params)
            data = response.json()
            if 'error_response' in data:
                raise Exception(data['error_response']['msg'])
            return data['tbk_item_info_get_response']['results']['n_tbk_item'][0]
        except Exception as e:
            print(f"获取商品详情失败: {str(e)}")
            return {}