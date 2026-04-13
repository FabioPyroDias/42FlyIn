import sys
from typing import Any
from src.consts import MAP_KEYS, HUB_METADATA_KEYS
from src.consts import METADATA_ZONE_VALUES, METADATA_COLOR_VALUES


class Parser():
    def __init__(self, map_name: str) -> None:
        self.map_name = map_name
        self.configs: dict[str, Any] = {}

    def add_node(self, node: dict[str, Any]) -> None:
        """
        Checks for duplicated nodes.
        If not, add node to list.

        Args:
            node (dict[str, Any]): node the be added

        Returns:
            None

        Notes:
            - Raises ValueError if duplicated node
        """

        nodes = self.configs.get("nodes", None)

        if not nodes:
            self.configs["nodes"] = [node]
            return

        for existing_node in nodes:
            if existing_node["name"] == node["name"]:
                raise ValueError(f"Repeated node: {node['name']}")
            if existing_node["coordinates"] == node["coordinates"]:
                raise ValueError(f"Repeated coordinates: "
                                 f"Node {node['name']} has the same "
                                 f"coordinates as {existing_node['name']}")

        self.configs["nodes"].append(node)

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
            self.configs["connections"] = connection
            return

        node1 = connection["node1"]
        node2 = connection["node2"]

        for existing_connection in connections:
            equality = 0
            if (existing_connection["node1"] == node1 or
               existing_connection["node2"] == node1):
                equality += 1
            if (existing_connection["node1"] == node2 or
               existing_connection["node2"] == node2):
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

        #TODO: Verificar se coneccao tem o mesmo node1 e node2
        # Exemplo:
        # nodeA-nodeA -> ERRO!

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
        if node_names[0] not in nodes or node_names[1] not in nodes:
            raise ValueError(f"Connection invalid. "
                             f"Node not found in {connection_values[0]}")

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

    def parse_first_line(self, line: str) -> int:
        """
        Ensures the first line of map file is "nb_drones: positive integer"

        Args:
            line (str): The first line of the file already trimmed

        Returns:
            int: number of drones

        Notes:
            - Raises ValueError if line is not correctly configured
        """

        first_line_elements = line.split(":")

        # After split, ensures there is a "key:value" format and
        #   the key is "nb_drones"
        if (len(first_line_elements) != 2 or
           first_line_elements[0].strip() != "nb_drones"):
            raise ValueError("First line should have \"nb_drones:\""
                             "followed by positive integer")

        # Typecasts number of drones to integer
        number_of_drones = int(first_line_elements[1].strip())

        if number_of_drones <= 0:
            raise ValueError("\"nb_drones\" must be positive")

        return number_of_drones

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

        # By now, when this method is called, nb_drones already appeared.
        #   If it appears now, there's a duplicated key
        if key == "nb_drones":
            raise ValueError("nb_drones duplicated")

        if key == "start_hub" or key == "end_hub" or key == "hub":
            node = self.validate_hubs(key, elements[1].strip())
            self.add_node(node)
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
                line_index = 0
                for line in map:
                    clean_line = line.strip()
                    if line_index == 0:
                        self.configs["nb_drones"] = (
                            self.parse_first_line(clean_line))
                        line_index += 1
                    else:
                        if len(clean_line) == 0 or clean_line[0] == "#":
                            continue

                        self.parse_line(clean_line)

            # Checks if all required keys exist
            checker_drones = self.configs.get("nb_drones", None)
            if not checker_drones:
                raise ValueError("Required key not found: nb_drones")

            return self.configs

        except FileNotFoundError:
            sys.exit(f"ERROR: {self.map_name} not found")
        except ValueError as error:
            sys.exit(f"ERROR: {error}")
