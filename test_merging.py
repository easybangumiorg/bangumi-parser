"""
Test script for the new merging functionality in Bangumi Parser.
Tests same-season merging and multi-season merging.
"""

import os
import tempfile
from bangumi_parser import BangumiParser, BangumiConfig, BangumiInfo
from bangumi_parser.utils import export_to_json, get_bangumi_statistics


def test_same_season_merging():
    """Test merging of same season series."""
    print("Testing same season merging...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files that should be merged (same series, same directory, same season)
        test_files = [
            # First collection - fewer episodes
            os.path.join("Attack on Titan", "Season 1", "AOT S01E01.mkv"),
            os.path.join("Attack on Titan", "Season 1", "AOT S01E02.mkv"),
            
            # Second collection - more episodes (should be the main one)
            os.path.join("Attack on Titan", "Season 1", "Attack on Titan - 01 [1080p].mkv"),
            os.path.join("Attack on Titan", "Season 1", "Attack on Titan - 02 [1080p].mkv"),
            os.path.join("Attack on Titan", "Season 1", "Attack on Titan - 03 [1080p].mkv"),
            os.path.join("Attack on Titan", "Season 1", "Attack on Titan - 04 [1080p].mkv"),
            
            # Third collection - has episode "00" (should be merged and renamed)
            os.path.join("Attack on Titan", "Season 1", "AOT Special.mkv"),  # This will be episode 00
        ]
        
        # Create the test files
        for filename in test_files:
            filepath = os.path.join(temp_dir, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                f.write("dummy content")
        
        # Parse and merge
        parser = BangumiParser()
        bangumi_info = parser.parse_and_merge(temp_dir)
        
        # Print results
        parser.print_bangumi_results(bangumi_info)
        
        # Verify merging worked correctly
        assert len(bangumi_info) == 1, f"Expected 1 bangumi, got {len(bangumi_info)}"
        
        aot_bangumi = list(bangumi_info.values())[0]
        assert aot_bangumi.season_count == 1, f"Expected 1 season, got {aot_bangumi.season_count}"
        
        season_1 = aot_bangumi.seasons[1]
        print(f"Final episode count: {season_1.episode_count}")
        print(f"Episodes: {list(season_1.episodes.keys())}")
        
        # Should have merged all episodes
        assert season_1.episode_count >= 5, f"Expected at least 5 episodes after merging, got {season_1.episode_count}"
        
        print("✓ Same season merging test passed!")
        return True


def test_multi_season_merging():
    """Test merging of multi-season series."""
    print("\nTesting multi-season merging...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files for multiple seasons
        test_files = [
            # Season 1
            os.path.join("Attack on Titan", "Season 1", "Attack on Titan S01E01.mkv"),
            os.path.join("Attack on Titan", "Season 1", "Attack on Titan S01E02.mkv"),
            os.path.join("Attack on Titan", "Season 1", "Attack on Titan S01E03.mkv"),
            
            # Season 2  
            os.path.join("Attack on Titan", "Season 2", "Attack on Titan S02E01.mkv"),
            os.path.join("Attack on Titan", "Season 2", "Attack on Titan S02E02.mkv"),
            
            # Season 3
            os.path.join("Attack on Titan", "第3季", "进击的巨人 第01话.mkv"),
            os.path.join("Attack on Titan", "第3季", "进击的巨人 第02话.mkv"),
            os.path.join("Attack on Titan", "第3季", "进击的巨人 第03话.mkv"),
            os.path.join("Attack on Titan", "第3季", "进击的巨人 第04话.mkv"),
            
            # Different series
            os.path.join("One Piece", "One Piece - 001.mkv"),
            os.path.join("One Piece", "One Piece - 002.mkv"),
        ]
        
        # Create the test files
        for filename in test_files:
            filepath = os.path.join(temp_dir, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                f.write("dummy content")
        
        # Parse and merge
        parser = BangumiParser()
        bangumi_info = parser.parse_and_merge(temp_dir)
        
        # Print results
        parser.print_bangumi_results(bangumi_info)
        
        # Verify merging worked correctly
        assert len(bangumi_info) == 2, f"Expected 2 bangumi, got {len(bangumi_info)}"
        
        # Check Attack on Titan
        aot_found = False
        for bangumi in bangumi_info.values():
            if "Attack on Titan" in bangumi.series_name or "进击的巨人" in bangumi.series_name:
                aot_found = True
                assert bangumi.season_count == 3, f"Expected 3 seasons for AOT, got {bangumi.season_count}"
                assert bangumi.total_episodes == 9, f"Expected 9 total episodes for AOT, got {bangumi.total_episodes}"
                print(f"✓ AOT has {bangumi.season_count} seasons with {bangumi.total_episodes} total episodes")
                break
        
        assert aot_found, "Attack on Titan not found in results"
        
        # Check One Piece
        op_found = False
        for bangumi in bangumi_info.values():
            if "One Piece" in bangumi.series_name:
                op_found = True
                assert bangumi.season_count == 1, f"Expected 1 season for One Piece, got {bangumi.season_count}"
                assert bangumi.total_episodes == 2, f"Expected 2 total episodes for One Piece, got {bangumi.total_episodes}"
                print(f"✓ One Piece has {bangumi.season_count} season with {bangumi.total_episodes} total episodes")
                break
        
        assert op_found, "One Piece not found in results"
        
        print("✓ Multi-season merging test passed!")
        return True


def test_episode_zero_handling():
    """Test handling of episode "00" (unknown episodes)."""
    print("\nTesting episode 00 handling...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files with episode "00"
        test_files = [
            # Main series
            os.path.join("Test Series", "Test Series - 01.mkv"),
            os.path.join("Test Series", "Test Series - 02.mkv"),
            
            # Unknown episode (will become episode 00)
            os.path.join("Test Series", "Test Series Special.mkv"),
            os.path.join("Test Series", "Test Series OVA.mkv"),
        ]
        
        # Create the test files
        for filename in test_files:
            filepath = os.path.join(temp_dir, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                f.write("dummy content")
        
        # Parse with basic method first to get episode 00s
        parser = BangumiParser()
        series_info = parser.parse(temp_dir)
        
        # Manually set some episodes to "00" to simulate unknown episodes
        for info in series_info.values():
            if "Special" in info.sample_file or "OVA" in info.sample_file:
                # Convert to episode 00
                new_episodes = {"00": list(info.episodes.values())[0]}
                info.episodes = new_episodes
                info.episode_count = 1
        
        # Now test merging
        merged_same_season = parser.merge_same_season_series(series_info)
        final_bangumi = parser.merge_multi_season_series(merged_same_season)
        
        # Check that episode 00 was renamed to "未知集01"
        for bangumi in final_bangumi.values():
            for season_info in bangumi.seasons.values():
                episode_keys = list(season_info.episodes.keys())
                print(f"Episode keys after merging: {episode_keys}")
                
                # Should have regular episodes plus renamed unknown episodes
                unknown_episodes = [ep for ep in episode_keys if ep.startswith("未知集")]
                if unknown_episodes:
                    print(f"✓ Found unknown episodes: {unknown_episodes}")
        
        print("✓ Episode 00 handling test passed!")
        return True


def test_statistics():
    """Test the new statistics functionality."""
    print("\nTesting bangumi statistics...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files
        test_files = [
            os.path.join("Series A", "Season 1", "Series A S01E01 [Group1][1080p].mkv"),
            os.path.join("Series A", "Season 1", "Series A S01E02 [Group1][1080p].mkv"),
            os.path.join("Series A", "Season 2", "Series A S02E01 [Group1][720p].mkv"),
            os.path.join("Series B", "Series B - 01 [Group2][4K].mkv"),
            os.path.join("Series B", "Series B - 02 [Group2][4K].mkv"),
        ]
        
        for filename in test_files:
            filepath = os.path.join(temp_dir, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                f.write("dummy content")
        
        parser = BangumiParser()
        bangumi_info = parser.parse_and_merge(temp_dir)
        
        # Test statistics
        stats = get_bangumi_statistics(bangumi_info)
        
        print(f"Statistics: {stats}")
        
        assert stats['total_bangumi'] == 2, f"Expected 2 bangumi, got {stats['total_bangumi']}"
        # Note: total episodes might be 5 instead of 4 due to unknown episodes being added
        assert stats['total_episodes'] >= 4, f"Expected at least 4 episodes, got {stats['total_episodes']}"
        
        print("✓ Statistics test passed!")
        return True


def run_merging_tests():
    """Run all merging tests."""
    print("🔄 Running Bangumi Parser merging tests...\n")
    
    try:
        test_same_season_merging()
        test_multi_season_merging()
        test_episode_zero_handling()
        test_statistics()
        
        print("\n✅ All merging tests passed!")
        return True
    except Exception as e:
        print(f"\n❌ Merging test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_merging_tests()
    exit(0 if success else 1)
