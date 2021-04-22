import pygame
from loguru import logger


default_colors = {
    'field': '00 00 00',
    'square': '80 80 80',
    'start': '00 00 FF',
    'end': 'FF 00 00',
    'wall': '00 00 00',
    'path': 'FF FF 00',
    1: '80 80 80',
    2: 'FF DF DC',
    3: 'F5 B2 AC',
    4: 'FF C4 6B',
    5: 'FC 9A 40',
    6: 'C9 FF BF',
    7: 'BE F7 61',
    8: 'D7 FF FE',
    9: 'B7 D4 FF'
}

for k, v in default_colors.items():
    default_colors[k] = tuple(map(lambda x: int(x, 16), v.split()))


class Square:

    __color = default_colors['square']
    __weight = 1
    path_to_start = float('inf')
    dist_to_end = float('inf')
    parent = None

    def __init__(self, x, y, size, screen):
        self.x = x
        self.y = y
        self.__size = size
        self.screen = screen
        self.__font = pygame.font.SysFont(None, size)
        self.__text_obj = self.__font.render(str(self.__weight), True, default_colors['wall'])
        self.__text_rect = self.__text_obj.get_rect()
        x, y = self.__screen_coordinates
        self.__text_rect.topright = (x + size - 1, y + 1)

    def draw(self, color=None):
        color = color or self.__color
        x, y = self.__screen_coordinates
        rect = pygame.Rect(x + 1, y + 1, self.__size - 1, self.__size - 1)
        pygame.draw.rect(self.screen, color, rect)
        if self.__weight > 1:
            self.screen.blit(self.__text_obj, self.__text_rect)

    @property
    def __screen_coordinates(self):
        return self.x * self.__size, self.y * self.__size

    @property
    def size(self):
        return self.__size

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, new_weight):
        self.__weight = new_weight
        self.__text_obj = self.__font.render(str(self.__weight), True, default_colors['wall'])
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
        self.__weight = 1
        self.__color = default_colors['square']
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
