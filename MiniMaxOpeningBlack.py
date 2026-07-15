import sys

class MiniMaxOpeningBlack:
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

    def estimate_opening(self, board):
        self.eval_count += 1
        return board.count('B') - board.count('W')  # Black's perspective

    def closeMill(self, pos, board):
        piece = board[pos]
        if piece == 'x':
            return False
        for pair in self.mill_patterns.get(pos, []):
            if board[pair[0]] == piece and board[pair[1]] == piece:
                return True
        return False

    def generate_moves_opening(self, board, is_black):
        temp_board = board if is_black else self.flip_colors(board)
        result = []

        for i in range(21):
            if temp_board[i] == 'x':
                new_board = temp_board[:i] + 'B' + temp_board[i+1:]
                if self.closeMill(i, new_board):
                    removed = False
                    for j in range(21):
                        if new_board[j] == 'W' and not self.closeMill(j, new_board):
                            modified = new_board[:j] + 'x' + new_board[j+1:]
                            result.append(modified if is_black else self.flip_colors(modified))
                            removed = True
                    if not removed:
                        result.append(new_board if is_black else self.flip_colors(new_board))
                else:
                    result.append(new_board if is_black else self.flip_colors(new_board))
        return result

    def flip_colors(self, board):
        return ''.join(['B' if c == 'W' else 'W' if c == 'B' else c for c in board])

    def minimax(self, board, depth, is_maximizing):
        if depth == 0:
            return self.estimate_opening(board), board

        best_move = None
        if is_maximizing:
            value = float('-inf')
            for move in self.generate_moves_opening(board, True):  # Black's move
                score, _ = self.minimax(move, depth - 1, False)
                if score > value:
                    value, best_move = score, move
            return value, best_move
        else:
            value = float('inf')
            for move in self.generate_moves_opening(board, False):  # White move
                score, _ = self.minimax(move, depth - 1, True)
                if score < value:
                    value, best_move = score, move
            return value, best_move

if __name__ == "__main__":
    input_file = "board1.txt"
    output_file = "board2.txt"
    depth = 2

    with open(input_file, 'r') as f:
        start_board = f.read().strip()

    game = MiniMaxOpeningBlack()
    score, best_board = game.minimax(start_board, depth, True)

    with open(output_file, 'w') as f:
        f.write(best_board)

    print(f"Board Position: {best_board}")
    print(f"Positions evaluated by static estimation: {game.eval_count}.")
    print(f"MINIMAX estimate: {score}.")