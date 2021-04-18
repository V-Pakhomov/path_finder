import pygame
import time


class Field:

    walls = []
    start = None
    end = None
    screen = None
    clock = None
    running = True
    fps = 60
    square_size = 0

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__init_pygame_field()
        self.main_loop()

    def __init_pygame_field(self):
        pygame.init()
        user_screen_info = pygame.display.Info()
        self.clock = pygame.time.Clock()
        self.square_size = int(min(user_screen_info.current_w * 0.8 // self.width,
                                   user_screen_info.current_h * 0.8 // self.height))
        pygame.display.set_caption('Path finder')
        self.screen = pygame.display.set_mode((self.square_size * self.width, self.square_size * self.height))
        self.screen.fill('white')
        for i in range(0, self.height * self.square_size, self.square_size):
            for j in range(0, self.width * self.square_size, self.square_size):
                rect = pygame.Rect(j + 1, i + 1, self.square_size - 1, self.square_size - 1)
                pygame.draw.rect(self.screen, 'grey', rect)

    def sq_coord(self, x, y):
        x //= self.square_size
        y //= self.square_size
        x *= self.square_size
        y *= self.square_size
        return int(x), int(y)

    def configure(self):
        pass

    def solve(self):
        pass

    def main_loop(self):
        while self.running:
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()

        pygame.quit()
        exit()


def change_square_color(screen, event, square_size):
    try:
        buttons = event.buttons
    except AttributeError:
        if event.button > 3:
            return
        buttons = [0, 0, 0]
        buttons[event.button - 1] = 1
    if sum(buttons) != 1:
        return
    left, mid, right = buttons
    if left:
        color = 'red'
    elif right:
        color = 'blue'
    else:
        color = 'black'
    i, j = event.pos
    i //= square_size
    j //= square_size
    rect = pygame.Rect(i*square_size + 1, j*square_size + 1, square_size - 1, square_size - 1)
    pygame.draw.rect(screen, color, rect)


def init_field(squares_count=20, width=500, height=500, fps=60):
    square_size = 500 / squares_count
    pygame.init()
    pygame.display.set_caption("path finder")
    print(pygame.display.Info())
    screen = pygame.display.set_mode((width, height))
    screen.fill('white')
    for i in range(50):
        for j in range(50):
            rect = pygame.Rect(i*square_size + 1, j*square_size + 1, square_size - 1, square_size - 1)
            pygame.draw.rect(screen, 'grey', rect)
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                change_square_color(screen, event, square_size)

        pygame.display.flip()


def solve():
    pass


def main():
    field = Field(48, 27)
    time.sleep(100)
    init_field()
    solve()
    pygame.quit()


if __name__ == '__main__':
    main()