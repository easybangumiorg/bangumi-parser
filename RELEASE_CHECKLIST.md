# 发布检查清单

在发布新版本之前，请确保完成以下检查：

## 📋 发布前检查清单

### 1. 代码质量检查
- [ ] 所有测试通过
- [ ] 代码风格检查通过 (black, flake8)
- [ ] 类型检查通过 (mypy)
- [ ] 没有明显的安全问题

### 2. 版本管理
- [ ] 更新 `src/bangumi_parser/__init__.py` 中的版本号
- [ ] 更新 `pyproject.toml` 中的版本号
- [ ] 版本号遵循语义化版本控制 (SemVer)

### 3. 文档更新
- [ ] README.md 内容是最新的
- [ ] CHANGELOG.md 已更新（如果存在）
- [ ] 所有新功能都有相应的文档说明

### 4. 测试覆盖
- [ ] 核心功能有单元测试
- [ ] 新功能有对应的测试用例
- [ ] 测试覆盖率达到合理水平

### 5. 依赖检查
- [ ] `pyproject.toml` 中的依赖是最新的
- [ ] 没有不必要的依赖
- [ ] Python 版本要求是合理的

## 🚀 发布步骤

### 本地发布（推荐用于测试）

1. **安装发布工具**
   ```bash
   pip install build twine
   ```

2. **清理旧的构建文件**
   ```bash
   rm -rf build/ dist/ *.egg-info/
   ```

3. **构建包**
   ```bash
   python -m build
   ```

4. **检查包**
   ```bash
   python -m twine check dist/*
   ```

5. **上传到 TestPyPI（测试）**
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```

6. **测试安装**
   ```bash
   pip install --index-url https://test.pypi.org/simple/ bangumi-parser
   ```

7. **上传到 PyPI（正式发布）**
   ```bash
   python -m twine upload dist/*
   ```

### 使用发布脚本

```bash
# 构建并检查包
python release.py

# 上传到 TestPyPI
python release.py --test

# 上传到 PyPI
python release.py --release

# 同时上传到 TestPyPI 和 PyPI
python release.py --test --release
```

### GitHub Actions 自动发布

1. 在 GitHub 仓库设置中添加 PyPI API token
   - 设置名称：`PYPI_API_TOKEN`
   - 值：你的 PyPI API token

2. 创建 GitHub Release
   - GitHub Actions 会自动触发发布流程

## 🔧 配置说明

### PyPI API Token 设置

1. 访问 [PyPI Account Settings](https://pypi.org/manage/account/)
2. 滚动到 "API tokens" 部分
3. 点击 "Add API token"
4. 选择作用域（推荐选择特定项目）
5. 复制生成的 token

### TestPyPI 配置（可选）

如果要使用 TestPyPI 进行测试：

1. 在 [TestPyPI](https://test.pypi.org/) 注册账号
2. 获取 API token
3. 添加到 GitHub Secrets（名称：`TEST_PYPI_API_TOKEN`）

## 📝 发布后步骤

- [ ] 验证包在 PyPI 上可以正常安装
- [ ] 创建 GitHub Release（如果使用手动发布）
- [ ] 更新项目文档
- [ ] 通知用户新版本发布

## 🚨 常见问题

### 版本冲突
- 确保版本号是唯一的，不能重复发布相同版本号

### 构建失败
- 检查 `pyproject.toml` 配置
- 确保所有必需的文件都存在

### 上传失败
- 检查 API token 是否正确
- 确保有上传权限
- 检查网络连接

## 📚 参考资源

- [Python Packaging User Guide](https://packaging.python.org/)
- [Semantic Versioning](https://semver.org/)
- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
