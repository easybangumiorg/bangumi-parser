# GitHub Actions 工作流说明

## 工作流概述

项目现在包含以下GitHub Actions工作流：

### 1. 持续集成 (CI) - `test.yml` 和 `python-package.yml`

**触发条件：**
- 推送到 `main` 分支
- 创建针对 `main` 分支的Pull Request

**功能：**
- 在多个操作系统 (Ubuntu, Windows, macOS) 上测试
- 支持多个Python版本 (3.10, 3.11, 3.12)
- 使用 `uv` 管理依赖
- 运行 pytest 测试
- 生成代码覆盖率报告
- 运行 flake8 代码质量检查

### 2. 预发布 - `prerelease.yml`

**触发条件：**
- 推送带有 `v*` 格式的标签 (如 `v1.0.0`, `v1.2.3-beta`)

**功能：**
- 运行完整的测试套件
- 构建Python包
- 验证包的完整性
- 自动创建GitHub预发布 (Pre-release)
- 上传构建的包文件作为发布资产

### 3. 正式发布到PyPI - `publish.yml`

**触发条件：**
- 将GitHub预发布标记为正式发布 (Published)

**功能：**
- 再次运行测试确保质量
- 构建Python包
- 验证包的完整性
- 自动上传到PyPI

## 使用流程

### 创建新版本的完整流程：

1. **开发完成后，为分支添加版本标签：**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **自动触发预发布流程：**
   - GitHub Actions会自动运行测试
   - 构建包并创建预发布
   - 您可以在GitHub Releases页面看到新的预发布

3. **测试预发布版本：**
   - 下载预发布的包文件进行测试
   - 确认所有功能正常工作

4. **发布到PyPI：**
   - 在GitHub Releases页面找到预发布
   - 点击"Edit release"
   - 取消勾选"This is a pre-release"
   - 点击"Update release"
   - 这将自动触发发布到PyPI的流程

## 环境配置要求

### PyPI令牌设置

在GitHub仓库设置中添加以下Secret：

1. 进入GitHub仓库的 Settings → Secrets and variables → Actions
2. 添加新的Repository Secret：
   - **Name:** `PYPI_API_TOKEN`
   - **Value:** 您的PyPI API令牌

### 获取PyPI API令牌：

1. 登录 [PyPI](https://pypi.org/)
2. 进入 Account settings → API tokens
3. 点击 "Add API token"
4. 选择 "Entire account" 或指定项目范围
5. 复制生成的令牌并添加到GitHub Secrets

## 版本号管理

- 建议使用语义化版本号 (Semantic Versioning)
- 格式：`vMAJOR.MINOR.PATCH` (如 `v1.0.0`)
- 预发布版本可以使用：`v1.0.0-alpha`, `v1.0.0-beta`, `v1.0.0-rc1`

## 故障排除

### 常见问题：

1. **测试失败**
   - 检查代码是否通过本地测试
   - 确保所有依赖都在 pyproject.toml 中正确声明

2. **PyPI上传失败**
   - 确认 PYPI_API_TOKEN 已正确设置
   - 检查包名是否已被占用
   - 确认版本号未重复

3. **预发布未创建**
   - 确认标签格式正确 (v*)
   - 检查GitHub Actions权限设置

### 本地测试命令：

```bash
# 安装依赖
uv sync --dev

# 运行测试
uv run pytest tests/ -v

# 构建包
uv build

# 检查包
uv run twine check dist/*
```

这样的工作流确保了代码质量，并提供了安全的发布流程，让您可以在正式发布前充分测试预发布版本。
