from chess_player import ChessPlayer
from copy import deepcopy
import random

class jcottrel_ChessPlayer(ChessPlayer):

    def __init__(self, board, color):
        super().__init__(board, color)
        self.moves = 0

    # Returns the difference of material scores between myself and the opponent
    def get_material_scores(self, board, piece_values={'p':1, 'n':3, 'b':3, 'q':8, 'k':0, 'r':5, 'y':5, 's':7, 'f':3}):
        my_material_score = 0
        opp_material_score = 0
        for piece in board.values():
            # Check piece color
            if piece.get_notation().isupper():
                piece_color = 'white'
            else:
                piece_color = 'black'
            # Calculate value
            if piece_color == self.color:
                my_material_score += piece_values[piece.get_notation().lower()]
            else:
                opp_material_score += piece_values[piece.get_notation().lower()]
        # Account for checks
        if board.is_king_in_check(self.color):
            opp_material_score += 4
        elif board.is_king_in_check(self.oppColor()):
            my_material_score += 4
        # Return difference
        return my_material_score - opp_material_score

    # Returns the opponents color
    def oppColor(self):
        if self.color == 'white':
            return 'black'
        else:
            return 'white'


    def minimax(self, board, depth, alpha, beta, my_player):
        # Termination conditions
        # Reached depth
        if depth == 0:
            return self.get_material_scores(board), None
        # Either king in checkmate
        elif board.is_king_in_checkmate(self.color):
            return float('-inf'), None
        elif board.is_king_in_checkmate(self.oppColor()):
            return float('inf'), None
        # Stalemate
        elif board.is_king_in_check(self.oppColor()) and len(board.get_all_available_legal_moves(self.oppColor())) == 0:
            return float('-inf'), None
        
        #Initialize best move
        best_move = None

        # Minimax with alpha beta pruning
        if my_player:
            my_eval = float('-inf') # Initialize eval at negative infinity
            my_legal_moves = board.get_all_available_legal_moves(self.color) # Get my moves
            for move in my_legal_moves: # Loop through moves
                new_board = deepcopy(board) # Do move
                new_board.make_move(move[0], move[1])
                # Quick check to move fast if a move is obvious
                if self.get_material_scores(new_board) > self.get_material_scores(board) + 5:
                    return self.get_material_scores(new_board), move
                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, False) # Recursively search for future possible boards
                if eval > my_eval: # If this move is better than my best move by my evaluation function
                    my_eval = eval # Update
                    best_move = move
                alpha = max(alpha, eval) # Update the alpha if necessary
                if beta <= alpha: # If this is outside of the beta range we can safely ignore it because the opponent will never choose it
                    break
            return my_eval, best_move
        else: # Same as above but opposite
            opp_eval = float('inf')
            opp_legal_moves = board.get_all_available_legal_moves(self.oppColor())
            for move in opp_legal_moves:
                new_board = deepcopy(board)
                new_board.make_move(move[0], move[1])
                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, True)
                if eval < opp_eval:
                    opp_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return opp_eval, best_move










    def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
        # Increment moves
        self.moves += 1
        # Faster sometimes to save time
        if self.moves < 7 or your_remaining_time < 100 or self.get_material_scores(self.board) > 15:
            return self.minimax(self.board, 3, float('-inf'), float('inf'), True)[1]
        else:
            return self.minimax(self.board, 4, float('-inf'), float('inf'), True)[1]