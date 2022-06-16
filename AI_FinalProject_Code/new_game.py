import random
import sys

import numpy as np

import GameBoard
import minmax
from MCTS_algorithm import MCTS, Board
from minmax import *

pygame.init()
board_width = 15
X_n = board_width
Y_n = board_width
margin_X = 27
margin_Y = 27
screen_X = (X_n - 1) * 44 + margin_X * 2
screen_Y = (Y_n - 1) * 44 + margin_Y * 2
screen = pygame.display.set_mode((screen_X, screen_Y))
modes_list = ['MANUAL', 'MANUAL']
prev_x, prev_y = -1, -1

screen_color = [238, 154, 73]  # background_color
line_color = [0, 0, 0]  # line_color


# get the position where a piece can be placed
def find_pos(x, y):
    for i in range(margin_X, screen_X, 44):
        for j in range(margin_Y, screen_X, 44):
            L1 = i - 22
            L2 = i + 22
            R1 = j - 22
            R2 = j + 22
            if x >= L1 and x <= L2 and y >= R1 and y <= R2:
                return i, j
    return -1, -1


# check whether the poistion piece been placed
def is_placed(x, y, over_pos):
    for val in over_pos:
        if val[0][0] == x and val[0][1] == y:
            return True
    return False


flag = False
time = 0

# the positions of placed peices
placed_pos = []
white_color = [255, 255, 255]
black_color = [0, 0, 0]


#
def is_End(placed_pos):
    mp = np.zeros([X_n, Y_n], dtype=int)
    for val in placed_pos:
        x = int((val[0][0] - margin_X) / 44)
        y = int((val[0][1] - margin_Y) / 44)
        if val[1] == white_color:
            mp[x][y] = 2  # white piece
        else:
            mp[x][y] = 1  # black piece

    # 一直線
    for i in range(X_n):
        pos1 = []
        pos2 = []
        for j in range(Y_n):
            if mp[i][j] == 1:
                pos1.append([i, j])
            else:
                pos1 = []
            if mp[i][j] == 2:
                pos2.append([i, j])
            else:
                pos2 = []
            if len(pos1) >= 5:  # win
                return [1, pos1]
            if len(pos2) >= 5:  # win
                return [2, pos2]
    # 一橫線
    for j in range(Y_n):
        pos1 = []
        pos2 = []
        for i in range(X_n):
            if mp[i][j] == 1:
                pos1.append([i, j])
            else:
                pos1 = []
            if mp[i][j] == 2:
                pos2.append([i, j])
            else:
                pos2 = []
            if len(pos1) >= 5:  # win
                return [1, pos1]
            if len(pos2) >= 5:  # win
                return [2, pos2]

    for i in range(X_n):
        for j in range(Y_n):
            pos1 = []
            pos2 = []
            for k in range(max(X_n, Y_n)):
                if i + k >= X_n or j + k >= Y_n:
                    break
                if mp[i + k][j + k] == 1:
                    pos1.append([i + k, j + k])
                else:
                    pos1 = []
                if mp[i + k][j + k] == 2:
                    pos2.append([i + k, j + k])
                else:
                    pos2 = []
                if len(pos1) >= 5:  # win
                    return [1, pos1]
                if len(pos2) >= 5:  # win
                    return [2, pos2]
    for i in range(X_n):
        for j in range(Y_n):
            pos1 = []
            pos2 = []
            for k in range(max(X_n, Y_n)):
                if i + k >= X_n or j - k < 0:
                    break
                if mp[i + k][j - k] == 1:
                    pos1.append([i + k, j - k])
                else:
                    pos1 = []
                if mp[i + k][j - k] == 2:
                    pos2.append([i + k, j - k])
                else:
                    pos2 = []
                if len(pos1) >= 5:  # win
                    return [1, pos1]
                if len(pos2) >= 5:  # win
                    return [2, pos2]
    return [0, []]

