# ExileNexus

A modular ecosystem for Path of Exile (PoE) tools built with a Pub/Sub architecture using WebSockets.

## Architecture Overview

ExileNexus follows a **Publisher/Subscriber (Pub/Sub)** pattern with a centralized message broker. This design enables loose coupling between services and allows multiple components to communicate asynchronously.

### Core Components

1. **Broker Hub** (`broker/hub.py`): Central message hub that receives messages from publishers and broadcasts them to all connected subscribers via WebSocket connections.

2. **Log Monitor** (`monitor_log/watcher.py`): Watches the Path of Exile `Client.txt` file for changes and publishes events (e.g., area entries) to the broker.

3. **Shared Library** (`shared_lib/models.py`): Common Pydantic models for message contracts, ensuring type safety and validation across all services.

4. **Voice Engine** (`voice_engine/`): Text-to-speech and translation logic (placeholder).

5. **Dashboard UI** (`dashboard_ui/`): Modern user interface (placeholder).

6. **API Wrapper** (`api_wrapper/`): Connectors for GGG API and Poe-Ninja (placeholder).

## Architecture Diagram

```
┌─────────────┐
│ Log Monitor │──┐
└─────────────┘  │
                 │  Publish
┌─────────────┐  │  Messages
│Voice Engine │──┤
└─────────────┘  │
                 ▼
         ┌───────────────┐
         │  Broker Hub   │
         │ (WebSocket)   │
         │  localhost    │
         │    :8888      │
         └───────────────┘
                 │
                 │  Broadcast
                 │  Messages
         ┌───────┴───────┐
         │               │
         ▼               ▼
┌─────────────┐   ┌─────────────┐
│  Dashboard  │   │  Voice      │
│     UI      │   │  Engine     │
└─────────────┘   └─────────────┘
```

## Message Contract

All messages follow a standardized structure defined in `shared_lib/models.py`:

```json
{
  "header": {
    "id": "uuid",
    "source": "service_name",
    "event_type": "area_entered",
    "timestamp": "2024-01-01T00:00:00Z",
    "priority": 5
  },
  "payload": {
    "area_name": "Lioneye's Watch",
    "raw_line": "Entered [Lioneye's Watch]"
  }
}
```

### Event Types

- `area_entered`: Player enters a new area
- `area_left`: Player leaves an area
- `item_drop`: Item dropped
- `trade_received`: Trade request received
- `trade_accepted`: Trade accepted
- `chat_message`: Chat message received
- `death`: Player death
- `level_up`: Player level up
- `custom`: Custom events

## Installation

### Prerequisites

- Python 3.10 or higher
- Windows OS (optimized for Windows file handling)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ExileNexus
```

2. Install dependencies using `uv` or `poetry`:
```bash
# Using uv
uv pip install -e .

# Using pip
pip install -e .

# Using poetry
poetry install
```

3. Configure environment variables (optional):
```bash
# Set Path of Exile Client.txt location (default: %USERPROFILE%\Documents\My Games\Path of Exile\Client.txt)
set POE_CLIENT_LOG=C:\Path\To\Client.txt
```

## Usage

### Starting the Broker

The broker must be running before starting any services:

```bash
python -m broker.hub
```

The broker will start on `ws://localhost:8888`.

### Starting the Log Monitor

In a separate terminal:

```bash
python -m monitor_log.watcher
```

The log monitor will:
- Watch the `Client.txt` file for changes
- Parse "Entered [Area]" events
- Publish messages to the broker
- Auto-reconnect to the broker if connection is lost

### Connection Endpoints

- **Publisher**: `ws://localhost:8888/publish` or `ws://localhost:8888/publisher`
- **Subscriber**: `ws://localhost:8888` (any other path)

## Development

### Code Standards

- **Language**: All code, comments, and documentation in English
- **Style**: PEP 8 compliant
- **Formatting**: Ruff/Black
- **Type Hints**: Strict type hinting required
- **Validation**: Pydantic v2 for all message contracts

### Project Structure

```
ExileNexus/
├── shared_lib/          # Common logic and Pydantic models
├── broker/              # Central message hub
├── monitor_log/         # Log watcher service
├── voice_engine/        # TTS and translation logic
├── dashboard_ui/        # Modern UI (placeholder)
├── api_wrapper/         # GGG/Poe-Ninja connectors
├── data/                # SQLite databases and YAML dictionaries
├── pyproject.toml       # Project configuration
└── README.md            # This file
```

### Running Linters

```bash
# Format code
ruff format .

# Check code
ruff check .

# Type checking
mypy .
```

## Technical Details

### Windows Performance

The log watcher opens `Client.txt` with shared read access, allowing the game to write to the file while the watcher reads from it without blocking.

### Concurrency

All I/O operations use `asyncio` for non-blocking performance:
- WebSocket connections are async
- File watching uses `watchdog` with async event processing
- Message queue processing is async

### Auto-Reconnect Logic

The log watcher includes robust auto-reconnect logic:
- Detects connection failures
- Re-queues messages during disconnection
- Automatically reconnects with configurable delay
- Gracefully handles connection interruptions

### Logging

All modules use `loguru` for unified, structured logging across the ecosystem.

## License

[Add your license here]

## Contributing

[Add contributing guidelines here]
