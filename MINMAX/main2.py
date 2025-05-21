from enum import Enum
from typing import List, Tuple, Optional
import sys


class Player(Enum):
    X = 'X'
    O = 'O'
    None_ = '-'


class TicTacToeGame:
    def __init__(self):
        self.board_size = 3
        self.board = [[Player.None_ for _ in range(self.board_size)] for _ in range(self.board_size)]

    def make_move(self, row: int, col: int, player: Player) -> None:
        if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
            raise ValueError("Invalid board position")

        if self.board[row][col] != Player.None_:
            raise ValueError("Position already occupied")

        self.board[row][col] = player

    def is_game_over(self) -> Tuple[bool, Player]:
        # Check rows
        for i in range(self.board_size):
            if self.board[i][0] != Player.None_ and self.board[i][0] == self.board[i][1] == self.board[i][2]:
                return (True, self.board[i][0])

        # Check columns
        for j in range(self.board_size):
            if self.board[0][j] != Player.None_ and self.board[0][j] == self.board[1][j] == self.board[2][j]:
                return (True, self.board[0][j])

        # Check diagonals
        if self.board[0][0] != Player.None_ and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return (True, self.board[0][0])

        if self.board[0][2] != Player.None_ and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return (True, self.board[0][2])

        # Check for draw
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == Player.None_:
                    return (False, Player.None_)

        return (True, Player.None_)

    def get_available_moves(self) -> List[Tuple[int, int]]:
        moves = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == Player.None_:
                    moves.append((i, j))
        return moves

    def clone(self) -> 'TicTacToeGame':
        new_game = TicTacToeGame()
        new_game.board = [row.copy() for row in self.board]
        return new_game

    def print_board(self) -> None:
        for row in self.board:
            print(' '.join(cell.value for cell in row))
        print()


class MinMaxAI:
    def find_best_move(self, game: TicTacToeGame, ai_player: Player, max_depth: int) -> Tuple[int, int]:
        human_player = Player.O if ai_player == Player.X else Player.X
        best_score = -sys.maxsize
        best_move = (-1, -1)

        for move in game.get_available_moves():
            new_game = game.clone()
            new_game.make_move(move[0], move[1], ai_player)

            score = self.minimax(new_game, 1, False, ai_player, human_player, -sys.maxsize, sys.maxsize, max_depth)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def minimax(self, game: TicTacToeGame, depth: int, is_maximizing: bool,
                ai_player: Player, human_player: Player, alpha: int, beta: int, max_depth: int) -> int:
        game_over, winner = game.is_game_over()
        if game_over:
            if winner == ai_player:
                return 10 - depth
            elif winner == human_player:
                return depth - 10
            else:
                return 0

        if depth >= max_depth:
            return self.evaluate_board(game, ai_player, human_player)

        if is_maximizing:
            best_score = -sys.maxsize
            for move in game.get_available_moves():
                new_game = game.clone()
                new_game.make_move(move[0], move[1], ai_player)
                score = self.minimax(new_game, depth + 1, False, ai_player, human_player, alpha, beta, max_depth)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = sys.maxsize
            for move in game.get_available_moves():
                new_game = game.clone()
                new_game.make_move(move[0], move[1], human_player)
                score = self.minimax(new_game, depth + 1, True, ai_player, human_player, alpha, beta, max_depth)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score

    def evaluate_board(self, game: TicTacToeGame, ai_player: Player, human_player: Player) -> int:
        score = 0
        for i in range(3):
            for j in range(3):
                if game.board[i][j] == ai_player:
                    score += 1
                elif game.board[i][j] == human_player:
                    score -= 1
        return score


def main():
    game = TicTacToeGame()
    ai = MinMaxAI()
    current_player = Player.X

    max_depth = int(input("Podaj maksymalną głębokość przeszukiwania dla AI (np. 2): "))

    while True:
        game_over, winner = game.is_game_over()
        if game_over:
            break

        game.print_board()

        if current_player == Player.X:
            print("Player X turn (row and column, 0-2):")
            row, col = map(int, input().split())
            game.make_move(row, col, Player.X)
        else:
            best_move = ai.find_best_move(game, Player.O, max_depth)
            game.make_move(best_move[0], best_move[1], Player.O)
            print(f"AI chose: {best_move[0]}, {best_move[1]}")

        current_player = Player.O if current_player == Player.X else Player.X

    game.print_board()
    game_over, winner = game.is_game_over()
    if winner != Player.None_:
        print(f"{winner.value} wins!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()