"""
Command line interface for Bangumi Parser.
"""

import argparse
import os
import sys
from bangumi_parser import BangumiParser, BangumiConfig
from bangumi_parser.utils import export_to_json, export_to_csv, export_bangumi_to_csv, get_series_statistics, get_bangumi_statistics


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Parse and organize anime video files")
    parser.add_argument("directory", help="Directory to scan for video files")
    parser.add_argument("--config", "-c", help="Path to custom configuration file")
    parser.add_argument("--output", "-o", help="Output file path for results")
    parser.add_argument("--format", "-f", choices=["json", "csv"], default="json",
                        help="Output format (default: json)")
    parser.add_argument("--stats", "-s", action="store_true", help="Show statistics")
    parser.add_argument("--merge", "-m", action="store_true", help="Merge series with the same name")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    # Check if directory exists and is accessible
    if not os.path.exists(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist.")
        sys.exit(1)
    
    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a directory.")
        sys.exit(1)
    
    if not os.access(args.directory, os.R_OK):
        print(f"Error: Directory '{args.directory}' is not readable.")
        sys.exit(1)
    
    # Validate output path if specified
    if args.output:
        output_dir = os.path.dirname(os.path.abspath(args.output))
        if not os.path.exists(output_dir):
            print(f"Error: Output directory '{output_dir}' does not exist.")
            sys.exit(1)
        if not os.access(output_dir, os.W_OK):
            print(f"Error: Output directory '{output_dir}' is not writable.")
            sys.exit(1)
    
    # Load configuration
    config = None
    if args.config:
        if os.path.exists(args.config):
            try:
                config = BangumiConfig(args.config)
                print(f"Loaded configuration from {args.config}")
            except Exception as e:
                print(f"Error loading configuration file '{args.config}': {e}")
                if args.verbose:
                    import traceback
                    traceback.print_exc()
                sys.exit(1)
        else:
            print(f"Warning: Configuration file '{args.config}' not found. Using default configuration.")
    
    # Create parser with new options
    bangumi_parser = BangumiParser(config)
    
    # Show parsing mode
    if args.verbose:
        mode = "merge mode" if args.merge else "standard mode"
        print(f"Starting analysis in {mode}...")
    
    # Initialize variables
    bangumi_info = None
    series_info = None
    
    try:
        if args.merge:
            bangumi_info = bangumi_parser.parse_and_merge(args.directory)
            if args.verbose:
                print(f"Found {len(bangumi_info)} unique series")
        else:
            series_info = bangumi_parser.parse(args.directory)
            if args.verbose:
                print(f"Found {len(series_info)} series directories")
    except Exception as e:
        print(f"Error during parsing: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    
    # Show results
    if args.merge and bangumi_info is not None:
        bangumi_parser.print_bangumi_results(bangumi_info)
    else:
        bangumi_parser.print_analysis_results()
    
    # Show statistics if requested
    if args.stats:
        if args.merge and bangumi_info is not None:
            stats = get_bangumi_statistics(bangumi_info)
        elif not args.merge and series_info is not None:
            stats = get_series_statistics(series_info)
        else:
            print("Error: No data available for statistics")
            sys.exit(1)
            
        print("\n=== Statistics ===")
        print(f"Total series: {stats['total_series']}")
        print(f"Total episodes: {stats['total_episodes']}")
        print(f"Average episodes per series: {stats['average_episodes_per_series']:.1f}")
        
        if stats.get('release_groups'):
            print("\nRelease groups:")
            for group, count in sorted(stats['release_groups'].items()):
                print(f"  {group}: {count} series")
        
        if stats.get('tags'):
            print("\nMost common tags:")
            sorted_tags = sorted(stats['tags'].items(), key=lambda x: x[1], reverse=True)
            for tag, count in sorted_tags[:10]:  # Show top 10
                print(f"  {tag}: {count}")
    
    # Export results if output file specified
    if args.output:
        try:
            # Check if we have data to export
            if args.merge and bangumi_info is not None:
                if args.format == "json":
                    export_to_json(bangumi_info, args.output)
                elif args.format == "csv":
                    export_bangumi_to_csv(bangumi_info, args.output)
            elif not args.merge and series_info is not None:
                if args.format == "json":
                    export_to_json(series_info, args.output)
                elif args.format == "csv":
                    export_to_csv(series_info, args.output)
            else:
                print("Error: No data available for export")
                sys.exit(1)
            
            print(f"\nResults exported to {args.output}")
            if args.verbose:
                file_size = os.path.getsize(args.output)
                print(f"File size: {file_size} bytes")
                mode_str = "merged bangumi data" if args.merge else "series data"
                print(f"Format: {args.format.upper()}, Content: {mode_str}")
        except Exception as e:
            print(f"Error exporting results: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    main()
