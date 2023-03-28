import os
import logging
from pathlib import Path
from datetime import datetime
from rich.logging import RichHandler

class Logger:
    def __init__(
            self, name: str, level: str = "DEBUG", 
            log_file: str = None, verbose: bool = False,
            enable_datetime_stamp: bool = True, 
            out_dir: str = "./"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if verbose:
            self.handler = RichHandler(show_time=False, rich_tracebacks=True)
            formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
            self.handler.setFormatter(formatter)
            self.logger.addHandler(self.handler)

        if log_file:
            Path(out_dir).mkdir(parents=True, exist_ok=True)
            log_file_prefix = datetime.now().strftime('%Y-%m-%dT%H-%M-%S') if enable_datetime_stamp else ""
            log_file_path = os.path.join(out_dir, f"{log_file_prefix}_{log_file}")
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setLevel(level)
            file_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)