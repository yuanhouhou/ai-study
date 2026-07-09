import torchvision
from torch.utils.data import DataLoader
from model import *
from torch.utils.tensorboard import SummaryWriter
import time
# 定义设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("使用设备: {}".format(device))

train_data = torchvision.datasets.CIFAR10(root=r"E:\vscode_project\python_study\deeplearning_file\study_resourece\cifar-10-python",train=True,transform=torchvision.transforms.ToTensor(),download=True)

test_data = torchvision.datasets.CIFAR10(root=r"E:\vscode_project\python_study\deeplearning_file\study_resourece\cifar-10-python",train=False,transform=torchvision.transforms.ToTensor(),download=True)

#测试集长度
train_data_size = len(train_data)
test_data_size = len(test_data)
print("训练数据集的长度:{}".format(train_data_size))
print("测试数据集的长度:{}".format(test_data_size))

#用dataloader加载数据集
train_dataloader = DataLoader(train_data,batch_size=64)
test_dataloader = DataLoader(test_data,batch_size=64)

#创建网络模型
test = Test().to(device)

#损失函数
#交叉熵的计算公式为Σp(x)lnq(x)
loss_fn = nn.CrossEntropyLoss()

#优化器
learning_rate = 0.001
optimizer = torch.optim.Adam(test.parameters(), lr=learning_rate)

#设置训练网络参数
total_train_step = 0 #训练次数
total_test_step = 0 #测试次数
epoch = 10 #训练轮数


#加入tensorboard
start_time = time.time()
writer = SummaryWriter("logs_test_train")

for  i in range(10):
    print("-------第{}轮训练开始-----".format(i+1))
    
    #训练
    for data in train_dataloader:
        imgs,targets = data
        imgs = imgs.to(device)
        targets = targets.to(device)
        outputs = test(imgs)
        loss = loss_fn(outputs,targets)
        #优化器优化模型
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        total_train_step += 1
        if total_train_step % 100 == 0:
            endtime = time.time()
            print("训练时间:{}".format(endtime-start_time))
            print("训练次数:{},loss:{}".format(total_train_step,loss))
            writer.add_scalar("train_loss",loss,total_train_step)
    #测试步骤开始
    total_test_loss = 0 #测试loss
    total_accurancy = 0 #正确率
    
    with torch.no_grad():
        for data in test_dataloader:
            imgs,targets = data
            imgs = imgs.to(device)
            targets = targets.to(device)
            outputs = test(imgs)
            loss = loss_fn(outputs,targets)
            total_test_loss += loss.item()
            accurancy = (outputs.argmax(1) == targets).sum()
            total_accurancy += accurancy
            
    print("整体数据集上的loss:{}".format(total_test_loss))
    print("整体数据集上的正确率:{}".format(total_accurancy / test_data_size))
    writer.add_scalar("test_loss",total_test_loss,total_test_step)
    writer.add_scalar("test_accurancy",total_accurancy / test_data_size,total_test_step)
    total_test_step += 1
    
    torch.save(test,"test_{}.pth".format(i))
    print("模型已保存")
writer.close()