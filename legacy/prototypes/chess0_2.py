import pygame
pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)  
width = screen.get_width()
height = screen.get_height()

board_size=height-60
board_start_pt=30 
square_size=board_size/8

font = pygame.font.Font('freesansbold.ttf', 20)
smallfont = pygame.font.Font('freesansbold.ttf', 35)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60

sq_size=(board_size)/8
p_size=sq_size-17
white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
captured_pieces_white = []
captured_pieces_black = []

# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = 100
valid_moves = []

b_k=pygame.image.load('images/black_k.png')
b_n=pygame.image.load('images/black_n.png')
b_p=pygame.image.load('images/black_p.png')
b_b=pygame.image.load('images/black_b.png')
b_q=pygame.image.load('images/black_q.png')
b_r=pygame.image.load('images/black_r.png')

w_k=pygame.image.load('images/white_k.png')
w_n=pygame.image.load('images/white_n.png')
w_p=pygame.image.load('images/white_p.png')
w_b=pygame.image.load('images/white_b.png')
w_q=pygame.image.load('images/white_q.png')
w_r=pygame.image.load('images/white_r.png')

b_p=pygame.transform.scale(b_p,(p_size,p_size))
b_k=pygame.transform.scale(b_k,(p_size,p_size))
b_n=pygame.transform.scale(b_n,(p_size,p_size))
b_b=pygame.transform.scale(b_b,(p_size,p_size))
b_q=pygame.transform.scale(b_q,(p_size,p_size))
b_r=pygame.transform.scale(b_r,(p_size,p_size))

w_p=pygame.transform.scale(w_p,(p_size,p_size))
w_k=pygame.transform.scale(w_k,(p_size,p_size))
w_n=pygame.transform.scale(w_n,(p_size,p_size))
w_b=pygame.transform.scale(w_b,(p_size,p_size))
w_q=pygame.transform.scale(w_q,(p_size,p_size))
w_r=pygame.transform.scale(w_r,(p_size,p_size))

white_images = [w_p,w_q,w_k,w_n,w_r,w_b]
white_promotions = ['bishop', 'knight', 'rook', 'queen']
white_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]
black_images = [b_p,b_q,b_k,b_n,b_r,b_b]
black_promotions = ['bishop', 'knight', 'rook', 'queen']
black_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

# check variables/ flashing counter
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

def chess_canvas():
    pygame.draw.rect(screen, "white", pygame.Rect(board_start_pt,board_start_pt, board_size, board_size))
    light_color=pygame.Color(255,255,255)
    dark_color=pygame.Color(100,100,100)
    bor_color=pygame.Color("silver")
    pygame.draw.rect(screen, bor_color, [board_start_pt-5,board_start_pt-5,board_size+10,board_size+10],5)
    for col in range(8):
        for row in range(8):
            # print(board_start_pt+(row*square_size),board_start_pt+(col*square_size))
            if((row%2==0 and col%2==0) or (row%2!=0 and col%2!=0)):
                pygame.draw.rect(screen, dark_color, [board_start_pt+(row*square_size),board_start_pt+(col*square_size), square_size,square_size])
            else:
                pygame.draw.rect(screen, light_color, [board_start_pt+(row*square_size)+(col*square_size),board_start_pt+(row*square_size)+(col*square_size), square_size,square_size])
                
   
def set_pieces():
  
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(w_p, (white_locations[i][0] * square_size +36, white_locations[i][1] * square_size +40))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * square_size + 37, white_locations[i][1] * square_size + 40))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * square_size +31, white_locations[i][1] * square_size +31,
                                                 square_size+1, square_size+1], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(b_p, (black_locations[i][0] * square_size+36, black_locations[i][1] * square_size + 40))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * square_size+37, black_locations[i][1] * square_size+40))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * square_size + 31, black_locations[i][1] * square_size + 31,
                                                  square_size+1, square_size+1], 2)    

# function to check all pieces valid options on board
def check_options(pieces, locations, turn):
    global castling_moves
    moves_list = []
    all_moves_list = []
    castling_moves = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list, castling_moves = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list

