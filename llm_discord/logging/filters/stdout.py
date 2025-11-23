import logging


class StdoutFilter(logging.Filter):
    def filter(self, record):
        return record.levelno <= logging.WARN
