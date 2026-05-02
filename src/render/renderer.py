import pygame
from src.manager import Manager
from src.map.node import Node


class Renderer():
    def __init__(self, manager: Manager):
        pygame.init()
        screen = pygame.display.set_mode((1000, 1000))
        clock = pygame.time.Clock()

    def draw_nodes(self, nodes: list[Node]):
        for node in nodes:
            coordinates = node.coords

    def end(self):
        pygame.quit()