# check king valid moves
def check_king(position, color):
    moves_list = []
    castle_moves = check_castling()
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for kings, they can go one square any direction
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (int(position[0] + targets[i][0]), int(position[1] + targets[i][1]))
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7 :
            moves_list.append(target)
    return moves_list, castle_moves


# check queen valid moves
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list


# check bishop moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((int(position[0] + (chain * x)), int(position[1] + (chain * y))))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check rook moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((int(position[0] + (chain * x)), int(position[1] + (chain * y))))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check valid pawn moves
def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] < 7:
            moves_list.append((int(position[0]), int(position[1] - 1)))
            # indent the check for two spaces ahead, so it is only checked if one space ahead is also open
            if (position[0], position[1] - 2) not in white_locations and \
                    (position[0], position[1] - 2) not in black_locations and position[1] == 6:
                moves_list.append((int(position[0]), int(position[1] - 2)))
        if (position[0] + 1, position[1] - 1) in black_locations:
            moves_list.append((int(position[0] + 1), int(position[1] - 1)))
        if (position[0] - 1, position[1] - 1) in black_locations:
            moves_list.append((int(position[0] - 1), int(position[1] - 1)))
        # add en passant move checker
        if (position[0] + 1, position[1] -1) == black_ep:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) == black_ep:
            moves_list.append((position[0] - 1, position[1] - 1))
    else:
        if (position[0], position[1]+ 1) not in white_locations and \
                (position[0], position[1]+ 1) not in black_locations and position[1] > 0:
            moves_list.append((int(position[0]), int(position[1]+ 1)))
            # indent the check for two spaces ahead, so it is only checked if one space ahead is also open
            if (position[0], position[1]+ 2) not in white_locations and \
                    (position[0], position[1]+ 2) not in black_locations and position[1] == 1:
                moves_list.append((int(position[0]), int(position[1]+ 2)))
        if (position[0] + 1, position[1]+ 1) in white_locations:
            moves_list.append((int(position[0] + 1), int(position[1]+ 1)))
        if (position[0] - 1, position[1]+ 1) in white_locations:
            moves_list.append((int(position[0] - 1), int(position[1]+ 1)))
        # add en passant move checker
        if (position[0] + 1, position[1]+ 1) == white_ep:
            moves_list.append((position[0] + 1, position[1]+ 1))
        if (position[0] - 1, position[1]+ 1) == white_ep:
            moves_list.append((position[0] - 1, position[1]+ 1))
    return moves_list


# check valid knight moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (int(position[0] + targets[i][0]), int(position[1] + targets[i][1]))
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# check for valid moves for just selected piece
def check_valid_moves():
    main_list=[]
    if turn_step < 2:
        options_list = white_options
        for a in range(len(options_list)):
            print("kuch")
            print(a)
            valid_options = options_list[a]
            print("valid options white:")
            print(valid_options)
            for i in range(len(valid_options)-1,-1,-1):
                original_loc = white_locations[a]
                print("white locations before update:")
                print(white_locations)
                white_locations[a] = valid_options[i]
                print("white locations after update:")
                print(white_locations)
                if in_check('white',valid_options[i]):
                    valid_options.remove(valid_options[i])
                white_locations[selection] = original_loc
                main_list.append(valid_options)
                
                if len(valid_options) ==0 :
                    winner = 'black'
        print("yele")
        print(main_list)
                    
    # if turn_step < 2:
    #     options_list = white_options
       
    #     valid_options = options_list[selection]
    #     print("valid options white:")
    #     print(valid_options)
    #     for i in range(len(valid_options)-1,-1,-1):
    #         original_loc = white_locations[selection]
    #         print("white locations before update:")
    #         print(white_locations)
    #         white_locations[selection] = valid_options[i]
    #         print("white locations after update:")
    #         print(white_locations)
    #         if in_check('white',valid_options[i]):
    #             valid_options.remove(valid_options[i])
    #         white_locations[selection] = original_loc
    #         if len(valid_options) ==0 :
    #             winner = 'black'

    else:
        options_list = black_options
        valid_options = options_list[selection]
        print("valid options black:")
        print(valid_options)
        for i in range(len(valid_options)-1,-1,-1):
            original_loc = black_locations[selection]
            print("black locations before update:")
            print(black_locations)
            black_locations[selection] = valid_options[i]
            print("black locations after update:")
            print(black_locations)
            if in_check('black',valid_options[i]):
                valid_options.remove(valid_options[i])
            black_locations[selection] = original_loc
            if len(valid_options) ==0 :
                winner = 'white'
    return valid_options

