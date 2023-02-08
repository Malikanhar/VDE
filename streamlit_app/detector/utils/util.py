""" Created on Wed Feb 08 11:34:38 2023

Utils helper for Vibrio Detector

@author: Malik Anhar Maulana
"""
import logging


def add_log_handler(
    logger: logging.Logger,
    log_level: int,
) -> None:
    """Handlers will be added to the logger:

    - StreamHandler
    """
    log_formatter = logging.Formatter(
        '[%(levelname)s %(asctime)s.%(msecs)03d %(filename)s:%(lineno)d] %(message)s', '%y%m%d %H:%M:%S')
    logger_stream_handler = logging.StreamHandler()
    logger_stream_handler.setLevel(log_level)
    logger_stream_handler.setFormatter(log_formatter)
    logger.addHandler(logger_stream_handler)
