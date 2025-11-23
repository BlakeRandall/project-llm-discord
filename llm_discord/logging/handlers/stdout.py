import sys
import logging
from llm_discord.logging.filters.stdout import StdoutFilter


class StdoutHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__(stream=sys.stdout)
        self.addFilter(StdoutFilter())
