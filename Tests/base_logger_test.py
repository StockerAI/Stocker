
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from Control.Loggers.base_logger import Logger

def base_logger_tester():

    logger = Logger("example", log_file="example.log", verbose=False)
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")


if __name__ == "__main__":
    base_logger_tester()
