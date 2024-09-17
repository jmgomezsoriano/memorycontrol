# MemoryControl

MemoryControl is a Python library that monitors the memory usage of processes on both Linux and Windows systems. It can gracefully terminate processes when they exceed a defined memory limit and forcefully kill them if they exceed a second, higher threshold.

# Features

- Monitors processes based on their command line.
- Configurable memory limits for graceful termination and forced shutdown.
- Cross-platform support for Linux and Windows.
- Automatically sends appropriate signals depending on the operating system (SIGINT and SIGKILL for Linux, terminate and kill for Windows).
- Customizable time intervals between memory checks.

# Installation

```bash
pip install memorycontrol
```

# Usage

## Command line

```text
memorycontrol -h
usage: __main__.py [-h] [-s MB] [-k MB] [--check-interval SECONDS] [--log-level LEVEL] COMMAND [COMMAND ...]

Monitor a process by its command line and memory limits.

positional arguments:
  COMMAND               Exact command line of the process to monitor (e.g., 'uvicorn api.server:app --port 8001').

options:
  -h, --help            show this help message and exit
  -s MB, --stop-memory MB
                        Memory limit in MB to send an interrupt signal. By default, 100 MB.
  -k MB, --kill-memory MB
                        Memory threshold in MB to forcefully terminate the process. By default, 200 MB.If this argument is set to 0, then, no limit.
  --check-interval SECONDS
                        Interval in seconds for memory checks (default: 5 seconds).
  --log-level LEVEL     Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
```

For example, if you want to monitor the command "uvicorn api.server:app --port 8001":

```bash
memorycontrol --stop-memory 100 --kill-memory 200 --check-interval 5 -- uvicorn api.server:app --port 8001
```

## Module

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