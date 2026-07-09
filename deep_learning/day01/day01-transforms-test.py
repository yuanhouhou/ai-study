from PIL import Image
from torchvision import transforms
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter("logs")
img_path = r"E:\vscode_project\python_study\deeplearning_file\study_resourece\test_dateset\test_photo.jpg"
img = Image.open(img_path)

trans_tensor = transforms.ToTensor()
img_tensor = trans_tensor(img)
writer.add_image("test_tensor", img_tensor)

#normalize 
trans_normalize = transforms.Normalize(mean=[0.1, 0.3, 0.5], std=[0.3, 0.2, 0.1])
img_normalize = trans_normalize(img_tensor)
writer.add_image("test_normalize", img_normalize,3)

#resize
trans_resize = transforms.Resize((512, 512))
#img pil -> resize -> img_resize pil   
img_resize = trans_resize(img)
print(img_resize)
#img_resize tensor -> img_resize tensor
img_resize = trans_tensor(img_resize)

writer.add_image("test_resize", img_resize,0)   

#compose
trans_compose = transforms.Resize(512)
trans_compose = transforms.Compose([trans_compose,trans_tensor])
img_compose = trans_compose(img)
writer.add_image("test_compose", img_compose,0)

writer.close()