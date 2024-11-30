"""Logging module."""

import re
import json
from datetime import datetime
from pathlib import Path
import logging
from logging.handlers import TimedRotatingFileHandler

from config import ENV


# https://pkg.go.dev/github.com/shafiqaimanx/pastax/colors
STYLES = {
    "ENDC": "\033[0m",
    "BOLD": "\033[1m",
    "ITALIC": "\033[3m",
    "UNDERLINE": "\033[4m",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "BLUE": "\033[34m",
    "MAGENTA": "\033[35m",
    "CYAN": "\033[36m",
    "DARKGRAY": "\033[90m",
    "LIGHTRED": "\033[91m",
    "PINK": "\033[95m",
    "FIREBRICK": "\033[38;5;124m",
    "ORANGERED": "\033[38;5;202m",
    "TOMATO": "\033[38;5;203m",
    "GRAPEFRUIT": "\033[38;5;208m",
    "DARKORANGE": "\033[38;5;214m",
    "OKRED": "\033[91m",
    "OKGREEN": "\033[92m",
    "OKYELLOW": "\033[93m",
    "OKBLUE": "\033[94m",
    "OKMAGENTA": "\033[95m",
    "OKCYAN": "\033[96m",
}

# With name version (for debugging)
# LOG_FORMAT = "%(asctime)s | %(name)-12s | %(levelname)-8s | %(message)s"
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class ANSIColorRemovingFormatter(logging.Formatter):
    def format(self, record):
        formatted = super().format(record)
        return re.sub(r"\x1b\[[0-9;]*m", "", formatted)


class TqdmLogger:
    def write(self, message: str):
        log_info(message.lstrip("\r\n"))

    def flush(self):
        pass


def setup_advanced_logger(
    logger_name: str = None,
    log_level: str = "INFO",
    log_format: str = LOG_FORMAT,
    date_format: str = LOG_DATE_FORMAT,
    log_to_console: bool = True,
    log_to_file: bool = True,
    log_dir: str = "logs",
    file_rotation: str = "midnight",
    file_backup_count: int = 7,
) -> logging.Logger:
    """
    Setup an advanced logger with flexible configuration options.
    Keeps colors in console output, removes them in file output.

    Args:
        logger_name (str): Name of the logger. If None, root logger is used.
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_format (str): Format string for log messages.
        date_format (str): Format string for timestamps in log messages.
        log_to_console (bool): Whether to log to console.
        log_to_file (bool): Whether to log to file.
        log_dir (str): Directory to store log files.
        log_file_prefix (str): Prefix for log file names.
        file_rotation (str): When to rotate the log file (e.g., 'midnight', 'h' for hourly).
        file_backup_count (int): Number of backup log files to keep.

    Returns:
        logging.Logger: Configured logger object.
    """
    # Create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Create formatters
    color_formatter = logging.Formatter(log_format, datefmt=date_format)
    no_color_formatter = ANSIColorRemovingFormatter(log_format, datefmt=date_format)

    # Console handler (with colors)
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(color_formatter)
        logger.addHandler(console_handler)

    # File handler (without colors)
    if log_to_file:
        log_dir_path = Path(log_dir)
        log_dir_path.mkdir(parents=True, exist_ok=True)

        current_date = datetime.now().strftime("%Y-%m-%d")
        log_file_name = f"{current_date}.log"
        log_file_path = log_dir_path / log_file_name

        file_handler = TimedRotatingFileHandler(
            filename=log_file_path,
            when=file_rotation,
            backupCount=file_backup_count,
        )
        file_handler.setFormatter(no_color_formatter)
        file_handler.flush = lambda: file_handler.stream.flush()
        logger.addHandler(file_handler)

    return logger


def pretty_dict(s: str) -> str:
    """Pretty print dictionary.

    Args:
        s (str): The dictionary to pretty print.

    Returns:
        str: The pretty printed dictionary.
    """
    json_str = json.dumps(s, indent=2, ensure_ascii=False)
    json_str = json_str.replace('\\"', "'")
    return json_str


def slog(
    msg: str, style: str | None = None, level: str = "info", dump: bool = True
) -> str:
    """Stylish log message.

    Args:
        msg (str): The message to log.
        style (str): The style of the message.
        level (str): The log level.
        dump (bool): The dump flag.

    Returns:
        str: The stylish message.
    """
    try:
        if dump:
            msg = pretty_dict(msg)
            msg = msg.strip('"')  # remove redundant quotes
    except:
        pass

    if ENV in ("dev", "prd"):
        stylish_msg = msg
    elif style:
        stylish_msg = f"{STYLES['BOLD']}{STYLES[style]}{msg}{STYLES['ENDC']}"
    else:
        stylish_msg = msg

    match level:
        case "info":
            logger.info(stylish_msg)
        case "error":
            logger.error(stylish_msg)
        case "warning":
            logger.warning(stylish_msg)
        case "debug":
            logger.debug(stylish_msg)
        case _:
            print(stylish_msg)

    return stylish_msg


def log_info(msg: str, dump: bool = True) -> str:
    """Stylish info log.

    Args:
        msg (str): The message to log.
        dump (bool): The dump flag. Defaults to True.
    """
    return slog(msg, style="GREEN", dump=dump)


def log_success(msg: str, dump: bool = True, prefix: bool = True) -> str:
    """Stylish success log.

    Args:
        msg (str): The message to log.
        dump (bool): The dump flag. Defaults to True.
        prefix (bool): The prefix flag. Defaults to True.
    """
    if prefix:
        msg = f"[SUCCESS] {msg}"
    return slog(msg, style="OKBLUE", dump=dump)


def log_error(msg: str, dump: bool = False, prefix: bool = True) -> str:
    """Stylish error log.

    Args:
        msg (str): The message to log.
        dump (bool): The dump flag. Defaults to True.
    """
    if prefix:
        msg = f"[FAILED] {msg}"
    return slog(msg, style="TOMATO", level="error", dump=dump)


def log_warning(msg: str, dump: bool = False, prefix: bool = True) -> str:
    """Stylish warning log.

    Args:
        msg (str): The message to log.
        dump (bool): The dump flag. Defaults to True.
    """
    if prefix:
        msg = f"[WARNING] {msg}"
    return slog(msg, style="GRAPEFRUIT", level="warning", dump=dump)


def log_api(msg: str, error: bool = False) -> None:
    """Stylish api log.

    Args:
        msg (str): The message to log.
        error (bool): The error status of the API. Defaults to False.
    """
    if error:
        log_error("Request API:")
        log_error(msg, dump=True)
    else:
        log_success("Request API:")
        log_success(msg)


# Setup default logger
logger = setup_advanced_logger()


# Disable logging for specific modules
for name in ("elastic_transport.transport", "urllib3.connectionpool", "httpx"):
    _logger = logging.getLogger(name)
    _logger.setLevel(logging.ERROR)

# Get tqdm file
tqdm_file = TqdmLogger()


if __name__ == "__main__":
    log_info("This is an info message.")
    log_success("This is a success message.")
    log_error("This is an error message.")
    log_warning("This is a warning message.")
    log_api("This is an API message.")
    for style in STYLES:
        slog(f"This is a {style} message.", style=style)
