from src.parser.parser import Parser
from src.map.map import Map

if __name__ == "__main__":

    parser = Parser("test3.txt")
    configs = parser.parse_map()
    graph = Map(configs)