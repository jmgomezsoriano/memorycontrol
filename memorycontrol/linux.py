try:
    import psutil
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "ModuleNotFoundError: No module named 'psutil'. Please install it with the command:\n\n"
        "pip install psutil"
    )

import os
import signal
import time

def send_ctrl_c(pid):
    """Sends the SIGINT (Ctrl+C) signal to the process."""
    try:
        os.kill(pid, signal.SIGINT)
        print(f"SIGINT signal sent to process {pid}.")
    except ProcessLookupError:
        print(f"Process with PID {pid} not found.")
    except PermissionError:
        print(f"Permission denied to send signal to process {pid}.")

def force_kill(pid):
    """Forcefully terminates the process with SIGKILL."""
    try:
        os.kill(pid, signal.SIGKILL)
        print(f"SIGKILL signal sent to process {pid}. Process has been forcefully terminated.")
    except ProcessLookupError:
        print(f"Process with PID {pid} not found.")
    except PermissionError:
        print(f"Permission denied to send signal to process {pid}.")

def get_process(command_line):
    """Finds the process by its exact command line, excluding the current script's process."""
    current_pid = os.getpid()  # Get the PID of the current script process
    script_name = os.path.basename(__file__)  # Get current filename
    for proc in psutil.process_iter(['pid', 'cmdline']):
        cmdline = " ".join(proc.info['cmdline'])
        
        # Exclude the current script's process and name, and check if the command line matches
        if proc.info['pid'] != current_pid and script_name not in cmdline and command_line in cmdline:
            print(f"Process found: {proc.info}")
            return proc
    return None

def monitor_linux(command_line, memory_limit, kill_memory_threshold, check_interval):
    """Continuously monitors the memory usage of a process and terminates it if necessary."""
    sigint_sent = False  # Variable to track if SIGINT has already been sent

    while True:
        process = get_process(command_line)

        if not process:
            print(f"The process with command line '{command_line}' was not found. Retrying in {check_interval} seconds...")
            time.sleep(check_interval)
            continue

        try:
            memory_usage = process.memory_info().rss / (1024 * 1024)  # Convert to MB
            print(f"Memory usage: {memory_usage:.2f}MB")

            if memory_usage > kill_memory_threshold:
                # If memory exceeds the kill threshold, forcefully terminate the process
                print(f"Memory usage exceeds the kill threshold ({kill_memory_threshold}MB). Sending SIGKILL...")
                force_kill(process.pid)

            elif memory_usage > memory_limit:
                if not sigint_sent:
                    print(f"Memory usage exceeds the first threshold ({memory_limit}MB). Attempting to send SIGINT...")
                    send_ctrl_c(process.pid)
                    sigint_sent = True  # Mark SIGINT as sent
            else:
                sigint_sent = False  # Reset the flag if memory usage drops below the first threshold

            time.sleep(check_interval)

        except psutil.NoSuchProcess:
            print(f"The process with command line '{command_line}' has ended.")
            break
