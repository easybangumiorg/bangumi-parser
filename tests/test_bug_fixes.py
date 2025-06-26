"""
Test bug fixes in Bangumi Parser.
Tests the specific cases mentioned in the bug report.
"""

import os
import tempfile
import pytest
from bangumi_parser import BangumiParser, BangumiConfig


class TestBugFixes:
    """Test various bug fixes."""

    def test_episode_extraction_fixes(self):
        """Test the episode extraction fixes."""
        # Create a temporary directory with test files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files for the specific cases mentioned
            test_files = [
                # Case 1: BanG Dream! Ave Mujica - 01.mkv format
                "BanG Dream! Ave Mujica - 01.mkv",
                "BanG Dream! Ave Mujica - 02.mkv",
                "BanG Dream! Ave Mujica - 03.mkv",

                # Case 2: Season directory structure
                os.path.join("Hannibal", "Season 01", "汉尼拔 (2013) S01E01.mp4"),
                os.path.join("Hannibal", "Season 01", "汉尼拔 (2013) S01E02.mp4"),
                os.path.join("Hannibal", "Season 01", "汉尼拔 (2013) S01E03.mp4"),

                # Additional test cases
                "Attack on Titan S4E01 [1080p].mkv",
                "Attack on Titan S4E02 [1080p].mkv",

                # Chinese season format
                os.path.join("进击的巨人", "第4季", "进击的巨人 第25话.mkv"),
                os.path.join("进击的巨人", "第4季", "进击的巨人 第26话.mkv"),
            ]

            # Create the test files
            for filename in test_files:
                filepath = os.path.join(temp_dir, filename)
                # Create directory if needed
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, 'w') as f:
                    f.write("dummy content")

            # Test parsing
            parser = BangumiParser()
            series_info = parser.parse(temp_dir)

            # Basic verification
            assert len(series_info) > 0, "Should find at least one series"

            # Check that we can find the expected series
            series_names = [info.series_name for info in series_info.values()]
            assert any(
                "BanG Dream" in name for name in series_names), "Should find BanG Dream series"

    def test_chinese_episode_patterns(self):
        """Test Chinese episode patterns."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_files = [
                "测试动画 第01话.mkv",
                "测试动画 第02话.mkv",
                "测试动画 第03话.mkv",
            ]

            for filename in test_files:
                filepath = os.path.join(temp_dir, filename)
                with open(filepath, 'w') as f:
                    f.write("dummy content")

            parser = BangumiParser()
            series_info = parser.parse(temp_dir)

            assert len(series_info) > 0, "Should find series with Chinese episode patterns"

            # Find the series and check episode count
            test_series = None
            for info in series_info.values():
                if "测试动画" in info.series_name:
                    test_series = info
                    break

            assert test_series is not None, "Should find the test series"
            assert test_series.episode_count == 3, f"Expected 3 episodes, got {test_series.episode_count}"

    def test_season_directory_structure(self):
        """Test parsing of season directory structures."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_files = [
                os.path.join("TestSeries", "Season 01", "TestSeries S01E01.mkv"),
                os.path.join("TestSeries", "Season 01", "TestSeries S01E02.mkv"),
                os.path.join("TestSeries", "Season 02", "TestSeries S02E01.mkv"),
                os.path.join("TestSeries", "Season 02", "TestSeries S02E02.mkv"),
            ]

            for filename in test_files:
                filepath = os.path.join(temp_dir, filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, 'w') as f:
                    f.write("dummy content")

            parser = BangumiParser()
            series_info = parser.parse(temp_dir)

            # Should find separate seasons
            assert len(series_info) >= 2, "Should find at least 2 seasons"

            # Check that seasons are properly identified
            season_counts = {}
            for info in series_info.values():
                if "TestSeries" in info.series_name:
                    season_counts[info.season] = season_counts.get(info.season, 0) + 1

            assert len(season_counts) >= 2, "Should identify multiple seasons"

    def test_episode_number_extraction(self):
        """Test extraction of episode numbers from various formats."""
        parser = BangumiParser()

        test_cases = [
            ("BanG Dream! Ave Mujica - 01.mkv", "01"),
            ("Attack on Titan S4E01 [1080p].mkv", "01"),
            ("汉尼拔 (2013) S01E01.mp4", "01"),
            ("进击的巨人 第25话.mkv", "25"),
            ("Test Series EP01.mkv", "01"),
            ("Another Series 第02话.mkv", "02"),
        ]

        for filename, expected_episode in test_cases:
            # Test the episode extraction directly
            # This would require exposing the episode extraction method
            # For now, we'll test through file parsing
            with tempfile.TemporaryDirectory() as temp_dir:
                filepath = os.path.join(temp_dir, filename)
                with open(filepath, 'w') as f:
                    f.write("dummy content")

                series_info = parser.parse(temp_dir)
                assert len(series_info) > 0, f"Should parse file: {filename}"

                # Check that episode was extracted
                series = list(series_info.values())[0]
                assert len(
                    series.episodes) > 0, f"Should extract episode from: {filename}"
                assert expected_episode in series.episodes, f"Should find episode {expected_episode} in {filename}"
