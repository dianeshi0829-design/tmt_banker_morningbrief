#!/usr/bin/env python3
"""
TMT Morning Brief - Main Entry Point
定时生成并推送TMT投行晨报

Usage:
    python main.py                          # 生成并推送晨报
    python main.py --generate-only          # 仅生成，不推送
    python main.py --test-email             # 发送测试邮件
    python main.py --test-wechat            # 发送测试微信
    python main.py --dry-run                # 获取数据但不生成邮件（调试）
"""
import argparse
import os
import sys
import json
from datetime import datetime

# 确保能导入本地模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_fetcher import fetch_all_data
from email_template import render_html, render_text_version
from email_sender import send_brief_email, send_test_email
from wechat_notifier import send_brief_wechat, test_wechat
import config


def generate_and_send_brief(generate_only: bool = False) -> bool:
    """
    生成晨报并推送
    
    Args:
        generate_only: 如果为True，只生成不推送
    
    Returns:
        bool: 整体是否成功
    """
    print("=" * 60)
    print(f"🚀 TMT Morning Brief - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # Step 1: 获取数据
    print("\n📡 Step 1: Fetching market data & news...")
    try:
        brief_data = fetch_all_data()
    except Exception as e:
        print(f"❌ Data fetching failed: {e}")
        return False
    
    # Step 2: 渲染邮件
    print("\n🎨 Step 2: Rendering email template...")
    try:
        html_content = render_html(brief_data)
        text_content = render_text_version(brief_data)
    except Exception as e:
        print(f"❌ Template rendering failed: {e}")
        return False
    
    # Step 3: 保存到本地（无论是否推送都保存）
    print("\n💾 Step 3: Saving to local file...")
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    date_str = brief_data.get("date", datetime.now().strftime("%Y-%m-%d"))
    
    html_path = os.path.join(config.OUTPUT_DIR, f"brief_{date_str}.html")
    json_path = os.path.join(config.OUTPUT_DIR, f"brief_{date_str}.json")
    txt_path = os.path.join(config.OUTPUT_DIR, f"brief_{date_str}.txt")
    
    try:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"  ✓ HTML saved: {html_path}")
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(brief_data, f, ensure_ascii=False, indent=2, default=str)
        print(f"  ✓ JSON saved: {json_path}")
        
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text_content)
        print(f"  ✓ Text saved: {txt_path}")
            
    except Exception as e:
        print(f"  ⚠️ Save failed (non-critical): {e}")
    
    if generate_only:
        print("\n✅ Brief generated successfully (not sent)")
        return True
    
    # Step 4: 推送邮件
    success = True
    if config.ENABLE_EMAIL:
        print("\n📧 Step 4: Sending email...")
        email_sent = send_brief_email(html_content, text_content)
        if not email_sent:
            print("  ⚠️ Email sending failed")
            success = False
    else:
        print("\n⏭️ Step 4: Email disabled, skipping...")
    
    # Step 5: 推送微信
    if config.ENABLE_WECHAT:
        print("\n💬 Step 5: Sending WeChat notification...")
        wechat_sent = send_brief_wechat(text_content)
        if not wechat_sent:
            print("  ⚠️ WeChat sending failed")
            success = False
    else:
        print("\n⏭️ Step 5: WeChat disabled, skipping...")
    
    # Summary
    print("\n" + "=" * 60)
    if success:
        print("✅ Morning Brief completed successfully!")
    else:
        print("⚠️ Morning Brief completed with some issues")
    print("=" * 60)
    
    return success


def check_config() -> bool:
    """
    检查必要配置是否就绪
    """
    print("🔧 Configuration Check:")
    print(f"  SMTP_USER: {'✅ Set' if config.SMTP_USER else '❌ Not set'}")
    print(f"  SMTP_PASSWORD: {'✅ Set' if config.SMTP_PASSWORD else '❌ Not set'}")
    print(f"  RECIPIENT_EMAIL: {config.RECIPIENT_EMAIL}")
    print(f"  NEWSAPI_KEY: {'✅ Set' if config.NEWSAPI_KEY else '⚠️ Not set (news will be limited)'}")
    print(f"  SERVERCHAN_KEY: {'✅ Set' if config.SERVERCHAN_KEY else '⚠️ Not set (WeChat via ServerChan disabled)'}")
    print(f"  WECHAT_WEBHOOK: {'✅ Set' if config.WECHAT_WEBHOOK else '⚠️ Not set (WeChat via Work WeChat disabled)'}")
    print(f"  ENABLE_EMAIL: {config.ENABLE_EMAIL}")
    print(f"  ENABLE_WECHAT: {config.ENABLE_WECHAT}")
    
    if not config.SMTP_USER or not config.SMTP_PASSWORD:
        print("\n⚠️  Warning: Email not fully configured. Set SMTP_USER and SMTP_PASSWORD env vars.")
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="TMT Morning Brief Generator")
    parser.add_argument("--generate-only", action="store_true", help="Only generate, don't send")
    parser.add_argument("--test-email", action="store_true", help="Send test email")
    parser.add_argument("--test-wechat", action="store_true", help="Send test WeChat message")
    parser.add_argument("--dry-run", action="store_true", help="Fetch data but don't render/send")
    parser.add_argument("--check", action="store_true", help="Check configuration")
    
    args = parser.parse_args()
    
    if args.check:
        check_config()
        return
    
    if args.test_email:
        check_config()
        print("\n📧 Sending test email...")
        send_test_email()
        return
    
    if args.test_wechat:
        print("\n💬 Sending test WeChat message...")
        test_wechat()
        return
    
    if args.dry_run:
        print("🔍 Dry run mode - fetching data only...")
        brief_data = fetch_all_data()
        print(f"\n✅ Data fetched: {len(brief_data.get('executive_summary', []))} summary items")
        return
    
    # 正常运行
    check_config()
    generate_and_send_brief(generate_only=args.generate_only)


if __name__ == "__main__":
    main()
