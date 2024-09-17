import argparse
import logging

from memorycontrol import monitor


def main():
    parser = argparse.ArgumentParser(description="Monitor a process by its command line and memory limits.")
    parser.add_argument(
        'command', type=str, metavar='COMMAND', nargs='+',
        help="Exact command line of the process to monitor (e.g., 'uvicorn api.server:app --port 8001')."
    )
    parser.add_argument('-s', '--stop-memory', type=int, default=100, metavar='MB',
                        help="Memory limit in MB to send an interrupt signal. By default, 100 MB.")
    parser.add_argument('-k', '--kill-memory', type=int, default=200, metavar='MB',
                        help='Memory threshold in MB to forcefully terminate the process. By default, 200 MB.'
                             'If this argument is set to 0, then, no limit.')
    parser.add_argument('--check-interval', type=int, default=5, metavar='SECONDS',
                        help="Interval in seconds for memory checks (default: 5 seconds).")
    parser.add_argument('--log-level', metavar='LEVEL', type=str, default='WARNING',
                        choices=('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
                        help='Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')

    args = parser.parse_args()
    if args.kill_memory and args.kill_memory <= args.stop_memory:
        parser.error('The --kill-memory cannot be equal or lower than --stop-memory' )

    log_level = getattr(logging, args.log_level, logging.WARNING)
    logging.basicConfig(level=log_level)
    # Call the main monitoring function
    monitor(args.command, args.stop_memory, args.kill_memory, args.check_interval)


if __name__ == "__main__":
    main()
