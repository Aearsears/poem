# Poem

A CLI tool for managing poetry versions.

## Goals

Enforce consistent Poetry versions across teams.

Provide an easy CLI for installing, switching, and managing versions.

Support automatic version switching when entering a project.

Be lightweight and Poetry-specific (no need for asdf or heavy polyglot managers).

## Installation

```
pip install poem
```

## Core Commands

-   [ ] `pvm install <version>` – Install a specific Poetry version
-   [ ] `pvm uninstall <version>` – Remove an installed Poetry version
-   [ ] `pvm use <version>` – Switch Poetry version for the current shell session
-   [ ] `pvm global <version>` – Set a global default Poetry version
-   [ ] `pvm current` – Show the active Poetry version and source (local/global)
-   [ ] `pvm list` – List installed Poetry versions
-   [ ] `pvm ls-remote` – List available Poetry versions (from GitHub releases)

## Utility Commands

-   [ ] `pvm which poetry` – Show the path to the active Poetry binary
-   [ ] `pvm doctor` – Diagnose setup issues (shims, PATH, install dirs)

## Usage

List available poetry versions:

```
poem list
```

List installed poetry versions:

```
poem list --installed
```

Show the current poetry version:

```
poem current
```

Install a specific poetry version:

```
poem install 1.1.0
```

Switch to a specific poetry version:

```
poem use 1.1.0
```

# Install a Poetry version

pvm install 1.8.3

# Use it in current shell

pvm use 1.8.3

# Set a global default version

pvm global 1.7.1

# Create a project-specific version

echo "1.8.3" > .poetry-version
cd my_project/ # auto-switch to 1.8.3

# Show current version

pvm current

# -> 1.8.3 (from .poetry-version)

# List installed versions

pvm list

# List available versions

pvm ls-remote

## License

GPL-3.0
