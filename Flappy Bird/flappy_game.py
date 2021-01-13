import random
import sys
import pygame
from pygame.locals import *

#GOLBAL VARIABLES
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GAME_SPRITES = {}
GAME_SOUNDS = {}
BASE_Y = SCREENHEIGHT*0.8  # BASE with start from this height
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'


def showWelcomeScreen():


    playerx = SCREENWIDTH/5
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.15)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key ==K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['base'],(basex,BASE_Y))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def showMainGame():
    score =0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex = 0

    #creating pipes
    newPipe1 = getPipes()
    newPipe2 = getPipes()

    upperPipes = [
        {'x':SCREENWIDTH+200,'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+200+SCREENWIDTH/2,'y':newPipe2[0]['y']}
    ]

    lowerPipes = [
        {'x':SCREENWIDTH+200,'y':newPipe1[1]['y']},
        {'x':SCREENWIDTH+200+SCREENWIDTH/2,'y':newPipe2[1]['y']}
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccV = 1
    playerFlapAccv = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or(event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery>0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
        
        crashTest = isCollide(playerx,playery,upperPipes,lowerPipes)

        if crashTest:
            return

        #checking score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos< pipeMidPos+4:
                score+=1
                GAME_SOUNDS['point'].play()
        
        if playerVelY<playerMaxVelY and not playerFlapped:
            playerVelY += playerAccV

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY,BASE_Y-playerHeight-playery)

        #moving pipes to left
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX
        
        if 0<upperPipes[0]['x']<5:
            newPipe = getPipes()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        #removing pipes when out of vision
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # here comes the real game
        SCREEN.blit(GAME_SPRITES['background'],(0,0))

        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'],(basex,BASE_Y))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
        
        
        digits = [int(x) for x in str(score)]
        width = 0
        for digit in digits:
            width += GAME_SPRITES['numbers'][digit].get_width()

        xoffset = (SCREENWIDTH-width)/2
        
        for digit in digits:
            digitPic = GAME_SPRITES['numbers'][digit]
            SCREEN.blit(digitPic,(xoffset,SCREENHEIGHT*0.12))
            xoffset += digitPic.get_width()
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)



def isCollide(playerx,playery,upperPipes,lowerPipes):
    #when player hits ground or top 
    if playery > BASE_Y - 25 or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if playery< pipeHeight+ pipe['y'] and abs(playerx-pipe['x'])<GAME_SPRITES['pipe'][0].get_width():
             GAME_SOUNDS['hit'].play()
             return True

    for pipe in lowerPipes:
        if playery + GAME_SPRITES['player'].get_height()>pipe['y'] and abs(playerx-pipe['x'])<GAME_SPRITES['pipe'][0].get_width():
             GAME_SOUNDS['hit'].play()
             return True


    return False      


def getPipes():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height()- 1.2*offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset

    pipe = [{'x':pipex,'y':-y1},{'x':pipex,'y':y2}]
    return pipe

        




if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock() # fps clock is a limiter for fps
    pygame.display.set_caption("Flappy Bird By Pravesh")
    
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
        
    )

    GAME_SPRITES['message'] =  pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] =  pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['background'] =  pygame.image.load(BACKGROUND).convert_alpha()
    GAME_SPRITES['player'] =  pygame.image.load(PLAYER).convert_alpha()

    GAME_SPRITES['pipe'] =  (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
    pygame.image.load(PIPE).convert_alpha())


    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')

    while True:
        showWelcomeScreen()
        showMainGame()
