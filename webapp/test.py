import torch
from generator_model import Generator
from PIL import Image
import numpy as np
import cv2
import config
from torchvision.utils import save_image
import os
# from dataset import MapDataset

from torch.utils.data import DataLoader


def load_model():
    gen = Generator(in_channels=3, features=64).to(config.DEVICE)
    gen.load_state_dict(torch.load('webapp/gen.pth.tar')['state_dict'])
    gen.eval()
    return gen

def test_image(gen,image):
    image=cv2.resize(image,(256,256))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    array = np.array(image)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.merge([gray_image, gray_image, gray_image])
    gray_array = np.array(gray_image)
    augmentations = config.both_transform(image=gray_array, image0=array)
    input_image = augmentations["image"]
    target_image = augmentations["image0"]

    input_image = config.transform_only_input(image=gray_array)["image"]
    target_image = config.transform_only_mask(image=array)["image"]
    input_image = input_image.unsqueeze(0)
    target_image = target_image.unsqueeze(0)
    input_image = input_image.to(config.DEVICE)
    target_image = target_image.to(config.DEVICE)
    gen = gen.to(config.DEVICE)
    with torch.no_grad():
        prediction = gen(input_image)
        prediction = prediction * 0.5 + 0.5
    return prediction
    