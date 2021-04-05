from enum import Enum, auto

class PieceTypes(Enum):
    EMPTY = 0
    BLACK_KING = auto() #1
    WHITE_KING = auto() #2
    BLACK_QUEEN = auto() #3
    WHITE_QUEEN = auto() #4
    BLACK_ROOK = auto() #5
    WHITE_ROOK = auto() #6
    BLACK_BISHOP = auto() #7
    WHITE_BISHOP = auto() #8
    BLACK_KNIGHT = auto() #9 
    WHITE_KNIGHT = auto() #10
    BLACK_PAWN = auto() #11
    WHITE_PAWN = auto() #12

    sprites = ['', 'black/king.png', 'white/king.png',
                   'black/queen.png', 'white/queen.png',
                   'black/rook.png', 'white/rook.png',
                   'black/bishop.png', 'white/bishop.png',
                   'black/knight.png', 'white/knight.png',
                   'black/pawn.png', 'white/pawn.png']

starting_board_state = {
    'board': [6, 10, 8, 4, 2, 8, 10, 6,
              12, 12, 12, 12, 12, 12, 12, 12,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              11, 11, 11, 11, 11, 11, 11, 11,
              5, 9, 7, 3, 1, 7, 9, 5],
    'turn': 0,
    'castling': 15,
    'en_passant': None
}

def legal_moves(board_state):
    legal_pieces = []
    legal_moves = []

    for pos, piece in enumerate(board_state['board']):
        if piece % 2 == board_state['turn'] and piece!=0:
            legal_pieces.append((pos, piece))
    
    for piece in legal_pieces:
        if piece[1] == PieceTypes.BLACK_KING.value or piece[1] == PieceTypes.WHITE_KING.value:
            pass


def make_move(board_state, sq_from, sq_to):
    pass

def check_white(board_state):
    pass

def mate_white(board_state):
    return check_white(board_state) and len(legal_moves(board_state))==0

def check_white(board_state):
    pass

def mate_black(board_state):
    return check_black(board_state) and len(legal_moves(board_state))==0