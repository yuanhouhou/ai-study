#relu降低灰度 sigmoid降低对比度
import torch
import torch.nn as nn
from   torch.utils.tensorboard import SummaryWriter
import torchvision

datasets = torchvision.datasets.CIFAR10(root=r"E:\vscode_project\python_study\deeplearning_file\study_resourece\cifar-10-python",train=False,transform=torchvision.transforms.ToTensor(),download=True)
dataloader = torch.utils.data.DataLoader(datasets,batch_size=64)

writer = SummaryWriter("logs_relu")

class Test1(nn.Module):
    def __init__(self):
        super(Test1,self).__init__()
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        
    def forward(self,input):
        output = self.sigmoid(input)
        return output

test1 = Test1()
step = 0

for data in dataloader:
    img,target = data
    writer.add_images("input",img,step)
    output = test1(img)
    writer.add_images("output",output,step)
    step += 1