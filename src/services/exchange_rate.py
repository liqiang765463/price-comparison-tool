import requests
from datetime import datetime
from typing import Dict
import json
from pathlib import Path
import os

class ExchangeRateService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = 'https://v6.exchangerate-api.com/v6'
        self.cache_file = Path('cache/exchange_rates.json')
        self._rates_cache = {}
        self._last_update = None
        self._load_cache()

    def _load_cache(self):
        """从缓存文件加载汇率数据"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    self._rates_cache = data['rates']
                    self._last_update = datetime.fromisoformat(data['last_update'])
            except Exception as e:
                print(f"加载汇率缓存失败: {str(e)}")

    def _save_cache(self):
        """保存汇率数据到缓存文件"""
        try:
            self.cache_file.parent.mkdir(exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump({
                    'rates': self._rates_cache,
                    'last_update': self._last_update.isoformat()
                }, f)
        except Exception as e:
            print(f"保存汇率缓存失败: {str(e)}")

    def get_rate(self, from_currency: str, to_currency: str = 'CNY') -> float:
        """获取汇率"""
        # 检查缓存是否需要更新（每24小时更新一次）
        now = datetime.utcnow()
        if not self._last_update or (now - self._last_update).days >= 1:
            self._update_rates()

        if from_currency == to_currency:
            return 1.0

        # 转换为人民币的汇率
        if to_currency == 'CNY':
            return 1 / self._rates_cache.get(from_currency, 1.0)

        # 其他货币之间的转换
        from_rate = self._rates_cache.get(from_currency, 1.0)
        to_rate = self._rates_cache.get(to_currency, 1.0)
        return to_rate / from_rate

    def _update_rates(self):
        """更新汇率缓存"""
        try:
            response = requests.get(f'{self.base_url}/{self.api_key}/latest/CNY')
            data = response.json()
            
            if data['result'] == 'success':
                self._rates_cache = data['conversion_rates']
                self._last_update = datetime.utcnow()
                self._save_cache()
            else:
                raise Exception(f"API返回错误: {data.get('error-type')}")
        except Exception as e:
            print(f"更新汇率失败: {str(e)}")
            # 如果更新失败，继续使用旧的汇率

    def convert_price(self, amount: float, from_currency: str, to_currency: str = 'CNY') -> Dict:
        """转换价格"""
        rate = self.get_rate(from_currency, to_currency)
        converted_amount = amount * rate
        
        return {
            'original_amount': amount,
            'original_currency': from_currency,
            'converted_amount': round(converted_amount, 2),
            'converted_currency': to_currency,
            'rate': rate,
            'timestamp': datetime.utcnow().isoformat()
        }