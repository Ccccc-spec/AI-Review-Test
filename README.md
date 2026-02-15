# AI PR Review

基于大语言模型的 GitHub Pull Request 自动代码审查。在 PR 打开或更新时，自动获取改动 Diff，调用 AI 进行审查，并将结果以评论形式发布到 PR 中。

## 功能特性

- **自动触发**：PR 打开（`opened`）或同步更新（`synchronize`）时自动运行
- **基于最终 Diff**：针对 PR 的汇总改动进行审查，忽略中间已修复的问题
- **多模型容错**：优先使用 Gemini 系列模型，失败时自动尝试备用模型
- **评论去重**：每次运行前清理旧的 AI 评论，只保留最新一条

审查维度包括：

- 逻辑缺陷（边界条件、内存泄漏、死锁等）
- 性能优化
- 安全性（注入、敏感信息、鉴权等）
- 可维护性（命名、复杂度、Clean Code）

## 工作流程

1. 开发者创建或更新 PR
2. GitHub Actions 触发 `AI PR Review` workflow
3. 拉取代码、安装依赖，执行 `scripts/ai_review.py`
4. 脚本获取 PR 的完整 Diff，调用 OpenRouter API（Gemini 等模型）生成审查建议
5. 将带 `## AI Code Review` 标记的评论发布到该 PR

## 配置说明

### 1. 启用 GitHub Actions

将本仓库中的 `workflows/ai-review.yml` 复制到你的仓库的 `.github/workflows/` 目录下（例如 `.github/workflows/ai-review.yml`），这样 PR 触发时才会运行。

### 2. 仓库 Secrets

在 GitHub 仓库 **Settings → Secrets and variables → Actions** 中配置：

| Secret 名称     | 说明 |
|----------------|------|
| `GITHUB_TOKEN` | 一般无需手动添加，Actions 运行时会自动注入；需保证 workflow 有 `pull-requests: write` 权限（已配置） |
| `LLM_API_KEY`  | [OpenRouter](https://openrouter.ai/) 的 API Key，用于调用大模型 |

### 3. 获取 LLM API Key

1. 打开 [OpenRouter](https://openrouter.ai/)
2. 注册/登录后，在 API Keys 页面创建 Key
3. 将 Key 填入仓库的 `LLM_API_KEY` Secret

脚本当前使用的模型（按优先级）：`google/gemini-2.0-flash-001`、`google/gemini-2.0-flash-thinking-exp:free`、`google/gemini-flash-1.5`，均通过 OpenRouter 调用。

## 本地运行（可选）

仅用于调试脚本逻辑，不会真正发评论到 GitHub（需自行准备测试用 repo/pr/token）。

```bash
# 依赖
pip install openai requests

# 环境变量
export REPO="owner/repo"
export PR_NUMBER="1"
export GITHUB_TOKEN="ghp_xxx"
export LLM_API_KEY="sk-or-xxx"

python scripts/ai_review.py
```

## 项目结构

```
workflows/
  ai-review.yml      # PR 触发、Python 环境与依赖、调用 ai_review.py（使用前需放到 .github/workflows/）
scripts/
  ai_review.py       # 拉取 Diff、调用 OpenRouter、清理旧评论、发布新评论
PR-TEST/             # 示例/测试用目录
README.md
```

## 依赖

- Python 3.11
- `openai`（兼容 OpenRouter API）
- `requests`