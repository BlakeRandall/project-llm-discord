import logging
from llm_discord.config.app import AppConfig
from llm_discord.logging.handlers.stdout import StdoutHandler
from llm_discord.logging.handlers.stderr import StderrHandler

app_config = AppConfig()


def setup_logging():
    logging.basicConfig(
        level=app_config.log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[StdoutHandler(), StderrHandler()],
        force=True,
    )
