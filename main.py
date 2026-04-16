from src.zones.zones import NormalZone, BlockedZone
from src.zones.zones import RestrictedZone, PriorityZone
from src.parser.parser import Parser

if __name__ == "__main__":
    zones = [
        NormalZone(),
        BlockedZone(),
        RestrictedZone(),
        PriorityZone()
    ]

    parser = Parser("maps/hard/02_capacity_hell.txt")
    configs = parser.parse_map()
    graph = Map(configs)