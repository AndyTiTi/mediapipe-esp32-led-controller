### 两种运行方式
#### 方式1：直接本机安装依赖（最简单）
打开命令行执行
```bash
pip install opencv-python mediapipe pyserial numpy
```
装好直接运行脚本即可

#### 方式2：创建虚拟环境（隔离依赖，推荐项目规范用法）
```bash
# 创建虚拟环境
python -m venv blink_env

# 激活环境
# Windows cmd
blink_env\Scripts\activate
# PowerShell
.\blink_env\Scripts\Activate.ps1

# 安装依赖
pip install opencv-python mediapipe pyserial numpy
```
退出环境输入`deactivate`就行

## 操作说明
**1. 降低灵敏度（防误触发）**
- 使用双阈值机制：`EYE_OPEN_THRESH = 10` 和 `EYE_CLOSE_THRESH = 8`
- 需要完整眨眼动作：闭眼 → 睁眼 才算一次有效触发
- 之前只要 eye_h < 7 就触发，现在需要眼睛高度变化超过阈值差

**2. 添加时间戳日志**
- 所有日志输出格式：`[HH:MM:SS] 消息内容`
- 例如：`[14:23:45] ✅ 眨眼触发！LED 翻转 (eye_h=12.3)`

**3. 改进的显示**
- 窗口显示眼睛高度数值和状态（OPEN/CLOSED）
- 方便调试阈值设置

如果还是太灵敏，可以调大 `EYE_CLOSE_THRESH` 和 `EYE_OPEN_THRESH` 的值（比如设为 12 和 15）。

## 手势功能说明
- 举起左手（手腕超过红线）→ 发送 `ON` → LED 亮
- 放下左手 → 发送 `OFF` → LED 灭
- 窗口显示左右手状态和 LED 状态
- 红线表示手举起/放下的阈值位置

如果 `HAND_RAISE_THRESH = 0.3` 太灵敏或不够灵敏，可以调整这个值（0-1之间，越小需要举得越高）。