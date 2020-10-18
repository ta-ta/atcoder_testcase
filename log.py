from logging import getLogger, Formatter, StreamHandler, INFO

def get_logger(name):
    logger = getLogger(name)
    logger.setLevel(INFO)
    formatter = Formatter('%(message)s')

    handler = StreamHandler()
    handler.setLevel(INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