font = pygame.font.SysFont(None, 44 * 2 // 3)
board=GameBoard.Map(board_width,board_width)
while True:

    # EXIT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == ord('a'):
                modes_list[0] = 'MANUAL'
            if event.key == ord('s'):
                modes_list[0] = 'RANDOM'
            if event.key == ord('d'):
                modes_list[0] = 'MCTS'
            if event.key == ord('f'):
                modes_list[0] = 'MINIMAX'
            if event.key == ord('h'):
                modes_list[1] = 'MANUAL'
            if event.key == ord('j'):
                modes_list[1] = 'RANDOM'
            if event.key == ord('k'):
                modes_list[1] = 'MCTS'
            if event.key == ord('l'):
                modes_list[1] = 'MINIMAX'

    screen.fill(screen_color)

    # vertical lines
    for i in range(27, screen_X, 44):

        if i == 27 or i == screen_X - 27:
            pygame.draw.line(screen, line_color, [i, margin_X], [i, screen_X - margin_X], 4)
        else:
            pygame.draw.line(screen, line_color, [i, margin_X], [i, screen_X - margin_X], 2)

    # horizonal lines
    for i in range(27, screen_Y, 44):
        if i == 27 or i == screen_Y - 27:
            pygame.draw.line(screen, line_color, [margin_Y, i], [screen_Y - margin_Y, i], 4)
        else:
            pygame.draw.line(screen, line_color, [margin_Y, i], [screen_Y - margin_Y, i], 2)
    # central dot
    pygame.draw.circle(screen, line_color, [margin_X + 44 * (int((X_n) / 2)), margin_Y + 44 * (int((Y_n) / 2))], 8, 0)

    i = 1
    # show all the pieces
    for val in placed_pos:
        pygame.draw.circle(screen, val[1], val[0], 20, 0)
        if i % 2 == 0:
            text=font.render(str(i), True,black_color , white_color)
        else:
            text=font.render(str(i), True,white_color , black_color)
        text_rect=text.get_rect()
        text_rect.center=tuple(val[0])
        screen.blit(text,text_rect)
        i=i+1

    if prev_x != -1 and prev_y != -1:
        pygame.draw.rect(screen, [255, 0, 0], [prev_x - 22, prev_y - 22, 44, 44], 2, 1)

    # check if the game is over
    res = is_End(placed_pos)
    if res[0] != 0:
        for pos in res[1]:
            pygame.draw.rect(screen, [238, 48, 167], [pos[0] * 44 + 27 - 22, pos[1] * 44 + 27 - 22, 44, 44], 2, 1)
        pygame.display.update()
        continue

    if modes_list[len(placed_pos) % 2] == 'MANUAL':
        # get the position of where the cursor
        x, y = pygame.mouse.get_pos()
        x, y = find_pos(x, y)
        if not is_placed(x, y, placed_pos) and (x != -1 and y != -1):
            # draw a sqaure to show exactly where the piece is going to be placed
            pygame.draw.rect(screen, [0, 229, 238], [x - 22, y - 22, 44, 44], 2, 1)

        # get mouse_click info
        keys_pressed = pygame.mouse.get_pressed()
        # place the piece
        if keys_pressed[0] and time == 0:
            flag = True
            if not is_placed(x, y, placed_pos) and (x != -1 and y != -1):
                if len(placed_pos) % 2 == 0:
                    pos1 = int((x - margin_X) / 44)
                    pos2 = int((y - margin_Y) / 44)
                    board.click(pos1,pos2,GameBoard.MAP_ENTRY_TYPE.MAP_PLAYER_ONE)  # black piece
                    placed_pos.append([[x, y], black_color])
                else:
                    pos1 = int((x - margin_X) / 44)
                    pos2 = int((y - margin_Y) / 44)
                    board.click(pos1, pos2, GameBoard.MAP_ENTRY_TYPE.MAP_PLAYER_TWO)  # white piece
                    placed_pos.append([[x, y], white_color])
                prev_x, prev_y = x, y
    elif modes_list[len(placed_pos) % 2] == 'RANDOM':
        x, y = random.random() * screen_X, random.random() * screen_Y
        x, y = find_pos(x, y)
        if time == 0:
            flag = True
            if not is_placed(x, y, placed_pos) and (x != -1 and y != -1):
                if len(placed_pos) % 2 == 0:
                    pos1 = int((x - margin_X) / 44)
                    pos2 = int((y - margin_Y) / 44)
                    board.click(pos1, pos2, GameBoard.MAP_ENTRY_TYPE.MAP_PLAYER_ONE)  # black piece
                    placed_pos.append([[x, y], black_color])
                else:
                    pos1 = int((x - margin_X) / 44)
                    pos2 = int((y - margin_Y) / 44)
                    board.click(pos1, pos2, GameBoard.MAP_ENTRY_TYPE.MAP_PLAYER_TWO)  # white piece
                    placed_pos.append([[x, y], white_color])
                prev_x, prev_y = x, y
    elif modes_list[len(placed_pos) % 2] == 'MCTS':
        if time == 0:
            flag = True
            mcts_board = Board(X_n, Y_n, 5)
            mcts_board.init_board()
            for val in placed_pos:
                x = int((val[0][0] - margin_X) / 44)
                y = int((val[0][1] - margin_Y) / 44)
                if val[1] == black_color:
                    player = 1
                else:
                    player = 2
                mcts_board.update(player, mcts_board.location_to_move([x, y]))
            mcts = MCTS(mcts_board, [len(placed_pos) % 2 + 1, 2 - len(placed_pos) % 2])
            pos = mcts_board.move_to_location(mcts.get_action())
            x = margin_X + 44 * pos[0]
            y = margin_Y + 44 * pos[1]
            if len(placed_pos) % 2 == 0:
                pos1 = int((x - margin_X) / 44)
                pos2 = int((y - margin_Y) / 44)
                board.click(pos1, pos2, GameBoard.MAP_ENTRY_TYPE.MAP_PLAYER_ONE)  # black piece
                placed_pos.append([[x, y], black_color])
            else:
                pos1 = int((x - margin_X) / 44)
                pos2 = int((y - margin_Y) / 44)
                board.click(pos1, pos2, GameBoard.MAP_ENTRY_TYPE.MAP_PLAYER_TWO)  # white piece
                placed_pos.append([[x, y], white_color])
            prev_x, prev_y = x, y
    elif modes_list[len(placed_pos) % 2] == 'MINIMAX':
        if time == 0:
            flag = True
            turn=len(placed_pos) % 2 + 1
            for val in placed_pos:
                x = int((val[0][0] - margin_X) / 44)
                y = int((val[0][1] - margin_Y) / 44)
                if val[1] == white_color:
                    board.click(x,y,GameBoard.MAP_ENTRY_TYPE.MAP_PLAYER_TWO)  # white piece
                else:
                    board.click(x,y,GameBoard.MAP_ENTRY_TYPE.MAP_PLAYER_ONE)  # black piece
            if turn==1:
                now=GameBoard.MAP_ENTRY_TYPE.MAP_PLAYER_ONE
            else:
                now=GameBoard.MAP_ENTRY_TYPE.MAP_PLAYER_TWO
            ai=minmax.ChessAI(board_width,board.map)
            pos1,pos2=ai.findBestChess(board.map,now)
            x = margin_X + 44 * pos1
            y = margin_Y + 44 * pos2
            if len(placed_pos) % 2 == 0:
                placed_pos.append([[x, y], black_color])
            else:
                placed_pos.append([[x, y], white_color])
            prev_x, prev_y = x, y

    if flag:
        time += 1
    if time % 50 == 0:
        flag = False
        time = 0

    pygame.display.update()
