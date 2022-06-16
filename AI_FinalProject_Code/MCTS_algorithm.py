import copy
import math
import time
from random import choice


class Board(object):
    """
    board for game
    """

    def __init__(self, width=15, height=15, n_in_row=5):
        self.availables = None
        self.width = width
        self.height = height
        self.states = {}  # 紀錄當前棋盤的狀態，鍵是位置，值是棋子，這裡用玩家來表示棋子類型
        self.n_in_row = n_in_row  # 表示幾個相同的棋子連成一線算作勝利

    def init_board(self):
        if self.width < self.n_in_row or self.height < self.n_in_row:
            raise Exception('board width and height can not less than %d' % self.n_in_row)  # 棋盤不能過小

        self.availables = list(range(self.width * self.height))  # 表示棋盤上所有合法的位置，這裡簡單認為空的位置即合法

        for m in self.availables:
            self.states[m] = -1  # -1表示當前位置為空

    def move_to_location(self, move):
        h = move // self.width
        w = move % self.width
        return [h, w]

    def location_to_move(self, location):
        if len(location) != 2:
            return -1
        h = location[0]
        w = location[1]
        move = h * self.width + w
        if move not in range(self.width * self.height):
            return -1
        return move

    def update(self, player, move):  # player在move處落子，更新棋盤
        self.states[move] = player
        self.availables.remove(move)


