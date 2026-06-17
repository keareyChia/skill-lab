# WeChat Article Fetch

一个用于抓取微信公众号文章并转换为 Markdown 的 Skill。

## 1. 这个 Skill 是什么？

`wechat-article-fetch` 专门处理 `mp.weixin.qq.com` 的公众号文章链接。

它解决的问题是：browserless / 浏览器自动化在访问微信公众号文章时，经常被微信拦到“环境异常”验证码页；但很多公开文章用 **iPhone MicroMessenger User-Agent** 直接 HTTP 请求，仍然可以拿到完整 HTML。这个 Skill 把这条可用路径沉淀成稳定流程和脚本。

## 2. 它解决什么问题？

- browserless 打开微信公众号文章时触发 `环境异常` / `去验证`
- 需要把公众号文章正文抓出来给 LLM 阅读、总结或入库
- 需要把公众号文章转换成 Markdown
- 需要在 wiki / Obsidian / 知识库流程中自动保存公众号正文

## 3. 核心思路

1. 使用 iPhone 微信内置浏览器 UA 请求文章 HTML
2. 检查是否被重定向到 `wappoc_appmsgcaptcha`
3. 从 HTML 内联变量提取标题、时间等元数据
4. 从 `#js_content` 提取正文
5. 清理 HTML 标签、实体和重复空行
6. 输出 Markdown 或 JSON

关键 UA：

```text
Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.42
```

## 4. 快速使用

```bash
python3 scripts/wechat_article_fetch.py \
  'https://mp.weixin.qq.com/s/ARTICLE_ID' \
  --out article.md
```

输出 JSON：

```bash
python3 scripts/wechat_article_fetch.py \
  'https://mp.weixin.qq.com/s/ARTICLE_ID' \
  --json
```

也可以读取已经保存的 HTML：

```bash
python3 scripts/wechat_article_fetch.py article.html --out article.md
```

## 5. 输出 Markdown 格式

```markdown
# 文章标题

来源：https://mp.weixin.qq.com/s/...
公众号：公众号名或未提取到
发布时间：2026-06-03 07:00:00
抓取方式：curl/urllib + iPhone MicroMessenger UA

---

正文内容...
```

## 6. 成功和失败判断

成功时脚本退出码为 `0`，并输出类似：

```text
OK title='...' chars=8608 lines=212 out=article.md
```

失败时脚本退出码为 `2`，常见错误：

- `CAPTCHA_OR_ENVIRONMENT_ABNORMAL`：被微信环境验证拦截
- `NO_JS_CONTENT`：页面里没有公众号正文容器
- `EXTRACTED_TEXT_TOO_SHORT`：提取结果过短，可能不是正文
- `FETCH_FAILED`：网络请求失败

## 7. 适用范围

适合：

- 公开微信公众号文章
- `mp.weixin.qq.com/s/...` 链接
- 需要正文文本 / Markdown 的场景

不适合：

- 普通网页通用抓取
- 小红书、抖音、视频号
- 需要登录态、付费、私密或账号权限的微信内容
- 只在微信客户端动态渲染、HTML 里没有 `#js_content` 的页面

## 8. 和 browserless 的关系

这个 Skill 不是替代所有浏览器抓取，而是微信公众号文章的专用 fallback。

推荐路由：

- 微信公众号文章：优先使用本 Skill
- 普通网页：使用通用网页正文提取器或 browserless
- 强登录 / 强风控页面：让用户复制正文或提供安全的授权方式

## 9. 已验证样例

以下文章在 browserless 被验证码拦截后，用本脚本成功抓取：

```text
https://mp.weixin.qq.com/s/q3JDrXeDUUrtzlknw_Ol8g
```

结果：

- 标题：`136k Star！微软开源了一个「AI 喂食工具」——PDF、Word、PPT、Excel、视频、音频一行命令全变 Markdown，LLM 真正读懂你的文档`
- 正文约 8500+ 字
- 212 行
- 发布时间：`2026-06-03 07:00:00`

## 10. 文件结构

```text
wechat-article-fetch/
├── README.md
├── SKILL.md
└── scripts/
    └── wechat_article_fetch.py
```

## 11. 注意事项

- 微信反爬策略可能变化，UA 和提取规则需要维护
- 公众号名有时无法从 HTML 里稳定提取，缺失不代表正文失败
- 图片、视频、小程序卡片不会被完整保留，脚本主要抓文本
- 不要把这个脚本当成通用网页抓取器，它是微信公众号文章专用工具
