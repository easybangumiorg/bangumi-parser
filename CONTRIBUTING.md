# 开发者指南

欢迎为 Bangumi Parser 项目贡献代码！

## 🛠️ 开发环境设置

### 1. 克隆仓库
```bash
git clone https://github.com/EasyBangumi/bangumi-parser.git
cd bangumi-parser
```

### 2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. 安装开发依赖
```bash
pip install -e ".[dev]"
```

## 🏗️ 项目结构

```
bangumi-parser/
├── src/
│   └── bangumi_parser/
│       ├── __init__.py
│       ├── cli.py          # 命令行接口
│       ├── config.py       # 配置管理
│       ├── core.py         # 核心解析逻辑
│       └── utils.py        # 工具函数
├── tests/                  # 测试文件
├── .github/
│   └── workflows/         # GitHub Actions
├── docs/                  # 文档（如果有）
├── pyproject.toml         # 项目配置
├── README.md
├── LICENSE
└── CHANGELOG.md           # 变更日志（如果有）
```

## 🧪 运行测试

### 运行所有测试
```bash
pytest
```

### 运行带覆盖率的测试
```bash
pytest --cov=src/bangumi_parser --cov-report=html
```

### 使用 tox 进行多环境测试
```bash
# 安装 tox
pip install tox

# 运行所有环境的测试
tox

# 运行特定环境
tox -e py310
tox -e lint
tox -e type-check
```

## 🎨 代码风格

项目使用以下工具来保持代码质量：

### Black（代码格式化）
```bash
# 格式化代码
black src/ tests/

# 检查格式
black --check src/ tests/
```

### Flake8（代码检查）
```bash
flake8 src/ tests/
```

### MyPy（类型检查）
```bash
mypy src/bangumi_parser
```

### 一次性运行所有检查
```bash
tox -e lint,type-check
```

## 📝 贡献流程

### 1. Fork 项目
在 GitHub 上 fork 这个项目

### 2. 创建功能分支
```bash
git checkout -b feature/your-feature-name
```

### 3. 开发和测试
- 编写代码
- 添加测试
- 确保所有测试通过
- 检查代码风格

### 4. 提交代码
```bash
git add .
git commit -m "Add: your feature description"
```

### 5. 推送到你的 fork
```bash
git push origin feature/your-feature-name
```

### 6. 创建 Pull Request
在 GitHub 上创建 Pull Request

## 🔧 本地开发技巧

### 1. 使用可编辑安装
```bash
pip install -e .
```
这样你可以直接测试你的修改，无需重新安装。

### 2. 运行 CLI 命令
```bash
# 直接运行
python -m bangumi_parser.cli /path/to/anime

# 或者如果安装了脚本
bangumi-parser /path/to/anime
```

### 3. 调试技巧
- 使用 `--verbose` 参数获取详细输出
- 在代码中添加 `print()` 或使用调试器
- 使用小的测试数据集进行快速测试

## 📦 发布新版本

请参考 [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) 了解完整的发布流程。

### 快速发布步骤
1. 更新版本号
2. 运行测试
3. 构建包：`python -m build`
4. 检查包：`python -m twine check dist/*`
5. 上传：`python -m twine upload dist/*`

## 🐛 调试指南

### 常见问题

1. **导入错误**
   - 确保使用 `-e` 安装了项目
   - 检查 Python 路径

2. **测试失败**
   - 检查测试数据是否正确
   - 确保所有依赖都已安装

3. **类型检查错误**
   - 添加必要的类型注解
   - 使用 `# type: ignore` 忽略不重要的错误

### 性能调优
- 使用 `cProfile` 进行性能分析
- 考虑缓存重复计算的结果
- 对于大量文件，使用多进程处理

## 📚 开发资源

### 有用的链接
- [Python Packaging Guide](https://packaging.python.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Documentation](https://black.readthedocs.io/)
- [MyPy Documentation](https://mypy.readthedocs.io/)

### 代码示例
查看 `example_usage.py` 和 `tests/` 目录了解如何使用 API。

## 🤝 社区

- 在 Issues 中报告 bug 或请求功能
- 在 Discussions 中进行一般讨论
- 遵循 [Code of Conduct](CODE_OF_CONDUCT.md)（如果有）

## 📧 联系方式

如果你有任何问题，可以：
- 创建 GitHub Issue
- 发邮件给维护者：support@easybangumi.org

感谢你的贡献！🎉
