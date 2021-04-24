import pygame
from settings import colors, draw
from loguru import logger


class Square:

    __color = colors[1]
    __cost = 1
    path_to_start = float('inf')
    dist_to_end = float('inf')
    parent = None

    def __init__(self, x, y, size, screen):
        self.x = x
        self.y = y
        self.__size = size
        self.screen = screen
        self.__font = pygame.font.SysFont(None, size)
        self.__text_obj = self.__font.render(str(self.__cost), True, colors['wall'])
        self.__text_rect = self.__text_obj.get_rect()
        x, y = self.__screen_coordinates
        self.__text_rect.topright = (x + size - 1, y + 1)

    def draw(self, color=None):
        color = color or self.__color
        x, y = self.__screen_coordinates
        rect = pygame.Rect(x + 1, y + 1, self.__size - 1, self.__size - 1)
        pygame.draw.rect(self.screen, color, rect)
        if draw['cost'] and self.__cost >= draw['min_cost_to_draw']:
            self.screen.blit(self.__text_obj, self.__text_rect)

    @property
    def __screen_coordinates(self):
        return self.x * self.__size, self.y * self.__size

    @property
    def size(self):
        return self.__size

    @property
    def cost(self):
        return self.__cost

    @cost.setter
    def cost(self, new_cost):
        self.__cost = new_cost
        self.__text_obj = self.__font.render(str(self.__cost), True, colors['wall'])
        self.__text_rect = self.__text_obj.get_rect()
        x, y = self.__screen_coordinates
        self.__text_rect.topright = (x + self.size - 1, y + 1)
        self.draw()

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, new_color):
        self.__change_color(new_color)

    def __change_color(self, color):
        self.__color = color
        self.draw()

    def reset(self):
        self.__cost = 1
        self.__color = colors[1]
        self.draw()

    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5

    def neighbours(self, field):
        neighbours = []
        for diff in (-1, 1):
            if 0 <= self.x + diff < field.width and field.nodes[(self.x + diff, self.y)] not in field.walls:
                neighbours.append((self.x + diff, self.y))
            if 0 <= self.y + diff < field.height and field.nodes[(self.x, self.y + diff)] not in field.walls:
                neighbours.append((self.x, self.y + diff))
        return neighbours

    def light(self):
        r, g, b = self.__color
        r = (255 + r) // 2
        g = (255 + g) // 2
        b = (255 + b) // 2
        self.draw((r, g, b))

    def dark(self):
        r, g, b = self.__color
        r //= 2
        g //= 2
        b //= 2
        self.draw((r, g, b))

    def __str__(self):
        return f'x={self.x}, y={self.y}, to_start={self.path_to_start}, to_end={self.dist_to_end}'

    def __repr__(self):
        return f'({self.__str__()})'
