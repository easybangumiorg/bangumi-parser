"""
Test script for the secondary parsing functionality.
Tests the extraction of clean anime titles from complex directory names.
"""

import os
import tempfile
import pytest

from bangumi_parser import BangumiParser


@pytest.mark.parametrize("input_title,expected", [
    ('[北宇治字幕组&LoliHouse] 坂本日常  SAKAMOTO DAYS [01-12][WebRip 1080p HEVC-10bit AACx2][简繁日内封字幕]',
     '坂本日常 SAKAMOTO DAYS'),
    ('[Nekomoe kissaten&LoliHouse] Kanpekiseijo [01-12][WebRip 1080p HEVC-10bit AAC ASSx2]', 'Kanpekiseijo'),
    ('[LoliHouse] Ore wa Subete wo Parry suru [01-12][WebRip 1080p HEVC-10bit AAC]',
     'Ore wa Subete wo Parry suru'),
    ('[Sakurato] Summer Pockets [01-10][AVC-8bit 1080p AAC][CHS]', 'Summer Pockets'),
    ('【我推的孩子】 第一季', '【我推的孩子】 第一季'),
    ('BanG Dream! Ave Mujica', 'BanG Dream! Ave Mujica'),
    ('关于我转生变成史莱姆这档事 第三季', '关于我转生变成史莱姆这档事 第三季'),
    ('[VCB-Studio] 进击的巨人 最终季 [01-16][Ma10p_1080p][x265_flac]', '进击的巨人 最终季'),
    ('[GM-Team][国漫][时光代理人][Shiguang Dailiren][2021][01-11 Fin][AVC][GB][1080P]',
     '时光代理人 Shiguang Dailiren'),
    ('[ANi] 鬼灭之刃 刀匠村篇 [01-11][1080p][简体][招募翻译]', '鬼灭之刃 刀匠村篇'),
    ('我推的孩子 第二季', '我推的孩子 第二季'),
    ('Attack on Titan Season 4', 'Attack on Titan Season 4'),
    ('进击的巨人 第四部', '进击的巨人 第四部'),
])
def test_secondary_parsing(input_title, expected):
    """Test the secondary parsing functionality with various complex directory names."""
    parser = BangumiParser()
    result = parser._extract_clean_anime_title(input_title)
    assert result == expected, f"输入: {input_title}，期望: {expected}，实际: {result}"


@pytest.mark.parametrize("input_path,expected", [
    # Chinese numerals
    ('我推的孩子 第一季', 1),
    ('进击的巨人 第二季', 2),
    ('鬼灭之刃 第三期', 3),
    ('某番剧 第四部', 4),
    # Arabic numerals
    ('某系列 第1季', 1),
    ('某系列 第2期', 2),
    ('某系列 3季', 3),
    # English patterns
    ('Attack on Titan Season 4', 4),
    ('Some Series S01', 1),
    ('Another Series S2', 2),
    # No season info
    ('BanG Dream! Ave Mujica', None),
    ('坂本日常 SAKAMOTO DAYS', None),
])
def test_season_extraction(input_path, expected):
    """Test the enhanced season extraction functionality."""
    parser = BangumiParser()
    result = parser.extract_season_info(input_path)
    assert result == expected, f"输入: {input_path}，期望: {expected}，实际: {result}"


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


def test_integration_with_season_preservation(temp_dir):
    """Test that seasons are properly preserved and separated after secondary parsing."""
    # Create test directory structure with different seasons
    test_structure = [
        "我推的孩子 第一季/我推的孩子 第一季 - 01.mkv",
        "我推的孩子 第二季/我推的孩子 第二季 - 01.mkv",
        "我推的孩子 第二季/我推的孩子 第二季 - 02.mkv",
        "关于我转生变成史莱姆这档事 第一季/关于我转生变成史莱姆这档事 第一季 - 01.mkv",
        "关于我转生变成史莱姆这档事 第三季/关于我转生变成史莱姆这档事 第三季 - 01.mkv",
        "Attack on Titan Season 1/Attack on Titan S01E01.mkv",
        "Attack on Titan Season 4/Attack on Titan S04E01.mkv",
    ]

    # Create the test files
    for file_path in test_structure:
        full_path = os.path.join(temp_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write("dummy content")

    # Parse the directory using the new merge functionality
    parser = BangumiParser()
    bangumi_info = parser.parse_and_merge(temp_dir)

    # Expected results
    expected_seasons = {
        "我推的孩子": 2,  # Should have 2 seasons
        "关于我转生变成史莱姆这档事": 2,  # Should have 2 seasons (1 and 3)
        "Attack on Titan": 2  # Should have 2 seasons (1 and 4)
    }

    # Check if we have the right number of bangumi
    assert len(bangumi_info) == len(
        expected_seasons), f"期望 {len(expected_seasons)} 个番剧，实际获得 {len(bangumi_info)} 个"

    # Check season counts
    for bangumi_name, expected_season_count in expected_seasons.items():
        found_bangumi = None
        for name, info in bangumi_info.items():
            if bangumi_name in name:
                found_bangumi = info
                break

        assert found_bangumi is not None, f"番剧 '{bangumi_name}' 未找到"
        assert found_bangumi.season_count == expected_season_count, f"{bangumi_name}: 期望 {expected_season_count} 季，实际 {found_bangumi.season_count} 季"
