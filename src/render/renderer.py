import sys
import pygame
from typing import Any
from src.manager import Manager
from src.map.node import Node
from src.map.zones import Zone, NormalZone, PriorityZone
from src.map.zones import BlockedZone, RestrictedZone

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
                 color: str, scale: float, surface: pygame.Surface,
                 zone: Zone) -> None:
        """
        Visual representation of the Node.
        Responsible for initializing

        Args:
            coords (tuple[int, int]): node coordinates in the graphic space
            color (str): node color
            scale (float): the visual scale of the node
            surface (pygame.Surface): Where the node will be drawn
            zone (Zone): Normal, Priority, Reserved or Blocked Zone

        Returns:
            None
        """

        self.coords = coords
        self.color_name = color
        self.color = COLORS[self.color_name]
        self.scale = scale
        self.surface = surface

        # Aids the scale of the node
        factor = 4

        if self.color_name != "rainbow":
            # Load the images, separated by layers.
            # This gives a much better look to the nodes
            self.border_surface = pygame.image.load("assets/Border.png").convert_alpha()
            self.base_surface = pygame.image.load("assets/Base.png").convert_alpha()
            self.highlight_surface = pygame.image.load("assets/Highlight.png").convert_alpha()
            self.shadow_surface = pygame.image.load("assets/Shadow.png").convert_alpha()

            # Image dimensions based on the scale and factor
            image_width = self.border_surface.get_width() * ((self.scale / 100) / factor)
            image_height = self.border_surface.get_height() * ((self.scale / 100) / factor)

            # Some images will change their color based on the color parameter.
            #   fill() method is used to tint the node with the passed color.
            # These will use the special flag "BLEND_MULT"
            self.border_surface = pygame.transform.scale(self.border_surface, (int(image_width), int(image_height)))
            self.base_surface = pygame.transform.scale(self.base_surface, (int(image_width), int(image_height)))
            self.base_surface.fill(self.color, special_flags=pygame.BLEND_MULT)
            self.highlight_surface = pygame.transform.scale(self.highlight_surface, (int(image_width), int(image_height)))
            self.highlight_surface.fill(self.color, special_flags=pygame.BLEND_MULT)
            self.shadow_surface = pygame.transform.scale(self.shadow_surface, (int(image_width), int(image_height)))
        else:
            # In case there's a "rainbow" color, a specific image is loaded
            #   with a rainbow pattern.
            self.rainbow_surface = pygame.image.load("assets/RainbowNode.png").convert_alpha()

            image_width = self.rainbow_surface.get_width() * ((self.scale / 100) / factor)
            image_height = self.rainbow_surface.get_height() * ((self.scale / 100) / factor)

            self.rainbow_surface = pygame.transform.scale(self.rainbow_surface, (int(image_width), int(image_height)))

        # The nodes have Zones and, if they're not "Normal", which is the
        #   standard zone type, an image is loaded to identify the nodes.
        self.zone_surface = None

        if not isinstance(zone, NormalZone):
            self.zone_surface = pygame.image.load("assets/Zone.png").convert_alpha()
            zone_width = self.zone_surface.get_width() * ((self.scale / 100) / factor)
            zone_height = self.zone_surface.get_height() * ((self.scale / 100) / factor)
            self.zone_surface = pygame.transform.scale(self.zone_surface, (int(zone_width), int(zone_height)))

        # They're color-coded as well to make it easier to identify their type.
        if isinstance(zone, PriorityZone):
            self.zone_surface.fill(COLORS["green"], special_flags=pygame.BLEND_MULT)
        elif isinstance(zone, RestrictedZone):
            self.zone_surface.fill(COLORS["yellow"], special_flags=pygame.BLEND_MULT)
        elif isinstance(zone, BlockedZone):
            self.zone_surface.fill(COLORS["red"], special_flags=pygame.BLEND_MULT)

    def get_coords(self) -> tuple[float, float]:
        """
        Returns VisualNode graphical space coordinates

        Args:
            None

        Returns:
            tuple[float, float]: Visual node coords
        """

        return self.coords

    def draw(self) -> None:
        """
        Displays the visual representation of the VisualNode

        Args:
            None

        Returns:
            None
        """

        if self.color_name != "rainbow":
            self.surface.blit(self.border_surface, self.border_surface.get_rect(center = self.coords))
            self.surface.blit(self.base_surface, self.base_surface.get_rect(center = self.coords))
            self.surface.blit(self.highlight_surface, self.highlight_surface.get_rect(center = self.coords))
            self.surface.blit(self.shadow_surface, self.shadow_surface.get_rect(center = self.coords))
        else:
            self.surface.blit(self.rainbow_surface, self.rainbow_surface.get_rect(center = self.coords))

        if self.zone_surface:
            self.surface.blit(self.zone_surface, self.zone_surface.get_rect(center = self.coords))


