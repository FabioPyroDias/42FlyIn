from src.parser.parser import Parser
from src.map.map import Map
from src.manager import Manager

if __name__ == "__main__":

    #Easy
    parser = Parser("maps/easy/01_linear_path.txt")
    #parser = Parser("maps/easy/02_simple_fork.txt")
    #parser = Parser("maps/easy/03_basic_capacity.txt")
    #------------------

    #Medium
    #parser = Parser("maps/medium/01_dead_end_trap.txt")
    #parser = Parser("maps/medium/02_circular_loop.txt")
    #parser = Parser("maps/medium/03_priority_puzzle.txt")
    #------------------

    #Hard
    #parser = Parser("maps/hard/01_maze_nightmare.txt")
    #parser = Parser("maps/hard/02_capacity_hell.txt")
    #parser = Parser("maps/hard/03_ultimate_challenge.txt")
    #------------------

    #Challenger
    #parser = Parser("maps/challenger/01_the_impossible_dream.txt")

    configs = parser.parse_map()
    graph = Map(configs)
    manager = Manager(graph)
    manager.run()