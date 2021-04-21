import pygame


default_colors = {
    'field': 'white',
    'square': 'grey',
    'start': 'blue',
    'end': 'red',
    'wall': 'black'
}


class Square:

    __color = default_colors['square']

    def __init__(self, x, y, size, screen, weight=1):
        self.x = x
        self.y = y
        self.__size = size
        self.screen = screen
        self.__weight = weight
        self.__font = pygame.font.SysFont(None, size//2)
        self.__text_obj = self.__font.render(str(self.__weight), True, default_colors['wall'])
        self.__text_rect = self.__text_obj.get_rect()
        self.__text_rect.topleft = (x * size + 1, y * size + 1)

    def draw(self):
        x, y = self.__screen_coordinates
        rect = pygame.Rect(x + 1, y + 1, self.__size - 1, self.__size - 1)
        pygame.draw.rect(self.screen, self.__color, rect)
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
