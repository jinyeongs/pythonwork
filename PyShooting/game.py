# 테스트입니다.

import pygame
import random
from time import sleep

class Butterfly :
    images = []
    sounds=[]
    x=0
    y=0
    life=3
    isShot = False;
    def __init__(self,x,y,images,sounds):
        self.x = x
        self.y = y
        self.image = images
        self.sounds = sounds



BLACK = (0, 0, 0) #검은색 rgb값
padWidth = 480 #게임판 너비
padHeight = 640 #게임판 높이

pygame.init()
gamePad = pygame.display.set_mode((padWidth, padHeight))
pygame.display.set_caption('PyShooting')
background = pygame.image.load('background.png')
fighter =  pygame.image.load('fighter.png')
missile = pygame.image.load('missile.png')
explosion = pygame.image.load('explosion.png')
butterfly_red = pygame.image.load('n1.png')
butterfly_yellow= pygame.image.load('n2.png')
butterfly_blue =pygame.image.load('n3.png')
butterfly_scream_cat = pygame.mixer.Sound('cat_scream.wav')
butterfly_scream_zombie = pygame.mixer.Sound('zombie_scream.wav')
butterfly_scream_fox = pygame.mixer.Sound('fox_scream.wav')
pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1)
missileSound = pygame.mixer.Sound('missile.wav')
gameOverSound = pygame.mixer.Sound('gameover.wav')
clock = pygame.time.Clock()
# pygame.time.set_timer()

rockImage = ['rock01.png', 'rock02.png', 'rock03.png', 'rock04.png', 'rock05.png',
             'rock06.png', 'rock07.png', 'rock08.png', 'rock09.png', 'rock10.png',
             'rock11.png', 'rock12.png', 'rock13.png', 'rock14.png', 'rock15.png',
             'rock16.png', 'rock17.png', 'rock18.png', 'rock19.png', 'rock20.png',
             'rock21.png', 'rock22.png', 'rock23.png', 'rock24.png', 'rock25.png',
             'rock26.png', 'rock27.png', 'rock28.png', 'rock29.png', 'rock30.png']
explosionSound = ['explosion01.wav', 'explosion02.wav', 'explosion03.wav', 'explosion04.wav']

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

def writeScore(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('파괴한 수: ' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))

