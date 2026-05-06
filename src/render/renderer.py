import pygame
import time
from typing import Any
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
    "rainbow": pygame.Color(255, 255, 255)
}

class VisualNode():
    def __init__(self, coords: tuple[Any, Any],
                 color: str, scale: float, surface: pygame.Surface) -> None:
        self.coords = coords
        if color == "rainbow":
            self.color = COLORS["rainbow"]
        else:
            self.color = COLORS[color]
        self.scale = scale
        self.surface = surface

    def get_coords(self) -> tuple[float, float]:
        return self.coords

    def draw(self) -> None:
        pygame.draw.circle(self.surface, self.color, 
                           self.coords, self.scale / 4)


class VisualConnection():
    def __init__(self, node_1: VisualNode, node_2: VisualNode,
                 surface: pygame.Surface) -> None:
        self.coords_1 = node_1.get_coords()
        self.coords_2 = node_2.get_coords()
        self.surface = surface
        self.color = pygame.Color(51, 51, 255)
        #import random
        #self.color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def draw(self):
        pygame.draw.line(self.surface, self.color,
                         self.coords_1, self.coords_2)



class VisualDrone():
    def __init__(self) -> None:
        pass


class Renderer():
    def __init__(self, manager: Manager):
        self.manager = manager
        pygame.init()

        self.set_window_size()

        self.surface = pygame.display.set_mode((self.width, self.height))




        self.create_visual_nodes()
        self.create_visual_connections()

        self.clock = pygame.time.Clock()

        # Passos deste init:
        # 1. Preparar janela para a impressao do mapa.                  DONE
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

    def set_window_size(self) -> None:
        self.scale = 100

        min_width = 800
        max_width = 1600
        min_height = 800
        max_height = 1000

        self.width = min_width
        self.height = min_height

        self.draw_width_margin = 200
        self.draw_height_margin = 200
        self.draw_width = self.width - self.draw_width_margin
        self.draw_height = self.height - self.draw_height_margin

        sorted_coords_x = sorted(self.manager.graph.nodes.values(),
                                 key=lambda node: node.coords[0])
        sorted_coords_y = sorted(self.manager.graph.nodes.values(),
                                 key=lambda node: node.coords[1])

        self.coords_x = [sorted_coords_x[0].coords[0],
                         sorted_coords_x[-1].coords[0]]
        self.coords_y = [sorted_coords_y[0].coords[1],
                         sorted_coords_y[-1].coords[1]]

        dimensions_x = (abs(self.coords_x[0]) +
                        abs(self.coords_x[1])) * self.scale
        dimensions_y = (abs(self.coords_y[0]) +
                        abs(self.coords_y[1])) * self.scale

        if dimensions_x > min_width:
            self.width = dimensions_x
            self.draw_width = self.width - self.draw_width_margin
        if dimensions_y > min_height:
            self.height = dimensions_y
            self.draw_height = self.height - self.draw_height_margin

        scale_x = self.scale
        scale_y = self.scale

        if self.width > max_width:
            self.width = max_width
            self.draw_width = max_width - self.draw_width_margin
            scale_x = (max_width /
                       (abs(self.coords_x[0]) + abs(self.coords_x[1])))
        if self.height > max_height:
            self.height = max_height
            self.draw_height = max_height - self.draw_height_margin
            scale_y = (max_height /
                       (abs(self.coords_y[0]) + abs(self.coords_y[1])))

        if abs(self.coords_x[0]) + abs(self.coords_x[1]) != 0:
            scale_x = (self.draw_width /
                       (abs(self.coords_x[0]) + abs(self.coords_x[1])))
        if abs(self.coords_y[0]) + abs(self.coords_y[1]) != 0:
            scale_y = (self.draw_height /
                       (abs(self.coords_y[0]) + abs(self.coords_y[1])))

        self.scale = scale_x if scale_x <= scale_y else scale_y
        self.scale = int(self.scale)

        self.middle_point_x = (self.coords_x[1] - self.coords_x[0]) / 2
        self.middle_point_y = (self.coords_y[1] - self.coords_y[0]) / 2

    def create_visual_nodes(self) -> None:
        self.visual_nodes = {}

        map_range_x = self.coords_x[1] - self.coords_x[0]
        map_range_y = self.coords_y[1] - self.coords_y[0]

        for node in self.manager.graph.nodes.values():
            x = 0
            y = 0

            if map_range_x == 0:
                x = self.width / 2
            else:
                x = (((node.coords[0] - self.coords_x[0]) * self.draw_width) /
                     map_range_x) + self.draw_width_margin / 2

            if map_range_y == 0:
                y = self.height / 2
            else:
                y = (((node.coords[1] - self.coords_y[0]) * self.draw_height) /
                     map_range_y) + self.draw_height_margin / 2
                y = (self.height / 2) + ((self.height / 2) - y)

            if node.name == "maze_dead_a":
                print(f"x {x} | y {y}")
            if node.name == "maze_trap_a3":
                print(f"x {x} | y {y}")

            self.visual_nodes[node.name] = (
                VisualNode((x, y), node.color, self.scale, self.surface))

    def create_visual_connections(self) -> None:
        self.visual_connections = []

        for connection in self.manager.graph.connections.values():
            node_1 = self.visual_nodes[connection.node_1]
            node_2 = self.visual_nodes[connection.node_2]
            if (connection.node_1 == "maze_dead_a" and connection.node_2 == "maze_trap_a3") or (connection.node_1 == "maze_trap_a3" and connection.node_2 == "maze_dead_a"):
                print(f"A -> {node_1.get_coords()} | B -> {node_2.get_coords()}")
            self.visual_connections.append(
                VisualConnection(node_1, node_2, self.surface))


    def draw_nodes(self) -> None:
        for node in self.visual_nodes.values():
            node.draw()

    def draw_connections(self) -> None:
        for connection in self.visual_connections:
            connection.draw()

    def run(self) -> None:
        for turn in self.manager.turns:
            for event in turn:
                #self.screen.fill()
                self.draw_connections()
                self.draw_nodes()
                pygame.display.flip()
                time.sleep(2)
        #pygame.quit()
