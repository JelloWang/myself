#!/usr/bin/env python3
"""daily-ai-notes 生成器 —— 每天生成一篇 AI 应用实战笔记。

默认用模板 + 当周主题生成一篇结构化的笔记，开箱即用，不需要任何 API key。

想升级成「AI 每天写全新内容」：
  1. 在仓库 Settings -> Secrets and variables -> Actions 里加一个 secret，
     名字叫 OPENAI_API_KEY（或你用的模型 key）
  2. 把这个文件里 `USE_AI = False` 改成 `USE_AI = True`
  3. 补上下面 AI 分支里的调用逻辑即可
"""

import datetime
import os
import re
import sys
from pathlib import Path

# ---- 配置 ----
USE_AI = False          # 想接 AI 生成就改成 True
NOTES_DIR = Path(__file__).resolve().parent.parent / "notes"
TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "template.md"

# 每周轮换的主题（按 ISO 周号取一个）。AI 应用 × FDE 人设。
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
    """按周数轮换主题。第 N 周用 TOPICS[N % len]。"""
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
