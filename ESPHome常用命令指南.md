# ESPHome 常用命令指南

本文档整理了 ESPHome 的常用命令，帮助您快速掌握 ESP 设备的管理、配置和调试方法。

## 一、基础命令

### 1. 启动 ESPHome Dashboard

ESPHome Dashboard 是一个 Web 界面，用于管理和配置您的 ESP 设备。

```bash
# 在当前目录启动 Dashboard
esphome dashboard .

# 指定端口启动 Dashboard
esphome dashboard . --port 8080
```

**功能说明**：
- 在 `http://localhost:6052`（默认端口）启动 Web 界面
- 可以查看、编辑和管理当前目录下的所有 ESPHome 配置文件
- 提供编译、上传、查看日志等一体化操作界面

### 2. 检查 ESPHome 版本

```bash
esphome version
```

**功能说明**：显示当前安装的 ESPHome 版本信息。

## 二、设备管理命令

### 1. 编译配置文件

```bash
# 编译指定的配置文件
esphome compile your_config.yaml

# 清理构建缓存后编译
esphome compile your_config.yaml --clean
```

**功能说明**：
- 根据配置文件生成固件，但不上传到设备
- 检查配置文件语法是否正确
- 确认依赖项是否完整

### 2. 上传固件到设备

```bash
# 上传指定配置文件的固件
esphome upload your_config.yaml

# 指定端口上传固件
esphome upload your_config.yaml --device COM5
```

**功能说明**：
- 编译配置文件并将生成的固件上传到连接的 ESP 设备
- 自动检测并选择可用的串口端口
- 显示上传进度和结果

### 3. 查看设备日志

```bash
# 查看指定设备的日志
esphome logs your_config.yaml

# 指定端口查看日志
esphome logs your_config.yaml --device COM5
```

**功能说明**：
- 实时显示设备运行日志
- 可查看设备启动过程、传感器数据、错误信息等
- 使用 `Ctrl+C` 停止查看日志

### 4. 运行特定命令

```bash
# 执行单个命令（如查看状态）
esphome run your_config.yaml
```

**功能说明**：
- 提供交互式界面，可选择执行编译、上传、日志等操作
- 适合初次配置或不确定需要执行哪个具体操作时使用

## 三、高级命令

### 1. 查看连接的 ESP 设备

```bash
# 自动发现局域网内的 ESPHome 设备
esphome discover

# 使用配置文件参数发现设备
esphome discover your_config.yaml
```

**功能说明**：
- 搜索并显示局域网内运行 ESPHome 的设备
- 显示设备名称、IP 地址等信息

### 2. 创建新配置文件

```bash
# 交互式创建新的配置文件
esphome wizard new_config.yaml
```

**功能说明**：
- 引导您通过问答方式创建新的 ESPHome 配置文件
- 设置设备名称、选择板子类型、配置 WiFi 等基本信息

### 3. 清理构建文件

```bash
# 清理指定设备的构建文件
esphome clean your_config.yaml
```

**功能说明**：
- 删除指定设备的构建缓存和中间文件
- 解决某些编译错误或依赖冲突问题

### 4. 验证配置文件

```bash
# 验证配置文件语法是否正确
esphome config your_config.yaml
```

**功能说明**：
- 检查配置文件的语法错误
- 显示解析后的配置信息
- 不执行编译或上传操作

## 四、Windows 系统下的设备端口查看

在 Windows 系统中，可以使用以下命令查看连接的串口设备：

```powershell
# 查看所有串口设备
Get-PnpDevice -Class Ports -ErrorAction SilentlyContinue

# 查看 USB 串口设备
Get-PnpDevice | Where-Object {$_.Class -eq "Ports" -and $_.Manufacturer -like "*USB*"}
```

## 五、使用示例

### 示例 1：完整工作流程

1. 创建配置文件：
   ```bash
   esphome wizard my_device.yaml
   ```

2. 启动 Dashboard 进行配置编辑：
   ```bash
   esphome dashboard .
   ```

3. 编译并上传固件：
   ```bash
   esphome run my_device.yaml
   ```

4. 查看设备运行状态：
   ```bash
   esphome logs my_device.yaml
   ```

### 示例 2：快速调试

当设备出现问题时，可以使用以下命令快速诊断：

1. 检查设备是否连接：
   ```powershell
   Get-PnpDevice -Class Ports
   ```

2. 查看设备日志，寻找错误信息：
   ```bash
   esphome logs my_device.yaml
   ```

3. 重新编译并上传固件：
   ```bash
   esphome compile my_device.yaml --clean
   esphome upload my_device.yaml
   ```

## 六、注意事项

1. 确保在执行命令前已安装 ESPHome：
   ```bash
   pip install esphome
   ```

2. 运行命令时，请确保您位于正确的配置文件目录下

3. 某些命令需要管理员权限才能访问串口设备

4. 使用 `Ctrl+C` 可以随时中断正在执行的命令

5. 配置文件中的敏感信息（如 WiFi 密码）建议使用 `secrets.yaml` 文件存储

---

**更新时间**：2025-09-20
**适用版本**：ESPHome 最新版