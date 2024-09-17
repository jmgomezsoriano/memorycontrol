import platform
import os

from enum import Enum
from logging import getLogger
from time import sleep
from typing import List, Union, Callable

from psutil import Process, NoSuchProcess, AccessDenied, process_iter
from signal import Signals


class Signal(Enum):
    """ Sent signals. """
    STOP = 1
    KILL = 2


class StandardOS(Enum):
    """ Operative systems. """
    UNIX = 1
    WINDOWS = 2


OS = {'linux': StandardOS.UNIX, 'darwin': StandardOS.UNIX, 'windows': StandardOS.WINDOWS}

logger = getLogger(__name__)


def send_signal(process: Process, signal: Signal) -> None:
    """ Send a STOP or KILL signals to a process.

    :param process: The process to stop or kill
    :param signal: The signal to send.
    """
    try:
        # Get the OS code
        system = OS[platform.system().lower()]
        # If it is a stop signal
        if signal == Signal.STOP:
            if system == StandardOS.UNIX:
                os.kill(process.pid, Signals.SIGINT)
            else:
                process.terminate()
            logger.info(f'Terminate signal sent to process {process.pid}.')
        # If it is a kill signal
        elif signal == Signal.KILL:
            if system == StandardOS.UNIX:
                os.kill(process.pid, Signals.SIGKILL)
            else:
                process.kill()
            logger.info(f'Process {process.pid} killed.')
        # If it is a wrong signal
        else:
            raise ValueError(f'Wrong signal: "{signal.name}". Accepted signals: SIGINT or SIGKILL.')
    except KeyError:
        # Raise an exception if the OS platform is not supported
        raise OSError(f'Operating system {platform.system()} not supported. '
                      f'The supported OS are: Linux, Darwin and Windows')
    except NoSuchProcess:
        logger.warning(f'Process with PID {process.pid} not found.')
    except AccessDenied:
        logger.error(f'Permission denied to send signal to process {process.pid}.')


def stop(processes: Union[Process, List[Process]]) -> None:
    """ Send a stop signal to a process or a list of processes.

    :param processes: The process or processes.
    """
    processes = [processes] if isinstance(processes, Process) else processes
    for process in processes:
        send_signal(process, Signal.STOP)


def kill(processes: Union[Process, List[Process]]) -> None:
    """ Send a kill signal to a process or a list of processes.

    :param processes: The process or processes.
    """
    processes = [processes] if isinstance(processes, Process) else processes
    for process in processes:
        send_signal(process, Signal.KILL)


def always_run() -> bool:
    """ Default function to stop the monitor. By default, it never stops.
    :return: Always True.
    """
    return False


def monitor(
        command: List[str],
        stop_memory: int,
        kill_memory: int,
        check_interval: int = 5,
        stop_condition: Callable[[], bool] = always_run
) -> None:
    """ Monitor an OS command and terminate it if it exceeds memory usage limits.

    :param command: The command to monitor, e.g., 'python ./test.py' or 'python.exe .\test.py'.
    :param stop_memory: The memory threshold (in MB/GB) at which a stop signal is sent.
    :param kill_memory: The maximum memory usage (in MB/GB) before forcefully killing the process.
    :param check_interval: Time interval (in seconds) between memory usage checks.
    :param stop_condition: A callable function that determines when the monitor should stop.
           By default, the monitor runs indefinitely.
    """
    stop_signal = False
    while not stop_condition():
        processes = get_processes(command)
        if processes:
            memory_usage = sum([p.memory_info().rss for p in processes]) / (1024 * 1024)  # Convert to MB
            logger.info(f'Memory usage by {command}: {memory_usage:.2f}MB')
            if kill_memory and memory_usage > kill_memory:
                logger.warning(f'Memory usage exceeds the kill threshold ({kill_memory}MB). '
                               f'Forcefully terminating the process...')
                kill(processes)
            elif memory_usage > stop_memory:
                if not stop_signal:
                    logger.info(f'Memory usage exceeds the first threshold ({stop_memory}MB), send stop signal.')
                    stop(processes)
                    stop_signal = True  # Mark that we attempted to terminate the process
                else:
                    logger.info(f'Memory usage exceeds the first threshold but stop signal already sent. '
                                f'Continue monitoring...')
            else:
                stop_signal = False
        else:
            logger.info(f'The process with command line {command} was not found. '
                        f'Retrying in {check_interval} seconds...')
        sleep(check_interval)


def get_processes(command: List[str]) -> List[Process]:
    """ Find processes by its command line, excluding the current script's process.

    :param command: The command to check.
    :return: A list of processes that match with that command.
    """
    return [process for process in process_iter(['pid', 'cmdline']) if match_command(command, process.info['cmdline'])]


def match_command(command: List[str], process: List[str]) -> bool:
    """ Check when a command and a process are compatible.

    :param command: The command to find.
    :param process: The process command to compare with.

    :return: True if both command lines are equivalents, otherwise, False.
    """
    if command and process and len(command) == len(process) and command[0] in process[0]:
        for i, cmd in enumerate(command[1:], 1):
            if cmd != process[i]:
                return False
        return True
    return False
