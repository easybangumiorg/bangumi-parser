"""
Example usage of Bangumi Parser library.
"""

import os
import pathlib
from bangumi_parser import BangumiParser, BangumiConfig
from bangumi_parser.utils import export_to_json, get_series_statistics, generate_playlist


def main():
    # Example 1: Using default configuration
    print("=== Example 1: Default Configuration ===")
    parser = BangumiParser()
    
    # Set the directory to scan (using Downloads folder as in original code)
    scan_dir = os.path.join(pathlib.Path.home(), "Downloads")
    
    try:
        # Parse the directory
        series_info = parser.parse(scan_dir)
        
        # Print results
        parser.print_analysis_results()
        
        # Get statistics
        stats = get_series_statistics(series_info)
        print(f"\nStatistics:")
        print(f"Total series: {stats['total_series']}")
        print(f"Total episodes: {stats['total_episodes']}")
        print(f"Average episodes per series: {stats['average_episodes_per_series']:.1f}")
        print(f"Release groups found: {list(stats['release_groups'].keys())}")
        
        # Example 4: Export functionality
        print("\n\n=== Example 4: Export Functionality ===")
        
        # Export to JSON
        json_output = "series_info.json"
        export_to_json(series_info, json_output)
        print(f"Series information exported to {json_output}")
        
        # Generate playlists
        playlist_dir = "playlists"
        if not os.path.exists(playlist_dir):
            os.makedirs(playlist_dir)
        generate_playlist(series_info, scan_dir, playlist_dir)
        print(f"Playlists generated in {playlist_dir} directory")
        
    except FileNotFoundError:
        print(f"Directory not found: {scan_dir}")
        print("Please modify the scan_dir variable to point to a valid directory.")
    
    # Example 2: Using custom configuration
    print("\n\n=== Example 2: Custom Configuration ===")
    
    # Load custom configuration
    config = BangumiConfig()
    
    # Add custom release groups
    config.add_release_group("MyCustomGroup")
    config.add_release_group("AnotherGroup")
    
    # Add custom tags
    config.add_tag("4K HDR")
    config.add_tag("Dolby Vision")
    
    # Add custom episode pattern
    config.add_episode_pattern(r'EP(\d{1,2})')  # Matches EP01, EP02, etc.
    
    # Create parser with custom config
    custom_parser = BangumiParser(config)
    
    print("Custom configuration loaded:")
    print(f"Release groups: {len(config.known_release_groups)} groups")
    print(f"Video tags: {len(config.common_tags)} tags")
    print(f"Episode patterns: {len(config.episode_patterns)} patterns")
    
    # Example 3: Loading configuration from file
    print("\n\n=== Example 3: Configuration from File ===")
    
    config_file = "config_example.json"
    if os.path.exists(config_file):
        file_config = BangumiConfig(config_file)
        file_parser = BangumiParser(file_config)
        print(f"Configuration loaded from {config_file}")
        print(f"Additional release groups from file: {file_config.known_release_groups[-2:]}")
    else:
        print(f"Config file {config_file} not found. Creating example...")
        config.save_config(config_file)
        print(f"Example configuration saved to {config_file}")
    
    # Example 4: Export functionality
    print("\n\n=== Example 4: Export Functionality ===")
    
    print("Export functionality is demonstrated in the try block above when parsing succeeds.")
    
    print("\n=== Examples completed ===")


if __name__ == "__main__":
    main()
