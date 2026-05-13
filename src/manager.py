from typing import Optional, Any
from src.map.drone import Drone
from src.map.map import Map
from src.map.connection import Connection
from src.map.zones import RestrictedZone


class Manager():
    def __init__(self, graph: Map) -> None:
        """
        Sets up the simulation and creates the Drones

        Args:
            graph (Map): contains all the information for the simulation

        Returns:
            None
        """

        # Graph holds all the information of the map
        self.graph = graph

        # "active_drones" possesses all the drones actively running
        #   in the simulation
        # When they arrive at "end_hub", they will be removed.
        self.active_drones = []

        # Holds the history for each turn.
        # There's two formats possible:
        #   1. The drone already arrived at the target node:
        #   [drone_id, target_node]
        #   2. The drone is in the middle of the connection:
        #   [drone_id, current_node, target_node]
        # Every turn, a new list will be added to "self.turns"
        self.turns: list[list[Any]] = []

        # The number of turns it took to complete the simulation
        self.complete_simulation = 0

        # Instantiating the drones
        drone_index = 0
        while drone_index < self.graph.drone_count:
            self.active_drones.append(Drone(f"D{drone_index + 1}",
                                            self.graph.start_hub))
            self.graph.start_hub.current_drones += 1
            drone_index += 1

    def run(self) -> None:
        """
        Runs the simulation until the end.
        Keeps track of each event in each turn and the number of turns

        Args:
            None

        Returns:
            None
        """

        # Counts the turns. "self.complete_simulation" will hold this
        #   value when the simulation is over
        turns = 0

        # The best optimal path for the map
        current_path = self.graph.path

        # This algorithm was developed to take into account more than one path.
        # After analising the results, multiple paths had worse efficiency.
        # So, the "self.paths" is now only one path.
        # The while loop in line 113 is just a one loop iteration.
        # Yes, I could have removed it and have the code cleaner, but I'm lazy.
        # ----------
        # The algorithm is divided into simple steps with a set of rules:
        #   1. It will run while there are drones outside the "end_hub".
        #   2. The "current_drone" will take into account the
        #       "previous_drone" position.
        #       This will highly influence the drone pathing.
        #   3. First check is if there is a drone in the connection between
        #       the node where the "current_drone" is and the node where
        #       it needs to go.
        #       If there is, skip this drone.
        #   4. Check if the "target_node" can possess the "current_drone".
        #       Since there's only one path and all the drones will follow it,
        #       If the node's zone is "restricted", a node variable
        #       "to_arrive" will be checked. This ensures the "current_drone"
        #       can start to move into that node and it will arrive when
        #       the "previous_drone" already left.
        #   5. If all this conditions are valid, the "target_node" will be
        #       assigned to the destination of the "current_drone" and all
        #       it's relevant parameters updated.
        #   6. After cycling through all the nodes, makes them move and
        #       follows another set of parameters update.
        #   7. If the "drone.move()" message exists, a successful movement
        #       was made. This needs to be stored and, at the end of the turn,
        #       printed as well as stored in the "turn_history" which
        #       will be added in the "self.turns".
        #   8. Finally, the drones "current_node" are checked to validate
        #       if they arrived at "end_hub". If so, remove them from
        #       "self.active_drones".
        #       To avoid any unpredictable behaviour, the "self.active_drones"
        #       is looped from end to start.
        while len(self.active_drones) > 0:
            drone_index = 0
            turn_history = []
            output_message = ""
            for drone in self.active_drones:

                # In case the drone is already moving, there's no need to
                #   check for a Connection or set a new "target_node".
                # Simply call the "move()" method, store the output message
                #   as well as the event in the turn history.
                # After that, skip the current turn for this specific drone
                if drone.is_moving:
                    drone_message = drone.move()
                    if len(drone_message) != 0:
                        if len(output_message) == 0:
                            output_message = drone_message
                        else:
                            output_message += f" {drone_message}"

                        if drone.current_node and drone.target_node:
                            turn_history.append(
                                [drone.drone_id,
                                 drone.current_node.name,
                                 drone.target_node.name])
                        else:
                            turn_history.append(
                                [drone.drone_id, drone.current_node.name])

                    # continue keyword simply skips this iteration.
                    continue

                # Get the current node where the drone is at the current turn
                current_node = drone.current_node
                current_node_name = current_node.name

                # Get the "next_node" in the path and, alongside the
                #   "current_node", gets the Connection between both.
                current_node_index = current_path.index(current_node_name)
                next_node_name = current_path[current_node_index + 1]
                connection: Optional[Connection] = self.graph.connections[
                    f"{current_node_name}-{next_node_name}"]

                # Check the Connection capacity. (Step 3)
                if connection and (connection.current_drones ==
                                   connection.max_link_capacity):
                    connection = None
                    continue

                # Now evaluates the capacity of the "target_node".
                #   With the exception of being a "RestrictedZone" (Step 4)
                next_node = self.graph.nodes[next_node_name]
                if next_node.current_drones == next_node.max_drones:
                    if isinstance(next_node.zone, RestrictedZone):
                        if next_node.to_arrive >= 2:
                            connection = None
                            next_node = None
                            continue
                    else:
                        connection = None
                        next_node = None
                        continue

                # If every check is valid, the drone now has a
                #   "target_node" assigned.
                if connection:
                    drone.set_target(next_node, connection)
                drone_index += 1

                # After the drones evaluation is done and successfull
                #   the "move()" method is called.
                # If there is movement, the message will have a length
                #   greater than 0. This message is stored to be printed
                #   at the end of the turn, alongisde all other sucessfull
                #   movements. (Step 7)
                drone_message = drone.move()
                if len(drone_message) != 0:
                    if len(output_message) == 0:
                        output_message = drone_message
                    else:
                        output_message += f" {drone_message}"

                    # Here it's decided the format of the message depending
                    #   if the drone reached the "target_node" in the
                    #   same turn or is still moving to it.
                    if drone.is_moving:
                        if drone.current_node and drone.target_node:
                            turn_history.append(
                                [drone.drone_id,
                                 drone.current_node.name,
                                 drone.target_node.name])
                    else:
                        turn_history.append(
                            [drone.drone_id, drone.current_node.name])

            # Finished turn and stored all of the events.
            self.turns.append(turn_history)

            # Display the turn events output
            print(output_message)

            # Check and remove drones that already
            #   arrived at "end_hub" (Step 8)
            drone_index = len(self.active_drones) - 1
            while drone_index >= 0:
                drone = self.active_drones[drone_index]
                if drone.current_node == self.graph.end_hub:
                    self.active_drones.pop(drone_index)
                    drone.coords = 0
                drone_index -= 1
            turns += 1

        # After the simulation is done, the number of turns is stored for
        #   future use in the "Renderer" class.
        self.complete_simulation = turns
