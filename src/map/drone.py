from src.map.node import Node
from src.map.connection import Connection
from typing import Optional
import math


class Drone():
    def __init__(self, drone_id: str, current_node: Node) -> None:
        self.drone_id = drone_id
        self.coords = current_node.coords
        self.rotation = (0, 0)
        self.in_node = True
        self.current_node = current_node
        self.target_node: Optional[Node] = None
        self.is_moving = False
        self.turns_to_move = 0
        self.connection: Optional[Connection] = None

    def set_target(self, target_node: Node, connection: Connection) -> None:
        if self.is_moving:
            return

        self.target_node = target_node
        self.target_node.add_drone()

        self.connection = connection
        self.connection.add_drone()

        self.turns_to_move = target_node.get_cost()
        self.in_node = True
        self.is_moving = True

        self.coords = ((self.current_node.coords[0] + self.target_node.coords[0]) / 2,
                       (self.current_node.coords[1] + self.target_node.coords[1]) / 2)

        self.rotation = -math.degrees(math.atan2(self.target_node.coords[1] - self.current_node.coords[1],
                                                 self.target_node.coords[0] - self.current_node.coords[0]))

    def move(self) -> str:
        if not self.target_node:
            return ""

        if self.is_moving:
            self.turns_to_move -= 1
            if self.turns_to_move == 0:
                if self.in_node:
                    self.current_node.remove_drone()
                self.current_node = self.target_node

                self.target_node = None

                if self.connection:
                    self.connection.remove_drone()
                    self.connection = None

                self.is_moving = False

                self.coords = self.current_node.coords

                return f"{self.drone_id}-{self.current_node.name}"
            else:
                self.in_node = False
                self.current_node.remove_drone()

                return (f"{self.drone_id}-{self.current_node.name}"
                        f"-{self.target_node.name}")
        return ""

    def __str__(self) -> str:
        text = (f"Drone {self.drone_id} | "
                f"Current Node: {self.current_node.name} | "
                f"Target Node: ")
        if not self.target_node:
            text += "None | "
        else:
            text += f"{self.target_node.name} | "
        text += f"Turns to move: {self.turns_to_move}"

        return text
