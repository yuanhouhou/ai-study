from torch.utils.tensorboard import SummaryWriter
import numpy as np
from PIL import Image

writer = SummaryWriter("logs") #日志
imag_path = r"E:\vscode_project\python_study\deeplearning_file\study_resourece\test_dateset\hymenoptera_data\hymenoptera_data\train\bees\2959730355_416a18c63c.jpg"
img_PIL = Image.open(imag_path) #读取图片
imag_array = np.array(img_PIL) #图片转为数组
writer.add_image("test", imag_array, 2, dataformats="HWC") #

for i in range(100):
    writer.add_scalar("y=2x",  2*i, i) #标量

#在终端用tensorboard --logdir=logs  来查看日志
#writer.close()