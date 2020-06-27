import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

WIDTH = 20
HEIGHT = 20
MARGIN = 1
ROWS = 25
COLUMNS = 25
WINDOW_SIZE = [(HEIGHT + MARGIN) * COLUMNS, (WIDTH + MARGIN) * ROWS]
FRAME_RATE = 10

print("Window Size: " + ", ".join(list(map(str, WINDOW_SIZE))))
print("Grid: " + ", ".join(list(map(str, [COLUMNS, ROWS]))))

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Game of Life")


class Board(object):
    def __init__(self, rows=16, columns=16):
        self.columns = columns
        self.rows = rows
        self.grid = [[0] * self.columns for _ in range(self.rows)]
        self.pause = True

    def update(self):
        temp = [[0] * self.columns for _ in range(self.rows)]

        for y in range(self.rows):
            for x in range(self.columns):
                total = sum([self.grid[j][i] for (i, j) in self.neighbours(x, y)])

                if self.grid[y][x] == 1:
                    if total < 2:
                        temp[y][x] = 0
                    elif 2 <= total <= 3:
                        temp[y][x] = 1
                    elif total >= 3:
                        temp[y][x] = 0
                elif self.grid[y][x] == 0 and total == 3:
                    temp[y][x] = 1

        self.grid = temp

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

    def draw(self):
        if not self.pause:
            self.update()

        for r in range(self.rows):
            for c in range(self.columns):
                color = WHITE
                if self.grid[r][c] == 1:
                    color = GREEN

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


game = Board(ROWS, COLUMNS)

done = False
hide_ui = False
i = 0
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)

            try:
                game.grid[row][column] = not game.grid[row][column]
            except IndexError:
                pass

            print("Click ", pos, "Grid coordinates: ", row, column)

        elif event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            if key_name == "space":
                game.pause = not game.pause
            elif key_name == "h":
                hide_ui = not hide_ui

    screen.fill(BLACK)
    game.draw()
    if not hide_ui:
        font = pygame.font.SysFont(None, 25)
        text = font.render(f"Iterations: {i}", True, BLACK)
        screen.blit(text, (1, 1))

    # Limit to 10 frames per second
    clock.tick(FRAME_RATE)

    pygame.display.flip()
    if not game.pause:
        i += 1

pygame.quit()
