"""
Bangumi Parser 配置模块。
允许用户自定义解析行为并添加/修改元数据。
"""

import json
import os
from typing import Dict, List, Optional, Any


class BangumiConfig:
    """Bangumi Parser 配置类。"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置。

        Args:
            config_path: 自定义配置文件路径
        """
        self.config_path = config_path
        self._load_default_config()
        if config_path and os.path.exists(config_path):
            self._load_custom_config(config_path)
        if config_path and not os.path.exists(config_path):
            raise FileNotFoundError(f"Can`t find Custom config file: {config_path}")

    def _load_default_config(self):
        """加载默认配置。"""
        # 中文数字映射表 - 用于将中文数字转换为阿拉伯数字，支持第一季、第二季等季度解析
        self.chinese_nums = {
            '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10
        }

        # 支持的视频文件扩展名 - 定义哪些文件类型被识别为视频文件进行解析
        self.video_extensions = [
            '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm'
        ]

        # 已知的发布组名称 - 用于识别和提取文件名中的制作组信息，帮助分类和过滤
        self.known_release_groups = [
            'NC-Raws', 'GM-Team', 'KTXP', 'Crimson',
            'SweetSub', 'Sakurato', 'Nekomoe kissaten',
            'ANi', 'Philosophy-Raws', 'LoliHouse', 'MCE',
            'VCB-Studio', '北宇治字幕组', 'Leopard-Raws',
            'Lilith-Raws', "桜都字幕组", "喵萌奶茶屋", "天香字幕社",
            "猪猪字幕组", "幻樱字幕组", "悠哈璃羽字幕社", "动漫国字幕组"
        ]

        # 常见标签 - 识别文件名中的质量、格式、语言等标识符，用于元数据提取
        self.common_tags = [
            'BDRip', 'ENG', '简繁', 'x265', 'x265_flac', 'WebRip',
            'FLAC', '繁体', '国漫', 'GB', '1080p', '480p', 'HEVC',
            '720p', '招募', 'CHT', 'AC3', 'CHS', '8bit', 'Ma10p',
            'ASSx2', 'SRTx2', 'Fin', 'BIG5', '10bit', '字幕', 'AAC',
            '外挂', '翻译', '内封', 'JP', 'DTS', '简体', 'x264', 'AVC',
            '4K', "BD", "TV", "WEB", "HDR", "杜比全景声"
        ]

        # 括号匹配模式 - 用于提取括号内的信息，如发布组名、标签等
        self.bracket_patterns = [
            r'\[(.*?)\]',    # 方括号
            r'\((.*?)\)',    # 圆括号
            r'【(.*?)】',    # 全角方括号
            r'『(.*?)』',    # 全角大括号
            r'\{(.*?)\}'     # 大括号
        ]

        # 集数识别模式 - 从文件名中提取集数信息的正则表达式，支持多种命名格式
        self.episode_patterns = [
            r'[ \-_\[](\d{1,2})[ \-_\]]',  # 默认模式: - 01, [01], _01_
            r'[Ee][Pp]?(\d{1,2})',         # EP01, E01, ep01
            r'第(\d{1,2})[话話集]',          # 第01话, 第01集
            r'(\d{1,2})[话話集]',           # 01话, 01集
            # 系列名称 - 01.mkv
            r'- (\d{1,2})\.(?:mkv|mp4|avi|mov|wmv|flv|webm)',
            r'S\d+E(\d{1,2})',             # S01E01, S1E1
            r'\.(\d{1,2})\.(?:mkv|mp4|avi|mov|wmv|flv|webm)',  # Series.01.mkv
            r'_(\d{1,2})_',                # Series_01_
            r'\s(\d{1,2})\s',              # Series 01 (带空格)
            r'(?:第|Episode|Ep)(\d{1,2})',  # 第01, Episode01, Ep01
            # 【SeriesName】01 (直接连接全角括号)
            r'】(\d{1,2})$',
            # SeriesName01 (直接连接在末尾)
            r'(\d{1,2})$',
        ]

        # 季度识别模式 - 从文件名或目录名中提取季度信息，支持中英文格式
        self.season_patterns = [
            r'S(\d{1,2})',                          # S01, S1, S2
            r'Season\s*(\d{1,2})',                  # Season 01, Season 1
            r'第(\d{1,2})[季期部]',                  # 第1季, 第1期, 第1部
            r'(\d{1,2})[季期部]',                   # 1季, 1期, 1部
            r'第([一二三四五六七八九十]+)[季期部]',      # 第一季, 第二期, 第三部
            r'([一二三四五六七八九十]+)[季期部]',       # 一季, 二期, 三部
        ]

        # 季度移除模式 - 从番剧名称中移除季度标识，获得干净的番剧标题
        self.season_removal_patterns = [
            r'\s+第[一二三四五六七八九十\d]+[季期部]$',  # 第一季, 第2期, 第三部
            r'\s+Season\s*\d+$',                      # Season 1, Season 4
            r'\s+S\d+$',                             # S1, S4
            r'\s+[一二三四五六七八九十\d]+[季期部]$',   # 一季, 2期, 三部 (无第)
        ]

        # 清理模式 - 从番剧名称中移除不必要的信息，如文件扩展名、年份等
        self.cleanup_patterns = [
            r'\.mkv|\.mp4|\.avi|\.mov|\.wmv|\.flv|\.webm',  # 扩展名
            r'\(\d{4}\)',  # 括号中的年份，如 (2013)
            r'\d{4}',  # 独立的年份
            r'Season\s*\d+',  # 季度标识（但不包括 S01 格式）
            r'第\d+[季期]',   # 中文季度标识
            r'\d+[季期]',     # 无第的中文季度标识
        ]

        # 忽略目录模式 - 提取番剧名称时应忽略的目录名称模式，避免将季度目录误认为番剧名
        self.ignore_directory_patterns = [
            # 精确命名为 "Season 01"、"Season 1" 等的目录
            r'^Season\s*\d+$',
            r'^S\d+$',          # 精确命名为 "S01"、"S1" 等的目录
            r'^第\d+[季期]$',    # 精确命名为 "第1季"、"第1期" 等的目录
            r'^\d+[季期]$',      # 精确命名为 "1季"、"1期" 等的目录
        ]
        
        self.unknown_prefix = "NC"  # 未知集数的前缀，用于标识未解析的集数

    def _load_custom_config(self, config_path: str):
        """从JSON文件加载自定义配置。"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                custom_config = json.load(f)

            # 使用自定义值更新配置
            for key, value in custom_config.items():
                if hasattr(self, key):
                    if isinstance(getattr(self, key), list):
                        # 对于列表，使用自定义值扩展
                        getattr(self, key).extend(value)
                    else:
                        # 对于其他类型，直接替换
                        setattr(self, key, value)
        except Exception as e:
            print(f"警告: 加载自定义配置失败: {e}")

    def set_chinese_num(self, num: str, value: int):
        """添加新的中文数字映射。"""
        if num not in self.chinese_nums:
            self.chinese_nums[num] = value

    def add_video_extension(self, extension: str):
        """向配置中添加新的视频文件扩展名。"""
        if extension not in self.video_extensions:
            self.video_extensions.append(extension)

    def add_release_group(self, group_name: str):
        """向配置中添加新的发布组。"""
        if group_name not in self.known_release_groups:
            self.known_release_groups.append(group_name)

    def add_tag(self, tag: str):
        """向配置中添加新的标签。"""
        if tag not in self.common_tags:
            self.common_tags.append(tag)

    def add_bracket_pattern(self, pattern: str):
        """向配置中添加新的括号模式。"""
        if pattern not in self.bracket_patterns:
            self.bracket_patterns.append(pattern)

    def add_episode_pattern(self, pattern: str):
        """向配置中添加新的集数模式。"""
        if pattern not in self.episode_patterns:
            self.episode_patterns.append(pattern)

    def add_season_pattern(self, pattern: str):
        """向配置中添加新的季度模式。"""
        if pattern not in self.season_patterns:
            self.season_patterns.append(pattern)

    def add_season_removal_pattern(self, pattern: str):
        """向配置中添加新的季度移除模式。"""
        if pattern not in self.season_removal_patterns:
            self.season_removal_patterns.append(pattern)

    def add_cleanup_pattern(self, pattern: str):
        """向配置中添加新的清理模式。"""
        if pattern not in self.cleanup_patterns:
            self.cleanup_patterns.append(pattern)

    def add_ignore_directory_pattern(self, pattern: str):
        """添加新的要忽略的目录模式。"""
        if pattern not in self.ignore_directory_patterns:
            self.ignore_directory_patterns.append(pattern)

    def save_config(self, output_path: str):
        """将当前配置保存到JSON文件。"""
        config_data = {
            'chinese_nums': self.chinese_nums,
            'video_extensions': self.video_extensions,
            'known_release_groups': self.known_release_groups,
            'common_tags': self.common_tags,
            'bracket_patterns': self.bracket_patterns,
            'episode_patterns': self.episode_patterns,
            'season_patterns': self.season_patterns,
            'season_removal_patterns': self.season_removal_patterns,
            'cleanup_patterns': self.cleanup_patterns,
            'ignore_directory_patterns': self.ignore_directory_patterns
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)

    def get_config_dict(self) -> Dict[str, Any]:
        """获取配置作为字典。"""
        return {
            'chinese_nums': self.chinese_nums,
            'video_extensions': self.video_extensions,
            'known_release_groups': self.known_release_groups,
            'common_tags': self.common_tags,
            'bracket_patterns': self.bracket_patterns,
            'episode_patterns': self.episode_patterns,
            'season_patterns': self.season_patterns,
            'season_removal_patterns': self.season_removal_patterns,
            'cleanup_patterns': self.cleanup_patterns,
            'ignore_directory_patterns': self.ignore_directory_patterns
        }
