#!/usr/bin/env python3
"""
Test case specifically for full-width bracket handling.
This test ensures that full-width brackets 【】 are preserved as part of anime titles,
while half-width brackets [] are processed as technical information.
"""

import os
import re
import pytest

from bangumi_parser import BangumiParser, BangumiConfig


@pytest.mark.parametrize("input_str,expected,description", [
    ('【我推的孩子】', '【我推的孩子】', 'Simple title with full-width brackets'),
    ('【我推的孩子】 第一季', '【我推的孩子】 第一季', 'Title with full-width brackets and season'),
    ('[字幕组] 【我推的孩子】 [01-11][1080p]', '【我推的孩子】',
     'Mixed brackets: remove half-width tech info, keep full-width title'),
    ('[LoliHouse] 【我推的孩子】 第二季 [WebRip 1080p HEVC-10bit AACx2]',
     '【我推的孩子】 第二季', 'Complex case with mixed brackets and season info'),
    ('【间谍过家家】 SPY×FAMILY', '【间谍过家家】 SPY×FAMILY',
     'Title with full-width brackets and English name'),
    ('[北宇治字幕组] 【电锯人】 [01-12][WebRip 1080p]', '【电锯人】',
     'Fansub group with full-width title brackets'),
])
def test_full_width_brackets_preservation(input_str, expected, description):
    """Test that full-width brackets are preserved in anime titles."""
    config = BangumiConfig()
    parser = BangumiParser(config)
    result = parser._extract_clean_anime_title(input_str)
    assert result == expected, f"{description}: 输入='{input_str}', 期望='{expected}', 实际='{result}'"


@pytest.mark.parametrize("input_str,expected,description", [
    ('[字幕组] 进击的巨人 [01-12][1080p]', '进击的巨人',
     'Standard format with fansub group and tech info'),
    ('[LoliHouse] 坂本日常 SAKAMOTO DAYS [WebRip 1080p HEVC-10bit]',
     '坂本日常 SAKAMOTO DAYS', 'Complex title with quality info'),
    ('关于我转生变成史莱姆这档事 第三季', '关于我转生变成史莱姆这档事 第三季',
     'Title without brackets (should remain unchanged)'),
])
def test_half_width_brackets_removal(input_str, expected, description):
    """Test that half-width brackets are still processed correctly."""
    config = BangumiConfig()
    parser = BangumiParser(config)
    result = parser._extract_clean_anime_title(input_str)
    assert result == expected, f"{description}: 输入='{input_str}', 期望='{expected}', 实际='{result}'"


@pytest.mark.parametrize("filename,expected_series,description", [
    ('【我推的孩子】 01.mkv', '【我推的孩子】', 'Full-width brackets in filename with episode'),
    ('[LoliHouse] 【间谍过家家】 第二季 - 01 [WebRip 1080p].mkv',
     '【间谍过家家】 第二季', 'Mixed brackets with season info'),
    ('【电锯人】 Chainsaw Man - 12 [1080p].mkv', '【电锯人】 Chainsaw Man',
     'Full-width brackets with English title and quality'),
])
def test_integration_with_parsing(filename, expected_series, description):
    """Test the series name extraction logic with realistic filename cleaning."""
    config = BangumiConfig()
    parser = BangumiParser(config)

    # Remove extension and clean with _extract_clean_anime_title
    base_name = os.path.splitext(filename)[0]

    # Remove episode numbers first to get better title extraction
    clean_name = base_name
    for pattern in config.episode_patterns:
        clean_name = re.sub(pattern, ' ', clean_name, flags=re.IGNORECASE)

    # Apply the core cleaning logic
    series_name = parser._extract_clean_anime_title(clean_name.strip())

    assert series_name == expected_series, f"{description}: 文件名='{filename}', 期望='{expected_series}', 实际='{series_name}'"
