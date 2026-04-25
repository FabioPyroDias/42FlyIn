from src.map.node import Node

class Drone():
    def __init__(self, drone_id: str, current_node: Node) -> None:
        self.drone_id = drone_id
        self.current_node = current_node
        self.target_node = None
        self.is_moving = False
        self.turns_to_move = 0

    def set_target(self, target_node: Node) -> None:
        if self.is_moving:
            return

        self.target_node = target_node
        self.turns_to_move = target_node.get_cost()
        self.is_moving = True

    def move(self) -> str:
        if not self.target_node:
            return ""

        if self.is_moving:
            self.turns_to_move -= 1
            if self.turns_to_move == 0:
                self.current_node = self.target_node
                self.target_node = None
                self.is_moving = False
                return f"{self.drone_id}-{self.current_node.name}"
            else:
                return (f"{self.drone_id}-{self.current_node.name}"
                        f"-{self.target_node.name}")
        return ""

    def __str__(self) -> str:
        return (f"Drone {self.drone_id} | "
               f"Current Node: {self.current_node.name} | "
               f"Target Node: {self.target_node} | "
               f"Turns to move: {self.turns_to_move} | "
               f"Reached end_hub: {self.reached_end_hub}")
