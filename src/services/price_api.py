import requests
from typing import Dict, List
from datetime import datetime

class PriceAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.priceapi.com/v2"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def search_products(self, keyword: str, sources: List[str] = None) -> List[Dict]:
        """
        搜索商品价格
        sources: ["amazon", "google_shopping", "ebay"]
        """
        if sources is None:
            sources = ["amazon", "ebay"]

        try:
            response = requests.post(
                f"{self.base_url}/search",
                headers=self.headers,
                json={
                    "query": keyword,
                    "sources": sources,
                    "country": "CN",
                    "limit": 20
                }
            )
            return response.json()["results"]
        except Exception as e:
            print(f"搜索商品失败: {str(e)}")
            return []

    def get_price_history(self, product_url: str, days: int = 30) -> List[Dict]:
        """获取商品历史价格"""
        try:
            response = requests.post(
                f"{self.base_url}/history",
                headers=self.headers,
                json={
                    "url": product_url,
                    "days": days
                }
            )
            return response.json()["history"]
        except Exception as e:
            print(f"获取价格历史失败: {str(e)}")
            return []

    def track_competitor(self, product_url: str, competitor_urls: List[str]) -> Dict:
        """追踪竞争对手价格"""
        try:
            response = requests.post(
                f"{self.base_url}/track",
                headers=self.headers,
                json={
                    "target_url": product_url,
                    "competitor_urls": competitor_urls,
                    "notification_url": "https://your-webhook-url.com/price-alert"
                }
            )
            return response.json()
        except Exception as e:
            print(f"设置竞争对手追踪失败: {str(e)}")
            return {}

    def get_market_insights(self, category: str, platform: str = "amazon") -> Dict:
        """获取市场洞察"""
        try:
            response = requests.get(
                f"{self.base_url}/insights",
                headers=self.headers,
                params={
                    "category": category,
                    "platform": platform,
                    "country": "CN"
                }
            )
            return response.json()
        except Exception as e:
            print(f"获取市场洞察失败: {str(e)}")
            return {}