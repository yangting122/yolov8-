# -*- coding: utf-8 -*-
import cv2
from ultralytics import YOLO
import numpy as np
import time

# 替换为你的 YOLOv8 模型路径
model = YOLO('/workspace/123/best1.engine', task='detect')

# 摄像头
cap = cv2.VideoCapture(0)

# 获取摄像头的宽度和高度
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# 初始化输出视频变量
out = None
recording = False  # 记录录影状态

def estimate_distance(bbox_width, focal_length, real_width):
    return (real_width * focal_length) / bbox_width

# 设置焦距和车辆的实际宽度
focal_length = 700
real_width = 2.0

# 存储上一帧的距离信息
previous_distances = {}
object_timers = {}
danger_display_times = {}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 使用 YOLOv8 模型进行预测
    results = model(frame)

    # 检查检测结果是否为空
    if not results[0].boxes:
        continue

    # 遍历检测到的对象
    current_distances = {}
    current_timers = {}
    current_danger_times = {}

    for detection in results[0].boxes:
        # 获取边界框坐标和标签
        bbox = detection.xyxy[0].cpu().numpy()  # [x1, y1, x2, y2]
        class_id = int(detection.cls[0].cpu().numpy())  # 类别ID
        label = results[0].names[class_id]  # 类别名称

        # 计算距离（使用边界框的宽度）
        bbox_width = bbox[2] - bbox[0]
        distance = estimate_distance(bbox_width, focal_length, real_width)

        # 画出边界框
        cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)

        # 计算物体中心点位置
        object_center_x = (bbox[0] + bbox[2]) / 2

        # 判断物体是否位于相机正前方（画面 2/5 到 3/5 区域）
        in_front = (frame_width * 2 / 5) < object_center_x < (frame_width * 3 / 5)

        # 设置类名和距离文字的位置
        text_x = int(bbox[0])
        text_y = int(bbox[1]) - 10
        distance_text_y = text_y + 20 if text_y >= 20 else int(bbox[3]) + 40
        
        # 绘制类别名称和距离信息
        cv2.putText(frame, f'{label}', (text_x, text_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, f'Distance: {distance:.2f}m', 
                    (text_x, distance_text_y), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, (255, 0, 0), 2)

        # 更新当前距离和计时器
        current_distances[class_id] = distance
        current_timers[class_id] = time.time()

        # 计算相对速度（假设每帧间隔相等）
        if class_id in previous_distances:
            speed = previous_distances[class_id] - distance
            
            # 判断危险情况并绘制“DANGER”标示
            if distance < previous_distances[class_id] and speed > 17 and in_front:
                if class_id in object_timers and (time.time() - object_timers[class_id]) > 0.08:
                    danger_text_y = text_y - 20 if text_y > 20 else text_y + 40
                    cv2.putText(frame, 'DANGER', (text_x, danger_text_y), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 3)
                    current_danger_times[class_id] = time.time()

    # 更新上一帧的距离信息、计时器和危险标示显示时间
    previous_distances = current_distances
    object_timers = current_timers
    danger_display_times = current_danger_times

    # 在画面上绘制正前方区域的辅助线
    cv2.line(frame, (int(frame_width * 2 / 5), 0), (int(frame_width * 2 / 5), frame_height), (255, 0, 0), 2)
    cv2.line(frame, (int(frame_width * 3 / 5), 0), (int(frame_width * 3 / 5), frame_height), (255, 0, 0), 2)

    # 显示帧
    cv2.imshow('frame', frame)

    # 按下 'a' 键开始录影
    if cv2.waitKey(1) & 0xFF == ord('a') and not recording:
        out = cv2.VideoWriter("Video.mp4", cv2.VideoWriter_fourcc(*'XVID'), 20.0, (frame_width, frame_height))
        recording = True
        print("开始录影...")

    # 如果正在录影，写入影格
    if recording:
        out.write(frame)

    # 按下 'q' 键跳出循环结束录影
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("录影结束...")
        break

# 释放资源
cap.release()
if out:
    out.release()
cv2.destroyAllWindows()

