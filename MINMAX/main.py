import math
import random


def print_board(board):
    print()
    for i in range(0, 9, 3):
        print(board[i:i + 3])
    print()


def check_winner(board):
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for line in wins:
        if board[line[0]] == board[line[1]] == board[line[2]] != ' ':
            return board[line[0]]
    if ' ' not in board:
        return 'Draw'
    return None


def evaluate_board(board):
    result = check_winner(board)
    if result == 'X':
        return 10
    elif result == 'O':
        return -10
    elif result == 'Draw':
        return 0

    def count_lines(player):
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        count = 0
        for line in lines:
            if all(board[i] == player or board[i] == ' ' for i in line):
                count += 1
        return count

    x_lines = count_lines('X')
    o_lines = count_lines('O')
    return x_lines - o_lines


def minimax(board, depth, max_depth, alpha, beta, is_maximizing):
    score = evaluate_board(board)
    result = check_winner(board)

    if depth == max_depth or result is not None:
        return score

    if is_maximizing:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                eval = minimax(board, depth + 1, max_depth, alpha, beta, False)
                board[i] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                eval = minimax(board, depth + 1, max_depth, alpha, beta, True)
                board[i] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval


def best_move(board, max_depth):
    best_score = -math.inf
    best_move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            score = minimax(board, 0, max_depth, -math.inf, math.inf, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    return best_move


def player_move(board):
    while True:
        try:
            move = int(input("Twój ruch (0-8): "))
            if 0 <= move < 9 and board[move] == ' ':
                return move
            else:
                print("Nieprawidlowy ruch. Sprobuj jeszcze raz.")
        except ValueError:
            print("Podaj liczbe od 0 do 8.")


def play_game():
    board = [' '] * 9
    print("Gra w Kolko i Krzyzyk – Ty grasz jako 'O'.")
    print("Numeracja pol:")
    print_board([str(i) for i in range(9)])

    max_depth = int(input("Podaj maksymalną głębokość przeszukiwania dla AI (1-9): "))
    max_depth = max(1, min(9, max_depth))

    current_player = 'X'

    while True:
        if current_player == 'X':
            move = best_move(board, max_depth)
            board[move] = 'X'
            print(f"\nAI (X) wykonuje ruch na polu {move}:")
        else:
            move = player_move(board)
            board[move] = 'O'
            print(f"\nTwoj ruch (O) na pole {move}:")

        print_board(board)

        winner = check_winner(board)
        if winner:
            if winner == 'Draw':
                print("Remis!")
            elif winner == 'X':
                print("AI (X) wygralo!")
            else:
                print("Wygrales!")
            break

        current_player = 'O' if current_player == 'X' else 'X'


play_game()