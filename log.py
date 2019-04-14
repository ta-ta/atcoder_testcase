# -*- coding: utf-8 -*-

import logging

from config import LOGGER

formatter = logging.Formatter('%(message)s')

logger = logging.getLogger(LOGGER)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)
