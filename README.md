# Waze Home CLI

A command-line tool that provides the quickest route between home and work using Waze data.

## Features

- Get the fastest route between home and work
- Set and manage custom locations
- Display turn-by-turn directions
- Show alternative routes
- Save your frequently used locations

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Quick Install (Using Installation Scripts)

Use the provided installation scripts:

**On Linux/macOS:**
```bash
# Clone the repository
git clone https://github.com/andrewlarder/waze-home-cli.git
cd waze-home-cli

# Make the script executable
chmod +x install.sh

# Run the installer
./install.sh
```

**On Windows:**
```
# Clone the repository
git clone https://github.com/andrewlarder/waze-home-cli.git
cd waze-home-cli

# Run the installer
install.bat
```

These scripts will check for Python, create a virtual environment, install the package, and verify the installation.


### Building from source

The simplest way to install and use the CLI:

```bash
# Clone the repository
git clone https://github.com/andrewlarder/waze-home-cli.git
cd waze-home-cli

# Create a virtual environment (recommended)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install the package
pip install -e .
```

After installation, you can use the `waze-home` command directly in your terminal.



### Manual Installation

If you prefer to install the dependencies manually:

1. Clone the repository:
   ```bash
   git clone https://github.com/andrewlarder/waze-home-cli.git
   cd waze-home-cli
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the CLI using the module syntax:
   ```bash
   python -m waze_home [command]
   ```

### Verify Installation

To verify that the installation was successful, run:

```bash
waze-home --help
```

You should see the help message with available commands.


After installation, they can use the `waze-home` command directly in their terminal.

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