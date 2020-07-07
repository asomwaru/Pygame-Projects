import pygame

RULES = [0,0,0,1,1,1,1,0][::-1]
CELLS = 50
board = [[0] * CELLS]
GEN = CELLS

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCALE = 10
WIDTH = CELLS * SCALE
HEIGHT = GEN * SCALE
WINDOW_SIZE = [HEIGHT, WIDTH]
FRAME_RATE = 10

print("Window Size: " + ", ".join(list(map(str, WINDOW_SIZE))))

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Elementary Cellular Automata")

def generate():
    for y in range(GEN):
        new_arr = [0] * CELLS
        current = board[y]

        for x in range(CELLS):
            left = (x - 1) % (len(current))
            center = x
            right = (x + 1) % (len(current))

            binary = int("".join(map(str, [current[left], current[center], current[right]])), 2)
            new_arr[x] = RULES[binary]

        board.append(new_arr)

def display_board():
    for x in board:
        print(" ".join(['#' if y == 1 else '.' for y in x]))

def draw():
    for r in range(CELLS):
        for c in range(GEN):
            color = None

            if board[r][c] == 1:
                color = BLACK
            elif board[r][c] == 0:
                color = WHITE

            pygame.draw.rect(
                screen,
                color,
                [
                    SCALE * c,
                    SCALE * r,
                    SCALE,
                    SCALE,
                ],
            )


def main():
    done = False

    board[0][CELLS // 2] = 1
    generate()
    display_board()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill((0, 0, 0))
        draw()

        clock.tick(FRAME_RATE)

        pygame.display.flip()


if __name__ == '__main__':
    main()