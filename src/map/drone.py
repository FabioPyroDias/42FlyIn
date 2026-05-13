from src.map.node import Node
from src.map.zones import RestrictedZone
from src.map.connection import Connection
from typing import Optional


class Drone():
    def __init__(self, drone_id: str, current_node: Node) -> None:
        """
        Drone travels through Nodes via Connections.

        Args:
            drone_id (str): Drone identifier
            current_node (Node): where the Drone exists currently.
                By default, it starts in the "start_hub"

        Returns:
            None
        """

        # Drone identifier
        self.drone_id = drone_id

        # These coordinates will change between being the same as a node
        #   and the middle point between two nodes.
        self.coords = current_node.coords
        self.in_node = True

        # The "current_node" where the drone is and the "target_node" is
        #   the node where our target is headed.
        #   In certain turns, drone might not have a target.
        self.current_node = current_node
        self.target_node: Optional[Node] = None
        self.is_moving = False

        # The cost of moving to a particular node
        self.turns_to_move = 0

        # Current connection between "current_node" and "target_node"
        self.connection: Optional[Connection] = None

    def set_target(self, target_node: Node, connection: Connection) -> None:
        """
        Sets the "target_node" to the desired destination as well as the
            connection between both "current_node" and "target_node"

        Args:
            target_node (Node): Desired Node location
            connection (Connection): Connection between "current_node" and
                "target_node"

        Returns:
            None
        """

        # If the drone is already moving, "target_node" cannot change
        # This happens specifically when traveling to a Node with the
        #   restricted zone
        if self.is_moving:
            return

        # Sets target and adds a drone to the Node
        self.target_node = target_node
        self.target_node.add_drone()

        # Sets connection and adds a drone to the Connection
        self.connection = connection
        self.connection.add_drone()

        # Affects flags and updates the "turns_to_move" to the
        #   "target_node" cost
        self.turns_to_move = target_node.get_cost()
        self.in_node = True
        self.is_moving = True

        # In case the "target_node" is a RestrictedZone, the Node records
        #   the number of turns it will take this drone to arrive at the
        #   node.
        if isinstance(target_node, RestrictedZone):
            target_node.to_arrive = self.turns_to_move

        # The drone coordinates are set to the middle of the Connection
        #   between "current_node" and "target_node".
        # When the method "move()" is called, the "turns_to_move"
        #   property is updated and, if the drone reached the "target_node"
        #   in that turn, the coordinates are updated to those of the target.
        # This is just a way to make the drone be in the middle of Connection
        self.coords = ((self.current_node.coords[0] +
                        self.target_node.coords[0]) / 2,
                       (self.current_node.coords[1] +
                        self.target_node.coords[1]) / 2)

    def move(self) -> str:
        """
        Moves drone.
        Simulates a turn

        Args:
            None

        Returns:
            str: Output message
        """

        # If there's no "target_node", the drone doesn't move
        if not self.target_node:
            return ""

        # Updates the turns to move
        self.turns_to_move -= 1

        # Reached the "target_node"
        if self.turns_to_move == 0:
            # If it took the drone one move to arrive to "target_node"
            #   remove the drone from the "current_node"
            if self.in_node:
                self.current_node.remove_drone()

            # Update the "current_node" to "target_node"
            # Reset the "target_node" to None
            self.current_node = self.target_node
            self.target_node = None

            # Remove drone from Connection and reset it to None
            if self.connection:
                self.connection.remove_drone()
                self.connection = None

            self.is_moving = False

            # As previously stated, the drone coordinates are now the exact
            #   same as the updated "current_node"
            self.coords = self.current_node.coords

            # Output message follows the "drone_id - current_node" format
            return f"{self.drone_id}-{self.current_node.name}"
        else:
            # Drone has left the current_node, updated it and update
            #   the turns to arrive to "target_node"
            # The only time this condition is reached it's when
            #   the drone is moving towards a Restricted zone.
            self.in_node = False
            self.current_node.remove_drone()
            self.target_node.to_arrive -= 1

            # Output message follows the
            #   "drone_id - current_node - target_node" format
            return (f"{self.drone_id}-{self.current_node.name}"
                    f"-{self.target_node.name}")
