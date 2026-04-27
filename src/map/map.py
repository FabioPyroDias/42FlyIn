import sys
from typing import Any
from src.map.node import Node
from src.map.connection import Connection


class Map():
    def __init__(self, configs: dict[str, Any]) -> None:
        """
        
        """

        # self.drones holds the number of drones
        self.drone_count = configs["nb_drones"]

        # self.nodes will hold every single node in the graph.
        # This list starts with the "start_hub" node
        self.nodes = dict({configs["start_hub"]["name"]: Node(configs["start_hub"], start_hub=True)})

        # Add all intermidary nodes.
        hubs = configs.get("nodes", None)
        if hubs:
            for hub in hubs:
                self.nodes[hub["name"]] = Node(hub)

        # Finish the list with the "end_hub" node
        self.nodes[configs["end_hub"]["name"]] = Node(configs["end_hub"], end_hub=True)

        # Holding references for easier access to "start_hub" and "end_hub"
        self.start_hub = self.nodes[configs["start_hub"]["name"]]
        self.end_hub = self.nodes[configs["end_hub"]["name"]]

        # This dictionary will hold all neighbours for every single node
        connections: dict[str, set[str]] = {}

        # This dictionary will hold Connection instances
        # The difference beteen this "self.connections" and "connections"
        #   is that "connections" alone only holds the neighbours.
        # "self.connections" holds all the information of that Connection.
        # Two keys will hold the exact same instance.
        # Example:
        # Connection A - B will have two keys: "A-B" and "B-A".
        # Following this, if a drone intends to move from A to B
        #   and other drone from B to A, both of these two are the
        #   same connection. Therefore, any change in one direction
        #   must be reflected on the other.
        self.connections: dict[str, Connection] = {}

        # Both nodes in the connection will exist as keys.
        # Check the key already exists.
        #   If not, create the key and the value will be the connected node
        #   If it does, add the connected node to the value
        # This way, it's ensured that all nodes will reference all neighbours
        #
        # In the case of "self.connections", parser already assured that
        #   connection only appear one-sided, once.
        # So, if "A-B" appears, "B-A" doesn't. Therefore, the key will never
        #   be repeated. But both keys need to exist.
        for connection in configs["connections"]:
            node1_name = connection["node1"]
            node2_name = connection["node2"]

            node1 = connections.get(node1_name, None)
            if not node1:
                connections[node1_name] = set([node2_name])
            else:
                connections[node1_name].add(node2_name)
            node2 = connections.get(node2_name, None)
            if not node2:
                connections[node2_name] = set([node1_name])
            else:
                connections[node2_name].add(node1_name)
            
            connection_info = Connection(connection.get("max_link_capacity", 1))
            self.connections[f"{node1_name}-{node2_name}"] = connection_info
            self.connections[f"{node2_name}-{node1_name}"] = connection_info

        # === Fabio ALgorithm ===
        # We start with the "start_hub"
        # We get all the neighbours and we verify if they are the "end_hub"
        #   If so, add the list containing both to "self.paths"
        #   If they're not, add them to the "queue"
        #
        # - self.paths will hold all the valid nodes that
        #       connect "start_hub" to "end_hub".
        # - queue holds tuples of three arguments:
        #       1. The current node
        #       2. The path from "start_hub" to that node, inclusively
        #       3. The cost of the path so far.
        #
        # The goal of the algorithm is simple: Get all valid paths
        #   that connect "start_hub" to "end_hub"
        #
        # To do this, we remove the first element of "queue".
        # We get the neighbours from the current node and, for each of them
        #   We check if the node already exists in the path.
        #       If so, we ignore this neighbour
        #   We check if it is the "end_hub", if it isn't, we add it to
        #       the path so far, update the cost, the current node and
        #       we add it back to the queue.
        #   If it is, we update the path and the cost,
        #       and add it to "self.paths"
        #   After all the neighbours are checked, we repeat the process again.
        # We repeat all these steps until the queue is empty.
        # After that, "self.paths" contains all
        #   valid paths alongside the respective cost.

        # Holds the valid paths
        self.paths = []
        # Holds the tuple with current node, path and cost.
        queue = []

        # Since the valid path must include the "start_hub", we can populate
        #   the queue with it's neighbours that are not a valid path.
        # If a valid path is found, we instead add it to "self.paths"
        for neighbour in connections.get(configs["start_hub"]["name"], []):
            if neighbour == self.end_hub:
                self.paths.append(tuple([[configs["start_hub"]["name"], neighbour], self.nodes[neighbour].get_cost()]))
            else:
                queue.append(tuple([neighbour, [configs["start_hub"]["name"], neighbour], self.nodes[neighbour].get_cost()]))

        # While there's still nodes to be explored, departing from "start_hub"
        #   the algorithm continues
        while len(queue) > 0:
            current_path = queue.pop(0)
            neighbours = connections[current_path[0]]
            for neighbour in neighbours:
                if neighbour in current_path[1]:
                    continue
                # If I don't copy the path, the object itself is changed,
                #   having some unexpected behaviours.
                # Copying the path and change it later, fixed it.
                new_path = current_path[1].copy()
                new_path.append(neighbour)
                if self.nodes[neighbour] == self.end_hub:
                    self.paths.append(tuple([new_path, current_path[2] + self.nodes[neighbour].get_cost()]))
                else:
                    queue.append(tuple([neighbour, new_path, current_path[2] + self.nodes[neighbour].get_cost()]))

        try:
            # If "self.paths" doesn't have any valid paths,
            #   the map is unsolvable
            if len(self.paths) == 0:
                raise ValueError("ERROR Map unsolvable")
        except ValueError as error:
            print(error)
            sys.exit()

        # Order the path by cost.
        self.paths = sorted(self.paths, key=lambda x: x[1])
