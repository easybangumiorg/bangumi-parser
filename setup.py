"""
Setup script for Bangumi Parser.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bangumi-parser",
    version="1.0.0",
    author="AyalaKaguya",
    author_email="support@easybangumi.org",
    description="A library for parsing and organizing anime video files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EasyBangumi/bangumi-parser",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies required
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black",
            "flake8",
        ],
    },
    entry_points={
        "console_scripts": [
            "bangumi-parser=bangumi_parser.cli:main",
        ],
    },
)
