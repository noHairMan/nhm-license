# grace

grace 是一个 License 服务管理平台，旨在为用户提供便捷的 License 文件分发与校验功能。

### 🚀 项目概述

本项目专注于 License 的全生命周期管理，主要包含以下核心能力：
- **License 分发**：根据用户信息、到期时间、功能权限等维度生成并向用户分发 License 文件。
- **License 校验 API**：提供标准化的 API 接口，供客户端程序在启动或运行期间校验 License 的合法性和有效性。

### ✨ 主要功能

- [x] **多样化分发**：支持多种 License 策略配置。
- [x] **高安全性**：采用加密/签名技术，确保 License 文件不可篡改。
- [x] **标准化校验**：提供易于集成的 RESTful API 校验接口。
- [ ] **可视化管理**：(规划中) 提供管理后台查看 License 分发与使用情况。

### 🛠️ 快速开始

> [!NOTE]
> 项目目前处于初期阶段，代码正陆续上传中。

#### 环境要求
- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

#### 安装步骤
1. 克隆仓库
   ```bash
   git clone https://github.com/your-repo/grace.git
   cd grace
   ```

2. 安装依赖并创建虚拟环境
   ```bash
   uv sync
   ```

3. 启动服务
   ```bash
   uv run grace
   ```

### 📖 API 接口说明

#### 1. License 校验
验证客户端提供的 License 文件是否有效。

- **URL**: `/api/v1/license/verify`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "licenseKey": "string",
    "clientId": "string"
  }
  ```
- **Response**:
  - `200 OK`: 校验通过
  - `403 Forbidden`: License 已过期或无效

### 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。