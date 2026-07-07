# 📊 TMT Morning Brief - 自动化晨报推送

> 面向中国TMT Investment Banker的每日晨报自动化推送方案
> 基于 GitHub Actions + Python，完全免费，零服务器成本

---

## ✨ 功能特点

- **⏰ 定时推送**：每周一至周五早上8:00（北京时间）自动运行
- **📧 邮件推送**：精美HTML邮件，支持Gmail等主流邮箱
- **💬 微信推送**：支持Server酱和企业微信机器人
- **📈 市场行情**：A股/港股/美股主要指数 + 商品/利率/汇率
- **📰 新闻聚合**：全球TMT、中国科技、监管政策、Deal动态
- **💰 Deal Tracker**：IPO/ECM/M&A/私募融资动态
- **🎯 投行视角**：Executive Summary + Banker's Take

---

## 🚀 快速开始（5分钟搞定）

### 第一步：Fork本仓库

1. 点击右上角的 **Fork** 按钮，将本仓库复制到您的GitHub账号下

### 第二步：配置邮件推送（必须）

> 晨报将推送到您的邮箱 **dianeshi0829@gmail.com**

#### Gmail配置（推荐）

1. **开启2步验证**（必须）：
   - 访问 [Google账号安全性](https://myaccount.google.com/security)
   - 开启"两步验证"

2. **创建应用专用密码**：
   - 在同一页面搜索"应用专用密码"
   - 选择"邮件" → 生成16位密码
   - **记录这个密码，后续步骤需要**

3. **设置GitHub Secrets**：
   - 打开您fork的仓库 → **Settings** → **Secrets and variables** → **Actions**
   - 点击 **New repository secret**，依次添加：

| Secret名称 | 值 | 说明 |
|-----------|-----|------|
| `SMTP_USER` | 您的Gmail地址 | 如 `you@gmail.com` |
| `SMTP_PASSWORD` | 应用专用密码 | 刚才生成的16位密码 |
| `RECIPIENT_EMAIL` | `dianeshi0829@gmail.com` | 收件人邮箱 |

> ⚠️ **重要**：不要使用您的Gmail登录密码，必须使用"应用专用密码"

### 第三步：配置NewsAPI（强烈推荐）

NewsAPI提供高质量的新闻数据，免费版每天100次请求。

1. 访问 [NewsAPI.org](https://newsapi.org/register) 免费注册
2. 获取API Key
3. 在GitHub Secrets中添加：

| Secret名称 | 值 |
|-----------|-----|
| `NEWSAPI_KEY` | 您的NewsAPI Key |

### 第四步：配置微信推送（可选）

#### 方案A：Server酱（推送到个人微信）

1. 访问 [Server酱](https://sct.ftqq.com/) 扫码登录
2. 复制 **SendKey**
3. 在GitHub Secrets中添加 `SERVERCHAN_KEY`

#### 方案B：企业微信机器人（推送到工作群）

1. 在企业微信群 → 群设置 → 添加群机器人
2. 复制Webhook地址
3. 在GitHub Secrets中添加 `WECHAT_WEBHOOK`

### 第五步：激活定时任务

1. 在您fork的仓库中，进入 **Actions** 标签页
2. 点击 **"I understand my workflows, go ahead and enable them"**
3. 工作流已激活！每天早8点会自动运行

### 第六步：立即测试

手动触发一次测试：
1. 进入仓库 → **Actions** → **TMT Morning Brief**
2. 点击 **Run workflow** → 选择分支 → **Run workflow**
3. 等待约2-3分钟，检查您的邮箱

---

## 📋 完整的Secrets配置参考

| Secret | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `SMTP_USER` | ✅ | - | 发件邮箱（Gmail地址） |
| `SMTP_PASSWORD` | ✅ | - | 邮箱应用专用密码 |
| `RECIPIENT_EMAIL` | ✅ | - | 收件人邮箱 |
| `SMTP_HOST` | ❌ | smtp.gmail.com | SMTP服务器 |
| `SMTP_PORT` | ❌ | 587 | SMTP端口 |
| `NEWSAPI_KEY` | ❌ | - | 新闻API密钥 |
| `SERVERCHAN_KEY` | ❌ | - | Server酱SendKey |
| `WECHAT_WEBHOOK` | ❌ | - | 企业微信机器人Webhook |
| `ENABLE_EMAIL` | ❌ | true | 是否启用邮件 |
| `ENABLE_WECHAT` | ❌ | false | 是否启用微信 |

---

## 📁 项目结构

```
tmt-morning-brief/
├── .github/
│   └── workflows/
│       └── morning-brief.yml    # GitHub Actions定时工作流
├── config.py                    # 配置文件（从环境变量读取）
├── data_fetcher.py              # 数据获取模块
├── email_template.py            # HTML邮件模板渲染
├── email_sender.py              # 邮件发送模块
├── wechat_notifier.py           # 微信推送模块
├── main.py                      # 主入口脚本
├── requirements.txt             # Python依赖
├── README.md                    # 本文档
└── output/                      # 生成的晨报文件（自动创建）
```

---

## 🔧 本地运行调试

### 安装依赖

```bash
pip install -r requirements.txt
```

### 设置环境变量

```bash
# 必需
export SMTP_USER="your_email@gmail.com"
export SMTP_PASSWORD="your_app_password"
export RECIPIENT_EMAIL="dianeshi0829@gmail.com"

# 强烈推荐
export NEWSAPI_KEY="your_newsapi_key"

# 可选（微信推送）
export SERVERCHAN_KEY="your_serverchan_key"
# 或
export WECHAT_WEBHOOK="your_wechat_webhook_url"
```

### 运行命令

```bash
# 生成并推送晨报
python main.py

# 仅生成，不推送
python main.py --generate-only

# 发送测试邮件
python main.py --test-email

# 发送测试微信
python main.py --test-wechat

# 仅获取数据（调试）
python main.py --dry-run

# 检查配置
python main.py --check
```

---

## 📊 晨报内容结构

| # | 板块 | 说明 |
|---|------|------|
| 1 | 🔥 Executive Summary | 5条市场要闻，含Capital Market Impact |
| 2 | 📈 Capital Market Dashboard | A股/港股/美股指数 + 商品/利率/汇率 |
| 3 | 📋 Regulatory Update | 中国及香港监管政策动态 |
| 4 | 🌍 Global TMT Headlines | 全球科技行业要闻 |
| 5 | 🇨🇳 China TMT Headlines | 中国科技行业要闻 |
| 6 | 💰 Deal Tracker | IPO/ECM/M&A/私募融资动态 |
| 7 | 📊 Sector Watch | 3个热门行业追踪 |
| 8 | 📑 Research Highlights | 卖方研究观点摘要 |
| 9 | ⏰ Upcoming Catalysts | 未来7天关键事件 |
| 10 | 💡 Banker's Take | 投行观点 |

---

## 🌐 数据源

| 类别 | 数据源 | 费用 |
|------|--------|------|
| A股行情 | 东方财富API | 免费 |
| 港股/美股行情 | Yahoo Finance API | 免费 |
| 全球新闻 | NewsAPI | 免费（100次/天） |
| 监管政策 | NewsAPI聚合 | 免费 |
| Deal数据 | NewsAPI聚合 | 免费 |

---

## ⚠️ 常见问题

### Q: 邮件发送失败，提示认证错误
A: Gmail必须使用"应用专用密码"，不是您的登录密码。开启2步验证后，在Google账号安全性页面创建。

### Q: 新闻内容不够丰富
A: 免费版NewsAPI有每日100次请求限制。建议注册获取API Key，新闻质量和数量会显著提升。

### Q: 可以推送到多个邮箱吗？
A: 可以修改 `config.py` 中的 `RECIPIENT_EMAIL` 为逗号分隔的多个地址，或修改 `email_sender.py` 支持多收件人。

### Q: 微信推送没有收到
A: 
- Server酱：检查SendKey是否正确，免费版每天限5条
- 企业微信：检查Webhook地址是否正确，机器人是否在群内

### Q: 定时任务没有按时运行
A: GitHub Actions的定时任务可能有15分钟延迟，属正常现象。如需精确时间，建议使用外部定时服务触发workflow webhook。

### Q: 可以自定义晨报内容吗？
A: 可以修改 `config.py` 中的 `SECTIONS` 字典来启用/禁用特定板块，或修改 `data_fetcher.py` 添加自定义数据源。

---

## 🔒 隐私与安全

- 所有敏感信息（密码、API Key）均存储在GitHub Secrets中，不会暴露在代码里
- 晨报数据来源于公开API，不包含任何非公开信息
- 邮件内容仅发送给配置的收件人

---

## 📜 开源协议

MIT License - 可自由修改和分发

---

## 💡 进阶建议

1. **添加Capital IQ数据**：手动导出Capital IQ数据上传，脚本会自动识别并标注来源
2. **自定义行业关注**：修改 `NEWS_QUERIES` 添加您关注的特定行业或公司
3. **增加数据源**：可接入东方财富公告API、港交所披露易等增强Deal Tracker
4. **部署到自己的服务器**：如果有云服务器，可用 `cron` 替换GitHub Actions实现更精确的控制

---

> 📧 **推送地址**: dianeshi0829@gmail.com  
> 🕒 **推送时间**: 周一至周五 08:00 (北京时间)  
> 🔄 **版本**: v1.0 | 基于 tmt-ib-morning-brief skill
