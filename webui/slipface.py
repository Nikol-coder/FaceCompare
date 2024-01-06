import cv2
import dlib
import shutil
import os

# 删除文件夹，如果存在的话
if os.path.exists('./static/test_video'):
    shutil.rmtree('./static/test_video')

# 创建文件夹，如果不存在的话
os.makedirs('./static/test_video')

# 加载 dlib 的人脸检测器
detector = dlib.get_frontal_face_detector()

# 打开视频文件
cap = cv2.VideoCapture('./static/video/1.mp4')

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

            # 保存人脸到 test_video 文件夹
            cv2.imwrite(f'./static/test_video/face_{frame_number}_{i}.jpg', face_img)

    frame_number += 1

# 释放视频文件
cap.release()