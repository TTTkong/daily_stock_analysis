#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试 EastMoneyNewsProvider 全球资讯接口。

每次运行同时输出日志到 test_eastmoney_global_news.log。
"""

import logging
import os
import sys
from pathlib import Path

# 添加项目根目录到 sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# ── 日志：同时输出到控制台 + 同名 .log 文件 ──────────────────────────
LOG_FILE = Path(__file__).with_suffix(".log")
logger = logging.getLogger("eastmoney_global_news_test")
logger.setLevel(logging.DEBUG)

_fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%H:%M:%S")

fh = logging.FileHandler(str(LOG_FILE), mode="w", encoding="utf-8")
fh.setLevel(logging.DEBUG)
fh.setFormatter(_fmt)
logger.addHandler(fh)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
ch.setFormatter(_fmt)
logger.addHandler(ch)

logger.info("日志文件: %s", LOG_FILE.resolve())

# ── 测试主体 ─────────────────────────────────────────────────────────

def test_eastmoney_global_news():
    """测试全球资讯抓取。"""
    from src.search_service import EastMoneyNewsProvider

    provider = EastMoneyNewsProvider()
    logger.info("✓ EastMoneyNewsProvider 初始化成功")

    logger.info("=" * 60)
    logger.info("测试东财 7×24 全球资讯")

    try:
        news = provider._eastmoney_global_news(page_size=50)
        logger.info("  返回 %d 条快讯", len(news))

        # 统计来源（这里都是东方财富）
        for i, item in enumerate(news[:10]):
            logger.info("  [%02d] %s | %s",
                        i + 1,
                        item.get("time", "")[:16],
                        item.get("title", "")[:80])

        if not news:
            logger.warning("  ⚠ 无快讯（可能网络问题或API变更）")
    except Exception as e:
        logger.error("  ✗ 失败: %s", e)

    logger.info("✅ 全球资讯测试完成")


def test_search_service_integration():
    """测试 SearchService 集成：大盘复盘场景使用全球资讯。"""
    from src.search_service import SearchService

    svc = SearchService(eastmoney_news_enabled=True)
    # 大盘复盘调用：传市场关键词而非股票代码
    response = svc.search_stock_news("market", "A股市场", max_results=10)
    logger.info("--- SearchService 大盘新闻 ---")
    logger.info("success=%s, results=%d, provider=%s, time=%.2fs",
                response.success, len(response.results),
                response.provider, response.search_time)
    for r in response.results[:5]:
        logger.info("  %s | %s", r.published_date or "?", r.title[:60])


if __name__ == "__main__":
    test_eastmoney_global_news()
    test_search_service_integration()
