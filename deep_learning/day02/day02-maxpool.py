#maxpool的作用就是用来 提取最大特征，可以降低大小，ceil_mode代表保留，true 保留 false不保留
#stride默认等于kernel_size，ceil_mode默认false
import torch
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter
import torchvision

input = torch.tensor([[1,2,0,3,1],
                      [0,1,2,3,1],
                      [1,2,1,0,0],
                      [5,2,3,1,1],
                      [2,1,0,1,1]])

input = torch.reshape(input,(1,1,5,5))

dataset = torchvision.datasets.CIFAR10(root=r"E:\vscode_project\python_study\deeplearning_file\study_resourece\cifar-10-python",train=False,transform=torchvision.transforms.ToTensor(),download=True)
dateloader = torch.utils.data.DataLoader(dataset,batch_size=64)

class Test1(nn.Module):
    def __init__(self):
        super(Test1,self).__init__()
        self.maxpool = nn.MaxPool2d(kernel_size = 3,ceil_mode = False)
        
    def forward(self,input):
        output = self.maxpool(input)
        return output

test1 = Test1()

writer = SummaryWriter("logs_maxpool")
step = 0

for date in dateloader:
    img, target = date
    writer.add_images("input",img,step)
    output = test1(img)
    writer.add_images("output",output,step)
    step = step + 1
