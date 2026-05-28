"""
Contains all the functions used in drawing elements on the SCREEN
"""

import time
from constants import *
from game_state import *
# from chess_main import black_options,white_options

def chess_canvas():
    back_ground_color=pygame.Color(0,0,0)
    SCREEN.fill(back_ground_color)
    pygame.draw.rect(SCREEN, "white", pygame.Rect(BOARD_START_PT,BOARD_START_PT, BOARD_SIZE, BOARD_SIZE))
    light_color=pygame.Color(255,255,255)
    dark_color=pygame.Color(100,100,100)
    bor_color=pygame.Color("silver")
    pygame.draw.rect(SCREEN, bor_color, [BOARD_START_PT-5,BOARD_START_PT-5,BOARD_SIZE+10,BOARD_SIZE+10],5)
    for col in range(8):
        for row in range(8):
            # print(BOARD_START_PT+(row*SQUARE_SIZE),BOARD_START_PT+(col*SQUARE_SIZE))
            if((row%2==0 and col%2==0) or (row%2!=0 and col%2!=0)):
                pygame.draw.rect(SCREEN, dark_color, [BOARD_START_PT+(row*SQUARE_SIZE),BOARD_START_PT+(col*SQUARE_SIZE), SQUARE_SIZE,SQUARE_SIZE])
            else:
                pygame.draw.rect(SCREEN, light_color, [BOARD_START_PT+(row*SQUARE_SIZE)+(col*SQUARE_SIZE),BOARD_START_PT+(row*SQUARE_SIZE)+(col*SQUARE_SIZE), SQUARE_SIZE,SQUARE_SIZE])
                
   
