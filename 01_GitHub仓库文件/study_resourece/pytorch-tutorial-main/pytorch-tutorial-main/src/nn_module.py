# -*- coding: utf-8 -*-
# 作者：小土堆
# 公众号：我是土堆
import torch
from torch import nn


class Tudui(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, input):
        output = input + 1
        return output


tudui = Tudui()
x = torch.tensor(1.0)
output = tudui(x)
print(output)