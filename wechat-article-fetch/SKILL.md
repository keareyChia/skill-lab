---
name: wechat-article-fetch
description: Use when fetching WeChat Official Account articles from mp.weixin.qq.com links without browserless. Provides a curl/urllib + iPhone MicroMessenger UA workflow, extraction script, validation checks, and fallbacks for captcha/anti-bot cases.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wechat, mp.weixin, article, fetch, markdown, ingestion]
    related_skills: [wiki-ingest]
---

# WeChat Article Fetch

## Overview

This skill captures the working non-browser approach for extracting WeChat Official Account articles (`https://mp.weixin.qq.com/s/...`). Browserless/browser automation often lands on WeChat's `环境异常` captcha page, especially from data-center IPs without residential proxy. In practice, direct HTTP fetching with a mobile WeChat User-Agent can still return the full article HTML for many public article URLs.

The core workflow is:

1. Fetch article HTML with an iPhone `MicroMessenger` User-Agent.
2. Verify the response is a real article, not a captcha/interstitial page.
3. Extract metadata from inline JavaScript variables.
4. Extract the readable body from `#js_content`.
5. Convert the result into Markdown suitable for LLM ingestion or wiki storage.

## When to Use

Use this skill when:

- The user provides a `mp.weixin.qq.com/s/...` or `mp.weixin.qq.com/s?__biz=...` article link and asks to fetch, save, summarize, or ingest it.
- `browser_navigate` opens a WeChat captcha page (`环境异常`, `去验证`, `wappoc_appmsgcaptcha`).
- You need a reusable script for WeChat article → Markdown conversion.
- A wiki-ingest flow needs the full article body rather than just the URL.

Do not use this skill for:

- Private/account-gated WeChat content that requires the user's logged-in cookies.
- WeChat articles that intentionally block unauthenticated access.
- Mini-program pages, WeChat Channels video pages, or comment/paywall-only content.

## Quick Start

Run the bundled script:

```bash
python3 scripts/wechat_article_fetch.py \
  'https://mp.weixin.qq.com/s/q3JDrXeDUUrtzlknw_Ol8g' \
  --out /tmp/article.md
```

Expected success signal:

```text
OK title='...' chars=8608 lines=212 out=/tmp/article.md
```

If the response is blocked, the script exits non-zero and reports a clear reason such as `CAPTCHA_OR_ENVIRONMENT_ABNORMAL` or `NO_JS_CONTENT`.

## Design

### Why not browserless first?

WeChat applies aggressive environment checks. In Browserbase/browserless without residential proxy, public article URLs can be redirected to:

```text
https://mp.weixin.qq.com/mp/wappoc_appmsgcaptcha?poc_token=...&target_url=...
```

The rendered page usually contains only:

- `环境异常`
- `去验证`
- an iframe verification challenge

That proves the browser itself works, but the environment is not trusted by WeChat.

### Why direct HTTP can work

Many WeChat public article pages still include the article HTML in the initial response when requested with a plausible mobile WeChat UA. The key UA marker is `MicroMessenger/...`.

Recommended UA:

```text
Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.42
```

Fetch headers:

```text
User-Agent: <above>
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Referer: https://mp.weixin.qq.com/
```

### Extraction model

Metadata is usually present in inline JavaScript variables:

- `var msg_title = '...'`
- `var nickname = "..."` (sometimes missing/obfuscated)
- `var ct = "1780441200"` Unix timestamp
- `var publish_time = "..."` when available

Body content is inside:

```html
<div id="js_content" ...> ... </div>
```

The robust extractor should:

1. Locate the opening `#js_content` div.
2. Stop near the following script or `#js_sg_bar` block.
3. Convert `<br>`, `</p>`, `</section>`, `</div>`, `</li>`, headings, and blockquotes to newlines before stripping tags.
4. HTML-unescape entities (`&nbsp;`, `&amp;`, etc.).
5. Normalize spaces and blank lines.
6. Remove adjacent duplicate lines.

## Script Contract

The bundled `scripts/wechat_article_fetch.py` supports:

