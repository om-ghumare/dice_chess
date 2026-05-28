"""
Main driver file for handling user input and current state of Game
"""


import random
import sys
from game_state import *
from constants import *
from chess_engine import *

timer = pygame.time.Clock()

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
            
            # for ind in range(len(enemy_list)):
            #     valid_options = enemy_list[ind]
            #     for i in range(len(valid_options)-1,-1,-1):
            #         original_loc = black_locations[ind]
            #         black_locations[ind] = valid_options[i]
                    
            #         if in_check('black',valid_options[i]):
            #             enemy_list[ind].remove(valid_options[i])

            #         black_locations[ind] = original_loc
            
            is_append=True
            for piece_moves in enemy_list:
                if (castle_option[0] in piece_moves) or (castle_option[1] in piece_moves):
                    is_append=False
                    break
            if is_append:
                castle_moves.append(castle_option)        

        # print("white castle moves",castle_moves)
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
        
            # for ind in range(len(enemy_list)):
            #     valid_options = enemy_list[ind]
            #     for i in range(len(valid_options)-1,-1,-1):
            #         original_loc = white_locations[ind]
            #         white_locations[ind] = valid_options[i]
                    
            #         if in_check('white',valid_options[i]):
            #             enemy_list[ind].remove(valid_options[i])

            #         white_locations[ind] = original_loc
            
            is_append=True
            for piece_moves in enemy_list:
                if (castle_option[0] in piece_moves) or (castle_option[1] in piece_moves):
                    is_append=False
                    break
            if is_append:
                castle_moves.append(castle_option)
        # print("black castle moves",castle_moves)
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

def check_promotion_select():
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    x_pos = mouse_pos[0] // 100
    y_pos = mouse_pos[1] // 100
    if white_promote and left_click and x_pos > 7 and y_pos < 4:
        white_pieces[promo_index] = white_promotions[y_pos]
    elif black_promote and left_click and x_pos > 7 and y_pos < 4:
        black_pieces[promo_index] = black_promotions[y_pos]


load_images()
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')

run = True
while run:

    mouse = pygame.mouse.get_pos()
    timer.tick(MAX_FPS)
    
    chess_canvas()
    set_pieces()
    # print("1",black_options)
    # print("2",white_options)
    # print("1",check_w,check_b)
    draw_check(black_options,white_options)
    # print("3",black_options)
    # print("4",white_options)
    # print(check_w,check_b)
    dice_show(roll_num)
    draw_captured()
    draw_right_screen(mouse,turn_step)
    

    # draw promotion of pawn
    if not game_over:
        white_promote, black_promote, promo_index = check_promotion()
        if white_promote or black_promote:
            draw_promotion()
            check_promotion_select()
    
    # highlight the pieces that can be moved 
    if  turn_step<2:
        draw_highlight(piece_highlights_white)
    if turn_step>1:
        draw_highlight(piece_highlights_black)

    # draw valid moves of a selected piece
    if selection != 100:
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

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and  game_over: 
            if exit_button_rect.collidepoint(event.pos):
                run=False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and  exit_button.collidepoint(event.pos): 
            run=False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and (rematch_button.collidepoint(event.pos) or (rematch_button_rect.collidepoint(event.pos) and game_over)):
            reset_game_state()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:            
        
            x_coord = (event.pos[0] -30)// SQUARE_SIZE
            y_coord = (event.pos[1]-30) // SQUARE_SIZE
            click_coords = (int(x_coord), int(y_coord)) 
            
            if turn_step <= 1 :
                piece_highlights_black=[]
                if roll_p1_rect.collidepoint(event.pos) and not dice_rolled:
                    all_possible_options,castling_moves = check_valid_moves()
                    # print(all_possible_options)
                    # print(castling_moves)
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
                        print(selected_piece , click_coords)
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
                                print(selected_piece , click_coords)
                        continue

            if turn_step > 1:
                piece_highlights_white=[]
               
                if roll_p2_rect.collidepoint(event.pos) and dice_rolled:
                    all_possible_options,castling_moves = check_valid_moves()
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
                           
                    
                    if click_coords in play_piece:                
                        selection = black_locations.index(click_coords)
                        valid_moves = all_possible_options[selection]
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
                        print(selected_piece , click_coords)
                        # print("black",black_moved)
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
                                print(selected_piece , click_coords)
                        continue
                

    if winner != '':
        game_over = True
        draw_game_over(mouse)
    
    pygame.display.flip()    
pygame.quit()
sys.exit()

