import logging

'''
This is a global logger module used to instantiate a
logger instance on the file residing in the same dir
'''
LOG_FILE = 'setup.log'

def enable_logging(name):
    logFormatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger(name)

    fileHandler = logging.FileHandler(LOG_FILE)
    fileHandler.setFormatter(logFormatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)

    #consoleHandler = logging.StreamHandler()
    #consoleHandler.setFormatter(logFormatter)
    #logger.addHandler(consoleHandler)
    return logger
