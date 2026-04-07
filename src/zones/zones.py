from abc import ABC


class Zone(ABC):
    def __init__(self, cost: int = 1, is_blocked: bool = False,
                 priority: bool = False) -> None:
        self.cost = cost
        self.is_blocked = is_blocked
        self.priority = priority

    def get_cost(self) -> int:
        return self.cost

    def get_is_blocked(self) -> bool:
        return self.is_blocked

    def get_priority(self) -> bool:
        return self.priority


class NormalZone(Zone):
    pass


class BlockedZone(Zone):
    def __init__(self) -> None:
        super().__init__(is_blocked=True)


class RestrictedZone(Zone):
    def __init__(self) -> None:
        super().__init__(cost=2)


class PriorityZone(Zone):
    def __init__(self) -> None:
        super().__init__(priority=True)
