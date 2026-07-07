"""
TMT Morning Brief - Data Fetcher
从公开API获取行情、新闻和Deal数据
"""
import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import config

# 请求会话（复用连接池）
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
})


def fetch_eastmoney_stock(secid: str, fields: str = "f43,f44,f45,f46,f47,f48,f57,f58,f60,f170,f169") -> Dict:
    """
    东方财富行情API
    secid格式: market.code (1=上海, 0=深圳)
    """
    url = "https://push2.eastmoney.com/api/qt/stock/get"
    params = {
        "secid": secid,
        "fields": fields,
    }
    try:
        resp = session.get(url, params=params, timeout=15)
        data = resp.json()
        if data.get("data"):
            return data["data"]
        return {}
    except Exception as e:
        print(f"[EastMoney Error] secid={secid}: {e}")
        return {}


def fetch_yahoo_quote(symbol: str) -> Dict:
    """
    Yahoo Finance 行情获取
    """
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    params = {
        "interval": "1d",
        "range": "2d",
        "includeAdjustedClose": "true",
    }
    try:
        resp = session.get(url, params=params, timeout=15)
        data = resp.json()
        result = data.get("chart", {}).get("result", [{}])[0]
        meta = result.get("meta", {})
        timestamps = result.get("timestamp", [])
        closes = result.get("indicators", {}).get("quote", [{}])[0].get("close", [])
        
        if not closes or len(closes) < 1:
            return {}
        
        latest_close = closes[-1]
        prev_close = meta.get("previousClose", closes[-2] if len(closes) > 1 else closes[0])
        change = latest_close - prev_close
        change_pct = (change / prev_close * 100) if prev_close else 0
        
        return {
            "symbol": symbol,
            "price": round(latest_close, 2),
            "change": round(change, 2),
            "change_pct": round(change_pct, 2),
            "currency": meta.get("currency", ""),
        }
    except Exception as e:
        print(f"[Yahoo Error] symbol={symbol}: {e}")
        return {}


def fetch_newsapi(query: str, from_date: Optional[str] = None, page_size: int = 10) -> List[Dict]:
    """
    NewsAPI 新闻搜索
    免费版限制: 100 req/day
    """
    if not config.NEWSAPI_KEY:
        return []
    
    if from_date is None:
        from_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "from": from_date,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": page_size,
        "apiKey": config.NEWSAPI_KEY,
    }
    try:
        resp = session.get(url, params=params, timeout=15)
        data = resp.json()
        if data.get("status") == "ok":
            articles = data.get("articles", [])
            # 简化返回结构
            return [
                {
                    "title": a.get("title", ""),
                    "description": a.get("description", ""),
                    "url": a.get("url", ""),
                    "publishedAt": a.get("publishedAt", ""),
                    "source": a.get("source", {}).get("name", ""),
                }
                for a in articles
            ]
        return []
    except Exception as e:
        print(f"[NewsAPI Error] query={query}: {e}")
        return []


