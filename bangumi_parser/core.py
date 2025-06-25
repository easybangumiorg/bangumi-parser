"""
Core functionality for Bangumi Parser.
Handles video file discovery, series grouping, and metadata extraction.
"""

import os
import re
import pathlib
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Any

from .config import BangumiConfig


class SeriesInfo:
    """Data class to hold series information."""
    
    def __init__(self):
        self.dir_name: str = ""
        self.series_name: str = ""
        self.season: Optional[int] = None  # Add season information
        self.release_group: Optional[str] = None
        self.tags: List[str] = []
        self.episode_count: int = 0
        self.sample_file: str = ""
        self.episodes: Dict[str, str] = {}  # Format: {"01": "path/to/episode.mkv"}
        self.pattern: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'dir_name': self.dir_name,
            'series_name': self.series_name,
            'season': self.season,
            'release_group': self.release_group,
            'tags': self.tags,
            'episode_count': self.episode_count,
            'sample_file': self.sample_file,
            'episodes': self.episodes,
            'pattern': self.pattern
        }


class BangumiInfo:
    """Data class to hold complete bangumi information with multiple seasons."""
    
    def __init__(self):
        self.series_name: str = ""
        self.seasons: Dict[int, SeriesInfo] = {}  # season_number -> SeriesInfo
        self.total_episodes: int = 0
        self.season_count: int = 0
        self.release_groups: List[str] = []  # All release groups found
        self.tags: List[str] = []  # All tags found
    
    def add_season(self, season_info: SeriesInfo):
        """Add a season to this bangumi."""
        season_num = season_info.season or 1  # Default to season 1 if no season specified
        
        # If season already exists, merge episodes
        if season_num in self.seasons:
            existing = self.seasons[season_num]
            # Merge episodes
            existing.episodes.update(season_info.episodes)
            existing.episode_count = len(existing.episodes)
            # Update other info if needed
            if season_info.release_group and season_info.release_group not in self.release_groups:
                self.release_groups.append(season_info.release_group)
            for tag in season_info.tags:
                if tag not in self.tags:
                    self.tags.append(tag)
        else:
            self.seasons[season_num] = season_info
            if season_info.release_group and season_info.release_group not in self.release_groups:
                self.release_groups.append(season_info.release_group)
            for tag in season_info.tags:
                if tag not in self.tags:
                    self.tags.append(tag)
        
        # Update totals
        self.season_count = len(self.seasons)
        self.total_episodes = sum(info.episode_count for info in self.seasons.values())
        
        # Update series name if not set
        if not self.series_name:
            self.series_name = season_info.series_name
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        seasons_dict = {}
        for season_num, season_info in self.seasons.items():
            seasons_dict[f"season_{season_num}"] = season_info.to_dict()
        
        return {
            'series_name': self.series_name,
            'season_count': self.season_count,
            'total_episodes': self.total_episodes,
            'release_groups': self.release_groups,
            'tags': self.tags,
            'seasons': seasons_dict
        }


