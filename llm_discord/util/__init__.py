import logging
import importlib
import pkgutil


logger = logging.getLogger(__name__)


def auto_import_submodules(package_name):
    package_info = importlib.import_module(package_name)
    logger.info(f"Importing submodules of {package_info}")
    for module_info in pkgutil.walk_packages(
        package_info.__path__, f"{package_info.__name__}."
    ):
        try:
            module = importlib.import_module(module_info.name)
            logger.info(f"Imported {module}")
        except Exception as exc:
            raise ImportError(f"Failed to import {module_info.name}") from exc
