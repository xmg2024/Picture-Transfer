##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## Created by: xmg2024
## Email: ml112265@126.com
## Copyright (c) 2025
##
## This source code is licensed under the MIT-style license found in the
## LICENSE file in the root directory of this source tree 
##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os

import numpy as np
import torch
from PIL import Image
from torch.autograd import Variable
import torchvision.models as models
from torchvision.models import VGG16_Weights

from net import Vgg16

def tensor_load_rgbimage(filename, size=None, scale=None, keep_asp=False):
    img = Image.open(filename).convert('RGB')
    if size is not None:
        if keep_asp:
            size2 = int(size * 1.0 / img.size[0] * img.size[1])
            img = img.resize((size, size2), Image.Resampling.LANCZOS)
        else:
            img = img.resize((size, size), Image.Resampling.LANCZOS)

    elif scale is not None:
        img = img.resize((int(img.size[0] / scale), int(img.size[1] / scale)), Image.Resampling.LANCZOS)
    img = np.array(img).transpose(2, 0, 1)
    img = torch.from_numpy(img).float()
    return img


def tensor_save_rgbimage(tensor, filename, cuda=False):
    if cuda:
        img = tensor.clone().cpu().clamp(0, 255).numpy()
    else:
        img = tensor.clone().clamp(0, 255).numpy()
    img = img.transpose(1, 2, 0).astype('uint8')
    img = Image.fromarray(img)
    img.save(filename)


def tensor_save_bgrimage(tensor, filename, cuda=False):
    (b, g, r) = torch.chunk(tensor, 3)
    tensor = torch.cat((r, g, b))
    tensor_save_rgbimage(tensor, filename, cuda)


def gram_matrix(y):
    (b, ch, h, w) = y.size()
    features = y.view(b, ch, w * h)
    features_t = features.transpose(1, 2)
    gram = features.bmm(features_t) / (ch * h * w)
    return gram


def subtract_imagenet_mean_batch(batch):
    """Subtract ImageNet mean pixel-wise from a BGR image."""
    mean = torch.zeros_like(batch)
    mean[:, 0, :, :] = 103.939
    mean[:, 1, :, :] = 116.779
    mean[:, 2, :, :] = 123.680
    mean = mean.to(batch.device)
    return batch - mean


def add_imagenet_mean_batch(batch):
    """Add ImageNet mean pixel-wise to a BGR image."""
    tensortype = type(batch.data)
    mean = tensortype(batch.data.size())
    mean[:, 0, :, :] = 103.939
    mean[:, 1, :, :] = 116.779
    mean[:, 2, :, :] = 123.680
    return batch + Variable(mean)

def imagenet_clamp_batch(batch, low, high):
    batch[:,0,:,:].data.clamp_(low-103.939, high-103.939)
    batch[:,1,:,:].data.clamp_(low-116.779, high-116.779)
    batch[:,2,:,:].data.clamp_(low-123.680, high-123.680)


def preprocess_batch(batch):
    batch = batch.transpose(0, 1)
    (r, g, b) = torch.chunk(batch, 3)
    batch = torch.cat((b, g, r))
    batch = batch.transpose(0, 1)
    return batch


def init_vgg16(model_folder):
    vgg = models.vgg16(weights=VGG16_Weights.IMAGENET1K_V1).features
    vgg = vgg.eval()
    return vgg


class StyleLoader(object):
    def __init__(self, style_folder, style_size, device, cuda=True):
        self.folder = style_folder
        self.style_size = style_size
        self.device = device
        self.files = os.listdir(style_folder)
        self.cuda = cuda
    
    def get(self, i):
        idx = i%len(self.files)
        filepath = os.path.join(self.folder, self.files[idx])
        style = tensor_load_rgbimage(filepath, self.style_size)    
        style = style.unsqueeze(0)
        style = preprocess_batch(style)
        style = style.to(self.device)
        style_v = Variable(style, requires_grad=False)
        return style_v

    def size(self):
        return len(self.files)
