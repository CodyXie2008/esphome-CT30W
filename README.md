# ESPHome CT30W红外遥控器配置项目

这是一个专门用于CT30W红外遥控器刷写ESPHome固件的配置项目，同时也支持ESP32-C3 Super Mini、esp-remote系列等多种ESP设备。通过这个项目，您可以方便地为红外遥控器和其他ESP设备编译、上传固件并集成到Home Assistant智能家居系统中，实现远程控制各种红外设备的功能。

## 支持的设备

- ESP32-C3 Super Mini
- ESP32-C3
- esp-remote
- esp-remote-orvibo
- esprmt-geek
- esprmt-orvibo
- esprmt-remote-geek

## CT30W红外遥控器硬件操作指南

对于CT30W红外遥控器的硬件操作，包括拆机、接线和烧录步骤，请参考详细的硬件操作指南：

- **[红外遥控器 (CT30W) 刷esphome.md](红外遥控器%20(CT30W)%20刷esphome.md)**: 包含完整的CT30W红外遥控器硬件操作流程，详细介绍了：
  - 硬件准备清单
  - 设备拆解方法（多种方案对比）
  - 主板和电路板介绍
  - USB转TTL接线方法
  - GPIO0短接进入刷机模式的多种方案
  - 首次烧录的详细步骤

请根据此文档完成CT30W红外遥控器的硬件改造和初始固件烧录。

## 项目结构

```
├── .esphome/         # 编译构建文件和存储信息
├── archive/          # 存档文件
├── assets/           # 项目图片和资源文件
├── esp-remote-orvibo.yaml  # 远程控制设备配置
├── esp32-c3.yaml     # ESP32-C3基础配置
├── esprmt-remote-geek.yaml # 遥控器配置
├── pronto_to_hex.py  # 将Pronto码转换为HEX码的工具
├── secrets.yaml      # 敏感信息配置（WiFi、密码等）- 不应提交到git
├── secrets_template.yaml # 敏感信息模板文件 - 可安全提交到git
├── ESP32-C3-Super-Mini-ESPHome-完整指南.md # 详细指南
├── ESPHome常用命令指南.md  # 命令参考文档
└── 红外遥控器 (CT30W) 刷esphome.md # CT30W遥控器刷写指南
```

## 快速开始

### 1. 环境准备

确保您的系统已安装：
- Python 3.9或更高版本
- pip（Python包管理器）

### 2. 安装ESPHome

使用pip安装ESPHome：

```bash
# Windows
pip install esphome

# Linux/Mac
sudo pip install esphome
# 或
pip install --user esphome
```

### 3. 配置敏感信息

**重要提示**：`secrets.yaml` 文件包含敏感信息（如WiFi密码），不应提交到代码仓库中。项目已在 `.gitignore` 中排除了此文件。

项目提供了 `secrets_template.yaml` 模板文件，请按照以下步骤配置：

1. 将 `secrets_template.yaml` 复制并重命名为 `secrets.yaml`
2. 编辑 `secrets.yaml` 文件，填入您的实际信息：

```yaml
hz_iot_wifi_name: "您的WiFi名称"
hz_iot_wifi_password: "您的WiFi密码"
ota_password: "您的OTA更新密码"
api_encryption_key: "您的API加密密钥"
fallback_ap_password: "备用AP密码"
```

**注意**：请确保 `secrets.yaml` 已添加到 `.gitignore` 中，避免敏感信息泄露。

### 4. 生成API加密密钥

如果需要生成新的API加密密钥，可以使用以下命令：

```bash
# Windows PowerShell
-join ((1..16) | ForEach {'{0:X2}' -f (Get-Random -Max 256)})

# Linux/Mac
openssl rand -hex 16
```

### 5. 启动ESPHome Dashboard

在项目目录中运行以下命令启动ESPHome Web界面：

```bash
# 进入项目目录（根据您的实际路径调整）
cd e:\Creation\mycode\esphome-CT30W

# 启动ESPHome仪表板（使用默认端口6052）
esphome dashboard .

# 如果端口6052被占用，可以使用其他端口，例如8080
# esphome dashboard . --port 8080
```

