"""
CIFAR-10 数据集下载脚本
========================
由于直接从多伦多大学下载经常超时，推荐手动下载后本地加载。

手动下载步骤（只需做一次）：
  1. 用浏览器/迅雷/IDM 打开：
     https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
     （文件约 170MB）
  2. 将下载的 cifar-10-python.tar.gz 放到 data/ 目录下
  3. 解压到当前文件夹，
     确保出现 data/cifar-10-batches-py/ 这个目录
  4. 运行本脚本即可

pip 清华镜像（安装 torchvision 时用）：
    pip install torchvision -i https://pypi.tuna.tsinghua.edu.cn/simple/
"""
import os
import tarfile
import torchvision

DATA_ROOT = "../data"

# ==============================================
# 如果需要自动解压（当你手动下载了 tar.gz 但还没解压时）
# ==============================================
TAR_PATH = os.path.join(DATA_ROOT, "cifar-10-python.tar.gz")
EXTRACT_DIR = os.path.join(DATA_ROOT, "cifar-10-batches-py")

if os.path.exists(TAR_PATH) and not os.path.exists(EXTRACT_DIR):
    print("检测到 cifar-10-python.tar.gz，正在解压...")
    with tarfile.open(TAR_PATH, "r:gz") as tar:
        tar.extractall(path=DATA_ROOT, filter="data")  # 兼容 Python 3.12+
    print("解压完成！")
    os.remove(TAR_PATH)  # 解压后删除压缩包省空间
    print(f"已删除 {TAR_PATH}")

# ==============================================
# 加载数据集（download=False，不联网）
# ==============================================
DATA_EXISTS = os.path.isdir(EXTRACT_DIR)

if DATA_EXISTS:
    print("本地数据已就绪，直接加载...")
    train_set = torchvision.datasets.CIFAR10(
        root=DATA_ROOT, train=True, download=False
    )
    test_set = torchvision.datasets.CIFAR10(
        root=DATA_ROOT, train=False, download=False
    )
else:
    print("=" * 60)
    print("未找到本地数据！请先手动下载：")
    print()
    print("  1. 用浏览器打开：")
    print("     https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz")
    print()
    print("  2. 下载后把 cifar-10-python.tar.gz 放到：")
    print(f"     {os.path.abspath(DATA_ROOT)}")
    print()
    print("  3. 重新运行本脚本，会自动解压并加载")
    print("=" * 60)
    exit(1)

# ==============================================
# 输出数据集信息
# ==============================================
print(f"训练集大小: {len(train_set)}")
print(f"测试集大小: {len(test_set)}")
print(f"类别数: {len(train_set.classes)}")
print(f"类别名: {train_set.classes}")
