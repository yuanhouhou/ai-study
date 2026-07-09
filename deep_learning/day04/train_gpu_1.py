import torchvision
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torch import nn
import torch
import time  
  
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
#神经网络
class Test(nn.Module):
    def __init__(self):
        super(Test,self).__init__()
        self.model = nn.Sequential(
            nn.Conv2d(3,32,5,1,2),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32,32,5,1,2),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32,64,5,1,2),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(1024,64),
            nn.Linear(64,10)
        )

    def forward(self,x):
        x = self.model(x)
        return x
    

test = Test()
test.cuda()

#损失函数
#交叉熵的计算公式为Σp(x)lnq(x)
loss_fn = nn.CrossEntropyLoss()
loss_fn = loss_fn.cuda()

#优化器
learning_rate = 0.01
optimizer = torch.optim.SGD(test.parameters(),learning_rate)

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
        imgs = imgs.cuda()
        targets = targets.cuda()
        outputs = test(imgs)
        loss = loss_fn(outputs,targets)
        #优化器优化模型
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        total_train_step += 1
        if total_train_step % 100 == 0:
            end_time = time.time()
            print("训练时间L:{}".format(end_time-start_time))
            print("训练次数:{},loss:{}".format(total_train_step,loss))
            writer.add_scalar("train_loss",loss,total_train_step)
    #测试步骤开始
    total_test_loss = 0 #测试loss
    total_accurancy = 0 #正确率
    
    with torch.no_grad():
        for data in test_dataloader:
            imgs,targets = data
            imgs = imgs.cuda()
            targets = targets.cuda()
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