class VisualConnection():
    def __init__(self, node_1: VisualNode, node_2: VisualNode,
                 surface: pygame.Surface) -> None:
        """
        Visual representation of the Connection.
        Responsible for initializing

        Args:
            node1 (VisualNode): Used for their graphical space coordinates
            node2 (VisualNode): Used for their graphical space coordinates
            surface (pygame.Surface): Where the node will be drawn

        Returns:
            None
        """

        self.coords_1 = node_1.get_coords()
        self.coords_2 = node_2.get_coords()
        self.surface = surface
        self.color = pygame.Color(21, 234, 229)

    def draw(self):
        """
        Displays the visual representation of the VisualConnection

        Args:
            None

        Returns:
            None
        """

        pygame.draw.line(self.surface, self.color,
                         self.coords_1, self.coords_2, 6)


class VisualDrone():
    def __init__(self, id: int, coords: tuple[float, float],
                 scale: float, surface: pygame.Surface) -> None:
        self.id = str(id)
        self.can_move = False
        self.coords = coords
        self.scale = scale
        factor = 3
        self.surface = surface
        self.drone_surface = pygame.image.load("assets/Drone.png").convert_alpha()

        image_width = self.drone_surface.get_width() * ((self.scale / 100) / factor)
        image_height = self.drone_surface.get_height() * ((self.scale / 100) / factor)
        
        self.drone_surface = pygame.transform.scale(self.drone_surface, (int(image_width), int(image_height)))

        standard_font_size = 28
        self.font_size = standard_font_size

        if self.scale / 2 < standard_font_size:
            self.font_size = int(self.scale / 2)

    def get_coords(self) -> tuple[Any]:
        return self.coords

    def set_turn_target(self, target_coords: tuple[float, float], duration: float):
        self.can_move = True
        self.x = target_coords[0] / duration
        self.y = target_coords[1] / duration

    def move(self, delta: int):
        if not self.can_move:
            return
        self.coords = (self.coords[0] + (self.x * delta), self.coords[1] + (self.y * delta))

    def draw(self):
        self.surface.blit(self.drone_surface, self.drone_surface.get_rect(center = self.coords))

        font = pygame.font.SysFont(None, self.font_size)
        text_surface = font.render(self.id, True, (0, 0, 0))
        self.surface.blit(text_surface, text_surface.get_rect(center = (self.coords)))

    def reset_can_move(self) -> None:
        self.can_move = False


