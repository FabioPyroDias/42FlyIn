class Connection():
    def __init__(self, max_link_capacity: int,
                 node_1: str, node_2: str) -> None:
        self.max_link_capacity = max_link_capacity
        self.current_drones = 0
        self.node_1 = node_1
        self.node_2 = node_2

    def add_drone(self) -> None:
        self.current_drones += 1

    def remove_drone(self) -> None:
        self.current_drones -= 1

    def get_current_drones(self) -> int:
        return self.current_drones
