import os
import sys
import logging
from logging import Logger
from contextlib import contextmanager

def setup_logger(output_file: str):
    if os.path.exists(output_file):
        os.remove(output_file)
    
    logger = logging.getLogger('spike_sorting')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(message)s')

    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Add file handler
    file_handler = logging.FileHandler(output_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

@contextmanager
def capture_console_output(logger: Logger):
    class LoggerWriter:
        def __init__(self, logger, level):
            self.logger = logger
            self.level = level

        def write(self, message):
            if message.rstrip() != "":
                self.logger.log(self.level, message.rstrip())

        def flush(self):
            pass

    stdout_original = sys.stdout
    stderr_original = sys.stderr

    try:
        sys.stdout = LoggerWriter(logger, logging.INFO)
        sys.stderr = LoggerWriter(logger, logging.ERROR)
        yield
    finally:
        sys.stdout = stdout_original
        sys.stderr = stderr_original