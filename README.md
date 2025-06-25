# Bangumi Parser

一个用于解析和组织动漫视频文件的Python库。

> [!IMPORTANT]
> 这个库是通过一系列的提示词和过程完全由AI生成的，AI有的时候会犯错，请注意甄别
> 由于鬼知道AI从哪里扣来一部分代码（如Jellyfin），所以有版权问题请联系Ayala删除

## 功能特点

- 自动扫描指定目录中的视频文件
- 智能识别番剧系列和集数
- 提取字幕组、视频标签等元数据信息
- 支持自定义配置文件
- 多种导出格式（JSON、CSV、播放列表）
- 可扩展的解析规则

## 安装

直接将 `bangumi_parser` 文件夹放入你的项目目录即可使用。

## 快速开始

### 基本使用

```python
from bangumi_parser import BangumiParser
import os
import pathlib

# 创建解析器实例
parser = BangumiParser()

# 扫描下载目录
scan_dir = os.path.join(pathlib.Path.home(), "Downloads")
series_info = parser.parse(scan_dir)

# 打印解析结果
parser.print_analysis_results()
```

**解析季**

```python
from bangumi_parser import BangumiParser, BangumiConfig, BangumiInfo
from bangumi_parser.utils import export_to_json, get_bangumi_statistics

parser = BangumiParser()
bangumi_info = parser.parse_and_merge(r"E:\Bangumi")
parser.print_bangumi_results(bangumi_info)
```

### 自定义配置

```python
from bangumi_parser import BangumiParser, BangumiConfig

# 创建自定义配置
config = BangumiConfig()

# 添加自定义字幕组
config.add_release_group("MyFavoriteGroup")
config.add_release_group("AnotherGroup")

# 添加自定义标签
config.add_tag("4K HDR")
config.add_tag("Dolby Vision")

# 添加自定义集数识别模式
config.add_episode_pattern(r'EP(\d{1,2})')  # 识别 EP01, EP02 等

# 使用自定义配置
parser = BangumiParser(config)
```

### 从配置文件加载

```python
from bangumi_parser import BangumiParser, BangumiConfig

# 从JSON文件加载配置
config = BangumiConfig("my_config.json")
parser = BangumiParser(config)
```

配置文件示例 (`my_config.json`)：

```json
{
  "known_release_groups": [
    "MyCustomGroup",
    "AnotherGroup"
  ],
  "common_tags": [
    "CustomTag",
    "4K HDR"
  ],
  "episode_patterns": [
    "第(\\d{1,2})[话話集]"
  ]
}
```

### 导出功能

```python
from bangumi_parser.utils import export_to_json, generate_playlist, get_series_statistics

# 导出为JSON
export_to_json(series_info, "series_data.json")

# 生成播放列表
generate_playlist(series_info, scan_dir, "playlists")

# 获取统计信息
stats = get_series_statistics(series_info)
print(f"总共 {stats['total_series']} 个系列")
print(f"总共 {stats['total_episodes']} 集")
```

## 配置选项

### 视频格式

默认支持的视频格式：`.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm`

### 字幕组识别

默认支持的字幕组：
- LoliHouse
- Sakurato
- Nekomoe kissaten
- ANi
- NC-Raws
- Leopard-Raws
- VCB-Studio
- 等等...

### 视频标签识别

默认支持的标签：
- 画质：1080p, 720p, 4K
- 编码：HEVC, AVC, x264, x265
- 音频：AAC, FLAC, AC3, DTS
- 字幕：CHS, CHT, JP, ENG
- 等等...

### 集数识别模式

默认支持的集数模式：
- `[ \-_\[](\d{1,2})[ \-_\]]` - 01, -01, [01] 等
- `[Ee][Pp]?(\d{1,2})` - EP01, E01, ep01 等
- `第(\d{1,2})[话話集]` - 第01话, 第01集
- `(\d{1,2})[话話集]` - 01话, 01集

## API 文档

### BangumiParser

主要的解析器类。

#### 方法

- `__init__(config=None)` - 初始化解析器
- `scan_directory(directory)` - 扫描目录中的视频文件
- `group_series()` - 按系列分组视频文件
- `analyze_series()` - 分析系列信息
- `parse(directory)` - 完整的解析流程
- `print_analysis_results()` - 打印解析结果

### BangumiConfig

配置管理类。

#### 方法

- `__init__(config_path=None)` - 初始化配置
- `add_release_group(group_name)` - 添加字幕组
- `add_tag(tag)` - 添加标签
- `add_episode_pattern(pattern)` - 添加集数模式
- `save_config(output_path)` - 保存配置到文件

### SeriesInfo

系列信息数据类。

#### 属性

- `series_name` - 系列名称
- `dir_name` - 目录名称
- `release_group` - 字幕组
- `tags` - 标签列表
- `episode_count` - 集数
- `episodes` - 集数映射 ({"01": "path/to/episode.mkv"})

## 工具函数

### bangumi_parser.utils

- `export_to_json(series_info, output_path)` - 导出为JSON
- `export_to_csv(series_info, output_path)` - 导出为CSV
- `generate_playlist(series_info, base_dir, output_dir)` - 生成播放列表
- `create_symlinks(series_info, target_dir, source_dir)` - 创建符号链接
- `get_series_statistics(series_info)` - 获取统计信息

## 示例

参见 `example_usage.py` 文件获取更多使用示例。

## 许可证

MIT License
