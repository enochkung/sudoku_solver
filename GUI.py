# sudoku solver GUI
import pygame
from sudoku_solver import solve, check_valid, get_col, get_nine_group, get_row
import time

pygame.font.init()


class Board:

    board = [
        [0, 0, 0, 0, 7, 8, 0, 4, 0],
        [2, 0, 1, 0, 6, 0, 0, 7, 0],
        [0, 0, 0, 1, 5, 0, 8, 3, 0],
        [0, 0, 8, 0, 0, 0, 4, 0, 7],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [7, 0, 5, 0, 0, 0, 1, 0, 0],
        [0, 6, 7, 0, 9, 2, 0, 0, 0],
        [0, 5, 0, 0, 1, 0, 7, 0, 9],
        [0, 1, 0, 6, 3, 0, 0, 0, 0],
    ]

    def __init__(self, rows, cols, height, width):
        self.rows = rows
        self.cols = cols
        self.cubes = [
            [Cube(self.board[i][j], i, j, width, height) for i in range(9)]
            for j in range(9)
        ]
        self.width = width
        self.height = height
        self.selected = None

    def update_model(self):
        self.model = [
            [self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)
        ]

    def place(self, temp_value):
        x, y = self.selected
        if self.cubes[x][y].value == 0:
            self.cubes[x][y].set(temp_value)
            self.update_model()

            if check_valid(self.model, (x, y), temp_value) and solve(self.model):
                return True
            else:
                self.cubes[x][y].set(0)
                self.cubes[x][y].set_temp(0)
                self.update_model()
                return False

    def select(self, x, y):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.selected = (x, y)
        self.cubes[x][y].selected = True

    def click(self, pos):
        xseg = self.width / 9
        yseg = self.height / 9

        xblock = [x for x in range(9) if x * xseg <= pos[0]][-1]
        yblock = [y for y in range(9) if y * yseg <= pos[1]][-1]

        return xblock, yblock

    def sketch(self, key):
        x, y = self.selected
        self.cubes[x][y].set_temp(key)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(
                win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick
            )

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def clear(self):
        x, y = self.selected
        if self.cubes[x][y].value == 0:
            self.cubes[x][y].set_temp(0)

    def is_finished(self):
        for x in range(self.rows):
            for y in range(self.cols):
                if self.cubes[x][y].value == 0:
                    return False
        return True


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

    def draw(self, win):
        font = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(
                text,
                (
                    x + 0.5 * (gap - text.get_width()),
                    y + 0.5 * (gap - text.get_height()),
                ),
            )
        if self.selected:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)


def redraw_window(win, board, time, strikes):
    win.fill((255, 255, 255))
    # time
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render("time: " + format_time(time), 1, (0, 0, 0))
    win.blit(text, (540 - 160, 560))
    # strikes
    text = font.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # draw
    board.draw(win)


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    board = Board(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    strikes = 0

    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None
                    if board.is_finished():
                        print("Game Over")
                        run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()