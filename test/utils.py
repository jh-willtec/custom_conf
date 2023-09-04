from pathlib import Path

from custom_conf.config import BaseConfig


TEST_DIR = Path(__file__)


class TestConfig(BaseConfig):
    @property
    def config_dir(self) -> Path:
        return TEST_DIR

    @property
    def default_config_path(self) -> Path:
        return self.config_dir.joinpath()

    @property
    def source_dir(self) -> Path:
        return TEST_DIR.parents[1] / "src/custom_conf"
