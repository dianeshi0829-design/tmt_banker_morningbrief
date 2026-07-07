"""
TMT Morning Brief - Email Sender
通过SMTP发送HTML邮件晨报
"""
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional

import config


def send_brief_email(
    html_content: str,
    text_content: Optional[str] = None,
    subject: Optional[str] = None,
    recipient: Optional[str] = None,
    sender: Optional[str] = None,
    smtp_host: Optional[str] = None,
    smtp_port: Optional[int] = None,
    smtp_password: Optional[str] = None,
) -> bool:
    """
    发送晨报邮件
    
    Args:
        html_content: HTML格式邮件正文
        text_content: 纯文本备份（可选）
        subject: 邮件主题（可选，默认自动生成）
        recipient: 收件人邮箱（默认从config读取）
        sender: 发件人邮箱（默认从config读取）
        smtp_host: SMTP服务器地址
        smtp_port: SMTP端口
        smtp_password: SMTP密码/应用专用密码
    
    Returns:
        bool: 发送是否成功
    """
    # 使用配置默认值
    recipient = recipient or config.RECIPIENT_EMAIL
    sender = sender or config.SMTP_USER
    smtp_host = smtp_host or config.SMTP_HOST
    smtp_port = smtp_port or config.SMTP_PORT
    smtp_password = smtp_password or config.SMTP_PASSWORD
    
    if not all([sender, smtp_password, recipient]):
        print("[Email Error] 缺少邮件配置: 请检查 SMTP_USER, SMTP_PASSWORD, RECIPIENT_EMAIL 环境变量")
        return False
    
    if not subject:
        today = datetime.now().strftime("%Y-%m-%d")
        weekday = datetime.now().strftime("%a")
        subject = f"📊 TMT Morning Brief | {today} ({weekday}) | Daily IB Intelligence"
    
    # 构建邮件
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"TMT Morning Brief <{sender}>"
    msg["To"] = recipient
    
    # 添加纯文本版本（fallback）
    if text_content:
        msg.attach(MIMEText(text_content, "plain", "utf-8"))
    
    # 添加HTML版本
    msg.attach(MIMEText(html_content, "html", "utf-8"))
    
    # 发送邮件
    try:
        context = ssl.create_default_context()
        
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls(context=context)
            server.login(sender, smtp_password)
            server.sendmail(sender, [recipient], msg.as_string())
        
        print(f"[Email Sent] 晨报邮件已发送至 {recipient}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("[Email Error] SMTP认证失败: 请检查邮箱地址和密码/应用专用密码")
        print("  Gmail用户提示: 需要使用'应用专用密码'而非登录密码")
        print("  设置步骤: Google账号 → 安全性 → 2步验证 → 应用专用密码")
        return False
    except smtplib.SMTPConnectError:
        print(f"[Email Error] 无法连接SMTP服务器 {smtp_host}:{smtp_port}")
        return False
    except Exception as e:
        print(f"[Email Error] 邮件发送失败: {e}")
        return False


def send_test_email() -> bool:
    """
    发送测试邮件（用于验证配置）
    """
    html = """<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family: Arial, sans-serif; padding: 20px;">
<h2>✅ TMT Morning Brief - 邮件配置测试</h2>
<p>这是一封测试邮件，用于验证您的邮件发送配置是否正确。</p>
<p>如果您收到这封邮件，说明晨报推送功能已就绪！</p>
<hr>
<p style="color: #666; font-size: 12px;">TMT Morning Brief Automation</p>
</body>
</html>"""
    
    return send_brief_email(
        html_content=html,
        subject="📧 TMT Morning Brief - 邮件配置测试",
    )


if __name__ == "__main__":
    # 测试发送
    print("测试邮件发送...")
    print(f"SMTP_HOST: {config.SMTP_HOST}")
    print(f"SMTP_PORT: {config.SMTP_PORT}")
    print(f"SMTP_USER: {config.SMTP_USER}")
    print(f"RECIPIENT: {config.RECIPIENT_EMAIL}")
    
    if not config.SMTP_USER:
        print("\n请先设置环境变量:")
        print("  export SMTP_USER=your_email@gmail.com")
        print("  export SMTP_PASSWORD=your_app_password")
        print("  export RECIPIENT_EMAIL=dianeshi0829@gmail.com")
    else:
        send_test_email()
