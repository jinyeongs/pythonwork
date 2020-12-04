
import pygame
import random
from time import sleep

#나비 클래스
class Butterfly :
    images = [] #색이 다른 나비이미지들
    sounds=[] #미사일에 맞았을때 나오는 소리들
    x=0 #나비의 x좌표
    y=0 #나비의 y좌표
    life=3 #나비의 체력
    isShot = False; #미사일에 맞았는지 안맞았는지
    def __init__(self,x,y,images,sounds): #나비클래스의 생성자
        self.x = x #나비의 초기 x,y좌표를 입력받는다
        self.y = y
        self.image = images #나비가 변할 이미지를 저장
        self.sounds = sounds #나비가 미사일에 맞았을 때 바뀔 사운드를 저장



BLACK = (0, 0, 0) #검은색 rgb값
padWidth = 480 #게임판 너비
padHeight = 640 #게임판 높이

pygame.init()
gamePad = pygame.display.set_mode((padWidth, padHeight))
pygame.display.set_caption('PyShooting')
background = pygame.image.load('background.png') #게임판(배경)의 이미지를 파일로 부터 불러오기
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

def drawObject(obj, x, y): # 오브젝트를 게임판에 그려주는 함수
    global gamePad
    gamePad.blit(obj, (x, y))

def writeScore(count): # 게임판에 텍스트(글자)를 그려 준다
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('파괴한 수: ' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))

def writePassed(count): # 놓친 운석 수를 게임판에 그려준다
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('놓친 수: ' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (340, 0))

def writeMessage(text): # 전투기 파괴 또는 운석을 놓쳐서 게임이 종료될 경우 메시지 출력
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

def crash(): #전투기 파괴 시키는 함수
    global gamePad
    writeMessage('전투기 파괴!')

def gameOver(): #게임을 종료 시키는 함수
    global gamePad
    writeMessage('게임 오버!')

fighterSize = fighter.get_rect().size
fighterWidth = fighterSize[0]
fighterHeight = fighterSize[1]
butterflySize = butterfly_red.get_rect().size #나비의 크기를 (width,heigt)
butterflyWidth = butterflySize[0] # 나비의 너비
butterflyHeight = butterflySize[1] #나비의 높이
butterflyX = random.randrange(0, padWidth-butterflyWidth) #나비의 초기 x좌표 (0~width사이의 값에서 랜덤생성)
butterflyY = 0 # 나비의 초기 Y좌표 화면 맨 위에서 생성 맨위왼쪽(0,0) 맨위오른쪽(0,480) 맨아래왼쪽(640,0)맨아래오른쪽(640,480)
# 나비를 생성한다
#Butterfly( 초기X좌표 , 초기Y좌표 , 나비이미지의 리스트, 나비의 사운드 리스트 )
butterfly = Butterfly(butterflyX,butterflyY,[butterfly_red,butterfly_yellow,butterfly_blue], [butterfly_scream_cat,butterfly_scream_zombie,butterfly_scream_fox])
#나비의 속도
butterflySpeed =2

x = padWidth *0.45
y = padHeight * 0.9
fighterX = 0

missileXY = []
butterflyXY =[] # 여러개 생성된 나비들을 가지고 있을 리스트
butterflyXY.append(butterfly) #생성한 나비를 나비리스트에 넣는다
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
bfTime=0 #나비가 최근 생성된 시간

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
    # 나비리스트에 있는 나비들이 비행기와 충돌했는지 체크하고 충돌처리를 한다
    for bf in butterflyXY:
        if y< bf.y + butterflyHeight : # y : 비행기의 y좌표   /  bf : 나비리스트에 있는 하나의 나비
            if(bf.x > x and bf.x < x + fighterWidth) or (bf.x+butterflyWidth > x and bf.x + butterflyWidth < x + butterflyWidth) :
                crash()

    drawObject(fighter, x, y)

    if len(missileXY) != 0:
        for i, bxy in enumerate(missileXY): #missileXY : 미사일들이 들어있는 리스트 / i 미사일하나의 인덱스
            bxy[1] -= 10 # bxy : 미사일 하나의 x,y를 둘다 가지고 있음
            missileXY[i][1] = bxy[1]

            if bxy[1] < rockY:
                if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                    missileXY.remove(bxy)
                    isShot = True
                    shotCount += 1
                    continue
            for bf in butterflyXY : #나비들이 미사일에 맞았는지 체크한다
                if bxy[1] < bf.y:
                    if bxy[0] > bf.x and bxy[0] < bf.x + butterflyWidth:
                        missileXY.remove(bxy) # 미사일이 나비에 맞았으면 미사일을 제거
                        bf.isShot = True #나비의 맞았는지 안맞았는지의 상태를 변경

            if bxy[1] <= 0:
                try:
                    missileXY.remove(bxy)
                except:
                    pass

    if len(missileXY) != 0:
        for bx, by in missileXY:
            drawObject(missile, bx, by)

    writeScore(shotCount)
    #나비들을 아래로 떨어뜨린다(speed만큼 y좌표를 증가시킨다)
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
        if bf.y > padHeight: #나비가 화면 밖으로 나갔으면 제거 / padHeight : 게임판의 높이
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
    #미사일에 맞은 나비가 있는지 확인
    for bf in butterflyXY :
        if bf.isShot: #미사일에 맞은 나비인 경우
            bf.life -= 1 #나비의 라이프를 -1
            bf.sounds[bf.life].play() #나비 사운드의 n번째 소리를 재생
            if bf.life <=0 : #나비의 라이프가 0이하인경우 폭발처리
                drawObject(explosion, bf.x, bf.y) #폭발이미지를 나비의 좌표에 그려준다
                butterflyXY.remove(bf) #나비를 제거

                shotCount += 1
            bf.isShot = False #다시 안맞은 상태로 돌려놓는다
            butterflySpeed += 0.02 #나비 한마리가 죽을때 마다 나비들의 속도를 올려준다
            if butterflySpeed >= 10: # 나비의 최대 속도 제한
                butterflySpeed = 10
    #나비가 3초 주기로 나오게 한다
    #bfTime : 게임이 시작되고 나비가 최근에 생성된 시간
    second = pygame.time.get_ticks() /1000 # second : 게임이 시작되고 경과한 시간(초)
    if second -bfTime >3 : #나비가 생성되고 3초가 지나면 새로운 나비를 생성
        bfTime = second #최근 생성시간을 현재 경과시간으로 바꾼다
        butterflyX = random.randrange(0, padWidth - butterflyWidth)
        butterflyY = 0
        butterfly = Butterfly(butterflyX, butterflyY, [butterfly_red, butterfly_yellow, butterfly_blue],
                              [butterfly_scream_cat, butterfly_scream_zombie, butterfly_scream_fox])
        butterflyXY.append(butterfly)

    drawObject(rock, rockX, rockY)
    #나비들을 게임판에 그려준다
    for bf in butterflyXY:
        drawObject(bf.image[bf.life-1], bf.x, bf.y) #각 나비의 life에 따라 다른 색상으로 나비를 출력 인덱스 범위 0~2
    pygame.display.update()

    clock.tick(60) #게임진행속도

pygame.quit()