def in_check(color,moved_pos):
    global check_w
    global check_b
    check_w=False
    check_b=False
    
    
    if(color =='white'):
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            print("white king location:" )
            print(king_location)
            
            black_options_dummy = check_options(black_pieces,black_locations,'black')
            if(moved_pos in black_locations):
                del_ind = black_locations.index(moved_pos)
                black_options_dummy[del_ind] = []

            print("dummy_moves:")
            print(black_options_dummy)
            for black_option in black_options_dummy:
                    if king_location in black_option:
                        check_w = True
                        return True
                    
                        
    if(color =='black'):
        if 'king' in black_pieces:
                king_index = black_pieces.index('king')
                king_location = black_locations[king_index]
                print("black king location: ")
                print(king_location)
                white_options_dummy = check_options(white_pieces,white_locations,'white')
                if(moved_pos in white_locations):
                    del_ind = white_locations.index(moved_pos)
                    white_options_dummy[del_ind] = []
                print("dummy_moves:")
                print(white_options_dummy)
                for white_option in white_options_dummy:
                    if king_location in white_option:
                        check_b = True
                        return True
                    
                        

# draw valid moves on screen
def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * square_size + 50, moves[i][1] * square_size + 50), 5)


# # draw captured pieces on side of screen
# def draw_captured():
#     for i in range(len(captured_pieces_white)):
#         captured_piece = captured_pieces_white[i]
#         index = piece_list.index(captured_piece)
#         screen.blit(small_black_images[index], (825, 5 + 50 * i))
#     for i in range(len(captured_pieces_black)):
#         captured_piece = captured_pieces_black[i]
#         index = piece_list.index(captured_piece)
#         screen.blit(small_white_images[index], (925, 5 + 50 * i))


# draw a flashing square around king if in check
def draw_check():
    
    global check_w
    global check_b
    check_w=False
    check_b=False
    
    
    # if turn_step < 2:
    if 'king' in white_pieces:
        king_index = white_pieces.index('king')
        king_location = white_locations[king_index]
        for i in range(len(black_options)):
                if king_location in black_options[i]:
                    check_w = True
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * square_size + 31,
                                                              white_locations[king_index][1] * square_size + 31, square_size, square_size], 5)
    
    if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    check_b = True
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * square_size+31,
                                                               black_locations[king_index][1] * square_size + 31, square_size, square_size], 5)



# add castling
def check_castling():
    # king must not currently be in check, neither the rook nor king has moved previously, nothing between
    # and the king does not pass through or finish on an attacked piece
    castle_moves = []  # store each valid castle move as [((king_coords), (castle_coords))]
    rook_indexes = []
    rook_locations = []
    king_index = 0
    king_pos = (0, 0)
    if turn_step > 1:
        for i in range(len(white_pieces)):
            # print("white")
            if white_pieces[i] == 'rook':
                rook_indexes.append(white_moved[i])
                rook_locations.append(white_locations[i])
                # print(rook_indexes)
            if white_pieces[i] == 'king':
                king_index = i
                king_pos = white_locations[i]
        if not white_moved[king_index] and False in rook_indexes and not check_w:
            for i in range(len(rook_indexes)):
                castle = True
                # print(rook_locations[i][0] ,king_pos[0], king_pos[1])
                if rook_locations[i][0] < king_pos[0]:
                    
                    empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1]),
                                     (king_pos[0] - 3, king_pos[1])]
                else:
                    empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1])]
                for j in range(len(empty_squares)):
                    if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                            empty_squares[j] in black_options or rook_indexes[i]:
                        castle = False
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    else:
        for i in range(len(black_pieces)):
            # print("black")
            if black_pieces[i] == 'rook':
                rook_indexes.append(black_moved[i])
                rook_locations.append(black_locations[i])
            if black_pieces[i] == 'king':
                king_index = i
                king_pos = black_locations[i]
        if not black_moved[king_index] and False in rook_indexes and not check_b:
            for i in range(len(rook_indexes)):
                # print(rook_locations[i][0] ,king_pos[0], king_pos[1])
                castle = True
                if rook_locations[i][0] < king_pos[0]:
                    empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1]),
                                     (king_pos[0] - 3, king_pos[1])]
                else:
                    empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1])]
                for j in range(len(empty_squares)):
                    if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                            empty_squares[j] in white_options or rook_indexes[i]:
                        castle = False
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    return castle_moves

