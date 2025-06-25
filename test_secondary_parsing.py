"""
Test script for the secondary parsing functionality.
Tests the extraction of clean anime titles from complex directory names.
"""

import os
import sys
import tempfile

# Add the parent directory to the path so we can import bangumi_parser
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bangumi_parser import BangumiParser


def test_secondary_parsing():
    """Test the secondary parsing functionality with various complex directory names."""
    print("Testing secondary parsing functionality...")
    
    # Test cases with complex directory names
    test_cases = [
        {
            'input': '[北宇治字幕组&LoliHouse] 坂本日常  SAKAMOTO DAYS [01-12][WebRip 1080p HEVC-10bit AACx2][简繁日内封字幕]',
            'expected': '坂本日常 SAKAMOTO DAYS'
        },
        {
            'input': '[Nekomoe kissaten&LoliHouse] Kanpekiseijo [01-12][WebRip 1080p HEVC-10bit AAC ASSx2]',
            'expected': 'Kanpekiseijo'
        },
        {
            'input': '[LoliHouse] Ore wa Subete wo Parry suru [01-12][WebRip 1080p HEVC-10bit AAC]',
            'expected': 'Ore wa Subete wo Parry suru'
        },
        {
            'input': '[Sakurato] Summer Pockets [01-10][AVC-8bit 1080p AAC][CHS]',
            'expected': 'Summer Pockets'
        },
        {
            'input': '【我推的孩子】 第一季',
            'expected': '【我推的孩子】 第一季'  # 现在应该保留季度信息
        },
        {
            'input': 'BanG Dream! Ave Mujica',
            'expected': 'BanG Dream! Ave Mujica'
        },
        {
            'input': '关于我转生变成史莱姆这档事 第三季',
            'expected': '关于我转生变成史莱姆这档事 第三季'  # 保留季度信息
        },
        {
            'input': '[VCB-Studio] 进击的巨人 最终季 [01-16][Ma10p_1080p][x265_flac]',
            'expected': '进击的巨人 最终季'
        },
        {
            'input': '[GM-Team][国漫][时光代理人][Shiguang Dailiren][2021][01-11 Fin][AVC][GB][1080P]',
            'expected': '时光代理人 Shiguang Dailiren'
        },
        {
            'input': '[ANi] 鬼灭之刃 刀匠村篇 [01-11][1080p][简体][招募翻译]',
            'expected': '鬼灭之刃 刀匠村篇'
        },
        # 新增季度测试用例
        {
            'input': '我推的孩子 第二季',
            'expected': '我推的孩子 第二季'
        },
        {
            'input': 'Attack on Titan Season 4',
            'expected': 'Attack on Titan Season 4'
        },
        {
            'input': '进击的巨人 第四部',
            'expected': '进击的巨人 第四部'
        }
    ]
    
    parser = BangumiParser()
    
    print("\n=== Secondary Parsing Test Results ===")
    passed = 0
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        input_title = test_case['input']
        expected = test_case['expected']
        
        # Test the _extract_clean_anime_title method directly
        result = parser._extract_clean_anime_title(input_title)
        
        status = "✓ PASS" if result == expected else "✗ FAIL"
        if result == expected:
            passed += 1
        
        print(f"{i:2}. {status}")
        print(f"    Input:    {input_title}")
        print(f"    Expected: {expected}")
        print(f"    Got:      {result}")
        if result != expected:
            print(f"    NOTE: Difference detected!")
        print()
    
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    return passed == total


