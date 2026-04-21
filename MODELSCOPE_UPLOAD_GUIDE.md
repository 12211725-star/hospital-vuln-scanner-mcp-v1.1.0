# 魔搭 MCP 广场上传指南

## 📋 前置准备

### 1. 注册魔搭账号
- 访问 https://modelscope.cn/
- 点击右上角注册/登录
- 完成实名认证（如需发布公开项目）

### 2. 准备项目文件
确保你的项目包含以下文件：
```
hospital-vuln-mcp/
├── src/                        ✅ 源代码
├── pyproject.toml             ✅ Python 配置
├── README.md                  ✅ 英文文档
├── README_CN.md               ✅ 中文文档（新增）
├── modelscope.yaml            ✅ 魔搭配置（新增）
├── LICENSE                    ✅ 许可证
└── .gitignore                 ✅ Git 忽略
```

---

## 🚀 上传步骤

### 方法一：通过 Git 上传（推荐）

#### 步骤 1：在魔搭创建仓库

1. 登录 https://modelscope.cn/
2. 点击右上角 **+** → **新建模型/数据集**
3. 选择 **"创建仓库"**
4. 填写信息：
   | 字段 | 建议填写 |
   |------|----------|
   | **仓库名称** | `hospital-vuln-mcp` |
   | **中文名称** | 医院漏洞扫描 MCP 服务器 |
   | **仓库类型** | **MCP** |
   | **可见性** | 公开 / 私有 |
   | **许可证** | MIT |
   | **描述** | 为 AI 助手提供医疗系统安全扫描能力的 MCP 服务器 |

5. 点击 **创建仓库**

#### 步骤 2：推送代码

在 PowerShell 中执行：

```powershell
# 1. 进入项目目录
cd "C:\Users\刘涛\Desktop\hospital-vuln-mcp"

# 2. 移除原来的 Git 配置（如果有）
Remove-Item -Path ".git" -Recurse -Force

# 3. 初始化新的 Git 仓库
git init

# 4. 配置 Git 信息（替换为你的魔搭账号）
git config user.name "你的魔搭用户名"
git config user.email "你的邮箱"

# 5. 添加所有文件
git add .

# 6. 提交
git commit -m "Initial commit: Hospital Vulnerability Scanner MCP Server

- 14 个安全扫描工具
- 支持漏洞扫描、网络发现、报告生成
- 专为医疗系统设计"

# 7. 连接魔搭仓库（替换 你的用户名）
git remote add origin https://www.modelscope.cn/你的用户名/hospital-vuln-mcp.git

# 8. 推送代码
git push -u origin master
```

#### 步骤 3：配置 MCP 信息

1. 在魔搭仓库页面，点击 **"设置"**
2. 找到 **"MCP 配置"** 标签
3. 填写 MCP 信息：
   - **MCP 名称**: `hospital-vuln-mcp`
   - **运行方式**: `stdio` 或 `sse`
   - **安装命令**: `uvx hospital-vuln-mcp`
   - **Python 包名**: `hospital-vuln-mcp`
4. 保存配置

---

### 方法二：网页上传

#### 步骤 1：打包项目

```powershell
# 在项目目录外执行
$source = "C:\Users\刘涛\Desktop\hospital-vuln-mcp"
$dest = "C:\Users\刘涛\Desktop\hospital-vuln-mcp-upload.zip"

# 排除 .git 文件夹压缩
Compress-Archive -Path "$source\src", "$source\*.toml", "$source\*.md", "$source\LICENSE", "$source\.gitignore", "$source\modelscope.yaml" -DestinationPath $dest -Force

Write-Host "✅ 打包完成: $dest"
```

#### 步骤 2：在魔搭创建并上传

1. 访问 https://modelscope.cn/
2. 创建新的 MCP 仓库（同上）
3. 在仓库页面，找到 **"上传文件"** 按钮
4. 拖拽或选择打包的 zip 文件
5. 等待上传完成
6. 解压并提交

---

## ⚙️ MCP 配置详情

### modelscope.yaml 说明

这个文件告诉魔搭如何运行你的 MCP：

```yaml
name: hospital-vuln-mcp                    # MCP 名称
version: 1.0.0                             # 版本
description: 医院漏洞扫描...              # 中文描述
description_en: Hospital Vulnerability... # 英文描述

mcp:
  name: hospital-vuln-mcp
  transport:                               # 传输方式
    - stdio                               # 标准输入输出
    - sse                                 # Server-Sent Events
  port: 8000                               # SSE 端口

tools:                                     # 工具列表
  - name: start_scan
    description: 启动漏洞扫描任务
    description_en: Start a vulnerability scan task
    
categories:                                # 分类
  - security
  - healthcare
  
tags:                                      # 标签
  - mcp
  - security
  - hospital
  - 安全
  - 漏洞扫描
  - 医院

install:                                   # 安装方式
  pypi: hospital-vuln-mcp                 # PyPI 包名
  command: uvx hospital-vuln-mcp          # 运行命令
```

---

## ✅ 上传后检查清单

上传完成后，请确认：

- [ ] 代码已上传到魔搭仓库
- [ ] `modelscope.yaml` 文件已包含
- [ ] README 文档完整（中英文）
- [ ] MCP 配置已设置
- [ ] 工具列表正确显示
- [ ] 安装命令可正常运行

---

## 🧪 测试 MCP

上传后，可以在魔搭平台测试：

1. 在 MCP 广场找到你的项目
2. 点击 **"在线体验"**
3. 测试各个工具是否正常工作

或在本地测试：
```bash
# 安装
uvx hospital-vuln-mcp

# 测试 SSE 模式
hospital-vuln-mcp --transport sse --port 8000
```

---

## 📌 注意事项

1. **隐私安全**: 不要上传包含敏感信息（密码、密钥）的文件
2. **依赖管理**: 确保 `pyproject.toml` 中的依赖完整
3. **文档完整**: 提供清晰的中英文文档
4. **版本管理**: 使用语义化版本号（如 1.0.0）
5. **许可证**: 建议开源许可证（MIT/Apache-2.0）

---

## 🔗 相关链接

- 魔搭 MCP 文档: https://modelscope.cn/docs/mcp
- MCP 协议文档: https://modelcontextprotocol.io/
- FastMCP 文档: https://github.com/jlowin/fastmcp

---

## 🆘 常见问题

### Q1: 推送失败提示 "403 Forbidden"
A: 检查魔搭账号是否有权限，或仓库是否设置为私有

### Q2: MCP 在魔搭不显示工具
A: 检查 `modelscope.yaml` 中的 tools 配置是否正确

### Q3: 如何更新已上传的 MCP
A: 修改代码后执行 `git push` 即可自动更新

### Q4: 可以同时上传到 GitHub 和魔搭吗
A: 可以！添加多个 remote：
```bash
git remote add github https://github.com/用户名/仓库.git
git remote add modelscope https://www.modelscope.cn/用户名/仓库.git
git push github master
git push modelscope master
```
