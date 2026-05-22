# 手势控制 LED 系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Arduino](https://img.shields.io/badge/Arduino-ESP32-green.svg)](https://www.arduino.cc/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-orange.svg)](https://mediapipe.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**[English](README.md)** | **中文**

基于 MediaPipe 手部检测的双 LED 实时手势控制系统。通过摄像头识别左右手位置，独立控制两个 LED 灯。

![演示](demo.gif) *(在此添加演示动图)*

## 功能特性

- **双手检测** - 同时识别左右手
- **独立控制** - 左手控制 LED1，右手控制 LED2
- **骨架可视化** - 实时手部骨架渲染（蜘蛛网风格）
- **键盘控制** - 手动 LED 控制用于测试
- **实时 FPS 显示** - 监控性能
- **串口调试输出** - 独立调试端口输出日志

## 演示

| 手势 | 动作 | LED |
|------|------|-----|
| 举起左手 | 手超过阈值线 | LED1 亮 |
| 放下左手 | 手低于阈值线 | LED1 灭 |
| 举起右手 | 手超过阈值线 | LED2 亮 |
| 放下右手 | 手低于阈值线 | LED2 灭 |

## 硬件要求

| 组件 | 说明 |
|------|------|
| ESP32 开发板 | 或 Arduino 兼容板 |
| 2个 LED | 任意颜色 |
| 2个 220Ω 电阻 | LED 限流电阻 |
| USB 数据线 | 用于编程和串口通信 |
| USB-TTL 模块 | 可选，用于调试日志 |
| 摄像头 | 任意 USB 摄像头 |

## 接线说明

```
ESP32 Pin 8  ────────────► LED1 (+) ──► GND
ESP32 Pin 18 ────────────► LED2 (+) ──► GND
ESP32 Pin 17 ────────────► USB-TTL RX (调试输出)
ESP32 GND   ─────────────► USB-TTL GND
```

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/hand-gesture-led-control.git
cd hand-gesture-led-control
```

### 2. 安装 Python 依赖

```bash
# 方式1：直接安装
pip install opencv-python mediapipe pyserial numpy

# 方式2：虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows

pip install opencv-python mediapipe pyserial numpy
```

### 3. 下载 MediaPipe 模型

```bash
# Windows PowerShell
curl -o hand_landmarker.task https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task

# Linux/Mac
wget https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
```

或直接下载：[hand_landmarker.task](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task)

### 4. 上传 Arduino 代码

1. 在 Arduino IDE 中打开 `mediapipe-esp32-led-controller.ino`
2. 选择开发板（推荐 ESP32）
3. 选择正确的 COM 端口
4. 点击上传

### 5. 运行程序

```bash
python main.py
```

## 键盘控制

| 按键 | 功能 |
|------|------|
| `1` | LED1 开 |
| `2` | LED1 关 |
| `3` | LED2 开 |
| `4` | LED2 关 |
| `m` | 切换显示模式（简单/骨架） |
| `q` | 退出程序 |

## 配置参数

编辑 `main.py` 进行自定义：

```python
SERIAL_PORT = "COM14"          # Arduino 串口号
HAND_RAISE_THRESH = 0.5        # 举手阈值（0-1，越小需要举得越高）
HAND_DISPLAY_MODE = "skeleton" # "skeleton" 骨架 或 "simple" 简单
```

## 项目结构

```
hand-gesture-led-control/
├── main.py                                         # Python 主程序
├── mediapipe-esp32-led-controller.ino              # Arduino 固件
├── hand_landmarker.task                            # MediaPipe 模型文件
├── README.md                                       # 英文文档
├── README-zh.md                                    # 中文文档
└── blink_env/                                      # Python 虚拟环境
```

## 工作原理

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   摄像头    │────►│  MediaPipe   │────►│   Python    │
│             │     │  手部追踪     │     │   脚本      │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                    ┌───────────────────────────┘
                    │ 串口通信
                    ▼
           ┌────────────────┐
           │     ESP32      │
           │  ┌────┐ ┌────┐ │
           │  │LED1│ │LED2│ │
           │  └────┘ └────┘ │
           └────────────────┘
```

1. **采集** - OpenCV 从摄像头捕获实时视频
2. **检测** - MediaPipe 检测手部 21 个关键点
3. **识别** - 通过关键点位置判断左右手
4. **追踪** - 监控手部位置（举起/放下）
5. **控制** - 发送串口指令到 Arduino
6. **执行** - Arduino 切换对应的 LED

## 手部骨架可视化

骨架模式显示 21 个手部关键点：

```
关键点编号：
0      - 手腕
1-4    - 拇指
5-8    - 食指
9-12   - 中指
13-16  - 无名指
17-20  - 小指
```

## 故障排查

<details>
<summary><b>串口无法打开</b></summary>

- 检查 Arduino 是否已连接
- 在设备管理器（Windows）或 `ls /dev/tty*`（Linux/Mac）中确认 COM 端口
- 关闭 Arduino 串口监视器
- 确保没有其他程序占用串口
</details>

<details>
<summary><b>手部检测不工作</b></summary>

- 确保 `hand_landmarker.task` 文件存在于项目目录
- 检查摄像头是否正常工作，未被其他程序占用
- 改善光照条件
- 保持手在摄像头画面内
</details>

<details>
<summary><b>LED 无响应</b></summary>

- 检查接线是否正确
- 检查 LED 极性（长脚为正极）
- 确认引脚正确：LED1=Pin 8，LED2=Pin 18
- 查看 Python 控制台的串口通信日志
</details>

<details>
<summary><b>Serial2 无调试输出</b></summary>

- 检查 USB-TTL 连接：RX→Pin 17，GND→GND
- 确认波特率为 115200
- 尝试交换 RX/TX 线
- 确保 USB-TTL 驱动已安装
</details>

## 参与贡献

欢迎提交 Pull Request 参与贡献！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 致谢

- [MediaPipe](https://mediapipe.dev/) - 手部追踪解决方案
- [OpenCV](https://opencv.org/) - 计算机视觉库
- [Arduino](https://www.arduino.cc/) - 开源硬件平台

## 联系方式

栈先锋 - [@栈先锋](https://space.bilibili.com/317356181)

项目地址：[https://github.com/AndyTiTi/mediapipe-esp32-led-controller](https://github.com/AndyTiTi/mediapipe-esp32-led-controller)

---

⭐ 如果这个项目对你有帮助，请给个 Star！
