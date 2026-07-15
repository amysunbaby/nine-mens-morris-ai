import sys

class ABOpening:
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
        return board.count('W') - board.count('B')

    def closeMill(self, pos, board):
        piece = board[pos]
        if piece == 'x':
            return False
        for pair in self.mill_patterns.get(pos, []):
            if board[pair[0]] == piece and board[pair[1]] == piece:
                return True
        return False

    def generate_moves_opening(self, board, is_white):
        temp_board = list(board if is_white else self.flip_colors(board))
        result = []

        for i in range(21):
            if temp_board[i] == 'x':
                temp_board[i] = 'W'
                if self.closeMill(i, temp_board):
                    removed = False
                    for j in range(21):
                        if temp_board[j] == 'B' and not self.closeMill(j, temp_board):
                            temp_board[j] = 'x'
                            result.append(''.join(temp_board) if is_white else self.flip_colors(''.join(temp_board)))
                            temp_board[j] = 'B'
                            removed = True
                    if not removed:
                        result.append(''.join(temp_board) if is_white else self.flip_colors(''.join(temp_board)))
                else:
                    result.append(''.join(temp_board) if is_white else self.flip_colors(''.join(temp_board)))
                temp_board[i] = 'x'

        return result

    def flip_colors(self, board):
        return ''.join(['B' if c == 'W' else 'W' if c == 'B' else c for c in board])

    def alphabeta(self, board, depth, alpha, beta, is_maximizing):
        if depth == 0:
            return self.estimate_opening(board), board

        best_move = None
        if is_maximizing:
            value = float('-inf')
            for move in self.generate_moves_opening(board, True):
                score, _ = self.alphabeta(move, depth - 1, alpha, beta, False)
                if score > value:
                    value, best_move = score, move
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # pruning
        else:
            value = float('inf')
            for move in self.generate_moves_opening(board, False):
                score, _ = self.alphabeta(move, depth - 1, alpha, beta, True)
                if score < value:
                    value, best_move = score, move
                beta = min(beta, value)
                if alpha >= beta:
                    break  # pruning

        return value, best_move

if __name__ == "__main__":
    input_file = "board1.txt"
    output_file = "board2.txt"
    depth = 2

    with open(input_file, 'r') as f:
        start_board = f.read().strip()

    game = ABOpening()
    score, best_board = game.alphabeta(start_board, depth, float('-inf'), float('inf'), True)

    with open(output_file, 'w') as f:
        f.write(best_board)

    print(f"Board Position: {best_board}")
    print(f"Positions evaluated by static estimation: {game.eval_count}.")
    print(f"ALPHA-BETA estimate: {score}.")