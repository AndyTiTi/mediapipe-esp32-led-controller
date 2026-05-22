import cv2
import mediapipe as mp
import serial
import time

# ===================== 配置 =====================
SERIAL_PORT = "COM14"  # 改成你的串口号
HAND_RAISE_THRESH = 0.5  # 手腕y坐标阈值（0.5 = 窗口中线）
# =================================================

# 串口初始化
try:
    ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)
    time.sleep(2)
    print(f"[{time.strftime('%H:%M:%S')}] Serial {SERIAL_PORT} connected")
except serial.SerialException as e:
    print(f"[{time.strftime('%H:%M:%S')}] Error: Cannot open {SERIAL_PORT} - {e}")
    exit(1)

def send_command(cmd):
    """发送指令并读取Arduino回复"""
    try:
        ser.write((cmd + '\n').encode())
        ser.flush()
        time.sleep(0.1)
        # 读取Arduino回复
        while ser.in_waiting > 0:
            response = ser.readline().decode().strip()
            if response:
                print(f"[Arduino] {response}")
    except serial.SerialException as e:
        print(f"[{time.strftime('%H:%M:%S')}] Send failed: {e}")

# MediaPipe 手部检测
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# 下载 hand_landmarker.task 模型
# https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=2  # 检测两只手
)

# 摄像头
cap = cv2.VideoCapture(0)

# FPS 计算
prev_time = 0

# 手势状态
left_hand_raised = False
last_led_state = False

def log(msg):
    """带时间戳的日志输出"""
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    print(f"[{timestamp}] {msg}")

def is_left_hand(landmarks):
    """判断是否为左手"""
    # 手腕(0) 和 小指根部(17) 的相对位置
    # 左手: 小指根部在手腕的右侧 (x坐标更大)
    wrist = landmarks[0]
    pinky_mcp = landmarks[17]
    return pinky_mcp.x > wrist.x

print("=== Hand Control LED ===")
log("Left hand UP -> LED ON | Left hand DOWN -> LED OFF")
log("Press '1' to manually turn ON, '0' to turn OFF, 'q' to quit")

# 创建检测对象
with HandLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 转换为 mediapipe 图像格式
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))
        res = landmarker.detect_for_video(mp_image, timestamp)

        # 计算 FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
        prev_time = curr_time

        left_hand_status = "DOWN"
        right_hand_status = "DOWN"

        if res.hand_landmarks:
            for idx, hand in enumerate(res.hand_landmarks):
                # 判断左右手
                is_left = is_left_hand(hand)
                
                # 手腕位置 (landmark 0)
                wrist = hand[0]
                
                # 手举起判断: 手腕y坐标小于阈值 (y轴向下为正)
                hand_raised = wrist.y < HAND_RAISE_THRESH
                
                if is_left:
                    left_hand_status = "UP" if hand_raised else "DOWN"
                    
                    # 状态变化时发送指令
                    if hand_raised and not left_hand_raised:
                        # 左手举起 → 亮灯
                        send_command('ON')
                        left_hand_raised = True
                        last_led_state = True
                    elif not hand_raised and left_hand_raised:
                        # 左手放下 → 灭灯
                        send_command('OFF')
                        left_hand_raised = False
                        last_led_state = False
                    
                    # 绘制左手标记
                    wrist_px = (int(wrist.x * w), int(wrist.y * h))
                    cv2.circle(frame, wrist_px, 10, (0, 255, 0), -1)
                else:
                    right_hand_status = "UP" if hand_raised else "DOWN"

        # 显示界面
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Left Hand: {left_hand_status}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Right Hand: {right_hand_status}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        led_status = "OPEN" if last_led_state else "CLOSE"
        cv2.putText(frame, f"LED: {led_status}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # 绘制阈值线
        thresh_y = int(HAND_RAISE_THRESH * h)
        cv2.line(frame, (0, thresh_y), (w, thresh_y), (0, 0, 255), 2)
        cv2.putText(frame, "Raise Line", (w - 120, thresh_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        cv2.imshow("Hand Control LED", frame)

        # 键盘控制
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('1'):
            # 手动开灯
            send_command('ON')
            last_led_state = True
        elif key == ord('0'):
            # 手动关灯
            send_command('OFF')
            last_led_state = False

cap.release()
cv2.destroyAllWindows()
ser.close()
log("程序退出")
