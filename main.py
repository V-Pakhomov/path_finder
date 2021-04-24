import pygame
import time
from loguru import logger
from square import Square
from settings import colors, field as f
from algorithms import bfs, dijkstra, greedy, A_star


class Field:

    def __init__(self):
        self.width = f['width']
        self.height = f['height']
        self.__init__attributes__()
        self.__init_pygame_field()
        self.__reset_screen()

    def __init__attributes__(self):
        self.nodes = {}
        self.walls = []
        self.start = None
        self.end = None
        self.screen = None
        self.clock = None
        self.running = True
        self.fps = f['fps']
        self.square_size = 0
        self.captions = ('BFS', 'Greedy', 'Dijkstra', 'A*')
        self.algo_num = 0
        self.modes = {
            pygame.K_w: 'wall',
            pygame.K_s: 'start',
            pygame.K_e: 'end'
        }
        for k in range(2, 10):
            self.modes[pygame.K_0 + k] = k
        self.curr_mode = 'start'

    def __init_pygame_field(self):
        pygame.init()
        user_screen_info = pygame.display.Info()
        self.clock = pygame.time.Clock()
        self.square_size = int(min(user_screen_info.current_w * 0.9 // self.width,
                                   user_screen_info.current_h * 0.9 // self.height))
        pygame.display.set_caption(self.captions[0])
        self.screen = pygame.display.set_mode((self.square_size * self.width, self.square_size * self.height))
        for y in range(self.height):
            for x in range(self.width):
                self.nodes[x, y] = Square(x, y, self.square_size, self.screen)

    def __reset_screen(self):
        self.start = None
        self.end = None
        self.walls = []
        self.screen.fill(colors['wall'])
        for square in self.nodes.values():
            square.reset()

    def __square_coordinate(self, x, y):
        return int(x // self.square_size), int(y // self.square_size)

    def configure(self):
        while self.running:
            self.clock.tick(self.fps)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    if event.key == pygame.K_RETURN:
                        return
                    if event.key == pygame.K_BACKSPACE:
                        self.__reset_screen()
                    elif event.key == pygame.K_RIGHT:
                        self.algo_num += 1
                    elif event.key == pygame.K_LEFT:
                        self.algo_num -= 1
                    elif event.key in self.modes:
                        self.curr_mode = self.modes[event.key]
                    pygame.display.set_caption(self.captions[self.algo_num % len(self.captions)])
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = self.__square_coordinate(*event.pos)
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

    def __set_square(self, x, y):
        square = self.nodes[x, y]
        if square in self.walls:
            return
        if self.curr_mode == 'start':
            if square == self.end:
                return
            if self.start:
                self.start.color = colors[self.start.cost]
            self.start = square
        elif self.curr_mode == 'end':
            if square == self.start:
                return
            if self.end:
                self.end.color = colors[self.end.cost]
            self.end = square
        elif self.curr_mode == 'wall':
            if square in (self.start, self.end):
                return
            self.walls.append(square)
        else:
            if square in (self.start, self.end):
                return
            square.cost = self.curr_mode
        square.color = colors[self.curr_mode]

    def __clear_square(self, x, y):
        square = self.nodes[x, y]
        if self.start == square:
            self.start = None
        elif self.end == square:
            self.end = None
        if square in self.walls:
            self.walls.remove(square)
        square.reset()

    def __path(self):
        path = []
        square = self.end.parent
        while square and square != self.start:
            path.append(square)
            square = square.parent
        return path

    def run_algorithm(self):
        if not self.start or not self.end:
            logger.warning('There must be a start and an end on the field ')
            return

        caption = self.captions[self.algo_num % len(self.captions)]
        pause = False
        algorithm_duration = 0
        start = time.time()

        current_squares = [self.start]
        used_squares = []
        algorithm = {'BFS': bfs, 'Greedy': greedy, 'Dijkstra': dijkstra, 'A*': A_star}[caption]
        done = False
        for square in self.nodes.values():
            square.dist_to_end = square.distance(self.end)
        self.start.path_to_start = 0

        while self.running:
            self.clock.tick(self.fps)

            if not done:
                if pause:
                    pygame.display.set_caption(f'{caption} ({round(algorithm_duration, 3)}s)')
                else:
                    pygame.display.set_caption(f'{caption} ({round(algorithm_duration + time.time() - start, 3)}s)')

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    if event.key == pygame.K_RETURN:
                        return
                    if event.key == pygame.K_SPACE and not done:
                        pause = not pause
                        if pause:
                            algorithm_duration += time.time() - start
                        else:
                            start = time.time()

            if pause or done:
                self.clock.tick(f['path_drawing_fps'])
                if done and path:
                    path.pop().draw(colors['path'])
                    pygame.display.flip()
                continue

            algorithm(self, current_squares, used_squares)
            if self.end in used_squares or not current_squares:
                caption = pygame.display.get_caption()[0]
                if self.end in used_squares:
                    pygame.display.set_caption(f'{caption} path cost = {self.end.path_to_start}')
                else:
                    pygame.display.set_caption(f'{caption} path not found')
                path = self.__path()
                done = True

            pygame.display.flip()

    def restore_configure(self):
        for square in self.nodes.values():
            square.parent = None
            square.path_to_start = float('inf')
            square.dist_to_end = float('inf')
            square.draw()


if __name__ == '__main__':
    field = Field()
    while True:
        field.configure()
        field.run_algorithm()
        field.restore_configure()
