     1	"""
     2	TMT Morning Brief - Configuration
     3	所有敏感信息通过环境变量注入，不硬编码
     4	"""
     5	import os
     6	
     7	# ======== 邮件配置 ========
     8	# 发件邮箱（建议使用Gmail应用专用密码）
     9	# 使用 "or default" 模式处理空字符串情况
    10	SMTP_HOST = os.getenv("SMTP_HOST") or "smtp.gmail.com"
    11	SMTP_PORT = int(os.getenv("SMTP_PORT") or "587")
    12	SMTP_USER = os.getenv("SMTP_USER") or ""  # 发件邮箱，如 yourname@gmail.com
    13	SMTP_PASSWORD = os.getenv("SMTP_PASSWORD") or ""  # 邮箱密码或应用专用密码
    14	
    15	# 收件人配置
    16	RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL") or "dianeshi0829@gmail.com"
    17	
    18	# ======== NewsAPI 配置 ========
    19	# 免费注册获取API Key: https://newsapi.org/register
    20	NEWSAPI_KEY = os.getenv("NEWSAPI_KEY") or ""
    21	
    22	# ======== 微信推送配置（可选） ========
    23	# 方案1: Server酱 (https://sct.ftqq.com/) - 免费版支持每日5条
    24	SERVERCHAN_KEY = os.getenv("SERVERCHAN_KEY") or ""
    25	# 方案2: 企业微信机器人 Webhook
    26	WECHAT_WEBHOOK = os.getenv("WECHAT_WEBHOOK") or ""
    27	
    28	# ======== 推送开关 ========
    29	ENABLE_EMAIL = (os.getenv("ENABLE_EMAIL") or "true").lower() == "true"
    30	ENABLE_WECHAT = (os.getenv("ENABLE_WECHAT") or "false").lower() == "true"
    31	
    32	# ======== 晨报内容配置 ========
    33	# 是否包含各板块
    34	SECTIONS = {
    35	    "executive_summary": True,
    36	    "market_dashboard": True,
    37	    "regulatory_update": True,
    38	    "global_tmt": True,
    39	    "china_tmt": True,
    40	    "deal_tracker": True,
    41	    "sector_watch": True,
    42	    "research_highlights": True,
    43	    "upcoming_catalysts": True,
    44	    "bankers_take": True,
    45	}
    46	
    47	# 市场指数配置
    48	MARKET_INDICES = {
    49	    # A股
    50	    "sh_index": {"name": "上证指数", "code": "1.000001", "source": "eastmoney"},
    51	    "sz_index": {"name": "深证成指", "code": "0.399001", "source": "eastmoney"},
    52	    "chinext": {"name": "创业板指", "code": "1.399006", "source": "eastmoney"},
    53	    "kcb50": {"name": "科创50", "code": "1.000688", "source": "eastmoney"},
    54	    # 港股
    55	    "hsi": {"name": "恒生指数", "symbol": "^HSI", "source": "yahoo"},
    56	    "hstech": {"name": "恒生科技", "symbol": "^HSTECH", "source": "yahoo"},
    57	    # 美股
    58	    "nasdaq": {"name": "Nasdaq", "symbol": "^IXIC", "source": "yahoo"},
    59	    "sp500": {"name": "S&P 500", "symbol": "^GSPC", "source": "yahoo"},
    60	    "sox": {"name": "费城半导体", "symbol": "^SOX", "source": "yahoo"},
    61	}
    62	
    63	# 商品/利率
    64	COMMODITIES_RATES = {
    65	    "gold": {"name": "黄金", "symbol": "GC=F", "source": "yahoo"},
    66	    "oil": {"name": "WTI原油", "symbol": "CL=F", "source": "yahoo"},
    67	    "copper": {"name": "铜", "symbol": "HG=F", "source": "yahoo"},
    68	    "us_10y": {"name": "US 10Y", "symbol": "^TNX", "source": "yahoo"},
    69	}
    70	
    71	# 汇率
    72	FX_RATES = {
    73	    "usdcny": {"name": "USD/CNY", "symbol": "CNY=X", "source": "yahoo"},
    74	    "usdhkd": {"name": "USD/HKD", "symbol": "HKD=X", "source": "yahoo"},
    75	}
    76	
    77	# NewsAPI 搜索关键词（按板块）
    78	NEWS_QUERIES = {
    79	    "global_tmt": [
    80	        "technology IPO semiconductor AI funding",
    81	        "tech M&A acquisition cloud enterprise",
    82	    ],
    83	    "china_tmt": [
    84	        "Tencent Alibaba Huawei ByteDance Baidu",
    85	        "China technology AI policy regulatory",
    86	    ],
    87	    "regulatory": [
    88	        "CSRC China securities regulatory policy",
    89	        "HKEX Hong Kong IPO listing regulation",
    90	        "SEC regulation technology IPO",
    91	    ],
    92	    "deals": [
    93	        "technology funding round venture capital",
    94	        "Hong Kong IPO listing",
    95	        "semiconductor AI robot private placement",
    96	    ],
    97	    "research": [
    98	        "Morgan Stanley Goldman Sachs tech valuation",
    99	        "JPMorgan UBS semiconductor internet outlook",
   100	    ],
   101	}
   102	
   103	# 数据请求间隔（秒）- 遵守各服务rate limit
   104	REQUEST_DELAY = 0.5
   105	
   106	# 输出文件路径
   107	OUTPUT_DIR = os.getenv("OUTPUT_DIR") or "./output"
   108	
