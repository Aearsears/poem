# Development Guide

This guide explains how to set up your development environment for working on the Poem CLI tool.

## Project Structure

```
poem/
├── src/              # Source code directory
│   └── poem/         # Main package
│       ├── __init__.py
│       ├── cli.py    # Command-line interface
│       └── core.py   # Core functionality
├── tests/            # Test directory
├── pyproject.toml    # Project configuration
└── README.md         # Project documentation
```

The project uses a src-layout which helps avoid import issues during development and ensures consistent behavior between development and installed versions.

## Setup

1. Clone the repository:

    ```
    git clone https://github.com/Aearsears/poem.git
    cd poem
    ```

2. Create a virtual environment (optional but recommended):

    ```
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # OR
    source venv/bin/activate  # On Unix/Linux
    ```

3. Install the project in development mode:
    ```
    pip install -e .
    ```

## Testing

Run tests using pytest:

```
pytest
```

## Running the CLI in development

For development, you can run the CLI directly using:

```
python run_poem.py [command]
```

For example:

```
python run_poem.py list
python run_poem.py current
```

## Building and Distribution

Build the package using:

```
python -m build
```

This will create distributable packages in the `dist/` directory.

## Contributing

1. Create a new branch for your feature or bugfix
2. Make your changes
3. Add tests for your changes
4. Run the tests to make sure everything passes
5. Submit a pull request
