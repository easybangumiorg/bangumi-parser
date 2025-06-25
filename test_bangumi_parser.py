"""
Simple test for Bangumi Parser functionality.
"""

import os
import tempfile
from bangumi_parser import BangumiParser, BangumiConfig


def test_basic_functionality():
    """Test basic functionality of the parser."""
    print("Testing basic functionality...")
    
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
        assert len(series_info) >= 2, f"Expected at least 2 series, got {len(series_info)}"
        
        # Check that episodes are properly grouped
        total_episodes = sum(info.episode_count for info in series_info.values())
        assert total_episodes == len(test_files), f"Expected {len(test_files)} episodes, got {total_episodes}"
        
        print("✓ Basic functionality test passed")


def test_custom_configuration():
    """Test custom configuration functionality."""
    print("Testing custom configuration...")
    
    # Create custom configuration
    config = BangumiConfig()
    config.add_release_group("TestGroup")
    config.add_tag("TestTag")
    config.add_episode_pattern(r'EP(\d{1,2})')
    
    # Verify configuration
    assert "TestGroup" in config.known_release_groups
    assert "TestTag" in config.common_tags
    assert r'EP(\d{1,2})' in config.episode_patterns
    
    # Test parser with custom config
    parser = BangumiParser(config)
    assert parser.config == config
    
    print("✓ Custom configuration test passed")


def test_configuration_file():
    """Test loading configuration from file."""
    print("Testing configuration file loading...")
    
    # Create temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_data = {
            "known_release_groups": ["FileGroup"],
            "common_tags": ["FileTag"],
            "episode_patterns": [r'Episode(\d{1,2})']
        }
        import json
        json.dump(config_data, f)
        config_file = f.name
    
    try:
        # Load configuration from file
        config = BangumiConfig(config_file)
        
        # Verify file configuration was loaded
        assert "FileGroup" in config.known_release_groups
        assert "FileTag" in config.common_tags
        
        print("✓ Configuration file test passed")
    finally:
        # Clean up
        os.unlink(config_file)


def run_tests():
    """Run all tests."""
    print("Running Bangumi Parser tests...\n")
    
    try:
        test_basic_functionality()
        test_custom_configuration()
        test_configuration_file()
        
        print("\n✅ All tests passed!")
        return True
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
