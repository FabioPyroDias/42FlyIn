from abc import ABC


class Zone(ABC):
    def __init__(self, cost: int = 1, is_blocked: bool = False,
                 priority: bool = False) -> None:
        """
        Base class for the Zone types of the Nodes

        Args:
            cost (int): turns to arrive at the node
            is_blocked (bool): availability of the node
            priority (bool): preference in the pathfinding algorithm

        Returns:
            None
        """

        self._cost = cost
        self._is_blocked = is_blocked
        self._priority = priority

    def get_cost(self) -> int:
        """
        Returns the number of turns to arrive at the node

        Args:
            None

        Returns:
            int: turns to arrive at the node
        """

        return self._cost

    def get_is_blocked(self) -> bool:
        """
        Returns availability of the node

        Args:
            None

        Returns:
            bool: availability of the node
        """

        return self._is_blocked

    def get_priority(self) -> bool:
        """
        Returns preference in the pathfinding algorithm

        Args:
            None

        Returns:
            bool: preference in the pathfinding algorithm
        """

        return self._priority


class NormalZone(Zone):
    pass


class BlockedZone(Zone):
    def __init__(self) -> None:
        """
        BlockedZone is the type of zone that's unreachable.
        The is_blocked property must be overwritten to "True"

        Args:
            None

        Returns:
            None
        """

        super().__init__(is_blocked=True)


class RestrictedZone(Zone):
    def __init__(self) -> None:
        """
        RestrictedZone takes two turns to arrive.
        The cost property must be overwritten to "2"

        Args:
            None

        Returns:
            None
        """

        super().__init__(cost=2)


class PriorityZone(Zone):
    def __init__(self) -> None:
        """
        PriorityZone is prefered in the pathfinding algorithm.
        The priority property must be overwritten to "True"

        Args:
            None

        Returns:
            None
        """

        super().__init__(priority=True)
