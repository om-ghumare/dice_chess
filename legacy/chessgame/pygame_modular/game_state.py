white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

white_castle_boxes=[]
black_castle_boxes=[]

captured_pieces_white = []
captured_pieces_black = []

# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0

# index of selected piece in list of pieces
selection = 100

valid_moves = []
piece_highlights_white=[]
piece_highlights_black=[]

white_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]

black_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]

roll_num = 0
counter = 0
winner = ''
game_over = False
white_ep = (100, 100)
black_ep = (100, 100)
white_promote = False
black_promote = False
promo_index = 100
check_w = False
check_b=False
castling_moves = []

black_options = []
white_options = []

white_promotions = []
black_promotions = []
dice_rolled = False
# mouse = (0,0)

def reset_game_state():
    global white_pieces
    global white_locations
    global black_pieces
    global black_locations
    global white_castle_boxes
    global black_castle_boxes
    global captured_pieces_white
    global captured_pieces_black
    global turn_step
    global selection
    global valid_moves
    global piece_highlights_white
    global piece_highlights_black
    global white_moved
    global black_moved
    global roll_num
    global winner
    global game_over
    global white_promote
    global black_promote
    global promo_index
    global check_w
    global check_b
    global castling_moves
    global black_options
    global white_options
    global white_promotions
    global black_promotions
    global dice_rolled
    # global mouse

    white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
    white_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
    black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
    black_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

    white_castle_boxes=[]
    black_castle_boxes=[]

    captured_pieces_white = []
    captured_pieces_black = []

    # 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
    turn_step = 0
    selection = 100
    valid_moves = []
    piece_highlights_white=[]
    piece_highlights_black=[]

    white_moved = [False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False]

    black_moved = [False, False, False, False, False, False, False, False,
                False, False, False, False, False, False, False, False]

    roll_num = 0
    winner = ''
    game_over = False
    white_ep = (100, 100)
    black_ep = (100, 100)
    white_promote = False
    black_promote = False
    promo_index = 100
    check_w = False
    check_b=False
    castling_moves = []
    white_castle_boxes=[]
    black_castle_boxes=[]
    white_promotions = []
    black_promotions = []
    dice_rolled = False
    # mouse = (0,0)