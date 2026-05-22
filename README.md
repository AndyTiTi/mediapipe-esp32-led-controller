# Hand Control Dual LED System

基于 MediaPipe 手部检测的双 LED 手势控制系统。通过摄像头识别左右手位置，控制 Arduino 上的两个 LED 灯。

## 功能特性

- **左手控制 LED1 (Pin 18)**：举起左手亮灯，放下左手灭灯
- **右手控制 LED2 (Pin 17)**：举起右手亮灯，放下右手灭灯
- **双手同时检测**：可同时识别和控制两个 LED
- **手动键盘控制**：支持键盘快捷键测试
- **实时状态显示**：窗口显示 FPS、手势状态、LED 状态
- **串口通信调试**：显示 Arduino 回复的指令确认

## 硬件要求

- Arduino 开发板（ESP32 推荐）
- 2 个 LED 灯
- USB 数据线
- 摄像头

## 接线说明

```
LED1 (左手控制) -> Pin 18
LED2 (右手控制) -> Pin 17
LED 负极 -> GND (通过 220Ω 电阻)
```

## 安装依赖

### 方式1：直接本机安装（简单）

```bash
pip install opencv-python mediapipe pyserial numpy
```

### 方式2：虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv blink_env

# 激活环境 (Windows)
blink_env\Scripts\activate
# 或 PowerShell
.\blink_env\Scripts\Activate.ps1

# 安装依赖
pip install opencv-python mediapipe pyserial numpy
```

退出环境：`deactivate`

## 下载模型文件

运行前需要下载 MediaPipe 手部检测模型：

```bash
# Windows PowerShell
curl -o hand_landmarker.task https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
```

或直接下载：[hand_landmarker.task](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task)

将文件放到项目根目录 `d:\ArduinoProjects\FaceCtrlLED\`

## 使用方法

### 1. 上传 Arduino 代码

1. 打开 Arduino IDE
2. 加载 `FaceCtrlLED.ino`
3. 选择正确的开发板和端口
4. 点击上传

### 2. 运行 Python 程序

```bash
python main.py
```

### 3. 手势控制

| 手势 | 动作 | 指令 | LED |
|------|------|------|-----|
| 左手举起 | 手腕超过红线 | LON | LED1 亮 |
| 左手放下 | 手腕低于红线 | LOFF | LED1 灭 |
| 右手举起 | 手腕超过红线 | RON | LED2 亮 |
| 右手放下 | 手腕低于红线 | ROFF | LED2 灭 |

### 4. 键盘快捷键

| 按键 | 功能 |
|------|------|
| `1` | 手动开 LED1 |
| `2` | 手动关 LED1 |
| `3` | 手动开 LED2 |
| `4` | 手动关 LED2 |
| `m` | 切换手部显示模式 |
| `q` | 退出程序 |

## 手部显示模式

支持两种手部可视化模式，可在配置中设置或运行时切换：

### 模式说明

| 模式 | 描述 |
|------|------|
| `skeleton` | 蜘蛛网骨架模式（默认）- 显示手部 21 个关键点和骨架连线 |
| `simple` | 简单模式 - 只显示手腕位置的圆点和 L/R 标签 |

### 配置方式

**方式1：修改配置文件**

在 `main.py` 中修改：

```python
HAND_DISPLAY_MODE = "skeleton"  # "skeleton" 或 "simple"
```

**方式2：运行时切换**

按 `m` 键在两种模式间切换。

### 骨架结构说明

蜘蛛网模式显示手部 21 个关键点的完整骨架：

```
关键点编号：
0  - 手腕
1-4 - 拇指 (手腕→拇指尖)
5-8 - 食指 (手腕→食指尖)
9-12 - 中指 (手腕→中指尖)
13-16 - 无名指 (手腕→无名指尖)
17-20 - 小指 (手腕→小指尖)

连线关系：
- 每根手指的关节依次连接
- 手掌根部 (5, 9, 13, 17) 横向连接形成手掌骨架
```

### 显示颜色

| 手 | 关键点颜色 | 连线颜色 |
|----|-----------|---------|
| 左手 | 白色 | 绿色 |
| 右手 | 白色 | 蓝色 |

## 配置参数

在 `main.py` 中可调整：

```python
SERIAL_PORT = "COM14"          # 串口号
HAND_RAISE_THRESH = 0.5        # 举手阈值 (0-1，越小需要举得越高)
HAND_DISPLAY_MODE = "skeleton" # 手部显示模式: "skeleton" 或 "simple"
```

## 项目结构

```
FaceCtrlLED/
├── main.py                  # Python 主程序
├── FaceCtrlLED.ino          # Arduino 代码
├── hand_landmarker.task     # MediaPipe 模型文件
├── README.md                # 项目说明
└── blink_env/               # Python 虚拟环境
```

## 工作原理

1. **摄像头采集**：OpenCV 捕获实时视频流
2. **手部检测**：MediaPipe 检测手部 21 个关键点
3. **左右手判断**：通过手腕和小指根部的相对位置判断左右手
4. **举起检测**：手腕 y 坐标小于阈值时判定为举起
5. **串口通信**：发送指令到 Arduino 控制 LED

## 常见问题

### Q: 串口无法打开？

- 检查 Arduino 是否已连接
- 确认串口号是否正确（可在设备管理器查看）
- 关闭 Arduino IDE 串口监视器

### Q: 手势识别不准确？

- 调整 `HAND_RAISE_THRESH` 值
- 确保光线充足
- 保持手在摄像头视野内

### Q: LED 不亮？

- 检查接线是否正确
- 确认引脚与代码一致
- 查看 Python 控制台是否收到 Arduino 回复

## 技术栈

- **Python 3.x**
- **OpenCV** - 图像处理
- **MediaPipe** - 手部检测
- **PySerial** - 串口通信
- **Arduino** - 硬件控制

## License

MIT
