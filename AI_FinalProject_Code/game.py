import pygame
import sys
from pygame.locals import QUIT,KEYDOWN
import numpy as np

pygame.init()
X_n=15
Y_n=15
screen_X=670
screen_Y=670
screen = pygame.display.set_mode((screen_X,screen_Y))
margin_X = int((screen_X - 44 * (X_n-1))/2)
margin_Y = int((screen_Y - 44 * (Y_n-1))/2)


screen_color=[238,154,73]#background_color
line_color = [0,0,0]#line_color


# get the position where a piece can be placed
def find_pos(x,y):
    for i in range(margin_X,screen_X,44):
        for j in range(margin_Y,screen_X,44):
            L1=i-22
            L2=i+22
            R1=j-22
            R2=j+22
            if x>=L1 and x<=L2 and y>=R1 and y<=R2:
                return i,j
    return x,y



#check whether the poistion ghas been placed
def is_placed(x,y,over_pos):
    for val in over_pos:
        if val[0][0]==x and val[0][1]==y:
            return True
    return False
flag=False
tim=0

# the positions of placed peices
placed_pos=[] 
white_color=[255,255,255]
black_color=[0,0,0]

# 
def is_End(placed_pos):
    mp=np.zeros([15,15],dtype=int)
    for val in placed_pos:
        x=int((val[0][0]-27)/44)
        y=int((val[0][1]-27)/44)
        if val[1]==white_color:
            mp[x][y]=2# white piece
        else:
            mp[x][y]=1# black piece

    for i in range(15):
        pos1=[]
        pos2=[]
        for j in range(15):
            if mp[i][j]==1:
                pos1.append([i,j])
            else:
                pos1=[]
            if mp[i][j]==2:
                pos2.append([i,j])
            else:
                pos2=[]
            if len(pos1)>=5:# win
                return [1,pos1]
            if len(pos2)>=5:
                return [2,pos2]

    for j in range(15):
        pos1=[]
        pos2=[]
        for i in range(15):
            if mp[i][j]==1:
                pos1.append([i,j])
            else:
                pos1=[]
            if mp[i][j]==2:
                pos2.append([i,j])
            else:
                pos2=[]
            if len(pos1)>=5:
                return [1,pos1]
            if len(pos2)>=5:
                return [2,pos2]
    for i in range(15):
        for j in range(15):
            pos1=[]
            pos2=[]
            for k in range(15):
                if i+k>=15 or j+k>=15:
                    break
                if mp[i+k][j+k]==1:
                    pos1.append([i+k,j+k])
                else:
                    pos1=[]
                if mp[i+k][j+k]==2:
                    pos2.append([i+k,j+k])
                else:
                    pos2=[]
                if len(pos1)>=5:
                    return [1,pos1]
                if len(pos2)>=5:
                    return [2,pos2]
    for i in range(15):
        for j in range(15):
            pos1=[]
            pos2=[]
            for k in range(15):
                if i+k>=15 or j-k<0:
                    break
                if mp[i+k][j-k]==1:
                    pos1.append([i+k,j-k])
                else:
                    pos1=[]
                if mp[i+k][j-k]==2:
                    pos2.append([i+k,j-k])
                else:
                    pos2=[]
                if len(pos1)>=5:
                    return [1,pos1]
                if len(pos2)>=5:
                    return [2,pos2]
    return [0,[]]

while True:
    
    # EXIT
    for event in pygame.event.get():
        if event.type in (QUIT,KEYDOWN):
            sys.exit()


    screen.fill(screen_color)

    # vertical lines
    for i in range(27,screen_X,44):
        
        if i==27 or i==screen_X-27:
            pygame.draw.line(screen,line_color,[i,margin_X],[i,screen_X-margin_X],4)
        else:
            pygame.draw.line(screen,line_color,[i,margin_X],[i,screen_X-margin_X],2)
    
    # horizonal lines
    for i in range(27,screen_Y,44):
        if i==27 or i==screen_Y-27:
            pygame.draw.line(screen,line_color,[margin_Y,i],[screen_Y-margin_Y,i],4)
        else:
            pygame.draw.line(screen,line_color,[margin_Y,i],[screen_Y-margin_Y,i],2)
    # central dot
    pygame.draw.circle(screen, line_color,[margin_X+44*(int((X_n)/2)),margin_Y+44*(int((Y_n)/2))], 8,0)

    
  

    #show all the pieces
    for val in placed_pos:
        pygame.draw.circle(screen, val[1],val[0], 20,0)

    #check if the game is over
    res=is_End(placed_pos)
    if res[0]!=0:
        for pos in res[1]:
            pygame.draw.rect(screen,[238,48,167],[pos[0]*44+27-22,pos[1]*44+27-22,44,44],2,1)
        pygame.display.update()
        continue
    
    # get the position of where the cursor
    x,y = pygame.mouse.get_pos()
    x,y=find_pos(x,y)
    if not is_placed(x,y,placed_pos):
        # draw a sqaure to show exactly where the piece is going to be placed
        pygame.draw.rect(screen,[0 ,229 ,238 ],[x-22,y-22,44,44],2,1)
    
    # get mouse_click info 
    keys_pressed = pygame.mouse.get_pressed()
    # place the piece
    if keys_pressed[0] and tim==0:
        flag=True
        if not is_placed(x,y,placed_pos):
            if len(placed_pos)%2==0:
                placed_pos.append([[x,y],black_color])
            else:
                placed_pos.append([[x,y],white_color])

    
    if flag:
        tim+=1
    if tim%50==0:
        flag=False
        tim=0

    pygame.display.update()