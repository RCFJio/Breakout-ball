

import pygame
from pygame.locals import *
from tkinter import messagebox
from tkinter import *
pygame.init()
screen_w=600
screen_h=600
screen=pygame.display.set_mode((screen_w,screen_h))
pygame.display.set_caption('Breakout')
bg=(234,218,184)
block_r=(242,85,96)
block_g=(86,174,87)
block_b=(69,177,232)
paddle_col=(142,135,123)
paddle_outline=(100,100,100)
col=6
row=6
clock=pygame.time.Clock()
fps=60
live_ball=False
gameover=0
life=2
status=1
paused=False
def pause():
    paused=True
    while(paused):
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                pygame.QUIT()
                quit()
            elif(event.type==pygame.KEYDOWN):
                key=pygame.key.get_pressed()
                if(key[pygame.K_c]):
                    paused=False
                elif(key[pygame.K_q]):
                    pygame.QUIT()
                    quit()
        screen.fill((255,255,255))
        pause_text = pygame.font.SysFont('Consolas', 18).render('Paused Enter c to continue or q to exit', True, pygame.color.Color('black'))
        screen.blit(pause_text, (100, 100))
        pygame.display.flip()
        clock.tick(60)

        
class wall():

    def __init__(self):
        self.width=screen_w//col
        self.height=50

    def create_wall(self):
        self.blocks=[]
        block=[]
        for i in range(row):
            block_row=[]
            for j in range(col):
                x=j*self.width
                y=i*self.height
                rect=pygame.Rect(x,y,self.width,self.height)
                if(i<2):
                    streng=3
                elif(i<4):
                    streng=2
                elif(i<6):
                    streng=1
                block=[rect,streng] 
                block_row.append(block)
            self.blocks.append(block_row)
        
    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                if(block[1]==3):
                    block_col=block_b
                elif(block[1]==2):
                    block_col=block_g
                elif(block[1]==1):
                    block_col=block_r
                pygame.draw.rect(screen,block_col,block[0])
                pygame.draw.rect(screen,bg,block[0],2)

class paddle():
    
    def __init__(self):
        self.reset()
    
    def move(self):
        self.direct=0
        key=pygame.key.get_pressed()
        if(key[pygame.K_LEFT] and self.rect.left>0):
            self.rect.x-=self.speed
            self.direct=1
        if(key[pygame.K_RIGHT] and self.rect.right<screen_w):
            self.rect.x+=self.speed
            self.direct=0
    
    def draw(self):
        pygame.draw.rect(screen,paddle_col,self.rect)
        pygame.draw.rect(screen,paddle_outline,self.rect,2)
    
    def reset(self):
        self.height=20
        self.width=screen_w//col
        self.x=screen_w//2-self.width//2
        self.y=screen_h-self.height*2
        self.speed=10
        self.rect=Rect(self.x,self.y,self.width,self.height)
        self.direct=0

class g_ball():
    
    def __init__(self,x,y):
        self.reset(x,y)
    
    def move(self):
        collision=5
        wall_des=1
        rc=0
        for rows in wall.blocks:
            c=0
            for item in rows:
                if(self.rect.colliderect(item[0])):
                    if(abs(self.rect.bottom-item[0].top)<collision and self.yspeed>0):
                        self.yspeed*=-1
                    if(abs(self.rect.top-item[0].bottom)<collision and self.yspeed<0):
                        self.yspeed*=-1
                    if(abs(self.rect.right-item[0].left)<collision and self.xspeed>0):
                        self.xspeed*=-1
                    if(abs(self.rect.left-item[0].right)<collision and self.xspeed<0):
                        self.xspeed*=-1
                    if(wall.blocks[rc][c][1]>1):
                        wall.blocks[rc][c][1]-=1
                    else:
                        wall.blocks[rc][c][0]=(0,0,0,0)
                if(wall.blocks[rc][c][0]!=(0,0,0,0)):
                    wall_des=0
                c+=1
            rc+=1
        if(wall_des==1):
            self.gameover=1



                    
        if(self.rect.left<0 or self.rect.right>screen_w):
            self.xspeed*=-1
        if(self.rect.top<0):
            self.yspeed*=-1
        if(self.rect.bottom>screen_h):
            self.gameover=-1
        if(self.rect.colliderect(paddle)):
            if(abs(self.rect.bottom-paddle.rect.top)<collision and self.yspeed>0):
                self.yspeed*=-1
                self.xspeed+=paddle.direct
                if(self.xspeed>self.maxspeed):
                    self.xspeed=self.maxspeed
                elif(self.xspeed<0 and self.xspeed<-self.maxspeed):
                    self.xspeed=-self.maxspeed
            else:
                self.xspeed*=-1



        
        self.rect.x+=self.xspeed
        self.rect.y+=self.yspeed
        return self.gameover
    
    def draw(self):
        pygame.draw.circle(screen,paddle_col,(self.rect.x+self.ball_rad,self.rect.y+self.ball_rad),self.ball_rad)
        pygame.draw.circle(screen,paddle_outline,(self.rect.x+self.ball_rad,self.rect.y+self.ball_rad),self.ball_rad)
    
    def reset(self,x,y):
        self.ball_rad=10
        self.x=x-self.ball_rad
        self.y=y
        self.rect=Rect(self.x,self.y,self.ball_rad*2,self.ball_rad*2)
        self.xspeed=4
        self.yspeed=-4
        self.maxspeed=5
        self.gameover=0


wall=wall()
wall.create_wall()
paddle=paddle()
ball=g_ball(paddle.x+(paddle.width//2),paddle.y-paddle.height)


run=True
while run:
    clock.tick(fps)
    screen.fill(bg)
    wall.draw_wall()
    paddle.draw()
    ball.draw()
    if(live_ball):
        paddle.move()
        gameover=ball.move()
        if(gameover==0):
            status=1
        if(gameover!=0):
            live_ball=False
        if(gameover==-1 and life==0):
            Tk().wm_withdraw()
            res=messagebox.askquestion('you loose', 'do you want to continue ?')
            if(res=="yes"):
                life=2
                status=0
            if(res=="no"):
                run=False
        elif(gameover==-1 and life>0):
            life-=1
            root=Tk()
            root.withdraw()
            root.after(2500, root.destroy)
            st='number of lives remaining '+str(life+1)
            messagebox.showwarning('current lives', st, master=root)


        if(gameover==1):
            Tk().wm_withdraw()
            res=messagebox.askquestion('you won', 'do you want to play again ?')
            if(res=="yes"):
                life=2
                status=0
            if(res=="no"):
                run=False
    for event in pygame.event.get():
        key1=pygame.key.get_pressed()
        if(event.type==pygame.QUIT):
            run=False
        elif(key1[pygame.K_p]):
            pause()
        
        key=pygame.key.get_pressed()
        if((key[pygame.K_LEFT] or key[pygame.K_RIGHT]) and live_ball==False):
            if(status==1):
                live_ball=True
                ball.reset(paddle.x+(paddle.width//2),paddle.y-paddle.height)
                paddle.reset()
            elif(status==0):
                live_ball=True
                ball.reset(paddle.x+(paddle.width//2),paddle.y-paddle.height)
                paddle.reset()
                wall.create_wall()
                status=1
             

    pygame.display.update()
pygame.quit()