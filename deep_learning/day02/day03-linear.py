import torch
import torch.nn as nn
from   torch.utils.tensorboard import SummaryWriter
import torchvision
from  torch.utils.data import DataLoader

datasets = torchvision.datasets.CIFAR10(root=r"E:\vscode_project\python_study\deeplearning_file\study_resourece\cifar-10-python",train=False,transform=torchvision.transforms.ToTensor(),download=True)
dataloader = DataLoader(datasets,batch_size=64)
class Test1(nn.Module):
    def __init__(self):
        super(Test1,self).__init__()
        self.linear = nn.Linear(196608,10)
    
    def forward(self,input):
        ouput = self.linear(input)
        return output

test1 = Test1()

writer = SummaryWriter("logs_linear")
step = 0

for data in dataloader:
    imgs,targets = data
    writer.add_images("input",imgs,step)
    output = test1(imgs)
    writer.add_images("output",output,step)
    step += 1