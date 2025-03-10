# Waze Home CLI

A command-line tool that provides the quickest route between home and work using Waze data.

## Features

- Get the fastest route between home and work
- Set and manage custom locations
- Display turn-by-turn directions
- Show alternative routes
- Save your frequently used locations

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/waze-home.git
   cd waze-home
   ```

2. Install using uv:
   ```
   uv pip install -e .
   ```

## Usage

### Get the fastest route home

```
python -m waze_home home
```

### Get the fastest route to work

```
python -m waze_home work
```

### Get a route between any two saved locations

```
python -m waze_home route --from location1 --to location2
```

### Set a new location

```
python -m waze_home set-location office "123 Business St, City"
```

### List all saved locations

```
python -m waze_home get-location
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