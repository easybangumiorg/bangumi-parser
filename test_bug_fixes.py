"""
Test script for the bug fixes in Bangumi Parser.
Tests the specific cases mentioned in the bug report.
"""

import os
import tempfile
from bangumi_parser import BangumiParser, BangumiConfig


def test_episode_extraction_fixes():
    """Test the episode extraction fixes."""
    print("Testing episode extraction fixes...")
    
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
        
        print(f"Found {len(series_info)} series:")
        parser.print_analysis_results()
        
        # Verify specific fixes
        
        # Check BanG Dream case
        bang_dream_found = False
        for info in series_info.values():
            if "BanG Dream" in info.series_name:
                bang_dream_found = True
                assert info.episode_count == 3, f"Expected 3 episodes for BanG Dream, got {info.episode_count}"
                print("✓ BanG Dream! Ave Mujica case fixed")
                break
        
        if not bang_dream_found:
            print("❌ BanG Dream! Ave Mujica case not found")
        
        # Check Hannibal case
        hannibal_found = False
        for info in series_info.values():
            if "Hannibal" in info.series_name or "汉尼拔" in info.series_name:
                hannibal_found = True
                assert info.series_name != "Season 01", f"Series name should not be 'Season 01', got '{info.series_name}'"
                assert info.season == 1, f"Expected season 1, got {info.season}"
                print(f"✓ Hannibal case fixed - Series: '{info.series_name}', Season: {info.season}")
                break
        
        if not hannibal_found:
            print("❌ Hannibal case not found")
        
        # Check Attack on Titan case
        aot_found = False
        for info in series_info.values():
            if "Attack on Titan" in info.series_name:
                aot_found = True
                assert info.season == 4, f"Expected season 4, got {info.season}"
                print(f"✓ Attack on Titan season detection working - Season: {info.season}")
                break
        
        if not aot_found:
            print("❌ Attack on Titan case not found")
        
        print("Episode extraction fixes test completed!")
        return True


def test_new_episode_patterns():
    """Test individual episode patterns."""
    print("\nTesting new episode patterns...")
    
    config = BangumiConfig()
    parser = BangumiParser(config)
    
    test_cases = [
        ("BanG Dream! Ave Mujica - 01.mkv", 1),
        ("Series Name - 05.mp4", 5),
        ("Show S01E10.mkv", 10),
        ("Movie.03.avi", 3),
        ("进击的巨人 第25话.mkv", 25),
        ("Animation Episode12.mp4", 12),
        ("Test_07_.mkv", 7),
        ("Series 08 Final.mp4", 8),
    ]
    
    for filename, expected_episode in test_cases:
        pattern, episode = parser.extract_series_info(filename)
        if episode == expected_episode:
            print(f"✓ {filename} -> Episode {episode}")
        else:
            print(f"❌ {filename} -> Expected {expected_episode}, got {episode}")
    
    print("Episode pattern testing completed!")


def test_season_extraction():
    """Test season extraction functionality."""
    print("\nTesting season extraction...")
    
    parser = BangumiParser()
    
    test_cases = [
        ("Hannibal/Season 01/episode.mp4", 1),
        ("Show/S02/show.mkv", 2),
        ("进击的巨人/第4季/episode.mkv", 4),
        ("Series/3季/episode.mp4", 3),
        ("Regular Series/episode.mkv", None),
        ("Show S05E01.mkv", 5),
    ]
    
    for path, expected_season in test_cases:
        season = parser.extract_season_info(path)
        if season == expected_season:
            print(f"✓ {path} -> Season {season}")
        else:
            print(f"❌ {path} -> Expected {expected_season}, got {season}")
    
    print("Season extraction testing completed!")


def run_bug_fix_tests():
    """Run all bug fix tests."""
    print("🔧 Running Bangumi Parser bug fix tests...\n")
    
    try:
        test_new_episode_patterns()
        test_season_extraction()
        test_episode_extraction_fixes()
        
        print("\n✅ All bug fix tests completed!")
        return True
    except Exception as e:
        print(f"\n❌ Bug fix test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_bug_fix_tests()
    exit(0 if success else 1)
