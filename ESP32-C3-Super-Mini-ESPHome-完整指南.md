# ESP32-C3 Super Mini ESPHome 完整安装配置指南

## 📋 目录
1. [系统要求](#系统要求)
2. [安装ESPHome](#安装esphome)
3. [创建项目](#创建项目)
4. [配置设备](#配置设备)
5. [烧录固件](#烧录固件)
6. [Home Assistant集成](#home-assistant集成)
7. [常见问题解决](#常见问题解决)
8. [高级配置](#高级配置)

---

## 🖥️ 系统要求

### 硬件要求
- **开发板**: ESP32-C3 Super Mini
- **USB数据线**: 支持数据传输的USB-C线
- **电脑**: Windows 10/11, macOS, 或 Linux

### 软件要求
- **Python**: 3.8 或更高版本
- **Git**: 用于版本控制
- **串口驱动**: CP2102 或 CH340 驱动

---

## 🔧 安装ESPHome

### 1. 安装Python
```bash
# 检查Python版本
python --version
# 或
python3 --version
```

如果未安装Python，请从 [python.org](https://www.python.org/downloads/) 下载安装。

### 2. 安装ESPHome
```bash
# 使用pip安装ESPHome
pip install esphome

# 验证安装
esphome version
```

### 3. 安装依赖工具
```bash
# 安装PlatformIO (ESPHome会自动安装)
pip install platformio
```

---

## 📁 创建项目

### 1. 创建项目目录
```bash
# 创建项目文件夹
mkdir esphome-project
cd esphome-project

# 初始化ESPHome项目
esphome wizard esp32-c3-super-mini.yaml
```

### 2. 选择配置选项
在向导中选择以下选项：
- **设备名称**: `esp32-c3-super-mini`
- **开发板**: `ESP32-C3-DevKitM-1`
- **WiFi网络**: 输入您的WiFi信息
- **密码**: 设置OTA更新密码

---

## ⚙️ 配置设备

### 基础配置文件 (`esp32-c3-super-mini.yaml`)
```yaml
esphome:
  name: esp32-c3-super-mini
  friendly_name: ESP32-C3 Super Mini
  min_version: 2025.8.4

esp32:
  board: esp32-c3-devkitm-1
  framework:
    type: esp-idf
    version: recommended
  flash_size: 4MB
  cpu_frequency: 160MHz

# 日志配置
logger:
  level: DEBUG
  hardware_uart: USB_SERIAL_JTAG

# Home Assistant API
api:
  encryption:
    key: "your-32-byte-base64-key-here"

# OTA更新
ota:
  - platform: esphome
    password: "your-ota-password"

# WiFi配置
wifi:
  ssid: "your-wifi-ssid"
  password: "your-wifi-password"
  fast_connect: true
  
  # 备用热点
  ap:
    ssid: "ESP32-C3-Fallback"
    password: "12345678"

# 状态LED
status_led:
  pin: GPIO2

# 设备信息传感器
text_sensor:
  - platform: version
    name: "Version"
  - platform: wifi_info
    ip_address:
      name: "IP Address"
    ssid:
      name: "Connected SSID"
    mac_address:
      name: "MAC Address"

# 状态监控传感器
sensor:
  - platform: wifi_signal
    name: "WiFi Signal"
    update_interval: 60s
  - platform: uptime
    name: "Uptime"
  - platform: template
    name: "Free Heap"
    unit_of_measurement: "bytes"
    update_interval: 60s
    lambda: |-
      return esp_get_free_heap_size();

# 耗电量监控传感器
  - platform: template
    name: "CPU Temperature"
    unit_of_measurement: "°C"
    device_class: temperature
    update_interval: 60s
    lambda: |-
      return temperatureRead();
    accuracy_decimals: 1
    
  - platform: template
    name: "CPU Frequency"
    unit_of_measurement: "MHz"
    update_interval: 60s
    lambda: |-
      return getCpuFrequencyMhz();
    accuracy_decimals: 0
    
  - platform: template
    name: "Power Consumption"
    unit_of_measurement: "mA"
    device_class: current
    update_interval: 30s
    lambda: |-
      // 估算功耗：基础功耗 + WiFi功耗 + CPU负载
      float base_power = 50.0;  // 基础功耗约50mA
      float wifi_power = 80.0;  // WiFi功耗约80mA
      float cpu_load = (160.0 - getCpuFrequencyMhz()) / 160.0 * 100.0;  // CPU负载百分比
      float cpu_power = cpu_load * 0.3;  // CPU动态功耗
      return base_power + wifi_power + cpu_power;
    accuracy_decimals: 1
    
  - platform: template
    name: "Estimated Daily Consumption"
    unit_of_measurement: "mAh"
    device_class: energy
    update_interval: 300s  # 5分钟更新一次
    lambda: |-
      // 基于当前功耗估算日耗电量
      float current_power = 130.0;  // 当前功耗估算
      float daily_hours = 24.0;
      return (current_power * daily_hours) / 1000.0;  // 转换为mAh
    accuracy_decimals: 2
    
  - platform: template
    name: "Total Energy Consumption"
    unit_of_measurement: "Wh"
    device_class: energy
    state_class: total_increasing
    update_interval: 60s
    lambda: |-
      // 累计功耗计算（基于运行时间）
      static float total_energy = 0.0;
      static uint32_t last_update = 0;
      uint32_t now = millis();
      
      if (last_update > 0) {
        float time_diff = (now - last_update) / 3600000.0;  // 转换为小时
        float avg_power = 130.0;  // 平均功耗130mA
        float voltage = 3.3;  // 工作电压3.3V
        total_energy += (avg_power * voltage * time_diff) / 1000.0;  // 转换为Wh
      }
      last_update = now;
      return total_energy;
    accuracy_decimals: 3
    
  - platform: template
    name: "Power Efficiency"
    unit_of_measurement: "%"
    update_interval: 60s
    lambda: |-
      // 计算功耗效率（基于CPU频率和负载）
      float max_freq = 160.0;
      float current_freq = getCpuFrequencyMhz();
      float efficiency = (current_freq / max_freq) * 100.0;
      return efficiency;
    accuracy_decimals: 1

# RGB LED控制
light:
  - platform: rgb
    red: red_output
    green: green_output
    blue: blue_output
    name: "ESP32 LED"
    id: esp32_led
    restore_mode: ALWAYS_OFF

output:
  - platform: ledc
    pin: GPIO8
    id: red_output
    channel: 0
    inverted: true
  - platform: ledc
    pin: GPIO9
    id: green_output
    channel: 1
    inverted: true
  - platform: ledc
    pin: GPIO10
    id: blue_output
    channel: 2
    inverted: true

# 开关控制
switch:
  - platform: restart
    name: "Restart"
  - platform: gpio
    pin: GPIO3
    name: "Living Room Light"
    id: living_room_light
  - platform: gpio
    pin: GPIO4
    name: "Fan Control"
    id: fan_control

# 二进制传感器
binary_sensor:
  - platform: status
    name: "Status"
  - platform: gpio
    pin: 
      number: GPIO1
      mode: INPUT_PULLUP
    name: "Living Room Window"
    id: living_room_window
  - platform: gpio
    pin: 
      number: GPIO0
      mode: INPUT_PULLUP
    name: "Button"
    id: button
```

### 创建密钥文件 (`secrets.yaml`)
```yaml
# WiFi配置
wifi_ssid: "your-wifi-ssid"
wifi_password: "your-wifi-password"

# OTA密码
ota_password: "your-ota-password"

# API加密密钥 (32字节base64编码)
api_encryption_key: "dGhpcyBpcyBhIDMyIGJ5dGUgZW5jcnlwdGlvbiBrZXk="
```

---

## 🔥 烧录固件

### 方法1: 串口烧录 (首次安装)

#### 1. 进入下载模式
- **按住BOOT按钮**
- **按下RESET按钮**
- **松开RESET按钮**
- **松开BOOT按钮**
- 设备进入下载模式（红色LED常亮）

#### 2. 烧录固件
```bash
# 通过串口烧录
esphome run esp32-c3-super-mini.yaml --device COM4
```

**Windows端口号**:
- COM3, COM4, COM5 等

**macOS/Linux端口号**:
- `/dev/ttyUSB0`, `/dev/tty.usbserial-*` 等

### 方法2: OTA更新 (后续更新)

#### 1. 确保设备连接WiFi
```bash
# 检查设备状态
esphome logs esp32-c3-super-mini.yaml
```

#### 2. OTA更新
```bash
# 无线更新
esphome run esp32-c3-super-mini.yaml
```

---

## 🏠 Home Assistant集成

### 1. 在Home Assistant中添加设备

#### 方法1: 自动发现
1. 确保ESP32和Home Assistant在同一网络
2. 在Home Assistant中，转到 **配置** > **设备与服务**
3. 点击 **添加集成**
4. 搜索 **ESPHome**
5. 输入设备IP地址或使用自动发现

#### 方法2: 手动添加
1. 在Home Assistant配置文件中添加：
```yaml
esphome:
  devices:
    esp32-c3-super-mini:
      api_encryption_key: "your-32-byte-base64-key"
```

### 2. 配置实体
在Home Assistant中，您将看到以下实体：

**传感器**:
- `sensor.wifi_signal` - WiFi信号强度
- `sensor.uptime` - 运行时间
- `sensor.free_heap` - 可用内存

**开关**:
- `switch.restart` - 重启设备
- `switch.living_room_light` - 客厅灯
- `switch.fan_control` - 风扇控制

**灯光**:
- `light.esp32_led` - RGB LED控制

**二进制传感器**:
- `binary_sensor.status` - 设备状态
- `binary_sensor.living_room_window` - 客厅窗户
- `binary_sensor.button` - 按钮

**耗电量监控传感器**:
- `sensor.cpu_temperature` - CPU温度
- `sensor.cpu_frequency` - CPU频率
- `sensor.power_consumption` - 实时功耗
- `sensor.estimated_daily_consumption` - 日耗电量估算
- `sensor.total_energy_consumption` - 累计耗电量
- `sensor.power_efficiency` - 功耗效率

### 3. 创建耗电量监控仪表盘

在Home Assistant中创建仪表盘卡片来显示耗电量信息：

#### 能耗统计卡片
```yaml
type: entities
title: ESP32-C3 耗电量监控
entities:
  - entity: sensor.power_consumption
    name: 实时功耗
    icon: mdi:lightning-bolt
  - entity: sensor.estimated_daily_consumption
    name: 日耗电量
    icon: mdi:battery-clock
  - entity: sensor.total_energy_consumption
    name: 累计耗电量
    icon: mdi:chart-line
  - entity: sensor.power_efficiency
    name: 功耗效率
    icon: mdi:speedometer
```

#### 系统状态卡片
```yaml
type: entities
title: ESP32-C3 系统状态
entities:
  - entity: sensor.cpu_temperature
    name: CPU温度
    icon: mdi:thermometer
  - entity: sensor.cpu_frequency
    name: CPU频率
    icon: mdi:cpu-64-bit
  - entity: sensor.wifi_signal
    name: WiFi信号
    icon: mdi:wifi
  - entity: sensor.uptime
    name: 运行时间
    icon: mdi:timer
```

#### 能耗图表卡片
```yaml
type: history-graph
title: ESP32-C3 功耗趋势
entities:
  - sensor.power_consumption
  - sensor.cpu_temperature
hours_to_show: 24
refresh_interval: 30
```

---

## 🔧 常见问题解决

### 1. 编译错误
```bash
# 清理构建缓存
esphome clean esp32-c3-super-mini.yaml

# 重新编译
esphome run esp32-c3-super-mini.yaml
```

### 2. 串口连接失败
- 检查USB线是否支持数据传输
- 安装正确的串口驱动
- 确认端口号正确
- 关闭其他可能占用串口的程序

### 3. WiFi连接问题
- 检查WiFi密码是否正确
- 确保2.4GHz网络（ESP32不支持5GHz）
- 检查网络信号强度

### 4. OTA更新失败
- 确保设备已连接WiFi
- 检查网络连接
- 尝试串口烧录

### 5. LED控制问题
- 检查GPIO引脚配置
- 确认LED连接正确
- 调整`inverted`参数

---

## 🚀 高级配置

### 1. 添加传感器
```yaml
# DHT温湿度传感器
sensor:
  - platform: dht
    pin: GPIO5
    model: DHT22
    temperature:
      name: "Temperature"
    humidity:
      name: "Humidity"
    update_interval: 60s

# 光照传感器
sensor:
  - platform: adc
    pin: GPIO6
    name: "Light Level"
    update_interval: 60s
```

### 2. 添加执行器
```yaml
# 继电器控制
switch:
  - platform: gpio
    pin: GPIO7
    name: "Relay 1"
    id: relay1

# 舵机控制
output:
  - platform: ledc
    pin: GPIO8
    id: servo_output
    frequency: 50Hz

servo:
  - id: my_servo
    output: servo_output
    min_level: 0.025
    max_level: 0.125
```

### 3. 自动化配置
```yaml
# 自动化规则
automation:
  - alias: "Button Pressed"
    trigger:
      platform: state
      entity_id: binary_sensor.button
      to: 'on'
    action:
      - service: light.toggle
        entity_id: light.esp32_led
```

---

## 📚 参考资源

### 官方文档
- [ESPHome官方文档](https://esphome.io/)
- [ESP32-C3技术参考](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/)

### 社区资源
- [ESPHome社区论坛](https://community.home-assistant.io/c/esphome/)
- [GitHub仓库](https://github.com/esphome/esphome)

### 开发板信息
- **ESP32-C3 Super Mini**: 基于ESP32-C3芯片的紧凑型开发板
- **GPIO引脚**: 支持0-21号GPIO
- **WiFi**: 支持2.4GHz WiFi
- **蓝牙**: 支持BLE 5.0

---

## 📝 更新日志

### v1.0 (2025-01-27)
- 初始版本
- 基础配置和烧录指南
- 常见问题解决方案

---

## 🤝 支持

如果您在使用过程中遇到问题，可以：

1. 查看本文档的常见问题部分
2. 访问ESPHome官方文档
3. 在社区论坛寻求帮助
4. 检查GitHub Issues

---

**祝您使用愉快！** 🎉
