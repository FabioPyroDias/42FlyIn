import sys
from src.parser.parser import Parser
from src.map.map import Map
from src.manager import Manager
from src.render.renderer import Renderer

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError("Parameter not found: Map path and name "
                             "needs to be the second parameter")
    except ValueError as error:
        sys.exit(f"ERROR: {error}")

    parser = Parser(sys.argv[1])
    configs = parser.parse_map()
    graph = Map(configs)
    manager = Manager(graph)
    manager.run()
    renderer = Renderer(manager)
    renderer.run()
