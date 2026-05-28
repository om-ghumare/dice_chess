
import random
import sys
from game_state import *
from game_constants import *
from chess_blits import *
from checker_funtctions import *


selected_piece=''
def black_turn(event,click_coords):
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
            # print(selected_piece , click_coords)
            # print("black",black_moved)
    
        
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
                    # print(selected_piece , click_coords)
 