class Renderer():
    def __init__(self, manager: Manager):
        self.manager = manager
        pygame.init()

        self.set_window_size()
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.image.load("assets/Background.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        self.create_visual_nodes()
        self.create_visual_connections()
        self.create_visual_drones()

        self.turn_duration = 1000
        self.turn_cooldown = 100
        self.after_time = 2000

        self.fps = 60

        self.zone_legend = pygame.image.load("assets/Zone.png").convert_alpha()

    def set_window_size(self) -> None:
        self.scale = 100

        self.min_width = 800
        self.max_width = 1600
        self.min_height = 800
        selfmax_height = 1000

        self.width = self.min_width
        self.height = self.min_height

        self.draw_width_margin = 400
        self.draw_height_margin = 400
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

        if dimensions_x > self.min_width:
            self.width = dimensions_x
            self.draw_width = self.width - self.draw_width_margin
        if dimensions_y > self.min_height:
            self.height = dimensions_y
            self.draw_height = self.height - self.draw_height_margin

        scale_x = self.scale
        scale_y = self.scale

        if self.width > self.max_width:
            self.width = self.max_width
            self.draw_width = self.max_width - self.draw_width_margin
            scale_x = (self.max_width /
                       (abs(self.coords_x[0]) + abs(self.coords_x[1])))
        if self.height > selfmax_height:
            self.height = selfmax_height
            self.draw_height = selfmax_height - self.draw_height_margin
            scale_y = (selfmax_height /
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

            self.visual_nodes[node.name] = (
                VisualNode((x, y), node.color, self.scale, self.surface,
                           node.zone))

    def create_visual_connections(self) -> None:
        self.visual_connections = []

        for connection in self.manager.graph.connections.values():
            node_1 = self.visual_nodes[connection.node_1]
            node_2 = self.visual_nodes[connection.node_2]
            self.visual_connections.append(
                VisualConnection(node_1, node_2, self.surface))

    def create_visual_drones(self) -> None:
        self.visual_drones = {}

        for index in range(self.manager.graph.drone_count):
            coords = self.visual_nodes[self.manager.graph.start_hub.name].get_coords()
            self.visual_drones[f"D{index + 1}"] = VisualDrone(index + 1, coords, self.scale, self.surface)

    def draw_nodes(self) -> None:
        for node in self.visual_nodes.values():
            node.draw()

    def draw_connections(self) -> None:
        for connection in self.visual_connections:
            connection.draw()

    def draw_drones(self) -> None:
        for drone in self.visual_drones.values():
            drone.draw()

    def draw_turn(self, current_turn: int) -> None:
        font_size = 42
        text = f"{current_turn}/{self.manager.complete_simulation}"

        pygame.draw.rect(self.surface, pygame.Color(13, 19, 95), pygame.Rect(20, 20, 100, 60), border_radius=25)

        font = pygame.font.SysFont(None, font_size)
        text_surface = font.render(text, True, COLORS["white"])
        self.surface.blit(text_surface, text_surface.get_rect(center = (70, 50)))

    def draw_legend(self) -> None:
        font_size = 26
        factor = 8
        legend_margin = 20
        scale = 50
        background_width = self.min_width / 2

        text_priority = "Priority"
        text_restricted = "Restricted"
        text_blocked = "Blocked"

        font = pygame.font.SysFont(None, font_size)

        width = self.zone_legend.get_width() * (scale / 100) / factor
        height = self.zone_legend.get_height() * (scale / 100) / factor

        zone_priority = pygame.transform.scale(self.zone_legend, (int(width), int(height)))
        zone_priority.fill(COLORS["green"], special_flags=pygame.BLEND_MULT)
        font_priority = font.render(text_priority, True, COLORS["white"])

        zone_restricted = pygame.transform.scale(self.zone_legend, (int(width), int(height)))
        zone_restricted.fill(COLORS["yellow"], special_flags=pygame.BLEND_MULT)
        font_restricted = font.render(text_restricted, True, COLORS["white"])

        zone_blocked = pygame.transform.scale(self.zone_legend, (int(width), int(height)))
        zone_blocked.fill(COLORS["red"], special_flags=pygame.BLEND_MULT)
        font_blocked = font.render(text_blocked, True, COLORS["white"])

        background_rect = pygame.Rect(20, self.height - (self.draw_height_margin / 4), background_width, self.draw_height_margin / 3)

        text_priority_coords = (background_rect.x + legend_margin, background_rect.centery - font_priority.get_rect().height)
        zone_priority_coords = (text_priority_coords[0] + font_priority.get_rect().width + legend_margin, background_rect.centery - zone_priority.get_rect().centery)

        text_restricted_coords = (background_rect.width / 3 + legend_margin, background_rect.centery - font_restricted.get_rect().height)
        zone_restricted_coords = (text_restricted_coords[0] + font_restricted.get_rect().width + legend_margin, background_rect.centery - zone_restricted.get_rect().centery)

        text_blocked_coords = (2 * (background_rect.width / 3) + legend_margin, background_rect.centery - font_blocked.get_rect().height)
        zone_blocked_coords = (text_blocked_coords[0] + font_blocked.get_rect().width + legend_margin, background_rect.centery - zone_blocked.get_rect().centery)


        pygame.draw.rect(self.surface, pygame.Color(13, 19, 95), background_rect, border_radius=20)

        self.surface.blit(font_priority, font_priority.get_rect(topleft = text_priority_coords))
        self.surface.blit(zone_priority, zone_priority.get_rect(center = zone_priority_coords))

        self.surface.blit(font_restricted, font_restricted.get_rect(topleft = text_restricted_coords))
        self.surface.blit(zone_restricted, zone_restricted.get_rect(center = zone_restricted_coords))

        self.surface.blit(font_blocked, font_blocked.get_rect(topleft = text_blocked_coords))
        self.surface.blit(zone_blocked, zone_blocked.get_rect(center = zone_blocked_coords))

    def set_turn_event(self, events: list[Any]):
        for event in events:
            target_coords = ()
            drone_coords = self.visual_drones[event[0]].get_coords()
            node_coords = self.visual_nodes[event[1]].get_coords()
            if len(event) == 2:
                target_coords = (
                    node_coords[0] - drone_coords[0],
                    node_coords[1] - drone_coords[1],
                )
            else:
                node_2_coords = self.visual_nodes[event[2]].get_coords()
                middle_point = (
                    (node_2_coords[0] + node_coords[0]) / 2,
                    (node_2_coords[1] + node_coords[1]) / 2,
                )
                target_coords = (
                    middle_point[0] - drone_coords[0],
                    middle_point[1] - drone_coords[1],
                )
            self.visual_drones[event[0]].set_turn_target(target_coords, self.turn_duration)

    def run(self) -> None:
        clock = pygame.time.Clock()
        current_turn = 0
        for turn in self.manager.turns:
            self.set_turn_event(turn)

            current_turn += 1
            current_time = 0

            while current_time < self.turn_duration:
                self.surface.blit(self.background, (0, 0))
                self.draw_connections()
                self.draw_nodes()
                self.draw_drones()

                self.draw_turn(current_turn)
                self.draw_legend()

                pygame.display.flip()
                self.check_pygame_event()

                delta = clock.tick(self.fps)

                for drone in self.visual_drones.values():
                    drone.move(delta)
                current_time += delta

            current_time = 0

            while current_time < self.turn_cooldown:
                self.check_pygame_event()
                current_time += delta
            
            for drone in self.visual_drones.values():
                drone.reset_can_move()

        current_time = 0
        while current_time < self.after_time:
            delta = clock.tick(self.fps)
            current_time += delta
            self.check_pygame_event()

        pygame.quit()

    def check_pygame_event(self):
        for pygame_event in pygame.event.get():
                if pygame_event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
