import cv2
import mediapipe as mp
import serial
import time

# ===================== 配置 =====================
SERIAL_PORT = "COM14"  # 改成你的串口号
HAND_RAISE_THRESH = 0.5  # 手腕y坐标阈值（0.5 = 窗口中线）

# 手部显示模式
HAND_DISPLAY_MODE = "skeleton"  # "simple" = 只显示手腕圆点, "skeleton" = 蜘蛛网骨架
# =================================================

# ====================== 手部骨架连线定义（蜘蛛网） ======================
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),           # 拇指
    (0, 5), (5, 6), (6, 7), (7, 8),           # 食指
    (0, 9), (9, 10), (10, 11), (11, 12),     # 中指
    (0, 13), (13, 14), (14, 15), (15, 16),   # 无名指
    (0, 17), (17, 18), (18, 19), (19, 20),   # 小指
    (5, 9), (9, 13), (13, 17)                # 手掌横连
]

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
        time.sleep(0.05)
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

# 左手状态 (控制 LED1 - Pin 18)
left_hand_raised = False
led1_state = False

# 右手状态 (控制 LED2 - Pin 17)
right_hand_raised = False
led2_state = False

def draw_hand(frame, hand, w, h, color, label):
    """绘制手部标记"""
    if HAND_DISPLAY_MODE == "skeleton":
        # 蜘蛛网骨架模式
        # 画21个关键点
        for id, lm in enumerate(hand):
            x = int(lm.x * w)
            y = int(lm.y * h)
            cv2.circle(frame, (x, y), 3, (255, 255, 255), -1)  # 白色小圆点
        
        # 画连线
        for (p1, p2) in HAND_CONNECTIONS:
            x1 = int(hand[p1].x * w)
            y1 = int(hand[p1].y * h)
            x2 = int(hand[p2].x * w)
            y2 = int(hand[p2].y * h)
            cv2.line(frame, (x1, y1), (x2, y2), color, 1)
    else:
        # 简单模式：只显示手腕圆点
        wrist = hand[0]
        wrist_px = (int(wrist.x * w), int(wrist.y * h))
        cv2.circle(frame, wrist_px, 10, color, -1)
        cv2.putText(frame, label, (wrist_px[0] - 5, wrist_px[1] + 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

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

print("=" * 50)
print("       Hand Control Dual LED System")
print("=" * 50)
log("Left hand  -> LED1 (Pin 18) | Right hand -> LED2 (Pin 17)")
log("Keyboard: '1'/'2' = LED1 ON/OFF, '3'/'4' = LED2 ON/OFF, 'm' = toggle display mode, 'q' = quit")
print("=" * 50)

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

        left_hand_status = "---"
        right_hand_status = "---"

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
                    
                    # 左手状态变化时发送指令
                    if hand_raised and not left_hand_raised:
                        send_command('LON')  # Left hand ON
                        left_hand_raised = True
                        led1_state = True
                    elif not hand_raised and left_hand_raised:
                        send_command('LOFF')  # Left hand OFF
                        left_hand_raised = False
                        led1_state = False
                    
                    # 绘制左手 (绿色)
                    draw_hand(frame, hand, w, h, (0, 255, 0), "L")
                else:
                    right_hand_status = "UP" if hand_raised else "DOWN"
                    
                    # 右手状态变化时发送指令
                    if hand_raised and not right_hand_raised:
                        send_command('RON')  # Right hand ON
                        right_hand_raised = True
                        led2_state = True
                    elif not hand_raised and right_hand_raised:
                        send_command('ROFF')  # Right hand OFF
                        right_hand_raised = False
                        led2_state = False
                    
                    # 绘制右手 (蓝色)
                    draw_hand(frame, hand, w, h, (255, 0, 0), "R")

        # ------------------- 界面显示 -------------------
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # 左手状态 (绿色)
        cv2.putText(frame, f"Left Hand: {left_hand_status}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        led1_color = (0, 255, 0) if led1_state else (100, 100, 100)
        cv2.putText(frame, f"LED1(Pin18): {'ON' if led1_state else 'OFF'}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, led1_color, 1)
        
        # 右手状态 (蓝色)
        cv2.putText(frame, f"Right Hand: {right_hand_status}", (10, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 0), 1)
        led2_color = (255, 100, 0) if led2_state else (100, 100, 100)
        cv2.putText(frame, f"LED2(Pin17): {'ON' if led2_state else 'OFF'}", (10, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.5, led2_color, 1)
        
        # 阈值线
        thresh_y = int(HAND_RAISE_THRESH * h)
        cv2.line(frame, (0, thresh_y), (w, thresh_y), (0, 0, 255), 1)
        
        # 阈值线文字居中
        text = "Raise Line"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.4
        thickness = 1
        (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
        text_x = (w - text_w) // 2
        text_y = thresh_y - 8
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, (0, 0, 255), thickness)
        
        cv2.imshow("Hand Control Dual LED", frame)

        # 键盘控制
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('1'):
            send_command('LON')
            led1_state = True
        elif key == ord('2'):
            send_command('LOFF')
            led1_state = False
        elif key == ord('3'):
            send_command('RON')
            led2_state = True
        elif key == ord('4'):
            send_command('ROFF')
            led2_state = False
        elif key == ord('m'):
            # 切换显示模式
            HAND_DISPLAY_MODE = "simple" if HAND_DISPLAY_MODE == "skeleton" else "skeleton"
            log(f"Display mode: {HAND_DISPLAY_MODE}")

cap.release()
cv2.destroyAllWindows()
ser.close()
log("Program exited")
