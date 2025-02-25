import chess

class ChessGame:
    def __init__(self, fen_string=None):
        self.board = chess.Board(fen_string) if fen_string else chess.Board()

    def is_valid_move(self, from_square, to_square):
        try:
            move = chess.Move.from_uci(f"{from_square}{to_square}")
            return move in self.board.legal_moves
        except ValueError:
            return False

    def make_move(self, from_square, to_square):
        try:
            move = chess.Move.from_uci(f"{from_square}{to_square}")
            if move in self.board.legal_moves:
                piece = self.board.piece_at(chess.parse_square(from_square)).symbol()
                self.board.push(move)
                return {
                    'status': 'success',
                    'piece': piece,
                    'game_state': self.board.fen(),
                    'is_checkmate': self.board.is_checkmate(),
                    'is_check': self.board.is_check(),
                    'current_turn': 'black' if self.board.turn == chess.BLACK else 'white'
                }
            return {'status': 'error', 'message': 'Invalid move'}
        except ValueError:
            return {'status': 'error', 'message': 'Invalid square notation'}

    def get_piece_at(self, square):
        try:
            piece = self.board.piece_at(chess.parse_square(square))
            return piece.symbol() if piece else None
        except ValueError:
            return None

    def is_game_over(self):
        return self.board.is_game_over()

    def get_game_state(self):
        return {
            'fen': self.board.fen(),
            'is_checkmate': self.board.is_checkmate(),
            'is_check': self.board.is_check(),
            'is_stalemate': self.board.is_stalemate(),
            'is_insufficient_material': self.board.is_insufficient_material(),
            'current_turn': 'black' if self.board.turn == chess.BLACK else 'white'
        }