"""Setup configuration for GIID system."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="giid",
    version="1.0.0",
    author="GIID Team",
    author_email="giid@example.com",
    description="Global Institutional Intelligence Desk - Production-ready intelligence system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/barlevi12/aicopilotbar",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=[
        "pyyaml>=6.0.1",
        "aiohttp>=3.9.0",
        "python-dateutil>=2.8.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "giid=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["config/*.yaml", "report/templates/*.md"],
    },
)
