import random
import sys
from game_state import *
from game_constants import *
from chess_blits import *
from checker_funtctions import *

selected_piece=''
def white_turn(event,click_coords):
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
            # print(selected_piece , click_coords)
           
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
                    # print(selected_piece , click_coords)
          
