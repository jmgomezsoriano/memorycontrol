try:
    import psutil
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "ModuleNotFoundError: No module named 'psutil'. Please install it with the command:\n\n"
        "pip install psutil"
    )

import os
import time

def send_ctrl_c_or_terminate(process):
    """Attempts to send a CTRL_C_EVENT or terminate the process gracefully."""
    try:
        # First, try to terminate the process gracefully
        process.terminate()
        print(f"Terminate signal sent to process {process.pid}.")
        
        try:
            process.wait(timeout=5)  # Wait for 5 seconds for process to terminate
        except psutil.TimeoutExpired:
            print(f"Process {process.pid} did not terminate within the timeout, continuing to monitor...")
    except psutil.NoSuchProcess:
        print(f"Process with PID {process.pid} not found.")
    except psutil.AccessDenied:
        print(f"Permission denied to send signal to process {process.pid}.")

def force_kill(process):
    """Forcefully terminates the process."""
    try:
        process.kill()
        print(f"Process {process.pid} has been forcefully terminated.")
    except psutil.NoSuchProcess:
        print(f"Process with PID {process.pid} not found.")
    except psutil.AccessDenied:
        print(f"Permission denied to terminate process {process.pid}.")

def get_process(command_line):
    """Finds the process by its exact command line, excluding the current script's process."""
    current_pid = os.getpid()  # Get the PID of the current script process
    script_name = os.path.basename(__file__)  # Get current filename
    for proc in psutil.process_iter(['pid', 'cmdline']):
        cmdline = proc.info['cmdline']
        
        # Ensure cmdline is a valid list before attempting to join it
        if cmdline and isinstance(cmdline, list):
            cmdline_str = " ".join(cmdline)

            # Exclude the current script's process and check if the command line matches
            if proc.info['pid'] != current_pid and script_name not in cmdline  and command_line in cmdline_str:
                print(f"Process found: {proc.info}")
                return proc
    return None

def monitor_windows(command_line, memory_limit, kill_memory_threshold, check_interval):
    """Continuously monitors the memory usage of a process and terminates it if necessary."""
    ctrl_c_sent = False  # Variable to track if termination attempt has already been made

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
                print(f"Memory usage exceeds the kill threshold ({kill_memory_threshold}MB). Forcefully terminating the process...")
                force_kill(process)

            elif memory_usage > memory_limit:
                if not ctrl_c_sent:
                    print(f"Memory usage exceeds the first threshold ({memory_limit}MB). Attempting to send CTRL_C_EVENT...")
                    send_ctrl_c_or_terminate(process)
                    ctrl_c_sent = True  # Mark that we attempted to terminate the process
                else:
                    print(f"Memory usage exceeds the first threshold but CTRL_C_EVENT already sent. Monitoring continues...")

            else:
                print("Memory usage is within limits. Continuing to monitor...")
                # Do not reset ctrl_c_sent here to prevent sending CTRL_C_EVENT multiple times

            time.sleep(check_interval)

        except psutil.NoSuchProcess:
            print(f"The process with command line '{command_line}' has ended.")
            break
