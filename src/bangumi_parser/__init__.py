"""
Bangumi Parser - A library for parsing and organizing anime video files.
"""

from .core import BangumiParser, PlayList, BangumiInfo
from .config import BangumiConfig
from . import utils

__version__ = "1.0.5"
__all__ = ["BangumiParser", "BangumiConfig", "PlayList", "BangumiInfo", "utils"]
