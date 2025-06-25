# Bangumi Parser

一个用于解析和组织动漫视频文件的Python库。

> [!IMPORTANT]
> 这个库是通过一系列的提示词和过程完全由AI生成的，AI有的时候会犯错，请注意甄别
> 
> 由于鬼知道AI从哪里扣来一部分代码（如Jellyfin），所以有版权问题请联系Ayala删除

## 功能特点

- 自动扫描指定目录中的视频文件
- 智能识别番剧系列和集数
- 提取字幕组、视频标签等元数据信息
- **番剧目录名二次解析** - 自动去除字幕组、画质等无关信息，提取真正的番剧名
- **智能合并同季重复内容**
- **多季番剧统一管理**
- **季度信息自动提取**
- 支持自定义配置文件
- 多种导出格式（JSON、CSV、播放列表）
- 可扩展的解析规则
- **未知集数智能重命名**

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

# 使用新的合并解析功能
parser = BangumiParser()
bangumi_info = parser.parse_and_merge(r"E:\Bangumi")
parser.print_bangumi_results(bangumi_info)

# 获取番剧统计信息
stats = get_bangumi_statistics(bangumi_info)
print(f"总共 {stats['total_bangumi']} 部番剧")
print(f"总共 {stats['total_seasons']} 季")
print(f"总共 {stats['total_episodes']} 集")
```

### 智能合并功能

新版本支持两种智能合并：

#### 1. 同季合并
自动合并同一系列、同一目录、同一季的重复内容：
```python
# 这些文件会被智能合并
# Attack on Titan/Season 1/AOT S01E01.mkv (较少集数)
# Attack on Titan/Season 1/Attack on Titan - 01 [1080p].mkv (较多集数，成为主集合)
# Attack on Titan/Season 1/AOT Special.mkv (未知集数，重命名为"未知集01")

parser = BangumiParser()
series_info = parser.parse("video_directory")
merged_series = parser.merge_same_season_series(series_info)
```

**合并规则：**
- 更多集数的优先（作为主集合）
- 解析出具体集数的优先于默认"00"
- 集数为"00"的重命名为"未知集01"、"未知集02"等

#### 2. 多季合并
将同一系列名称不同季的结果合并到BangumiInfo中：
```python
# 这些会被合并为一个番剧
# Attack on Titan/Season 1/...
# Attack on Titan/Season 2/...
# Attack on Titan/第3季/...

bangumi_info = parser.merge_multi_season_series(merged_series)
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
from bangumi_parser.utils import (
    export_to_json, export_bangumi_to_csv, 
    generate_bangumi_playlist, get_bangumi_statistics
)

# 导出番剧信息为JSON
export_to_json(bangumi_info, "bangumi_data.json")

# 导出番剧信息为CSV
export_bangumi_to_csv(bangumi_info, "bangumi_data.csv")

# 生成番剧播放列表（每个番剧和每季都有独立播放列表）
generate_bangumi_playlist(bangumi_info, scan_dir, "playlists")

# 获取详细统计信息
stats = get_bangumi_statistics(bangumi_info)
print(f"总共 {stats['total_bangumi']} 部番剧")
print(f"总共 {stats['total_seasons']} 季")
print(f"总共 {stats['total_episodes']} 集")
print(f"平均每部番剧 {stats['average_seasons_per_bangumi']:.1f} 季")

# 传统方式（兼容旧版本）
from bangumi_parser.utils import generate_playlist, get_series_statistics

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
- `- (\d{1,2})\.(?:mkv|mp4|...)` - **新增** Series Name - 01.mkv
- `S\d+E(\d{1,2})` - **新增** S01E01, S1E1
- `\.(\d{1,2})\.(?:mkv|mp4|...)` - **新增** Series.01.mkv
- `[Ee][Pp]?(\d{1,2})` - EP01, E01, ep01 等
- `第(\d{1,2})[话話集]` - 第01话, 第01集
- `(\d{1,2})[话話集]` - 01话, 01集
- `_(\d{1,2})_` - **新增** Series_01_
- `\s(\d{1,2})\s` - **新增** Series 01 (with spaces)
- `(?:第|Episode|Ep)(\d{1,2})` - **新增** 第01, Episode01, Ep01

### 季度识别模式

**新功能** - 自动识别季度信息：
- `S(\d{1,2})` - S01, S1
- `Season\s*(\d{1,2})` - Season 01, Season 1  
- `第(\d{1,2})[季期]` - 第1季, 第1期
- `(\d{1,2})[季期]` - 1季, 1期

## 番剧目录名二次解析

### 智能番剧名提取

