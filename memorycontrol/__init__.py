import platform

def monitor(program, memory_limit=100, kill_memory_threshold=200, check_interval=5):
    """
    Main function to monitor a process and manage its memory usage.

    Parameters:
    - program: The command of the process to monitor.
    - memory_limit: Memory limit in MB to send an interrupt signal (SIGINT or equivalent).
    - kill_memory_threshold: Memory threshold in MB to forcefully terminate the process (SIGKILL or equivalent).
    - check_interval: Time interval in seconds between memory checks.
    """
    system = platform.system().lower()
    
    if system == 'linux':
        from .linux import monitor_linux
        monitor_linux(program, memory_limit, kill_memory_threshold, check_interval)
    elif system == 'windows':
        from .windows import monitor_windows
        monitor_windows(program, memory_limit, kill_memory_threshold, check_interval)
    else:
        raise OSError(f"Operating system {system} not supported.")
