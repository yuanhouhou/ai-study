# AGENTS.md

本文件是 `01_GitHub仓库文件/` 的项目级规则。这个目录是用户主要维护并上传到 GitHub 的学习仓库内容。

## 1. README 与文档维护

- 修改或新增本目录下的学习文件后，同步检查 `README.md` 是否需要更新入口、用途、运行方式和学习要点。
- README 重构必须先读当前真实内容，再基于现有栏目重排；不要直接套通用模板。
- 对资源型 README，优先整理为：总览、目录或分区、每节说明、统一资源链接、来源或许可说明。
- 链接应尽量用可读的 Markdown 列表呈现，不要把大量原始 URL 堆在段落里。
- 文档说明应保留来源线索，但不要复制大段原文。

## 2. 学习代码与资料

- 解释 Python、PyTorch、FastAPI 等学习代码时，优先结合当前文件和用户看到的错误，不要只给抽象教程。
- 修改训练脚本时，优先使用可复用的 `device = torch.device(...)` 与 `.to(device)` 模式，避免硬编码 `.cuda()`。
- 新增 FastAPI 示例文件后，同步更新 `fastapi_file/README.md` 的文件清单、目录、运行命令和对应概念说明。
- FastAPI / MySQL / SQLAlchemy 学习任务优先保持用户当前技术路线；不要为了临时跑通而擅自把 MySQL 示例改成 SQLite。
- MySQL ORM 排查按层拆开：本机 MySQL Server 是否启动、Database Client 是否能连接、Python ORM 是否读取到正确 `.env`、脚本是否能完成最小查询。
- SQL 练习脚本可以独立新增，避免强行塞进 Python 文件；新增后说明应在 Database Client 里运行还是在 Python 中运行。
- FastAPI、SQLAlchemy、MySQL 等学习代码可以读取本地配置文件，但不要把真实数据库连接串、密钥或 `.env` 提交到仓库。
- 本目录的本地数据库配置优先放在 `config/.env`、`config/*.local` 或 `config/*.secret`，并保持这些路径被根目录 `.gitignore` 忽略。

## 3. 开源资料与许可证

- `hello-agents/` 来源于 Datawhale 开源学习资料，移动、整理或说明时保留原项目来源和许可证。
- `Claude Code 学习手册/` 来源于开源手册项目，移动、整理或说明时保留原项目来源和许可证。
- 复制、整理第三方内容时，优先保留原 README、LICENSE、来源链接和必要说明。

## 4. 提交前检查

- 提交前确认只包含本目录中需要上传 GitHub 的学习资料和必要说明。
- 不提交本地缓存、虚拟环境、日志、密钥、临时输出和大型数据集。
- 如果用户明确要求上传被忽略的数据或资料，先说明原因和影响，再使用 `git add -f <path>`。
