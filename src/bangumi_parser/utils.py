"""
Utility functions for Bangumi Parser.
"""

import json
import os
from typing import Dict, Any, List, Union
from .core import SeriesInfo, BangumiInfo


def export_to_json(data: Union[Dict[str, SeriesInfo], Dict[str, BangumiInfo]], output_path: str):
    """
    Export series information or bangumi information to JSON file.
    
    Args:
        data: Dictionary of series information or bangumi information
        output_path: Path to save JSON file
    """
    export_data = {}
    
    for key, value in data.items():
        if hasattr(value, 'to_dict'):
            export_data[key] = value.to_dict()
        else:
            export_data[key] = value
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)


def export_bangumi_to_csv(bangumi_info: Dict[str, BangumiInfo], output_path: str):
    """
    Export bangumi information to CSV file.
    
    Args:
        bangumi_info: Dictionary of bangumi information
        output_path: Path to save CSV file
    """
    import csv
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['series_name', 'season_count', 'total_episodes', 'release_groups', 'tags', 'seasons_detail']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for bangumi in bangumi_info.values():
            seasons_detail = []
            for season_num, season_info in bangumi.seasons.items():
                seasons_detail.append(f"S{season_num}:{season_info.episode_count}eps")
            
            writer.writerow({
                'series_name': bangumi.series_name,
                'season_count': bangumi.season_count,
                'total_episodes': bangumi.total_episodes,
                'release_groups': ', '.join(bangumi.release_groups),
                'tags': ', '.join(bangumi.tags),
                'seasons_detail': ', '.join(seasons_detail)
            })


