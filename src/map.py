from typing import Any


class Map():
    def __init__(self, configs: dict[str, Any]) -> None:
        self.start_hub = Node(configs["start_hub"])
        self.end_hub = Node(configs["end_hub"])
        self.zones = []
