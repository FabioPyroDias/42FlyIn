from src.parser.parser import Parser
from src.map.map import Map
from src.manager import Manager

if __name__ == "__main__":

    parser = Parser("test2.txt")
    configs = parser.parse_map()
    graph = Map(configs)
    manager = Manager(graph)