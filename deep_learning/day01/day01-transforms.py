from torchvision import transforms
from PIL import Image
import cv2
from torch.utils.tensorboard import SummaryWriter

#tensor的数据类型
#通过transforms.ToTensor()解决两个问题，1.如何使用，2.为啥要这个数据类型
#通过transforms.ToTensor()将PIL Image或者numpy.ndarray转换为tensor，并且归一化到[0,1]之间

img_path = r"E:\vscode_project\python_study\deeplearning_file\study_resourece\test_dateset\hymenoptera_data\hymenoptera_data\train\bees\2959730355_416a18c63c.jpg"
img_PIL = Image.open(img_path) #读取图片

writer = SummaryWriter("logs") #日志


#1.如何使用transforms
tensor_trans = transforms.ToTensor() #实例化对象
tensor_img = tensor_trans(img_PIL) #调用对象

writer.add_image("test11", tensor_img) #添加图片到日志
writer.close()
