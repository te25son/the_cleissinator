import logging


# set format for all logs to read time - log level - message
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')


def setup_logger(name, log_file, level=logging.INFO, mode='a'):
    """
    Sets up a logger to be used by the Cleissinator
    """
    handler = logging.FileHandler(log_file, mode=mode)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
