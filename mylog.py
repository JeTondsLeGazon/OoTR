import logging
from datetime import datetime

# TODO: parametrize logger
LOG_FILE = "log.log"
CSV_HEADER = "Action number,Action,Item found,Estimated time,Bonus,Malus,Path"


def create_logger(logger_name, log_file, formatter, level=logging.INFO, header=None):
    logger = logging.getLogger(logger_name)
    if not logger.hasHandlers():
        file_handler = logging.FileHandler(log_file, mode="w")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    logger.setLevel(level)
    logger.propagate = False
    if header:
        logger.info(header)
    return logger


def setup_logger(logger_name, log_file, level=logging.INFO):
    formatter = logging.Formatter("%(levelname)s : %(message)s")
    return create_logger(logger_name, log_file, formatter, level)


def setup_csv_logger(logger_name, log_file, level=logging.INFO):
    formatter = logging.Formatter("%(message)s")
    return create_logger(logger_name, log_file, formatter, level, CSV_HEADER)


logger = setup_logger("main", LOG_FILE)
logger.info(datetime.now().strftime("%H:%M:%S"))
