# daily-ai-notes

每天一篇 AI 应用实战笔记，由 GitHub Actions 每天早上自动生成并提交。
方向：AI 应用开发 × 目标 FDE（Forward Deployed Engineer）。

## 怎么运作

- 每天 UTC 0:00（北京时间 8:00），GitHub Actions 运行 `scripts/generate.py`
- 从 `templates/template.md` 生成一篇当天的笔记，写到 `notes/YYYY-MM-DD.md`
- 主题按周轮换（见 `generate.py` 里的 TOPICS）
- 提交后你可以在仓库里看到每天新增的文章，绿色贡献格子也会持续变绿

## 手动测试

在仓库的 Actions 页面点 **Run workflow** 立即跑一次。

## 想升级成 AI 每天写全新内容？

默认是模板生成（稳定、免费、无需 key）。想接入 AI：

1. 仓库 Settings → Secrets → 新建 `OPENAI_API_KEY`
2. `scripts/generate.py` 里把 `USE_AI = False` 改成 `True`
3. 在 AI 分支接上你的模型调用
