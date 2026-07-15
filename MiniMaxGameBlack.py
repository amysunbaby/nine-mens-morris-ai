import sys

class MiniMaxGameBlack:
    def __init__(self):
        self.eval_count = 0
        self.mill_patterns = {
            0: [(2, 4), (6, 18)], 1: [(3, 5), (11, 20)], 2: [(0, 4), (7, 15)],
            3: [(1, 5), (8, 12)], 4: [(0, 2), (9, 14)], 5: [(1, 3), (10, 17)],
            6: [(0, 18), (7, 8)], 7: [(2, 15), (6, 8)], 8: [(3, 12), (6, 7)],
            9: [(4, 14), (10, 11)], 10: [(5, 17), (9, 11)], 11: [(1, 20), (9, 10)],
            12: [(8, 3), (13, 14)], 13: [(12, 14), (16, 19)], 14: [(4, 9), (12, 13)],
            15: [(7, 2), (16, 17)], 16: [(15, 17), (13, 19)], 17: [(5, 10), (15, 16)],
            18: [(0, 6), (19, 20)], 19: [(16, 13), (18, 20)], 20: [(1, 11), (18, 19)]
        }

    def closeMill(self, pos, board):
        piece = board[pos]
        if piece == 'x':
            return False
        for pair in self.mill_patterns.get(pos, []):
            if board[pair[0]] == piece and board[pair[1]] == piece:
                return True
        return False

    def get_neighbors(self, pos):
        return {
            0: [1, 2, 6], 1: [0, 3, 11], 2: [0, 3, 4, 7],
            3: [1, 2, 5, 8], 4: [2, 5, 9], 5: [3, 4, 10],
            6: [0, 7, 18], 7: [2, 6, 8, 15], 8: [3, 7, 9, 12],
            9: [4, 8, 10, 14], 10: [5, 9, 11, 17], 11: [1, 10, 20],
            12: [8, 13, 15], 13: [12, 14, 16], 14: [9, 13, 17],
            15: [7, 12, 18], 16: [13, 15, 17, 19], 17: [10, 14, 16, 20],
            18: [6, 15, 19], 19: [16, 18, 20], 20: [11, 17, 19]
        }.get(pos, [])

    def generate_remove(self, board, is_black):
        opponent = 'W' if is_black else 'B'
        removed_boards = []
        found = False
        for i in range(21):
            if board[i] == opponent and not self.closeMill(i, board):
                b = board[:i] + 'x' + board[i+1:]
                removed_boards.append(b)
                found = True
        if not found:
            removed_boards.append(board)
        return removed_boards

    def generate_moves_midgame_endgame(self, board, is_black):
        piece = 'B' if is_black else 'W'
        count = board.count(piece)
        moves = []

        if count == 3:
            for i in range(21):
                if board[i] == piece:
                    for j in range(21):
                        if board[j] == 'x':
                            new_board = list(board)
                            new_board[i], new_board[j] = 'x', piece
                            new_board = ''.join(new_board)
                            if self.closeMill(j, new_board):
                                moves.extend(self.generate_remove(new_board, is_black))
                            else:
                                moves.append(new_board)
        else:
            for i in range(21):
                if board[i] == piece:
                    for j in self.get_neighbors(i):
                        if board[j] == 'x':
                            new_board = list(board)
                            new_board[i], new_board[j] = 'x', piece
                            new_board = ''.join(new_board)
                            if self.closeMill(j, new_board):
                                moves.extend(self.generate_remove(new_board, is_black))
                            else:
                                moves.append(new_board)

        return list(set(moves))

    def estimate_midgame(self, board):
        self.eval_count += 1
        white = board.count('W')
        black = board.count('B')
        white_moves = len(self.generate_moves_midgame_endgame(board, False))  # Count white moves

        if white <= 2:
            return 10000  # Black wins
        elif black <= 2:
            return -10000  # White wins
        elif white_moves == 0:
            return 10000  # Black wins (no white moves)
        else:
            return 1000 * (black - white) - white_moves  # Favor black

    def minimax(self, board, depth, is_maximizing):
        if depth == 0:
            return self.estimate_midgame(board), board

        best_move = None
        if is_maximizing:  # Black's turn (maximizing player)
            value = float('-inf')
            for move in self.generate_moves_midgame_endgame(board, True):  # Generate black moves
                score, _ = self.minimax(move, depth - 1, False)
                if score > value:
                    value, best_move = score, move
        else:  # White's turn (minimizing player)
            value = float('inf')
            for move in self.generate_moves_midgame_endgame(board, False):  # Generate white moves
                score, _ = self.minimax(move, depth - 1, True)
                if score < value:
                    value, best_move = score, move

        return value, best_move

if __name__ == "__main__":
    input_file = "board3.txt"
    output_file = "board4.txt"
    depth = 2

    with open(input_file, 'r') as f:
        start_board = f.read().strip()

    game = MiniMaxGameBlack()
    score, best_board = game.minimax(start_board, depth, True)

    with open(output_file, 'w') as f:
        f.write(best_board)

    print(f"Board Position: {best_board}")
    print(f"Positions evaluated by static estimation: {game.eval_count}")
    print(f"MINIMAX estimate: {score}")
