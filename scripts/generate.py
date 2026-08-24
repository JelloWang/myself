#!/usr/bin/env python3
"""daily-ai-notes v2 — 抓 AI 新闻 + AI 点评，生成每日日报。"""

import datetime
import json
import os
import urllib.request
from pathlib import Path
from xml.etree import ElementTree

NOTES_DIR = Path(__file__).resolve().parent.parent / "notes"

RSS_FEEDS = [
    "https://hnrss.org/newest?q=AI&count=10",
    "https://hnrss.org/newest?q=LLM&count=8",
    "https://hnrss.org/newest?q=OpenAI&count=6",
]
MAX_ITEMS = 12


def fetch_rss(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "daily-ai-notes/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        root = ElementTree.fromstring(data)
        items = []
        for item in root.iter("item"):
            t = item.find("title")
            l = item.find("link")
            if t is not None and t.text:
                link = l.text.strip() if l is not None and l.text else ""
                items.append((t.text.strip(), link))
        return items
    except Exception as e:
        print(f"[warn] 抓取失败 {url}: {e}")
        return []


def collect_news():
    seen, news = set(), []
    for feed in RSS_FEEDS:
        for title, link in fetch_rss(feed):
            k = title.lower()
            if k in seen:
                continue
            seen.add(k)
            news.append((title, link))
    return news[:MAX_ITEMS]


def ai_summarize(news):
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    news_text = "\n".join(f"- {t} ({l})" for t, l in news)
    prompt = (
        "你是一位专注 AI 应用落地的技术博主，正在成长为 Forward Deployed Engineer（FDE）。"
        "下面是今天的一批 AI 新闻标题。请你：\n"
        "1. 挑出最值得关注的 3-5 条\n"
        "2. 每条用一两句话点评它对 AI 应用落地/企业实践的意义（有你自己的观点）\n"
        "3. 最后写一段 100 字左右的『今日思考』，站在 FDE 视角谈趋势\n"
        "用中文，markdown 格式，专业但不啰嗦。\n\n"
        f"今日新闻：\n{news_text}"
    )
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }).encode("utf-8")
    try:
        req = urllib.request.Request(
            f"{base_url}/chat/completions", data=payload,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[warn] AI 调用失败，降级为纯摘要: {e}")
        return None


def build_markdown(news, ai_content):
    date = datetime.date.today().isoformat()
    lines = [f"# AI 应用日报 — {date}", ""]
    if ai_content:
        lines += [ai_content, "", "---", "", "## 📰 今日新闻原文链接", ""]
    else:
        lines += ["> 今日 AI 领域值得关注的新闻（自动抓取）", ""]
    for title, link in news:
        lines.append(f"- [{title}]({link})" if link else f"- {title}")
    lines += ["", "---", "*自动生成 · 一个未来 FDE 的 AI 应用日报*"]
    return "\n".join(lines)


def main():
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    news = collect_news()
    if not news:
        print("[error] 没抓到新闻，跳过")
        return
    print(f"抓到 {len(news)} 条新闻")
    ai_content = ai_summarize(news)
    md = build_markdown(news, ai_content)
    date = datetime.date.today().isoformat()
    out = NOTES_DIR / f"{date}.md"
    out.write_text(md, encoding="utf-8")
    print(f"已生成: {out}")


if __name__ == "__main__":
    main()
