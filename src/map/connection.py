class Connection():
    def __init__(self, max_link_capacity: int,
                 node_1: str, node_2: str) -> None:
        """
        Bridge between two nodes.
        Holds the capacity and current drones using it

        Args:
            max_link_capacity (int): maximum number of drones simultaneously
            node_1 (str): name of the node
            node_2 (str): name of the node

        Returns:
            None
        """

        self.max_link_capacity = max_link_capacity
        self.current_drones = 0
        self.node_1 = node_1
        self.node_2 = node_2

    def add_drone(self) -> None:
        """
        Increases the current number of drones

        Args:
            None

        Returns:
            None
        """

        self.current_drones += 1

    def remove_drone(self) -> None:
        """
        Decreases the current number of drones

        Args:
            None

        Returns:
            None
        """

        self.current_drones -= 1

    def get_current_drones(self) -> int:
        """
        Returns the current number of drones in the Connection

        Args:
            None

        Returns:
            int: current number of drones
        """

        return self.current_drones
