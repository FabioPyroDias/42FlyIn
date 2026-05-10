from typing import Any


class MapConfig():
    def __init__(self, configs: dict[str, Any]) -> None:
        """
        Serves as a container for the parsed map configuration

        Args:
            None

        Returns:
            None
        """

        self.configs = configs
