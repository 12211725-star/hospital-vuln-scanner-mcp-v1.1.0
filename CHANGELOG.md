# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.3] - 2026-04-22

### Fixed

- 🐛 修复 README 中 PyPI 包名错误（hospital-vuln-scanner-mcp → hospital-vuln-mcp）
- 🐛 修复魔搭不可部署问题（包名与 PyPI 不一致）

## [1.1.2] - 2026-04-22

### Changed

- 🔧 GitHub 仓库名改为 `hospital-vuln-scanner-mcp`（更规范）
- 🔧 更新所有文档中的 GitHub 链接

## [1.1.1] - 2026-04-22

### Added

- 📝 完善使用方法文档，添加场景化示例
- 📝 新增提示词指南（安全评估、定期巡检、等保合规、应急响应、资产盘点）
- 📝 新增扫描引擎说明（nmap/nuclei 自动检测机制）
- 📝 新增内置漏洞检测规则文档
- 📝 新增医疗系统指纹识别说明

### Changed

- 📝 README.md 重构为更完整的使用指南
- 📝 README_CN.md 中文版同步更新

## [1.1.0] - 2026-04-21

### Added

- ✨ 新增 `scanner.py` 真实扫描引擎
- ✨ 新增 nmap/nuclei 自动检测，有则用，没有自动回退到 Python
- ✨ 新增 Python 原生端口扫描（socket 多线程）
- ✨ 新增内置漏洞检测规则（MySQL/Redis/MongoDB/RDP 暴露检测）
- ✨ 新增医疗系统指纹识别（HIS/PACS/LIS/RIS/EMR）
- ✨ 新增 HTTP Banner 识别和厂商检测

### Changed

- 🔧 `start_scan` 现在返回真实扫描结果而非 Mock 数据
- 🔧 `scan_host_ports` 支持真实端口探测
- 🔧 `identify_medical_systems` 支持基于 Banner 的系统识别
- 🔧 `get_system_status` 显示 nmap/nuclei 可用状态

### Fixed

- 🐛 修复扫描任务创建后永远卡在 `running 0%` 的问题
- 🐛 修复扫描不执行任何实际检测的问题

## [1.0.0] - 2026-04-21

### Added

- 🎉 初始发布
- ✨ 14 个 MCP 工具（扫描管理、漏洞管理、网络工具、报告工具、系统工具）
- ✨ FastMCP 框架集成
- ✨ 支持 stdio/sse/http 三种传输模式
- ✨ 魔搭 MCP 广场上架
- ✨ PyPI 发布

---

## 版本说明

### 版本号格式

- **主版本号 (Major)**: 重大架构变更或不兼容更新
- **次版本号 (Minor)**: 新增功能，保持向下兼容
- **修订号 (Patch)**: Bug 修复和小改进

### 变更类型图标

| 图标 | 类型 | 说明 |
|------|------|------|
| ✨ | Added | 新增功能 |
| 🔧 | Changed | 功能变更 |
| 🐛 | Fixed | Bug 修复 |
| 📝 | Docs | 文档更新 |
| 🔒 | Security | 安全相关 |
| ⚠️ | Deprecated | 即将废弃 |
| 🗑️ | Removed | 已移除 |
