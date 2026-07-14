# AGENTS.md

本文件记录本仓库中 Codex 后续协作时应遵循的项目级规则。规则来自本仓库近期会话复盘，重点服务于 Windows / VS Code / Python 学习仓库、Git/GitHub 操作、README 整理、skill 检索和本地文件整理任务。

## 1. 默认沟通风格

- 默认使用中文回答配置、工具链、README、学习路线、文件整理和 Git 问题；用户切换语言时跟随用户。
- 用户问“这是什么问题”、发截图或贴报错时，先给一句清晰的 plain-language 诊断，再给检查步骤和解决办法。
- 对 Git、CLI、扩展配置、环境检查等问题，优先给手把手步骤，并用简短中文解释关键命令含义。
- 术语解释要贴近用户当前屏幕、当前文件或当前命令；先讲可用例子，再补充概念。
- 复杂学习主题应按阶段组织：每阶段说明学什么、练什么、如何判断能否进入下一阶段。

## 2. 读取与修改文件

- 修改或解释本仓库文件前，先读取真实文件内容，不要凭记忆或模板直接改。
- 中文 Markdown、README、配置说明等文本文件优先用 UTF-8 读取，避免 PowerShell 默认编码导致乱码。
- 编辑文件前简要说明将改什么；涉及较大改动时先给结构化方案。
- 不要覆盖或回滚用户已有改动。遇到未预期的本地变更，先判断是否相关；相关时顺着现状处理，无关时忽略。
- 本地生成的复盘、缓存、日志、数据集等不应随手纳入版本控制；先检查 `.gitignore` 是否已有对应规则。

## 3. Git 与 GitHub

- Git 操作前先检查状态：`git status --short --branch`。需要诊断历史时再查 `git log --oneline --decorate --max-count=5`、`git rev-parse HEAD`、`git reflog`。
- 提交前避免宽泛使用 `git add -A`；优先按用户目标定向 staged，确认不会带入无关文件。
- 用户明确要上传被 `.gitignore` 忽略的路径时，优先说明并使用 `git add -f <path>`，不要为了单次上传反复改 `.gitignore`。
- 遇到 VS Code Git 弹窗，尤其是 `cannot lock ref 'HEAD'` 或旧 hash 相关提示，先验证 `HEAD`、`origin/main`、`reflog`，不要直接建议 reset 或修历史。
- 如果本地与远程已经对齐，优先把 VS Code Git 弹窗解释为 Source Control stale 状态，并建议刷新 Source Control 或执行 `Developer: Reload Window`。
- GitHub 上传大文件前先测量文件大小：浏览器上传受 25 MiB 单文件限制，GitHub 仓库单文件上限通常为 100 MiB。
- GitHub 网络失败时，先区分直连、代理、repo-local Git config 和系统网络设置。修改代理配置时明确说明变更范围。

## 4. 网络、代理与系统范围

- 涉及网络、代理、Git config、系统配置时，必须说明改动是项目级、仓库级、用户级还是机器级。
- GitHub 连接失败时，优先用 PowerShell 检查：`Test-NetConnection github.com -Port 443`。
- 如果需要设置 Git 代理，优先使用仓库级 `.git/config`，并告诉用户这不会修改系统网络设置。
- 不要把当前机器上的代理端口、认证状态或远程状态当成永久事实；执行前重新检查。

## 5. Windows 文件整理任务

- 对桌面、下载目录、班级资料等有副作用的文件整理任务，先确认路径和当前状态，再执行移动、重命名或删除。
- 如果用户要求“开始前先总结”，必须先列出工作步骤和影响范围。
- 批量整理默认按人名或对象分组，保留可见状态标签，例如 `(empty)`、`(no-cover)`、文件数量等。
- 脚本被中断、用户改变要求或前一次尝试失败后，必须重新检查部分执行状态，再只处理剩余工作。
- 批量移动和重命名后生成报告或映射文件，避免终端换行导致结果难审计。
- 若用户提供应用快捷方式路径，优先使用该路径，不要先大范围搜索安装目录。

## 6. VS Code、扩展与 CLI 排查

