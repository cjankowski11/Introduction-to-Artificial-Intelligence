"""
Author: Katarzyna Nałęcz-Charkiewicz, Cezary Jankowski
"""

from board import Board
from player import Player
from random import choice


class MinMaxPlayer(Player):
    def __init__(self, name: str, depth_limit: int, board_size: int):
        super().__init__(name)
        self.depth_limit = depth_limit
        self.grading_tab = []
        self.create_grading_board(board_size)

    def make_move(self, board: Board, your_side: str):
        # TODO
        possible_moves = []
        for move in board.empty_indexes():
            board_after_move = board.clone()
            board_after_move.register_move(move)
            if your_side == "x":
                possible_moves.append((move, self.minimax(board_after_move, "o",
                                       self.depth_limit - 1, float('-inf'), float('inf'))))
            else:
                possible_moves.append((move, self.minimax(board_after_move, "x",
                                       self.depth_limit - 1, float('-inf'), float('inf'))))
        # print(possible_moves)
        if your_side == "x":
            value = max(possible_moves, key=lambda x: x[1])[1]

        else:
            value = min(possible_moves, key=lambda x: x[1])[1]
        # print(value)
        # print(self.grading_tab)
        best_move = [i[0] for i in possible_moves if i[1] == value]
        
        return choice(best_move)

    def minimax(self, board: Board, side: str, depth: int, alpha, beta):
        # TODO
        winner = board.who_is_winner()
        if winner is not None:
            if winner == "x":
                return float('inf')
            elif winner == "o":
                return float('-inf')
        if len(board.empty_indexes()) == 0:
            return 0
        if depth == 0:
            return self.evaluate(board)
        
        if side == "o":
            
            for move in board.empty_indexes():
                board_after_move = board.clone()
                board_after_move.register_move(move)
                value = self.minimax(board_after_move, "x", depth - 1, alpha, beta)
                if value < beta:
                    beta = value
                if alpha >= beta:
                    break
            return beta
        elif side == "x":
            
            for move in board.empty_indexes():
                board_after_move = board.clone()
                board_after_move.register_move(move)
                value = self.minimax(board_after_move, "o", depth - 1, alpha, beta)
                if value > alpha:
                    alpha = value
                if alpha >= beta:
                    break
            return alpha

    def evaluate(self, board: Board):
        # TODO
        score = 0
        
        for sign in range(len(board.board)):
            if board.board[sign] == "x":
                score += self.grading_tab[sign // board.size][sign % board.size]
            elif board.board[sign] == "o":
                score -= self.grading_tab[sign // board.size][sign % board.size]
        return score
    
    def create_grading_board(self, board_size):
        for i in range(board_size):
            self.grading_tab.append([])
            for _ in range(board_size):
                self.grading_tab[i].append(2)
        for i in range(board_size):
            self.grading_tab[i][i] += 1
            self.grading_tab[board_size-1-i][i] += 1

    def evaluate2(self, board: Board):
        # TODO
        score = 0
        
        for sign in range(len(board.board)):
            if board.board[sign] == "x":
                score += self.grading_tab[sign // board.size][sign % board.size]
            elif board.board[sign] == "o":
                score -= self.grading_tab[sign // board.size][sign % board.size]
        for i in range(board.size):
            row = board.board[i*board.size:board.size*i + board.size]
            o = row.count("o")
            x = row.count("x")
            if x == 0:
                score -= 3*o
            elif o == 0:
                score += 3*x
        
        for i in range(board.size):
            column = [board.board[j*board.size + i] for j in range(board.size)]
            o = column.count("o")
            x = column.count("x")
            if x == 0:
                score -= 3*o
            elif o == 0:
                score += 3*x
        diag1 = [board.board[i*board.size + i] for i in range(board.size)]
        diag2 = [board.board[(i+1)*(board.size-1)] for i in range(board.size)]
        for diag in [diag1, diag2]:
            x_count = diag.count("x")
            o_count = diag.count("o")
            if x_count > 0 and o_count == 0:
                score += 3*x_count
            elif o_count > 0 and x_count == 0:
                score -= 3*o_count
        if board.size % 2 == 1:
            sign = board.board[len(board.board)//2]
            if sign == "x":
                score += 2
            elif sign == "o":
                score -= 2
        return score