import pygame
import time
from loguru import logger


def caller(func):
    def wrapper(*args, **kwargs):
        logger.debug(f'{func.__name__} is called')
        result = func(*args, **kwargs)
        return result

    return wrapper


class Field:

    walls = []
    start = None
    end = None
    screen = None
    clock = None
    running = True
    fps = 60
    square_size = 0
    captions = ('BFS', 'Dijkstra', 'Greedy', 'A*')
    algo_num = 0
    modes = {
        pygame.K_0: 'wall',
        pygame.K_s: 'start',
        pygame.K_e: 'end'
    }
    for k in range(2, 10):
        modes[pygame.K_0 + k] = k
    curr_mode = 'start'

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__init_pygame_field()

    def __init_pygame_field(self):
        pygame.init()
        user_screen_info = pygame.display.Info()
        self.clock = pygame.time.Clock()
        self.square_size = int(min(user_screen_info.current_w * 0.2 // self.width,
                                   user_screen_info.current_h * 0.2 // self.height))
        pygame.display.set_caption(self.captions[0])
        self.screen = pygame.display.set_mode((self.square_size * self.width, self.square_size * self.height))
        self.screen.fill('white')
        for i in range(0, self.height * self.square_size, self.square_size):
            for j in range(0, self.width * self.square_size, self.square_size):
                rect = pygame.Rect(j + 1, i + 1, self.square_size - 1, self.square_size - 1)
                pygame.draw.rect(self.screen, 'grey', rect)

    def __square_coordinate(self, x, y):
        return int(x // self.square_size), int(y // self.square_size)

    def __left_top_corner_square_coordinate(self, x, y):
        return x * self.square_size, y * self.square_size

    @caller
    def __change_square_color(self, x, y, color):
        x, y = self.__left_top_corner_square_coordinate(x, y)
        logger.debug(f'{x}, {y}')
        rect = pygame.Rect(x + 1, y + 1, self.square_size - 1, self.square_size - 1)
        pygame.draw.rect(self.screen, color, rect)

    def configure(self):
        pass

    def solve(self):
        pass

    def main_loop(self):
        while self.running:
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.algo_num += 1
                    elif event.key == pygame.K_LEFT:
                        self.algo_num -= 1
                    elif event.key in self.modes:
                        self.curr_mode = self.modes[event.key]
                    pygame.display.set_caption(self.captions[self.algo_num % len(self.captions)])
                    logger.debug(f'current mode: {self.curr_mode}')
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_RIGHT:
                        self.__clear_square(*self.__square_coordinate(*event.pos))
                    elif event.button == pygame.BUTTON_LEFT:
                        self.__set_square(*self.__square_coordinate(*event.pos))
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()

        pygame.quit()

    @caller
    def __set_square(self, x, y):
        logger.debug(f'{x}, {y}')
        if self.curr_mode == 'start':
            if (x, y) == self.end or (x, y) in self.walls:
                return
            if self.start:
                self.__clear_square(*self.start)
            self.start = (x, y)
            self.__change_square_color(x, y, 'blue')
        elif self.curr_mode == 'end':
            if (x, y) == self.start or (x, y) in self.walls:
                return
            if self.end:
                self.__clear_square(*self.end)
            self.end = (x, y)
            self.__change_square_color(x, y, 'red')

    @caller
    def __clear_square(self, x, y):
        if self.start == (x, y):
            self.start = None
        elif self.end == (x, y):
            self.end = None
        if (x, y) in self.walls:
            self.walls.remove((x, y))
        self.__change_square_color(x, y, 'grey')


if __name__ == '__main__':
    field = Field(16, 9)
    field.main_loop()
