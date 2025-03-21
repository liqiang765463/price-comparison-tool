# 跨境电商价格比较工具

实时监控和比较国内外电商平台的商品价格差异。

## 主要功能

- 支持多平台数据采集（淘宝、天猫、京东、Amazon、eBay等）
- 商品智能匹配（基于图像识别和文本相似度）
- 实时价格比较和历史价格追踪
- 价差提醒功能
- 数据可视化展示

## 安装说明

1. 克隆仓库
```bash
git clone https://github.com/liqiang765463/price-comparison-tool.git
cd price-comparison-tool
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的API密钥
```

4. 运行应用
```bash
uvicorn main:app --reload
```

## 使用说明

1. 访问 http://localhost:8000/docs 查看API文档
2. 使用Web界面（http://localhost:8000）进行价格比较

## API文档

详细的API文档请参考 [API文档](docs/API.md)

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License