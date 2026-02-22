from pathlib import Path
from importlib import resources
from importlib.resources.abc import Traversable
from platformdirs import user_config_dir


class PackageDirs:
    def __init__(self):
        self.valley_config = resources.files("endfield_ocr_core.config").joinpath(
            "valley.toml"
        )
        self.wuling_config = resources.files("endfield_ocr_core.config").joinpath(
            "wuling.toml"
        )

        self.base_dir = Path(user_config_dir("endfield_ocr_core"))
        self.base_dir.mkdir(parents=True, exist_ok=True)

        self.log_dir = self.base_dir / "Logs"
        self.debug_files_dir = self.base_dir / "Debug"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.debug_files_dir.mkdir(parents=True, exist_ok=True)

    @property
    def valley(self) -> Traversable:
        return self.valley_config

    @property
    def wuling(self) -> Traversable:
        return self.wuling_config

    @property
    def logs(self) -> Path:
        return self.log_dir

    @property
    def debug_files(self) -> Path:
        return self.debug_files_dir
