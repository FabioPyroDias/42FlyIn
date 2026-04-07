import sys
from typing import Any


class Parser():
    def __init__(self, map_name: str) -> None:
        self.map_name = map_name

    def parse_map(self) -> dict[str, Any]:
        try:
            with open(self.map_name, 'r') as map:
                configs = {}
                line_index = 0
                try:
                    for line in map:
                        clean_line = line.strip()
                        if line_index == 0:
                            first_line_elements = clean_line.split(":")
                            if (len(first_line_elements) != 2 or
                               first_line_elements[0].strip() != "nb_drones"):
                                raise ValueError("First line should have "
                                                 "\"nb_drones:\" followed by "
                                                 "positive integer")
                            number_of_drones = int(
                                first_line_elements[1].strip())
                            if number_of_drones <= 0:
                                raise ValueError("\"nb_drones must be "
                                                 "positive\"")
                            configs["nb_drones"] = number_of_drones
                        line_index += 1
                except ValueError as error:
                    sys.exit(f"ERROR: {error}")
        except FileNotFoundError:
            sys.exit(f"ERROR: {self.map_name} not found")
