from cgitb import small
from cmath import rect
from turtle import pos
import pygame  
import random
import time


roll_num=3


FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()
pygame.init()  
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)  

  
width = screen.get_width()
height = screen.get_height()
smallfont = pygame.font.SysFont('comicsansms',35)



sq_size=(height-60)/8
p_size=sq_size-17


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



# class Piece:
 
#     def __init__(self, chess_colour):
#         self._chess_colour = chess_colour
#         self._is_active = True
 
#     # chess_colour getter
#     @property
#     def chess_colour(self):
#         return self._chess_colour
 
#     # is_active setter/getter
#     @property
#     def is_active(self):
#         return self._is_active
 
#     @is_active.setter
#     def is_active(self, value):
#         self._is_active = value

def set_peice(x,y,isWhite,pos):
    x=x+8
    y=y+7
    if (pos[1]=='2'):
        screen.blit(w_p,(x,y))

    if (pos[1]=='7'):
        screen.blit(b_p,(x,y))
    
    if pos[1]=='1' and (pos[0]=='A' or pos[0]=='H'):
        screen.blit(w_r,(x,y))
    
    if pos[1]=='1' and (pos[0]=='B' or pos[0]=='G'):
        screen.blit(w_n,(x,y))

    if pos[1]=='1' and (pos[0]=='C' or pos[0]=='F'):
        screen.blit(w_b,(x,y))

    if (pos[1]=='1' and pos[0]=='D'):
        screen.blit(w_q,(x,y))
    
    if (pos[1]=='1' and pos[0]=='E'):
        screen.blit(w_k,(x,y))

    if pos[1]=='8' and (pos[0]=='A' or pos[0]=='H'):
        screen.blit(b_r,(x,y))
    
    if pos[1]=='8' and (pos[0]=='B' or pos[0]=='G'):
        screen.blit(b_n,(x,y))

    if pos[1]=='8' and (pos[0]=='C' or pos[0]=='F'):
        screen.blit(b_b,(x,y))

    if (pos[1]=='8' and pos[0]=='D'):
        screen.blit(b_q,(x,y))
    
    if (pos[1]=='8' and pos[0]=='E'):
        screen.blit(b_k,(x,y))

    
    
    

    

    


    

def calculate_coordinates(x,y,is_white,square_size,position):
    
    x_coordinate=x*square_size+30
    y_coordinate=y*square_size+30
    tuple=[x_coordinate,y_coordinate,is_white,position]
    return tuple



def board_square(board_size,board_start_pt):
    chess_board=[]
    is_white=False
    square_size=board_size/8
    for y in range(8):
        chess_row=[]
        is_white=not is_white
        for x in range(8):
            position = chr(x+65) + str(8-y)
            chess_row.append(calculate_coordinates(x,y,is_white,square_size,position))
            is_white= not is_white
        chess_board.append(chess_row)
    
    count=0
    for row in chess_board:                             #[x_coordinate,y_coordinate,is_white,position]
        for square in row:
            count =count+1
            # print(square[3][1])
            surf=pygame.Surface((square_size,square_size))

            if square[2]:
                surf.fill((255,255,255))
            else:
                surf.fill((100,100,100))
            
            rect = surf.get_rect()
            screen.blit(surf,(square[0],square[1]))
            print(square[0],square[1],square[2],square[3])
            # pygame.display.flip()
            set_peice(square[0],square[1],square[2],square[3])

def chesscanvas():
    board_size=height-60
    board_start_pt=30 
    player1=smallfont.render('Player 1',True,"white")
    player2=smallfont.render('Player 2',True,"white")
    screen.blit(player1,(board_size+50, 30))
    pygame.draw.rect(screen, "white", pygame.Rect(board_start_pt,board_start_pt, board_size, board_size))
    board_square(board_size,board_start_pt)
    screen.blit(player2,(board_size+50,board_size-20))


# def show_score(score):
#     Scoring=smallfont.render(str(score),True,"white")
#     screen.blit(Scoring, (925,500))




# def dice_sect(roll_num):
#     #roll_num=1
#     dice_show(roll_num)


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

def main():
    score=0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if width-415 <= mouse[0] <= width-295 and height/2+120 <= mouse[1] <= height/2+180:
                    dice_roll()
                if width-415 <= mouse[0] <= width-295 and (height/2)-180 <= mouse[1] <= (height/2)-120:
                    dice_roll()
                if width-85 <= mouse[0] <= width-5 and 7 <= mouse[1] <= 60:
                    running = False
            # elif event.type == pygame.MOUSEBUTTONDOWN:
                if width-285<= mouse[0] <= width-90 and 7 <= mouse[1] <= 60:
                    running=False
                    main()

                  
 
               

            
            mouse = pygame.mouse.get_pos()
            global roll_p1
            global roll_p2
            global Quit 
            global rematch

            
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
            

            if width-85 <= mouse[0] <= width-5 and 7 <= mouse[1] <= 60:
                Quit = smallfont.render('Exit' , True , "yellow")
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                Quit = smallfont.render('Exit' , True , "white")
                # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if width-285<= mouse[0] <= width-90 and 7 <= mouse[1] <= 60:
                rematch=smallfont.render('Play Again',True,"yellow")
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                rematch=smallfont.render('Play Again',True,"white")

        # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        back_ground_color=pygame.Color(0,0,0)
        screen.fill(back_ground_color)
        screen.blit(roll_p1 , (width-390,height/2+126))
        screen.blit(roll_p2 , (width-390,height/2-166))
        screen.blit(Quit , (width-80,10))
        screen.blit(rematch , (width-280,10))
        # show_score(score)

                           
        
        chesscanvas()
    
        dice_show(roll_num)
        # pygame.draw.rect(screen,'grey',pygame.Rect(width-415,height/2+120,120,60))-------------------------
        # dice_show()
        
        # pygame.draw.rect(screen, "red", pygame.Rect(900,500,20,50))




        pygame.display.update()
        fpsClock.tick(FPS)


if __name__ == "__main__":
    main()