def test_season_extraction():
    """Test the enhanced season extraction functionality."""
    print("\n=== Season Extraction Test ===")
    
    season_test_cases = [
        # Chinese numerals
        {'input': '我推的孩子 第一季', 'expected': 1},
        {'input': '进击的巨人 第二季', 'expected': 2},
        {'input': '鬼灭之刃 第三期', 'expected': 3},
        {'input': '某番剧 第四部', 'expected': 4},
        
        # Arabic numerals  
        {'input': '某系列 第1季', 'expected': 1},
        {'input': '某系列 第2期', 'expected': 2},
        {'input': '某系列 3季', 'expected': 3},
        
        # English patterns
        {'input': 'Attack on Titan Season 4', 'expected': 4},
        {'input': 'Some Series S01', 'expected': 1},
        {'input': 'Another Series S2', 'expected': 2},
        
        # No season info
        {'input': 'BanG Dream! Ave Mujica', 'expected': None},
        {'input': '坂本日常 SAKAMOTO DAYS', 'expected': None},
    ]
    
    parser = BangumiParser()
    
    print("Testing season extraction:")
    passed = 0
    total = len(season_test_cases)
    
    for i, test_case in enumerate(season_test_cases, 1):
        input_path = test_case['input']
        expected = test_case['expected']
        
        result = parser.extract_season_info(input_path)
        
        status = "✓ PASS" if result == expected else "✗ FAIL"
        if result == expected:
            passed += 1
        
        print(f"{i:2}. {status} - '{input_path}' -> Season {result} (expected {expected})")
    
    print(f"\nSeason extraction results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    return passed == total


def test_integration_with_season_preservation():
    """Test that seasons are properly preserved and separated after secondary parsing."""
    print("\n=== Season Preservation Integration Test ===")
    
    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory() as temp_dir:
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
        
        print("Parsed bangumi with preserved seasons:")
        for bangumi_name, info in bangumi_info.items():
            print(f"  {bangumi_name}: {info.season_count} seasons, {info.total_episodes} episodes")
            for season_num in sorted(info.seasons.keys()):
                season_info = info.seasons[season_num]
                print(f"    Season {season_num}: {season_info.episode_count} episodes")
        
        # Expected results
        expected_bangumi = ["我推的孩子", "关于我转生变成史莱姆这档事", "Attack on Titan"]
        expected_seasons = {
            "我推的孩子": 2,  # Should have 2 seasons
            "关于我转生变成史莱姆这档事": 2,  # Should have 2 seasons (1 and 3)
            "Attack on Titan": 2  # Should have 2 seasons (1 and 4)
        }
        
        success = True
        
        # Check if we have the right number of bangumi
        if len(bangumi_info) != len(expected_bangumi):
            print(f"✗ Expected {len(expected_bangumi)} bangumi, got {len(bangumi_info)}")
            success = False
        
        # Check season counts
        for bangumi_name, expected_season_count in expected_seasons.items():
            found_bangumi = None
            for name, info in bangumi_info.items():
                if bangumi_name in name:
                    found_bangumi = info
                    break
            
            if not found_bangumi:
                print(f"✗ Bangumi '{bangumi_name}' not found")
                success = False
                continue
            
            if found_bangumi.season_count != expected_season_count:
                print(f"✗ {bangumi_name}: expected {expected_season_count} seasons, got {found_bangumi.season_count}")
                success = False
            else:
                print(f"✓ {bangumi_name}: correctly has {found_bangumi.season_count} seasons")
        
        if success:
            print("✓ Season preservation integration test PASSED")
            return True
        else:
            print("✗ Season preservation integration test FAILED")
            return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing Secondary Parsing Functionality with Season Preservation")
    print("=" * 60)
    
    # Run the tests
    test1_passed = test_secondary_parsing()
    test2_passed = test_season_extraction()
    test3_passed = test_integration_with_season_preservation()
    
    print("\n" + "=" * 60)
    print("Overall Test Results:")
    print(f"Secondary Parsing Test: {'PASS' if test1_passed else 'FAIL'}")
    print(f"Season Extraction Test: {'PASS' if test2_passed else 'FAIL'}")
    print(f"Season Preservation Integration Test: {'PASS' if test3_passed else 'FAIL'}")
    
    if test1_passed and test2_passed and test3_passed:
        print("\n🎉 All tests PASSED! Secondary parsing with season preservation is working correctly.")
        return True
    else:
        print("\n❌ Some tests FAILED. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
