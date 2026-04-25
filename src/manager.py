from src.map.drone import Drone
from src.map.map import Map
import sys

class Manager():
    def __init__(self, graph: Map):
        self.graph = graph
        self.active_drones = []
        self.finished_drones = []

        drone_index = 0
        while drone_index < self.graph.drone_count:
            self.active_drones.append(Drone(f"D{drone_index}", self.graph.start_hub))
            self.graph.start_hub.current_drones += 1
            drone_index += 1

    # This method works and achieves all benchmarks for easy, medium and hard.
    # Impossible Dream becomes infinite loop.
    def run(self) -> None:
        turns = 0
        while len(self.active_drones) > 0:
            drone_index = 0
            for drone in self.active_drones:
                found_path = False
                path_index = 0
                while not found_path and path_index < len(self.graph.paths):
                    current_path = self.graph.paths[path_index][0]
                    current_node_name = drone.current_node.name
                    path_index += 1
                    if current_node_name not in current_path:
                        continue
                    current_node_index = current_path.index(current_node_name)
                    next_node_name = current_path[current_node_index + 1]
                    connection = self.graph.connections[f"{current_node_name}-{next_node_name}"]
                    if connection.max_link_capacity > 0:
                        if connection.current_drones == connection.max_link_capacity:
                            continue
                    next_node = self.graph.nodes[next_node_name]
                    if next_node.max_drones > 0:
                        if next_node.current_drones == next_node.max_drones:
                            continue
                    drone.set_target(next_node)
                    drone.current_node.current_drones -= 1
                    next_node.current_drones += 1
                    found_path = True
                drone_index += 1
                
                drone_message = drone.move()
                if len(drone_message) != 0:
                    print(drone_message)


            drone_index = len(self.active_drones) - 1
            while drone_index >= 0:
                drone = self.active_drones[drone_index]
                if drone.current_node == self.graph.end_hub:
                    self.active_drones.pop(drone_index)
                    self.finished_drones.append(drone)
                drone_index -= 1
            turns += 1
        print(turns)


    def run_impossible_dream(self) -> None:
        pass