class BangumiParser:
    """Main parser class for anime video files."""
    
    def __init__(self, config: Optional[BangumiConfig] = None):
        """
        Initialize the parser.
        
        Args:
            config: BangumiConfig instance. If None, uses default configuration.
        """
        self.config = config or BangumiConfig()
        self.video_files: List[str] = []
        self.series_groups: Dict[str, List[Tuple[int, str]]] = defaultdict(list)
        self.series_info: Dict[str, SeriesInfo] = {}
    
    def scan_directory(self, directory: str) -> List[str]:
        """
        Scan directory for video files.
        
        Args:
            directory: Directory path to scan
            
        Returns:
            List of relative paths to video files
        """
        self.video_files = []
        
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, directory)
                if any(file.lower().endswith(ext) for ext in self.config.video_extensions):
                    self.video_files.append(rel_path)
        
        return self.video_files
    
    def extract_series_info(self, filename: str) -> Tuple[str, int]:
        """
        Extract series pattern and episode number from filename.
        
        Args:
            filename: The filename to analyze
            
        Returns:
            Tuple of (series_pattern, episode_number)
        """
        # Get just the filename without path
        base_filename = os.path.basename(filename)
        
        # Try each episode pattern in order of specificity
        for pattern in self.config.episode_patterns:
            match = re.search(pattern, base_filename, re.IGNORECASE)
            if match:
                episode_num = int(match.group(1))
                # Replace the episode number with a placeholder
                series_pattern = re.sub(pattern, ' {EP_NUM} ', filename, flags=re.IGNORECASE)
                return (series_pattern, episode_num)
        
        return (filename, 0)  # Return original if no pattern found
    
    def extract_season_info(self, path: str) -> Optional[int]:
        """
        Extract season number from file path or filename.
        
        Args:
            path: The full file path to analyze
            
        Returns:
            Season number if found, None otherwise
        """
        # Check both the full path and just the filename
        for text in [path, os.path.basename(path)]:
            for pattern in self.config.season_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return int(match.group(1))
        return None
    
    def extract_parameters_from_brackets(self, filename: str) -> List[str]:
        """
        Extract parameters from various bracket types.
        
        Args:
            filename: The filename to analyze
            
        Returns:
            List of parameters found in brackets
        """
        parameters = []
        for pattern in self.config.bracket_patterns:
            matches = re.findall(pattern, filename)
            parameters.extend(matches)
        
        return parameters
    
    def identify_release_group(self, parameters: List[str]) -> Optional[str]:
        """
        Identify release group from parameters.
        
        Args:
            parameters: List of parameters extracted from brackets
            
        Returns:
            Release group name if found, None otherwise
        """
        for param in parameters:
            for group in self.config.known_release_groups:
                if group in param:
                    return group
        return None
    
    def extract_tags(self, parameters: List[str]) -> List[str]:
        """
        Extract video tags from parameters.
        
        Args:
            parameters: List of parameters extracted from brackets
            
        Returns:
            List of identified tags
        """
        tags = []
        for param in parameters:
            words = param.split()
            for word in words:
                if any(tag in word for tag in self.config.common_tags):
                    if word not in tags:
                        tags.append(word)
        return tags
    
    def extract_series_name_from_path(self, file_path: str, base_name: str, parameters: List[str]) -> str:
        """
        Extract series name from file path with improved logic.
        
        Args:
            file_path: Full file path
            base_name: Base filename
            parameters: Parameters extracted from brackets
            
        Returns:
            Cleaned series name
        """
        # Get directory structure
        dir_path = os.path.dirname(file_path)
        path_parts = dir_path.split(os.sep) if dir_path else []
        
        # Try to find the best series name from directory structure
        series_name = None
        
        # Look through directory parts from deepest to shallowest
        for i in range(len(path_parts) - 1, -1, -1):
            part = path_parts[i]
            if not part:
                continue
                
            # Skip directories that match ignore patterns
            should_ignore = False
            for ignore_pattern in self.config.ignore_directory_patterns:
                if re.match(ignore_pattern, part, re.IGNORECASE):
                    should_ignore = True
                    break
            
            if not should_ignore:
                series_name = part
                break
        
        # If no good directory name found, extract from filename
        if not series_name:
            # Remove extension and episode number pattern
            clean_name = base_name
            
            # Remove episode patterns
            for pattern in self.config.episode_patterns:
                clean_name = re.sub(pattern, ' ', clean_name, flags=re.IGNORECASE)
            
            # Remove parameters in brackets
            for param in parameters:
                clean_name = clean_name.replace(f"[{param}]", "")
                clean_name = clean_name.replace(f"({param})", "")
                clean_name = clean_name.replace(f"【{param}】", "")
                clean_name = clean_name.replace(f"『{param}』", "")
                clean_name = clean_name.replace(f"{{{param}}}", "")
            
            # Apply cleanup patterns
            for pattern in self.config.cleanup_patterns:
                clean_name = re.sub(pattern, '', clean_name, flags=re.IGNORECASE)
            
            # Clean up extra spaces and special characters
            clean_name = re.sub(r'[-_\s]+', ' ', clean_name).strip()
            
            if clean_name:
                series_name = clean_name
        
        return series_name or "Unknown Series"
    
    def group_series(self) -> Dict[str, List[Tuple[int, str]]]:
        """
        Group video files by series.
        
        Returns:
            Dictionary mapping series patterns to lists of (episode_num, filepath) tuples
        """
        self.series_groups = defaultdict(list)
        
        for video in self.video_files:
            series_pattern, episode_num = self.extract_series_info(video)
            self.series_groups[series_pattern].append((episode_num, video))
        
        # Sort each group by episode number
        for pattern in self.series_groups:
            self.series_groups[pattern].sort()
        
        return dict(self.series_groups)
    
    def analyze_series(self) -> Dict[str, SeriesInfo]:
        """
        Analyze grouped series to extract detailed information.
        
        Returns:
            Dictionary mapping series patterns to SeriesInfo objects
        """
        self.series_info = {}
        
        for pattern, videos in self.series_groups.items():
            info = SeriesInfo()
            info.pattern = pattern
            
            # Take first file as sample
            sample_file = videos[0][1]
            info.sample_file = sample_file
            
            # Get the base name (without extension)
            base_name = os.path.basename(sample_file)
            
            # Extract directory name (often contains original title)
            dir_name = os.path.dirname(sample_file)
            info.dir_name = dir_name
            
            # Extract all parameters from brackets
            parameters = self.extract_parameters_from_brackets(base_name)
            
            # Identify release group
            info.release_group = self.identify_release_group(parameters)
            
            # Extract tags
            info.tags = self.extract_tags(parameters)
            
            # Extract season information
            info.season = self.extract_season_info(sample_file)
            
            # Extract series name using improved logic
            info.series_name = self.extract_series_name_from_path(sample_file, base_name, parameters)
            
            # Create episode map with format "01": "full/path/to/episode.mkv"
            episode_map = {}
            for ep_num, file_path in videos:
                # Format episode number as two digits
                ep_str = f"{ep_num:02d}"
                episode_map[ep_str] = file_path
            
            info.episodes = episode_map
            info.episode_count = len(videos)
            
            self.series_info[pattern] = info
        
        return self.series_info
    
    def parse(self, directory: str) -> Dict[str, SeriesInfo]:
        """
        Complete parsing workflow: scan, group, and analyze.
        
        Args:
            directory: Directory to scan for videos
            
        Returns:
            Dictionary mapping series patterns to SeriesInfo objects
        """
        self.scan_directory(directory)
        self.group_series()
        return self.analyze_series()
    
    def get_series_list(self) -> List[Dict[str, Any]]:
        """
        Get list of series information as dictionaries.
        
        Returns:
            List of series information dictionaries
        """
        return [info.to_dict() for info in self.series_info.values()]
    
    def print_analysis_results(self):
        """Print detailed analysis results to console."""
        print("=== Bangumi Parser Analysis Results ===")
        print(f"Found {len(self.series_info)} series with {len(self.video_files)} total episodes\n")
        
        for pattern, info in self.series_info.items():
            print(f"Series: {info.series_name}")
            if info.season:
                print(f"Season: {info.season}")
            print(f"Directory: {info.dir_name}")
            print(f"Release Group: {info.release_group}")
            print(f"Tags: {', '.join(info.tags) if info.tags else 'None'}")
            print(f"Episodes: {info.episode_count}")
            print(f"Sample file: {os.path.basename(info.sample_file)}")
            print("\nEpisode map:")
            # Print first 3 episodes as examples
            for i, (ep_num, path) in enumerate(list(info.episodes.items())[:3]):
                print(f"  {ep_num}: {os.path.basename(path)}")
            if len(info.episodes) > 3:
                print(f"  ... and {len(info.episodes) - 3} more episodes")
            print("-" * 50)
    
    def merge_same_season_series(self, series_info: Dict[str, SeriesInfo]) -> Dict[str, SeriesInfo]:
        """
        Merge series that belong to the same series, directory, and season.
        
        Rules:
        1. More episodes takes priority
        2. Specific episode numbers take priority over default "00"
        3. Merge episodes from smaller collections into larger ones
        4. Rename episode "00" to "未知集01" when merging
        
        Args:
            series_info: Dictionary of series information
            
        Returns:
            Dictionary of merged series information
        """
        # Group by (series_name, dir_name, season)
        groups = defaultdict(list)
        
        for pattern, info in series_info.items():
            key = (info.series_name, info.dir_name, info.season or 1)
            groups[key].append((pattern, info))
        
        merged_series = {}
        
        for key, series_list in groups.items():
            if len(series_list) == 1:
                # Only one series in this group, keep as is
                pattern, info = series_list[0]
                merged_series[pattern] = info
            else:
                # Multiple series need merging
                # Sort by priority: more episodes first, then specific episodes over "00"
                def priority_key(item):
                    pattern, info = item
                    has_specific_episodes = any(ep != "00" for ep in info.episodes.keys())
                    return (info.episode_count, has_specific_episodes)
                
                series_list.sort(key=priority_key, reverse=True)
                
                # Take the highest priority series as base
                main_pattern, main_info = series_list[0]
                
                # Merge other series into the main one
                for pattern, info in series_list[1:]:
                    print(f"Merging {info.series_name} ({info.episode_count} eps) into main collection ({main_info.episode_count} eps)")
                    
                    # Merge episodes
                    for ep_num, file_path in info.episodes.items():
                        if ep_num == "00":
                            # Rename "00" episode to "未知集01" or next available number
                            new_ep_num = "未知集01"
                            counter = 1
                            while new_ep_num in main_info.episodes:
                                counter += 1
                                new_ep_num = f"未知集{counter:02d}"
                            main_info.episodes[new_ep_num] = file_path
                        else:
                            # Add episode if not already exists
                            if ep_num not in main_info.episodes:
                                main_info.episodes[ep_num] = file_path
                    
                    # Merge tags
                    for tag in info.tags:
                        if tag not in main_info.tags:
                            main_info.tags.append(tag)
                    
                    # Update release group if not set
                    if not main_info.release_group and info.release_group:
                        main_info.release_group = info.release_group
                
                # Update episode count
                main_info.episode_count = len(main_info.episodes)
                merged_series[main_pattern] = main_info
        
        return merged_series
    
    def merge_multi_season_series(self, series_info: Dict[str, SeriesInfo]) -> Dict[str, BangumiInfo]:
        """
        Merge series with the same name but different seasons into BangumiInfo objects.
        
        Args:
            series_info: Dictionary of series information
            
        Returns:
            Dictionary of BangumiInfo objects indexed by series name
        """
        bangumi_dict = {}
        
        for pattern, info in series_info.items():
            series_name = info.series_name
            
            if series_name not in bangumi_dict:
                bangumi_dict[series_name] = BangumiInfo()
                bangumi_dict[series_name].series_name = series_name
            
            bangumi_dict[series_name].add_season(info)
        
        return bangumi_dict
    
    def parse_and_merge(self, directory: str) -> Dict[str, BangumiInfo]:
        """
        Complete parsing workflow with merging: scan, group, analyze, and merge.
        
        Args:
            directory: Directory to scan for videos
            
        Returns:
            Dictionary mapping series names to BangumiInfo objects
        """
        # Step 1: Basic parsing
        series_info = self.parse(directory)
        
        # Step 2: Merge same season series
        print("\n=== Merging same season series ===")
        merged_same_season = self.merge_same_season_series(series_info)
        
        # Step 3: Merge multi-season series
        print("\n=== Merging multi-season series ===")
        final_bangumi = self.merge_multi_season_series(merged_same_season)
        
        return final_bangumi
    
    def print_bangumi_results(self, bangumi_info: Dict[str, BangumiInfo]):
        """Print merged bangumi analysis results."""
        print("=== Final Bangumi Analysis Results ===")
        total_series = len(bangumi_info)
        total_episodes = sum(bangumi.total_episodes for bangumi in bangumi_info.values())
        total_seasons = sum(bangumi.season_count for bangumi in bangumi_info.values())
        
        print(f"Found {total_series} bangumi series with {total_seasons} seasons and {total_episodes} total episodes\n")
        
        for series_name, bangumi in bangumi_info.items():
            print(f"Bangumi: {bangumi.series_name}")
            print(f"Seasons: {bangumi.season_count}")
            print(f"Total Episodes: {bangumi.total_episodes}")
            print(f"Release Groups: {', '.join(bangumi.release_groups) if bangumi.release_groups else 'None'}")
            print(f"Tags: {', '.join(bangumi.tags) if bangumi.tags else 'None'}")
            
            print("\nSeason Details:")
            for season_num in sorted(bangumi.seasons.keys()):
                season_info = bangumi.seasons[season_num]
                print(f"  Season {season_num}: {season_info.episode_count} episodes")
                print(f"    Directory: {season_info.dir_name}")
                print(f"    Sample: {os.path.basename(season_info.sample_file)}")
                
                # Show first few episodes
                episodes = list(season_info.episodes.items())[:3]
                for ep_num, path in episodes:
                    print(f"      {ep_num}: {os.path.basename(path)}")
                if len(season_info.episodes) > 3:
                    print(f"      ... and {len(season_info.episodes) - 3} more episodes")
            
            print("-" * 60)
