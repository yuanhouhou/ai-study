# Python 并发编程总结

这个目录主要围绕 Python 并发编程学习，涉及：

- `blog_craw.py`：同步爬虫函数，负责请求网页和解析文章标题。
- `tread_pool.py`：使用 `ThreadPoolExecutor` 做并发爬虫。
- `tread_process_cpu_bound.py`：对比单线程、多线程、多进程执行 CPU 密集型任务。
- `flask_thread_pool.py`：在 Flask Web 服务中使用线程池并发处理 I/O 操作。
- `flask_process_pool.py`：在 Flask Web 服务中使用进程池处理质数判断。
- `lock.py`：演示多线程共享变量时为什么需要加锁。

> 注意：文件名里的 `tread` 应该是 `thread` 的拼写误差，但不影响运行。

## 1. 为什么要引入并发编程

引入并发编程，核心目标是：

> 提高程序运行速度，尤其是减少等待时间。

典型场景：

- 网络爬虫：顺序下载可能花 1 小时，引入并发后可能降到 20 分钟。
- Web 应用：一个页面加载涉及文件、数据库、远程 API，顺序处理可能 3 秒，并发处理可能 200 毫秒级。
- 后台服务：大量用户同时访问时，需要同时处理多个请求。

程序提速大致有几类方法：

| 方法 | 含义 | Python 常见方式 |
|---|---|---|
| 单线程串行 | 一个任务做完再做下一个 | 普通函数调用 |
| 多线程并发 | 一个进程里多个线程一起处理任务 | `threading` / `ThreadPoolExecutor` |
| 多 CPU 并行 | 多个 CPU 核心真正同时计算 | `multiprocessing` / `ProcessPoolExecutor` |
| 多机器并行 | 多台机器一起处理任务 | 分布式系统 |

## 2. CPU 密集型和 I/O 密集型

学习并发之前，要先判断任务类型。

### 2.1 CPU 密集型

CPU 密集型，也叫计算密集型。

特点是：

- 大部分时间 CPU 都在计算。
- I/O 等待很少。
- CPU 使用率通常较高。

例子：

- 压缩、解压缩。
- 加密、解密。
- 正则表达式大量搜索。
- 图像处理。
- 判断大数是不是质数。

本目录里的例子：

```python
def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True
```

这个函数在不断做取模计算，属于 CPU 密集型任务。

### 2.2 I/O 密集型

I/O 密集型指程序大部分时间在等待外部输入输出。

特点是：

- CPU 很多时候是空闲的。
- 程序经常等磁盘、网络、数据库、远程 API。
- CPU 使用率通常不高。

例子：

- 文件读写。
- 网络爬虫。
- 数据库查询。
- 请求远程服务 API。

本目录里的例子：

```python
def craw(url):
    r = requests.get(url)
    return r.text
```

`requests.get(url)` 大部分时间是在等网络返回，所以它属于 I/O 密集型。

## 3. Python 对并发编程的支持

Python 常见并发工具：

| 工具 | 模块 | 适合场景 |
|---|---|---|
| 多线程 | `threading` | I/O 密集型任务 |
| 多进程 | `multiprocessing` | CPU 密集型任务 |
| 异步 I/O | `asyncio` | 大量 I/O 并发任务 |
| 线程池 | `ThreadPoolExecutor` | 简化线程任务提交、等待和结果获取 |
| 进程池 | `ProcessPoolExecutor` | 简化进程任务提交、等待和结果获取 |
| 锁 | `Lock` | 保护共享变量，避免线程安全问题 |
| 队列 | `Queue` | 在线程或进程之间传递数据 |
| 子进程 | `subprocess` | 启动外部程序并与其输入输出交互 |

## 4. 进程、线程、协程对比

一句话理解：

> 进程是资源分配单位，线程是进程里的执行单位，协程是线程里由程序主动切换的轻量任务。

| 对比项 | 多进程 Process | 多线程 Thread | 多协程 Coroutine |
|---|---|---|---|
| 常用模块 | `multiprocessing` | `threading` | `asyncio` |
| 资源占用 | 最大 | 较小 | 最小 |
| 是否共享内存 | 默认不共享 | 共享同一进程内存 | 共享同一线程内存 |
| 调度者 | 操作系统 | 操作系统 | 程序事件循环 |
| 优点 | 可以利用多核 CPU，真正并行 | 创建轻量，适合 I/O 并发 | 切换成本低，适合超大量 I/O |
| 缺点 | 创建和通信成本高 | CPU 密集型受 GIL 限制 | 需要异步库支持，代码写法更复杂 |
| 适合 | CPU 密集型计算 | I/O 密集型任务 | 大量 I/O 任务 |

