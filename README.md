# ai-study

这个仓库用于整理 Python、深度学习、PyTorch、AI Agent 等学习资料和代码实践。

## 仓库内容

### 1. Python 基础

用于学习 Python 基础语法，以及常用第三方库 NumPy、Pandas、Matplotlib 等。

参考资料：

- [PyCharm | 创建你的第一个 Python 项目](https://www.bilibili.com/video/BV1A3411C7oL)
- [北理 Python 数据分析与展示：Numpy、Matplotlib、Pandas](https://www.bilibili.com/video/BV1L64y1X7om)

### 2. fishbook

经典深度学习入门书籍《深度学习入门：基于 Python 的理论与实践》，俗称“鱼书”。

### 3. study_resource

主要根据 B 站“我是小土堆”的 PyTorch 入门教程整理，包含课程源码和练习内容。

参考资料：

- [PyTorch 深度学习快速入门教程：小土堆](https://www.bilibili.com/video/BV1hE411t7RN)

### 4. Python 并发编程实战

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


### 5. FastAPI Web 开发

FastAPI 是一个现代化的 Python Web 框架，常用于快速构建高性能 API 服务。它基于 Python 类型注解进行参数校验、数据转换和接口文档生成，适合用来开发后端接口、机器学习模型服务、数据服务和前后端分离项目。

核心学习内容：

- 路由：定义接口路径，例如 `GET /items`、`POST /users`。
- 请求参数：接收路径参数、查询参数、请求体数据。
- Pydantic：使用数据模型完成参数校验和响应结构定义。
- 依赖注入：把数据库连接、权限校验、公共参数等逻辑拆分复用。
- 异步编程：使用 `async def` 提升 I/O 密集型接口的并发能力。
- ORM：配合数据库完成增删改查。
- 项目拆分：把路由、模型、数据库、业务逻辑拆成更清晰的模块。
- 部署与测试：学习接口测试、服务启动和线上部署流程。

FastAPI 的特点：

- 语法简洁，适合 Python 初学者从 Flask 过渡到现代 Web API 开发。
- 自动生成 Swagger / OpenAPI 文档，方便调试接口。
- 和异步编程结合紧密，适合高并发 API 服务。
- 类型提示友好，能减少参数错误和接口文档维护成本。

参考资源：

- [黑马程序员 PythonWeb 开发：FastAPI 从入门到实战](https://www.bilibili.com/video/BV1zV2QBtE39?vd_source=e2413576ab62a790f6f465afd377f842)


### 6. hello-agents

`hello-agents` 是 Datawhale 开源的 AI Agent 学习资料，已复制到本仓库的 `hello-agents/` 目录中。

原项目地址：

- [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents)

许可证说明：

- 原项目采用 CC BY-NC-SA 4.0 协议，请保留原项目的 `LICENSE.txt` 和来源说明。