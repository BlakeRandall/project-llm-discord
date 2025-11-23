import sys
import logging
from llm_discord.logging.filters.stderr import StderrFilter


class StderrHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__(stream=sys.stderr)
        self.addFilter(StderrFilter())
