import pygame
import random
import math
from pygame import mixer
#intialize pygame
pygame.init()
#creating screen
screen=pygame.display.set_mode((800,600))
#Title and Icon
pygame.display.set_caption("Space War")
icon=pygame.image.load('./images/solar-system.png')
#Background
b_ground=pygame.image.load('./images/5532919.png')
mixer.music.load('./audio/background.wav')
mixer.music.play(-1)

pygame.display.set_icon(icon)
#player image
player_img=pygame.image.load('./images/space.png')
playerX=370
playerY=480
playerX_change=0.7
#Enemy Image
enemy_img=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
for i in range(6):
    enemy_img.append(pygame.image.load('./images/alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0,150))
    enemyX_change.append(10)
    enemyY_change.append(15)


#bullet
bull_img=pygame.image.load('./images/bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=1.5
bullet_state="ready"
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10
over_font=pygame.font.Font('freesansbold.ttf',64)
def show_score(x,y):
    score=font.render("Score :" + str(score_value),True,(255,255,255))
    screen.blit(score, (x,y))
def game_over_text():
    over_text=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))

def fire_bullet(x,y):
     global bullet_state
     bullet_state="fire"
     screen.blit(bull_img,(x+16,y+10))

def player(x,y):
    screen.blit(player_img,(x,y))
def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))

def iscollision(x,x1,y,y1):
    coll=math.sqrt(math.pow((x-x1),2)+math.pow((y-y1),2))
    if coll<27:
        return True
    else:
        return False


#Game Loop
running =True
while running:
    # background image
    screen.fill((0, 0, 0))
    screen.blit(b_ground, (0, 0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    #key press
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-0.7
            if event.key==pygame.K_RIGHT:
                playerX_change=0.7
            if event.key==pygame.K_SPACE:
                 if bullet_state=="ready":
                  bullet_sound=mixer.Sound('./audio/laser.wav')
                  bullet_sound.play()
                  bulletX=playerX
                  fire_bullet(bulletX,bulletY)
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0



    #standard for RGB
    playerX+=playerX_change


    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736

    for i in range(6):
    #    print("cc")
       if enemyY[i]>440:
           for j in range(6):
               enemyY[j]=2000
               
           game_over_text()  
           break
       enemyX[i] += enemyX_change[i]
       if enemyX[i] <= 0:
           enemyX_change[i] = 0.5
           enemyY[i] += enemyY_change[i]
       elif enemyX[i] >= 736:
           enemyX_change[i] = -0.5
           enemyY[i] += enemyY_change[i]
       koll = iscollision(bulletX, enemyX[i], bulletY, enemyY[i])
       if koll:
           explosion_sound=mixer.Sound('./audio/explosion.wav')
           explosion_sound.play()
           bulletY = 480
           bullet_state = "ready"
           score_value += 1
           print(score_value)
           enemyX[i] = random.randint(0, 735)
           enemyY[i] = random.randint(50, 150)
       enemy(enemyX[i],enemyY[i],i)   



    if bulletY <= 0:
       bullet_state = "ready"
       bulletY = 480
   

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    player(playerX, playerY)
    
      


    show_score(textX,textY)
    pygame.display.update()
