#!/usr/bin/env python3
"""Fetch a WeChat Official Account article and convert it to Markdown.

Usage:
    python3 wechat_article_fetch.py URL_OR_HTML_FILE --out article.md
    python3 wechat_article_fetch.py URL_OR_HTML_FILE --json

The default network path uses an iPhone MicroMessenger User-Agent because
browser automation from data-center IPs often triggers WeChat's environment
captcha page.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import html as _html
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

WECHAT_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 "
    "MicroMessenger/8.0.42"
)

DEFAULT_HEADERS = {
    "User-Agent": WECHAT_UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://mp.weixin.qq.com/",
}

BLOCK_END_TAGS = r"p|section|div|h[1-6]|li|blockquote|tr|table"


def _js_string_var(html_text: str, name: str) -> str:
    patterns = [
        rf"var\s+{re.escape(name)}\s*=\s*'([^']*)'",
        rf'var\s+{re.escape(name)}\s*=\s*"([^"]*)"',
    ]
    for pattern in patterns:
        match = re.search(pattern, html_text)
        if match:
            return _html.unescape(match.group(1)).strip()
    return ""


def fetch_html(url: str, timeout: int = 45) -> tuple[str, str, int | None]:
    req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        charset = resp.headers.get_content_charset() or "utf-8"
        return raw.decode(charset, "ignore"), resp.geturl(), getattr(resp, "status", None)


def read_source(source: str) -> tuple[str, str, int | None]:
    if source.startswith(("http://", "https://")):
        return fetch_html(source)
    path = Path(source)
    return path.read_text(encoding="utf-8", errors="ignore"), str(path), None


def extract_content_html(html_text: str) -> str | None:
    """Extract the inner-ish HTML of #js_content.

    WeChat content has nested div/section tags, so a naive first </div> match is
    too short. Prefer the known following blocks/scripts as boundaries.
    """
    match = re.search(
        r'<div[^>]+id=["\']js_content["\'][^>]*>(.*?)(?:<div[^>]+id=["\']js_sg_bar["\']|<script[^>]+nonce|<script\b)',
        html_text,
        re.S | re.I,
    )
    if match:
        return match.group(1)

    # Fallback: locate opening tag and take a generous slice until footer-ish area.
    start = re.search(r'<div[^>]+id=["\']js_content["\'][^>]*>', html_text, re.S | re.I)
    if not start:
        return None
    tail = html_text[start.end() :]
    end = re.search(r'<div[^>]+id=["\']js_sg_bar["\']|<script\b', tail, re.S | re.I)
    return tail[: end.start()] if end else tail


def html_fragment_to_text(fragment: str) -> str:
    # Preserve block boundaries before stripping tags.
    fragment = re.sub(r"<br\s*/?>", "\n", fragment, flags=re.I)
    fragment = re.sub(rf"</({BLOCK_END_TAGS})\s*>", "\n", fragment, flags=re.I)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    text = _html.unescape(fragment)
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)

    clean_lines: list[str] = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if clean_lines and clean_lines[-1] == line:
            continue
        clean_lines.append(line)
    return "\n".join(clean_lines).strip()


def timestamp_to_local(ct: str) -> str:
    if not ct or not ct.isdigit():
        return ""
    # Use the machine's local timezone, matching normal Hermes terminal output.
    return _dt.datetime.fromtimestamp(int(ct)).strftime("%Y-%m-%d %H:%M:%S")


def build_markdown(result: dict[str, Any]) -> str:
    title = result.get("title") or "微信公众号文章"
    author = result.get("author") or "未提取到"
    publish_time = result.get("publish_time") or "未提取到"
    url = result.get("url") or result.get("final_url") or ""
    text = result.get("text") or ""
    return (
        f"# {title}\n\n"
        f"来源：{url}\n"
        f"公众号：{author}\n"
        f"发布时间：{publish_time}\n"
        f"抓取方式：curl/urllib + iPhone MicroMessenger UA\n\n"
        f"---\n\n"
        f"{text}\n"
    )


def extract(source: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "ok": False,
        "url": source,
        "final_url": "",
        "status": None,
        "title": "",
        "author": "",
        "publish_time": "",
        "ct": "",
        "char_count": 0,
        "line_count": 0,
        "text": "",
        "markdown": "",
        "error": None,
    }

    try:
        html_text, final_url, status = read_source(source)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        result["error"] = f"FETCH_FAILED: {exc}"
        return result

    result["final_url"] = final_url
    result["status"] = status

    if "wappoc_appmsgcaptcha" in final_url or ("环境异常" in html_text and "id=\"js_content\"" not in html_text):
        result["error"] = "CAPTCHA_OR_ENVIRONMENT_ABNORMAL"
        return result

    result["title"] = _js_string_var(html_text, "msg_title")
    result["author"] = _js_string_var(html_text, "nickname")
    result["ct"] = _js_string_var(html_text, "ct")
    result["publish_time"] = _js_string_var(html_text, "publish_time") or timestamp_to_local(result["ct"])

    content_html = extract_content_html(html_text)
    if not content_html:
        result["error"] = "NO_JS_CONTENT"
        return result

    text = html_fragment_to_text(content_html)
    result["text"] = text
    result["char_count"] = len(text)
    result["line_count"] = len(text.splitlines()) if text else 0

    if result["char_count"] < 100:
        result["error"] = "EXTRACTED_TEXT_TOO_SHORT"
        return result

    result["ok"] = True
    result["markdown"] = build_markdown(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="WeChat article URL or saved HTML file")
    parser.add_argument("--out", help="Write Markdown to this file")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown/status")
    args = parser.parse_args()

    result = extract(args.source)

    if args.out and result.get("markdown"):
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(result["markdown"], encoding="utf-8")

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result["ok"]:
        if not args.out:
            print(result["markdown"])
        print(
            f"OK title={result['title']!r} chars={result['char_count']} "
            f"lines={result['line_count']} out={args.out or '<stdout>'}",
            file=sys.stderr,
        )
    else:
        print(f"ERROR {result['error']}", file=sys.stderr)
        if result.get("final_url"):
            print(f"final_url={result['final_url']}", file=sys.stderr)

    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
