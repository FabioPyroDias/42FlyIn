from src.map.zones import Zone
from src.map.zones import NormalZone, BlockedZone, RestrictedZone, PriorityZone
from typing import Any


class Node():
    def __init__(self, configs: dict[str, Any],
                 start_hub: bool = False, end_hub: bool = False) -> None:
        """
        Node holds all the information of "hub" in the map.
        Holds the capacity and current drones using it

        Args:
            configs (dict[str, Any]): All the information of the current Node
            start_hub (bool): flag to indicate if the Node is the "start_hub"
            end_hub (bool): flag to indicate if the Node is the "end_hub"

        Returns:
            None
        """

        # All the basic information already parsed.
        self.name = configs["name"]
        self.coords = configs["coordinates"]

        # Instantiate the Zone Class.
        # This holds certain preset details of the Node, such as the cost.
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

        # This property will only be relevant the node is a RestrictedZone.
        # Whenever a Drone sets the Node as it's target, this property
        #   indicates how many turns will take the drone to arrive.
        # This will prove extremely useful to turn the solving algorithm
        #   way more efficient.
        self.to_arrive = 0

        # self.current_drones could be used as both a real drone count as
        #   well as a prediction. With this property, the purpose of
        #   self.current_drones is now only to keep track of the
        #   real drone count.
        self.predicted_drones = 0

        self.start = start_hub
        self.end = end_hub

    def add_predicted_drone(self) -> None:
        """
        Increases the current number of predicted drones

        Args:
            None

        Returns:
            None
        """

        self.predicted_drones += 1

    def remove_predicted_drone(self) -> None:
        """
        Decreases the current number of predicted drones

        Args:
            None

        Returns:
            None
        """

        self.predicted_drones -= 1

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
        Returns the current number of drones in the Node

        Args:
            None

        Returns:
            int: current number of drones
        """

        return self.current_drones

    def get_cost(self) -> int:
        """
        Returns the number of turns to arrive at the node

        Args:
            None

        Returns:
            int: turns to arrive at the node
        """

        return self.zone.get_cost()

    def get_is_blocked(self) -> bool:
        """
        Returns availability of the node

        Args:
            None

        Returns:
            bool: availability of the node
        """

        return self.zone.get_is_blocked()

    def get_priority(self) -> bool:
        """
        Returns preference in the pathfinding algorithm

        Args:
            None

        Returns:
            bool: preference in the pathfinding algorithm
        """

        return self.zone.get_priority()
