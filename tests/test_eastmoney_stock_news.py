#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试 EastMoneyNewsProvider 个股新闻接口。

每次运行同时输出日志到 test_eastmoney_stock_news.log。
"""

import logging
import os
import sys
from pathlib import Path

# 添加项目根目录到 sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# ── 日志：同时输出到控制台 + 同名 .log 文件 ──────────────────────────
LOG_FILE = Path(__file__).with_suffix(".log")
logger = logging.getLogger("eastmoney_stock_news_test")
logger.setLevel(logging.DEBUG)

_fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%H:%M:%S")

# 文件 handler
fh = logging.FileHandler(str(LOG_FILE), mode="w", encoding="utf-8")
fh.setLevel(logging.DEBUG)
fh.setFormatter(_fmt)
logger.addHandler(fh)

# 控制台 handler
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
ch.setFormatter(_fmt)
logger.addHandler(ch)

logger.info("日志文件: %s", LOG_FILE.resolve())

# ── 测试主体 ─────────────────────────────────────────────────────────

TEST_STOCKS = [
    ("600519", "贵州茅台"),
    ("000858", "五粮液"),
    ("300750", "宁德时代"),
    ("688017", "绿的谐波"),
]

def test_eastmoney_stock_news():
    """测试个股新闻抓取。"""
    from src.search_service import EastMoneyNewsProvider

    provider = EastMoneyNewsProvider()
    assert provider.name == "EastMoney", f"name={provider.name}"
    assert provider.is_available, "provider unavailable"
    logger.info("✓ EastMoneyNewsProvider 初始化成功")

    for code, name in TEST_STOCKS:
        logger.info("=" * 60)
        logger.info("测试 %s (%s)", name, code)
        try:
            news = provider._eastmoney_stock_news(code, page_size=10)
            logger.info("  返回 %d 条新闻", len(news))
            for i, item in enumerate(news[:10]):
                logger.info("  [%d] %s | %s | %s",
                            i + 1,
                            item.get("time", "")[:16],
                            item.get("source", ""),
                            item.get("title", "")[:60])
            if not news:
                logger.warning("  ⚠ 无新闻（可能该时段无更新或IP被风控）")
        except Exception as e:
            logger.error("  ✗ 失败: %s", e)

    logger.info("=" * 60)
    logger.info("✅ 个股新闻测试完成")


def test_provider_search():
    """测试通过 BaseSearchProvider.search() 接口调用。"""
    from src.search_service import EastMoneyNewsProvider

    provider = EastMoneyNewsProvider()
    logger.info("--- search() 接口测试 ---")

    for code, name in TEST_STOCKS[:2]:
        response = provider.search(query=code, max_results=5, days=3)
        logger.info("%s: success=%s, results=%d, provider=%s, time=%.2fs",
                    code, response.success, len(response.results),
                    response.provider, response.search_time)
        for r in response.results[:3]:
            logger.info("  %s | %s", r.published_date or "?", r.title[:60])


if __name__ == "__main__":
    test_eastmoney_stock_news()
    test_provider_search()