### 6. 访问Web界面

根据您启动时使用的端口，打开浏览器访问：
- 默认端口：http://localhost:6052
- 如果使用了其他端口（例如8080）：http://localhost:8080

### 7. 编译和烧录固件

1. 在Web界面中选择您需要的配置文件
2. 点击 "INSTALL" 按钮
3. 选择连接方式（首次烧录选择 "Plug into this computer"）
4. 选择正确的串口（通常是 COM 端口）
5. 点击 "INSTALL" 开始烧录

## 设备连接说明

### 串口连接
- **Windows**: 通常是 `COM3`, `COM4` 等
- **Linux**: 通常是 `/dev/ttyUSB0`, `/dev/ttyUSB1` 等
- **Mac**: 通常是 `/dev/cu.usbserial-*`

### 首次连接
1. 使用USB数据线连接ESP设备到电脑
2. 对于ESP32-C3 Super Mini，按住BOOT按钮，然后按一下RESET按钮进入下载模式
3. 在ESPHome中选择正确的串口进行烧录

## 特殊工具

- **pronto_to_hex.py**: 将红外遥控器的Pronto码转换为ESPHome可用的HEX码
  
  ### 使用方法
  ```bash
  # 运行转换工具
  python pronto_to_hex.py
  
  # 然后根据提示输入Pronto码，工具会自动转换为HEX格式
  ```
  
  转换后的HEX码可以直接用于ESPHome配置文件中的红外发射器组件。

## 项目特色功能

### 通用功能
- WiFi连接和状态监控
- Web服务器界面
- OTA无线更新
- Home Assistant集成
- 状态LED控制
- 设备信息监控
- 重启功能
- 时间同步
- WiFi连接失败时的备用AP模式

### CT30W红外遥控器特色功能
- **红外发射功能**：支持发送各种家电的红外控制信号
- **Pronto码支持**：可导入和发送标准Pronto格式的红外代码
- **自定义遥控器**：可创建多个自定义遥控器和按钮
- **智能家居集成**：通过Home Assistant实现语音控制和自动化场景
- **代码转换工具**：提供`pronto_to_hex.py`工具，方便将Pronto码转换为ESPHome可用的HEX格式
- **一键复制功能**：支持复制已录制的红外代码

## 详细文档

项目包含多个详细文档：

- **[ESP32-C3-Super-Mini-ESPHome-完整指南.md](ESP32-C3-Super-Mini-ESPHome-完整指南.md)**: ESP32-C3 Super Mini开发板的详细配置指南
- **[ESPHome常用命令指南.md](ESPHome常用命令指南.md)**: ESPHome命令的参考手册
- **[红外遥控器 (CT30W) 刷esphome.md](红外遥控器%20(CT30W)%20刷esphome.md)**: 提供CT30W红外遥控器硬件操作的完整指南，包括设备拆解、接线方法、GPIO0短接进入刷机模式的详细步骤，是硬件操作的必备参考

## 故障排除

### 1. 无法检测到设备
- 检查USB数据线是否支持数据传输
- 尝试不同的USB端口
- 安装正确的USB转串口驱动

### 2. 编译失败
- 检查网络连接
- 确保ESPHome Dashboard正常运行
- 查看终端输出获取详细错误信息

### 3. WiFi连接问题
- 检查WiFi名称和密码是否正确（在secrets.yaml中）
- 确保WiFi网络支持2.4GHz
- 检查信号强度

### 4. OTA更新失败
- 确保设备已连接到WiFi
- 检查OTA密码是否正确
- 确保设备有足够的存储空间

## 高级配置

如需添加更多功能或自定义配置，请参考各个设备的YAML配置文件和ESPHome官方文档。您可以添加各种传感器、开关、显示屏等组件来扩展设备功能。

## 相关链接

- [ESPHome官方文档](https://esphome.io/)
- [ESP32-C3技术规格](https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf)
- [Home Assistant集成](https://www.home-assistant.io/integrations/esphome/)

## 许可证

本项目采用MIT许可证。
