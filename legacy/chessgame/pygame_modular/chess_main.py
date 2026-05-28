import random
import sys
from game_state import *
from game_constants import *
from chess_blits import *
from checker_funtctions import*
from white_player import selected_piece,white_turn
from black_player import selected_piece,black_turn
from black_computer import *



# def main_game():
    # SCREEN.blit('black',(0,0))
load_images()
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')

run = True
while run:

    mouse = pygame.mouse.get_pos()
    timer.tick(MAX_FPS)
    
    chess_canvas()
    set_pieces()
    draw_check(black_options,white_options)
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
                white_turn(event,click_coords)
            if turn_step>1 :
                black_turn(event,click_coords)