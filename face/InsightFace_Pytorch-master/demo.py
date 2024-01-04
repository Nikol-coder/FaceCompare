from model import Backbone
import torch
from PIL import Image
from mtcnn import MTCNN
import os
import cv2
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片

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
save_path = "C:/Users/10698/Desktop/ff/FaceCompare/face"
file_path = os.path.join(save_path, "uploaded_image.jpg")

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
folder_path = 'C:/Users/10698/Desktop/ff/FaceCompare/webui/static/test/'


# 满足条件的图片库
destination_folder = 'C:/Users/10698/Desktop/ff/FaceCompare/webui/static/manzu/'

# 检查文件夹是否存在
if os.path.exists(destination_folder):
    # 删除文件夹及其内容
    shutil.rmtree(destination_folder)

# 重新创建文件夹
os.makedirs(destination_folder)

# 遍历文件夹下的所有文件
idx = 0
for filename in os.listdir(folder_path):

    # 获取文件的完整路径
    file_path = os.path.join(folder_path, filename)

    # 判断文件是否是图片
    if os.path.isfile(file_path) and file_path.endswith('.jpg'):
        idx += 1
        
        ## 显示图片 使用opencv
        # 读取图片
        # image = cv2.imread(file_path)
        # cv2.imshow('image', image)
        # cv2.waitKey(0)

        # 显示图片 使用matplotlib
        lena = mpimg.imread(file_path)
        # 此时 lena 就已经是一个 np.array 了，可以对它进行任意处理
        print("lena的维度:",lena.shape)  # (512, 512, 3)
        plt.imshow(lena)  # 显示图片
        plt.axis('off')  # 不显示坐标轴
        plt.show()

        img2 = get_img(file_path, device)
        emb2 = model(img2)[0]
        print(emb2.shape)
        sim_12 = emb1.dot(emb2).item()
        print("与第%d张图片的相似度为:%f"%(idx,sim_12))
        
        # 如果相似度大于0.5，将图片复制到指定目录
        if sim_12 > 0.5:
            shutil.copy(file_path, destination_folder)

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