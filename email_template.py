"""
TMT Morning Brief - HTML Email Template
将晨报数据渲染为精美的HTML邮件
"""
from datetime import datetime
from typing import Dict, List, Any


def render_html(brief_data: Dict[str, Any]) -> str:
    """
    渲染完整HTML邮件
    """
    date_str = brief_data.get("date", datetime.now().strftime("%Y-%m-%d"))
    weekday = datetime.now().strftime("%A")
    weekday_cn = {"Monday": "周一", "Tuesday": "周二", "Wednesday": "周三",
                  "Thursday": "周四", "Friday": "周五", "Saturday": "周六", "Sunday": "周日"}.get(weekday, weekday)
    
    # 各板块数据
    exec_summary = brief_data.get("executive_summary", [])
    market = brief_data.get("market_dashboard", {})
    regulatory = brief_data.get("regulatory", [])
    global_tmt = brief_data.get("global_tmt", [])
    china_tmt = brief_data.get("china_tmt", [])
    deals = brief_data.get("deals", [])
    sectors = brief_data.get("sector_watch", [])
    research = brief_data.get("research", [])
    catalysts = brief_data.get("catalysts", [])
    bankers_take = brief_data.get("bankers_take", "")
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TMT Morning Brief - {date_str}</title>
<style>
    @media only screen and (max-width: 600px) {{
        .container {{ width: 100% !important; }}
        .metric-box {{ width: 48% !important; margin-bottom: 8px; }}
        .headline {{ font-size: 15px !important; }}
    }}
    body {{ margin: 0; padding: 0; background-color: #0f172a; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; }}
    .container {{ max-width: 720px; margin: 0 auto; background-color: #0f172a; color: #e2e8f0; }}
    .header {{ background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 32px 24px; text-align: center; border-bottom: 3px solid #3b82f6; }}
    .header h1 {{ margin: 0; font-size: 24px; font-weight: 700; color: #f8fafc; letter-spacing: 0.5px; }}
    .header .subtitle {{ margin-top: 8px; font-size: 13px; color: #94a3b8; }}
    .header .date {{ margin-top: 4px; font-size: 14px; color: #60a5fa; font-weight: 500; }}
    .section {{ padding: 20px 24px; border-bottom: 1px solid #1e293b; }}
    .section-title {{ font-size: 16px; font-weight: 700; color: #f8fafc; margin: 0 0 14px 0; display: flex; align-items: center; gap: 8px; }}
    .section-icon {{ font-size: 18px; }}
    .tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; margin-right: 6px; }}
    .tag-must {{ background: #7f1d1d; color: #fca5a5; }}
    .tag-deal {{ background: #14532d; color: #86efac; }}
    .tag-market {{ background: #1e3a5f; color: #93c5fd; }}
    .tag-high {{ background: #4c1d95; color: #c4b5fd; }}
    .tag-watch {{ background: #713f12; color: #fde68a; }}
    .headline {{ font-size: 14px; font-weight: 600; color: #f1f5f9; line-height: 1.5; margin: 0 0 6px 0; }}
    .body-text {{ font-size: 13px; color: #cbd5e1; line-height: 1.7; margin: 0 0 16px 0; }}
    .body-text:last-child {{ margin-bottom: 0; }}
    .highlight {{ color: #60a5fa; font-weight: 500; }}
    .divider {{ border: none; border-top: 1px solid #334155; margin: 14px 0; }}
    .metrics-grid {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }}
    .metric-box {{ flex: 1; min-width: 120px; background: #1e293b; border-radius: 8px; padding: 12px; text-align: center; border: 1px solid #334155; }}
    .metric-name {{ font-size: 11px; color: #94a3b8; margin-bottom: 4px; }}
    .metric-value {{ font-size: 16px; font-weight: 700; }}
    .metric-change {{ font-size: 12px; margin-top: 2px; }}
    .up {{ color: #f87171; }}      /* A股/港股红涨 */
    .down {{ color: #4ade80; }}    /* A股/港股绿跌 */
    .up-us {{ color: #4ade80; }}   /* 美股绿涨 */
    .down-us {{ color: #f87171; }} /* 美股红跌 */
    .market-tone {{ background: #1e293b; border-left: 4px solid #3b82f6; padding: 10px 14px; font-size: 13px; color: #e2e8f0; border-radius: 0 6px 6px 0; }}
    .news-item {{ margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid #1e293b; }}
    .news-item:last-child {{ border-bottom: none; margin-bottom: 0; padding-bottom: 0; }}
    .news-source {{ font-size: 11px; color: #64748b; margin-top: 4px; }}
    .news-link {{ color: #60a5fa; text-decoration: none; }}
    .news-link:hover {{ text-decoration: underline; }}
    .deal-table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
    .deal-table th {{ background: #1e293b; color: #94a3b8; padding: 8px; text-align: left; font-weight: 600; border-bottom: 2px solid #334155; }}
    .deal-table td {{ padding: 8px; border-bottom: 1px solid #1e293b; color: #cbd5e1; }}
    .deal-table tr:last-child td {{ border-bottom: none; }}
    .sector-box {{ background: #1e293b; border-radius: 8px; padding: 14px; margin-bottom: 10px; border: 1px solid #334155; }}
    .sector-name {{ font-size: 14px; font-weight: 700; color: #f8fafc; margin: 0 0 6px 0; }}
    .catalyst-table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
    .catalyst-table th {{ background: #1e293b; color: #94a3b8; padding: 8px; text-align: left; font-weight: 600; border-bottom: 2px solid #334155; }}
    .catalyst-table td {{ padding: 8px; border-bottom: 1px solid #1e293b; color: #cbd5e1; }}
    .banker-take {{ background: linear-gradient(135deg, #1e293b 0%, #1a365d 100%); border-left: 4px solid #f59e0b; padding: 16px; border-radius: 0 8px 8px 0; font-size: 14px; color: #f8fafc; line-height: 1.8; font-style: italic; }}
    .footer {{ padding: 20px 24px; text-align: center; font-size: 11px; color: #64748b; }}
    .footer a {{ color: #60a5fa; text-decoration: none; }}
    .star-rating {{ color: #fbbf24; font-size: 12px; }}
    .item-label {{ font-size: 12px; color: #60a5fa; font-weight: 600; margin-right: 6px; }}
</style>
</head>
<body>
<div class="container">
    <!-- Header -->
    <div class="header">
        <h1>📊 TMT MORNING BRIEF</h1>
        <div class="subtitle">Investment Banking Daily Intelligence</div>
        <div class="date">{date_str} {weekday_cn} | Generated at {datetime.now().strftime('%H:%M')}</div>
    </div>
"""
    
    # ===== 1. Executive Summary =====
    if exec_summary:
        html += """
    <!-- Executive Summary -->
    <div class="section">
        <div class="section-title"><span class="section-icon">🔥</span> Executive Summary <span class="star-rating">★★★★★</span></div>
"""
        for item in exec_summary:
            tag_class = {
                "🔥 Must Know": "tag-must",
                "💼 Deal Relevant": "tag-deal",
                "📈 Market Moving": "tag-market",
                "⭐ High Impact": "tag-high",
                "📌 Watchlist": "tag-watch",
            }.get(item.get("tag", ""), "tag-high")
            tag_name = item.get("tag", "").replace("🔥 ", "").replace("💼 ", "").replace("📈 ", "").replace("⭐ ", "").replace("📌 ", "")
            
            html += f"""
        <div style="margin-bottom: 14px;">
            <span class="tag {tag_class}">{tag_name}</span>
            <div class="headline" style="margin-top: 6px;">{item.get('headline', '')}</div>
            <div class="body-text"><span class="item-label">Why it matters:</span>{item.get('why_it_matters', '')}</div>
            <div class="body-text"><span class="item-label">Capital Market Impact:</span><span class="highlight">{item.get('capital_market_impact', '')}</span></div>
        </div>
        <hr class="divider">
"""
        html += "    </div>\n"
    
    # ===== 2. Capital Market Dashboard =====
    html += """
    <!-- Capital Market Dashboard -->
    <div class="section">
        <div class="section-title"><span class="section-icon">📈</span> Capital Market Dashboard <span class="star-rating">★★★★</span></div>
"""
    
    # Equity indices
    equity = market.get("equity", {})
    if equity:
        html += '<div class="metrics-grid">\n'
        for key, info in equity.items():
            if isinstance(info, dict):
                price = info.get("price", "N/A")
                change_pct = info.get("change_pct", 0)
                name = info.get("name", key)
                is_us = key in ["nasdaq", "sp500", "sox"]
                up_class = "up-us" if is_us else "up"
                down_class = "down-us" if is_us else "down"
                color_class = up_class if change_pct > 0 else (down_class if change_pct < 0 else "")
                sign = "+" if change_pct > 0 else ""
                html += f"""            <div class="metric-box">
                <div class="metric-name">{name}</div>
                <div class="metric-value {color_class}">{price}</div>
                <div class="metric-change {color_class}">{sign}{change_pct:.2f}%</div>
            </div>
"""
        html += '        </div>\n'
    
    # Commodities & Rates
    commodities = market.get("commodities", {})
    rates = market.get("rates", {})
    fx = market.get("fx", {})
    
    all_other = {**{f"commodities_{k}": v for k, v in commodities.items() if isinstance(v, dict)},
                 **{f"rates_{k}": v for k, v in rates.items() if isinstance(v, dict)},
                 **{f"fx_{k}": v for k, v in fx.items() if isinstance(v, dict)}}
    
    if all_other:
        html += '<div class="metrics-grid">\n'
        for key, info in all_other.items():
            name = info.get("name", key)
            price = info.get("price", "N/A")
            change_pct = info.get("change_pct", 0)
            color_class = "up-us" if change_pct > 0 else ("down-us" if change_pct < 0 else "")
            sign = "+" if change_pct > 0 else ""
            html += f"""            <div class="metric-box">
                <div class="metric-name">{name}</div>
                <div class="metric-value {color_class}">{price}</div>
                <div class="metric-change {color_class}">{sign}{change_pct:.2f}%</div>
            </div>
"""
        html += '        </div>\n'
    
    # Market Tone
    tone = market.get("market_tone", "")
    if tone:
        html += f'        <div class="market-tone">📊 <strong>Market Tone:</strong> {tone}</div>\n'
    
    html += "    </div>\n"
    
    # ===== 3. Regulatory Update =====
    if regulatory:
        html += """
    <!-- Regulatory Update -->
    <div class="section">
        <div class="section-title"><span class="section-icon">📋</span> China & HK Regulatory Update <span class="star-rating">★★★★★</span></div>
"""
        for item in regulatory[:4]:
            html += f"""        <div class="news-item">
            <span class="tag tag-must">Regulatory</span>
            <div class="headline" style="margin-top: 6px;">{item.get('title', '')}</div>
            <div class="body-text">{item.get('description', '')}</div>
            <div class="news-source">Source: {item.get('source', 'NewsAPI')} | {item.get('publishedAt', '')[:10] if item.get('publishedAt') else ''}</div>
        </div>
"""
        html += "    </div>\n"
    
    # ===== 4. Global TMT Headlines =====
    if global_tmt:
        html += """
    <!-- Global TMT Headlines -->
    <div class="section">
        <div class="section-title"><span class="section-icon">🌍</span> Deal Relevant TMT Headlines <span class="star-rating">★★★★</span></div>
"""
        for item in global_tmt[:4]:
            html += f"""        <div class="news-item">
            <span class="tag tag-deal">Global TMT</span>
            <div class="headline" style="margin-top: 6px;"><a href="{item.get('url', '#')}" class="news-link" target="_blank">{item.get('title', '')}</a></div>
            <div class="body-text">{item.get('description', '')}</div>
            <div class="news-source">Source: {item.get('source', 'NewsAPI')}</div>
        </div>
"""
        html += "    </div>\n"
    
    # ===== 5. China TMT Headlines =====
    if china_tmt:
        html += """
    <!-- China TMT Headlines -->
    <div class="section">
        <div class="section-title"><span class="section-icon">🇨🇳</span> China TMT Headlines <span class="star-rating">★★★★</span></div>
"""
        for item in china_tmt[:4]:
            html += f"""        <div class="news-item">
            <span class="tag tag-high">China TMT</span>
            <div class="headline" style="margin-top: 6px;"><a href="{item.get('url', '#')}" class="news-link" target="_blank">{item.get('title', '')}</a></div>
            <div class="body-text">{item.get('description', '')}</div>
            <div class="news-source">Source: {item.get('source', 'NewsAPI')}</div>
        </div>
"""
        html += "    </div>\n"
    
    # ===== 6. Deal Tracker =====
    if deals:
        html += """
    <!-- Deal Tracker -->
    <div class="section">
        <div class="section-title"><span class="section-icon">💰</span> Deal Tracker <span class="star-rating">★★★★★</span></div>
        <p style="font-size: 12px; color: #94a3b8; margin-bottom: 12px;">Based on public news aggregation. For verified data, refer to HKEX Disclosure / SEC EDGAR / 披露易.</p>
"""
        html += """        <table class="deal-table">
            <thead>
                <tr><th>Company / Headline</th><th>Type</th><th>Source</th></tr>
            </thead>
            <tbody>
"""
        for item in deals[:8]:
            title = item.get('title', '')[:60]
            desc = item.get('description', '')[:80]
            source = item.get('source', 'NewsAPI')
            # 判断类型
            deal_type = "Deal"
            title_lower = title.lower()
            if any(k in title_lower for k in ['ipo', 'listing', '上市']):
                deal_type = '<span style="color: #60a5fa;">IPO</span>'
            elif any(k in title_lower for k in ['acquisition', 'm&a', 'acquire', '并购']):
                deal_type = '<span style="color: #f472b6;">M&A</span>'
            elif any(k in title_lower for k in ['funding', 'round', 'invest', '融资']):
                deal_type = '<span style="color: #4ade80;">Financing</span>'
            elif any(k in title_lower for k in ['bond', 'convertible', 'note']):
                deal_type = '<span style="color: #fbbf24;">ECM</span>'
            
            html += f"""                <tr>
                    <td><strong>{title}</strong><br><span style="color: #94a3b8; font-size: 11px;">{desc}</span></td>
                    <td>{deal_type}</td>
                    <td>{source}</td>
                </tr>
"""
        html += """            </tbody>
        </table>
    </div>
"""
    
    # ===== 7. Sector Watch =====
    if sectors:
        html += """
    <!-- Sector Watch -->
    <div class="section">
        <div class="section-title"><span class="section-icon">📊</span> Sector Watch <span class="star-rating">★★★</span></div>
"""
        for sector in sectors[:3]:
            html += f"""        <div class="sector-box">
            <div class="sector-name">{sector.get('name', '')}</div>
            <div class="body-text"><span class="item-label">Summary:</span>{sector.get('summary', '')}</div>
            <div class="body-text"><span class="item-label">Capital Market Impact:</span><span class="highlight">{sector.get('capital_market_impact', '')}</span></div>
        </div>
"""
        html += "    </div>\n"
    
    # ===== 8. Research Highlights =====
    if research:
        html += """
    <!-- Research Highlights -->
    <div class="section">
        <div class="section-title"><span class="section-icon">📑</span> Research Highlights <span class="star-rating">★★★</span></div>
"""
        for item in research[:3]:
            html += f"""        <div class="news-item">
            <span class="tag tag-watch">Research</span>
            <div class="headline" style="margin-top: 6px;"><a href="{item.get('url', '#')}" class="news-link" target="_blank">{item.get('title', '')}</a></div>
            <div class="body-text">{item.get('description', '')}</div>
            <div class="news-source">Source: {item.get('source', 'NewsAPI')}</div>
        </div>
"""
        html += "    </div>\n"
    
    # ===== 9. Upcoming Catalysts =====
    if catalysts:
        html += """
    <!-- Upcoming Catalysts -->
    <div class="section">
        <div class="section-title"><span class="section-icon">⏰</span> Upcoming Catalysts (7 Days) <span class="star-rating">★★★</span></div>
        <table class="catalyst-table">
            <thead>
                <tr><th>Date</th><th>Event</th><th>Potential Impact</th></tr>
            </thead>
            <tbody>
"""
        for cat in catalysts[:6]:
            html += f"""                <tr>
                    <td>{cat.get('date', 'TBD')}</td>
                    <td>{cat.get('event', '')}</td>
                    <td>{cat.get('impact', '')}</td>
                </tr>
"""
        html += """            </tbody>
        </table>
    </div>
"""
    
    # ===== 10. Banker's Take =====
    if bankers_take:
        html += f"""
    <!-- Banker's Take -->
    <div class="section">
        <div class="section-title"><span class="section-icon">💡</span> Banker's Take <span class="star-rating">★★★★★</span></div>
        <div class="banker-take">
            {bankers_take}
        </div>
    </div>
"""
    
    # ===== Footer =====
    html += f"""
    <!-- Footer -->
    <div class="footer">
        <p>TMT Morning Brief | Generated automatically by <a href="#">tmt-ib-morning-brief</a> skill</p>
        <p>Data sources: East Money, Yahoo Finance, NewsAPI | For reference only, not investment advice</p>
        <p style="margin-top: 8px; color: #475569;">{date_str} {datetime.now().strftime('%H:%M')}</p>
    </div>
</div>
</body>
</html>"""
    
    return html


def render_text_version(brief_data: Dict[str, Any]) -> str:
    """
    渲染纯文本版本（用于微信推送等纯文本场景）
    """
    date_str = brief_data.get("date", datetime.now().strftime("%Y-%m-%d"))
    lines = [
        f"📊 TMT MORNING BRIEF - {date_str}",
        "=" * 50,
        "",
    ]
    
    # Executive Summary
    exec_summary = brief_data.get("executive_summary", [])
    if exec_summary:
        lines.append("🔥 EXECUTIVE SUMMARY")
        lines.append("-" * 30)
        for item in exec_summary[:3]:
            lines.append(f"• {item.get('tag', '')} {item.get('headline', '')}")
            lines.append(f"  Why: {item.get('why_it_matters', '')}")
            lines.append("")
    
    # Market
    market = brief_data.get("market_dashboard", {})
    equity = market.get("equity", {})
    if equity:
        lines.append("📈 MARKET SNAPSHOT")
        lines.append("-" * 30)
        for key, info in equity.items():
            if isinstance(info, dict):
                sign = "+" if info.get("change_pct", 0) > 0 else ""
                lines.append(f"• {info.get('name', key)}: {info.get('price', 'N/A')} ({sign}{info.get('change_pct', 0):.2f}%)")
        lines.append(f"Tone: {market.get('market_tone', '')}")
        lines.append("")
    
    # Deals
    deals = brief_data.get("deals", [])
    if deals:
        lines.append("💰 DEAL TRACKER")
        lines.append("-" * 30)
        for item in deals[:5]:
            lines.append(f"• {item.get('title', '')}")
        lines.append("")
    
    # Banker's Take
    take = brief_data.get("bankers_take", "")
    if take:
        lines.append("💡 BANKER'S TAKE")
        lines.append("-" * 30)
        lines.append(take)
        lines.append("")
    
    lines.append("=" * 50)
    lines.append("Data: East Money, Yahoo Finance, NewsAPI")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # 测试渲染
    test_data = {
        "date": "2024-07-07",
        "executive_summary": [
            {
                "tag": "📈 Market Moving",
                "headline": "测试标题",
                "why_it_matters": "测试原因",
                "capital_market_impact": "测试影响",
            }
        ],
        "market_dashboard": {
            "equity": {
                "hsi": {"name": "恒生指数", "price": 17500, "change_pct": 1.2},
            },
            "market_tone": "Risk-on",
        },
        "deals": [],
        "bankers_take": "测试观点",
    }
    print(render_html(test_data)[:2000])
