import pygame
import random
import time
import sys
pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)  
width = screen.get_width()
height = screen.get_height()

board_size=height-60
board_start_pt=30 
square_size=board_size/8

font = pygame.font.Font('freesansbold.ttf', 20)
small_font = pygame.font.Font('freesansbold.ttf', 30)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60

sq_size=(board_size)/8
p_size=sq_size-18
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

#dice constants
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

roll_num=0

captured_pieces_white = []
captured_pieces_black = []

# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = 100
valid_moves = []
piece_highlights_white=[]
piece_highlights_black=[]

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

button_w = 200
button_h = 60
button_x = (board_size+width+50)//2 -button_w // 2
# button_x = width // 2 - button_w // 2
button_y_exit = height// 2 - button_h // 2
button_y_rematch = button_y_exit + button_h + 20
exit_button_rect = pygame.Rect(button_x, button_y_exit, button_w, button_h)
rematch_button_rect = pygame.Rect(button_x, button_y_rematch, button_w, button_h)

rematch_button = pygame.Rect(width - 150 - 20 - 150 - 20, 20, 150, 50)
exit_button = pygame.Rect(width - 150 - 20, 20, 150, 50)


button_color=pygame.Color(	159, 132, 189)
 
roll_p1_rect = pygame.Rect(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-60, (height / 2) + 130, 120, 60)
roll_p2_rect = pygame.Rect(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-60, (height / 2) - 180, 120, 60)
yele=['pawn','pawn','knight','queen','pawn','pawn','bishop','king','king','pawn']
o=0
highlight=False

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
            screen.blit(w_p, (white_locations[i][0] * square_size +40, white_locations[i][1] * square_size +40))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * square_size + 40, white_locations[i][1] * square_size + 40))
        if turn_step < 2:
            if selection == i:
                color=pygame.Color(0,255,0,255)
                rect_surf = pygame.Surface((square_size , square_size ), pygame.SRCALPHA)
                pygame.draw.circle(rect_surf,color,(square_size//2,square_size//2),square_size//2 +square_size//4+5,30)
                radius = 25
                blurred_rect_surf = pygame.transform.box_blur(rect_surf, radius)
                screen.blit(blurred_rect_surf, (white_locations[i][0] * square_size + 30, white_locations[i][1] * square_size + 30))
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(b_p, (black_locations[i][0] * square_size+36, black_locations[i][1] * square_size + 40))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * square_size+37, black_locations[i][1] * square_size+40))
        if turn_step >= 2:
            if selection == i:
                color=pygame.Color(0,255,0,255)
                rect_surf = pygame.Surface((square_size , square_size ), pygame.SRCALPHA)
                pygame.draw.circle(rect_surf,color,(square_size//2,square_size//2),square_size//2 +square_size//4+5,30)
                radius = 25
                blurred_rect_surf = pygame.transform.box_blur(rect_surf, radius)
                screen.blit(blurred_rect_surf, (black_locations[i][0] * square_size + 30, black_locations[i][1] * square_size + 30))
 
# function to check all pieces valid options on board
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []

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
            moves_list= check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list

# check king valid moves
def check_king(position, color):
    moves_list = []
   
    # print(castle_moves)
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
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7 and target:
            moves_list.append(target)
    return moves_list


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
    check_castling()

    if turn_step < 2:
        options_list = white_options
        for ind in range(len(options_list)):
            valid_options = options_list[ind]
            for i in range(len(valid_options)-1,-1,-1):
                original_loc = white_locations[ind]
                white_locations[ind] = valid_options[i]
                if in_check('white',valid_options[i]):
                    options_list[ind].remove(valid_options[i])
                white_locations[ind] = original_loc
        
        # white castling moves check
        castle_moves=[]
        for castle_option in white_castle_boxes:
            enemy_list = black_options
            
            for ind in range(len(enemy_list)):
                valid_options = enemy_list[ind]
                for i in range(len(valid_options)-1,-1,-1):
                    original_loc = black_locations[ind]
                    black_locations[ind] = valid_options[i]
                    
                    if in_check('black',valid_options[i]):
                        enemy_list[ind].remove(valid_options[i])

                    black_locations[ind] = original_loc
            
            is_append=True
            for piece_moves in enemy_list:
                if (castle_option[0] in piece_moves) or (castle_option[1] in piece_moves):
                    is_append=False
                    break
            if is_append:
                castle_moves.append(castle_option)        

        print("white castle moves",castle_moves)
    else:
        options_list = black_options
        
        for ind in range(len(options_list)):
            valid_options = options_list[ind]
            for i in range(len(valid_options)-1,-1,-1):
                original_loc = black_locations[ind]
                black_locations[ind] = valid_options[i]
                
                if in_check('black',valid_options[i]):
                    options_list[ind].remove(valid_options[i])

                black_locations[ind] = original_loc

        # black castling moves check
        castle_moves=[]
        for castle_option in black_castle_boxes:
            enemy_list = white_options
        
            for ind in range(len(enemy_list)):
                valid_options = enemy_list[ind]
                for i in range(len(valid_options)-1,-1,-1):
                    original_loc = white_locations[ind]
                    white_locations[ind] = valid_options[i]
                    
                    if in_check('white',valid_options[i]):
                        enemy_list[ind].remove(valid_options[i])

                    white_locations[ind] = original_loc
            
            is_append=True
            for piece_moves in enemy_list:
                if (castle_option[0] in piece_moves) or (castle_option[1] in piece_moves):
                    is_append=False
                    break
            if is_append:
                castle_moves.append(castle_option)
        print("black castle moves",castle_moves)
    return options_list,castle_moves

def in_check(color,moved_pos):
    global check_w
    global check_b
    check_w=False
    check_b=False
    
    if(color =='white'):
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            black_options_dummy = check_options(black_pieces,black_locations,'black')
            
            if(moved_pos in black_locations):
               
                del_ind = black_locations.index(moved_pos)
                del_piece = black_pieces[del_ind]
                black_pieces.pop(del_ind)
                black_locations.pop(del_ind)
                black_options_dummy = check_options(black_pieces,black_locations,'black')
                black_pieces.append(del_piece)
                black_locations.append(moved_pos)
           
            for black_option in black_options_dummy:
                    if king_location in black_option:
                        check_w = True
                        return True
                    
                        
    if(color =='black'):
        if 'king' in black_pieces:
                king_index = black_pieces.index('king')
                king_location = black_locations[king_index]
                white_options_dummy = check_options(white_pieces,white_locations,'white')

                if(moved_pos in white_locations):
                    del_ind = white_locations.index(moved_pos)
                    del_piece = white_pieces[del_ind]
                    white_pieces.pop(del_ind)
                    white_locations.pop(del_ind)
                    white_options_dummy = check_options(white_pieces,white_locations,'white')
                    white_pieces.append(del_piece)
                    white_locations.append(moved_pos)
                
                for white_option in white_options_dummy:
                    if king_location in white_option:
                        check_b = True
                        return True
                    
# piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']                 

def update_dice_list(all_ops,color):
    if color == 'white':
        remaining_pieces = white_pieces
    else :
        remaining_pieces = black_pieces
    dice_list=[]
    # print(all_ops)

    for ind in range(len(remaining_pieces)):
        # ind = remaining_pieces.index(piece)

        if len(all_ops[ind])>0 :
          
            if remaining_pieces[ind] not in dice_list:
                dice_list.append(remaining_pieces[ind])

    return dice_list

def dice_select(dice_list):
    if len(dice_list)==0:
        print("NOT POSSIBLE")
    else:
        face = random.randint(0,len(dice_list)-1)
        return dice_list[face]


def draw_highlight(piece_highlights):
    for i in range(len(piece_highlights)):
        # surf_high=pygame.Surface((square_size,square_size),pygame.SRCALPHA)
        # color=pygame.Color(0,255,50,150)
        # pygame.draw.circle(surf_high,color,(square_size//2,square_size//2),25)
        # # pygame.draw.rect(surf_high, color, [0,0, square_size-1, square_size-1], 10)
        # radius=10
        # highlighted=pygame.transform.box_blur(surf_high,radius)
        # screen.blit(highlighted,(piece_highlights[i][0]*square_size+30,piece_highlights[i][1]*square_size+30))
   
        # if (piece_highlights[i][0]+piece_highlights[i][1])%2!=0:
        #     color=pygame.Color(50,50,50,255)
        # else:
        #     color=pygame.Color(200,200,200,255)
        # print(color)
        color=pygame.Color(159, 132, 189,255)
        rect_surf = pygame.Surface((square_size , square_size ), pygame.SRCALPHA)
        # pygame.draw.rect(rect_surf, color, [0,0, square_size+2, square_size+2], 8)
        pygame.draw.circle(rect_surf,color,(square_size//2,square_size//2),square_size//2 +square_size/4+5,25)
        # radius = 15
        # blurred_rect_surf = pygame.transform.box_blur(rect_surf, radius)
        screen.blit(rect_surf, (piece_highlights[i][0] * square_size + 30, piece_highlights[i][1] * square_size + 30))
    piece_highlights=[]

# draw valid moves on screen
def draw_valid(moves):
    color = pygame.Color(0,255,0,120) 
    for i in range(len(moves)):
        surf=pygame.Surface((square_size,square_size),pygame.SRCALPHA)
        # pygame.draw.circle(surf, color, (0, 0), square_size//2-5,7)
        pygame.draw.circle(surf, color, ( square_size//2,  square_size//2), square_size//2-5,7)
        screen.blit(surf,(moves[i][0] * square_size +board_start_pt,moves[i][1] * square_size +board_start_pt))

# draw captured pieces on side of screen
def draw_captured():
    i=0
    for piece in piece_list:
        if piece in captured_pieces_black:
            count = small_font.render("X "+ str(captured_pieces_black.count(piece)),True,'white')
            index = piece_list.index(piece)
            screen.blit(pygame.transform.scale(white_images[index],(50,50)) , (height, 30 +60*i))
            screen.blit(count, (height+50,40 +60*i))
            i=i+1
    j=0        
    for piece in piece_list:
        if piece in captured_pieces_white:
            count = small_font.render("X"+ str(captured_pieces_white.count(piece)),True,'white')
            index = piece_list.index(piece)
            screen.blit(pygame.transform.scale(white_images[index],(50,50)) , (height, height-80- (60*j)))
            screen.blit(count, (height+50,  height-70- (60*j)))
            j=j+1    
    # for i in range(len(captured_pieces_black)):
    #     captured_piece = captured_pieces_black[i]
    #     index = piece_list.index(captured_piece)
    #     screen.blit(small_white_images[index], (925, 5 + 50 * i))


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
                pygame.draw.rect(screen, 'red', [white_locations[king_index][0] * square_size + 29, white_locations[king_index][1] * square_size + 29, square_size+2, square_size+2], 3)
                color=pygame.Color(255,0,0,200)
                rect_surf = pygame.Surface((square_size -1, square_size - 1), pygame.SRCALPHA)
                pygame.draw.rect(rect_surf, color, [0,0, square_size-1, square_size-1], 10)
                radius = 10 
                blurred_rect_surf = pygame.transform.box_blur(rect_surf, radius)
                screen.blit(blurred_rect_surf, (white_locations[king_index][0] * square_size + 32, white_locations[king_index][1] * square_size + 32))
    if 'king' in black_pieces:
        king_index = black_pieces.index('king')
        king_location = black_locations[king_index]
        for i in range(len(white_options)):
            if king_location in white_options[i]:
                check_b = True
                color=pygame.Color(255,0,0,200)
                pygame.draw.rect(screen, 'red', [black_locations[king_index][0] * square_size + 29, black_locations[king_index][1] * square_size + 29, square_size+2, square_size+2], 3)
                rect_surf = pygame.Surface((square_size -1, square_size - 1), pygame.SRCALPHA)
                pygame.draw.rect(rect_surf, color, [0,0, square_size-1, square_size-1], 10)
                radius = 10 
                blurred_rect_surf = pygame.transform.box_blur(rect_surf, radius)
                screen.blit(blurred_rect_surf, (black_locations[king_index][0] * square_size + 32, black_locations[king_index][1] * square_size + 32))
                
# add castling
def check_castling():
    global white_castle_boxes
    global black_castle_boxes
    white_castle_boxes=[]
    black_castle_boxes=[]
    # king must not currently be in check, neither the rook nor king has moved previously, nothing between
    # and the king does not pass through or finish on an attacked piece
    castle_moves = []  # store each valid castle move as [((king_coords), (castle_coords))]
    rook_indexes = []
    rook_locations = []
    king_index = 0
    king_pos = (0, 0)
    if turn_step < 2:
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
                        rook_indexes[i]:
                        castle = False
                        break
                if castle:
                    white_castle_boxes.append((empty_squares[1],empty_squares[0]))
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
                        rook_indexes[i]:
                        castle = False
                        break
                if castle:
                    black_castle_boxes.append((empty_squares[1], empty_squares[0]))
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    
    

def draw_castling(moves):
    
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0][0] * square_size + square_size//2 + board_start_pt, moves[i][0][1] * square_size + square_size//2 + board_start_pt), 8)
        screen.blit(font.render('king', True, 'black'), (moves[i][0][0] * square_size + square_size//2 - 20 + board_start_pt, moves[i][0][1] * square_size + square_size//2 + 10 + board_start_pt))
        pygame.draw.circle(screen, color, (moves[i][1][0] * square_size + square_size//2 + board_start_pt, moves[i][1][1] * square_size + square_size//2 +board_start_pt), 8)
        screen.blit(font.render('rook', True, 'black'),
                    (moves[i][1][0] * square_size + square_size//2 - 20 + board_start_pt, moves[i][1][1] * square_size + square_size//2 + 10 + board_start_pt))
        pygame.draw.line(screen, color, (moves[i][0][0] * square_size + square_size//2 + board_start_pt, moves[i][0][1] * square_size + square_size//2 + board_start_pt),
                         (moves[i][1][0] * square_size + square_size//2 + board_start_pt, moves[i][1][1] * square_size + square_size//2 + board_start_pt), 2)



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

#dice show
def dice_show(roll_num):        
    
    pygame.draw.rect(screen,'grey',pygame.Rect(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-135,height/2-115,270,238))
    screen.blit(pawn_1,(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-150,height/2-150))
    if roll_num=='pawn':
        screen.blit(pawn_1,(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-150,height/2-150))
    if roll_num=='rook':
        screen.blit(rook_5,(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-150,height/2-150))
    if roll_num=='bishop':
        screen.blit(bishop_3,(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-150,height/2-150))
    if roll_num=='knight':
        screen.blit(knight_4,(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-150,height/2-150))
    if roll_num=='queen':
        screen.blit(queen_6,(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-150,height/2-150))
    if roll_num=='king':
        screen.blit(king_2,(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-150,height/2-150))

def dice_roll(roll_num): 
    screen.blit(cor_1,(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-150,height/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(screen,'grey',pygame.Rect(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-135,height/2-115,270,238))
    pygame.display.update()
    screen.blit(cor_2,(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-150,height/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(screen,'grey',pygame.Rect(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-135,height/2-115,270,238))
    pygame.display.update()
    screen.blit(cor_3,(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-150,height/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(screen,'grey',pygame.Rect(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-135,height/2-115,270,238))
    pygame.display.update()
    screen.blit(cor_4,(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-150,height/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(screen,'grey',pygame.Rect(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-135,height/2-115,270,238))
    pygame.display.update()
    screen.blit(cor_1,(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-150,height/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(screen,'grey',pygame.Rect(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-135,height/2-115,270,238))
    pygame.display.update()
    screen.blit(cor_2,(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-150,height/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(screen,'grey',pygame.Rect(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-135,height/2-115,270,238))
    pygame.display.update()
    screen.blit(cor_3,(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-150,height/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(screen,'grey',pygame.Rect(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-135,height/2-115,270,238))
    pygame.display.update()
    screen.blit(cor_4,(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-150,height/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(screen,'grey',pygame.Rect(board_size+board_start_pt+(width-(board_size+board_start_pt))/2-135,height/2-115,270,238))
    pygame.display.update()
    dice_show(roll_num)
    

def draw_game_over():

    # Draw the "Game Over" text
    pygame.draw.rect(screen,'black',[board_size+50,0,width-(board_size+50),height])
    game_over_text = big_font.render(winner, True,'white')
    text_rect = game_over_text.get_rect()
    text_rect.midtop = ((board_size+width+50)//2, 100)
    screen.blit(game_over_text, text_rect)

    if exit_button_rect.collidepoint(mouse):
        pygame.draw.rect(screen, 'red', exit_button_rect)
    else:
        pygame.draw.rect(screen, 'silver', exit_button_rect)
    exit_text = font.render("Exit", True, 'white')
    exit_text_rect = exit_text.get_rect()
    exit_text_rect.center = exit_button_rect.center
    screen.blit(exit_text, exit_text_rect)
 
    if rematch_button_rect.collidepoint(mouse):
        pygame.draw.rect(screen, 'red', rematch_button_rect)
    else:
        pygame.draw.rect(screen, 'silver', rematch_button_rect)
    rematch_text = font.render("Rematch", True, 'white')
    rematch_text_rect = rematch_text.get_rect()
    rematch_text_rect.center = rematch_button_rect.center
    screen.blit(rematch_text, rematch_text_rect)

#main loop
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')

dice_rolled = False
run = True
while run:
    
    mouse = pygame.mouse.get_pos()
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
    dice_show(roll_num)
    draw_captured()
    
    if turn_step==0:
        pygame.draw.rect(screen, button_color, roll_p1_rect)
    if roll_p1_rect.collidepoint(mouse) and turn_step == 0:
        roll_p1 = small_font.render('Roll', True, 'green')
        pygame.draw.rect(screen, 'white', roll_p1_rect)
    else:
        roll_p1 = small_font.render('Roll', True, 'white')
    if turn_step==2:
        pygame.draw.rect(screen, button_color, roll_p2_rect)
    if roll_p2_rect.collidepoint(mouse) and turn_step == 2:
        roll_p2 = small_font.render('Roll', True, 'green')
    else:
        roll_p2 = small_font.render('Roll', True, 'white')

    if exit_button.collidepoint(mouse):
        exit_t = medium_font.render("Exit", True, 'Green')
    else:
        exit_t = medium_font.render("Exit", True, 'white')
        
    if rematch_button.collidepoint(mouse):
        rematch_t = medium_font.render("Rematch", True, 'Green')
    else:
        rematch_t = medium_font.render("Rematch", True, 'white')
        
        

    # screen.blit(roll_p1 , (width-390,height/2+146))
    # screen.blit(roll_p2 , (width-390,height/2-166))
    
    rollp1_rect = roll_p1.get_rect()
    rollp1_rect.center = roll_p1_rect.center
    screen.blit(roll_p1,rollp1_rect)
    
    rollp2_rect = roll_p2.get_rect()
    rollp2_rect.center = roll_p2_rect.center
    screen.blit(roll_p2,rollp2_rect)
     
     
    exit_t_rect = exit_t.get_rect()
    exit_t_rect.center = exit_button.center
    screen.blit(exit_t, exit_t_rect)

    
    rematch_t_rect = rematch_t.get_rect()
    rematch_t_rect.center = rematch_button.center
    screen.blit(rematch_t, rematch_t_rect)
    #exit aur rematch buttons add krdo
    
    if not game_over:
        white_promote, black_promote, promo_index = check_promotion()
        if white_promote or black_promote:
            draw_promotion()
            check_promo_select()
            black_options = check_options(black_pieces, black_locations, 'black')
            white_options = check_options(white_pieces, white_locations, 'white')
    
    if  turn_step<2:
        draw_highlight(piece_highlights_white)
    if turn_step>1:
        draw_highlight(piece_highlights_black)

    if selection != 100:
        draw_valid(valid_moves)
        if selected_piece == 'king':
            print(castling_moves)
            draw_castling(castling_moves)

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and  game_over: 
    
            if exit_button_rect.collidepoint(event.pos):
                run=False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and  exit_button.collidepoint(event.pos): 
            run=False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and (rematch_button.collidepoint(event.pos) or (rematch_button_rect.collidepoint(event.pos) and game_over)):
            game_over = False
            winner = ''
            white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
            white_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), 
                               (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
            white_moved = [False, False, False, False, False, False, False, False,
                           False, False, False, False, False, False, False, False]
            black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
            'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']                
            black_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
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
            roll_num=0
            dice_rolled=False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:            
        
            x_coord = (event.pos[0] -30)// square_size
            y_coord = (event.pos[1]-30) // square_size
            click_coords = (int(x_coord), int(y_coord)) 
            
            if turn_step <= 1 :
                piece_highlights_black=[]
                if roll_p1_rect.collidepoint(event.pos) and not dice_rolled:
                    all_possible_options,castling_moves = check_valid_moves()
                    dice_list = update_dice_list(all_possible_options,'white')
                    if len(dice_list)==0 and check_w:
                        winner='Black Wins!!!'
                        game_over=True
                    if len(dice_list)==0 and not check_w:
                        winner='Draw! STALEMATE!!'
                        game_over=True
                 
                    roll_num = dice_select(dice_list)
                    # roll_num=yele[o]
                    # o=o+1
                    dice_roll(roll_num)
                    dice_rolled = True
                    
                if dice_rolled:
                    play_piece=[]
                    piece_highlights_white=[]
                    for i in range(len(white_pieces)):
                        if white_pieces[i] == roll_num and len(all_possible_options[i])>0:
                            play_piece.append(white_locations[i])
                            piece_highlights_white.append(white_locations[i])
                            
                    if click_coords in play_piece:                      

                        selection = white_locations.index(click_coords)
                        valid_moves = all_possible_options[selection]
                        # check what piece is selected, so you can only draw castling moves if king is selected
                        selected_piece = white_pieces[selection]
                        if turn_step == 0:
                            turn_step = 1

                    if click_coords in valid_moves and selection != 100:
                        piece_highlights_white = []
                        white_locations[selection] = click_coords
                        white_moved[selection] = True
                        if click_coords in black_locations:
                            black_piece = black_locations.index(click_coords)
                            captured_pieces_white.append(black_pieces[black_piece])
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
                        continue
                    # add option to castle
                    elif selection != 100 and selected_piece == 'king':
                        for q in range(len(castling_moves)):
                            if click_coords == castling_moves[q][0]:
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
                        continue

            if turn_step > 1:
                piece_highlights_white=[]
                # roller=small_font.render("Black to Roll",True,'Silver')
                if roll_p2_rect.collidepoint(event.pos) and dice_rolled:
                    all_possible_options,castling_moves = check_valid_moves()
                    # print(all_possible_options)
                    dice_list = update_dice_list(all_possible_options,'black')
                    if len(dice_list)==0 and check_b:
                        winner='White Wins!!!'
                        game_over=True
                    if len(dice_list)==0 and not check_b:
                        winner='Draw! STALEMATE!!'
                        game_over=True
                        
                        
                    roll_num = dice_select(dice_list)
                    # roll_num=yele[o]
                    # o=o+1
                    dice_roll(roll_num)
                    dice_rolled = False
                
                if not dice_rolled:
                    piece_highlights_black = []
                    play_piece=[]
                    
                    for i in range(len(black_pieces)):
                        if black_pieces[i] == roll_num and len(all_possible_options[i])>0:
                            play_piece.append(black_locations[i])
                            piece_highlights_black.append(black_locations[i])
                            # highlight=True
                    
                    if click_coords in play_piece:                
                        selection = black_locations.index(click_coords)
                        valid_moves = all_possible_options[selection]
                        # check what piece is selected, so you can only draw castling moves if king is selected
                        selected_piece = black_pieces[selection]
                        if turn_step == 2:
                            turn_step = 3
                    if click_coords in valid_moves and selection != 100:
                        black_locations[selection] = click_coords
                        black_moved[selection] = True
                        if click_coords in white_locations:
                            white_piece = white_locations.index(click_coords)
                            captured_pieces_black.append(white_pieces[white_piece])
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
                        continue
                    
                    # add option to castle
                    elif selection != 100 and selected_piece == 'king':
                       
                        for q in range(len(castling_moves)):
                            if click_coords == castling_moves[q][0]:
                               
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
                        continue
                

    if winner != '':
        game_over = True
        draw_game_over()
  

    
    pygame.display.flip()
pygame.quit()
sys.exit()
