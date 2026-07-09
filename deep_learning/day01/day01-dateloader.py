import torchvision
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
#测试集
dataset_path = "E:\\vscode_project\\python_study\\deeplearning_file\\study_resourece\\cifar-10-python"
test_data = torchvision.datasets.CIFAR10(root=dataset_path, train=False, transform=torchvision.transforms.ToTensor())
test_loader = DataLoader(dataset=test_data, batch_size=64, shuffle=True, num_workers=0, drop_last=True)

img,target = test_data[0]
print(img.shape)
print(target)

writer = SummaryWriter("dataloader")

for epoch in range(2):
    step = 0
    for data in test_loader:
        imgs, targets = data
        writer.add_images(f"Epoch {epoch}", imgs,step)
        step += 1

writer.close()