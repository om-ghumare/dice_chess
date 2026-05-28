import pygame
pygame.init()

SCREEN = pygame.display.set_mode((0,0),pygame.FULLSCREEN)  
SCREEN_WIDTH = SCREEN.get_width()
SCREEN_HEIGHT = SCREEN.get_height()
MAX_FPS = 60

BOARD_SIZE=SCREEN_HEIGHT-60
BOARD_START_PT=30 
SQUARE_SIZE=BOARD_SIZE/8
PIECE_SIZE = SQUARE_SIZE -18

FONT = pygame.font.Font('freesansbold.ttf', 20)
SMALL_FONT = pygame.font.Font('freesansbold.ttf', 30)
MEDIUM_FONT = pygame.font.Font('freesansbold.ttf', 40)
BIG_FONT = pygame.font.Font('freesansbold.ttf', 50)

WHITE_PIECE_IMAGES = []
BLACK_PIECE_IMAGES = []
DICE_IMAGES = {}

def load_images():
    white_pieces = ['wp','wq','wk','wn','wr','wb'] 
    for piece in white_pieces:
        WHITE_PIECE_IMAGES.append (pygame.transform.scale(pygame.image.load("images2/" + piece + ".png" ), (PIECE_SIZE,PIECE_SIZE)))
    
    black_pieces = ['bp','bq','bk','bn','br','bb'] 
    for piece in black_pieces:
        BLACK_PIECE_IMAGES.append (pygame.transform.scale(pygame.image.load("images2/" + piece + ".png" ), (PIECE_SIZE,PIECE_SIZE)))

    dice_imgs = ['p','r','n','b','q','k','c1','c2','c3','c4']
    for img in dice_imgs:
        DICE_IMAGES[img] = pygame.transform.scale(pygame.image.load("images2/dice and frame/" + img + ".png"), (300,300))

piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

button_w = 200
button_h = 60
button_x = (BOARD_SIZE+ SCREEN_WIDTH+ 50)//2 -button_w // 2
# button_x = width // 2 - button_w // 2
button_y_exit = SCREEN_HEIGHT// 2 - button_h // 2
button_y_rematch = button_y_exit + button_h + 20
exit_button_rect = pygame.Rect(button_x, button_y_exit, button_w, button_h)
rematch_button_rect = pygame.Rect(button_x, button_y_rematch, button_w, button_h)

rematch_button = pygame.Rect(SCREEN_WIDTH - 150 - 20 - 150 - 20, 20, 150, 50)
exit_button = pygame.Rect(SCREEN_WIDTH - 150 - 20, 20, 150, 50)


button_color=pygame.Color(	159, 132, 189)
 
roll_p1_rect = pygame.Rect(BOARD_SIZE+ BOARD_START_PT+ (SCREEN_WIDTH- (BOARD_SIZE + BOARD_START_PT))/2-60, (SCREEN_HEIGHT / 2) + 130, 120, 60)
roll_p2_rect = pygame.Rect(BOARD_SIZE+ BOARD_START_PT+ (SCREEN_WIDTH- (BOARD_SIZE+BOARD_START_PT))/2-60, (SCREEN_HEIGHT / 2) - 180, 120, 60)



