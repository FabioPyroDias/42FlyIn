import sys
from typing import Any
from src.consts import MAP_KEYS, HUB_METADATA_KEYS
from src.consts import METADATA_ZONE_VALUES, METADATA_COLOR_VALUES


class Parser():
    def __init__(self, map_name: str) -> None:
        self.map_name = map_name
        self.configs: dict[str, Any] = {}
        self.nodes: dict[str, tuple[int, int]] = {}
        self.line = 0

    def add_node(self, key: str, node: dict[str, Any]) -> None:
        """
        Checks for duplicated nodes.
        If not, add node to list.

        Args:
            key (str): key to add the node
            node (dict[str, Any]): node the be added

        Returns:
            None

        Notes:
            - Raises ValueError if duplicated node
        """

        # Ensures there's only one "start_hub" or "end_hub"
        if key == "start_hub" or key == "end_hub":
            node_start = self.configs.get("start_hub", None)
            node_end = self.configs.get("end_hub", None)

            # Check for duplicates with the same key
            if key == "start_hub" and node_start:
                raise ValueError("Repeated \"start_hub\". Already exists")
            if key == "end_hub" and node_end:
                raise ValueError("Repeated \"end_hub\". Already exists")

            # Check if "start_hub" or "end_hub" node already exists
            for node_name in self.nodes.keys():
                if node["name"] == node_name:
                    raise ValueError(f"Node repeated in \"{key}\"")
                if node["coordinates"] == self.nodes[node_name]:
                    raise ValueError(f"Repeated coordinates: "
                                     f"Node {node_name} has the same "
                                     f"coordinates as {node_name}")

            # "start_hub" and "end_hub" need to have the "max_drones" metadata
            number_drones = node.get("max_drones", -1)
            if number_drones < 0:
                node["max_drones"] = self.configs["nb_drones"]
            elif number_drones < self.configs["nb_drones"]:
                raise ValueError(f"\"max_drones\" metadata field in "
                                 f"\"{key}\" is smaller than "
                                 f"\"nb_drones\"")

            # "start_hub" and "end_hub" cannot be a "blocked" zone
            zone_type = node.get("zone", None)
            if zone_type and zone_type == "blocked":
                raise ValueError(f"\"{key}\" zone cannot be \"blocked\"")

            self.configs[key] = node
            self.nodes[node["name"]] = node["coordinates"]
            return

        # Verify duplicates in existing nodes
        for existing_node in list(self.nodes.keys()):
            if existing_node == node["name"]:
                raise ValueError(f"Repeated node: {node['name']}")
            if self.nodes[existing_node] == node["coordinates"]:
                raise ValueError(f"Repeated coordinates: "
                                 f"Node {node['name']} has the same "
                                 f"coordinates as {existing_node}")

        if not self.configs.get("nodes", None):
            self.configs["nodes"] = [node]
            self.nodes[node["name"]] = node["coordinates"]
            return

        self.configs["nodes"].append(node)
        self.nodes[node["name"]] = node["coordinates"]

    def add_connection(self, connection: dict[str, Any]) -> None:
        """
        Checks for duplicated connections.
        If not, add connection to list.

        Args:
            node (dict[str, Any]): node the be added

        Returns:
            None

        Notes:
            - Raises ValueError if duplicated node
        """

        connections = self.configs.get("connections", None)

        if not connections:
            self.configs["connections"] = [connection]
            return

        node1 = connection["node1"]
        node2 = connection["node2"]

        for existing_connection in connections:
            equality = 0
            if (existing_connection == node1 or
               existing_connection == node1):
                equality += 1
            if (existing_connection == node2 or
               existing_connection == node2):
                equality += 1
            if equality == 2:
                raise ValueError("Connection invalid. "
                                 "Connection already exists")

        self.configs["connections"].append(connection)

    def validate_hubs(self, key: str, arguments: str) -> dict[str, Any]:
        """
        Validates "start_hub", "end_hub" and "hub".
        Validates node name, coordinates and it's metadata

        Args:
            key (str): is one of "start_hub", "end_hub", "hub" keys
            arguments (str): node information in line

        Returns:
            dict[str, Any]: valid node structure

        Notes:
            - Raises ValueError if line is not correctly configured
        """

        node: dict[str, Any] = {}

        node_values = arguments.split(" ")

        # By the map config, each node needs to have
        #   - name      -> 0
        #   - x coord   -> 1
        #   - y coord   -> 2
        # Additionally, nodes can have three types of Metadata (these
        #   can show up in any order):
        #   - zone
        #   - color
        #   - max_drones
        # This means, nodes will have at least 3 fields
        #   and a maximum of 6 fields
        if len(node_values) < 3 or len(node_values) > 6:
            raise ValueError("Invalid number of arguments for Node")

        # Parsing Constraints: Zone names can use any valid characters
        #   but dashes and spaces
        node_name = node_values[0].strip()

        if len(node_name) == 0:
            raise ValueError("Node name cannot be empty")

        if "-" in node_name:
            raise ValueError("Node name cannot have dashes")

        node["name"] = node_name

        # Parsing Constraints: valid integer coordinates
        node_coords_x = int(node_values[1].strip())
        node_coords_y = int(node_values[2].strip())
        node["coordinates"] = (node_coords_x, node_coords_y)

        # If there's no Metadata, return the node info
        if len(node_values) == 3:
            return node

        # Metadata needs to be presented between [].
        if (node_values[3][0] != "[" or
           node_values[len(node_values) - 1][-1] != "]"):
            raise ValueError("Metadata must be within []")

        # Metadata Fields
        metadata_index = 3
        while metadata_index < len(node_values):
            # Metadata fields follow the "key=value" format
            metadata = node_values[metadata_index].split("=")

            if len(metadata) != 2:
                raise ValueError("Metadata must have "
                                 "key=value")

            # All Metadata fields do not have [].
            #   This is just an encapsulation.
            # In order to validate the metadata keys, [] need to be removed.
            metadata_key = metadata[0].strip()
            metadata_value = metadata[1].strip()
            if metadata_index == 3:
                metadata_key = metadata_key[1:]
            if metadata_index == len(node_values) - 1:
                metadata_value = metadata_value[0:-1]

            if metadata_key not in HUB_METADATA_KEYS:
                raise ValueError(f"Metadata key {metadata_key} invalid")

            if metadata_key == "zone":
                if metadata_value not in METADATA_ZONE_VALUES:
                    raise ValueError(f"Specified {metadata_key} invalid. "
                                     f"Accepted Values: "
                                     f"{METADATA_ZONE_VALUES}")
                node[metadata_key] = metadata_value
            elif metadata_key == "color":
                if metadata_value not in METADATA_COLOR_VALUES:
                    raise ValueError(f"Specified {metadata_key} invalid. "
                                     f"Accepted Values: "
                                     f"{METADATA_COLOR_VALUES}")
                node[metadata_key] = metadata_value
            else:
                value = int(metadata_value)
                if value <= 0:
                    raise ValueError(f"Specified {metadata_key} invalid. "
                                     f"Value must be positive")
                if key == "start_hub" or key == "end_hub":
                    if value < self.configs["nb_drones"]:
                        raise ValueError(f"{metadata_key} in {key} cannot be "
                                         f"less than nb_drones: "
                                         f"{self.configs['nb_drones']}")
                node[metadata_key] = value

            metadata_index += 1

        return node

    def validate_connections(self, arguments: str) -> dict[str, Any]:
        """
        Validates "connections".
        Validates node name and it's metadata

        Args:
            arguments (str): connection information in line

        Returns:
            dict[str, Any]: valid connection structure

        Notes:
            - Raises ValueError if line is not correctly configured
        """

        connection: dict[str, Any] = {}

        nodes = self.configs.get("nodes", None)

        # Connections depends on existing nodes.
        if not nodes:
            raise ValueError("Connection invalid. No nodes available")

        connection_values = arguments.split(" ")

        # By the map config, each connection needs to have
        #   - node1
        #   - node2
        # Additionally, connections can have one type of Metadata:
        #   - max_link_capacity
        # This means, connection will have at least 1 field
        #   and a maximum of 2 fields
        if len(connection_values) < 1 and len(connection_values) > 2:
            raise ValueError("Invalid number of arguments for Connection")

        # Each node name is separated by "-" and they can't be empty
        node_names = connection_values[0].split("-")

        if len(node_names) != 2:
            raise ValueError("Invalid number of arguments for Connection")

        if len(node_names[0]) == 0 or len(node_names[1]) == 0:
            raise ValueError("Connection invalid. Node cannot be empty")

        # Nodes need to already exist
        if not (node_names[0] in self.nodes.keys() and
                node_names[1] in self.nodes.keys()):
            raise ValueError(f"Connection invalid. "
                             f"Node not found in {connection_values[0]}")

        # Nodes cannot be connected to themselves
        if node_names[0] == node_names[1]:
            raise ValueError("Connection invalid. "
                             "Connection between the same node is not valid")

        connection["node1"] = node_names[0]
        connection["node2"] = node_names[1]

        # Metadata fields
        if len(connection_values) == 2:
            metadata = connection_values[1].split("=")

            # Metadata follows the format key=value
            if len(metadata) != 2:
                raise ValueError(f"Metadata for connection "
                                 f"{connection_values[0]} invalid.")

            # Metada is between []
            if metadata[0][0] != "[" or metadata[1][-1] != "]":
                raise ValueError(f"Metadata for connection "
                                 f"{connection_values[0]} invalid. "
                                 f"Needs to be within []")

            # Removing []
            metadata[0] = metadata[0][1:]
            metadata[1] = metadata[1][:-1]

            if metadata[0] != "max_link_capacity":
                raise ValueError(f"Metadata for connection "
                                 f"{connection_values[0]} invalid. "
                                 f"Expected key \"max_link_capacity\"")

            metadata_value = int(metadata[1])

            if metadata_value < 0:
                raise ValueError(f"Metadata for connection "
                                 f"{connection_values[0]} invalid. "
                                 f"Value must be positive integer")

            connection["max"] = metadata_value

        return connection

    def parse_line(self, line: str) -> None:
        """
        Validates lines with content.
        Ensures the keys are "start_hub", "end_hub", "hub", "connection"
            as well as their values are correct.

        Args:
            line (str): line of the file already trimmed

        Returns:
            None

        Notes:
            - Raises ValueError if line is not correctly configured
        """

        elements = line.split(":")

        # After split, ensures there is a "key:value" format
        if len(elements) != 2:
            raise ValueError(f"Invalid configuration in \"{line.strip()}\"")

        key = elements[0].strip()

        # If key isn't start_hub, end_hub, hub or connection, raise Error
        if key not in MAP_KEYS:
            raise ValueError(f"{key} invalid")

        # If nb_drones already appeared, there's a duplicated key
        if key == "nb_drones":
            if self.configs.get("nb_drones", None):
                raise ValueError("nb_drones duplicated")

            # Typecasts number of drones to integer
            number_of_drones = int(elements[1].strip())

            if number_of_drones <= 0:
                raise ValueError("\"nb_drones\" must be positive")

            self.configs["nb_drones"] = number_of_drones
            return

        if key == "start_hub" or key == "end_hub" or key == "hub":
            if not self.configs.get("nb_drones", None):
                raise ValueError("First key must be \"nb_drone\"")
            node = self.validate_hubs(key, elements[1].strip())
            self.add_node(key, node)
        else:
            connection = self.validate_connections(elements[1].strip())
            self.add_connection(connection)

    def parse_map(self) -> dict[str, Any]:
        """
        Opens the map file and parses it, getting all the map information

        Args:
            None

        Returns:
            dict[str, Any]: map information

        Notes:
            - Raises ValueError and FileNotFoundError
        """

        try:
            with open(self.map_name, 'r') as map:
                for line in map:
                    self.line += 1
                    clean_line = line.strip()
                    if len(clean_line) == 0 or clean_line[0] == "#":
                        continue
                    self.parse_line(clean_line)

            # Checks if all required keys exist
            # - nb_drones
            # - start_hub
            # - end_hub
            # - nodes []
            # - connections []
            checker_drones = self.configs.get("nb_drones", None)
            if not checker_drones:
                raise ValueError("Required key not found: nb_drones")

            checker_start_hub = self.configs.get("start_hub", None)

            if not checker_start_hub:
                raise ValueError("Required key not found: start_hub")

            checker_end_hub = self.configs.get("end_hub", None)
            if not checker_end_hub:
                raise ValueError("Required key not found: end_hub")

            checker_hubs = self.configs.get("nodes", None)
            if not checker_hubs:
                raise ValueError("Required key not found: hub")

            checker_connections = self.configs.get("connections", None)
            if not checker_connections:
                raise ValueError("Required key not found: connection")

            return self.configs

        except FileNotFoundError:
            sys.exit(f"ERROR Line {self.line}: {self.map_name} not found")
        except ValueError as error:
            sys.exit(f"ERROR Line {self.line}: {error}")
