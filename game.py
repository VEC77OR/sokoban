import pygame, sys, time
import sqlite3
from pygame.locals import *


def move(direction, spritex, spritey, moves, board):
    j, i = board.get_cell((spritex, spritey))
    if direction:
        if direction == K_UP and board.is_empty(i - 1, j, 'up'):
            spritey -= 64
        elif direction == K_DOWN and board.is_empty(i + 1, j, 'down'):
            spritey += 64
        elif direction == K_LEFT and board.is_empty(i, j - 1, 'left'):
            spritex -= 64
        elif direction == K_RIGHT and board.is_empty(i, j + 1, 'right'):
            spritex += 64
    moves -= 1
    return spritex, spritey, moves

def draw(win, screen, width, height, id):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)

    if win:
        id += 1
        if id > 3:
            text = font.render("YOU WON!", 1, (100, 255, 100))
            f = open('save_id.txt', 'w')
            id = '1'
            f.write(id)
        else:
            main_board(id)
    else:
        main_board(id)
        

    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()

    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)

def get_click(pos):
    x, y = pos
    
    if 10 <= x <= 90:
        if 250 <= y <= 295:
            id = int(open('save_id.txt', 'r').read())
            main_board(id)
        elif 340 <= y <= 385:
            rules()


class Board:
    # создание поля
    def __init__(self, width, height, play_board, screen):
        self.screen = screen
        self.width = width
        self.height = height
        # значения по умолчанию
        self.green_rects = list()
        self.rects = [[0] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 64
        self.click = 1
        self.color = pygame.Color('white')
        
        # настройка игрового поля
        self.board = play_board

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                x = self.left + j * self.cell_size
                y = self.top + i * self.cell_size
                pygame.draw.rect(self.screen, self.color, (x, y,
                                                 self.cell_size,
                                                 self.cell_size), 1)

                self.rects[i][j] = (x, y, x + self.cell_size,
                                    y + self.cell_size)

                if self.board[i][j] == 1:
                    image = pygame.image.load('data//block_04.png')
                    myRect = (x, y)
                    self.screen.blit(image, myRect)
                
                if self.board[i][j] == 2:
                    image = pygame.image.load('data//crate_07.png')
                    myRect = (x, y)
                    self.screen.blit(image, myRect)
                
                if self.board[i][j] == 4:
                    image = pygame.image.load('data//block_06.png')
                    myRect = (x, y)
                    self.screen.blit(image, myRect)

                for rect in self.green_rects:
                    i_, j_ = rect
                    if self.board[i_][j_] != 2:
                        self.board[i_][j_] = 3

                if self.board[i][j] == 3:
                    color = pygame.Color('green')
                    pygame.draw.rect(self.screen, color, (x + 1, y + 1,
                                                 self.cell_size - 2,
                                                 self.cell_size - 2), 3)

    def get_cell(self, player_pos):
        exit_flag = False
        x, y = player_pos

        return x // 64, y // 64
        
    def is_empty(self, i, j, direction):
        if self.board[i][j] == 0:
            return True
        elif self.board[i][j] == 2 and self.can_move_block(i, j, direction):
            self.move_block(i, j, direction)
            return True
        if self.board[i][j] == 3:
            return True
        else:
            return False
    
    def move_block(self, i, j, direction):
        if direction == 'up':
            self.board[i][j] = 0
            self.board[i - 1][j] = 2
        elif direction == 'down':
            self.board[i][j] = 0
            self.board[i + 1][j] = 2
        elif direction == 'left':
            self.board[i][j] = 0
            self.board[i][j - 1] = 2
        elif direction == 'right':
            self.board[i][j] = 0
            self.board[i][j + 1] = 2
    
    def can_move_block(self, i, j, direction):
        if direction == 'up':
            i = i - 1
        elif direction == 'down':
            i = i + 1
        elif direction == 'left':
            j = j - 1
        elif direction == 'right':
            j = j + 1
        
        if self.board[i][j] == 0:
            return True
        elif self.board[i][j] == 3:
            self.remember_pos(i, j)
            return True
        else:
            return False
    
    def remember_pos(self, i, j):
        for _ in self.green_rects:
            x, y = _
            if self.board[x][y] == 3:
                self.green_rects.remove(_)
        self.green_rects.append((i, j))
    
    def return_board(self):
        return self.green_rects, self.board
    
# стартовое меню
def menu():
    pygame.init()
    
    size = width, height = 673, 423
    screen = pygame.display.set_mode(size)
    
    image = pygame.image.load('data//back.png')
    screen.blit(image, (0, 0))
    
    font = pygame.font.Font(None, 30)
    text = font.render('START!', 1, (100, 255, 100))
    text_x = 16
    text_y = 265
    screen.blit(text, (text_x, text_y))
    
    font = pygame.font.Font(None, 30)
    text = font.render('RULES', 1, (100, 255, 100))
    text_x = 16
    text_y = 355
    screen.blit(text, (text_x, text_y))
    
    pygame.draw.rect(screen, (0, 255, 0), (10, 250,
                                           80, 45), 2)
    pygame.draw.rect(screen, (0, 255, 0), (10, 340,
                                           80, 45), 2)
    
    pygame.display.flip()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                    get_click(event.pos)
                    running = False
                    
    pygame.quit()

# игровое поле
def main_board(id):
    pygame.init()
    
    con = sqlite3.connect('sokoban.db')
    
    cursor = con.cursor()
    if id == 1:
        new_board = open('level_1.txt', 'r').read().split('\n')
    elif id == 2:
        new_board = open('level_2.txt', 'r').read().split('\n')
    elif id == 3:
        new_board = open('level_3.txt', 'r').read().split('\n')
    
    play_board = list()
    new_line = list()
    for line in new_board:
        for elem in line.split(', '):
            new_line.append(int(elem))
        play_board.append(new_line)
        new_line = list()
    
    x = (cursor.execute('''SELECT width
                        FROM levels
                        WHERE id = "{}"'''.format(id))).fetchall()[0][0]
    y = (cursor.execute('''SELECT height
                        FROM levels
                        WHERE id = "{}"'''.format(id))).fetchall()[0][0]
    moves = (cursor.execute('''SELECT moves
                        FROM levels
                        WHERE id = "{}"'''.format(id))).fetchall()[0][0]
    player_x = (cursor.execute('''SELECT pl_x
                        FROM levels
                        WHERE id = "{}"'''.format(id))).fetchall()[0][0]
    player_y = (cursor.execute('''SELECT pl_y
                        FROM levels
                        WHERE id = "{}"'''.format(id))).fetchall()[0][0]
    FPS = 11
    fpsClock=pygame.time.Clock()
    
    con.close()
    
    size = (x * 64, y * 64)
    screen = pygame.display.set_mode(size)
    
    board = Board(x, y, play_board, screen)
    board.render()
    pygame.display.update()
    
    sprite=pygame.image.load('data//player_01.png')
    
    spritex = 64 * player_x
    spritey = 64 * player_y
    direction=False
    running = True
    
    while running:
        fpsClock.tick(FPS)
        screen.fill(pygame.Color('black'))
        screen.blit(screen,(0,0))
        screen.blit(sprite,(spritex,spritey))
    
        for event in pygame.event.get():   
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                direction = event.key
            if event.type == KEYUP:
                direction = False
    
        board.render()
        pygame.display.update()
    
        spritex, spritey, moves = move(direction, spritex, spritey,
                                       moves, board)
    
    pygame.quit()
    
    counter = 0
    green_rects, exit_board = board.return_board()
    for _ in green_rects:
        x, y = _
        if exit_board[x][y] == 2:
            counter += 1
    
    final_window(counter, green_rects, id)

# финальное окно
def final_window(counter, green_rects, id):
    pygame.init()
    
    size = width, height = 300, 100
    screen = pygame.display.set_mode(size)
    
    if counter == len(green_rects) and counter > 0:
        draw(True, screen, width, height, id)
    else:
        draw(False, screen, width, height, id)
    
    pygame.display.flip()
    
    while pygame.event.wait().type != pygame.QUIT:
        pass
    
    pygame.quit()

def rules():
    pass

menu()
