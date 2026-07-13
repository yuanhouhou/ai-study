本仓库默认使用中文回答配置、工具链、README 和学习路线问题，除非用户切换语言。
- 修改或解释本仓库文件前，先读取真实文件内容；中文文件优先 UTF-8。
- Git 操作必须先检查 `git status --short --branch`，提交前避免宽泛 `git add -A`，优先按用户目标定向 staged。
- 不要重置或覆盖用户已有改动；遇到 VS Code Git 弹窗先验证 `HEAD` / `origin/main` / `reflog`。
- 涉及网络、代理、Git config、系统配置时，明确说明变更范围是项目级、仓库级还是机器级。
- Windows 文件整理任务要先确认路径、总结步骤、输出报告，并在中断后重新检查状态。
- skill 检索任务先用可用 skill/工具，Windows 下使用独立 `.npm-cache-*` 缓存；无结果时及时转为候选资源比较。