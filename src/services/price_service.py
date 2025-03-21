from typing import Dict, List
from .fair_api import FairAPI
from .price_api import PriceAPI
from .taobao_api import TaobaoAPI

class PriceService:
    def __init__(self, config: Dict):
        """
        初始化价格服务
        config: {
            'fair_api_key': 'your_fair_api_key',
            'price_api_key': 'your_price_api_key',
            'taobao': {
                'app_key': 'your_app_key',
                'app_secret': 'your_app_secret'
            }
        }
        """
        self.fair_api = FairAPI(config.get('fair_api_key'))
        self.price_api = PriceAPI(config.get('price_api_key'))
        self.taobao_api = TaobaoAPI(
            config.get('taobao', {}).get('app_key'),
            config.get('taobao', {}).get('app_secret')
        )

    async def search_product_all_platforms(self, keyword: str) -> Dict:
        """在所有平台搜索商品"""
        results = {
            'domestic': [],  # 国内平台
            'international': [],  # 国际平台
            'price_comparison': []  # 价格对比
        }

        # 获取淘宝数据
        taobao_results = await self.taobao_api.search_products(keyword)
        if taobao_results:
            results['domestic'].extend(taobao_results)

        # 获取国际平台数据
        fair_results = self.fair_api.search_products(keyword)
        if fair_results:
            results['international'].extend(fair_results)

        # 获取价格对比数据
        price_results = self.price_api.search_products(keyword)
        if price_results:
            results['price_comparison'].extend(price_results)

        return results

    async def get_product_details(self, product_id: str, platform: str) -> Dict:
        """获取商品详细信息"""
        if platform == 'taobao':
            return await self.taobao_api.get_product_details(product_id)
        elif platform == 'amazon':
            return self.fair_api.get_product_details(product_id)
        else:
            return {}

    def track_price(self, product_urls: List[str]) -> Dict:
        """设置价格追踪"""
        # 使用PriceAPI进行价格追踪
        tracking_results = {}
        for url in product_urls:
            result = self.price_api.track_competitor(url, [])
            if result:
                tracking_results[url] = result
        return tracking_results

    def get_price_analysis(self, product_id: str, platform: str) -> Dict:
        """获取价格分析报告"""
        analysis = {
            'historical_prices': [],
            'market_insights': {},
            'price_comparison': []
        }

        # 获取历史价格
        if platform == 'taobao':
            product_url = f"https://item.taobao.com/item.htm?id={product_id}"
            analysis['historical_prices'] = self.price_api.get_price_history(product_url)

        # 获取市场洞察
        analysis['market_insights'] = self.price_api.get_market_insights(platform)

        return analysis