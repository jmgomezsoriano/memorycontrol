import argparse
from memorycontrol import monitor


def main():
    parser = argparse.ArgumentParser(description="Monitor a process by its command line and memory limits.")
    parser.add_argument(
        '--command_line', type=str, required=True,
        help="Exact command line of the process to monitor (e.g., 'uvicorn api.server:app --port 8001')."
    )
    parser.add_argument('--memory_limit', type=int, default=100,
                        help="Memory limit in MB to send an interrupt signal (default: 100 MB).")
    parser.add_argument('--kill_memory_threshold', type=int, default=200,
                        help="Memory threshold in MB to forcefully terminate the process (default: 200 MB).")
    parser.add_argument('--check_interval', type=int, default=5,
                        help="Interval in seconds for memory checks (default: 5 seconds).")

    args = parser.parse_args()

    # Call the main monitoring function
    monitor(args.command_line, args.memory_limit, args.kill_memory_threshold, args.check_interval)


if __name__ == "__main__":
    main()
