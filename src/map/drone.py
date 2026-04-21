from src.map.node import Node

class Drone():
    def __init__(self, drone_id: int, current_node: Node) -> None:
        self.drone_id = drone_id
        self.current_node = current_node
        self.target_node = None
        self.is_moving = False
        self.turns_to_move = 0
        self.reached_end_hub = False

    def set_target(self, target_node: Node) -> None:
        self.target_node = target_node
        self.turns_to_move = target_node.get_cost()
        self.is_moving = True

    def move(self) -> None:
        if self.reached_end_hub:
            return

        if self.is_moving:
            self.turns_to_move -= 1
            if self.turns_to_move == 0:
                self.current_node = self.target_node
                self.target_node = None
                self.is_moving = False
                if self.current_node.end_hub:
                    self.reached_end_hub = True
    
    def __str__(self) -> str:
        return (f"Drone {self.drone_id} | "
               f"Current Node: {self.current_node.name} | "
               f"Target Node: {self.target_node} | "
               f"Turns to move: {self.turns_to_move} | "
               f"Reached end_hub: {self.reached_end_hub}")