def draw_castling(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0][0] * 100 + 50, moves[i][0][1] * 100 + 70), 8)
        screen.blit(font.render('king', True, 'black'), (moves[i][0][0] * 100 + 30, moves[i][0][1] * 100 + 70))
        pygame.draw.circle(screen, color, (moves[i][1][0] * 100 + 50, moves[i][1][1] * 100 + 70), 8)
        screen.blit(font.render('rook', True, 'black'),
                    (moves[i][1][0] * 100 + 30, moves[i][1][1] * 100 + 70))
        pygame.draw.line(screen, color, (moves[i][0][0] * 100 + 50, moves[i][0][1] * 100 + 70),
                         (moves[i][1][0] * 100 + 50, moves[i][1][1] * 100 + 70), 2)



# add pawn promotion
def check_promotion():
    pawn_indexes = []
    white_promotion = False
    black_promotion = False
    promote_index = 100
    for i in range(len(white_pieces)):
        if white_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if white_locations[pawn_indexes[i]][1] == 0:
            white_promotion = True
            promote_index = pawn_indexes[i]
    pawn_indexes = []
    for i in range(len(black_pieces)):
        if black_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if black_locations[pawn_indexes[i]][1] == 7:
            black_promotion = True
            promote_index = pawn_indexes[i]
    return white_promotion, black_promotion, promote_index


def draw_promotion():
    pygame.draw.rect(screen, 'dark gray', [800, 0, 200, 420])
    if white_promote:
        color = 'white'
        for i in range(len(white_promotions)):
            piece = white_promotions[i]
            index = piece_list.index(piece)
            screen.blit(white_images[index], (860, 5 + 100 * i))
    elif black_promote:
        color = 'black'
        for i in range(len(black_promotions)):
            piece = black_promotions[i]
            index = piece_list.index(piece)
            screen.blit(black_images[index], (860, 5 + 100 * i))
    pygame.draw.rect(screen, color, [800, 0, 200, 420], 8)


def check_promo_select():
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    x_pos = mouse_pos[0] // 100
    y_pos = mouse_pos[1] // 100
    if white_promote and left_click and x_pos > 7 and y_pos < 4:
        white_pieces[promo_index] = white_promotions[y_pos]
    elif black_promote and left_click and x_pos > 7 and y_pos < 4:
        black_pieces[promo_index] = black_promotions[y_pos]


#dice
import time
import random

pawn_1=pygame.image.load('images/dice and frame/PAWN.png')
king_2=pygame.image.load('images/dice and frame/KING.png')
bishop_3=pygame.image.load('images/dice and frame/BISHOP.png')
knight_4=pygame.image.load('images/dice and frame/KNIGHT.png')
rook_5=pygame.image.load('images/dice and frame/ROOK.png')
queen_6=pygame.image.load('images/dice and frame/QUEEN.png')
cor_1=pygame.image.load('images/dice and frame/cor1.png')
cor_2=pygame.image.load('images/dice and frame/cor2.png')
cor_3=pygame.image.load('images/dice and frame/cor3.png')
cor_4=pygame.image.load('images/dice and frame/cor4.png')

