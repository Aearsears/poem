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

-   [] `poem install <version>` – Install a specific Poetry version
-   [] `poem uninstall <version>` – Remove an installed Poetry version
-   [] `poem use <version>` – Switch Poetry version for the current shell session
-   [] `poem global <version>` – Set a global default Poetry version
-   [] `poem current` – Show the active Poetry version and source (local/global)
-   [] `poem list` – List installed Poetry versions
-   [] `poem ls-remote` – List available Poetry versions (from GitHub releases)

## Utility Commands

-   [] `poem which` – Show the path to the active Poetry binary
-   [] `poem doctor` – Diagnose setup issues (shims, PATH, install dirs)
-   [] `poem local <version>` – Set a project-specific Poetry version (.poetry-version file)

## Usage Examples

List installed poetry versions:

```
poem list
```

List available poetry versions from GitHub:

```
poem ls-remote
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

Set a global default version:

```
poem global 1.7.1
```

Set a project-specific version:

```
poem local 1.8.3
```

Check your installation:

```
poem doctor
```

# Install a Poetry version

poem install 1.8.3

# Use it in current shell

poem use 1.8.3

# Set a global default version

poem global 1.7.1

# Create a project-specific version

echo "1.8.3" > .poetry-version
cd my_project/ # auto-switch to 1.8.3

# Show current version

poem current

# -> 1.8.3 (from .poetry-version)

# List installed versions

poem list

# List available versions

poem ls-remote

## License

GPL-3.0
