import chess
import random

class ChessBot:
    def __init__(self):
        self.board = None

    def set_board(self, fen_string):
        self.board = chess.Board(fen_string)

    def get_best_move(self):
        # Get all legal moves
        legal_moves = list(self.board.legal_moves)
        if not legal_moves:
            return None

        # For now, just return a random legal move
        # This can be enhanced with actual chess engine logic later
        move = random.choice(legal_moves)
        
        # Convert the move to from_square and to_square format
        from_square = chess.square_name(move.from_square)
        to_square = chess.square_name(move.to_square)
        piece = self.board.piece_at(move.from_square).symbol()

        # Make the move on the internal board
        self.board.push(move)

        return {
            'status': 'success',
            'from': from_square,
            'to': to_square,
            'piece': piece,
            'game_state': self.board.fen(),
            'is_checkmate': self.board.is_checkmate(),
            'is_check': self.board.is_check(),
            'is_stalemate': self.board.is_stalemate(),
            'is_insufficient_material': self.board.is_insufficient_material(),
            'current_turn': 'black' if self.board.turn == chess.BLACK else 'white'
        }