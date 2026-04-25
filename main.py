from src.parser.parser import Parser
from src.map.map import Map
from src.manager import Manager

if __name__ == "__main__":

    parser = Parser("test3.txt")
    #parser = Parser("maps/challenger/01_the_impossible_dream.txt")
    configs = parser.parse_map()
    graph = Map(configs)
    manager = Manager(graph)
    manager.run()