"""
Bangumi Parser - A library for parsing and organizing anime video files.
"""

from .core import BangumiParser, SeriesInfo, BangumiInfo
from .config import BangumiConfig
from . import utils

__version__ = "1.0.4"
__all__ = ["BangumiParser", "BangumiConfig", "SeriesInfo", "BangumiInfo", "utils"]