def export_to_csv(series_info: Dict[str, SeriesInfo], output_path: str):
    """
    Export series information to CSV file.
    
    Args:
        series_info: Dictionary of series information
        output_path: Path to save CSV file
    """
    import csv
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['series_name', 'season', 'dir_name', 'release_group', 'tags', 
                     'episode_count', 'episodes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for info in series_info.values():
            writer.writerow({
                'series_name': info.series_name,
                'season': info.season,
                'dir_name': info.dir_name,
                'release_group': info.release_group,
                'tags': ', '.join(info.tags),
                'episode_count': info.episode_count,
                'episodes': ', '.join(f"{k}:{os.path.basename(v)}" 
                                    for k, v in info.episodes.items())
            })


def create_symlinks(series_info: Dict[str, SeriesInfo], target_base_dir: str, 
                   source_base_dir: str):
    """
    Create symbolic links organized by series.
    
    Args:
        series_info: Dictionary of series information
        target_base_dir: Base directory for organized links
        source_base_dir: Base directory of source files
    """
    for info in series_info.values():
        # Create series directory
        series_dir = os.path.join(target_base_dir, info.series_name)
        os.makedirs(series_dir, exist_ok=True)
        
        # Create links for each episode
        for ep_num, rel_path in info.episodes.items():
            source_path = os.path.join(source_base_dir, rel_path)
            target_path = os.path.join(series_dir, f"Episode_{ep_num}_{os.path.basename(rel_path)}")
            
            try:
                if os.path.exists(target_path):
                    os.remove(target_path)
                os.symlink(source_path, target_path)
            except OSError as e:
                print(f"Failed to create symlink for {rel_path}: {e}")


def generate_playlist(series_info: Dict[str, SeriesInfo], base_dir: str, 
                     output_dir: str):
    """
    Generate M3U playlist files for each series.
    
    Args:
        series_info: Dictionary of series information
        base_dir: Base directory of video files
        output_dir: Directory to save playlist files
    """
    os.makedirs(output_dir, exist_ok=True)
    
    for info in series_info.values():
        playlist_path = os.path.join(output_dir, f"{info.series_name}.m3u")
        
        with open(playlist_path, 'w', encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            f.write(f"#PLAYLIST:{info.series_name}\n")
            
            for ep_num, rel_path in sorted(info.episodes.items()):
                full_path = os.path.join(base_dir, rel_path)
                f.write(f"#EXTINF:-1,Episode {ep_num}\n")
                f.write(f"{full_path}\n")


def filter_series_by_release_group(series_info: Dict[str, SeriesInfo], 
                                  release_group: str) -> Dict[str, SeriesInfo]:
    """
    Filter series by release group.
    
    Args:
        series_info: Dictionary of series information
        release_group: Release group to filter by
        
    Returns:
        Filtered dictionary of series information
    """
    return {
        pattern: info 
        for pattern, info in series_info.items()
        if info.release_group == release_group
    }


def get_series_statistics(series_info: Dict[str, SeriesInfo]) -> Dict[str, Any]:
    """
    Get statistics about the parsed series.
    
    Args:
        series_info: Dictionary of series information
        
    Returns:
        Dictionary containing statistics
    """
    total_series = len(series_info)
    total_episodes = sum(info.episode_count for info in series_info.values())
    
    release_groups = {}
    tags = {}
    
    for info in series_info.values():
        if info.release_group:
            release_groups[info.release_group] = release_groups.get(info.release_group, 0) + 1
        
        for tag in info.tags:
            tags[tag] = tags.get(tag, 0) + 1
    
    return {
        'total_series': total_series,
        'total_episodes': total_episodes,
        'release_groups': release_groups,
        'tags': tags,
        'average_episodes_per_series': total_episodes / total_series if total_series > 0 else 0
    }


def get_bangumi_statistics(bangumi_info: Dict[str, BangumiInfo]) -> Dict[str, Any]:
    """
    Get statistics about the parsed bangumi.
    
    Args:
        bangumi_info: Dictionary of bangumi information
        
    Returns:
        Dictionary containing statistics
    """
    total_bangumi = len(bangumi_info)
    total_seasons = sum(bangumi.season_count for bangumi in bangumi_info.values())
    total_episodes = sum(bangumi.total_episodes for bangumi in bangumi_info.values())
    
    release_groups = {}
    tags = {}
    season_distribution = {}
    
    for bangumi in bangumi_info.values():
        # Count release groups
        for group in bangumi.release_groups:
            release_groups[group] = release_groups.get(group, 0) + 1
        
        # Count tags
        for tag in bangumi.tags:
            tags[tag] = tags.get(tag, 0) + 1
        
        # Season distribution
        season_count = bangumi.season_count
        season_distribution[season_count] = season_distribution.get(season_count, 0) + 1
    
    return {
        'total_bangumi': total_bangumi,
        'total_seasons': total_seasons,
        'total_episodes': total_episodes,
        'release_groups': release_groups,
        'tags': tags,
        'season_distribution': season_distribution,
        'average_seasons_per_bangumi': total_seasons / total_bangumi if total_bangumi > 0 else 0,
        'average_episodes_per_bangumi': total_episodes / total_bangumi if total_bangumi > 0 else 0,
        'average_episodes_per_season': total_episodes / total_seasons if total_seasons > 0 else 0
    }


def create_bangumi_symlinks(bangumi_info: Dict[str, BangumiInfo], target_base_dir: str, 
                           source_base_dir: str):
    """
    Create symbolic links organized by bangumi and seasons.
    
    Args:
        bangumi_info: Dictionary of bangumi information
        target_base_dir: Base directory for organized links
        source_base_dir: Base directory of source files
    """
    for bangumi in bangumi_info.values():
        # Create bangumi directory
        bangumi_dir = os.path.join(target_base_dir, bangumi.series_name)
        os.makedirs(bangumi_dir, exist_ok=True)
        
        # Create season directories and links
        for season_num, season_info in bangumi.seasons.items():
            if bangumi.season_count > 1:
                # Multiple seasons, create season subdirectories
                season_dir = os.path.join(bangumi_dir, f"Season {season_num:02d}")
            else:
                # Single season, use bangumi directory directly
                season_dir = bangumi_dir
            
            os.makedirs(season_dir, exist_ok=True)
            
            # Create links for each episode
            for ep_num, rel_path in season_info.episodes.items():
                source_path = os.path.join(source_base_dir, rel_path)
                target_path = os.path.join(season_dir, f"S{season_num:02d}E{ep_num}_{os.path.basename(rel_path)}")
                
                try:
                    if os.path.exists(target_path):
                        os.remove(target_path)
                    os.symlink(source_path, target_path)
                except OSError as e:
                    print(f"Failed to create symlink for {rel_path}: {e}")


def generate_bangumi_playlist(bangumi_info: Dict[str, BangumiInfo], base_dir: str, 
                             output_dir: str):
    """
    Generate M3U playlist files for each bangumi and season.
    
    Args:
        bangumi_info: Dictionary of bangumi information
        base_dir: Base directory of video files
        output_dir: Directory to save playlist files
    """
    os.makedirs(output_dir, exist_ok=True)
    
    for bangumi in bangumi_info.values():
        # Create overall bangumi playlist
        bangumi_playlist_path = os.path.join(output_dir, f"{bangumi.series_name}_Complete.m3u")
        
        with open(bangumi_playlist_path, 'w', encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            f.write(f"#PLAYLIST:{bangumi.series_name} - Complete Series\n")
            
            # Add all episodes from all seasons
            for season_num in sorted(bangumi.seasons.keys()):
                season_info = bangumi.seasons[season_num]
                f.write(f"#EXTINF:-1,Season {season_num}\n")
                
                for ep_num, rel_path in sorted(season_info.episodes.items()):
                    full_path = os.path.join(base_dir, rel_path)
                    f.write(f"#EXTINF:-1,S{season_num:02d}E{ep_num}\n")
                    f.write(f"{full_path}\n")
        
        # Create individual season playlists if multiple seasons
        if bangumi.season_count > 1:
            for season_num, season_info in bangumi.seasons.items():
                season_playlist_path = os.path.join(output_dir, f"{bangumi.series_name}_S{season_num:02d}.m3u")
                
                with open(season_playlist_path, 'w', encoding='utf-8') as f:
                    f.write("#EXTM3U\n")
                    f.write(f"#PLAYLIST:{bangumi.series_name} - Season {season_num}\n")
                    
                    for ep_num, rel_path in sorted(season_info.episodes.items()):
                        full_path = os.path.join(base_dir, rel_path)
                        f.write(f"#EXTINF:-1,S{season_num:02d}E{ep_num}\n")
                        f.write(f"{full_path}\n")