def writePassed(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('놓친 수: ' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (340, 0))

def writeMessage(text):
    textfont = pygame.font.Font('NanumGothic.ttf', 80)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameOverSound.play()
    sleep(2)
    pygame.mixer.music.play(-1)

def crash():
    global gamePad
    writeMessage('전투기 파괴!')

def gameOver():
    global gamePad
    writeMessage('게임 오버!')

fighterSize = fighter.get_rect().size
fighterWidth = fighterSize[0]
fighterHeight = fighterSize[1]
butterflySize = butterfly_red.get_rect().size
butterflyWidth = butterflySize[0]
butterflyHeight = butterflySize[1]
butterflyX = random.randrange(0, padWidth-butterflyWidth)
butterflyY = 0
butterfly = Butterfly(butterflyX,butterflyY,[butterfly_red,butterfly_yellow,butterfly_blue], [butterfly_scream_cat,butterfly_scream_zombie,butterfly_scream_fox])
butterflySpeed =2

x = padWidth *0.45
y = padHeight * 0.9
fighterX = 0

missileXY = []
butterflyXY =[]
butterflyXY.append(butterfly)
rock = pygame.image.load(random.choice(rockImage))
rockSize = rock.get_rect().size
rockWidth = rockSize[0]
rockHeight = rockSize[1]
destroySound = pygame.mixer.Sound(random.choice(explosionSound))
marginLR = int(fighterWidth/2)
rockX = random.randrange(marginLR, padWidth - rockWidth - marginLR)
rockY = 0
rockSpeed = 2

isShot = False
shotCount = 0
rockPassed = 0
bfTime=0

while True:
    #gamePad.fill(BLACK)
    drawObject(background, 0, 0)

    event = pygame.event.poll()
    if event.type in [pygame.QUIT]:
        break

    if event.type in [pygame.KEYDOWN]:
        if event.key == pygame.K_LEFT:
            fighterX -= 5
        elif event.key == pygame.K_RIGHT:
            fighterX += 5
        elif event.key == pygame.K_SPACE:
            missileSound.play()
            missileX = x + fighterWidth/2
            missileY = y - fighterHeight
            missileXY.append([missileX, missileY])

    if event.type in [pygame.KEYUP]:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            fighterX = 0

    x += fighterX
    if x < 0:
        x = 0
    elif x > padWidth - fighterWidth:
        x = padWidth - fighterWidth

    if y < rockY + rockHeight:
        if (rockX > x and rockX < x + fighterWidth) or \
        (rockX + rockWidth > x  and rockX + rockWidth < x + fighterWidth):
            crash()
    for bf in butterflyXY:
        if y< bf.y + butterflyHeight :
            if(bf.x > x and bf.x < x + fighterWidth) or (bf.x+butterflyWidth > x and bf.x + butterflyWidth < x + butterflyWidth) :
                crash()

    drawObject(fighter, x, y)

    if len(missileXY) != 0:
        for i, bxy in enumerate(missileXY):
            bxy[1] -= 10
            missileXY[i][1] = bxy[1]

            if bxy[1] < rockY:
                if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                    missileXY.remove(bxy)
                    isShot = True
                    shotCount += 1
            for bf in butterflyXY :
                if bxy[1] < bf.y:
                    if bxy[0] > bf.x and bxy[0] < bf.x + butterflyWidth:
                        missileXY.remove(bxy)
                        bf.isShot = True

            if bxy[1] <= 0:
                try:
                    missileXY.remove(bxy)
                except:
                    pass

    if len(missileXY) != 0:
        for bx, by in missileXY:
            drawObject(missile, bx, by)

    writeScore(shotCount)
    for bf in butterflyXY :
        bf.y += butterflySpeed
    rockY += rockSpeed

    if rockY > padHeight:
        rock = pygame.image.load(random.choice(rockImage))
        rockSize = rock.get_rect().size
        rockWidth = rockSize[0]
        rockHeight = rockSize[1]
        rockX = random.randrange(marginLR, padWidth - rockWidth - marginLR)
        rockY = 0
        rockPassed += 1
    for bf in butterflyXY:
        if bf.y > padHeight:
            butterflyXY.remove(bf)

    if rockPassed == 3:
        gameOver()

    writePassed(rockPassed)

    if isShot:
        drawObject(explosion, rockX, rockY)
        destroySound.play()

        rock = pygame.image.load(random.choice(rockImage))
        rockSize = rock.get_rect().size
        rockWidth = rockSize[0]
        rockHeight = rockSize[1]
        rockX = random.randrange(marginLR, padWidth - rockWidth - marginLR)
        rockY = 0
        destroySound = pygame.mixer.Sound(random.choice(explosionSound))
        isShot = False

        rockSpeed += 0.02
        if rockSpeed >= 10:
            rockSpeed = 10
    for bf in butterflyXY :
        if bf.isShot:
            bf.life -= 1
            bf.sounds[bf.life].play()
            if bf.life <=0 :
                drawObject(explosion, bf.x, bf.y)
                butterflyXY.remove(bf)

                shotCount += 1
            bf.isShot = False
            butterflySpeed += 0.02
            if butterflySpeed >= 10:
                butterflySpeed = 10

    second = pygame.time.get_ticks() /1000
    if second -bfTime >3 :
        bfTime = second
        butterflyX = random.randrange(0, padWidth - butterflyWidth)
        butterflyY = 0
        butterfly = Butterfly(butterflyX, butterflyY, [butterfly_red, butterfly_yellow, butterfly_blue],
                              [butterfly_scream_cat, butterfly_scream_zombie, butterfly_scream_fox])
        butterflyXY.append(butterfly)

    drawObject(rock, rockX, rockY)
    for bf in butterflyXY:
        drawObject(bf.image[bf.life-1], bf.x, bf.y)
    pygame.display.update()

    clock.tick(60) #게임진행속도

pygame.quit()