from src.map.zones import Zone
from src.map.zones import NormalZone, BlockedZone, RestrictedZone, PriorityZone
from typing import Any


class Node():
    def __init__(self, configs: dict[str, Any],
                 start_hub: bool = False, end_hub: bool = False):
        self.name = configs["name"]
        self.coords = configs["coordinates"]
        zone = configs.get("zone", "normal")
        if zone == "normal":
            self.zone: Zone = NormalZone()
        elif zone == "blocked":
            self.zone = BlockedZone()
        elif zone == "restricted":
            self.zone = RestrictedZone()
        elif zone == "priority":
            self.zone = PriorityZone()

        self.color = configs.get("color", "gray")
        self.max_drones = configs.get("max_drones", 1)
        self.current_drones = 0

        self.start = start_hub
        self.end = end_hub

    def add_drone(self) -> None:
        self.current_drones += 1

    def remove_drone(self) -> None:
        self.current_drones -= 1

    def get_current_drones(self) -> int:
        return self.current_drones

    def get_cost(self) -> int:
        return self.zone.get_cost()

    def get_is_blocked(self) -> bool:
        return self.zone.get_is_blocked()

    def get_priority(self) -> bool:
        return self.zone.get_priority()
