import pygame
import time
from src.manager import Manager
from src.map.node import Node

METADATA_COLOR_VALUES = ["red", "yellow", "blue", "orange", "green", "purple",
                         "white", "gray", "black", "cyan", "brown", "lime",
                         "magenta", "gold", "maroon", "darkred", "crimson",
                         "violet", "rainbow"]

COLORS = {
    "red": pygame.Color(255, 0, 0),
    "yellow": pygame.Color(255, 255, 0),
    "blue": pygame.Color(0, 0, 255),
    "orange": pygame.Color(255, 125, 0),
    "green": pygame.Color(0, 255, 0),
    "purple": pygame.Color(125, 0, 255),
    "white": pygame.Color(255, 255, 255),
    "gray": pygame.Color(125, 125, 125),
    "black": pygame.Color(0, 0, 0),
    "cyan": pygame.Color(0, 255, 255),
    "brown": pygame.Color(139, 69, 19),
    "lime": pygame.Color(137, 243, 54),
    "magenta": pygame.Color(255, 0, 255),
    "gold": pygame.Color(239, 191, 4),
    "maroon": pygame.Color(85, 0, 0),
    "darkred": pygame.Color(149, 6, 6),
    "crimson": pygame.Color(178, 34, 34),
    "violet": pygame.Color(127, 0, 255),
    "rainbow": pygame.Color(0, 0, 0)
}

class NodeVisual():
    def __init__(self, node: Node) -> None:
        if node.color != "rainbow":
            node.color = COLORS[node.color]
        else:
            pass

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(self.screen, COLORS[node.color], 
                           (self.width / 2 * node.coords[0] / self.middle_point[0] + self.width / 4,
                           self.height / 2 * node.coords[1]),
                           self.scale / 3)


class DroneVisual():
    def __init__(self): -> None:
        pass


class Renderer():
    def __init__(self, manager: Manager):
        self.manager = manager
        pygame.init()
        self.width = 2000
        self.height = 1000
        self.draw_width = self.width - 400
        self.draw_height = self.height - 200
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.scale = 100

        coords_x = sorted(self.manager.graph.nodes.values(), key=lambda node: node.coords[0])
        coords_y = sorted(self.manager.graph.nodes.values(), key=lambda node: node.coords[1])
        self.coords_x = [coords_x[0].coords[0], coords_x[-1].coords[0]]
        self.coords_y = [coords_y[0].coords[1], coords_y[-1].coords[1]]
        self.middle_point = ((self.coords_x[0] + self.coords_x[1]) / 2,
                             (self.coords_y[0] + self.coords_y[1]) / 2)


        # Passos deste init:
        # 1. Preparar janela para a impressao do mapa.
        # 2. Criar representacoes visuais dos Nodes (NodeVisual)
        #   2.1. Definir cor
        #   2.2. Definir coordenadas adaptadas a janela.
        # 3. Criar representacoes visuais das Connections
        #   3.1. Especificar cor
        #   3.2. Definir inicio e fim.
        # 4. Criar representacoes visuais dos Drones (DroneVisual)
        #   4.1. Atribuir coordenadas aos Drones.
        # 5. Percorrer lista de turnos e cada evento
        #   5.1. Recriar eventos com animacao (X frames / Y segundos para cada turno simulado)

    def set_coords(self, node_coords: tuple[int, int]) -> tuple[int, int]:
        coord_x = 0
        coord_y = 0

        mid_point_x = self.draw_width / 2
        mid_point_y = self.draw_height / 2
        initial_pos_x = (self.width - self.draw_width) / 2
        initial_pos_y = (self.height - self.draw_height) / 2

        """ if self.middle_point[0] == 0:
            coord_x = mid_point_x * node_coords[0] / self.middle_point[0]
        else:
            coord_x = initial_pos_x + (mid_point_x * node_coords[0] / self.middle_point[0])

        if self.middle_point[1] == 0:
            if self.coords_y[-1].coords[1] == 0:
                coord_y = self.height / 2
            else:
                coord_y = initial_pos_y + (((node_coords[1] - self.coords_y[0].coords[1]) * ((self.draw_height) - initial_pos_y)) / (self.coords_y[-1].coords[0] - self.coords_y[0].coords[0]))
        else:
            coord_y = mid_point_y * node_coords[1] / self.middle_point[1]

        print(f"node_coords: {node_coords} -> {(coord_x, coord_y)}")
        return (coord_x, coord_y) """

    def draw_nodes(self):
        print(self.middle_point)
        for node in self.manager.graph.nodes.values():
            if node.color == "rainbow":
                pass
            else:
                pygame.draw.circle(self.screen, COLORS[node.color], 
                                   self.set_coords(node.coords),
                                   self.scale / 8)

    def run(self) -> None:
        for turn in self.manager.turns:
            for event in turn:
                #self.screen.fill()
                self.draw_nodes()
                pygame.display.flip()
                time.sleep(2)
        #pygame.quit()
