import pygame
import random

# up, right, down, left
DIRECTIONS = [
    [0, 1],
    [1, 0],
    [0, -1],
    [-1, 0]
]

WIDTH = 10
HEIGHT = 10
MARGIN = 1
ROWS = 75
COLUMNS = 75
WINDOW_SIZE = [(HEIGHT + MARGIN) * COLUMNS, (WIDTH + MARGIN) * ROWS]
FRAME_RATE = 60

print("Window Size: " + ", ".join(list(map(str, WINDOW_SIZE))))
print("Grid: " + ", ".join(list(map(str, [COLUMNS, ROWS]))))

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Langton's Ants")


class Board(object):
    def __init__(self, rows=16, columns=16):
        self.columns = columns
        self.rows = rows
        self.grid = [[1] * self.columns for _ in range(self.rows)]
        self.iterations = 0
        self.pause = True
        self.hide_ui = False

        self.ants = []

        self.colors = {
            "BLACK": (0, 0, 0),
            "WHITE": (255, 255, 255),
            "GREY": (127, 127, 127),
            "RED": (255, 0, 0),
        }

    def reset(self):
        self.grid = [[1] * self.columns for _ in range(self.rows)]
        self.pause = True
        self.iterations = 0
        self.ants = []

    def update(self):
        for i in range(len(self.ants)):
            current = self.ants[i]
            c_pos = current[0]
            facing = current[1]

            # this allows looping
            # try:
            #     c = c_pos[0] // (WIDTH + MARGIN)
            #     r = c_pos[1] // (HEIGHT + MARGIN)
            #     if [c_pos[0] % c, c_pos[1] % r] != c_pos:
            #         c_pos = [c_pos[0] % self.rows, c_pos[1] % self.columns]
            #
            #     if self.grid[c_pos[1]][c_pos[0]] in [1,2]:
            #         pass
            # except ZeroDivisionError:
            #     pass
            # except IndexError:
            #     print(c_pos)
            #     exit()

            if self.grid[c_pos[1]][c_pos[0]] in [1, 2]:
                new_facing = DIRECTIONS[(DIRECTIONS.index(facing)+1) % 4]
            elif self.grid[c_pos[1]][c_pos[0]] in [0, -2]:
                new_facing = DIRECTIONS[(DIRECTIONS.index(facing)-1) % 4]

            new_pos = [c_pos[0] + new_facing[0], c_pos[1] + new_facing[1]]

            # Kill switch for ants

            if new_pos[1] < 0 or new_pos[1] >= self.rows:
                self.ants[i] = None
                continue

            if new_pos[0] < 0 or new_pos[0] >= self.columns:
                self.ants[i] = None
                continue

            self.ants[i][0] = new_pos
            self.ants[i][1] = new_facing

            if self.grid[c_pos[1]][c_pos[0]] in [1, 2]:
                self.grid[c_pos[1]][c_pos[0]] = -2
            elif self.grid[c_pos[1]][c_pos[0]] in [0, -2]:
                self.grid[c_pos[1]][c_pos[0]] = 2

        self.ants = list(filter(lambda x: x, self.ants))
        self.iterations += 1

    def draw(self):
        if not self.pause:
            self.update()

        for r in range(self.rows):
            for c in range(self.columns):
                color = self.colors['WHITE']
                if self.grid[r][c] == 1:
                    color = self.colors['WHITE']
                elif self.grid[r][c] == 0:
                    color = self.colors['BLACK']
                elif self.grid[r][c] == 2:
                    color = self.colors['WHITE']
                elif self.grid[r][c] == -2:
                    color = self.colors['BLACK']

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

        for i in range(len(self.ants)):
            current_pos = self.ants[i][0]
            pygame.draw.circle(
                screen,
                self.colors['RED'],
                [
                    ((MARGIN + WIDTH) * current_pos[0] + MARGIN) + (WIDTH // 2),
                    ((MARGIN + HEIGHT) * current_pos[1] + MARGIN) + (HEIGHT // 2)
                ],
                4
            )

        if not self.hide_ui:
            font = pygame.font.SysFont(None, 25)
            text = font.render(f"Iterations: {self.iterations}", True, (0, 0, 0))
            screen.blit(text, (1, 1))


game = Board(ROWS, COLUMNS)

done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            m_pos = pygame.mouse.get_pos()

            column = m_pos[0] // (WIDTH + MARGIN)
            row = m_pos[1] // (HEIGHT + MARGIN)

            if game.grid[row][column] != 2:
                game.grid[row][column] = 2
                game.ants.append([(column, row), random.choice(DIRECTIONS)])

            print("Click ", m_pos, "Grid coordinates: ", row, column)

        elif event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            if key_name == "space":
                game.pause = not game.pause
            if key_name == "h":
                game.hide_ui = not game.hide_ui
            if key_name == 'r':
                game.reset()

    screen.fill((127, 127, 127))
    game.draw()

    # Cap the frames
    clock.tick(FRAME_RATE)

    pygame.display.flip()

pygame.quit()