结构关系：

```text
一个程序
  可以启动多个进程

一个进程
  可以启动多个线程

一个线程
  可以运行多个协程
```

## 5. Python 为什么有时慢

相对 C/C++/Java，Python 在一些场景下确实更慢，常见原因有两个：

### 5.1 动态类型语言，边解释边执行

Python 是动态类型语言，运行时需要做更多解释和类型判断。

例如：

```python
x = 1
x = "hello"
```

变量类型可以变化，解释器运行时要处理更多信息。

### 5.2 GIL 限制多线程 CPU 并行

GIL 全称是 Global Interpreter Lock，中文常叫全局解释器锁。

它的含义是：

> 在 CPython 解释器中，同一时刻通常只有一个线程在执行 Python 字节码。

所以即使你的电脑有多个 CPU 核心，Python 多线程在 CPU 密集型任务里也不一定能变快。

这就是为什么：

- I/O 密集型：多线程通常有用。
- CPU 密集型：多线程可能没用，甚至更慢。
- CPU 密集型想利用多核：通常用多进程。

## 6. 为什么 Python 要有 GIL

简单理解：

> Python 早期为了简化内存管理和线程同步，引入了 GIL，现在已经很难完全去掉。

Python 对象的内存管理大量依赖引用计数。

例如两个线程都引用同一个对象 `obj`，内部引用计数可能要变化：

```text
线程 A 引用 obj -> ref_count + 1
线程 B 引用 obj -> ref_count + 1
线程 A 释放 obj -> ref_count - 1
线程 B 释放 obj -> ref_count - 1
```

如果多个线程同时修改引用计数，就容易出错。GIL 用一个全局锁简化了这类问题。

代价是：CPU 密集型多线程不能充分利用多核。

## 7. 多线程 threading

多线程适合 I/O 密集型任务，因为等待 I/O 的时候，线程可以让出 CPU，让其他线程继续执行。

比如爬虫：

```text
线程 1 请求网页 A -> 等网络
线程 2 请求网页 B -> 等网络
线程 3 请求网页 C -> 等网络
```

虽然 GIL 限制了 CPU 计算并行，但 I/O 等待期间线程可以切换，所以整体能提速。

### 7.1 单线程和多线程的区别

单线程：

```python
for url in blog_craw.urls:
    blog_craw.craw(url)
```

执行方式：

```text
请求第 1 个网页 -> 等完成
请求第 2 个网页 -> 等完成
请求第 3 个网页 -> 等完成
```

多线程：

```python
t = threading.Thread(target=blog_craw.craw, args=(url,))
t.start()
t.join()
```

含义：

- `Thread(...)`：创建线程任务。
- `start()`：启动线程。
- `join()`：等待线程结束。

## 8. 线程安全和 Lock

线程安全指：

> 某个函数或变量在多线程环境中被同时调用或修改时，仍然能得到正确结果。

如果多个线程同时修改共享变量，可能出现不可预测结果。

例如账户余额：

```python
if account.balance >= amount:
    account.balance -= amount
```

假设余额是 1000，两个线程都取 800。如果没有锁，两个线程可能同时看到余额足够，然后都扣钱，导致结果错误。

### 8.1 Lock 的两种写法

写法一：`try-finally`

```python
lock.acquire()
try:
    # do something
finally:
    lock.release()
```

写法二：`with lock`

```python
with lock:
    # do something
```

推荐使用第二种，因为更简洁，也不容易忘记释放锁。

本目录 `lock.py` 使用的是：

```python
with lock:
    if account.balance >= amount:
        time.sleep(0.1)
        account.balance -= amount
```

`with lock:` 保护的是临界区，也就是不能被多个线程同时执行的代码。

## 9. 线程池 ThreadPoolExecutor

线程池的核心思想：

> 提前准备一批线程，任务来了就交给已有线程处理，避免反复创建和销毁线程。

线程生命周期大致是：

```text
新建 -> 就绪 -> 运行 -> 阻塞 -> 就绪 -> 运行 -> 终止
```

线程池的好处：

- 减少大量新建和终止线程的开销。
- 重用线程资源。
- 控制线程数量，避免无限创建线程导致系统压力过大。
- 代码比手动创建线程更简洁。