- 检查工具是否“配置好”时，分开汇报：VS Code 扩展是否安装、终端 CLI 是否在 PATH、配置目录是否存在、版本命令是否能运行。
- Git for VS Code 问题要说明：VS Code 使用系统 Git，不是把 Git 装在 VS Code 里面。
- Windows 普通 Intel/AMD 机器安装 Git 时，默认推荐 Git for Windows x64 Standalone Installer；安装后重启 VS Code，再检查 `git --version` 和 `where.exe git`。
- 对 Codex、Claude Code、Copilot 等工具能力差异，按实际工作流说明，不用产品宣传式语言。

## 7. README、Markdown 与内容系统

- README 重构必须先读当前真实内容，再基于现有栏目重排；不要直接套通用模板。
- 对资源型 README，优先整理为：总览、目录或分区、每节说明、统一资源链接、来源或许可说明。
- 链接应尽量用可读的 Markdown 列表呈现，不要把大量原始 URL 堆在段落里。
- 文档说明应保留来源线索，但不要复制大段原文。
- 如果 README/Markdown 排版 skill 找不到，应尽快转为 GitHub Markdown 的标题、列表、链接等通用规范，不要在 skill 搜索上耗太久。

## 8. Skill 检索与能力扩展

- 用户要求查找 skill 时，先读取相关 skill 的 `SKILL.md`，再执行检索。
- Windows 下多次运行 `npx skills find` 时，为每个主题使用独立 repo-local cache，例如 `.npm-cache-<query>`，避免默认缓存冲突。
- 本地 registry 精确词无结果时，尽快扩展到相邻概念，并补充 skills.sh、GitHub 等候选来源。
- skill 发现类回答应比较多个候选项的特点、适用场景和安装方式，让用户决定下一步。
- 不要因为某次查询无结果，就把“没有相关 skill”当成永久事实。

## 9. Python 与学习代码

- 解释 Python、PyTorch、FastAPI 等学习代码时，优先结合当前文件和用户看到的错误，不要只给抽象教程。
- 修改训练脚本时，优先使用可复用的 `device = torch.device(...)` 与 `.to(device)` 模式，避免硬编码 `.cuda()`。
- 讲解 tensor shape、训练流程、依赖注入、异步同步等概念时，至少给一个贴近当前代码的小例子。
- 运行或建议测试前，先看项目现有结构；只运行与当前任务相关的最小验证。

## 10. 安全边界

- 不要复现日志里的隐私内容、密钥、长对话原文或内部推理。
- 搜索会话历史或日志时，优先使用摘要、索引、元数据和关键词片段；不要整文件载入大型 session 文件。
- 涉及删除、批量移动、重置历史、覆盖文件等高风险操作时，必须确认目标路径和影响范围。
- 对从记忆或旧会话得来的事实，如版本号、远程状态、代理、认证状态等，执行前重新验证。

## 11. 会话复盘与风格档案维护

- 维护 `Codex会话复盘与个人风格档案.md` 时，优先使用可用的记忆索引、rollout summary、元数据和相关片段；不要整文件载入大型 `sessions/*.jsonl`。
- 复盘内容应按任务类型沉淀“问题做法、正确做法、适用场景”，并去重合并相近规则。
- 更新规则时保留日期范围或任务类型作为来源线索，但不要复现原始日志、隐私内容、密钥、长对话原文或内部 reasoning。
- 如果用户要求把复盘档案也上传到 GitHub，注意该文件当前被 `.gitignore` 忽略，需要明确说明并使用 `git add -f`。
- 长期规则是否加入用户级 AGENTS.md 需要单独询问；不要因为项目级复盘而擅自修改全局用户规则。

## 12. FastAPI、数据库与本地配置

- FastAPI、SQLAlchemy、MySQL 等学习代码可以读取 repo-local 配置文件，但不要把真实数据库连接串、密钥或 `.env` 提交到仓库。
- 本仓库的本地数据库配置优先放在 `config/.env`、`config/*.local` 或 `config/*.secret`，并保持这些路径被 `.gitignore` 忽略。
- 解释或修改 FastAPI / ORM 示例时，先结合当前文件说明启动流程、连接串来源、建表逻辑和最小验证方式。
- 提交数据库学习代码时，只提交源码、示例说明和 ignore 规则；真实连接配置留在本机。
