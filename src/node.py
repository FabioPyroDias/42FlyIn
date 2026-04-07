class Node():
    def __init__(self, name: str, coords: tuple[int, int], zone: str,
                 color: str, current_drones: int = 0, max_drones: int = 1):
        self.name = name
        self.coords = coords
        self.zone = zone
        self.color = color
        self.current_drones = current_drones
        self.max_drones = max_drones