def get_market_dashboard() -> Dict[str, Any]:
    """
    获取大盘行情Dashboard数据
    """
    dashboard = {
        "equity": {},
        "commodities": {},
        "rates": {},
        "fx": {},
        "market_tone": "",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    
    # A股指数 - 东方财富
    a_indices = {k: v for k, v in config.MARKET_INDICES.items() if v.get("source") == "eastmoney"}
    for key, info in a_indices.items():
        data = fetch_eastmoney_stock(info["code"])
        if data:
            dashboard["equity"][key] = {
                "name": info["name"],
                "price": data.get("f43", 0) / 100 if data.get("f43") else 0,  # 价格需要除以100
                "change_pct": data.get("f170", 0) / 100 if data.get("f170") else 0,
            }
        time.sleep(config.REQUEST_DELAY)
    
    # 港股/美股指数 - Yahoo Finance
    y_indices = {k: v for k, v in config.MARKET_INDICES.items() if v.get("source") == "yahoo"}
    for key, info in y_indices.items():
        data = fetch_yahoo_quote(info["symbol"])
        if data:
            dashboard["equity"][key] = {
                "name": info["name"],
                "price": data["price"],
                "change_pct": data["change_pct"],
                "currency": data.get("currency", ""),
            }
        time.sleep(config.REQUEST_DELAY)
    
    # 商品
    for key, info in config.COMMODITIES_RATES.items():
        data = fetch_yahoo_quote(info["symbol"])
        if data:
            target = "commodities" if key in ["gold", "oil", "copper"] else "rates"
            dashboard[target][key] = {
                "name": info["name"],
                "price": data["price"],
                "change_pct": data["change_pct"],
            }
        time.sleep(config.REQUEST_DELAY)
    
    # 汇率
    for key, info in config.FX_RATES.items():
        data = fetch_yahoo_quote(info["symbol"])
        if data:
            dashboard["fx"][key] = {
                "name": info["name"],
                "price": data["price"],
                "change_pct": data["change_pct"],
            }
        time.sleep(config.REQUEST_DELAY)
    
    # 简单市场情绪判断
    hsi = dashboard["equity"].get("hsi", {})
    nasdaq = dashboard["equity"].get("nasdaq", {})
    hsi_chg = hsi.get("change_pct", 0) if isinstance(hsi, dict) else 0
    ndq_chg = nasdaq.get("change_pct", 0) if isinstance(nasdaq, dict) else 0
    
    if hsi_chg > 0.5 and ndq_chg > 0.5:
        dashboard["market_tone"] = "Risk-on | 港股美股同步上涨，市场情绪积极"
    elif hsi_chg < -0.5 and ndq_chg < -0.5:
        dashboard["market_tone"] = "Risk-off | 全球主要市场承压，避险情绪升温"
    elif hsi_chg > 0.5:
        dashboard["market_tone"] = "Cautiously Positive | 港股领涨，关注A股联动"
    elif nasdaq.get("change_pct", 0) < -1:
        dashboard["market_tone"] = "Tech Under Pressure | 美股科技板块回调，关注对港A传导"
    else:
        dashboard["market_tone"] = "Mixed | 市场分化，结构性机会为主"
    
    return dashboard


def get_news_by_category(category: str, page_size: int = 8) -> List[Dict]:
    """
    按类别获取新闻
    """
    queries = config.NEWS_QUERIES.get(category, [])
    all_news = []
    seen_titles = set()
    
    for query in queries:
        articles = fetch_newsapi(query, page_size=page_size)
        for article in articles:
            # 去重
            title_key = article["title"][:30] if article["title"] else ""
            if title_key and title_key not in seen_titles:
                seen_titles.add(title_key)
                all_news.append(article)
        time.sleep(config.REQUEST_DELAY)
    
    return all_news[:page_size]


def get_regulatory_news() -> List[Dict]:
    """监管政策新闻"""
    return get_news_by_category("regulatory", page_size=6)


def get_global_tmt_news() -> List[Dict]:
    """全球TMT新闻"""
    return get_news_by_category("global_tmt", page_size=6)


def get_china_tmt_news() -> List[Dict]:
    """中国TMT新闻"""
    # 混合中英文搜索
    all_news = []
    seen_titles = set()
    
    for query in config.NEWS_QUERIES.get("china_tmt", []):
        articles = fetch_newsapi(query, page_size=8)
        for article in articles:
            title_key = article["title"][:30] if article["title"] else ""
            if title_key and title_key not in seen_titles:
                seen_titles.add(title_key)
                all_news.append(article)
        time.sleep(config.REQUEST_DELAY)
    
    return all_news[:6]


def get_deal_news() -> List[Dict]:
    """Deal相关新闻（作为Deal Tracker的补充）"""
    return get_news_by_category("deals", page_size=10)


def get_research_highlights() -> List[Dict]:
    """卖方研究观点"""
    return get_news_by_category("research", page_size=6)


def get_upcoming_catalysts() -> List[Dict]:
    """
    未来一周关键事件
    基于固定日历 + 新闻补充
    """
    today = datetime.now()
    catalysts = []
    
    # 尝试从新闻中获取即将到来的IPO/财报事件
    news_items = get_news_by_category("deals", page_size=10)
    
    # 添加新闻中提到的事件
    for item in news_items[:5]:
        catalysts.append({
            "date": "近期",
            "event": item.get("title", ""),
            "impact": "Deal flow / Market sentiment",
        })
    
    return catalysts


def generate_executive_summary(market_data: Dict, news_data: Dict) -> List[Dict]:
    """
    生成Executive Summary（最重要的5条）
    结合市场行情和头条新闻自动生成
    """
    summaries = []
    
    # 1. 市场动态
    hsi = market_data.get("equity", {}).get("hsi", {})
    nasdaq = market_data.get("equity", {}).get("nasdaq", {})
    
    if isinstance(hsi, dict) and hsi.get("change_pct", 0) != 0:
        direction = "上涨" if hsi["change_pct"] > 0 else "下跌"
        summaries.append({
            "tag": "📈 Market Moving",
            "headline": f"恒生指数{direction}{abs(hsi['change_pct']):.2f}%，港股{'随美股走强' if hsi['change_pct'] > 0 else '承压回调'}",
            "why_it_matters": f"港股{'表现强劲，反映外资对中国资产风险偏好回升' if hsi['change_pct'] > 0 else '跟随全球风险资产回调，短期流动性面临考验'}",
            "capital_market_impact": f"{'有利于IPO窗口和配售定价' if hsi['change_pct'] > 0 else '可能推迟部分IPO定价，关注承销商护盘意愿'}",
        })
    
    # 2. 全球TMT头条（从新闻中取第一条）
    global_news = news_data.get("global_tmt", [])
    if global_news:
        top = global_news[0]
        summaries.append({
            "tag": "💼 Deal Relevant",
            "headline": top.get("title", "全球TMT重要动态"),
            "why_it_matters": top.get("description", "")[:100] if top.get("description") else "关注全球科技行业最新动向",
            "capital_market_impact": "可能影响相关板块估值水平和并购交易活跃度",
        })
    
    # 3. 监管动态
    reg_news = news_data.get("regulatory", [])
    if reg_news:
        top = reg_news[0]
        summaries.append({
            "tag": "🔥 Must Know",
            "headline": top.get("title", "监管政策更新"),
            "why_it_matters": top.get("description", "")[:100] if top.get("description") else "政策变化直接影响资本市场运作",
            "capital_market_impact": "可能影响IPO审核节奏、并购审批流程和融资窗口",
        })
    
    # 4. 中国TMT
    china_news = news_data.get("china_tmt", [])
    if china_news:
        top = china_news[0]
        summaries.append({
            "tag": "⭐ High Impact",
            "headline": top.get("title", "中国科技行业动态"),
            "why_it_matters": top.get("description", "")[:100] if top.get("description") else "中国科技巨头动向影响港股和美股中概股",
            "capital_market_impact": "影响相关板块交易活跃度和投资者情绪",
        })
    
    # 5. Deal动态
    deal_news = news_data.get("deals", [])
    if deal_news:
        top = deal_news[0]
        summaries.append({
            "tag": "💼 Deal Relevant",
            "headline": top.get("title", "资本市场交易动态"),
            "why_it_matters": top.get("description", "")[:100] if top.get("description") else "关注最新融资和并购动向",
            "capital_market_impact": "为同类交易提供估值参考和市场情绪指标",
        })
    
    return summaries[:5]


def generate_sector_watch(news_data: Dict) -> List[Dict]:
    """生成Sector Watch（3个最热门行业）"""
    sectors = [
        {
            "name": "Artificial Intelligence",
            "summary": "AI基础设施投资持续活跃，大模型商业化加速",
            "capital_market_impact": "AI相关IPO和私募融资保持高估值，算力芯片需求驱动半导体板块",
        },
        {
            "name": "Semiconductor",
            "summary": "全球半导体周期复苏信号增强，国产替代逻辑持续",
            "capital_market_impact": "设备材料类公司融资活跃，关注科创板和港股18C章节IPO",
        },
        {
            "name": "Cloud & Enterprise Software",
            "summary": "企业数字化转型需求稳健，SaaS公司盈利能力改善",
            "capital_market_impact": "软件公司并购估值回升，私有化交易增加",
        },
    ]
    return sectors


def generate_bankers_take(summary: List[Dict], market: Dict) -> str:
    """生成Banker's Take（简短观点）"""
    hsi = market.get("equity", {}).get("hsi", {})
    hsi_chg = hsi.get("change_pct", 0) if isinstance(hsi, dict) else 0
    
    if hsi_chg > 1:
        return "港股强势反弹打开IPO发行窗口，建议加速推进已准备就绪的发行项目。关注AI和半导体板块的交易活跃度，适时推出相关ECM交易。"
    elif hsi_chg < -1:
        return "市场回调期间建议暂缓定价敏感的IPO项目，利用窗口期完善申报材料。关注防御性板块的并购机会，以及私有化交易的融资需求。"
    else:
        return "市场震荡格局下结构性机会突出，建议聚焦AI、半导体等高景气赛道的配售和定增项目。密切关注监管政策动向，提前布局潜在的政策受益板块。"


def fetch_all_data() -> Dict[str, Any]:
    """
    获取晨报所需的所有数据
    """
    print(f"[{datetime.now()}] 开始获取晨报数据...")
    
    data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "market_dashboard": {},
        "executive_summary": [],
        "regulatory": [],
        "global_tmt": [],
        "china_tmt": [],
        "deals": [],
        "sector_watch": [],
        "research": [],
        "catalysts": [],
        "bankers_take": "",
    }
    
    # 1. 市场行情
    print("  → 获取市场行情...")
    data["market_dashboard"] = get_market_dashboard()
    
    # 2. 新闻数据
    print("  → 获取监管新闻...")
    data["regulatory"] = get_regulatory_news()
    
    print("  → 获取全球TMT新闻...")
    data["global_tmt"] = get_global_tmt_news()
    
    print("  → 获取中国TMT新闻...")
    data["china_tmt"] = get_china_tmt_news()
    
    print("  → 获取Deal新闻...")
    data["deals"] = get_deal_news()
    
    print("  → 获取研究观点...")
    data["research"] = get_research_highlights()
    
    # 3. 生成分析内容
    print("  → 生成Executive Summary...")
    news_data = {
        "global_tmt": data["global_tmt"],
        "regulatory": data["regulatory"],
        "china_tmt": data["china_tmt"],
        "deals": data["deals"],
    }
    data["executive_summary"] = generate_executive_summary(data["market_dashboard"], news_data)
    
    print("  → 生成Sector Watch...")
    data["sector_watch"] = generate_sector_watch(news_data)
    
    print("  → 生成Banker's Take...")
    data["bankers_take"] = generate_bankers_take(data["executive_summary"], data["market_dashboard"])
    
    print("  → 生成Upcoming Catalysts...")
    data["catalysts"] = get_upcoming_catalysts()
    
    print(f"[{datetime.now()}] 数据获取完成")
    return data


if __name__ == "__main__":
    # 测试
    data = fetch_all_data()
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str)[:2000])
