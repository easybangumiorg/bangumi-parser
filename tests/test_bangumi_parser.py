"""
Test basic functionality of Bangumi Parser.
"""

import os
import tempfile
import json
import pytest
from bangumi_parser import BangumiParser, BangumiConfig


class TestBasicFunctionality:
    """Test basic functionality of the parser."""

    def test_basic_parsing(self):
        """Test basic functionality of the parser."""
        # Create a temporary directory with test files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test video files
            test_files = [
                "Series A - 01 [Group1][1080p].mkv",
                "Series A - 02 [Group1][1080p].mkv",
                "Series A - 03 [Group1][1080p].mkv",
                "Series B EP01 [Group2][720p].mp4",
                "Series B EP02 [Group2][720p].mp4",
                "Different Series 第01话 [Group3][4K].mkv",
                "Different Series 第02话 [Group3][4K].mkv",
            ]

            for filename in test_files:
                filepath = os.path.join(temp_dir, filename)
                with open(filepath, 'w') as f:
                    f.write("dummy content")

            # Test parsing
            parser = BangumiParser()
            series_info = parser.parse(temp_dir)

            # Verify results
            assert len(
                series_info) >= 2, f"Expected at least 2 series, got {len(series_info)}"

            # Check that episodes are properly grouped
            total_episodes = sum(info.episode_count for info in series_info.values())
            assert total_episodes == len(
                test_files), f"Expected {len(test_files)} episodes, got {total_episodes}"

    def test_empty_directory(self):
        """Test parsing an empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            parser = BangumiParser()
            series_info = parser.parse(temp_dir)
            assert len(series_info) == 0

    def test_directory_with_non_video_files(self):
        """Test parsing directory with non-video files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create non-video files
            non_video_files = [
                "readme.txt",
                "subtitles.srt",
                "image.jpg",
                "document.pdf"
            ]

            for filename in non_video_files:
                filepath = os.path.join(temp_dir, filename)
                with open(filepath, 'w') as f:
                    f.write("dummy content")

            parser = BangumiParser()
            series_info = parser.parse(temp_dir)
            assert len(series_info) == 0


class TestCustomConfiguration:
    """Test custom configuration functionality."""

    def test_custom_config_creation(self):
        """Test creating custom configuration."""
        # Create custom configuration
        config = BangumiConfig()
        config.add_release_group("TestGroup")
        config.add_tag("TestTag")
        config.add_episode_pattern(r'EP(\d{1,2})')

        # Verify configuration
        assert "TestGroup" in config.known_release_groups
        assert "TestTag" in config.common_tags
        assert r'EP(\d{1,2})' in config.episode_patterns

    def test_parser_with_custom_config(self):
        """Test parser with custom configuration."""
        config = BangumiConfig()
        config.add_release_group("TestGroup")

        # Test parser with custom config
        parser = BangumiParser(config)
        assert parser.config == config

    def test_configuration_file_loading(self):
        """Test loading configuration from file."""
        # Create temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config_data = {
                "known_release_groups": ["FileGroup"],
                "common_tags": ["FileTag"],
                "episode_patterns": [r'Episode(\d{1,2})']
            }
            json.dump(config_data, f)
            config_file = f.name

        try:
            # Load configuration from file
            config = BangumiConfig(config_file)

            # Verify file configuration was loaded
            assert "FileGroup" in config.known_release_groups
            assert "FileTag" in config.common_tags

        finally:
            # Clean up
            os.unlink(config_file)

    def test_invalid_config_file(self):
        """Test handling of invalid configuration file."""
        with pytest.raises((FileNotFoundError, json.JSONDecodeError)):
            BangumiConfig("nonexistent_file.json")
