import cv2
import dlib
import shutil
import os
import sys

# print(os.getcwd())
# this_path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
# print("this_path: ",this_path)

# 获取传入的参数
filename = sys.argv[1]
print("filename:",filename)
# # 删除文件夹，如果存在的话
# if os.path.exists('./static/test_video'):
#     shutil.rmtree('./static/test_video')

# # 创建文件夹，如果不存在的话
# os.makedirs('./static/test_video')


# 分离出文件名和扩展名
filename_without_ext, ext = os.path.splitext(filename)
print("filename_without_ext:",filename_without_ext)

# 确保路径存在
if not os.path.exists('./static/video_db/'):
    os.makedirs('./static/video_db/')

# 删除文件夹，如果存在的话
if os.path.exists(f'./static/video_db/{filename_without_ext}'):
    shutil.rmtree(f'./static/video_db/{filename_without_ext}')

# 创建一个新的文件夹
if not os.path.exists(f'./static/video_db/{filename_without_ext}'):
    os.makedirs(f'./static/video_db/{filename_without_ext}')


if os.path.exists(f'./static/video_db/{filename_without_ext}'):
    print("创建文件夹成功")
else:
    print("创建文件夹失败")

# 加载 dlib 的人脸检测器
detector = dlib.get_frontal_face_detector()

# 打开视频文件
cap = cv2.VideoCapture('./static/video/' + filename)

# # 打开视频文件
# cap = cv2.VideoCapture('./static/video/1.mp4')

# 设置每秒取一帧
# 获取视频的帧率
fps = int(cap.get(cv2.CAP_PROP_FPS))
print("帧率为：",fps)
cap.set(cv2.CAP_PROP_POS_FRAMES, fps)

frame_number = 0
while True:
    # 读取一帧
    ret, frame = cap.read()
    if not ret:
        break

    # 每秒处理一帧
    if frame_number % fps == 0:
        # 在这里处理帧，例如检测人脸
        # 检测人脸
        faces = detector(frame)

        # 对每一个检测到的人脸，截取并保存
        for i, face in enumerate(faces):
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()

            # 截取人脸
            face_img = frame[y1:y2, x1:x2]

            # 保存人脸到新的文件夹
            cv2.imwrite(f'./static/video_db/{filename_without_ext}/face_{frame_number}_{i}.jpg', face_img)

            # # 保存人脸到 test_video 文件夹
            # cv2.imwrite(f'./static/test_video/face_{frame_number}_{i}.jpg', face_img)

    frame_number += 1

# 释放视频文件
cap.release()