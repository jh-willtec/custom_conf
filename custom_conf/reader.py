import logging
from pathlib import Path
from typing import Any

from yaml import safe_load, YAMLError
from yaml.scanner import ScannerError


logger = logging.getLogger(__name__)


def read_yaml(path: Path) -> tuple[dict[str, Any], bool]:
    try:
        with open(path, encoding="utf-8") as config_file:
            return safe_load(config_file), True
    except (ScannerError, YAMLError) as error:
        if isinstance(error, ScannerError):
            # Indent error message.
            message = "\n\t".join(str(error).split("\n"))
        else:
            message = str(error)
        logger.error(f"Could not read configuration:\n\t{message}")
    return {}, False
