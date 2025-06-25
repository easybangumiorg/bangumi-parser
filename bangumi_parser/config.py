"""
Configuration module for Bangumi Parser.
Allows users to customize parsing behavior and add/modify metadata.
"""

import json
import os
from typing import Dict, List, Optional, Any


class BangumiConfig:
    """Configuration class for Bangumi Parser."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Path to custom configuration file
        """
        self.config_path = config_path
        self._load_default_config()
        if config_path and os.path.exists(config_path):
            self._load_custom_config(config_path)
    
    def _load_default_config(self):
        """Load default configuration."""
        self.video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm']
        
        self.known_release_groups = [
            'LoliHouse', 'Sakurato', 'Nekomoe kissaten', 'ANi', 'NC-Raws',
            'Leopard-Raws', 'VCB-Studio', 'SweetSub', 'Lilith-Raws',
            'GM-Team', 'MCE', 'KTXP', 'Crimson', 'Philosophy-Raws'
        ]
        
        self.common_tags = [
            'WebRip', 'BDRip', 'HEVC', 'AVC', 'x264', 'x265',
            '10bit', '8bit', '1080p', '720p', '480p', '4K',
            'AAC', 'FLAC', 'AC3', 'DTS', 'SRTx2', 'ASSx2',
            'CHS', 'CHT', 'JP', 'ENG', 'GB', 'BIG5'
        ]
        
        self.bracket_patterns = [
            r'\[(.*?)\]',    # Square brackets
            r'\((.*?)\)',    # Round brackets
            r'【(.*?)】',    # Full-width square brackets
            r'『(.*?)』',    # Full-width curly brackets
            r'\{(.*?)\}'     # Curly brackets
        ]
        
        self.episode_patterns = [
            r'[ \-_\[](\d{1,2})[ \-_\]]',  # Default pattern: - 01, [01], _01_
            r'[Ee][Pp]?(\d{1,2})',         # EP01, E01, ep01
            r'第(\d{1,2})[话話集]',          # 第01话, 第01集
            r'(\d{1,2})[话話集]',           # 01话, 01集
            r'- (\d{1,2})\.(?:mkv|mp4|avi|mov|wmv|flv|webm)',  # Series Name - 01.mkv
            r'S\d+E(\d{1,2})',             # S01E01, S1E1
            r'\.(\d{1,2})\.(?:mkv|mp4|avi|mov|wmv|flv|webm)',  # Series.01.mkv
            r'_(\d{1,2})_',                # Series_01_
            r'\s(\d{1,2})\s',              # Series 01 (with spaces)
            r'(?:第|Episode|Ep)(\d{1,2})',  # 第01, Episode01, Ep01
        ]
        
        # Season patterns for extracting season information
        self.season_patterns = [
            r'S(\d{1,2})',                 # S01, S1
            r'Season\s*(\d{1,2})',         # Season 01, Season 1
            r'第(\d{1,2})[季期]',           # 第1季, 第1期
            r'(\d{1,2})[季期]',            # 1季, 1期
        ]
        
        # Patterns to clean from series names
        self.cleanup_patterns = [
            r'\.mkv|\.mp4|\.avi|\.mov|\.wmv|\.flv|\.webm',  # Extensions
            r'\(\d{4}\)',  # Years in parentheses like (2013)
            r'\d{4}',  # Standalone years
            r'Season\s*\d+',  # Season markers (but not S01 format)
            r'第\d+[季期]',   # Chinese season markers
            r'\d+[季期]',     # Chinese season markers without 第
        ]
        
        # Directory patterns that should be ignored when extracting series names
        self.ignore_directory_patterns = [
            r'^Season\s*\d+$',  # Directories named exactly "Season 01", "Season 1", etc.
            r'^S\d+$',          # Directories named exactly "S01", "S1", etc.
            r'^第\d+[季期]$',    # Directories named exactly "第1季", "第1期", etc.
            r'^\d+[季期]$',      # Directories named exactly "1季", "1期", etc.
        ]
    
    def _load_custom_config(self, config_path: str):
        """Load custom configuration from JSON file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                custom_config = json.load(f)
            
            # Update configuration with custom values
            for key, value in custom_config.items():
                if hasattr(self, key):
                    if isinstance(getattr(self, key), list):
                        # For lists, extend with custom values
                        getattr(self, key).extend(value)
                    else:
                        # For other types, replace
                        setattr(self, key, value)
        except Exception as e:
            print(f"Warning: Failed to load custom config: {e}")
    
    def add_release_group(self, group_name: str):
        """Add a new release group to the configuration."""
        if group_name not in self.known_release_groups:
            self.known_release_groups.append(group_name)
    
    def add_tag(self, tag: str):
        """Add a new tag to the configuration."""
        if tag not in self.common_tags:
            self.common_tags.append(tag)
    
    def add_episode_pattern(self, pattern: str):
        """Add a new episode pattern to the configuration."""
        if pattern not in self.episode_patterns:
            self.episode_patterns.append(pattern)
    
    def save_config(self, output_path: str):
        """Save current configuration to JSON file."""
        config_data = {
            'video_extensions': self.video_extensions,
            'known_release_groups': self.known_release_groups,
            'common_tags': self.common_tags,
            'bracket_patterns': self.bracket_patterns,
            'episode_patterns': self.episode_patterns,
            'cleanup_patterns': self.cleanup_patterns
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
    
    def get_config_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary."""
        return {
            'video_extensions': self.video_extensions,
            'known_release_groups': self.known_release_groups,
            'common_tags': self.common_tags,
            'bracket_patterns': self.bracket_patterns,
            'episode_patterns': self.episode_patterns,
            'cleanup_patterns': self.cleanup_patterns
        }