pawn_1=pygame.transform.scale(pawn_1,(300,300))
king_2=pygame.transform.scale(king_2,(300,300))
bishop_3=pygame.transform.scale(bishop_3,(300,300))
knight_4=pygame.transform.scale(knight_4,(300,300))
rook_5=pygame.transform.scale(rook_5,(300,300))
queen_6=pygame.transform.scale(queen_6,(300,300))
cor_1=pygame.transform.scale(cor_1,(300,300))
cor_2=pygame.transform.scale(cor_2,(300,300))
cor_3=pygame.transform.scale(cor_3,(300,300))
cor_4=pygame.transform.scale(cor_4,(300,300))
frame=[cor_1,cor_2,cor_3,cor_4]
roll_num=3


def dice_show(roll_num):        
    
    pygame.draw.rect(screen,'grey',pygame.Rect(width-490,height/2-115,270,238))
    screen.blit(pawn_1,(width-500,height/2-150))
    if roll_num==1:
        screen.blit(pawn_1,(width-500,height/2-150))
        # print(roll_num)
    if roll_num==2:
        # print(roll_num)
        screen.blit(king_2,(width-500,height/2-150))
    if roll_num==3:
        # print(roll_num)
        screen.blit(bishop_3,(width-500,height/2-150))
    if roll_num==4:
        # print(roll_num)
        screen.blit(knight_4,(width-500,height/2-150))
    if roll_num==5:
        # print(roll_num)
        screen.blit(rook_5,(width-500,height/2-150))
    if roll_num==6:
        # print(roll_num)
        screen.blit(queen_6,(width-500,height/2-150))
    

