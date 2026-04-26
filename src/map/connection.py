class Connection():
    def __init__(self, max_link_capacity: int=-1) -> None:
        self.max_link_capacity = max_link_capacity
        self.current_drones = 0

    def add_drone(self) -> None:
        self.current_drones += 1

    def remove_drone(self) -> None:
        self.current_drones += 1

    def get_current_drones(self) -> int:
        return self.current_drones
