"""
TMT Morning Brief - WeChat Notifier
通过微信推送晨报摘要（支持Server酱和企业微信机器人）
"""
import requests
import json
from datetime import datetime
from typing import Optional

import config


def send_serverchan(title: str, content: str, skey: Optional[str] = None) -> bool:
    """
    通过Server酱推送消息到微信
    
    Args:
        title: 消息标题
        content: 消息内容（支持Markdown）
        skey: Server酱SendKey（默认从config读取）
    
    Returns:
        bool: 发送是否成功
    
    Setup:
        1. 访问 https://sct.ftqq.com/ 扫码登录
        2. 获取 SendKey
        3. 设置环境变量 SERVERCHAN_KEY=your_key
    """
    skey = skey or config.SERVERCHAN_KEY
    
    if not skey:
        print("[WeChat Error] 未配置Server酱Key: 请设置 SERVERCHAN_KEY 环境变量")
        print("  配置步骤:")
        print("    1. 访问 https://sct.ftqq.com/ 扫码登录")
        print("    2. 复制 SendKey")
        print("    3. export SERVERCHAN_KEY=your_key")
        return False
    
    url = f"https://sctapi.ftqq.com/{skey}.send"
    payload = {
        "title": title,
        "desp": content,
    }
    
    try:
        resp = requests.post(url, data=payload, timeout=15)
        data = resp.json()
        
        if data.get("code") == 0 or data.get("data", {}).get("errno") == 0:
            print(f"[WeChat Sent] Server酱推送成功")
            return True
        else:
            print(f"[WeChat Error] Server酱推送失败: {data}")
            return False
            
    except Exception as e:
        print(f"[WeChat Error] Server酱请求异常: {e}")
        return False


def send_wechat_webhook(content: str, webhook_url: Optional[str] = None, msg_type: str = "markdown") -> bool:
    """
    通过企业微信机器人Webhook推送
    
    Args:
        content: 消息内容
        webhook_url: 企业微信机器人Webhook地址
        msg_type: 消息类型 (text/markdown)
    
    Returns:
        bool: 发送是否成功
    
    Setup:
        1. 在企业微信群中创建群机器人
        2. 复制Webhook地址
        3. 设置环境变量 WECHAT_WEBHOOK=your_webhook_url
    """
    webhook_url = webhook_url or config.WECHAT_WEBHOOK
    
    if not webhook_url:
        print("[WeChat Error] 未配置企业微信Webhook: 请设置 WECHAT_WEBHOOK 环境变量")
        print("  配置步骤:")
        print("    1. 在企业微信群 → 群设置 → 添加群机器人")
        print("    2. 复制Webhook地址")
        print("    3. export WECHAT_WEBHOOK=https://qyapi.weixin.qq.com/cgi-bin/webhook/...")
        return False
    
    payload = {
        "msgtype": msg_type,
        "markdown" if msg_type == "markdown" else "text": {
            "content": content,
        }
    }
    
    try:
        resp = requests.post(webhook_url, json=payload, timeout=15)
        data = resp.json()
        
        if data.get("errcode") == 0:
            print(f"[WeChat Sent] 企业微信推送成功")
            return True
        else:
            print(f"[WeChat Error] 企业微信推送失败: {data}")
            return False
            
    except Exception as e:
        print(f"[WeChat Error] 企业微信请求异常: {e}")
        return False


def send_brief_wechat(text_content: str, title: Optional[str] = None) -> bool:
    """
    发送晨报摘要到微信（自动选择可用的推送渠道）
    
    Args:
        text_content: 纯文本晨报内容
        title: 推送标题（可选）
    
    Returns:
        bool: 是否成功发送到至少一个渠道
    """
    if not title:
        today = datetime.now().strftime("%Y-%m-%d")
        weekday = datetime.now().strftime("%a")
        title = f"📊 TMT Morning Brief | {today} ({weekday})"
    
    results = []
    
    # 优先尝试Server酱（个人微信推送）
    if config.SERVERCHAN_KEY:
        results.append(send_serverchan(title, text_content))
    
    # 其次尝试企业微信
    if config.WECHAT_WEBHOOK:
        # 企业微信markdown长度限制4096，截断处理
        truncated = text_content[:3500] + "\n\n...(truncated)" if len(text_content) > 3500 else text_content
        results.append(send_wechat_webhook(truncated, msg_type="markdown"))
    
    return any(results) if results else False


def test_wechat() -> bool:
    """
    发送测试消息到微信
    """
    title = "📧 TMT Morning Brief - 微信推送测试"
    content = """## ✅ 微信推送配置测试

这是一封测试消息，用于验证您的微信推送配置是否正确。

**如果您收到这条消息，说明微信推送功能已就绪！**

---
配置说明：
- Server酱: https://sct.ftqq.com/
- 企业微信机器人: 群设置 → 添加机器人
"""
    
    print("测试微信推送...")
    
    if config.SERVERCHAN_KEY:
        print("  → 测试Server酱...")
        return send_serverchan(title, content)
    elif config.WECHAT_WEBHOOK:
        print("  → 测试企业微信...")
        return send_wechat_webhook(content, msg_type="markdown")
    else:
        print("  ⚠️ 未配置任何微信推送渠道")
        print("  如需微信推送，请配置以下任一环境变量:")
        print("    export SERVERCHAN_KEY=your_key")
        print("    export WECHAT_WEBHOOK=your_webhook_url")
        return False


if __name__ == "__main__":
    test_wechat()
