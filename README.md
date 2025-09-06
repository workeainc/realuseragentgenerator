# User Agent Generator

A Python CLI tool for generating realistic USA-based user agents for Android and iOS devices with proper entropy.

## Features

- Generate realistic user agents for Android and iOS devices
- SQLite database storage for device information and generated user agents
- Entropy-based generation to avoid pure randomness
- CLI interface with multiple commands
- Support for batch generation
- Statistics tracking

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### GUI Version

Run the graphical user interface:
```bash
python ua_generator_ui.py
```

The GUI provides:
- Radio buttons to select device type (Android/iOS/Both)
- Generate button to create a new unique user agent
- Copy button to copy the current user agent to clipboard
- Automatic generation of new user agent after copying
- Status bar showing latest actions

### CLI Version

#### Generate User Agents

Generate 100 user agents (default):
```bash
python ua_generator.py generate
```

Generate specific number of user agents:
```bash
python ua_generator.py generate --count 50
```

Generate for specific device type:
```bash
python ua_generator.py generate --device android
python ua_generator.py generate --device ios
```

Save output to a file:
```bash
python ua_generator.py generate --output useragents.json
```

### View Statistics

View statistics for all generated user agents:
```bash
python ua_generator.py stats
```

View statistics for specific device type:
```bash
python ua_generator.py stats --device android
python ua_generator.py stats --device ios
```

## Database

The tool uses SQLite database (useragents.db) to store:
- Android device information
- iOS device information
- Chrome browser versions
- Safari browser versions
- Generated user agents history

## Notes

- The tool maintains entropy by:
  - Using real device and browser version combinations
  - Adding slight variations to user agent strings
  - Tracking generated user agents to avoid duplicates
  - Using USA-specific device models and versions
