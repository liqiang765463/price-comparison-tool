import requests
from typing import Dict, List
import json

class FairAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.fairapi.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def search_products(self, keyword: str, platforms: List[str] = None) -> List[Dict]:
        """
        跨平台搜索商品
        platforms: ["amazon", "ebay", "walmart", "shopify", "tiktok"]
        """
        if platforms is None:
            platforms = ["amazon", "ebay"]

        params = {
            "keyword": keyword,
            "platforms": platforms,
            "limit": 20
        }

        try:
            response = requests.get(
                f"{self.base_url}/products/search",
                headers=self.headers,
                params=params
            )
            return response.json()["data"]
        except Exception as e:
            print(f"搜索商品失败: {str(e)}")
            return []

    def get_product_details(self, product_id: str, platform: str) -> Dict:
        """获取商品详情"""
        try:
            response = requests.get(
                f"{self.base_url}/products/{platform}/{product_id}",
                headers=self.headers
            )
            return response.json()["data"]
        except Exception as e:
            print(f"获取商品详情失败: {str(e)}")
            return {}

    def track_price(self, product_id: str, platform: str) -> Dict:
        """追踪商品价格"""
        try:
            response = requests.post(
                f"{self.base_url}/tracking",
                headers=self.headers,
                json={
                    "product_id": product_id,
                    "platform": platform
                }
            )
            return response.json()
        except Exception as e:
            print(f"设置价格追踪失败: {str(e)}")
            return {}