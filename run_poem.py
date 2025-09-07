#!/usr/bin/env python
"""
Development entry point for poem CLI.
"""

from poem.cli import main
import sys
import os

# Add src directory to path for development
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
sys.path.insert(0, src_path)


if __name__ == "__main__":
    sys.exit(main())
