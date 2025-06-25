#!/usr/bin/env python3
"""
Test case specifically for full-width bracket handling.
This test ensures that full-width brackets 【】 are preserved as part of anime titles,
while half-width brackets [] are processed as technical information.
"""

import sys
import os
import re

# Add parent directory to path for importing bangumi_parser
sys.path.insert(0, os.path.abspath('.'))

from bangumi_parser import BangumiParser, BangumiConfig


def test_full_width_brackets_preservation():
    """Test that full-width brackets are preserved in anime titles."""
    print("=== Testing Full-Width Bracket Preservation ===")
    
    config = BangumiConfig()
    parser = BangumiParser(config)
    
    # Test cases with full-width brackets that should be preserved
    test_cases = [
        {
            'input': '【我推的孩子】',
            'expected': '【我推的孩子】',
            'description': 'Simple title with full-width brackets'
        },
        {
            'input': '【我推的孩子】 第一季',
            'expected': '【我推的孩子】 第一季', 
            'description': 'Title with full-width brackets and season'
        },
        {
            'input': '[字幕组] 【我推的孩子】 [01-11][1080p]',
            'expected': '【我推的孩子】',
            'description': 'Mixed brackets: remove half-width tech info, keep full-width title'
        },
        {
            'input': '[LoliHouse] 【我推的孩子】 第二季 [WebRip 1080p HEVC-10bit AACx2]',
            'expected': '【我推的孩子】 第二季',
            'description': 'Complex case with mixed brackets and season info'
        },
        {
            'input': '【间谍过家家】 SPY×FAMILY',
            'expected': '【间谍过家家】 SPY×FAMILY',
            'description': 'Title with full-width brackets and English name'
        },
        {
            'input': '[北宇治字幕组] 【电锯人】 [01-12][WebRip 1080p]',
            'expected': '【电锯人】',
            'description': 'Fansub group with full-width title brackets'
        }
    ]
    
    success_count = 0
    
    for i, case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {case['description']}")
        print(f"Input: '{case['input']}'")
        
        # Use the internal method to test title cleaning
        result = parser._extract_clean_anime_title(case['input'])
        
        print(f"Expected: '{case['expected']}'")
        print(f"Result:   '{result}'")
        
        if result == case['expected']:
            print("✓ PASS")
            success_count += 1
        else:
            print("✗ FAIL")
    
    print(f"\n=== Summary ===")
    print(f"Passed: {success_count}/{len(test_cases)}")
    print(f"Success Rate: {success_count/len(test_cases)*100:.1f}%")
    
    return success_count == len(test_cases)


def test_half_width_brackets_removal():
    """Test that half-width brackets are still processed correctly."""
    print("\n=== Testing Half-Width Bracket Processing ===")
    
    config = BangumiConfig()
    parser = BangumiParser(config)
    
    # Test cases with half-width brackets that should be processed
    test_cases = [
        {
            'input': '[字幕组] 进击的巨人 [01-12][1080p]',
            'expected': '进击的巨人',
            'description': 'Standard format with fansub group and tech info'
        },
        {
            'input': '[LoliHouse] 坂本日常 SAKAMOTO DAYS [WebRip 1080p HEVC-10bit]',
            'expected': '坂本日常 SAKAMOTO DAYS',
            'description': 'Complex title with quality info'
        },
        {
            'input': '关于我转生变成史莱姆这档事 第三季',
            'expected': '关于我转生变成史莱姆这档事 第三季',
            'description': 'Title without brackets (should remain unchanged)'
        }
    ]
    
    success_count = 0
    
    for i, case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {case['description']}")
        print(f"Input: '{case['input']}'")
        
        result = parser._extract_clean_anime_title(case['input'])
        
        print(f"Expected: '{case['expected']}'")
        print(f"Result:   '{result}'")
        
        if result == case['expected']:
            print("✓ PASS")
            success_count += 1
        else:
            print("✗ FAIL")
    
    print(f"\n=== Summary ===")
    print(f"Passed: {success_count}/{len(test_cases)}")
    print(f"Success Rate: {success_count/len(test_cases)*100:.1f}%")
    
    return success_count == len(test_cases)


def test_integration_with_parsing():
    """Test the series name extraction logic with realistic filename cleaning."""
    print("\n=== Testing Integration with File Name Cleaning ===")
    
    config = BangumiConfig()  
    parser = BangumiParser(config)
    
    # Test realistic filename scenarios
    test_files = [
        {
            'filename': '【我推的孩子】 01.mkv',
            'expected_series': '【我推的孩子】',
            'description': 'Full-width brackets in filename with episode'
        },
        {
            'filename': '[LoliHouse] 【间谍过家家】 第二季 - 01 [WebRip 1080p].mkv',
            'expected_series': '【间谍过家家】 第二季',
            'description': 'Mixed brackets with season info'
        },
        {
            'filename': '【电锯人】 Chainsaw Man - 12 [1080p].mkv',
            'expected_series': '【电锯人】 Chainsaw Man',
            'description': 'Full-width brackets with English title and quality'
        }
    ]
    
    success_count = 0
    
    for i, case in enumerate(test_files, 1):
        print(f"\nIntegration Test {i}: {case['description']}")
        print(f"Filename: {case['filename']}")
        
        try:
            # Remove extension and clean with _extract_clean_anime_title
            base_name = os.path.splitext(case['filename'])[0]
            
            # Remove episode numbers first to get better title extraction
            clean_name = base_name
            for pattern in config.episode_patterns:
                clean_name = re.sub(pattern, ' ', clean_name, flags=re.IGNORECASE)
            
            # Apply the core cleaning logic
            series_name = parser._extract_clean_anime_title(clean_name.strip())
            
            print(f"Expected Series: '{case['expected_series']}'")
            print(f"Parsed Series:   '{series_name}'")
            
            if series_name == case['expected_series']:
                print("✓ PASS")
                success_count += 1
            else:
                print("✗ FAIL")
                
        except Exception as e:
            print(f"✗ ERROR: {e}")
    
    print(f"\n=== Integration Summary ===")  
    print(f"Passed: {success_count}/{len(test_files)}")
    print(f"Success Rate: {success_count/len(test_files)*100:.1f}%")
    
    return success_count == len(test_files)


if __name__ == "__main__":
    print("Testing Full-Width Bracket Handling")
    print("=" * 50)
    
    # Run all tests
    test1_pass = test_full_width_brackets_preservation()
    test2_pass = test_half_width_brackets_removal()  
    test3_pass = test_integration_with_parsing()
    
    print("\n" + "=" * 50)
    print("FINAL RESULTS:")
    print(f"Full-Width Bracket Preservation: {'PASS' if test1_pass else 'FAIL'}")
    print(f"Half-Width Bracket Processing:   {'PASS' if test2_pass else 'FAIL'}")
    print(f"Integration Test:                {'PASS' if test3_pass else 'FAIL'}")
    
    if test1_pass and test2_pass and test3_pass:
        print("\n🎉 All tests passed! Full-width bracket handling is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        sys.exit(1)