```bash
python3 scripts/wechat_article_fetch.py URL_OR_HTML_FILE [--out article.md] [--json]
```

Outputs Markdown by default. With `--json`, outputs structured JSON:

```json
{
  "ok": true,
  "url": "https://mp.weixin.qq.com/s/...",
  "title": "...",
  "author": "...",
  "publish_time": "2026-06-03 07:00:00",
  "ct": "1780441200",
  "char_count": 8608,
  "line_count": 212,
  "text": "...",
  "markdown": "...",
  "error": null
}
```

## Validation Checklist

After fetching, verify:

- Response status is HTTP 200.
- Final URL is not `/mp/wappoc_appmsgcaptcha`.
- HTML does not contain `环境异常` without `id="js_content"`.
- HTML contains `id="js_content"`.
- Extracted body has a meaningful length, usually > 500 Chinese characters for a normal article.
- The title matches the user-provided article title, when known.
- Markdown file starts with `# {title}` and includes the original source URL.

## Fallback Ladder

1. **Direct fetch with MicroMessenger UA** — this skill's default path.
2. **Try another mobile WeChat UA** — e.g. newer `MicroMessenger/8.0.49` or Android WeChat UA.
3. **Search title for mirrors/reposts** — useful when WeChat blocks the exact URL.
4. **Ask user to forward/copy article content from mobile WeChat** — safest for hard-blocked articles.
5. **Use authenticated cookies only if the user explicitly provides them** — warn about account/security risks; never invent or request broad credentials casually.

## Wiki Ingest Integration

For WikiLei-style ingestion, write the generated Markdown to:

```text
/opt/data/wiki/_inbox/fetched/mp.weixin.qq.com/{article_slug}/article.md
```

Recommended front matter/body shape:

```markdown
# {title}

来源：{url}
公众号：{author or 未提取到}
发布时间：{publish_time or 未提取到}
抓取方式：curl/urllib + iPhone MicroMessenger UA

---

{article_text}
```

Then append to `/opt/data/wiki/log.md`:

```markdown
## [YYYY-MM-DD] ingest | {title}
- source: {url}
- stored: _inbox/fetched/mp.weixin.qq.com/{article_slug}/article.md
- status: 待归位
```

## Common Pitfalls

1. **Assuming browserless failure means the article cannot be fetched.** Browserless may hit captcha while direct mobile-UA HTTP succeeds.

2. **Using a desktop UA.** Desktop or generic curl UA is more likely to trigger interstitials or return unusable HTML.

3. **Regex that stops at the first `</div>`.** WeChat article content contains nested divs/sections. Stop near `#js_sg_bar` or a following script block instead.

4. **Flattening all whitespace into one paragraph.** Convert block tags to newlines before stripping HTML, otherwise tables/lists/headings become unreadable.

5. **Treating missing author as failure.** `nickname` can be absent even when title/body/timestamp are valid.

6. **Forgetting HTML entity decoding.** WeChat text often contains `&nbsp;`; run `html.unescape`.

7. **Not checking captcha markers.** Always detect `环境异常`, `wappoc_appmsgcaptcha`, and missing `#js_content` before claiming success.

## Known Working Example

The URL below was successfully fetched via direct HTTP after browserless was blocked by captcha:

```text
https://mp.weixin.qq.com/s/q3JDrXeDUUrtzlknw_Ol8g
```

Observed result:

- Title: `136k Star！微软开源了一个「AI 喂食工具」——PDF、Word、PPT、Excel、视频、音频一行命令全变 Markdown，LLM 真正读懂你的文档`
- Body length: 8608 chars
- Lines: 212
- Timestamp extracted from `ct`: `2026-06-03 07:00:00`
- Author: not extracted from the HTML used in that run

## Verification Command

A quick smoke test:

```bash
python3 scripts/wechat_article_fetch.py \
  'https://mp.weixin.qq.com/s/q3JDrXeDUUrtzlknw_Ol8g' \
  --json | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["ok"], d["char_count"], d["title"][:20])'
```

Expected shape:

```text
True 8608 136k Star！微软开源了一个
```
