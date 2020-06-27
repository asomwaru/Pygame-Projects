import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

WIDTH = 10
HEIGHT = 10
MARGIN = 1
COLUMNS = 100
ROWS = 75
WINDOW_SIZE = [(HEIGHT + MARGIN) * COLUMNS, (WIDTH + MARGIN) * ROWS]
FRAME_RATE = 10

print("Window Size: " + ", ".join(list(map(str, WINDOW_SIZE))))
print("Grid: " + ", ".join(list(map(str, [COLUMNS, ROWS]))))

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Brian's Brain")


class Board(object):
    def __init__(self, rows=16, columns=16):
        self.columns = columns
        self.rows = rows
        self.grid = [[3] * self.columns for _ in range(self.rows)]
        self.pause = True
        self.hide_ui = False
        self.iterations = 0

        self.colors = {
            "BLACK": (0, 0, 0),
            "BLUE": (0, 0, 255),
            "WHITE": (255, 255, 255),
            "GREY": (127, 127, 127),
            "CYAN": (0, 255, 255),
            "DARK_BLUE": (3, 63, 138)
        }

    def reset(self):
        self.grid = [[0] * self.columns for _ in range(self.rows)]
        self.pause = True
        self.iterations = 0

    def update(self):
        temp = [[1] * self.columns for _ in range(self.rows)]

        for y in range(self.rows):
            for x in range(self.columns):
                if self.grid[y][x] == 1:
                    temp[y][x] = 2
                elif self.grid[y][x] == 2:
                    temp[y][x] = 3
                elif self.grid[y][x] == 3:
                    total = sum([self.grid[j][i] in [1,2] for (i, j) in self.neighbours(x, y)])

                    if total == 2:
                        temp[y][x] = 1
                    else:
                        temp[y][x] = 3

        self.grid = temp
        self.iterations += 1

    def draw(self):
        if not self.pause:
            self.update()

        for r in range(self.rows):
            for c in range(self.columns):
                color = None
                if self.grid[r][c] == 1:
                    color = self.colors["BLUE"]
                elif self.grid[r][c] == 2:
                    color = self.colors['DARK_BLUE']
                elif self.grid[r][c] == 3:
                    color = self.colors['GREY']

                pygame.draw.rect(
                    screen,
                    color,
                    [
                        (MARGIN + WIDTH) * c + MARGIN,
                        (MARGIN + HEIGHT) * r + MARGIN,
                        WIDTH,
                        HEIGHT,
                    ],
                )

        if not self.hide_ui:
            font = pygame.font.SysFont(None, 25)
            text = font.render(f"Iterations: {self.iterations}", True, (0, 0, 0))
            screen.blit(text, (1, 1))

    def neighbours(self, x: int, y: int):
        for yp in range(-1, 2):
            for xp in range(-1, 2):
                if xp == 0 and yp == 0:
                    continue

                if xp + x >= self.columns or xp + x < 0:
                    continue

                if yp + y >= self.rows or yp + y < 0:
                    continue

                yield xp + x, yp + y


game = Board(ROWS, COLUMNS)

done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)

            game.grid[row][column] = 1

            print("Click ", pos, "Grid coordinates: ", row, column)

        elif event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            if key_name == "space":
                game.pause = not game.pause
            elif key_name == "h":
                game.hide_ui = not game.hide_ui
            elif key_name == 'r':
                game.reset()

    screen.fill((0,0,0))
    game.draw()

    # Limit to 10 frames per second
    clock.tick(FRAME_RATE)

    pygame.display.flip()

pygame.quit()
