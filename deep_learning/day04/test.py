from pathlib import Path

import torch
import torchvision
from PIL import Image
from torch import nn


class Test(nn.Module):
    def __init__(self):
        super(Test, self).__init__()
        self.model = nn.Sequential(
            nn.Conv2d(3, 32, 5, 1, 2),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 32, 5, 1, 2),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 5, 1, 2),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(1024, 64),
            nn.Linear(64, 10),
        )

    def forward(self, x):
        x = self.model(x)
        return x


classes = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck",
]

base_dir = Path(__file__).resolve().parent
project_dir = base_dir.parent
image_path = base_dir / "horse.png"
model_path = project_dir / "test_9.pth"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

image = Image.open(image_path).convert("RGB")
print(image)

transform = torchvision.transforms.Compose(
    [
        torchvision.transforms.Resize((32, 32)),
        torchvision.transforms.ToTensor(),
    ]
)

image = transform(image)
print(image.shape)
image = image.unsqueeze(0).to(device)

model = torch.load(model_path, map_location=device, weights_only=False)
model = model.to(device)
model.eval()

with torch.no_grad():
    output = model(image)
    predict_index = output.argmax(1).item()

print(output)
print("预测类别: {}".format(classes[predict_index]))
