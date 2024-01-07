from model import Backbone
import torch
from PIL import Image
from mtcnn import MTCNN
import os
import cv2
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片
import json

from torchvision.transforms import Compose, ToTensor, Normalize
import shutil
mtcnn = MTCNN()


def get_img(img_path, device):
    img = Image.open(img_path)
    img = img.convert("RGB")  # 转换为RGB图像
    face = mtcnn.align(img)
    transfroms = Compose(
        [ToTensor(), Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])
    return transfroms(face).to(device).unsqueeze(0)


device = 'cuda'
# device = 'cpu'

# img1 = get_img('./images/1.jpg', device)
# img2 = get_img('./images/2.jpg', device)
# img3 = get_img('./images/5.jpg', device)
# img4 = get_img('./images/7.jpg', device)
# print(img1.shape)


# 指定保存位置
# os.path.join('../face/', "uploaded_image.jpg")
this_path = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(this_path, "../uploaded_image.jpg")

#被测试图片
img1 = get_img(file_path, device)
print(img1.shape)

model = Backbone(num_layers=50, drop_ratio=0.6, mode='ir_se')
model.load_state_dict(torch.load('model_ir_se50.pth'),strict=False)
model.eval()
model.to(device)

emb1 = model(img1)[0]
print(emb1.shape)

#读取图片库
pa_folder_path = os.path.normpath(os.path.join(this_path, '../../webui/static/video_db/'))


# 满足条件的图片库
destination_folder = os.path.normpath(os.path.join(this_path,  '../../webui/static/manzu_video/'))
print("destination_folder: ", destination_folder)

# 检查文件夹是否存在
if os.path.exists(destination_folder):
    # 删除文件夹及其内容
    shutil.rmtree(destination_folder)

# 重新创建文件夹
os.makedirs(destination_folder)

# 在运行 demo_video.py 之前，先清空 valid_son_folders.json 文件
with open('../../webui/static/json/valid_son_folders.json', 'w') as f:
    f.write('')
# 创建一个列表来存储满足条件的 son_folder
valid_son_folders = []

# 定义基础目录和子文件夹
base_dir = pa_folder_path
print("base_dir: ", base_dir)
# 遍历子文件夹
for son_folder in os.listdir(base_dir):
    print("son_folder: ", son_folder)
    folder_path = os.path.join(pa_folder_path, son_folder)

    # 遍历文件夹下的所有文件
    idx = 0
    for filename in os.listdir(folder_path):

        # 获取文件的完整路径
        file_path = os.path.join(folder_path, filename)

        # 判断文件是否是图片
        if os.path.isfile(file_path) and file_path.endswith('.jpg'):
            # print("file_path: ", file_path)
            idx += 1

            # 显示图片 使用matplotlib
            image = mpimg.imread(file_path)
            # 在这里添加你的代码来显示图片
            img2 = get_img(file_path, device)
            emb2 = model(img2)[0]
            print(emb2.shape)
            sim_12 = emb1.dot(emb2).item()
            print("与第%d张图片的相似度为:%f"%(idx,sim_12))
            
            # 如果相似度大于0.5，将图片复制到指定目录
            if sim_12 > 0.5:
                # 获取 file_path 的文件名
                valid_son_folders.append(son_folder)
                # 获取新文件的完整路径
                new_file_path = os.path.join(destination_folder, son_folder)
                # print("new_file_path: ", new_file_path)
                # 检查文件夹是否存在
                if os.path.exists(new_file_path):
                    # 删除文件夹及其内容
                    shutil.rmtree(new_file_path)

                # 重新创建文件夹
                os.makedirs(new_file_path)
                # 将文件复制到新的位置
                # 检查 file_path 是否是 jpg 文件
                if file_path.lower().endswith('.jpg'):
                    # 将文件复制到新的位置
                    # print("file_path: ", file_path)
                    shutil.copy(file_path, new_file_path)
                else:
                    print("file_path is not a jpg file: ", file_path)

with open('../../webui/static/json/valid_son_folders.json', 'w') as f:
    json.dump(valid_son_folders, f)


# emb1 = model(img1)[0]
# emb2 = model(img2)[0]
# emb3 = model(img3)[0]
# emb4 = model(img4)[0]
# print(emb1.shape)

# sim_12 = emb1.dot(emb2).item()
# sim_13 = emb1.dot(emb3).item()
# sim_14 = emb1.dot(emb4).item()

# print(sim_12)
# print(sim_13)
# print(sim_14)