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
    'castling': [1, 1, 1, 1],
    'en_passant': None
}

def get_piece_at(board_state, square):
    return board_state['board'][8*(int(square[1])-1) + ord(square[0]) - ord('a')]

def legal_moves(board_state):
    legal_pieces = []
    legal_moves = []

    # select all white / all black pieces
    for pos, piece in enumerate(board_state['board']):
        if piece % 2 == board_state['turn'] and piece!=0:
            legal_pieces.append((pos, piece))

    valid = lambda r, c: c>=0 and c<=7 and r>=0 and r<=7
    index = lambda r, c: 8*r+c

    # standard move patterns
    for piece in legal_pieces:
        row = piece[0] // 8
        col = piece[0] % 8

        # king
        if piece[1] == PieceTypes.BLACK_KING.value or piece[1] == PieceTypes.WHITE_KING.value:
            for i in range(-1,2):
                for j in range(-1,2):
                    if valid(row+i, col+j) and (board_state['board'][index(row+i, col+j)] == 0 or (board_state['board'][index(row+i, col+j)] - piece[1]) % 2 == 1):
                        legal_moves.append((piece[0], index(row+i, col+j)))               

        # queen
        if piece[1] == PieceTypes.BLACK_QUEEN.value or piece[1] == PieceTypes.WHITE_QUEEN.value:
            for i in range(-1,2):
                for j in range(-1,2):
                    k = 1
                    while valid(row+i*k, col+j*k) and board_state['board'][index(row+i*k, col+j*k)] == 0:
                        legal_moves.append((piece[0], index(row+i*k, col+j*k)))
                        k+=1
                    if valid(row+i*k, col+j*k) and (board_state['board'][index(row+i*k, col+j*k)] - piece[1]) % 2 == 1:
                        legal_moves.append((piece[0], index(row+i*k, col+j*k)))

        # rook
        if piece[1] == PieceTypes.BLACK_ROOK.value or piece[1] == PieceTypes.WHITE_ROOK.value:
            for i in range(2):
                for j in range(-1,2):
                    k = 1
                    while valid(row+j*k*i, col+j*k*(1-i)) and board_state['board'][index(row+j*k*i, col+j*k*(1-i))] == 0:
                        legal_moves.append((piece[0], index(row+j*k*i, col+j*k*(1-i))))
                        k+=1
                    if valid(row+j*k*i, col+j*k*(1-i)) and (board_state['board'][index(row+j*k*i, col+j*k*(1-i))] - piece[1]) % 2 == 1:
                        legal_moves.append((piece[0], index(row+j*k*i, col+j*k*(1-i))))

        # bishop
        if piece[1] == PieceTypes.BLACK_BISHOP.value or piece[1] == PieceTypes.WHITE_BISHOP.value:
            for i in [-1,1]:
                for j in [-1,1]:
                    k = 1
                    while valid(row+i*k, col+j*k) and board_state['board'][index(row+i*k, col+j*k)] == 0:
                        legal_moves.append((piece[0], index(row+i*k, col+j*k)))
                        k+=1
                    if valid(row+i*k, col+j*k) and (board_state['board'][index(row+i*k, col+j*k)] - piece[1]) % 2 == 1:
                        legal_moves.append((piece[0], index(row+i*k, col+j*k)))

        # knight
        if piece[1] == PieceTypes.BLACK_KNIGHT.value or piece[1] == PieceTypes.WHITE_KNIGHT.value:
            for i in [-2, -1, 1, 2]:
                for j in [-1, 1]:
                    if valid(row+i, col+j*(3-abs(i))) and (board_state['board'][index(row+i, col+j*(3-abs(i)))] == 0 or (board_state['board'][index(row+i, col+j*(3-abs(i)))] - piece[1]) % 2 == 1):
                        legal_moves.append((piece[0], index(row+i, col+j*(3-abs(i))))) 

        # white pawn
        if piece[1] == PieceTypes.WHITE_PAWN.value:
            if row == 1 and board_state['board'][index(row+1, col)] == 0 and board_state['board'][index(row+2, col)] == 0:
                legal_moves.append((piece[0], index(row+2, col)))
            if valid(row+1, col) and board_state['board'][index(row+1, col)] == 0:
                legal_moves.append((piece[0], index(row+1, col)))
            if valid(row+1, col+1) and board_state['board'][index(row+1, col+1)] != 0 and (board_state['board'][index(row+1, col+1)] - piece[1]) % 2 == 1:
                legal_moves.append((piece[0], index(row+1, col+1)))
            if valid(row+1, col-1) and board_state['board'][index(row+1, col-1)] != 0 and (board_state['board'][index(row+1, col-1)] - piece[1]) % 2 == 1:
                legal_moves.append((piece[0], index(row+1, col-1)))

        # black pawn
        if piece[1] == PieceTypes.BLACK_PAWN.value:
            if row == 6 and board_state['board'][index(row-1, col)] == 0 and board_state['board'][index(row-2, col)] == 0:
                legal_moves.append((piece[0], index(row-2, col)))
            if valid(row-1, col) and board_state['board'][index(row-1, col)] == 0:
                legal_moves.append((piece[0], index(row-1, col)))
            if valid(row-1, col+1) and board_state['board'][index(row-1, col+1)] != 0 and (board_state['board'][index(row-1, col+1)] - piece[1]) % 2 == 1:
                legal_moves.append((piece[0], index(row-1, col+1)))
            if valid(row-1, col-1) and board_state['board'][index(row-1, col-1)] != 0 and (board_state['board'][index(row-1, col-1)] - piece[1]) % 2 == 1:
                legal_moves.append((piece[0], index(row-1, col-1)))

    # castling 
    #TODO

    # en passant
    #TODO

    legal_moves_str = []

    # move by white can't create a check for white, move for black can't create a check for black
    for move in legal_moves:
        piece_captured = board_state['board'][move[1]]

        # simulate move
        board_state['board'][move[1]] = board_state['board'][move[0]]
        board_state['board'][move[0]] = 0

        # check?
        if board_state['turn']:
            if not check_black(board_state):
                legal_moves_str.append(chr(ord('a') + move[0]%8) + str(move[0]//8+1) + chr(ord('a') + move[1]%8) + str(move[1]//8+1))
        else:
            if not check_white(board_state):
                legal_moves_str.append(chr(ord('a') + move[0]%8) + str(move[0]//8+1) + chr(ord('a') + move[1]%8) + str(move[1]//8+1))

        # move the piece back
        board_state['board'][move[0]] = board_state['board'][move[1]]
        board_state['board'][move[1]] = piece_captured
    
    return legal_moves_str


def make_move(board_state, sq_from, sq_to):
    index_from = 8*(int(sq_from[1])-1) + ord(sq_from[0]) - ord('a')
    index_to = 8*(int(sq_to[1])-1) + ord(sq_to[0]) - ord('a')
    
    piece_moved = board_state['board'][index_from]
    piece_captured = board_state['board'][index_to]

    # castling move rook
    if piece_moved == PieceTypes.WHITE_KING.value and sq_from == 'e1' and sq_to == 'g1':
        board_state['board'][5] = PieceTypes.WHITE_ROOK.value
        board_state['board'][7] = 0
    if piece_moved == PieceTypes.WHITE_KING.value and sq_from == 'e1' and sq_to == 'c1':
        board_state['board'][3] = PieceTypes.WHITE_ROOK.value
        board_state['board'][0] = 0
    if piece_moved == PieceTypes.WHITE_KING.value and sq_from == 'e8' and sq_to == 'g8':
        board_state['board'][61] = PieceTypes.WHITE_ROOK.value
        board_state['board'][63] = 0
    if piece_moved == PieceTypes.WHITE_KING.value and sq_from == 'e8' and sq_to == 'c8':
        board_state['board'][59] = PieceTypes.WHITE_ROOK.value
        board_state['board'][56] = 0

    # castling
    if piece_moved == PieceTypes.WHITE_KING.value:
        board_state['castling'][0], board_state['castling'][1] = 0, 0
    if piece_moved == PieceTypes.WHITE_ROOK.value and sq_from == 'a1':
        board_state['castling'][0] = 0
    if piece_moved == PieceTypes.WHITE_ROOK.value and sq_from == 'a8':
        board_state['castling'][1] = 0
    if piece_moved == PieceTypes.BLACK_KING.value:
        board_state['castling'][2], board_state['castling'][3] = 0, 0
    if piece_moved == PieceTypes.BLACK_ROOK.value and sq_from == 'h1':
        board_state['castling'][2] = 0
    if piece_moved == PieceTypes.BLACK_ROOK.value and sq_from == 'h8':
        board_state['castling'][3] = 0

    # en passant remove pawn
    if piece_moved == PieceTypes.WHITE_PAWN.value and sq_to == board_state['en_passant']:
        board_state['board'][index_to - 8] = 0
    if piece_moved == PieceTypes.BLACK_PAWN.value and sq_to == board_state['en_passant']:
        board_state['board'][index_to + 8] = 0

    # en passant
    if piece_moved == PieceTypes.WHITE_PAWN.value and sq_from[1] == '2' and sq_to[1] == '4':
        board_state['en_passant'] = sq_from[0] + '3'
    elif piece_moved == PieceTypes.BLACK_PAWN.value and sq_from[1] == '7' and sq_to[1] == '5':
        board_state['en_passant'] = sq_from[0] + '6'
    else:
        board_state['en_passant'] = None

    # change turn
    board_state['turn'] = 1 - board_state['turn']

    # move piece on the board
    board_state['board'][index_to] = board_state['board'][index_from]
    board_state['board'][index_from] = 0

    # promotion
    if piece_moved == PieceTypes.WHITE_PAWN.value and sq_to[1] == '8':
        board_state['board'][index_to] = PieceTypes.WHITE_QUEEN.value
    if piece_moved == PieceTypes.BLACK_PAWN.value and sq_to[1] == '1':
        board_state['board'][index_to] = PieceTypes.BLACK_QUEEN.value
        
def check_white(board_state):
    pos_king = board_state['board'].index(PieceTypes.WHITE_KING.value)

    valid = lambda r, c: c>=0 and c<=7 and r>=0 and r<=7
    index = lambda r, c: 8*r+c

    row = pos_king // 8
    col = pos_king % 8

    # pawns
    if valid(row+1, col+1) and board_state['board'][index(row+1, col+1)] == PieceTypes.BLACK_PAWN.value:
        return True
    if valid(row+1, col-1) and board_state['board'][index(row+1, col-1)] == PieceTypes.BLACK_PAWN.value:
        return True

    # king
    for i in range(-1,2):
        for j in range(-1,2):
            if valid(row+i, col+j) and board_state['board'][index(row+i, col+j)] == PieceTypes.BLACK_KING.value:
                return True

    # knights
    for i in [-2, -1, 1, 2]:
        for j in [-1, 1]:
            if valid(row+i, col+j*(3-abs(i))) and board_state['board'][index(row+i, col+j*(3-abs(i)))] == PieceTypes.BLACK_KNIGHT.value:
                return True

    # cardinal directions
    for i in range(2):
        for j in range(-1,2):
            k = 1
            while valid(row+j*k*i, col+j*k*(1-i)) and board_state['board'][index(row+j*k*i, col+j*k*(1-i))] == 0:
                k+=1
            if valid(row+j*k*i, col+j*k*(1-i)) and (board_state['board'][index(row+j*k*i, col+j*k*(1-i))] == PieceTypes.BLACK_ROOK.value or board_state['board'][index(row+j*k*i, col+j*k*(1-i))] == PieceTypes.BLACK_QUEEN.value):
                return True       

    # ordinal directions
    for i in [-1, 1]:
        for j in [-1, 1]:
            k = 1
            while valid(row+i*k, col+j*k) and board_state['board'][index(row+i*k, col+j*k)] == 0:
                k+=1
            if valid(row+i*k, col+j*k) and (board_state['board'][index(row+i*k, col+j*k)] == PieceTypes.BLACK_BISHOP.value or board_state['board'][index(row+i*k, col+j*k)] == PieceTypes.BLACK_QUEEN.value):
                return True

    return False

def mate_white(board_state):
    return check_white(board_state) and len(legal_moves(board_state))==0

def check_black(board_state):
    pos_king = board_state['board'].index(PieceTypes.BLACK_KING.value)

    valid = lambda r, c: c>=0 and c<=7 and r>=0 and r<=7
    index = lambda r, c: 8*r+c

    row = pos_king // 8
    col = pos_king % 8

    # pawns
    if valid(row-1, col+1) and board_state['board'][index(row-1, col+1)] == PieceTypes.WHITE_PAWN.value:
        return True
    if valid(row-1, col-1) and board_state['board'][index(row-1, col-1)] == PieceTypes.WHITE_PAWN.value:
        return True

    # king
    for i in range(-1,2):
        for j in range(-1,2):
            if valid(row+i, col+j) and board_state['board'][index(row+i, col+j)] == PieceTypes.WHITE_KING.value:
                return True

    # knights
    for i in [-2, -1, 1, 2]:
        for j in [-1, 1]:
            if valid(row+i, col+j*(3-abs(i))) and board_state['board'][index(row+i, col+j*(3-abs(i)))] == PieceTypes.WHITE_KNIGHT.value:
                return True

    # cardinal directions
    for i in range(2):
        for j in range(-1,2):
            k = 1
            while valid(row+j*k*i, col+j*k*(1-i)) and board_state['board'][index(row+j*k*i, col+j*k*(1-i))] == 0:
                k+=1
            if valid(row+j*k*i, col+j*k*(1-i)) and (board_state['board'][index(row+j*k*i, col+j*k*(1-i))] == PieceTypes.WHITE_ROOK.value or board_state['board'][index(row+j*k*i, col+j*k*(1-i))] == PieceTypes.WHITE_QUEEN.value):
                return True       

    # ordinal directions
    for i in [-1, 1]:
        for j in [-1, 1]:
            k = 1
            while valid(row+i*k, col+j*k) and board_state['board'][index(row+i*k, col+j*k)] == 0:
                k+=1
            if valid(row+i*k, col+j*k) and (board_state['board'][index(row+i*k, col+j*k)] == PieceTypes.WHITE_BISHOP.value or board_state['board'][index(row+i*k, col+j*k)] == PieceTypes.WHITE_QUEEN.value):
                return True

    return False

def mate_black(board_state):
    return check_black(board_state) and len(legal_moves(board_state))==0