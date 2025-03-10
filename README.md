# Waze Home CLI

A command-line tool that provides the quickest route between home and work using Waze data.

## Features

- Get the fastest route between home and work
- Set and manage custom locations
- Display turn-by-turn directions
- Show alternative routes
- Save your frequently used locations

## Installation

### Option 1: Install from PyPI (recommended)

```bash
pip install waze-home
```

Or if you use uv:

```bash
uv pip install waze-home
```

### Option 2: Install from source

1. Clone this repository:
   ```bash
   git clone https://github.com/andrewlarder/waze-home-cli.git
   cd waze-home-cli
   ```

2. Install in development mode:
   ```bash
   pip install -e .
   ```
   
   Or with uv:
   ```bash
   uv pip install -e .
   ```

## Usage

### Get the fastest route home

```bash
waze-home home
```

### Get the fastest route to work

```bash
waze-home work
```

### Get a route between any two saved locations

```bash
waze-home route --from location1 --to location2
```

### Set a new location

```bash
waze-home set-location office "123 Business St, City"
```

### List all saved locations

```bash
waze-home get-location
```

You can also use the module form if you prefer:

```bash
python -m waze_home [command]
```

## Configuration

By default, the application stores locations in a config file at `~/.config/waze-home/config.json`. You can also set locations using environment variables:

- `WAZE_HOME_LOCATION` - Your home address
- `WAZE_WORK_LOCATION` - Your work address

## Development

- Run linting: `ruff check .`
- Run type checking: `mypy .`
- Run tests: `pytest`

## Note

This is a mock implementation that simulates Waze routes. In a production environment, you would need to use the official Waze API or another routing service.