def dice_roll():
    global roll_num
    global frame
    # for frame in frame:
    #     screen.blit(frame,(width-500,height/2-150) )

    
    # pygame.draw.rect(screen, "red", pygame.Rect(900,500,20,50))
    print("rolling")
    #print(roll_num)
    screen.blit(cor_1,(width-500,height/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(screen,'grey',pygame.Rect(width-490,height/2-115,270,238))
    pygame.display.update()
    screen.blit(cor_2,(width-500,height/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(screen,'grey',pygame.Rect(width-490,height/2-115,270,238))
    pygame.display.update()
    screen.blit(cor_3,(width-500,height/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(screen,'grey',pygame.Rect(width-490,height/2-115,270,238))
    pygame.display.update()
    screen.blit(cor_4,(width-500,height/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(screen,'grey',pygame.Rect(width-490,height/2-115,270,238))
    pygame.display.update()
    screen.blit(cor_1,(width-500,height/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(screen,'grey',pygame.Rect(width-490,height/2-115,270,238))
    pygame.display.update()
    screen.blit(cor_2,(width-500,height/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(screen,'grey',pygame.Rect(width-490,height/2-115,270,238))
    pygame.display.update()
    screen.blit(cor_3,(width-500,height/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(screen,'grey',pygame.Rect(width-490,height/2-115,270,238))
    pygame.display.update()
    screen.blit(cor_4,(width-500,height/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(screen,'grey',pygame.Rect(width-490,height/2-115,270,238))
    pygame.display.update()
    roll_num=random.randint( 1,6 )
    dice_show(roll_num)



#main loop
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')

run = True
while run:
    
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    back_ground_color=pygame.Color(0,0,0)
    screen.fill(back_ground_color)
    chess_canvas()
    set_pieces()
    draw_check()
    
    
        #dice part
    dice_show(roll_num)
       
    mouse = pygame.mouse.get_pos()
    if width-415 <= mouse[0] <= width-295 and (height/2)+120 <= mouse[1] <= (height/2)+180:
        roll_p1=smallfont.render('Roll',True,'green')
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        roll_p1=smallfont.render('Roll',True,'white')
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    if width-415 <= mouse[0] <= width-295 and (height/2)-180 <= mouse[1] <= (height/2)-120:
        roll_p2=smallfont.render('Roll',True,'green')
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        roll_p2=smallfont.render('Roll',True,'white')
    screen.blit(roll_p1 , (width-390,height/2+126))
    screen.blit(roll_p2 , (width-390,height/2-166))
    
    
    #normal
    if not game_over:
        white_promote, black_promote, promo_index = check_promotion()
        if white_promote or black_promote:
            draw_promotion()
            check_promo_select()
    if selection != 100:
        # valid_moves = check_valid_moves()
        # valid_moves=all_val_try()
        draw_valid(valid_moves)
        if selected_piece == 'king':
            draw_castling(castling_moves)
    # event handling
    for event in pygame.event.get():
  
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            # print(event.pos[0],event.pos[1])
            #dice again
            if width-415 <= mouse[0] <= width-295 and height/2+120 <= mouse[1] <= height/2+180:
                dice_roll()
            if width-415 <= mouse[0] <= width-295 and (height/2)-180 <= mouse[1] <= (height/2)-120:
                dice_roll()
            #normal
            x_coord = (event.pos[0] -30)// square_size
            y_coord = (event.pos[1]-30) // square_size
            click_coords = (int(x_coord), int(y_coord)) 
            # print(click_coords)
            if turn_step <= 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'black'
       
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    valid_moves = check_valid_moves()
                    # check what piece is selected, so you can only draw castling moves if king is selected
                    selected_piece = white_pieces[selection]
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in valid_moves and selection != 100:
                    # white_ep = check_ep(white_locations[selection], click_coords)
                    white_locations[selection] = click_coords
                    white_moved[selection] = True
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                        black_moved.pop(black_piece)
                    # adding check if en passant pawn was captured
                    if click_coords == black_ep:
                        black_piece = black_locations.index((black_ep[0], black_ep[1]+ 1))
                        captured_pieces_white.append(black_pieces[black_piece])
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                        black_moved.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []
                # add option to castle
                elif selection != 100 and selected_piece == 'king':
                    # print(castling_moves)
                    for q in range(len(castling_moves)):
                        if click_coords == castling_moves[q][0]:
                            # print("hereW",castling_moves[q][0])
                            white_locations[selection] = click_coords
                            white_moved[selection] = True
                            if click_coords == (2, 7):
                                rook_coords = (0, 7)
                            else:
                                rook_coords = (7, 7)
                            rook_index = white_locations.index(rook_coords)
                            white_locations[rook_index] = castling_moves[q][1]
                            black_options = check_options(black_pieces, black_locations, 'black')
                            white_options = check_options(white_pieces, white_locations, 'white')
                            turn_step = 2
                            selection = 100
                            valid_moves = []
            if turn_step > 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'white'
                
            
                    
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    valid_moves = check_valid_moves()
                    # check what piece is selected, so you can only draw castling moves if king is selected
                    selected_piece = black_pieces[selection]
                    if turn_step == 2:
                        turn_step = 3
                if click_coords in valid_moves and selection != 100:
                    # black_ep = check_ep(black_locations[selection], click_coords)
                    black_locations[selection] = click_coords
                    black_moved[selection] = True
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                        white_moved.pop(white_piece)
                    if click_coords == white_ep:
                        white_piece = white_locations.index((white_ep[0], white_ep[1] + 1))
                        captured_pieces_black.append(white_pieces[white_piece])
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                        white_moved.pop(white_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
                # add option to castle
                elif selection != 100 and selected_piece == 'king':
                    # print(castling_moves)
                    for q in range(len(castling_moves)):
                        if click_coords == castling_moves[q][0]:
                            # print("hereB",castling_moves[q][0])
                            black_locations[selection] = click_coords
                            black_moved[selection] = True
                            
                            if click_coords == (2, 0):
                                rook_coords = (0, 0)
                            else:
                                rook_coords = (7, 0)
                            rook_index = black_locations.index(rook_coords)
                            black_locations[rook_index] = castling_moves[q][1]
                            black_options = check_options(black_pieces, black_locations, 'black')
                            white_options = check_options(white_pieces, white_locations, 'white')
                            turn_step = 0
                            selection = 100
                            valid_moves = []
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(0, 7), (1, 7), (2, 7), (4, 7), (3, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                white_moved = [False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False]
                black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0, 0), (1, 0), (2, 0), (4, 0), (3, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                black_moved = [False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')

    if winner != '':
        game_over = True
        # draw_game_over()

    
    pygame.display.flip()
pygame.quit()
 