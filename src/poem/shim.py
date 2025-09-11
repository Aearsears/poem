#!/usr/bin/env python
"""Runner script for the poem shim."""

import os
import sys
import subprocess
from pathlib import Path
from poem.core import _get_active_version, _get_poetry_bin


def main():
    """Run poetry with the appropriate version."""
    try:
        # Get the active version of Poetry
        version, source = _get_active_version()

        if version == "unknown":
            print("No poetry version is active. Please install one first:")
            print("  poem install 1.2.3")
            sys.exit(1)

        # Get the path to the appropriate Poetry binary
        poetry_bin = _get_poetry_bin(version)

        if not os.path.exists(poetry_bin):
            print(f"Poetry version {version} is not installed or is broken.")
            print(f"Please reinstall it: poem install {version}")
            sys.exit(1)

        # Forward all arguments to the Poetry binary
        result = subprocess.run(
            [poetry_bin] + sys.argv[1:],
            check=False,
        )

        # Exit with the same code as Poetry
        sys.exit(result.returncode)

    except Exception as e:
        print(f"Error in poem runner: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