### 9.1 `map` 用法

本目录 `tread_pool.py`：

```python
with concurrent.futures.ThreadPoolExecutor() as pool:
    htmls = pool.map(blog_craw.craw, blog_craw.urls)
    htmls = list(zip(blog_craw.urls, htmls))
```

含义：

- 把 `blog_craw.urls` 里的每个 URL 交给 `blog_craw.craw`。
- 线程池并发执行多个请求。
- `pool.map` 返回的结果顺序和输入顺序一致。

### 9.2 `submit` 用法

```python
future = pool.submit(blog_craw.parse, html)
futures[future] = url
```

含义：

- `submit` 提交一个任务。
- 返回 `future` 对象。
- `future.result()` 可以拿到任务执行结果。

这个写法适合需要记录“哪个任务对应哪个 URL”的场景。

## 10. Web 服务为什么适合并发

Web 服务基本结构：

```text
浏览器
  -> Web 服务器 Flask/Django
      -> 磁盘文件
      -> 数据库
      -> 远程 API
  <- 返回响应
```

Web 后台服务的特点：

- 响应时间要求高，比如希望 200ms 返回。
- 经常依赖 I/O 操作，比如磁盘、数据库、远程 API。
- 经常要处理大量用户的同时请求。

所以 Web 服务非常适合使用并发。

## 11. Flask 中使用线程池

本目录 `flask_thread_pool.py`：

```python
app = flask.Flask(__name__)
pool = ThreadPoolExecutor()
```

创建 Flask 应用和线程池。

```python
@app.route("/")
def index():
    result_file = pool.submit(read_file)
    result_db = pool.submit(read_db)
    result_api = pool.submit(read_api)

    return json.dumps({
        "result_file": result_file.result(),
        "result_db": result_db.result(),
        "result_api": result_api.result()
    })
```

`@app.route("/")` 的意思是：

> 当浏览器访问首页 `/` 时，Flask 调用下面的 `index()` 函数。

在 `index()` 中：

- `read_file()` 模拟读取磁盘文件，耗时 0.1 秒。
- `read_db()` 模拟读取数据库，耗时 0.2 秒。
- `read_api()` 模拟请求远程 API，耗时 0.3 秒。

如果串行执行，总耗时约：

```text
0.1 + 0.2 + 0.3 = 0.6 秒
```

如果线程池并发执行，总耗时接近最慢的那个：

```text
约 0.3 秒
```

这就是线程池对 I/O 型 Web 请求的加速效果。

## 12. 多进程 multiprocessing

有了多线程，为什么还要多进程？

因为遇到 CPU 密集型任务时，多线程会受到 GIL 限制，甚至可能因为线程切换开销导致更慢。

对于 CPU 密集型任务，多进程更适合：

- 每个进程有自己的 Python 解释器和 GIL。
- 多个进程可以在多个 CPU 核心上真正并行。
- 适合大计算任务。

但多进程也有成本：

- 创建进程比创建线程更重。
- 进程之间默认不共享普通变量。
- 参数和结果需要序列化、反序列化。
- Windows 下创建子进程成本更明显。

所以多进程不一定永远更快。只有当任务数量足够多、单个任务计算量足够大时，多进程优势才明显。

## 13. 线程和进程写法对比

| 语法条目 | 多线程 | 多进程 |
|---|---|---|
| 引入模块 | `from threading import Thread` | `from multiprocessing import Process` |
| 新建任务 | `t = Thread(target=func, args=(100,))` | `p = Process(target=func, args=(100,))` |
| 启动 | `t.start()` | `p.start()` |
| 等待结束 | `t.join()` | `p.join()` |
| 队列通信 | `queue.Queue()` | `multiprocessing.Queue()` |
| 加锁 | `threading.Lock()` | `multiprocessing.Lock()` |
| 池化工具 | `ThreadPoolExecutor` | `ProcessPoolExecutor` |

池化工具对比：

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor() as executor:
    results = executor.map(func, [1, 2, 3])
```

```python
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor() as executor:
    results = executor.map(func, [1, 2, 3])
```

两个 API 很像，区别在于底层一个用线程，一个用进程。

## 14. CPU 密集型实验：单线程、多线程、多进程

本目录 `tread_process_cpu_bound.py`：

```python
PRIMES = [11227253509529] * 100
```

这里准备了 100 个质数判断任务。

```python
def single_thread():
    for n in PRIMES:
        is_prime(n)
