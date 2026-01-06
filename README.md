# Personal Manager

CLI task and project organizer with shell integration.

## Features

- Shell command execution interface
- Task management (taskwarrior integration planned)
- Time tracking (timewarrior integration planned)
- Simple terminal-based UI

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Execute shell commands
pm shell ls -la
pm shell "git status"

# Task management (placeholder)
pm task list

# Time tracking (placeholder)  
pm time summary
```

## Development

Run tests:
```bash
python -m pytest tests/
```

## Requirements

- Python 3.8+
- Optional: taskwarrior, timewarrior for full functionality
