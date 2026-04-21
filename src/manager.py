from src.map.drone import Drone
from src.map.map import Map


class Manager():
    def __init__(self, graph: Map):
        self.graph = graph
        self.active_drones = []
        self.finished_drones = []

        drone_index = 0
        while drone_index < self.graph.drone_count:
            self.active_drones.append(Drone(drone_index, self.graph.start_hub))
            self.graph.start_hub.current_drones += 1
            drone_index += 1

        # This is the map solving logic
        while len(self.active_drones) > 0:
            return
