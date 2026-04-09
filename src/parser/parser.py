import sys
from typing import Any
from src.consts import MAP_KEYS, HUB_METADATA_KEYS
from src.consts import METADATA_ZONE_VALUES, METADATA_COLOR_VALUES


class Parser():
    def __init__(self, map_name: str) -> None:
        self.map_name = map_name

    def parse_first_line(line: str) -> int:
        """
        Ensures the first line of map file is "nb_drones: positive integer"

        Args:
            line (str): The first line of the file already trimmed.

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

    def parse_line(line: str) -> dict[str, dict[str, Any]]:
        """
        Validates lines with content.
        Ensures the keys are "start_hub", "end_hub", "hub", "connection"
            as well as their values are correct.

        Args:
            line (str): line of the file already trimmed.

        Returns:
            dict[str, dict[str, Any]]: valid key and node information

        Notes:
            - Raises ValueError if line is not correctly configured
        """

        elements = clean_line.split(":")

        # After split, ensures there is a "key:value" format
        if len(elements) != 2:
            raise ValueError(f"Invalid configuration in \"{line.strip()}\"")

        key = elements[0].strip()

        # If key 
        if key not in MAP_KEYS:
            raise ValueError(f"{key} invalid")
        if key == "nb_drones":
            raise ValueError("nb_drones duplicated")
        elif key == "start_hub" or key == "end_hub" or key == "hub":
            node = {}
            node_values = (elements[1].strip()).split(" ")
            if len(node_values) != 3 and len(node_values) != 4:
                raise ValueError("Invalid number of arguments for Node")
            node_name = node_values[0].strip()
            if len(node_name) == 0:
                raise ValueError("Node name cannot be empty")
            if "-" in node_name:
                raise ValueError("Node name cannot have dashes")
            node["name"] = node_name
            node_coords_x = int(node_values[1].strip())
            node_coords_y = int(node_values[2].strip())
            node["coordinates"] = (node_coords_x, node_coords_y)
            if len(node_values) == 4:
                if metadata[3][0] != "[" or metadata[3][-1] != "]":
                    raise ValueError("Metadata must be within []")
                metadata = node_values[3].split(" ")
                metadata_index = 0
                while metadata_index < len(metadata):
                    data = metadata[metadata_index].split("=")
                    if len(data) != 2:
                        raise ValueError("Metadata must have "
                                        "key=value")
                    metadata_key = data[0].strip()
                    metadata_value = data[1].strip()
                    if metadata_index == 0:
                        metadata_key = metadata_key[1:]
                    if metadata_index == len(data) - 1:
                        metadata_value = metadata_value[:-1]
                    
                    if metadata_key not in HUB_METADATA_KEYS:
                        raise ValueError("Metadata key invalid")
                    if metadata_key == "zone":
                        if metadata_value not in HUB_METADATA_KEYS:
                            raise ValueError("Specified zone invalid")
                    elif metadata_key == "color":
                        if metadata_value not in METADATA_COLOR_VALUES:
                            raise ValueError("Specified color invalid")
                    else:
                        value = int(metadata_value)
                        metadata_value = value
                        if key == "start_hub" or key == "end_hub":
                            if configs["nb_drones"] > metadata_value:
                                raise ValueError("max_drones cannot be lower than nb_drones in start_hub or end_hub")
                    
                    node[metadata_key] = metadata_value
                    metadata_index += 1

    def parse_map(self) -> dict[str, Any]:
        try:
            with open(self.map_name, 'r') as map:
                configs = {}
                line_index = 0
                for line in map:
                    clean_line = line.strip()
                    if line_index == 0:
                        configs["nb_drones"] = parse_first_line(clean_line)
                        line_index += 1
                    else:
                        if len(clean_line) == 0 or clean_line[0] == "#":
                            continue
                        parse_line(elements)
                        
                            #TODO Duplicate error not working
                            if configs.get("nodes", None):
                                if node["name"] in configs["nodes"]:
                                    raise ValueError("Node duplicated")
                        #connection
                        else:
                            pass


                except ValueError as error:
                    sys.exit(f"ERROR: {error}")
        except FileNotFoundError:
            sys.exit(f"ERROR: {self.map_name} not found")
