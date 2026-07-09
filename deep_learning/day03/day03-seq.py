from torch import nn
from torch.nn import Conv2d,MaxPool2d,Flatten,Linear
import torch
import torchvision

datasets = torchvision.datasets.CIFAR10(root=r"E:\vscode_project\python_study\deeplearning_file\study_resourece\cifar-10-python",train=False,transform=torchvision.transforms.ToTensor(),download=True)
dataloader = torch.utils.data.DataLoader(datasets,batch_size=32)

class Test2(nn.Module):
    def __init__(self):
        super(Test2,self).__init__()
        self.sequential = nn.Sequential(
            Conv2d(3,32,5,padding=2),
            MaxPool2d(2),
            Conv2d(32,32,5,padding=2),
            MaxPool2d(2), 
            Conv2d(32,64,5,padding=2),
            MaxPool2d(2),
            Flatten(),
            Linear(1024,64),
            Linear(64,10)
        )
    
    def forward(self,x):
        x = self.sequential(x)
        return x


test2 = Test2()
loss_cross = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(test2.parameters(),lr=0.001)
for epoch in range(2):
    running_loss = 0.0
    for data in dataloader:
        imgs,targets = data
        output = test2(imgs)
        result_loss = loss_cross(output,targets)
        optimizer.zero_grad()
        result_loss.backward()
        optimizer.step()
        running_loss = running_loss + result_loss
    print(running_loss)