def set_pieces():
    
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        SCREEN.blit(WHITE_PIECE_IMAGES[index], (white_locations[i][0] * SQUARE_SIZE + 40, white_locations[i][1] * SQUARE_SIZE + 40))
        if turn_step < 2:
            if selection == i:
                color=pygame.Color(0,255,0,255)
                rect_surf = pygame.Surface((SQUARE_SIZE , SQUARE_SIZE ), pygame.SRCALPHA)
                pygame.draw.circle(rect_surf,color,(SQUARE_SIZE//2,SQUARE_SIZE//2),SQUARE_SIZE//2 +SQUARE_SIZE//4+5,30)
                radius = 25
                blurred_rect_surf = pygame.transform.box_blur(rect_surf, radius)
                SCREEN.blit(blurred_rect_surf, (white_locations[i][0] * SQUARE_SIZE + 30, white_locations[i][1] * SQUARE_SIZE + 30))
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i]) 
        SCREEN.blit(BLACK_PIECE_IMAGES[index], (black_locations[i][0] * SQUARE_SIZE+37, black_locations[i][1] * SQUARE_SIZE+40))
        if turn_step >= 2:
            if selection == i:
                color=pygame.Color(0,255,0,255)
                rect_surf = pygame.Surface((SQUARE_SIZE , SQUARE_SIZE ), pygame.SRCALPHA)
                pygame.draw.circle(rect_surf,color,(SQUARE_SIZE//2,SQUARE_SIZE//2),SQUARE_SIZE//2 +SQUARE_SIZE//4+5,30)
                radius = 25
                blurred_rect_surf = pygame.transform.box_blur(rect_surf, radius)
                SCREEN.blit(blurred_rect_surf, (black_locations[i][0] * SQUARE_SIZE + 30, black_locations[i][1] * SQUARE_SIZE + 30))


def draw_highlight(piece_highlights):
    for i in range(len(piece_highlights)):
        color=pygame.Color(159, 132, 189,255)
        rect_surf = pygame.Surface((SQUARE_SIZE , SQUARE_SIZE ), pygame.SRCALPHA)
        pygame.draw.circle(rect_surf,color,(SQUARE_SIZE//2,SQUARE_SIZE//2),SQUARE_SIZE//2 +SQUARE_SIZE/4+5,25)
        SCREEN.blit(rect_surf, (piece_highlights[i][0] * SQUARE_SIZE + 30, piece_highlights[i][1] * SQUARE_SIZE + 30))
    piece_highlights=[]

# draw valid moves on SCREEN
def draw_valid(moves):
    color = pygame.Color(0,255,0,120) 
    for i in range(len(moves)):
        surf=pygame.Surface((SQUARE_SIZE,SQUARE_SIZE),pygame.SRCALPHA)
        # pygame.draw.circle(surf, color, (0, 0), SQUARE_SIZE//2-5,7)
        pygame.draw.circle(surf, color, ( SQUARE_SIZE//2,  SQUARE_SIZE//2), SQUARE_SIZE//2-5,7)
        SCREEN.blit(surf,(moves[i][0] * SQUARE_SIZE +BOARD_START_PT,moves[i][1] * SQUARE_SIZE +BOARD_START_PT))

# draw captured pieces on side of SCREEN
def draw_captured():
    i=0
    for piece in piece_list:
        if piece in captured_pieces_black:
            count = SMALL_FONT.render("X "+ str(captured_pieces_black.count(piece)),True,'white')
            index = piece_list.index(piece)
            SCREEN.blit(pygame.transform.scale(WHITE_PIECE_IMAGES[index],(50,50)) , (SCREEN_HEIGHT, 30 +60*i))
            SCREEN.blit(count, (SCREEN_HEIGHT+50,40 +60*i))
            i=i+1
    j=0        
    for piece in piece_list:
        if piece in captured_pieces_white:
            count = SMALL_FONT.render("X"+ str(captured_pieces_white.count(piece)),True,'white')
            index = piece_list.index(piece)
            SCREEN.blit(pygame.transform.scale(WHITE_PIECE_IMAGES[index],(50,50)) , (SCREEN_HEIGHT, SCREEN_HEIGHT-80- (60*j)))
            SCREEN.blit(count, (SCREEN_HEIGHT+50,  SCREEN_HEIGHT-70- (60*j)))
            j=j+1    
  


# draw a red square around king if in check
def draw_check(black_options,white_options):
    
    global check_w
    global check_b
    # check_w=False
    # check_b=False
    # print("1",check_w,check_b)
    # print("2",check_w,check_b)
    print("whiteloc",white_locations)
    # if turn_step < 2:
    if 'king' in white_pieces:
        king_index = white_pieces.index('king')
        king_location = white_locations[king_index]
        print(king_location,black_options)
        for i in range(len(black_options)):
            if king_location in black_options[i]:
                pygame.draw.rect(SCREEN, 'red', [white_locations[king_index][0] * SQUARE_SIZE + 29, white_locations[king_index][1] * SQUARE_SIZE + 29, SQUARE_SIZE+2, SQUARE_SIZE+2], 3)
                color=pygame.Color(255,0,0,200)
                rect_surf = pygame.Surface((SQUARE_SIZE -1, SQUARE_SIZE - 1), pygame.SRCALPHA)
                pygame.draw.rect(rect_surf, color, [0,0, SQUARE_SIZE-1, SQUARE_SIZE-1], 10)
                radius = 10 
                blurred_rect_surf = pygame.transform.box_blur(rect_surf, radius)
                SCREEN.blit(blurred_rect_surf, (white_locations[king_index][0] * SQUARE_SIZE + 32, white_locations[king_index][1] * SQUARE_SIZE + 32))
    if 'king' in black_pieces:
        king_index = black_pieces.index('king')
        king_location = black_locations[king_index]
        print(king_location,white_options)
        for i in range(len(white_options)):
            if king_location in white_options[i]:
                color=pygame.Color(255,0,0,200)
                pygame.draw.rect(SCREEN, 'red', [black_locations[king_index][0] * SQUARE_SIZE + 29, black_locations[king_index][1] * SQUARE_SIZE + 29, SQUARE_SIZE+2, SQUARE_SIZE+2], 3)
                rect_surf = pygame.Surface((SQUARE_SIZE -1, SQUARE_SIZE - 1), pygame.SRCALPHA)
                pygame.draw.rect(rect_surf, color, [0,0, SQUARE_SIZE-1, SQUARE_SIZE-1], 10)
                radius = 10 
                blurred_rect_surf = pygame.transform.box_blur(rect_surf, radius)
                SCREEN.blit(blurred_rect_surf, (black_locations[king_index][0] * SQUARE_SIZE + 32, black_locations[king_index][1] * SQUARE_SIZE + 32))


def draw_castling(moves):
    
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(SCREEN, color, (moves[i][0][0] * SQUARE_SIZE + SQUARE_SIZE//2 + BOARD_START_PT, moves[i][0][1] * SQUARE_SIZE + SQUARE_SIZE//2 + BOARD_START_PT), 8)
        SCREEN.blit(FONT.render('king', True, 'black'), (moves[i][0][0] * SQUARE_SIZE + SQUARE_SIZE//2 - 20 + BOARD_START_PT, moves[i][0][1] * SQUARE_SIZE + SQUARE_SIZE//2 + 10 + BOARD_START_PT))
        pygame.draw.circle(SCREEN, color, (moves[i][1][0] * SQUARE_SIZE + SQUARE_SIZE//2 + BOARD_START_PT, moves[i][1][1] * SQUARE_SIZE + SQUARE_SIZE//2 +BOARD_START_PT), 8)
        SCREEN.blit(FONT.render('rook', True, 'black'),
                    (moves[i][1][0] * SQUARE_SIZE + SQUARE_SIZE//2 - 20 + BOARD_START_PT, moves[i][1][1] * SQUARE_SIZE + SQUARE_SIZE//2 + 10 + BOARD_START_PT))
        pygame.draw.line(SCREEN, color, (moves[i][0][0] * SQUARE_SIZE + SQUARE_SIZE//2 + BOARD_START_PT, moves[i][0][1] * SQUARE_SIZE + SQUARE_SIZE//2 + BOARD_START_PT),
                         (moves[i][1][0] * SQUARE_SIZE + SQUARE_SIZE//2 + BOARD_START_PT, moves[i][1][1] * SQUARE_SIZE + SQUARE_SIZE//2 + BOARD_START_PT), 2)
        

def draw_promotion():
    pygame.draw.rect(SCREEN, 'dark gray', [800, 0, 200, 420])
    if white_promote:
        color = 'white'
        for i in range(len(white_promotions)):
            piece = white_promotions[i]
            index = piece_list.index(piece)
            SCREEN.blit(WHITE_PIECE_IMAGES[index], (860, 5 + 100 * i))
    elif black_promote:
        color = 'black'
        for i in range(len(black_promotions)):
            piece = black_promotions[i]
            index = piece_list.index(piece)
            SCREEN.blit(BLACK_PIECE_IMAGES[index], (860, 5 + 100 * i))
    pygame.draw.rect(SCREEN, color, [800, 0, 200, 420], 8)


#dice show
def dice_show(roll_num):        
    
    pygame.draw.rect(SCREEN,'grey',pygame.Rect(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-135,SCREEN_HEIGHT/2-115,270,238))
    SCREEN.blit(DICE_IMAGES['p'],(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-150,SCREEN_HEIGHT/2-150))
    if roll_num=='pawn':
        SCREEN.blit(DICE_IMAGES['p'],(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-150,SCREEN_HEIGHT/2-150))
    if roll_num=='rook':
        SCREEN.blit(DICE_IMAGES['r'],(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-150,SCREEN_HEIGHT/2-150))
    if roll_num=='bishop':
        SCREEN.blit(DICE_IMAGES['b'],(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-150,SCREEN_HEIGHT/2-150))
    if roll_num=='knight':
        SCREEN.blit(DICE_IMAGES['n'],(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-150,SCREEN_HEIGHT/2-150))
    if roll_num=='queen':
        SCREEN.blit(DICE_IMAGES['q'],(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-150,SCREEN_HEIGHT/2-150))
    if roll_num=='king':
        SCREEN.blit(DICE_IMAGES['k'],(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-150,SCREEN_HEIGHT/2-150))

def dice_roll(roll_num): 
    SCREEN.blit(DICE_IMAGES['c1'],(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-150,SCREEN_HEIGHT/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(SCREEN,'grey',pygame.Rect(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-135,SCREEN_HEIGHT/2-115,270,238))
    pygame.display.update()
    SCREEN.blit(DICE_IMAGES['c2'],(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-150,SCREEN_HEIGHT/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(SCREEN,'grey',pygame.Rect(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-135,SCREEN_HEIGHT/2-115,270,238))
    pygame.display.update()
    SCREEN.blit(DICE_IMAGES['c3'],(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-150,SCREEN_HEIGHT/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(SCREEN,'grey',pygame.Rect(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-135,SCREEN_HEIGHT/2-115,270,238))
    pygame.display.update()
    SCREEN.blit(DICE_IMAGES['c4'],(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-150,SCREEN_HEIGHT/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(SCREEN,'grey',pygame.Rect(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-135,SCREEN_HEIGHT/2-115,270,238))
    pygame.display.update()
    SCREEN.blit(DICE_IMAGES['c1'],(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-150,SCREEN_HEIGHT/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(SCREEN,'grey',pygame.Rect(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-135,SCREEN_HEIGHT/2-115,270,238))
    pygame.display.update()
    SCREEN.blit(DICE_IMAGES['c2'],(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-150,SCREEN_HEIGHT/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(SCREEN,'grey',pygame.Rect(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-135,SCREEN_HEIGHT/2-115,270,238))
    pygame.display.update()
    SCREEN.blit(DICE_IMAGES['c3'],(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-150,SCREEN_HEIGHT/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(SCREEN,'grey',pygame.Rect(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-135,SCREEN_HEIGHT/2-115,270,238))
    pygame.display.update()
    SCREEN.blit(DICE_IMAGES['c4'],(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-150,SCREEN_HEIGHT/2-150))
    pygame.display.update()
    time.sleep(0.08)
    pygame.draw.rect(SCREEN,'grey',pygame.Rect(BOARD_SIZE+BOARD_START_PT+(SCREEN_WIDTH-(BOARD_SIZE+BOARD_START_PT))/2-135,SCREEN_HEIGHT/2-115,270,238))
    pygame.display.update()
    dice_show(roll_num)
    

def draw_game_over(mouse):

    # Draw the "Game Over" text
    pygame.draw.rect(SCREEN,'black',[BOARD_SIZE+50,0,SCREEN_WIDTH-(BOARD_SIZE+50),SCREEN_HEIGHT])
    game_over_text = BIG_FONT.render(winner, True,'white')
    text_rect = game_over_text.get_rect()
    text_rect.midtop = ((BOARD_SIZE+SCREEN_WIDTH+50)//2, 100)
    SCREEN.blit(game_over_text, text_rect)

    if exit_button_rect.collidepoint(mouse):
        pygame.draw.rect(SCREEN, 'red', exit_button_rect)
    else:
        pygame.draw.rect(SCREEN, 'silver', exit_button_rect)
    exit_text = FONT.render("Exit", True, 'white')
    exit_text_rect = exit_text.get_rect()
    exit_text_rect.center = exit_button_rect.center
    SCREEN.blit(exit_text, exit_text_rect)
 
    if rematch_button_rect.collidepoint(mouse):
        pygame.draw.rect(SCREEN, 'red', rematch_button_rect)
    else:
        pygame.draw.rect(SCREEN, 'silver', rematch_button_rect)
    rematch_text = FONT.render("Rematch", True, 'white')
    rematch_text_rect = rematch_text.get_rect()
    rematch_text_rect.center = rematch_button_rect.center
    SCREEN.blit(rematch_text, rematch_text_rect)

def draw_right_screen(mouse,turn_step):
    # print(turn_step)
    if turn_step==0:
        pygame.draw.rect(SCREEN, button_color, roll_p1_rect)
    if roll_p1_rect.collidepoint(mouse) and turn_step == 0:
        roll_p1 = SMALL_FONT.render('Roll', True, 'green')
        pygame.draw.rect(SCREEN, 'white', roll_p1_rect)
    else:
        roll_p1 = SMALL_FONT.render('Roll', True, 'white')
        
    if turn_step==2:
        pygame.draw.rect(SCREEN, button_color, roll_p2_rect)
    if roll_p2_rect.collidepoint(mouse) and turn_step == 2:
        roll_p2 = SMALL_FONT.render('Roll', True, 'green')
    else:
        roll_p2 = SMALL_FONT.render('Roll', True, 'white')

    if exit_button.collidepoint(mouse):
        exit_t = MEDIUM_FONT.render("Exit", True, 'Green')
    else:
        exit_t = MEDIUM_FONT.render("Exit", True, 'white')
        
    if rematch_button.collidepoint(mouse):
        rematch_t = MEDIUM_FONT.render("Rematch", True, 'Green')
    else:
        rematch_t = MEDIUM_FONT.render("Rematch", True, 'white')
        
    rollp1_rect = roll_p1.get_rect()
    rollp1_rect.center = roll_p1_rect.center
    SCREEN.blit(roll_p1,rollp1_rect)
    
    rollp2_rect = roll_p2.get_rect()
    rollp2_rect.center = roll_p2_rect.center
    SCREEN.blit(roll_p2,rollp2_rect)
     
    exit_t_rect = exit_t.get_rect()
    exit_t_rect.center = exit_button.center
    SCREEN.blit(exit_t, exit_t_rect)
    
    rematch_t_rect = rematch_t.get_rect()
    rematch_t_rect.center = rematch_button.center
    SCREEN.blit(rematch_t, rematch_t_rect)