class MCTS(object):
    """
    AI player, use Monte Carlo Tree Search with UCB
    """

    def __init__(self, board, play_turn, n_in_row=5, time=30, max_actions=10000):

        self.board = board
        self.play_turn = play_turn  # 出手順序
        self.calculation_time = float(time)  # 最大運算時間
        self.max_actions = max_actions  # 每次模擬對局最多進行的步數
        self.n_in_row = n_in_row

        self.player = play_turn[0]  # 輪到電腦出手，所以出手順序中第一個總是電腦
        self.confident = 1.96  # UCB中的常數
        self.plays = {}  # 記錄著法參與模擬的次數，鍵形如(player, move)，即（玩家，落子）
        self.wins = {}  # 記錄著法獲勝的次數
        self.max_depth = 1

    def get_action(self):  # return move

        if len(self.board.availables) == 1:
            return self.board.availables[0]  # 棋盤只剩最後一個落子位置，直接返回
        adjacent = self.adjacent_moves(self.board, self.player, self.plays)
        print(adjacent)
        if len(adjacent) == 0:
            if self.board.width % 2 and self.board.height:
                move = (self.board.width * self.board.height - 1) / 2
            else:
                move = (self.board.width * self.board.height - 1) / 2  # 下在正中心
            return  move

        # 每次計算下一步時都要清空plays和wins表，因為經過AI和玩家的2步棋之後，整個棋盤的局面發生了變化，原來的記錄已經不適用了——原先普通的一步現在可能是致勝的一步，如果不清空，會影響現在的結果，導致這一步可能沒那麼“致勝”了
        self.plays = {}
        self.wins = {}
        simulations = 0
        begin = time.time()
        while time.time() - begin < self.calculation_time:
            board_copy = copy.deepcopy(self.board)  # 模擬會修改board的參數，所以必須進行深拷貝，與原board進行隔離
            play_turn_copy = copy.deepcopy(self.play_turn)  # 每次模擬都必須按照固定的順序進行，所以進行深拷貝防止順序被修改
            self.run_simulation(board_copy, play_turn_copy)  # 進行MCTS
            simulations += 1

        print("total simulations=", simulations)

        move = self.select_one_move()  # 選擇最佳著法
        location = self.board.move_to_location(move)
        print('Maximum depth searched:', self.max_depth)

        print("AI move: %d,%d\n" % (location[0], location[1]))

        return move

    def run_simulation(self, board, play_turn):
        """
        MCTS main process
        """

        plays = self.plays
        wins = self.wins
        availables = board.availables

        player = self.get_player(play_turn)  # 獲取當前出手的玩家
        visited_states = set()  # 記錄當前路徑上的全部著法
        winner = -1
        expand = True

        # Simulation
        for t in range(1, self.max_actions + 1):
            # Selection
            # 如果所有著法都有統計信息，則獲取UCB最大的著法
            adjacent = self.adjacent_moves(board, player, plays)
            flag = True
            for move in adjacent:
                if plays.get((player, move),0) < 10:
                    flag = False
            if flag:
                log_total = math.log(
                    sum(plays[(player, move)] for move in adjacent))
                # print(log_total)
                value = 0
                for moves in adjacent:
                    cur_value, cur_move = ((wins[(player, moves)] / plays[(player, moves)]) +
                                           math.sqrt(self.confident * log_total / plays[(player, moves)]), moves)
                    if cur_value > value:
                        value = cur_value
                        move = cur_move
                # value, move = max(
                #     ((wins[(player, move)] / plays[(player, move)]) +
                #      sqrt(self.confident * log_total / plays[(player, move)]), move)
                #     for move in availables)
            else:
                # 否則隨機選擇一個著法
                adjacents = []
                if len(availables) > self.n_in_row:
                    adjacents = self.adjacent_moves(board, player, plays)  # 沒有統計信息的鄰近位置

                if len(adjacents):
                    move = choice(adjacents)
                else:
                    peripherals = []
                    for move in availables:
                        if not plays.get((player, move)):
                            peripherals.append(move)  # 沒有統計信息的外圍位置
                    move = choice(peripherals)

            board.update(player, move)

            # Expand
            # 每次模擬最多擴展一次，每次擴展只增加一個著法
            if expand and (player, move) not in plays:
                expand = False
                plays[(player, move)] = 0
                wins[(player, move)] = 0
                if t > self.max_depth:
                    self.max_depth = t

            visited_states.add((player, move))

            is_full = not len(availables)
            win, winner = self.has_a_winner(board)
            if is_full or win:  # 遊戲結束，沒有落子位置或有玩家獲勝
                break

            player = self.get_player(play_turn)

            # Back-propagation
        for player, move in visited_states:
            if (player, move) not in plays:
                continue
            plays[(player, move)] += 1  # 當前路徑上所有著法的模擬次數加1
            if player == winner:
                wins[(player, move)] += 1  # 獲勝玩家的所有著法的勝利次數加1

    def adjacent_moves(self, board, player, plays):
        """
        獲取當前棋局中所有棋子的鄰近位置中沒有統計信息的位置
        """
        moved = list(set(range(board.width * board.height)) - set(board.availables))
        # print('moved:',moved)
        adjacents = set()
        width = board.width
        height = board.height

        for m in moved:
            h = m // width
            w = m % width
            if w < width - 1:
                adjacents.add(m + 1)  # 右
            if w > 0:
                adjacents.add(m - 1)  # 左
            if h < height - 1:
                adjacents.add(m + width)  # 上
            if h > 0:
                adjacents.add(m - width)  # 下
            if w < width - 1 and h < height - 1:
                adjacents.add(m + width + 1)  # 右上
            if w > 0 and h < height - 1:
                adjacents.add(m + width - 1)  # 左上
            if w < width - 1 and h > 0:
                adjacents.add(m - width + 1)  # 右下
            if w > 0 and h > 0:
                adjacents.add(m - width - 1)  # 左下
        # print("adjacent: ",adjacents)
        adjacents = list(set(adjacents) - set(moved))
        # for move in adjacents:
        #     if plays.get((player, move)):
        #         adjacents.remove(move)
        return adjacents

    def get_player(self, players):
        p = players.pop(0)
        players.append(p)
        return p

    def select_one_move(self):
        global move
        percent = 0
        adjacent = self.adjacent_moves(self.board, self.player, self.plays)
        print(adjacent)
        if len(adjacent) > 0:
            for moves in adjacent:
                cur_percent, cur_move = (self.wins.get((self.player, moves), 0) /
                                         self.plays.get((self.player, moves), 1),
                                         moves)
                print(cur_percent, self.board.move_to_location(moves))
                if cur_percent > percent:
                    percent = cur_percent
                    move = cur_move
        else:
            if self.board.width % 2 and self.board.height:
                move = (self.board.width * self.board.height - 1) / 2
            else:
                move = (self.board.width * self.board.height - 1) / 2  # 下在正中心
        print("best move percent:",percent)
        return move

    def has_a_winner(self, board):
        """
        檢查是否有玩家獲勝
        """
        moved = list(set(range(board.width * board.height)) - set(board.availables))
        if len(moved) < self.n_in_row + 2:
            return False, -1

        width = board.width
        height = board.height
        states = board.states
        n = self.n_in_row
        for m in moved:
            h = m // width
            w = m % width
            player = states[m]

            if (w in range(width - n + 1) and
                    len(set(states[i] for i in range(m, m + n))) == 1):  # 橫向連成一線
                return True, player

            if (h in range(height - n + 1) and
                    len(set(states[i] for i in range(m, m + n * width, width))) == 1):  # 豎向連成一線
                return True, player

            if (w in range(width - n + 1) and h in range(height - n + 1) and
                    len(set(states[i] for i in range(m, m + n * (width + 1), width + 1))) == 1):  # 右斜向上連成一線
                return True, player

            if (w in range(n - 1, width) and h in range(height - n + 1) and
                    len(set(states[i] for i in range(m, m + n * (width - 1), width - 1))) == 1):  # 左斜向下連成一線
                return True, player

        return False, -1