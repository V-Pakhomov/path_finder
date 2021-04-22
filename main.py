import pygame
import time
from loguru import logger
from square import Square, default_colors
from bfs import bfs


def caller(func):
    def wrapper(*args, **kwargs):
        # logger.debug(f'{func.__name__} is called')
        result = func(*args, **kwargs)
        return result

    return wrapper


class Field:

    nodes = {}
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
        pygame.K_w: 'wall',
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
        self.__reset_screen()

    def __init_pygame_field(self):
        pygame.init()
        user_screen_info = pygame.display.Info()
        self.clock = pygame.time.Clock()
        self.square_size = int(min(user_screen_info.current_w * 0.8 // self.width,
                                   user_screen_info.current_h * 0.8 // self.height))
        pygame.display.set_caption(self.captions[0])
        self.screen = pygame.display.set_mode((self.square_size * self.width, self.square_size * self.height))
        for y in range(self.height):
            for x in range(self.width):
                self.nodes[x, y] = Square(x, y, self.square_size, self.screen)

    def __reset_screen(self):
        self.start = None
        self.end = None
        self.walls = []
        self.screen.fill(default_colors['field'])
        for square in self.nodes.values():
            square.reset()

    def __square_coordinate(self, x, y):
        return int(x // self.square_size), int(y // self.square_size)

    def configure(self):
        self.fps = 200
        while self.running:
            self.clock.tick(self.fps)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return
                    if event.key == pygame.K_ESCAPE:
                        self.__reset_screen()
                    elif event.key == pygame.K_RIGHT:
                        self.algo_num += 1
                    elif event.key == pygame.K_LEFT:
                        self.algo_num -= 1
                    elif event.key in self.modes:
                        self.curr_mode = self.modes[event.key]
                    pygame.display.set_caption(self.captions[self.algo_num % len(self.captions)])
                    # logger.debug(f'current mode: {self.curr_mode}')
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = self.__square_coordinate(*event.pos)
                    # logger.debug(event.button)
                    if event.button == pygame.BUTTON_RIGHT:
                        self.__clear_square(x, y)
                    elif event.button == pygame.BUTTON_LEFT:
                        self.__set_square(x, y)
                elif event.type == pygame.MOUSEMOTION:
                    try:
                        l, _, r = event.buttons
                    except:
                        continue
                    if l + r != 1:
                        continue
                    if l:
                        self.__set_square(*self.__square_coordinate(*event.pos))
                    elif r:
                        self.__clear_square(*self.__square_coordinate(*event.pos))

            pygame.display.flip()

    # @caller
    def __set_square(self, x, y):
        # logger.debug(f'{x}, {y}')
        square = self.nodes[x, y]
        if square in self.walls:
            return
        if self.curr_mode == 'start':
            if square == self.end:
                return
            if self.start:
                self.start.color = default_colors[self.start.weight]
            self.start = square
        elif self.curr_mode == 'end':
            if square == self.start:
                return
            if self.end:
                self.end.color = default_colors[self.end.weight]
            self.end = square
        elif self.curr_mode == 'wall':
            if square in (self.start, self.end):
                return
            self.walls.append(square)
        else:
            if square in (self.start, self.end):
                return
            square.weight = self.curr_mode
        square.color = default_colors[self.curr_mode]

    # @caller
    def __clear_square(self, x, y):
        square = self.nodes[x, y]
        if self.start == square:
            self.start = None
        elif self.end == square:
            self.end = None
        if square in self.walls:
            self.walls.remove(square)
        square.reset()

    def __print_path(self):
        square = self.end.parent
        while square and square != self.start:
            square.draw(default_colors['path'])
            square = square.parent

    def run_algorithm(self):
        if not self.start or not self.end:
            logger.warning('There must be a start and an end on the field ')
            return

        logger.debug(list(self.nodes.keys()))

        self.fps = 15
        caption = self.captions[self.algo_num % len(self.captions)]
        pause = False
        algorithm_duration = 0
        start = time.time()

        current_squares = [self.start]
        used_squares = []
        algorithm = {'BFS': bfs}[caption]
        done = False

        while self.running:
            self.clock.tick(self.fps)

            if not done:
                if pause:
                    pygame.display.set_caption(f'{caption} ({round(algorithm_duration, 3)})')
                else:
                    pygame.display.set_caption(f'{caption} ({round(algorithm_duration + time.time() - start, 3)})')

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and done:
                        return
                    if event.key == pygame.K_SPACE and not done:
                        pause = not pause
                        if pause:
                            algorithm_duration += time.time() - start
                        else:
                            start = time.time()

            if pause or done:
                continue

            current_squares = algorithm(self, current_squares, used_squares)
            for square in current_squares:
                if square != self.end:
                    square.light()
            if self.end in used_squares or not current_squares:
                self.__print_path()
                done = True

            pygame.display.flip()

    def restore_configure(self):
        for square in self.nodes.values():
            square.parent = None
            square.draw()


if __name__ == '__main__':
    field = Field(50, 30)
    for _ in range(10):
        field.configure()
        field.run_algorithm()
        field.restore_configure()
