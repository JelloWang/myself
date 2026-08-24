#!/usr/bin/env python3
"""daily-ai-notes 生成器 —— 每天生成一篇 AI 应用实战笔记。"""

import datetime
from pathlib import Path

NOTES_DIR = Path(__file__).resolve().parent.parent / "notes"
TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "template.md"

TOPICS = [
    "用 LLM 做一个自动化的信息汇总工作流",
    "RAG：给你的知识库一个会说话的入口",
    "Agent 如何拆解一个真实业务任务",
    "把大模型接进你现有的业务系统",
    "Prompt 工程：从聊天到可复用的系统提示",
    "FDE 视角：到客户现场部署 AI 的一天",
    "用 GitHub Actions 让 AI 自动干活",
]


def pick_topic():
    week = datetime.date.today().isocalendar()[1]
    return TOPICS[week % len(TOPICS)]


def generate_from_template(topic):
    content = TEMPLATE.read_text(encoding="utf-8")
    content = content.replace("{{DATE}}", datetime.date.today().isoformat())
    content = content.replace("{{TOPIC}}", topic)
    return content


def main():
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    topic = pick_topic()
    content = generate_from_template(topic)
    today = datetime.date.today().isoformat()
    out = NOTES_DIR / f"{today}.md"
    if out.exists():
        print(f"{out} already exists, skipping")
        return
    out.write_text(content, encoding="utf-8")
    print(f"Generated: {out}")


if __name__ == "__main__":
    main()
