from src.map.zones import NormalZone, BlockedZone, RestrictedZone, PriorityZone
from typing import Any

class Node():
    def __init__(self, configs: dict[str, Any]):
        self.name = configs["name"]
        self.coords = configs["coordinates"]
        zone = configs.get("zone", "normal")
        if zone == "normal":
            self.zone = NormalZone()
        elif zone == "blocked":
            self.zone = BlockedZone()
        elif zone == "restricted":
            self.zone = RestrictedZone()
        elif zone == "priority":
            self.zone = PriorityZone()

        self.color = color
        self.current_drones = current_drones
        self.max_drones = max_drones
