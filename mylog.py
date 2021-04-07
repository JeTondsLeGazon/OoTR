import logging
from datetime import datetime

def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    if l.hasHandlers():
        l.handlers.clear()
    formatter = logging.Formatter('%(levelname)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    l.setLevel(level)

    l.addHandler(fileHandler)
    l.propagate = False
    
def setup_csv_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    if l.hasHandlers():
        l.handlers.clear()
    formatter = logging.Formatter('%(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    l.setLevel(level)

    l.addHandler(fileHandler)
    l.propagate = False
    l.info('Action number,Action,Item found,Estimated time,Bonus,Malus,Path')
    
LOG = 'log.log'

setup_logger('main', LOG)
logger = logging.getLogger('main')
logger.info(datetime.now().strftime("%H:%M:%S"))
logger.propagate = False