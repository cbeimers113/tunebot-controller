import datetime
import os

from typing import List

from colorama import Fore, Style  # type: ignore


class Log:
    """A simple logging tool."""

    def __init__(self) -> None:
        """Initialize the logger."""
        self._pref_info: str = "INFO"
        self._pref_warn: str = "WARN"
        self._pref_error: str = "ERR"
        self._txt_log: List[str] = []

    def clear(self):
        """Clear the screen."""
        os.system("clear")

    def reprint_log(self):
        """Reprint the log to the console."""
        for message in self._txt_log:
            print(message)

    def info(self, message: str) -> None:
        """Log a message with the 'info' prefix."""
        self._log(message, prefix=self._pref_info, color=Fore.GREEN)

    def warn(self, message: str) -> None:
        """Log a message with the 'warn' prefix."""
        self._log(message, prefix=self._pref_warn, color=Fore.YELLOW)

    def error(self, message: str) -> None:
        """Log a message with the 'error' prefix."""
        self._log(message, prefix=self._pref_error, color=Fore.RED)

    def no_prefix(self, message: str) -> None:
        """Log a message with nothing preceeding it."""
        self._log(message, prefix=None, color=Fore.WHITE)

    def _log(self, message, prefix, color) -> None:
        """Auxiliary logging function."""
        now: datetime.datetime = datetime.datetime.now()
        hour: str = str(now.hour)
        minute: str = str(now.minute)

        if len(hour) == 1:
            hour = '0' + hour

        if len(minute) == 1:
            minute = '0' + minute

        output: str = f"({Fore.YELLOW}{hour}:{minute}{Style.RESET_ALL})[{color}{prefix}{Style.RESET_ALL}] {message}"

        if prefix is not None:
            self._txt_log.append(output)
            print(output)
        else:
            self._txt_log.append(message)
            print(message)
