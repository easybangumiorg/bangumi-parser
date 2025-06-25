"""
Command line interface for Bangumi Parser.
"""

import argparse
import json
import os
import sys
from bangumi_parser import BangumiParser, BangumiConfig
from bangumi_parser.utils import export_to_json, export_to_csv, get_series_statistics


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Parse and organize anime video files")
    parser.add_argument("directory", help="Directory to scan for video files")
    parser.add_argument("--config", "-c", help="Path to custom configuration file")
    parser.add_argument("--output", "-o", help="Output file path for results")
    parser.add_argument("--format", "-f", choices=["json", "csv"], default="json",
                        help="Output format (default: json)")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    parser.add_argument("--quiet", "-q", action="store_true", help="Quiet mode")
    
    args = parser.parse_args()
    
    # Check if directory exists
    if not os.path.exists(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist.")
        sys.exit(1)
    
    # Load configuration
    config = None
    if args.config:
        if os.path.exists(args.config):
            config = BangumiConfig(args.config)
            if not args.quiet:
                print(f"Loaded configuration from {args.config}")
        else:
            print(f"Warning: Configuration file '{args.config}' not found. Using default configuration.")
    
    # Create parser
    bangumi_parser = BangumiParser(config)
    
    # Parse directory
    if not args.quiet:
        print(f"Scanning directory: {args.directory}")
    
    try:
        series_info = bangumi_parser.parse(args.directory)
    except Exception as e:
        print(f"Error during parsing: {e}")
        sys.exit(1)
    
    # Show results
    if not args.quiet:
        bangumi_parser.print_analysis_results()
    
    # Show statistics if requested
    if args.stats:
        stats = get_series_statistics(series_info)
        print("\n=== Statistics ===")
        print(f"Total series: {stats['total_series']}")
        print(f"Total episodes: {stats['total_episodes']}")
        print(f"Average episodes per series: {stats['average_episodes_per_series']:.1f}")
        
        if stats['release_groups']:
            print("\nRelease groups:")
            for group, count in sorted(stats['release_groups'].items()):
                print(f"  {group}: {count} series")
        
        if stats['tags']:
            print("\nMost common tags:")
            sorted_tags = sorted(stats['tags'].items(), key=lambda x: x[1], reverse=True)
            for tag, count in sorted_tags[:10]:  # Show top 10
                print(f"  {tag}: {count}")
    
    # Export results if output file specified
    if args.output:
        try:
            if args.format == "json":
                export_to_json(series_info, args.output)
            elif args.format == "csv":
                export_to_csv(series_info, args.output)
            
            if not args.quiet:
                print(f"\nResults exported to {args.output}")
        except Exception as e:
            print(f"Error exporting results: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