库内置了智能的番剧目录名二次解析功能，能自动从包含字幕组、画质等信息的复杂文件夹名中提取真正的番剧名。

#### 支持的格式转换

**标准字幕组格式：**
```
[北宇治字幕组&LoliHouse] 坂本日常  SAKAMOTO DAYS [01-12][WebRip 1080p HEVC-10bit AACx2][简繁日内封字幕]
-> 坂本日常 SAKAMOTO DAYS

[Nekomoe kissaten&LoliHouse] Kanpekiseijo [01-12][WebRip 1080p HEVC-10bit AAC ASSx2]
-> Kanpekiseijo

[LoliHouse] Ore wa Subete wo Parry suru [01-12][WebRip 1080p HEVC-10bit AAC]
-> Ore wa Subete wo Parry suru
```

**多括号复杂格式：**
```
[GM-Team][国漫][时光代理人][Shiguang Dailiren][2021][01-11 Fin][AVC][GB][1080P]
-> 时光代理人 Shiguang Dailiren
```

**带季度信息：**
```
【我推的孩子】 第一季
-> 【我推的孩子】

关于我转生变成史莱姆这档事 第三季
-> 关于我转生变成史莱姆这档事
```

#### 过滤规则

自动过滤以下信息：
- **字幕组名称**：LoliHouse、Sakurato、北宇治字幕组等
- **画质信息**：1080p、720p、4K、WebRip、BDRip等
- **编码信息**：HEVC、AVC、x264、x265、10bit、8bit等
- **音频信息**：AAC、FLAC、AC3、DTS等
- **字幕信息**：简体、繁体、简繁、内封、外挂、字幕等
- **集数范围**：[01-12]、[01-24]等
- **技术标签**：SRTx2、ASSx2、CHS、CHT等

#### 使用方法

二次解析功能在解析过程中自动启用，无需额外配置：

```python
from bangumi_parser import BangumiParser

parser = BangumiParser()
series_info = parser.parse("your_anime_directory")

# 解析结果中的 series_name 已经是清理后的番剧名
for pattern, info in series_info.items():
    print(f"清理后的番剧名: {info.series_name}")
    print(f"原始目录名: {info.dir_name}")
```

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
- **`parse_and_merge(directory)`** - **新增** 完整的解析和合并流程
- **`merge_same_season_series(series_info)`** - **新增** 合并同季系列
- **`merge_multi_season_series(series_info)`** - **新增** 合并多季系列
- **`print_bangumi_results(bangumi_info)`** - **新增** 打印番剧合并结果

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
- **`season`** - **新增** 季度信息
- `release_group` - 字幕组
- `tags` - 标签列表
- `episode_count` - 集数
- `episodes` - 集数映射 ({"01": "path/to/episode.mkv"})

### BangumiInfo

**新增** - 番剧信息数据类，支持多季管理。

#### 属性

- `series_name` - 番剧名称
- `seasons` - 季度信息字典 (Dict[int, SeriesInfo])
- `total_episodes` - 总集数
- `season_count` - 季数
- `release_groups` - 所有字幕组列表
- `tags` - 所有标签列表

#### 方法

- `add_season(season_info)` - 添加季度信息
- `to_dict()` - 转换为字典格式

## 工具函数

### bangumi_parser.utils

#### 传统函数（兼容旧版本）
- `export_to_json(series_info, output_path)` - 导出为JSON
- `export_to_csv(series_info, output_path)` - 导出为CSV
- `generate_playlist(series_info, base_dir, output_dir)` - 生成播放列表
- `create_symlinks(series_info, target_dir, source_dir)` - 创建符号链接
- `get_series_statistics(series_info)` - 获取统计信息

#### 新增番剧函数
- **`export_bangumi_to_csv(bangumi_info, output_path)`** - 导出番剧信息为CSV
- **`get_bangumi_statistics(bangumi_info)`** - 获取番剧统计信息
- **`create_bangumi_symlinks(bangumi_info, target_dir, source_dir)`** - 创建番剧符号链接
- **`generate_bangumi_playlist(bangumi_info, base_dir, output_dir)`** - 生成番剧播放列表

#### 新增统计信息
`get_bangumi_statistics()` 返回：
- `total_bangumi` - 番剧总数
- `total_seasons` - 季度总数
- `total_episodes` - 总集数
- `season_distribution` - 季度分布统计
- `average_seasons_per_bangumi` - 平均每部番剧季数
- `average_episodes_per_bangumi` - 平均每部番剧集数
- `average_episodes_per_season` - 平均每季集数

## 示例

参见 `example_usage.py` 文件获取更多使用示例。

## 许可证

MIT License