```

单线程是顺序执行。

```python
def multi_thread():
    with ThreadPoolExecutor() as pool:
        pool.map(is_prime, PRIMES)
```

多线程会并发提交任务，但因为 `is_prime` 是 CPU 密集型，受 GIL 影响，不一定更快。

```python
def multi_process():
    with ProcessPoolExecutor() as pool:
        pool.map(is_prime, PRIMES)
```

多进程更适合这个任务，因为多个进程可以利用多核 CPU。

不过建议显式消费结果：

```python
def multi_process():
    with ProcessPoolExecutor() as pool:
        return list(pool.map(is_prime, PRIMES))
```

否则学习计时时容易误解任务是否被完整执行。

## 15. Flask 中使用进程池

本目录 `flask_process_pool.py`：

```python
app = flask.Flask(__name__)
```

创建 Flask 应用。

```python
@app.route("/is_prime/<numbers>")
def api_is_prime(numbers):
    number_list = [int(x) for x in numbers.split(",")]
    results = pool.map(is_prime, number_list)
    return json.dumps(dict(zip(number_list, results)))
```

`@app.route("/is_prime/<numbers>")` 表示动态路由。

例如访问：

```text
http://127.0.0.1:5000/is_prime/7,11,12
```

此时：

```python
numbers == "7,11,12"
```

然后：

```python
number_list = [int(x) for x in numbers.split(",")]
```

得到：

```python
[7, 11, 12]
```

再交给进程池判断是否为质数：

```python
results = pool.map(is_prime, number_list)
```

返回结果类似：

```json
{"7": true, "11": true, "12": false}
```

这里用进程池，是因为质数判断属于 CPU 密集型计算。

## 16. 协程 asyncio

协程适合大量 I/O 并发任务。

核心语法：

```python
async def task():
    await something()
```

重要概念：

- `async def`：定义协程函数。
- `await`：等待异步操作，同时让出执行权。
- `asyncio.create_task()`：创建协程任务。
- `asyncio.gather()`：并发等待多个任务完成。

协程和线程的区别：

- 线程由操作系统调度。
- 协程由程序的事件循环调度。
- 协程切换成本更低。
- 协程需要异步库支持，例如网络请求通常要用 `aiohttp`，不能直接用阻塞式 `requests` 获得真正异步效果。

适合协程的场景：

- 高并发网络请求。
- 爬虫。
- WebSocket。
- 大量远程 API 调用。

## 17. 如何选择并发方案

### 17.1 I/O 密集型

优先选择：

```text
线程池 或 协程
```

例如：

- `blog_craw.py`
- `tread_pool.py`
- `flask_thread_pool.py`

如果代码使用同步阻塞库，比如 `requests`，线程池更直接。

如果使用异步库，比如 `aiohttp`，协程更合适。

### 17.2 CPU 密集型

优先选择：

```text
进程池
```

例如：

- `tread_process_cpu_bound.py`
- `flask_process_pool.py`

质数判断、大量计算、图像处理这类任务更适合多进程。

### 17.3 有共享变量

重点考虑：

```text
Lock / Queue / 避免共享状态
```

例如：

- 多线程修改账户余额要用 `Lock`。
- 多线程/多进程传递数据可以用 `Queue`。

## 18. 本目录代码对应关系

| 文件 | 主题 | 适合说明 |
|---|---|---|
| `blog_craw.py` | 网络请求和 HTML 解析 | I/O 密集型任务 |
| `tread_pool.py` | 线程池爬虫 | `ThreadPoolExecutor.map` / `submit` |
| `lock.py` | 线程安全 | `threading.Lock` |
| `tread_process_cpu_bound.py` | 质数计算 | CPU 密集型，多进程更适合 |
| `flask_thread_pool.py` | Flask + 线程池 | Web 服务中并发处理多个 I/O |
| `flask_process_pool.py` | Flask + 进程池 | Web 服务中处理 CPU 密集型计算 |

## 19. 一句话总结

- 并发编程的目标是提升程序运行速度，尤其是减少等待时间。
- I/O 密集型任务适合多线程或协程。
- CPU 密集型任务适合多进程。
- Python 多线程受 GIL 影响，不适合 CPU 密集型加速。
- 线程池和进程池可以简化任务提交、等待和结果获取。
- 共享变量一定要注意线程安全，必要时使用 `Lock`。
- Web 服务天然适合并发，因为它经常同时面对大量请求和大量 I/O 操作。
