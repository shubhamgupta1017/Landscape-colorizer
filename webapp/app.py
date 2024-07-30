import gradio as gr
from PIL import Image, ImageOps
from test import test_image, load_model
from torchvision.utils import save_image
import cv2
import os
def invert_image(img):
    gen = load_model()
    L,H,C=img.shape
    newi= cv2.resize(test_image(gen,img).squeeze(0).permute(1, 2, 0).cpu().numpy(), (H, L))
    return newi

files = os.listdir('webapp/sample')
file_list = []
for file in files:
    file_list.append(os.path.join('webapp/sample', file))
iface = gr.Interface(
    fn=invert_image,
    inputs=gr.Image(type="numpy"),
    outputs=gr.Image(type="numpy"),
    examples=file_list,
    live=True
)

if __name__ == "__main__":
    iface.launch()
