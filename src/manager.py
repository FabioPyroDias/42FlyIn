from src.map.drone import Drone
from src.map.map import Map
import sys
import time

class Manager():
    def __init__(self, graph: Map):
        self.graph = graph
        self.active_drones = []
        self.finished_drones = []

        drone_index = 0
        while drone_index < self.graph.drone_count:
            self.active_drones.append(Drone(f"D{drone_index + 1}", self.graph.start_hub))
            self.graph.start_hub.current_drones += 1
            drone_index += 1

    # This method works and achieves all benchmarks for easy, medium and hard.
    # Impossible Dream becomes infinite loop.
    def run(self) -> None:
        turns = 0
        while len(self.active_drones) > 0:
            drone_index = 0
            output_message = ""
            for drone in self.active_drones:
                found_path = False
                path_index = 0
                while not found_path and path_index < len(self.graph.paths):
                    current_node = drone.current_node
                    current_path = self.graph.paths[path_index][0]
                    current_node_name = current_node.name
                    path_index += 1
                    if current_node_name not in current_path:
                        continue
                    current_node_index = current_path.index(current_node_name)
                    next_node_name = current_path[current_node_index + 1]
                    connection = self.graph.connections[f"{current_node_name}-{next_node_name}"]
                    #if drone.drone_id == "D3":
                        #print(f"DEBUG - Connection: {current_node_name}-{next_node_name}: {connection.current_drones}")
                    if connection.current_drones == connection.max_link_capacity:
                        #if drone.drone_id == "D3":
                            #print(f"DEBUG - Connection: {current_node_name}-{next_node_name}: {connection.current_drones}")
                        connection = None
                        continue
                    next_node = self.graph.nodes[next_node_name]
                    if next_node.current_drones == next_node.max_drones:
                        connection = None
                        next_node = None
                        continue

                    path_worth = False
                    if path_index - 1 > 0:
                        current_path_cost = self.graph.paths[path_index - 1][1]
                        worth = 0
                        compare_index = 0
                        while compare_index < path_index - 1:
                            if self.graph.paths[compare_index][1] + drone_index < current_path_cost:
                                worth += 1
                            compare_index += 1
                        if worth == path_index - 1:
                            path_worth = True
                    else:
                        path_worth = True

                    if path_worth:
                        #print(f"DEBUG (Inside path_worth): {drone}")
                        drone.set_target(next_node, connection)
                        found_path = True
                drone_index += 1

                #print(f"DEBUG: {drone}")
                #print(connection.current_drones)

                drone_message = drone.move()
                if len(drone_message) != 0:
                    if len(output_message) == 0:
                        output_message = drone_message
                    else:
                        output_message += f" {drone_message}"

                #print(f"DEBUG - {drone.drone_id}: Connection ({current_node_name}-{next_node_name}): {connection.current_drones}")

            print(output_message)
            drone_index = len(self.active_drones) - 1
            while drone_index >= 0:
                drone = self.active_drones[drone_index]
                if drone.current_node == self.graph.end_hub:
                    self.active_drones.pop(drone_index)
                    self.finished_drones.append(drone)
                drone_index -= 1
            turns += 1
        print(turns)


    """ def run_impossible_dream(self) -> None:
        drone_index = 0
        drone_paths = []
        while drone_index < len(self.active_drones):
            path_index = 0
            while path_index < len(self.graph.paths):
                drone_sim = self.active_drones[drone_index].copy()
                chosen_path_drone = []
                for path in drone_paths:
                    if path[0] == path_index:
                        chosen_path_drone.append(path[1])
                while drone_sim.current_node != self.graph.end_hub:
                    pass
                path_index += 1
            drone_index += 1 """
