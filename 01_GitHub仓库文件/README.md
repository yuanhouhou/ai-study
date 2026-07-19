# ai-study

这个仓库用于整理 Python、深度学习、PyTorch、FastAPI、AI Agent、Claude Code 等学习资料和代码实践。

> PDF 文件如果无法在 GitHub 在线预览，可以下载到本地查看。

## 目录

- [仓库导航](#仓库导航)
- [Python 基础](#python-基础)
- [fishbook](#fishbook)
- [PyTorch 学习资料](#pytorch-学习资料)
- [Python 并发编程实战](#python-并发编程实战)
- [MySQL 数据库学习资料](#mysql-数据库学习资料)
- [FastAPI Web 开发](#fastapi-web-开发)
- [hello-agents](#hello-agents)
- [Claude Code 学习手册](#claude-code-学习手册)
- [来源与许可证](#来源与许可证)

## 仓库导航

| 目录 | 内容 |
| --- | --- |
| `deep_learning/` | Python、深度学习相关练习代码 |
| `fishbook/` | 《深度学习入门：基于 Python 的理论与实践》相关资料 |
| `study_resourece/` | PyTorch 入门课程资料和练习内容 |
| `process_thread_coroutine/` | 多线程、多进程、协程、异步 IO 学习内容 |
| `mysql/` | MySQL 数据库课程资料包和内容笔记 |
| `fastapi_file/` | FastAPI 后端开发学习代码和笔记 |
| `hello-agents/` | Datawhale AI Agent 开源学习资料 |
| `Claude Code 学习手册/` | Claude Code 学习手册 PDF 和配套 README |

## Python 基础

用于学习 Python 基础语法，以及常用第三方库 NumPy、Pandas、Matplotlib 等。

参考资料：

- [PyCharm | 创建你的第一个 Python 项目](https://www.bilibili.com/video/BV1A3411C7oL)
- [北理 Python 数据分析与展示：Numpy、Matplotlib、Pandas](https://www.bilibili.com/video/BV1L64y1X7om)

## fishbook

经典深度学习入门书籍《深度学习入门：基于 Python 的理论与实践》，俗称“鱼书”。

主要用于配合深度学习基础概念、神经网络、误差反向传播、卷积神经网络等内容学习。

## PyTorch 学习资料

`study_resourece/` 主要根据 B 站“我是小土堆”的 PyTorch 入门教程整理，包含课程源码和练习内容。

参考资料：

- [PyTorch 深度学习快速入门教程：小土堆](https://www.bilibili.com/video/BV1hE411t7RN)

## Python 并发编程实战

大模型 API 调用通常是 IO 密集型任务，掌握并发和异步编程非常重要。

核心知识点：

- 多线程
- 多进程
- 协程
- 异步 IO
- 线程池
- 进程池

参考资料：

- [Python 并发编程实战](https://www.bilibili.com/video/BV1bK411A7tV)

## MySQL 数据库学习资料

`mysql/` 用于整理 MySQL 数据库课程资料和内容笔记，适合配合后续 FastAPI、数据分析、后端接口开发学习。

这个目录包含：

- `MYSQL内容笔记.md`：根据 MySQL 课程 PDF 整理的结构化学习笔记
- `Mysql数据库.zip`：原始课程资料压缩包

核心学习内容：

- SQL 分类与基本 `SELECT` 查询
- 运算符、过滤条件、排序和分页
- 多表查询、连接、`UNION`
- 单行函数、聚合函数、`GROUP BY`、`HAVING`
- 子查询、数据库和表的创建管理
- 数据插入、更新、删除和视图
- 触发器、存储过程、存储函数
- 评价问题基础和数据分析扩展

## FastAPI Web 开发

`fastapi_file/` 用于记录 FastAPI 后端开发的学习代码和笔记。

FastAPI 是一个现代化的 Python Web 框架，常用于快速构建高性能 API 服务。它基于 Python 类型注解进行参数校验、数据转换和接口文档生成，适合开发后端接口、机器学习模型服务、数据服务和前后端分离项目。

核心学习内容：

- 路由：定义接口路径，例如 `GET /items`、`POST /users`
- 请求参数：接收路径参数、查询参数、请求体数据
- Pydantic：使用数据模型完成参数校验和响应结构定义
- 依赖注入：把数据库连接、权限校验、公共参数等逻辑拆分复用
- 异步编程：使用 `async def` 提升 I/O 密集型接口的并发能力
- 中间件：为请求前后添加统一处理逻辑
- ORM：配合数据库完成增删改查
- 项目拆分：把路由、模型、数据库、业务逻辑拆成更清晰的模块

FastAPI 的特点：

- 语法简洁，适合 Python 初学者从 Flask 过渡到现代 Web API 开发
- 自动生成 Swagger / OpenAPI 文档，方便调试接口
- 和异步编程结合紧密，适合高并发 API 服务
- 类型提示友好，能减少参数错误和接口文档维护成本

参考资源：

- [黑马程序员 PythonWeb 开发：FastAPI 从入门到实战](https://www.bilibili.com/video/BV1zV2QBtE39?vd_source=e2413576ab62a790f6f465afd377f842)

## hello-agents

`hello-agents/` 是 Datawhale 开源的 AI Agent 学习资料，已复制到本仓库中。

它适合用来了解 AI Agent 的基本概念、任务规划、工具调用、多 Agent 协作等内容。

原项目地址：

- [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents)

## Claude Code 学习手册

`Claude Code 学习手册/` 来自开源项目 `603419608/claude-code-learning-handbook`，已复制到本仓库中，方便集中管理 AI 编程工具相关学习资料。

这个目录包含：

- `README.md`：手册介绍、适合读者、完整目录
- `books/Claude Code 学习手册.pdf`：中文 PDF 版本
- `books/Claude Code Learning Handbook.pdf`：英文 PDF 版本
- `LICENSE`：原项目许可证

适合学习的内容包括：

- Claude Code 和普通聊天机器人的区别
- 代码阅读、Bug 修复、重构、测试和文档工作流
- Markdown 记忆系统、提示词工程、上下文和 Token 管理
- Skills、SubAgents、Hooks、MCP、Plugins 等扩展系统
- GitHub PR、CI、安全权限和自动化工作流

原项目地址：

- [603419608/claude-code-learning-handbook](https://github.com/603419608/claude-code-learning-handbook)

## 来源与许可证

本仓库包含自写学习笔记，也包含复制整理的开源学习资料。使用、传播或二次整理时，请注意保留原项目来源和许可证说明。

- `hello-agents/` 来源于 [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents)，请保留原项目的 `LICENSE.txt` 和来源说明。
- `Claude Code 学习手册/` 来源于 [603419608/claude-code-learning-handbook](https://github.com/603419608/claude-code-learning-handbook)，请保留原项目的 `LICENSE` 和来源说明。
