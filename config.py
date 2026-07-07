"""
TMT Morning Brief - Configuration
所有敏感信息通过环境变量注入，不硬编码
"""
import os

# ======== 邮件配置 ========
# 发件邮箱（建议使用Gmail应用专用密码）
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")  # 发件邮箱，如 yourname@gmail.com
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")  # 邮箱密码或应用专用密码

# 收件人配置
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "dianeshi0829@gmail.com")

# ======== NewsAPI 配置 ========
# 免费注册获取API Key: https://newsapi.org/register
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")

# ======== 微信推送配置（可选） ========
# 方案1: Server酱 (https://sct.ftqq.com/) - 免费版支持每日5条
SERVERCHAN_KEY = os.getenv("SERVERCHAN_KEY", "")
# 方案2: 企业微信机器人 Webhook
WECHAT_WEBHOOK = os.getenv("WECHAT_WEBHOOK", "")

# ======== 推送开关 ========
ENABLE_EMAIL = os.getenv("ENABLE_EMAIL", "true").lower() == "true"
ENABLE_WECHAT = os.getenv("ENABLE_WECHAT", "false").lower() == "true"

# ======== 晨报内容配置 ========
# 是否包含各板块
SECTIONS = {
    "executive_summary": True,
    "market_dashboard": True,
    "regulatory_update": True,
    "global_tmt": True,
    "china_tmt": True,
    "deal_tracker": True,
    "sector_watch": True,
    "research_highlights": True,
    "upcoming_catalysts": True,
    "bankers_take": True,
}

# 市场指数配置
MARKET_INDICES = {
    # A股
    "sh_index": {"name": "上证指数", "code": "1.000001", "source": "eastmoney"},
    "sz_index": {"name": "深证成指", "code": "0.399001", "source": "eastmoney"},
    "chinext": {"name": "创业板指", "code": "1.399006", "source": "eastmoney"},
    "kcb50": {"name": "科创50", "code": "1.000688", "source": "eastmoney"},
    # 港股
    "hsi": {"name": "恒生指数", "symbol": "^HSI", "source": "yahoo"},
    "hstech": {"name": "恒生科技", "symbol": "^HSTECH", "source": "yahoo"},
    # 美股
    "nasdaq": {"name": "Nasdaq", "symbol": "^IXIC", "source": "yahoo"},
    "sp500": {"name": "S&P 500", "symbol": "^GSPC", "source": "yahoo"},
    "sox": {"name": "费城半导体", "symbol": "^SOX", "source": "yahoo"},
}

# 商品/利率
COMMODITIES_RATES = {
    "gold": {"name": "黄金", "symbol": "GC=F", "source": "yahoo"},
    "oil": {"name": "WTI原油", "symbol": "CL=F", "source": "yahoo"},
    "copper": {"name": "铜", "symbol": "HG=F", "source": "yahoo"},
    "us_10y": {"name": "US 10Y", "symbol": "^TNX", "source": "yahoo"},
}

# 汇率
FX_RATES = {
    "usdcny": {"name": "USD/CNY", "symbol": "CNY=X", "source": "yahoo"},
    "usdhkd": {"name": "USD/HKD", "symbol": "HKD=X", "source": "yahoo"},
}

# NewsAPI 搜索关键词（按板块）
NEWS_QUERIES = {
    "global_tmt": [
        "technology IPO semiconductor AI funding",
        "tech M&A acquisition cloud enterprise",
    ],
    "china_tmt": [
        "Tencent Alibaba Huawei ByteDance Baidu",
        "China technology AI policy regulatory",
    ],
    "regulatory": [
        "CSRC China securities regulatory policy",
        "HKEX Hong Kong IPO listing regulation",
        "SEC regulation technology IPO",
    ],
    "deals": [
        "technology funding round venture capital",
        "Hong Kong IPO listing",
        "semiconductor AI robot private placement",
    ],
    "research": [
        "Morgan Stanley Goldman Sachs tech valuation",
        "JPMorgan UBS semiconductor internet outlook",
    ],
}

# 数据请求间隔（秒）- 遵守各服务rate limit
REQUEST_DELAY = 0.5

# 输出文件路径
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./output")
