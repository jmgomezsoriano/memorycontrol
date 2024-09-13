# MemoryControl

MemoryControl is a Python library that monitors the memory usage of processes on both Linux and Windows systems. It can gracefully terminate processes when they exceed a defined memory limit and forcefully kill them if they exceed a second, higher threshold.

## Features

- Monitors processes based on their command line.
- Configurable memory limits for graceful termination and forced shutdown.
- Cross-platform support for Linux and Windows.
- Automatically sends appropriate signals depending on the operating system (SIGINT and SIGKILL for Linux, terminate and kill for Windows).
- Customizable time intervals between memory checks.

## Installation

MemoryControl requires `psutil` to work. To install the necessary dependencies, run:

```bash
pip install psutil
```

## Usage

You can use the library either as a Python module or from the command line.

### As a Python Module

Import the `monitor` function and specify the command line, memory limits, and check intervals:

```python
from memorycontrol import monitor

# Define parameters
command_line = "uvicorn api.server:app --port 8001"
memory_limit = 100  # MB
kill_memory_threshold = 200  # MB
check_interval = 5  # seconds

# Start monitoring
monitor(command_line, memory_limit, kill_memory_threshold, check_interval)
```

### From the Command Line

You can also run the monitor directly from the command line:

```bash
python -m memorycontrol --command_line "uvicorn api.server:app --port 8001" --memory_limit 100 --kill_memory_threshold 200 --check_interval 5
```

## Example

1. Start a process you want to monitor, e.g., a `uvicorn` server:

```bash
uvicorn api.server:app --port 8001 
```

2. Monitor the process and enforce memory limits:

```python
from memorycontrol import monitor

monitor("uvicorn api.server:app --port 8001", memory_limit=100, kill_memory_threshold=200, check_interval=5)
````